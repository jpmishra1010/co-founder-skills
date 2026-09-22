#!/usr/bin/env python3
"""Local, offline context and evidence helpers. No model calls; no telemetry.

Python 3.10+. run-check executes only an explicitly approved argv and is NOT a
sandbox. Evidence gates check structure; they do not prove evidence authenticity.
"""
from __future__ import annotations
import argparse
from datetime import date, datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid

PACK = Path(__file__).resolve().parents[1]
TASKS = ['decide','feature-plan','impact-map','build-fix','verify-release','security-review','ui-polish','customer-care','growth','sales','content-studio','founder-brief']
ALIASES = {'fix':'build-fix','design':'ui-polish','promote':'content-studio','today':'founder-brief'}
CHECK_STATUSES = {'passed','failed','skipped','not-run','inconclusive'}
CONTEXT = {
 'decide':['company.md','state.json','claims.json'],
 'feature-plan':['company.md','product-map.json','claims.json'],
 'impact-map':['product-map.json'], 'build-fix':['product-map.json','policy.json'],
 'verify-release':['product-map.json','policy.json'], 'security-review':['product-map.json','policy.json'],
 'ui-polish':['company.md','brand.json','product-map.json'],
 'customer-care':['state.json','claims.json'], 'growth':['company.md','claims.json','state.json'],
 'sales':['company.md','claims.json','state.json'],
 'content-studio':['brand.json','claims.json'], 'founder-brief':['company.md','state.json'],
}
class CFError(ValueError):
    pass

def now(): return datetime.now(timezone.utc).isoformat()
def emit(obj): print(json.dumps(obj,indent=2,ensure_ascii=False))
def no_links(path: Path):
    for p in [path.absolute(),*path.absolute().parents]:
        if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()):
            raise CFError(f'Refusing linked path: {p}')
def root_path(value) -> Path:
    path=Path(value).expanduser().absolute(); no_links(path)
    if not path.is_dir(): raise CFError(f'Project directory does not exist: {path}')
    return path

def read_json(path: Path, max_bytes=2_000_000):
    no_links(path)
    if not path.is_file(): raise CFError(f'Missing JSON file: {path}')
    if path.stat().st_size>max_bytes: raise CFError(f'JSON too large: {path}')
    try: return json.loads(path.read_text(encoding='utf-8'))
    except (UnicodeError,ValueError) as exc: raise CFError(f'Invalid JSON: {path}: {exc}') from exc

def write_private(path: Path, data: str, *, exclusive=False):
    no_links(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    no_links(path.parent)
    if exclusive:
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(data)
    else:
        fd,name=tempfile.mkstemp(prefix='.cf-',dir=path.parent)
        try:
            with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(data)
            os.replace(name,path)
        finally:
            if os.path.exists(name): os.unlink(name)
    try: os.chmod(path,0o600)
    except OSError: pass

def context_dir(root: Path, must_exist=True):
    d=root/'.co-founder'; no_links(d)
    if must_exist and not d.is_dir(): raise CFError('Project context is not initialized. Run init explicitly first.')
    return d

def git(root: Path, args, *, okay=False, timeout=15):
    if shutil.which('git') is None:
        if okay: return None
        raise CFError('Git is not installed')
    env=os.environ.copy(); env['GIT_OPTIONAL_LOCKS']='0'; env['GIT_TERMINAL_PROMPT']='0'; env['GIT_PAGER']='cat'
    cmd=['git','-c','core.fsmonitor=false','-c','core.hooksPath=','-c','diff.external=', '-C',str(root),*args]
    try: r=subprocess.run(cmd,capture_output=True,timeout=timeout,env=env)
    except (OSError,subprocess.TimeoutExpired) as exc:
        if okay: return None
        raise CFError(f'Git read failed: {exc}') from exc
    if r.returncode:
        if okay: return None
        raise CFError('Git command failed: '+r.stderr.decode('utf-8','replace')[:1000])
    return r.stdout

def revision(root):
    rev=git(root,['rev-parse','--verify','HEAD'],okay=True)
    dirty=git(root,['status','--porcelain=v1','--untracked-files=normal'],okay=True)
    return {'head':rev.decode().strip() if rev else None,'dirty':bool(dirty) if dirty is not None else None}

def init_project(project):
    root=root_path(project); ctx=context_dir(root,False)
    ignore=root/'.gitignore'; no_links(ignore)
    if ignore.exists() and (not ignore.is_file() or ignore.stat().st_size>1_000_000): raise CFError('Refusing unexpected .gitignore')
    ctx.mkdir(exist_ok=True,mode=0o700)
    try: os.chmod(ctx,0o700)
    except OSError: pass
    created=[]; preserved=[]
    for name in ['company.md','product-map.json','brand.json','state.json','claims.json','policy.json','project.json','assets.json']:
        out=ctx/name; no_links(out)
        if out.exists(): preserved.append(name)
        else:
            write_private(out,(PACK/'assets/templates'/name).read_text(encoding='utf-8'),exclusive=True); created.append(name)
    for name in ['decisions','issues','evidence','drafts']:
        p=ctx/name; no_links(p); p.mkdir(exist_ok=True,mode=0o700)
    existing=ignore.read_text(encoding='utf-8') if ignore.exists() else ''
    if '/.co-founder/' not in existing.splitlines():
        # Appending preserves the previous content including comments and negation order.
        with ignore.open('a',encoding='utf-8') as f:
            if existing and not existing.endswith('\n'): f.write('\n')
            f.write('\n# Private Co-founder working context\n/.co-founder/\n')
    return {'project':str(root),'created':created,'preserved':preserved,'warning':'Ignore rules do not untrack already committed files. No secrets should be stored here. Run doctor.'}

def doctor(project):
    root=root_path(project); ctx=context_dir(root,False)
    tools={x:shutil.which(x) for x in ['git','python','node','ffmpeg','chromium','codex','claude']}
    names=['OPENAI_API_KEY','ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','CLAUDE_CODE_USE_BEDROCK','CLAUDE_CODE_USE_VERTEX','CLAUDE_CODE_USE_FOUNDRY']
    present=[n for n in names if os.environ.get(n)]
    tracked=git(root,['ls-files','--','.co-founder'],okay=True)
    # Only tracked path names are returned, never credentials/config contents.
    return {'project':str(root),'context_initialized':ctx.is_dir(),'tools':tools,
            'billing_related_environment_variable_names':present,
            'subscription_auth':'not verified; use codex login status / Claude /status in the host',
            'tracked_private_paths':tracked.decode('utf-8','replace').splitlines() if tracked else [],
            'network_tested':False,'security_audit':False,
            'warnings':['No credentials or host auth files were read.','Tool presence is not a guarantee that a browser, model, renderer or integration works.']}

def context_plan(project,task,max_bytes):
    root=root_path(project); ctx=context_dir(root)
    task=ALIASES.get(task,task)
    if task not in CONTEXT: raise CFError(f'Unknown task: {task}')
    if max_bytes<1 or max_bytes>2_000_000: raise CFError('max-bytes must be 1..2000000')
    files=[]; used=0
    for name in CONTEXT[task]:
        path=ctx/name; no_links(path)
        size=path.stat().st_size if path.is_file() else None
        action='missing' if size is None else 'read-scoped-excerpt' if used+size>max_bytes else 'read-when-relevant'
        if action=='read-when-relevant': used+=size
        files.append({'path':f'.co-founder/{name}','bytes':size,'suggestion':action})
    return {'task':task,'project_binding':'Resolve project_context.py before acting; this function is a size-only reading plan.','files':files,'full_file_bytes_within_budget':used,'byte_budget':max_bytes,
            'contents_returned':False,'token_estimate':None,'note':'Byte size is not model-token usage. This is a reading plan, not enforced model context control.'}

def validate_map(data):
    if not isinstance(data,dict) or not isinstance(data.get('modules'),list) or not isinstance(data.get('relationships',[]),list): raise CFError('Map needs modules and relationships lists')
    mods=data['modules']; ids=[]
    for m in mods:
        if not isinstance(m,dict) or not isinstance(m.get('id'),str) or not m['id'] or not isinstance(m.get('paths'),list): raise CFError('Each module needs id and paths')
        if not all(isinstance(p,str) and p and not p.startswith(('/','../')) for p in m['paths']): raise CFError('Invalid module path rule')
        ids.append(m['id'])
    if len(ids)!=len(set(ids)): raise CFError('Duplicate module IDs')
    for r in data.get('relationships',[]):
        if not isinstance(r,dict) or r.get('from') not in ids or r.get('to') not in ids: raise CFError('Unknown relationship module')
    return mods,data.get('relationships',[])

def path_sensitive(path):
    parts=Path(path).parts
    return any(x in {'.co-founder','.git','private','node_modules','.venv'} for x in parts) or any(x=='.env' or x.startswith('.env.') or x in {'id_rsa','id_ed25519','auth.json','credentials.json'} or x.endswith(('.pem','.key')) for x in parts)

def impact(project,base,map_path=None,max_paths=500):
    root=root_path(project)
    if not base or base.startswith('-') or len(base)>200: raise CFError('Invalid base revision')
    commit=git(root,['rev-parse','--verify',f'{base}^{{commit}}']).decode().strip()
    changed=git(root,['diff','--no-ext-diff','--no-textconv','--name-only','-z',commit,'--']).split(b'\0')
    untracked=git(root,['ls-files','--others','--exclude-standard','-z']).split(b'\0')
    raw=sorted({x.decode('utf-8','replace') for x in changed+untracked if x})
    excluded=sum(path_sensitive(x) for x in raw); visible=[x for x in raw if not path_sensitive(x)]
    paths=visible[:max_paths]
    p=Path(map_path).expanduser().absolute() if map_path else root/'.co-founder/product-map.json'
    if p.exists(): data=read_json(p); mods,rels=validate_map(data)
    else: mods=[]; rels=[]
    hits={m['id']:[p for p in paths if any(fnmatch.fnmatchcase(p,pat) for pat in m['paths'])] for m in mods}
    direct={k for k,v in hits.items() if v}; affected=set(direct)
    while True:
        expanded=affected|{r['to'] for r in rels if r['from'] in affected}|{r['from'] for r in rels if r['to'] in affected}
        if expanded==affected: break
        affected=expanded
    mapped={p for xs in hits.values() for p in xs}
    return {'base_revision':commit,'candidate':revision(root),'changed_paths':paths,'excluded_sensitive_path_count':excluded,
            'truncated':len(visible)>max_paths,'direct_modules':sorted(direct),'related_modules':sorted(affected-direct),
            'unmapped_paths':[p for p in paths if p not in mapped],
            'method':'path glob matching + conservative bidirectional relationship closure, not semantic analysis',
            'limitations':['No import, database or event inference. Review implicit coupling.','Working tree and untracked paths are included; baseline/candidate tests are not executed.']}

def run_check(project,name,command,execute=False,timeout=120):
    root=root_path(project); ctx=context_dir(root)
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]{0,63}',name): raise CFError('Check name must be a short safe identifier')
    if command and command[0]=='--': command=command[1:]
    if not command or not all(isinstance(x,str) and '\x00' not in x for x in command): raise CFError('Pass an argv after --; do not supply an empty command')
    if timeout<1 or timeout>1800: raise CFError('timeout must be 1..1800 seconds')
    if not execute:
        return {'status':'not-run','command':command,'project':str(root),'timeout':timeout,'warning':'Dry run. Review the command, then add --execute. Execution is not sandboxed.'},0
    eid=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    folder=ctx/'evidence'/eid; no_links(folder); folder.mkdir(parents=True,mode=0o700)
    initial=revision(root); started=now(); start=time.monotonic(); timed_out=False; output_limit=1_048_576
    stdout=folder/'stdout.txt'; stderr=folder/'stderr.txt'
    for log in [stdout,stderr]: write_private(log,'',exclusive=True)
    # Temporary files avoid unbounded in-memory capture; kill on total log growth.
    killed_for_output=False; exitcode=None
    with stdout.open('wb') as out, stderr.open('wb') as err:
        try:
            proc=subprocess.Popen(command,cwd=root,stdout=out,stderr=err,start_new_session=(os.name!='nt'))
            while proc.poll() is None:
                timed_out=time.monotonic()-start>timeout
                killed_for_output=stdout.stat().st_size+stderr.stat().st_size>output_limit
                if timed_out or killed_for_output:
                    if os.name!='nt':
                        try: os.killpg(proc.pid,signal.SIGKILL)
                        except ProcessLookupError: pass
                    else: proc.kill()
                    break
                time.sleep(0.05)
            exitcode=proc.wait(timeout=10)
        except FileNotFoundError:
            err.write(b'Executable not found.\n'); exitcode=127
        except OSError as exc:
            err.write(str(exc).encode('utf-8','replace')); exitcode=126
    final=revision(root)
    for log in [stdout,stderr]:
        if log.stat().st_size>output_limit:
            with log.open('r+b') as f: f.truncate(output_limit)
    status='inconclusive' if timed_out or killed_for_output else 'passed' if exitcode==0 else 'failed'
    data={'schema_version':1,'id':name,'status':status,'command':command,'started_at':started,'finished_at':now(),
          'duration_seconds':round(time.monotonic()-start,3),'exit_code':exitcode,'timed_out':timed_out,
          'output_limit_exceeded':killed_for_output,'candidate_before':initial,'candidate_after':final,
          'environment':'local user-provided command; not sandboxed',
          'evidence':[{'path':str(log.relative_to(root)),'sha256':hashlib.sha256(log.read_bytes()).hexdigest()} for log in [stdout,stderr]],
          'limitations':['Exit success only establishes the command result, not complete acceptance coverage.','Logs may contain sensitive information. Review before sharing.','On Windows, forced termination may not stop grandchildren; use an OS sandbox for untrusted commands.']}
    report=folder/'check.json'; write_private(report,json.dumps(data,indent=2)+'\n')
    data['report_path']=str(report)
    return data,0 if status=='passed' else 1

def evaluate_gate(report):
    if not isinstance(report,dict): raise CFError('Report must be an object')
    if report.get('schema_version')!=1: raise CFError('Unsupported report schema_version')
    required=report.get('required_checks'); checks=report.get('checks')
    if not isinstance(required,list) or not required or not all(isinstance(x,str) and x for x in required) or len(set(required))!=len(required): raise CFError('Required checks must be a nonempty unique string list')
    if not isinstance(checks,list): raise CFError('checks must be a list')
    index={}; blockers=[]; gaps=[]
    rev=report.get('candidate_revision')
    if not isinstance(rev,str) or not rev or rev in {'UNSET','unknown'}: gaps.append('Candidate revision is not identified')
    if report.get('environment') in {None,'','UNSET'}: gaps.append('Environment is not identified')
    for check in checks:
        if not isinstance(check,dict) or not isinstance(check.get('id'),str) or not check['id'] or check['id'] in index: raise CFError('Invalid or duplicate check ID')
        if check.get('status') not in CHECK_STATUSES: raise CFError('Invalid check status')
        ev=check.get('evidence',[])
        if not isinstance(ev,list) or not all((isinstance(x,str) and x.strip()) or (isinstance(x,dict) and isinstance(x.get('path'),str) and x['path']) for x in ev): raise CFError('Evidence must be a list of nonempty artifact references')
        index[check['id']]=check
    for cid in required:
        c=index.get(cid)
        if not c: gaps.append(f'Missing required check: {cid}'); continue
        if c['status']=='failed': blockers.append(f'Required check failed: {cid}')
        elif c['status']!='passed': gaps.append(f'Required check {cid}: {c["status"]}')
        elif not c.get('evidence'): gaps.append(f'No evidence for: {cid}')
        if c.get('candidate_revision')!=rev: gaps.append(f'Revision mismatch: {cid}')
    # Any reported failure requires explicit disposition; never hide it by omitting it from required.
    for cid,c in index.items():
        if cid not in required and c['status']=='failed': blockers.append(f'Additional check failed: {cid}')
    findings=report.get('blocking_findings',[])
    if not isinstance(findings,list): raise CFError('blocking_findings must be a list')
    for f in findings:
        if not isinstance(f,dict) or not isinstance(f.get('id'),str) or f.get('status') not in {'open','resolved'}: raise CFError('Each finding needs id and open/resolved status')
        if f['status']=='open': blockers.append(f'Open blocking finding: {f["id"]}')
        elif not f.get('evidence'): gaps.append(f'Resolved finding lacks evidence: {f["id"]}')
    changes=report.get('acceptance_changes',[])
    if not isinstance(changes,list): raise CFError('acceptance_changes must be a list')
    for c in changes:
        if not isinstance(c,dict) or not isinstance(c.get('description'),str): raise CFError('Acceptance change needs description')
        if c.get('approved') is not True or not c.get('approved_by') or not c.get('reason'): blockers.append('Unapproved or unexplained acceptance change')
    status='blocked' if blockers else 'inconclusive' if gaps else 'ready-for-review'
    return {'status':status,'blockers':blockers,'gaps':gaps,'required_checks':len(required),
            'limits':'Structural review only. Artifact references/approvals are self-reported; authenticity and coverage are not independently enforced. Not deployment authorization.'}

def brief(project,on_date=None,limit=3):
    root=root_path(project); state=read_json(context_dir(root)/'state.json')
    if not isinstance(state,dict): raise CFError('State must be an object')
    try: d=date.fromisoformat(on_date) if on_date else date.today()
    except ValueError as exc: raise CFError('date must be YYYY-MM-DD') from exc
    if limit<1 or limit>10: raise CFError('limit must be 1..10')
    candidates=[]; ranks={'urgent':0,'high':1,'normal':2,'low':3}; warnings=[]
    closed={'closed','resolved','customer-confirmed','done','lost','won','cancelled','retired'}
    for group in ['issues','tasks','sales']:
        items=state.get(group,[])
        if not isinstance(items,list): raise CFError(f'{group} must be a list')
        for item in items:
            if not isinstance(item,dict) or not item.get('id') or not item.get('title'): raise CFError(f'Each {group} item needs id and title')
            if item.get('status') in closed: continue
            due=item.get('due_date'); overdue=False
            if due:
                try: overdue=date.fromisoformat(due)<=d
                except (ValueError,TypeError): warnings.append(f'Invalid due_date: {item["id"]}')
            candidates.append((ranks.get(item.get('priority'),2),not overdue,0 if group=='issues' else 1,item['id'],
                               {'group':group,**item,'due_or_overdue':overdue}))
    candidates.sort(key=lambda x:x[:4])
    return {'date':d.isoformat(),'timezone':'system local date unless --date supplied; timezone must be established by the host',
            'source_updated_at':state.get('updated_at'),'priorities':[x[4] for x in candidates[:limit]],
            'warnings':warnings+([] if state.get('updated_at') else ['State freshness is unknown.']),
            'note':'Local sorting aid, not a business judgment. Review severity, promises and fresh evidence. No external accounts were queried.',
            'actions_executed':False}

def usage_add(project,source,input_tokens=None,output_tokens=None,cached_input_tokens=None,reasoning_tokens=None):
    root=root_path(project);ctx=context_dir(root)
    if not source or len(source)>160: raise CFError('Use a short source label identifying the measured usage record')
    values={'input_tokens':input_tokens,'output_tokens':output_tokens,'cached_input_tokens':cached_input_tokens,'reasoning_tokens':reasoning_tokens}
    for k,v in values.items():
        if v is not None and (isinstance(v,bool) or not isinstance(v,int) or v<0): raise CFError(f'{k} must be nonnegative integer or unknown')
    if all(v is None for v in values.values()): raise CFError('Supply at least one measured count')
    if cached_input_tokens is not None and (input_tokens is None or cached_input_tokens>input_tokens): raise CFError('Cached input is a subset of measured input')
    if reasoning_tokens is not None and (output_tokens is None or reasoning_tokens>output_tokens): raise CFError('This schema treats reasoning as a subset of measured output; convert provider fields correctly or leave unknown')
    entry={'recorded_at':now(),'source':source,**values,'accounting':'input includes cached; output includes reasoning; subsets must not be added twice'}
    path=ctx/'usage.jsonl'; no_links(path)
    # Exclusive lock: never silently lose concurrent entries.
    lock=ctx/'.usage.lock'
    try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError as exc: raise CFError('Usage log is locked. Check the active writer; remove a stale lock only after confirming no writer is running.') from exc
    try:
        os.close(fd)
        fd2=os.open(path,os.O_CREAT|os.O_APPEND|os.O_WRONLY,0o600)
        with os.fdopen(fd2,'a',encoding='utf-8') as f: f.write(json.dumps(entry)+'\n')
    finally: lock.unlink()
    return entry

def usage_summary(project):
    p=context_dir(root_path(project))/'usage.jsonl';no_links(p)
    if not p.exists(): return {'records':0,'total_tokens':None,'note':'No measured usage recorded; subscription allowance is not read.'}
    if p.stat().st_size>5_000_000: raise CFError('Usage file too large; archive reviewed records first')
    try: records=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    except ValueError as exc: raise CFError('Invalid usage JSONL') from exc
    keys=['input_tokens','output_tokens','cached_input_tokens','reasoning_tokens']; counts={k:0 for k in keys};unknown={k:0 for k in keys}
    for r in records:
        if not isinstance(r,dict): raise CFError('Invalid usage entry')
        for k in keys:
            v=r.get(k)
            if v is None: unknown[k]+=1
            elif isinstance(v,int) and not isinstance(v,bool) and v>=0: counts[k]+=v
            else: raise CFError('Invalid usage count')
    return {'records':len(records),'known_counts':counts,'records_with_unknown_counts':unknown,
            'total_tokens':counts['input_tokens']+counts['output_tokens'] if not unknown['input_tokens'] and not unknown['output_tokens'] else None,
            'remaining_subscription_allowance':None,'cost':None,
            'note':'Measured records only; cached/reasoning are subsets, not extra totals. No quota or billing access.'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
    for name in ['init','doctor','context','impact','run-check','brief','usage','usage-summary']:
        s=sub.add_parser(name);s.add_argument('--project',required=True)
        if name=='context': s.add_argument('--task',required=True);s.add_argument('--max-bytes',type=int,default=12000)
        if name=='impact': s.add_argument('--base',required=True);s.add_argument('--map');s.add_argument('--max-paths',type=int,default=500)
        if name=='run-check':
            s.add_argument('--name',required=True);s.add_argument('--execute',action='store_true');s.add_argument('--timeout',type=int,default=120);s.add_argument('command',nargs=argparse.REMAINDER)
        if name=='brief':s.add_argument('--date');s.add_argument('--limit',type=int,default=3)
        if name=='usage':
            s.add_argument('--source',required=True)
            for flag in ['input-tokens','output-tokens','cached-input-tokens','reasoning-tokens']:s.add_argument('--'+flag,type=int)
    s=sub.add_parser('gate');s.add_argument('--report',required=True)
    a=p.parse_args(argv)
    try:
        code=0
        if a.cmd=='init':result=init_project(a.project)
        elif a.cmd=='doctor':result=doctor(a.project)
        elif a.cmd=='context':result=context_plan(a.project,a.task,a.max_bytes)
        elif a.cmd=='impact':
            if not 1<=a.max_paths<=5000:raise CFError('max-paths must be 1..5000')
            result=impact(a.project,a.base,a.map,a.max_paths)
        elif a.cmd=='run-check':result,code=run_check(a.project,a.name,a.command,a.execute,a.timeout)
        elif a.cmd=='gate':result=evaluate_gate(read_json(Path(a.report).expanduser().absolute()));code=0 if result['status']=='ready-for-review' else 1
        elif a.cmd=='brief':result=brief(a.project,a.date,a.limit)
        elif a.cmd=='usage':result=usage_add(a.project,a.source,a.input_tokens,a.output_tokens,a.cached_input_tokens,a.reasoning_tokens)
        elif a.cmd=='usage-summary':result=usage_summary(a.project)
        emit(result);return code
    except (CFError,OSError,ValueError,TypeError,subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
