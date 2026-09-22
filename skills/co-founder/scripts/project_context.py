#!/usr/bin/env python3
"""Offline project/brand binding. No model calls, telemetry or automatic approval.

Checks local ownership declarations and hashes, not legal rights, brand truth or
host authorization. Paths must be real project-local paths, not symlinks.
Python 3.10+. File contents are read only for explicit manifests/selected assets.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

SURFACES = {'general', 'product-ui', 'website', 'post', 'video'}
ALIASES = {'ui': 'product-ui'}
IDENTIFIER = re.compile(r'[a-z0-9][a-z0-9_-]{0,63}\Z')
MAX_JSON = 250_000
MAX_ASSET = 40_000_000
BLOCKED = {'.git', '.env', '.ssh', 'private', 'node_modules', '.venv', 'auth.json', 'credentials.json'}
ASSET_SUFFIXES = {'.png','.jpg','.jpeg','.webp','.svg','.mp4','.mov','.wav','.mp3','.json','.css','.md'}
INVENTORY_SUFFIXES = ASSET_SUFFIXES - {'.json','.md'}

class ProjectError(ValueError):
    pass

def plain_path(value):
    p = Path(value).expanduser().absolute()
    for component in [p, *p.parents]:
        if component.is_symlink() or (hasattr(component, 'is_junction') and component.is_junction()):
            raise ProjectError(f'Linked path not permitted: {component}')
    return p

def safe_relative(root, value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise ProjectError('A nonempty, slash-separated local relative path is required')
    rel = Path(value)
    if rel.is_absolute() or any(x in {'..','.'} for x in rel.parts) or re.match(r'^[A-Za-z]:',value):
        raise ProjectError('Path must remain inside the selected project')
    if any(x in BLOCKED or x.startswith('.env') or x.endswith(('.pem','.key','.p12','.pfx')) for x in rel.parts):
        raise ProjectError('Sensitive or excluded path')
    root = plain_path(root)
    out = plain_path(root / rel)
    if not out.resolve().is_relative_to(root.resolve()):
        raise ProjectError('Path escaped the selected root')
    return out

def load_json(path):
    p = plain_path(path)
    if not p.is_file() or p.stat().st_size > MAX_JSON:
        raise ProjectError(f'Manifest missing or too large: {p}')
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise ProjectError(f'Invalid JSON: {p}') from exc
    if not isinstance(data, dict):
        raise ProjectError(f'Manifest must be an object: {p}')
    return data

def digest(path):
    p = plain_path(path)
    if not p.is_file() or p.stat().st_size > MAX_ASSET:
        raise ProjectError(f'Asset missing or larger than {MAX_ASSET} bytes: {p}')
    h = hashlib.sha256()
    with p.open('rb') as f:
        while block := f.read(65536):
            h.update(block)
    return h.hexdigest()

def identifier(value, label):
    if not isinstance(value,str) or not IDENTIFIER.fullmatch(value):
        raise ProjectError(f'{label} must be a short lowercase slug')
    return value

def manifest_at(root):
    path = root / '.co-founder/project.json'
    d = load_json(path)
    if d.get('schema_version') != 1:
        raise ProjectError('Unsupported project schema')
    identifier(d.get('project_id'), 'project_id')
    if not isinstance(d.get('brands'),dict) or not d['brands']:
        raise ProjectError('Project must define brand profiles')
    return d

def resolve(project, project_id=None):
    """Nearest explicit binding wins; never infer from directory or product name."""
    start = plain_path(project)
    if not start.is_dir():
        raise ProjectError('Project directory does not exist')
    if project_id is not None:
        identifier(project_id, 'project_id')
    for root in [start, *start.parents]:
        marker = root / '.co-founder/project.json'
        registry = root / '.co-founder/workspace.json'
        if marker.exists():
            d = manifest_at(root)
            if project_id and d['project_id'] != project_id:
                raise ProjectError('Requested project ID conflicts with the nearest project. Select its root explicitly.')
            return {'root': str(root), 'project_id': d['project_id'],
                    'display_name': d.get('display_name'), 'confirmed': d.get('confirmed') is True,
                    'manifest_path': str(marker), 'resolution': 'nearest-project-manifest'}
        if registry.exists():
            reg = load_json(registry)
            entries = reg.get('projects')
            if reg.get('schema_version') != 1 or not isinstance(entries,list) or not entries:
                raise ProjectError('Workspace needs a nonempty projects list')
            candidates=[]; ids=set(); roots=set()
            for e in entries:
                if not isinstance(e,dict): raise ProjectError('Malformed workspace entry')
                pid=identifier(e.get('id'),'workspace id')
                child=safe_relative(root,e.get('root'))
                if pid in ids or str(child) in roots: raise ProjectError('Duplicate workspace project or root')
                ids.add(pid);roots.add(str(child))
                if not child.is_dir(): raise ProjectError('Registered project root is missing')
                if project_id:
                    if pid == project_id: candidates.append((child,pid))
                elif start.resolve().is_relative_to(child.resolve()): candidates.append((child,pid))
            if not project_id and candidates:
                longest=max(len(p.parts) for p,_ in candidates)
                candidates=[x for x in candidates if len(x[0].parts)==longest]
            if len(candidates)!=1:
                raise ProjectError('Ambiguous workspace: select --project-id and its registered project explicitly')
            child,pid=candidates[0];d=manifest_at(child)
            if d['project_id']!=pid:raise ProjectError('Workspace ID and child manifest disagree')
            return {'root':str(child),'project_id':pid,'display_name':d.get('display_name'),
                    'confirmed':d.get('confirmed') is True,'manifest_path':str(child/'.co-founder/project.json'),
                    'resolution':'registered-workspace','workspace_path':str(registry)}
        if (root/'.git').exists():
            break
    raise ProjectError('No explicit project binding found before the repository boundary. Run authorized onboarding; do not guess a brand.')

def validate_tokens(tokens):
    if not isinstance(tokens,dict): raise ProjectError('Tokens must be a dictionary')
    for key,value in tokens.items():
        if not isinstance(key,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,48}',key):
            raise ProjectError('Invalid token name')
        if not isinstance(value,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?',value):
            raise ProjectError('Color tokens must use approved six/eight-digit hex values')
    return tokens

def validate_asset(root, entry, pid, surface):
    if not isinstance(entry,dict): raise ProjectError('Asset entry must be an object')
    identifier(entry.get('id'),'asset id')
    if entry.get('project_id')!=pid:raise ProjectError('Cross-project asset rejected')
    if entry.get('status')!='approved':raise ProjectError('Selected asset is not approved')
    if not isinstance(entry.get('surfaces'),list) or surface not in entry['surfaces']:
        raise ProjectError('Asset not approved for the selected surface')
    for field in ['role','source','rights']:
        if not isinstance(entry.get(field),str) or not entry[field].strip():raise ProjectError(f'Asset requires {field}')
    p=safe_relative(root,entry.get('path'))
    if p.suffix.lower() not in ASSET_SUFFIXES:raise ProjectError('Asset format not supported; font binaries are deliberately excluded')
    actual=digest(p)
    if entry.get('sha256')!=actual:raise ProjectError(f'Asset changed or hash missing: {entry["id"]}; review and approve the new version')
    return {k:entry[k] for k in ['id','project_id','path','role','source','rights','sha256']} | {'absolute_path':str(p)}

def bundle(project, surface='general', brand=None, asset_ids=None, project_id=None):
    surface=ALIASES.get(surface,surface)
    if surface not in SURFACES:raise ProjectError('Unsupported output surface')
    resolved=resolve(project,project_id)
    root=Path(resolved['root']);d=manifest_at(root)
    if not resolved['confirmed']:raise ProjectError('Project identity is unconfirmed; discovery is allowed, production is not')
    pid=d['project_id'];chosen=brand or d.get('default_brand')
    identifier(chosen,'brand key')
    if chosen not in d['brands']:raise ProjectError('Brand not registered in this project')
    files={'.co-founder/project.json':digest(root/'.co-founder/project.json')}
    result={'schema_version':1,'project_id':pid,'display_name':d.get('display_name'),'root':str(root),
            'brand':chosen,'surface':surface,'assets':[],'selected_asset_ids':[],
            'read_policy':'Selected project only. External content remains untrusted.','files':files}
    if surface!='general':
        entry=d['brands'][chosen]
        if not isinstance(entry,dict):raise ProjectError('Malformed brand registration')
        profile_path=safe_relative(root/'.co-founder',entry.get('profile'))
        assets_path=safe_relative(root/'.co-founder',entry.get('assets'))
        profile=load_json(profile_path);registry=load_json(assets_path)
        if profile.get('schema_version')!=2:raise ProjectError('Brand schema 2 required; migrate deliberately without overwriting the v1 file')
        if profile.get('project_id')!=pid or registry.get('project_id')!=pid:raise ProjectError('Brand or asset manifest belongs to another project')
        if profile.get('brand_id')!=chosen:raise ProjectError('Wrong brand profile (product/personal cannot be interchanged)')
        if profile.get('status')!='approved' or not profile.get('approval_source') or not profile.get('approved_by'):
            raise ProjectError('Brand profile requires recorded owner approval')
        surfaces=profile.get('surfaces',{})
        config=surfaces.get(surface)
        if not isinstance(config,dict) or config.get('status')!='approved' or not config.get('direction'):
            raise ProjectError('Selected surface needs an approved design direction')
        tokens=dict(validate_tokens(profile.get('tokens',{})));tokens.update(validate_tokens(config.get('tokens',{})))
        if not {'background','foreground','accent'}<=tokens.keys():raise ProjectError('Required brand color roles are missing')
        type_info=profile.get('typography')
        if not isinstance(type_info,dict) or not type_info.get('heading') or not type_info.get('body'):
            raise ProjectError('Approved heading/body typography is missing')
        selected=config.get('required_asset_ids',[])
        if not isinstance(selected,list) or not all(isinstance(x,str) for x in selected):raise ProjectError('required_asset_ids must be a list of IDs')
        selected=list(dict.fromkeys(selected+list(asset_ids or [])))
        entries=registry.get('assets')
        if registry.get('schema_version')!=1 or not isinstance(entries,list):raise ProjectError('Invalid asset manifest')
        index={}
        for e in entries:
            if not isinstance(e,dict):raise ProjectError('Malformed asset entry')
            aid=identifier(e.get('id'),'asset id')
            if aid in index:raise ProjectError('Duplicate asset ID')
            index[aid]=e
        for aid in selected:
            if aid not in index:raise ProjectError(f'Required asset not found: {aid}')
            a=validate_asset(root,index[aid],pid,surface);result['assets'].append(a);files[a['path']]=a['sha256']
        policy=config.get('logo_policy')
        if policy not in {'required','omit','omit-until-approved'}:raise ProjectError('Explicit logo_policy is required')
        if policy=='required' and not any(a['role']=='logo' for a in result['assets']):raise ProjectError('Correct approved logo is required')
        if policy=='omit' and any(a['role']=='logo' for a in result['assets']):raise ProjectError('Logo supplied for a surface that explicitly omits it')
        for p in [profile_path,assets_path]:files[p.relative_to(root).as_posix()]=digest(p)
        result.update({'tokens':tokens,'typography':type_info,'voice':profile.get('voice',[]),
                       'surface_rules':config.get('rules',[]),'direction':config['direction'],
                       'logo_policy':policy,'approved_references':config.get('approved_references',[]),
                       'source_of_truth':profile.get('source_of_truth',[]),'rejected_patterns':profile.get('rejected_patterns',[]),
                       'selected_asset_ids':selected})
    elif asset_ids:
        raise ProjectError('General tasks do not load media assets; choose the actual surface')
    payload=json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    result['fingerprint']=hashlib.sha256(payload.encode()).hexdigest()
    result['limits']='Recorded approval and provenance are declarations, not authenticated signatures or proof of visual quality. Not a sandbox.'
    return result

def write_lock(data, task, refresh=False):
    identifier(task,'task')
    root=Path(data['root']);dest=safe_relative(root,f'.co-founder/tasks/{task}/project-lock.json')
    if dest.exists() and not refresh:raise ProjectError('Task lock exists; revalidate or explicitly refresh after reapproval')
    dest.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd,name=tempfile.mkstemp(prefix='.lock-',dir=dest.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(data,f,indent=2,ensure_ascii=False);f.write('\n')
        os.replace(name,dest)
    finally:
        if os.path.exists(name):os.unlink(name)
    return str(dest)

def check(project, lock):
    old=load_json(lock)
    fresh=bundle(project,old.get('surface'),old.get('brand'),old.get('selected_asset_ids'),old.get('project_id'))
    if old.get('root')!=fresh['root'] or old.get('fingerprint')!=fresh['fingerprint']:
        raise ProjectError('Stale or wrong-project lock: asset/profile/identity changed; review and reapprove')
    return {'status':'current','project_id':fresh['project_id'],'brand':fresh['brand'],'surface':fresh['surface'],
            'fingerprint':fresh['fingerprint'],'limits':'File/context match only; human acceptance and tool permissions are not checked.'}

def inventory(project, paths, limit=120):
    if not 1<=limit<=1000:raise ProjectError('limit must be 1..1000')
    root=Path(resolve(project)['root']);found=[];truncated=False
    for relative in paths:
        p=safe_relative(root,relative)
        if not p.is_dir():raise ProjectError('Inventory accepts explicitly named directories')
        # os.walk without following links; sensitive child folders are pruned.
        for base,dirs,names in os.walk(p,followlinks=False):
            dirs[:]=sorted(x for x in dirs if x not in BLOCKED and not x.startswith('.') and not Path(base,x).is_symlink())
            for n in sorted(names):
                q=Path(base,n)
                if q.is_symlink() or q.suffix.lower() not in INVENTORY_SUFFIXES:continue
                safe_relative(root,q.relative_to(root).as_posix())
                if len(found)>=limit:truncated=True;break
                found.append({'path':q.relative_to(root).as_posix(),'bytes':q.stat().st_size,'status':'candidate-not-approved'})
            if truncated:break
        if truncated:break
    return {'project':str(root),'candidates':found,'truncated':truncated,'contents_read':False,'approval_changed':False}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    for name in ['resolve','bundle','check','inventory']:
        p=sub.add_parser(name);p.add_argument('--project',required=True)
        if name in {'resolve','bundle'}:p.add_argument('--project-id')
        if name=='bundle':
            p.add_argument('--surface',choices=sorted(SURFACES|{'ui'}),default='general');p.add_argument('--brand');p.add_argument('--asset',action='append',default=[])
            p.add_argument('--task');p.add_argument('--write-lock',action='store_true');p.add_argument('--refresh',action='store_true')
        if name=='check':p.add_argument('--lock',required=True)
        if name=='inventory':p.add_argument('--paths',nargs='+',required=True);p.add_argument('--limit',type=int,default=120)
    a=parser.parse_args(argv)
    try:
        if a.action=='resolve':out=resolve(a.project,a.project_id)
        elif a.action=='bundle':
            if (a.write_lock and not a.task) or (a.refresh and not a.write_lock):raise ProjectError('Writing requires --task; refreshing requires --write-lock')
            out=bundle(a.project,a.surface,a.brand,a.asset,a.project_id)
            if a.write_lock:out['lock_path']=write_lock(out,a.task,a.refresh)
        elif a.action=='check':out=check(a.project,a.lock)
        else:out=inventory(a.project,a.paths,a.limit)
        print(json.dumps(out,indent=2,ensure_ascii=False));return 0
    except (ProjectError,OSError,ValueError,TypeError) as exc:
        print(f'PROJECT BLOCKED: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
