#!/usr/bin/env python3
"""Validate the authored pack without dependencies, model APIs or network calls."""
from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES={'.ttf','.otf','.woff','.woff2','.p12','.pfx','.pem','.key','.pyc'}

def validate(root=ROOT):
 root=Path(root);errors=[];warnings=[]
 try:manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
 except (OSError,ValueError) as exc:return {'status':'failed','errors':[str(exc)]}
 expected=['co-founder']+['co-founder-'+x for x in manifest['specialists']]
 actual=sorted(p.name for p in (root/'skills').iterdir() if p.is_dir())
 if sorted(expected)!=actual:errors.append('Skill directories do not match manifest')
 skills=[]
 for name in expected:
  p=root/'skills'/name/'SKILL.md'
  if not p.is_file():errors.append(f'Missing {p.relative_to(root)}');continue
  s=p.read_text(encoding='utf-8')
  m=re.match(r'\A---\n(.*?)\n---\n',s,re.S)
  if not m:errors.append(f'Invalid frontmatter in {name}');continue
  header=m.group(1)
  n=re.search(r'^name:\s*(.+?)\s*$',header,re.M);d=re.search(r'^description:\s*(.+?)\s*$',header,re.M)
  if not n or n.group(1)!=name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>64:errors.append(f'Invalid skill name: {name}')
  if not d or not 1<=len(d.group(1).strip('"\''))<=1024:errors.append(f'Invalid description: {name}')
  if len(s)>15000:errors.append(f'Entry skill unexpectedly large: {name}')
  host=root/'skills'/name/'agents/openai.yaml'
  if not host.is_file():errors.append(f'Missing host metadata: {name}')
  if name!='co-founder' and not (root/'skills/co-founder/workflows'/f'{name.removeprefix("co-founder-")}.md').is_file():errors.append(f'Wrapper target missing: {name}')
  skills.append({'name':name,'entry_bytes':len(s.encode()),'entry_words':len(s.split())})
 for f in root.rglob('*'):
  if '.git' in f.parts or '__pycache__' in f.parts:continue
  if f.is_symlink():errors.append(f'Unexpected symlink: {f.relative_to(root)}');continue
  if not f.is_file():continue
  if f.suffix.lower() in FORBIDDEN_SUFFIXES:errors.append(f'Forbidden binary/credential-like file: {f.relative_to(root)}')
  if f.name=='.env' or f.name.startswith('.env.') and f.name!='.env.example':errors.append(f'Environment file in public pack: {f.relative_to(root)}')
  try:
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8'),filename=str(f))
   elif f.suffix=='.json':json.loads(f.read_text(encoding='utf-8'))
  except (OSError,ValueError,SyntaxError) as exc:errors.append(f'{f.relative_to(root)}: {exc}')
  if f.suffix=='.md':
   s=f.read_text(encoding='utf-8')
   for link in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',s):
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',link) or link.startswith('#'):continue
    path=link.split('#',1)[0]
    if path and not (f.parent/path).exists():errors.append(f'Broken local Markdown link: {f.relative_to(root)} → {link}')
 for name in manifest['specialists']:
  p=root/'skills/co-founder/workflows'/f'{name}.md'
  if not p.is_file() or len(p.read_text().split())<150:errors.append(f'Missing/substantial workflow expected: {name}')
 contracts=json.loads((root/'skills/co-founder/references/review-contracts.json').read_text())
 if set(contracts.get('workflows',{}))!=set(manifest['specialists']):errors.append('Review contracts must cover exactly all workflows')
 if (root/'VERSION').read_text().strip()!=manifest['version']:errors.append('Version/manifest mismatch')
 for name in manifest['specialists']:
  principle=root/'skills/co-founder/references/principles'/f'{name}.md'
  if not principle.is_file():errors.append(f'Missing workflow principles: {name}')
  else:
   text=principle.read_text()
   for criterion in contracts.get('workflows',{}).get(name,[]):
    if f"`{criterion['id']}`" not in text:errors.append(f'Missing principle criterion: {name}/{criterion["id"]}')
  wf=(root/'skills/co-founder/workflows'/f'{name}.md').read_text()
  if 'references/project-identity.md' not in wf or f'references/principles/{name}.md' not in wf:errors.append(f'Project/principle route missing: {name}')
  wrapper=(root/'skills'/f'co-founder-{name}'/'SKILL.md').read_text()
  if 'project-identity.md' not in wrapper:errors.append(f'Wrapper bypasses project route: {name}')
 allowed_contexts={f'examples/connected-brand/{folder}/.co-founder/{filename}' for folder in ['northline','second-project'] for filename in ['project.json','brand.json','assets.json']}
 for f in root.rglob('*'):
  if '.co-founder' in f.relative_to(root).parts and f.is_file() and f.relative_to(root).as_posix() not in allowed_contexts:errors.append(f'Unexpected private-context file in public pack: {f.relative_to(root)}')
 categories=list((root/'skills/co-founder/references/categories').glob('*.md'))
 if len(categories)!=17:errors.append('Expected 17 representative category guides')
 research=json.loads((root/'skills/co-founder/references/research-catalog.json').read_text())
 ids=[s['id'] for s in research['sources']]
 if len(ids)!=len(set(ids)):errors.append('Duplicate research IDs')
 if not research.get('no_full_external_video_playback'):warnings.append('Video access claim changed; attach actual viewing evidence')
 evals=json.loads((root/'evals/cases.json').read_text())
 if len({x['id'] for x in evals['cases']})!=len(evals['cases']):errors.append('Duplicate evaluation case IDs')
 if evals.get('results_claimed'):warnings.append('Model result claim present; validate evidence separately')
 for source in (root/'skills/co-founder/scripts').glob('*.py'):
  s=source.read_text()
  if re.search(r'https?://api\.(openai|anthropic)\.com',s):errors.append(f'Mandatory model endpoint found: {source}')
 return {'status':'passed' if not errors else 'failed','version':manifest['version'],'skills':skills,'skill_count':len(skills),'workflow_count':len(manifest['specialists']),'category_guides':len(categories),'research_sources':len(ids),'evaluation_cases':len(evals['cases']),'errors':errors,'warnings':warnings,'limits':'Checks authored structure/syntax/links, not every semantic requirement, credential pattern, model behavior or external source.'}

def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json-out');a=p.parse_args(argv);r=validate();print(json.dumps(r,indent=2))
 if a.json_out:
  out=Path(a.json_out)
  if out.exists():raise SystemExit('Refusing to overwrite existing validation output')
  out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2)+'\n')
 return 0 if r['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
