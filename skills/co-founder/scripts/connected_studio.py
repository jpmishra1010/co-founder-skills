#!/usr/bin/env python3
"""Render an explicitly approved, project-local HTML composition with bound assets.

Not a universal design generator. Templates execute JavaScript: inspect them first.
The optional browser blocks network requests; that is not a full execution sandbox.
No model APIs. No font redistribution. All exports remain subject to craft review.
"""
from __future__ import annotations
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cf_project_context_studio',HERE/'project_context.py')
pc=importlib.util.module_from_spec(spec);spec.loader.exec_module(pc)
class StudioError(ValueError):pass

def asset_data(path):
    path=pc.plain_path(path);
    if path.stat().st_size>pc.MAX_ASSET:raise StudioError('Asset exceeds size bound')
    data=path.read_bytes();ext=path.suffix.lower()
    if len(data)>pc.MAX_ASSET:raise StudioError('Asset exceeds size bound')
    allowed={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.svg':'image/svg+xml'}
    if ext not in allowed:raise StudioError('Inline asset must be PNG/JPEG/WebP/SVG')
    if ext=='.png' and not data.startswith(b'\x89PNG\r\n\x1a\n'):raise StudioError('Invalid PNG signature')
    if ext in {'.jpg','.jpeg'} and not data.startswith(b'\xff\xd8\xff'):raise StudioError('Invalid JPEG signature')
    if ext=='.webp' and not (data[:4]==b'RIFF' and data[8:12]==b'WEBP'):raise StudioError('Invalid WebP signature')
    if ext=='.svg':
        if len(data)>1_000_000:raise StudioError('SVG too large')
        if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():raise StudioError('SVG entities are not allowed')
        try:tree=ET.fromstring(data)
        except ET.ParseError as exc:raise StudioError('Invalid SVG') from exc
        if tree.tag.split('}')[-1]!='svg':raise StudioError('Not an SVG root')
        for e in tree.iter():
            tag=e.tag.split('}')[-1].lower()
            if tag not in {'svg','g','path','rect','circle','ellipse','line','polyline','polygon','text','tspan','title','desc','defs'}:raise StudioError('SVG must be self-contained vector artwork without embedded code/media')
            for k,v in e.attrib.items():
                key=k.split('}')[-1].lower()
                if key.startswith('on') or key in {'href','src','style'} or 'url(' in v.lower() or '@import' in v.lower():raise StudioError('Active or external SVG content rejected')
    return 'data:'+allowed[ext]+';base64,'+base64.b64encode(data).decode('ascii')

def compose(project,template,surface,brand=None):
    binding=pc.bundle(project,surface,brand)
    root=Path(binding['root']);source=pc.safe_relative(root,template)
    if source.suffix.lower()!='.html' or not source.is_file() or source.stat().st_size>1_000_000:raise StudioError('Expected a project-local HTML template under 1 MB')
    html=source.read_text(encoding='utf-8')
    if html.count('__BRAND_JSON__')!=1:raise StudioError('Template must contain exactly one __BRAND_JSON__ slot')
    payload={k:binding[k] for k in ['project_id','display_name','brand','surface','tokens','typography']}
    payload['assets']={a['id']:asset_data(a['absolute_path']) for a in binding['assets'] if Path(a['path']).suffix.lower() in {'.svg','.png','.jpg','.jpeg','.webp'}}
    raw=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    return html.replace('__BRAND_JSON__',raw),binding,pc.digest(source)

def destination(out,overwrite):
    p=pc.plain_path(out)
    if p.exists() and not overwrite:raise StudioError('Output exists; choose a new file or pass --overwrite explicitly')
    p.parent.mkdir(parents=True,exist_ok=True)
    return p

def build(project,template,surface,out,brand=None,overwrite=False):
    p=destination(out,overwrite)
    if p.suffix!='.html':raise StudioError('Build output must be HTML')
    html,b,sha=compose(project,template,surface,brand)
    p.write_text(html,encoding='utf-8')
    return {'path':str(p),'project_id':b['project_id'],'surface':b['surface'],'bundle_fingerprint':b['fingerprint'],'template_sha256':sha,'rendered':False,'human_accepted':False}

def export(project,template,surface,out,brand=None,browser=None,width=1440,height=1000,overwrite=False):
    if type(width)!=int or type(height)!=int or not 320<=width<=3840 or not 320<=height<=3840:raise StudioError('Dimensions must be integers within 320..3840')
    p=destination(out,overwrite)
    movie=surface=='video'
    if p.suffix!=('.mp4' if movie else '.png'):raise StudioError('Video needs MP4; other surfaces need PNG')
    receipt=p.with_suffix('.render.json');pc.plain_path(receipt)
    if receipt.exists() and not overwrite:raise StudioError('Render receipt exists; choose a new destination')
    html,b,sha=compose(project,template,surface,brand)
    try:from playwright.sync_api import sync_playwright
    except ImportError as exc:raise StudioError('Install optional Playwright/browser explicitly; see docs/MEDIA.md') from exc
    if movie and not shutil.which('ffmpeg'):raise StudioError('FFmpeg required for video; not installed automatically')
    with tempfile.TemporaryDirectory(prefix='cf-connected-') as td:
        tmp=Path(td);blocked=[];errors=[];issues=[];frames=1;fps=None;duration=None;safe_elements=0;viewport={'width':width,'height':height}
        with sync_playwright() as pw:
            opts={'headless':True}
            if browser:opts['executable_path']=browser
            engine=pw.chromium.launch(**opts)
            try:
                context=engine.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
                context.route('**/*',lambda route:(blocked.append(route.request.url.split('?')[0]),route.abort())[-1])
                page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
                page.set_content(html,wait_until='load');page.evaluate('document.fonts.ready')
                if movie:
                    info=page.evaluate('window.motionSpec')
                    if not isinstance(info,dict):raise StudioError('Video must expose window.motionSpec')
                    fps=info.get('fps');duration=info.get('seconds');w=info.get('width');h=info.get('height')
                    if type(fps)!=int or not 12<=fps<=60 or type(duration) not in {int,float} or not 1<=duration<=90:raise StudioError('Invalid movie duration/fps')
                    if type(w)!=int or type(h)!=int or not 320<=w<=3840 or not 320<=h<=3840 or w%2 or h%2:raise StudioError('Movie dimensions must be even, 320..3840')
                    frames=round(fps*duration);width=w;height=h;page.set_viewport_size({'width':w,'height':h})
                    page.evaluate('window.CF_EXPORT=true')
                elif page.locator('#stage').count():
                    rect=page.locator('#stage').bounding_box()
                    if rect:width=round(rect['width']);height=round(rect['height']);page.set_viewport_size({'width':width,'height':height})
                safe_elements=page.locator('[data-safe]').count()
                viewport=page.viewport_size
                for frame in range(frames):
                    if movie:page.evaluate('(t)=>window.renderAt(t)',frame/fps)
                    found=page.evaluate('''() => { const stage=document.querySelector('#stage')||document.documentElement; const box=stage.getBoundingClientRect(); const out=[]; for(const e of document.querySelectorAll('[data-safe]')) {const s=getComputedStyle(e), r=e.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0)continue;if(r.left<box.left-1||r.top<box.top-1||r.right>box.right+1||r.bottom>box.bottom+1)out.push((e.id||e.tagName)+':outside-safe-frame');}return out;}''')
                    if found:issues.append({'frame':frame,'issues':found})
                    if len(issues)>5:raise StudioError('Safe-frame failures: '+json.dumps(issues))
                    target=tmp/f'frame{frame:06d}.png'
                    if page.locator('#stage').count():page.locator('#stage').screenshot(path=str(target),animations='disabled')
                    else:page.screenshot(path=str(target),full_page=True,animations='disabled')
            finally:engine.close()
        if blocked or errors or issues:raise StudioError('Browser errors/network/safe-frame failures: '+json.dumps({'network':blocked,'errors':errors,'issues':issues})[:1800])
        # Rebinding detects changed source assets before publishing an export.
        after=pc.bundle(project,surface,brand)
        if after['fingerprint']!=b['fingerprint'] or pc.digest(pc.safe_relative(Path(b['root']),template))!=sha:raise StudioError('Project/brand/template changed during rendering; re-review')
        if movie:
            target=tmp/'output.mp4'
            cmd=['ffmpeg','-hide_banner','-loglevel','error','-framerate',str(fps),'-i',str(tmp/'frame%06d.png'),'-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
            done=subprocess.run(cmd,capture_output=True,timeout=240)
            if done.returncode:raise StudioError('FFmpeg failed: '+done.stderr.decode('utf-8','replace')[:700])
        else:target=tmp/'frame000000.png'
        shutil.copy2(target,p)
        if not movie:
            # PNG IHDR contains the actual full-page pixel dimensions.
            import struct
            with p.open('rb') as image:
                header=image.read(24)
            width,height=struct.unpack('>II',header[16:24])
    report={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'project_id':b['project_id'],'brand':b['brand'],'surface':b['surface'],'bundle_fingerprint':b['fingerprint'],
            'template_sha256':sha,'artifact_sha256':pc.digest(p),'width':width,'height':height,'frames':frames,'fps':fps,'seconds':duration,
            'viewport':viewport,'safe_elements':safe_elements,'safe_frames_checked':frames if safe_elements else 0,'network_requests':len(blocked),'javascript_errors':errors,'audio':'silent' if movie else 'not-applicable',
            'human_visual_acceptance':False,'full_playback_review':'not-performed-by-renderer',
            'limits':'Safe-frame geometry is not a craft, accessibility, behavior or security verdict.'}
    receipt.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report|{'path':str(p),'receipt':str(receipt)}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','export']);p.add_argument('--project',required=True);p.add_argument('--template',required=True);p.add_argument('--surface',choices=['product-ui','website','post','video'],required=True);p.add_argument('--brand');p.add_argument('--out',required=True);p.add_argument('--browser');p.add_argument('--width',type=int,default=1440);p.add_argument('--height',type=int,default=1000);p.add_argument('--overwrite',action='store_true');a=p.parse_args(argv)
    try:
        if a.action=='build':r=build(a.project,a.template,a.surface,a.out,a.brand,a.overwrite)
        else:r=export(a.project,a.template,a.surface,a.out,a.brand,a.browser,a.width,a.height,a.overwrite)
        print(json.dumps(r,indent=2));return 0
    except Exception as exc:
        print(f'STUDIO BLOCKED ({type(exc).__name__}): {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
