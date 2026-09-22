#!/usr/bin/env python3
"""Opt-in inline browser tests for the fictional connected-brand examples only.

No host login, backend, live URL navigation, persistence, or model behavior tested.
Requires explicitly installed Playwright and Chromium. Never installs dependencies.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cf_connected_browser',ROOT/'skills/co-founder/scripts/connected_studio.py')
studio=importlib.util.module_from_spec(spec);spec.loader.exec_module(studio)

def run(out,browser=None):
 out=studio.pc.plain_path(out)
 if out.exists():raise ValueError('Choose a new output directory; existing evidence is never overwritten')
 out.mkdir(parents=True)
 from playwright.sync_api import sync_playwright
 results=[];captures=[];errors=[];requests=[]
 def check(name,value,detail=''):
  results.append({'check':name,'status':'passed' if value else 'failed','detail':detail})
 def overflow(page):return page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
 north=ROOT/'examples/connected-brand/northline'
 html,binding,_=studio.compose(north,'ui.html','product-ui')
 with sync_playwright() as pw:
  opts={'headless':True}
  if browser:opts['executable_path']=browser
  engine=pw.chromium.launch(**opts)
  try:
   context=engine.new_context(device_scale_factor=1)
   context.route('**/*',lambda route:(requests.append(route.request.url.split('?')[0]),route.abort())[-1])
   def document(html,viewport):
    fresh=context.new_page();fresh.on('pageerror',lambda e:errors.append(str(e)));fresh.set_viewport_size(viewport);fresh.set_content(html);return fresh
   page=None
   for width,height,label in [(1440,1000,'desktop'),(768,1024,'tablet'),(390,844,'mobile')]:
    if page:page.close()
    page=document(html,{'width':width,'height':height});page.evaluate('document.fonts.ready')
    check(label+' horizontal overflow',not overflow(page))
    check(label+' assets loaded',page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'))
    check(label+' bound project',page.evaluate('document.documentElement.dataset.projectId')=='northline-demo')
    path=out/f'ui-{label}.png';page.screenshot(path=str(path),full_page=True);captures.append({'path':path.name,'viewport':[width,height]})
   page.get_by_role('button',name='Open navigation',exact=True).click()
   check('mobile navigation opens',page.locator('#sidebar').evaluate("e=>e.classList.contains('open')"))
   page.keyboard.press('Escape');check('mobile navigation closes',not page.locator('#sidebar').evaluate("e=>e.classList.contains('open')"))
   page.get_by_role('button',name='Open R-1048 Phone 14 Pro',exact=True).click();check('mobile detail replaces queue',page.locator('.detail').is_visible() and not page.locator('.queue').is_visible())
   page.screenshot(path=str(out/'ui-mobile-detail.png'),full_page=True);captures.append({'path':'ui-mobile-detail.png','viewport':[390,844]})
   page.get_by_role('button',name='Back to repairs').click();check('mobile back restores queue',page.locator('.queue').is_visible() and not page.locator('.detail').is_visible())
   check('mobile focus restored',page.locator('[data-repair-id="R-1048"]').evaluate('e=>e===document.activeElement'))
   page.close();page=document(html,{'width':1440,'height':1000})
   check('initial repair count',page.locator('#rows tr').count()==8)
   page.locator('#search').fill('R-1048');check('search filters correct record',page.locator('#rows tr').count()==1 and 'R-1048' in page.locator('#rows').inner_text())
   page.locator('#search').fill('not-a-record');check('search empty state',page.locator('#empty').is_visible() and page.locator('#rows tr').count()==0)
   page.locator('#search').fill('');page.locator('[data-filter="ready"]').click();check('ready filter',page.locator('#rows tr').count()==2)
   page.locator('[data-filter="all"]').click();page.locator('#sort').select_option('id');check('sort order',page.locator('#rows tr').first.inner_text().startswith('R-1045') or 'R-1045' in page.locator('#rows tr').first.inner_text())
   page.get_by_role('button',name='Open R-1049 Phone S23',exact=True).click();check('waiting part cannot complete',page.locator('#completeRepair').is_disabled())
   page.evaluate('completeSelected()');check('waiting part does not deduct',page.evaluate('demoState().stock')==24)
   page.get_by_role('button',name='Open R-1048 Phone 14 Pro',exact=True).click();page.locator('#completeRepair').click()
   s=page.evaluate('demoState()');check('completion updates one repair',next(j for j in s['jobs'] if j['id']=='R-1048')['status']=='ready')
   check('completion deducts exactly one part',s['stock']==23 and s['movements']==1)
   page.evaluate('completeSelected()');s=page.evaluate('demoState()');check('repeat completion is idempotent in fixture',s['stock']==23 and s['movements']==1)
   page.locator('[data-view="inventory"]').click();check('inventory view opens',page.locator('#view-inventory').is_visible())
   check('inventory reflects completion','23' in page.locator('#view-inventory').inner_text())
   page.locator('[data-view="activity"]').click();check('activity reflects completion','R-1048' in page.locator('#view-activity').inner_text())
   page.locator('[data-view="repairs"]').click();page.locator('#newJob').click();check('new-repair dialog opens',page.locator('#newDialog').is_visible())
   page.locator('[name="device"]').fill('Demo device');page.locator('[name="customer"]').fill('<img src=x onerror=alert(1)>')
   page.get_by_role('button',name='Add repair',exact=True).click();check('new repair added',page.evaluate('demoState().jobs.length')==9)
   check('user text not interpreted as markup',page.locator('#rows img[src="x"]').count()==0 and '<img src=x' in page.locator('#rows').inner_text())
   page.close();page=document(html,{'width':1440,'height':1000});check('fresh fixture explicitly resets in-memory data',page.evaluate('demoState().stock')==24 and page.evaluate('demoState().jobs.length')==8,'Not a reload/persistence test')
   page.evaluate("()=>{const e=document.createElement('div');e.id='deliberate-overflow';e.style.cssText='width:5000px;height:1px';document.body.append(e)}")
   check('detector catches deliberate overflow',overflow(page));page.locator('#deliberate-overflow').evaluate('e=>e.remove()');check('overflow cleanup',not overflow(page))
   # Brand isolation: same composition, different manifests, exact source artwork.
   observed=[]
   for folder in ['northline','second-project']:
    h,b,_=studio.compose(ROOT/'examples/connected-brand'/folder,'brand-proof.html','post');page.close();page=document(h,{'width':720,'height':460});page.evaluate('document.fonts.ready')
    check(folder+' exact logo',page.locator('#logo').get_attribute('src')==studio.asset_data(b['assets'][0]['absolute_path']))
    observed.append(page.evaluate("({id:document.documentElement.dataset.projectId,accent:getComputedStyle(document.documentElement).getPropertyValue('--accent'),heading:getComputedStyle(document.querySelector('h1')).fontFamily})"))
    path=out/f'brand-{folder}.png';page.screenshot(path=str(path));captures.append({'path':path.name,'viewport':[720,460]})
   check('different projects remain separate',all(observed[0][key]!=observed[1][key] for key in ['id','accent','heading']))
   # Movie semantic checkpoints are actual JS state checks, not a playback review.
   h,b,_=studio.compose(north,'motion.html','video');page.close();page=document(h,{'width':1280,'height':720});page.evaluate('window.CF_EXPORT=true')
   for at,stock,movements in [(5,24,0),(10.5,23,1),(15.8,23,1),(19.8,23,1)]:
    page.evaluate('(t)=>renderAt(t)',at);s=page.evaluate('window.motionState');check(f'motion state at {at}s',s.get('stock')==stock and s.get('movements')==movements,str(s))
   check('no JavaScript errors',not errors,str(errors));check('no external browser requests',not requests,str(requests))
  finally:engine.close()
 report={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'passed' if all(r['status']=='passed' for r in results) else 'failed','checks':results,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'captures':captures,'not_run':['live URL navigation','origin-backed reload persistence','production authentication/tenant isolation','authenticated Codex/Claude model execution','full audiovisual playback review'],'scope':'Inline fictional UI and declared motion state; not a product-security or creative-acceptance certification.'}
 (out/'browser-report.json').write_text(json.dumps(report,indent=2)+'\n');return report

def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--browser');a=p.parse_args(argv)
 try:r=run(a.out,a.browser);print(json.dumps(r,indent=2));return 0 if r['status']=='passed' else 1
 except Exception as e:print(f'SMOKE FAILED ({type(e).__name__}): {e}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
