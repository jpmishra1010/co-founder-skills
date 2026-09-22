#!/usr/bin/env python3
"""Optional local-browser fixture tests. Starts a loopback server only while running."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',ROOT/'skills/co-founder/scripts/ui_audit.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def run(out,browser=None,offline=False):
 from playwright.sync_api import sync_playwright
 dest=audit.safe_new_dir(out)
 server=None;thread=None;base=None
 if not offline:
  server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'examples/ui-fixture')))
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_address[1]}'
 checks=[]
 def record(name,okay,detail=''):
  checks.append({'id':name,'status':'passed' if okay else 'failed','detail':detail})
 try:
  raw=(ROOT/'examples/ui-fixture/index.html').read_text(encoding='utf-8')
  good=audit.audit_html(ROOT/'examples/ui-fixture/index.html',dest/'responsive',browser) if offline else audit.audit(base,['/'],dest/'responsive',browser)
  record('three-viewport-capture',all(x['status']=='captured' for x in good['results']))
  if offline:
   with tempfile.TemporaryDirectory() as td:
    f=Path(td).resolve()/'broken.html';f.write_text(raw.replace('</head>','<style>.main{min-width:980px!important}</style></head>'),encoding='utf-8');bad=audit.audit_html(f,dest/'intentional-overflow',browser,sizes=['390x844'])
  else:bad=audit.audit(base,['/?broken=1'],dest/'intentional-overflow',browser,sizes=['390x844'])
  record('intentional-overflow-detected',bad['results'][0].get('observations',{}).get('horizontalOverflow') is True)
  with sync_playwright() as p:
   opts={'headless':True}
   if browser:opts['executable_path']=browser
   b=p.chromium.launch(**opts)
   try:
    page=b.new_page(viewport={'width':1440,'height':1000})
    if offline:
     page.set_content(raw,wait_until='load');checks.append({'id':'live-navigation','status':'not-run','detail':'Offline inline-document mode; actual URL navigation not tested.'})
    else:
     page.goto(base);record('live-navigation',True)
    record('initial-synthetic-count',page.locator('#openCount').inner_text()=='3')
    page.locator('#add').click();record('dialog-focus',page.locator('#title').evaluate('(el)=>document.activeElement===el'))
    page.locator('#title').fill('Browser smoke fixture task');page.get_by_role('button',name='Add task',exact=True).click();record('create-task',page.locator('#openCount').inner_text()=='4')
    if offline:checks.append({'id':'local-persistence','status':'not-run','detail':'No authenticated/origin-backed reload in inline-document mode.'})
    else:
     page.reload();record('local-persistence',page.locator('#openCount').inner_text()=='4')
    page.locator('.rowbutton').first.click();record('completion-count',page.locator('#doneCount').inner_text()=='1')
    page.locator('#open').click();record('open-filter',page.locator('#rows tr').count()==3)
    page.locator('#add').click();page.keyboard.press('Escape');record('escape-closes-dialog',not page.locator('#dialog').evaluate('(el)=>el.open'))
    page.set_viewport_size({'width':390,'height':844});page.locator('#menu').click();record('mobile-menu-opens',page.locator('#menu').get_attribute('aria-expanded')=='true');page.locator('#menu').click();record('mobile-menu-closes',page.locator('#menu').get_attribute('aria-expanded')=='false')
    record('mobile-no-horizontal-overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    page.locator('#add').click();page.locator('#title').fill('<img src=x onerror=alert(1)>');page.get_by_role('button',name='Add task',exact=True).click();record('text-inserted-not-html',page.locator('#rows img').count()==0 and '<img src=x' in page.locator('#rows').inner_text())
   finally:b.close()
 finally:
  if server:
   server.shutdown();server.server_close();thread.join(timeout=3)
 report={'created_at':datetime.now(timezone.utc).isoformat(),'scope':'original synthetic local UI fixture only','checks':checks,'passed':sum(x['status']=='passed' for x in checks),'total':len(checks),'mode':'offline-inline-document' if offline else 'loopback-url','failed':sum(x['status']=='failed' for x in checks),'not_run':sum(x['status']=='not-run' for x in checks),'model_or_live_host_tested':False,'limitations':['No real product, authenticated account, external service, security audit or full accessibility audit tested.','Browser captures require separate human visual inspection.']}
 (dest/'browser-smoke.json').write_text(json.dumps(report,indent=2)+'\n');return report

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--browser');p.add_argument('--offline-fixture',action='store_true',help='Use inline document rendering when navigation is unavailable; persistence remains unverified');a=p.parse_args()
 try:
  r=run(a.out,a.browser,a.offline_fixture);print(json.dumps(r,indent=2));return 0 if r['failed']==0 else 1
 except Exception as exc:print(f'ERROR ({type(exc).__name__}): {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
