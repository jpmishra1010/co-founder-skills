#!/usr/bin/env python3
"""Validate an evidence-backed review record; never certify visual taste/security.

Offline, standard library only. Human acceptance is reported but not authenticated.
A ready-for-human-review result is not approval to publish, send or deploy.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
PACK=Path(__file__).resolve().parents[1]
VALID={'pass','revise','not-checked','not-applicable'}
class ReviewError(ValueError): pass

def evaluate(report):
    if not isinstance(report,dict) or report.get('schema_version')!=1:raise ReviewError('Expected review schema 1')
    contracts=json.loads((PACK/'references/review-contracts.json').read_text())
    workflow=report.get('workflow')
    if workflow not in contracts['workflows']:raise ReviewError('Unknown workflow')
    required={x['id'] for x in contracts['common']+contracts['workflows'][workflow]}
    if not isinstance(report.get('project_id'),str) or report['project_id'] in {'UNSET','unconfirmed',''}:raise ReviewError('A confirmed project ID is required')
    if not re.fullmatch(r'[a-f0-9]{64}',str(report.get('bundle_fingerprint',''))):raise ReviewError('Project bundle fingerprint is required')
    rows=report.get('checks');seen={};blocked=[];missing=[]
    if not isinstance(rows,list):raise ReviewError('checks must be a list')
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get('id'),str) or row.get('status') not in VALID:raise ReviewError('Invalid check')
        key=row['id']
        if key in seen:raise ReviewError('Duplicate check IDs')
        seen[key]=row
        if row['status']=='revise':blocked.append(key)
        elif row['status']=='not-checked':missing.append(key)
        elif row['status']=='not-applicable':
            if key in {'project','evidence','handoff','brand-fit','claims','terms'}:blocked.append(key)
            elif not isinstance(row.get('reason'),str) or len(row['reason'].strip())<12:missing.append(key)
        elif not isinstance(row.get('evidence'),list) or not row['evidence'] or not all(isinstance(x,str) and x.strip() for x in row['evidence']):missing.append(key)
    missing.extend(sorted(required-set(seen)))
    surface=report.get('surface','general')
    creative=workflow in {'ui-polish','content-studio'}
    if creative:
        if surface not in {'product-ui','website','post','video'}:raise ReviewError('Creative review needs the actual surface')
        if not re.fullmatch(r'[a-f0-9]{64}',str(report.get('artifact_sha256',''))):missing.append('artifact-hash')
        if not report.get('artifact_path') or report['artifact_path']=='UNSET':missing.append('artifact-path')
        observations=report.get('visual_observations')
        if not isinstance(observations,list) or not observations:missing.append('actual-visual-observations')
        else:
            for item in observations:
                if not isinstance(item,dict) or not item.get('location') or not item.get('observation') or not item.get('evidence'):missing.append('visual-observation-detail');break
        refs=report.get('reference_observations')
        if not isinstance(refs,list) or not refs:missing.append('reference-observations')
        else:
            for ref in refs:
                if not isinstance(ref,dict) or ref.get('access') not in {'image-inspected','live-ui-inspected','video-frames-inspected','video-played','approved-project-reference'} or not ref.get('observation') or not ref.get('source'):
                    missing.append('reference-not-visually-inspected');break
        if not isinstance(report.get('revisions'),list) or not report['revisions']:missing.append('critique-and-revision-record')
        if surface=='video':
            if report.get('full_playback')!='pass':missing.append('full-playback')
            if report.get('audio_review') not in {'pass','intentionally-silent'}:missing.append('audio-review')
    status='blocked' if blocked else 'inconclusive' if missing else 'ready-for-human-review'
    return {'status':status,'workflow':workflow,'project_id':report['project_id'],'blocking_checks':sorted(set(blocked)),
            'missing_or_unverified':sorted(set(missing)),'human_acceptance':report.get('human_acceptance'),
            'limits':'Self-reported structural evidence only. Does not authenticate approval, inspect linked artifacts, enforce host permissions, or certify taste/security. Never a publication permission.'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);a=p.parse_args(argv)
    try:
        path=Path(a.report)
        if path.is_symlink() or not path.is_file() or path.stat().st_size>250_000:raise ReviewError('Invalid/oversized review file')
        result=evaluate(json.loads(path.read_text(encoding='utf-8')));print(json.dumps(result,indent=2));return 0 if result['status']=='ready-for-human-review' else 1
    except (ReviewError,OSError,ValueError) as exc:print(f'REVIEW ERROR: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
