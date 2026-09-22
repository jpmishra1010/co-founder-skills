#!/usr/bin/env python3
"""Capture approved pages at multiple sizes; basic layout checks, NOT full UI QA.

Optional Python Playwright/Chromium required. Defaults to loopback-only targets.
No logins, form submissions, downloads, clicks, paid APIs, or automatic installs.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit,urlunsplit,urljoin

class AuditError(ValueError):pass

def origin(url):
    u=urlsplit(url)
    if u.scheme not in {'http','https'} or not u.hostname or u.username or u.password:raise AuditError('Use an http(s) URL without embedded credentials')
    try:p=u.port
    except ValueError as exc:raise AuditError('Invalid URL port') from exc
    host=u.hostname.lower();authority=('['+host+']') if ':' in host else host
    if p is not None and not (u.scheme=='http' and p==80 or u.scheme=='https' and p==443):authority+=':'+str(p)
    return u.scheme+'://'+authority

def validate_target(base,paths,allow_remote=False):
    o=origin(base);u=urlsplit(base)
    if u.path not in {'','/'} or u.query or u.fragment:raise AuditError('Base must be an origin; use --paths for page paths')
    if u.hostname not in {'localhost','127.0.0.1','::1'} and not allow_remote:raise AuditError('Remote targets require explicit --allow-remote and authorization to inspect them')
    targets=[]
    for p in paths:
        if not isinstance(p,str) or not p.startswith('/') or p.startswith('//') or '\\' in p or len(p)>500:raise AuditError('Paths must start with a single / and remain on the approved origin')
        target=urljoin(o,p)
        if origin(target)!=o:raise AuditError('Path changes the target origin')
        targets.append(target)
    if not 1<=len(targets)<=20:raise AuditError('Inspect 1..20 paths per run')
    return o,targets

def viewport(text):
    m=re.fullmatch(r'(\d{3,4})x(\d{3,4})',text)
    if not m:raise AuditError('Viewport must look like 390x844')
    w,h=map(int,m.groups())
    if not 320<=w<=2560 or not 480<=h<=2560:raise AuditError('Viewport outside supported bounds')
    return {'width':w,'height':h}

def safe_new_dir(value):
    path=Path(value).expanduser().absolute()
    for p in [path,*path.parents]:
        if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()):raise AuditError('Linked output paths are not supported')
    if path.exists():raise AuditError('Output directory must be new; existing evidence is never overwritten')
    path.mkdir(parents=True,mode=0o700);return path

def audit(base,paths,out,browser=None,sizes=None,allow_remote=False,allow_origins=None):
    o,targets=validate_target(base,paths,allow_remote)
    allowed={o}
    for x in allow_origins or []:allowed.add(origin(x))
    dims=[viewport(x) for x in sizes or ['390x844','768x1024','1440x1000']]
    if len(dims)>6:raise AuditError('At most 6 viewport sizes per run')
    try:from playwright.sync_api import sync_playwright
    except ImportError as exc:raise AuditError('Optional Playwright dependency missing; see docs/MEDIA.md') from exc
    folder=safe_new_dir(out);results=[]
    with sync_playwright() as p:
        options={'headless':True}
        if browser:options['executable_path']=browser
        browser_obj=p.chromium.launch(**options)
        try:
            for ix,url in enumerate(targets):
                for size in dims:
                    blocked=[];errors=[];ctx=browser_obj.new_context(viewport=size,device_scale_factor=1,accept_downloads=False,reduced_motion='reduce')
                    def route(r):
                        u=r.request.url
                        try:permitted=u.startswith('data:') or origin(u) in allowed
                        except AuditError:permitted=False
                        if permitted:r.continue_()
                        else:blocked.append(u.split('?')[0][:180]);r.abort()
                    ctx.route('**/*',route);page=ctx.new_page();page.on('pageerror',lambda exc:errors.append(str(exc)[:400]))
                    entry={'path':urlsplit(url).path,'viewport':size,'navigation':'direct-load only','status':'inconclusive'}
                    try:
                        response=page.goto(url,wait_until='domcontentloaded',timeout=20000)
                        page.wait_for_timeout(500)
                        if origin(page.url) not in allowed:raise AuditError('Unexpected redirect origin')
                        evidence=page.evaluate('''() => ({title:document.title, horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1, brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).slice(0,20).map(i=>({alt:i.alt,src:i.getAttribute('src')?.split('?')[0]})), unlabeledButtons:[...document.querySelectorAll('button')].filter(b=>!b.textContent.trim()&&!b.getAttribute('aria-label')&&!b.getAttribute('aria-labelledby')&&!b.querySelector('img[alt]')).length})''')
                        name=f'page-{ix+1:02d}-{size["width"]}x{size["height"]}.png'
                        page.screenshot(path=str(folder/name),full_page=True,animations='disabled',timeout=15000)
                        status=response.status if response else None
                        entry.update(http_status=status,screenshot=name,observations=evidence,
                                     status='findings' if status is None or status>=400 or evidence['horizontalOverflow'] or evidence['brokenImages'] or evidence['unlabeledButtons'] or errors or blocked else 'captured')
                    except Exception as exc:entry['error']=str(exc)[:600]
                    finally:
                        entry['blocked_resources']=sorted(set(blocked));entry['page_errors']=errors;results.append(entry);ctx.close()
        finally:browser_obj.close()
    report={'created_at':datetime.now(timezone.utc).isoformat(),'base_origin':o,'results':results,
            'limits':['Basic DOM observations and screenshots only. Not accessibility/security certification.','No authentication, interaction, navigation-return, refresh, backend persistence or device-native behavior verified.','A screenshot must be visually inspected before claiming visual QA. Blocked resources can affect appearance.','Screenshots and page text can expose private data. Use synthetic fixtures and review before sharing.']}
    (folder/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


def audit_html(html_path,out,browser=None,sizes=None):
    """Explicit offline document mode: inline render, no navigation or storage proof."""
    path=Path(html_path).expanduser().absolute()
    for q in [path,*path.parents]:
        if q.is_symlink() or (hasattr(q,'is_junction') and q.is_junction()):raise AuditError('Linked HTML inputs are not supported')
    if not path.is_file() or path.suffix.lower() not in {'.html','.htm'} or path.stat().st_size>2_000_000:raise AuditError('Provide a reviewed local HTML file below 2 MB')
    raw=path.read_text(encoding='utf-8')
    dims=[viewport(x) for x in sizes or ['390x844','768x1024','1440x1000']]
    if not 1<=len(dims)<=6:raise AuditError('Inspect 1..6 viewport sizes')
    from playwright.sync_api import sync_playwright
    folder=safe_new_dir(out);results=[]
    with sync_playwright() as p:
        options={'headless':True}
        if browser:options['executable_path']=browser
        b=p.chromium.launch(**options)
        try:
            for size in dims:
                blocked=[];errors=[];ctx=b.new_context(viewport=size,device_scale_factor=1,reduced_motion='reduce',accept_downloads=False)
                def block(r):blocked.append(r.request.url.split('?')[0][:180]);r.abort()
                ctx.route('**/*',block);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)[:400]))
                page.set_content(raw,wait_until='load');page.wait_for_timeout(100)
                evidence=page.evaluate("""() => ({title:document.title,horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1,brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).slice(0,20).map(i=>({alt:i.alt})),unlabeledButtons:[...document.querySelectorAll('button')].filter(b=>!b.textContent.trim()&&!b.getAttribute('aria-label')&&!b.getAttribute('aria-labelledby')&&!b.querySelector('img[alt]')).length})""")
                name=f'offline-{size["width"]}x{size["height"]}.png';page.screenshot(path=str(folder/name),full_page=True,animations='disabled')
                results.append({'viewport':size,'screenshot':name,'observations':evidence,'page_errors':errors,'blocked_resources':blocked,'status':'findings' if evidence['horizontalOverflow'] or evidence['brokenImages'] or evidence['unlabeledButtons'] or errors or blocked else 'captured','navigation':'none / inline HTML rendering'})
                ctx.close()
        finally:b.close()
    report={'created_at':datetime.now(timezone.utc).isoformat(),'mode':'offline-html','input_filename':path.name,'results':results,'limits':['Rendered a reviewed local HTML document, not a live URL.','No navigation, authenticated origin, storage persistence, backend or network behavior verified.','External and relative resources are blocked; incomplete rendering is possible.','Geometry and label heuristics are not visual/accessibility/security certification.']}
    (folder/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);target=p.add_mutually_exclusive_group(required=True);target.add_argument('--base');target.add_argument('--html',help='Explicit offline inline-HTML rendering; no navigation/storage proof');p.add_argument('--paths',nargs='+',default=['/']);p.add_argument('--out',required=True);p.add_argument('--browser');p.add_argument('--sizes',nargs='+');p.add_argument('--allow-remote',action='store_true');p.add_argument('--allow-origin',action='append',default=[]);a=p.parse_args(argv)
    try:
        r=audit_html(a.html,a.out,a.browser,a.sizes) if a.html else audit(a.base,a.paths,a.out,a.browser,a.sizes,a.allow_remote,a.allow_origin);print(json.dumps(r,indent=2));return 0 if all(x['status']=='captured' for x in r['results']) else 1
    except Exception as exc:print(f'ERROR ({type(exc).__name__}): {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
