#!/usr/bin/env python3
"""Original local HTML/PNG/carousel/silent-MP4 studio; no model APIs or remote assets."""
from __future__ import annotations
import argparse
import base64
from datetime import datetime,timezone
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

PACK=Path(__file__).resolve().parents[1]
class MediaError(ValueError):pass

def no_links(path):
    for p in [path.absolute(),*path.absolute().parents]:
        if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()): raise MediaError(f'Linked paths are not supported: {p}')

def integer(value,name,low,high):
    if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high:raise MediaError(f'{name} must be integer {low}..{high}')
    return value

def text(v,name,limit,empty=False):
    if not isinstance(v,str) or len(v)>limit or (not v.strip() and not empty) or '\x00' in v:raise MediaError(f'{name} must be text, maximum {limit} characters')
    return v

def local_asset(parent,value):
    text(value,'asset',240)
    p=Path(value)
    if p.is_absolute() or any(x in {'..',''} for x in p.parts) or ':' in value: raise MediaError('Assets must be relative files inside the config directory')
    target=parent/p;no_links(target)
    if not target.is_file() or target.stat().st_size>8_000_000:raise MediaError('Asset missing or above 8 MB')
    try:target.resolve().relative_to(parent.resolve())
    except ValueError as exc:raise MediaError('Asset escapes configuration directory') from exc
    data=target.read_bytes();ext=target.suffix.lower();mime={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'}.get(ext)
    valid=(ext=='.png' and data.startswith(b'\x89PNG\r\n\x1a\n')) or (ext in {'.jpg','.jpeg'} and data.startswith(b'\xff\xd8\xff')) or (ext=='.webp' and data.startswith(b'RIFF') and data[8:12]==b'WEBP')
    if not mime or not valid:raise MediaError('Only genuine PNG/JPEG/WebP assets are supported')
    return 'data:'+mime+';base64,'+base64.b64encode(data).decode('ascii')

def load_config(path):
    p=Path(path).expanduser().absolute();no_links(p)
    if not p.is_file() or p.stat().st_size>200_000:raise MediaError('Configuration missing or above 200 KB')
    try:c=json.loads(p.read_text(encoding='utf-8'))
    except ValueError as exc:raise MediaError('Invalid JSON configuration') from exc
    if not isinstance(c,dict) or c.get('version')!=1:raise MediaError('Expected configuration version 1')
    if c.get('type') not in {'post','carousel','video'}:raise MediaError('type must be post, carousel or video')
    integer(c.get('width'),'width',480,3840);integer(c.get('height'),'height',480,3840)
    if c['width']/c['height']<.45 or c['width']/c['height']>2.1:raise MediaError('Supported aspect ratios: 0.45 to 2.1')
    text(c.get('brand'),'brand',40);text(c.get('signature','OPEN SOURCE / CO-FOUNDER'),'signature',48)
    th=c.get('theme')
    if not isinstance(th,dict):raise MediaError('theme is required')
    for key in ['background','foreground','accent','muted','surface','border']:
        if not isinstance(th.get(key),str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',th[key]):raise MediaError(f'theme.{key} must be a six-digit hex color')
    scenes=c.get('scenes')
    if not isinstance(scenes,list) or not 1<=len(scenes)<=12:raise MediaError('Provide 1..12 scenes')
    if c['type']=='post' and len(scenes)!=1:raise MediaError('A post has exactly one scene')
    for s in scenes:
        if not isinstance(s,dict):raise MediaError('Each scene must be an object')
        if s.get('layout') not in {'editorial','feature','steps','statement'}:raise MediaError('Unknown scene layout')
        text(s.get('eyebrow'),'eyebrow',70);text(s.get('title'),'title',100);text(s.get('body',''),'body',220,True);text(s.get('footer','ILLUSTRATIVE DEMO · NO CUSTOMER DATA'),'footer',85)
        if 'assetData' in s:raise MediaError('Use a local asset field, not embedded assetData in input')
        if 'asset' in s:s['assetData']=local_asset(p.parent,s['asset']);text(s.get('assetAlt','Approved local asset'),'assetAlt',200)
        d=s.get('diagram',{'type':'flow','items':['Understand','Verify','Deliver']})
        if not isinstance(d,dict) or d.get('type') not in {'flow','checks','statement'}:raise MediaError('Unknown diagram type')
        if not isinstance(d.get('items'),list) or not 1<=len(d['items'])<=4:raise MediaError('diagram needs 1..4 items')
        for item in d['items']:text(item,'diagram item',38)
        text(d.get('label','WORKFLOW / ILLUSTRATIVE'),'diagram label',65)
        if 'number' in d:text(d['number'],'number',5)
        if c['type']=='video':
            v=s.get('seconds')
            if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 1<=v<=20:raise MediaError('Each video scene must last 1..20 seconds')
    if c['type']=='video':
        integer(c.get('fps',24),'fps',12,60)
        if sum(s['seconds'] for s in scenes)>90:raise MediaError('Starter video must be 90 seconds or less')
        if c['width']%2 or c['height']%2:raise MediaError('MP4 dimensions must be even')
    return c

def html_for(c):
    raw=json.dumps(c,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    return (PACK/'assets/studio/template.html').read_text(encoding='utf-8').replace('__CONFIG_JSON__',raw)

def output_path(value,overwrite=False):
    p=Path(value).expanduser().absolute();no_links(p)
    if p.exists() and not overwrite:raise MediaError(f'Output exists; choose another path or pass --overwrite: {p}')
    return p

def build(config,out,overwrite=False):
    """Legacy technical fixture renderer; not the creative default."""
    c=load_config(config);p=output_path(out,overwrite)
    if p.suffix.lower()!='.html':raise MediaError('Preview output must end in .html')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html_for(c),encoding='utf-8')
    return {'path':str(p),'type':'editable standalone HTML preview','network_required':False,'rendered_export':False}

def export(config,out,browser=None,overwrite=False):
    c=load_config(config);target=output_path(out,overwrite)
    if c['type']=='post' and target.suffix.lower()!='.png':raise MediaError('Post export must end in .png')
    if c['type']=='video' and target.suffix.lower()!='.mp4':raise MediaError('Video export must end in .mp4')
    if c['type']=='carousel' and target.suffix:raise MediaError('Carousel output must be a directory without a suffix')
    if c['type']=='carousel' and target.exists():raise MediaError('Carousel destination must be new; choose another folder (never deleting arbitrary folders)')
    try:from playwright.sync_api import sync_playwright
    except ImportError as exc:raise MediaError('Optional export dependency missing. Install Playwright explicitly; see docs/MEDIA.md.') from exc
    if c['type']=='video' and not shutil.which('ffmpeg'):raise MediaError('FFmpeg is required for video export; no automatic download')
    target.parent.mkdir(parents=True,exist_ok=True)
    tempdir=Path(tempfile.mkdtemp(prefix='co-founder-render-'))
    findings=[];outputs=[];checked=[];network_blocked=[]
    try:
        with sync_playwright() as pw:
            launch={'headless':True}
            if browser:launch['executable_path']=browser
            engine=pw.chromium.launch(**launch)
            try:
                context=engine.new_context(viewport={'width':c['width'],'height':c['height']},device_scale_factor=1,reduced_motion='reduce')
                def block(route):
                    network_blocked.append(route.request.url.split('?')[0][:200]);route.abort()
                context.route('**/*',block)
                page=context.new_page();page.set_content(html_for(c),wait_until='load');page.evaluate("document.body.classList.add('export')")
                page.evaluate('document.fonts.ready');page.wait_for_timeout(40)
                total=page.evaluate('window.studio.totalFrames')
                # Every exported frame is checked for box overflow; this is not full visual QA.
                for frame in range(total):
                    page.evaluate('(n)=>window.renderFrame(n)',frame)
                    issues=page.evaluate('window.checkLayout()')
                    if issues:findings.append({'frame':frame,'issues':issues})
                    if len(findings)>=5:break
                    dest=tempdir/(f'frame{frame:06d}.png' if c['type']=='video' else f'slide-{frame+1:02d}.png')
                    page.locator('#canvas').screenshot(path=str(dest),animations='disabled');outputs.append(dest);checked.append(frame)
                if findings:raise MediaError('Layout overflow; shorten/recompose content before export: '+json.dumps(findings)[:1800])
            finally:engine.close()
        if network_blocked:raise MediaError('Unexpected network request blocked; inspect template/dependencies')
        if c['type']=='carousel':
            target.mkdir();[shutil.copy2(p,target/p.name) for p in outputs];final=[str(target/p.name) for p in outputs];receipt=target/'render-report.json'
        elif c['type']=='post':
            shutil.copy2(outputs[0],target);final=[str(target)];receipt=target.with_suffix('.render.json')
        else:
            movie=tempdir/'output.mp4'
            cmd=['ffmpeg','-hide_banner','-loglevel','error','-framerate',str(c.get('fps',24)),'-i',str(tempdir/'frame%06d.png'),'-c:v','libx264','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)]
            r=subprocess.run(cmd,capture_output=True,timeout=180)
            if r.returncode:raise MediaError('FFmpeg failed: '+r.stderr.decode('utf-8','replace')[:1500])
            shutil.copy2(movie,target);final=[str(target)];receipt=target.with_suffix('.render.json')
        # Prevent replacing an unrelated report unless explicitly requested.
        no_links(receipt)
        report={'created_at':datetime.now(timezone.utc).isoformat(),'config_type':c['type'],'dimensions':[c['width'],c['height']],
                'frames_exported':len(outputs),'overflow_frames_checked':len(checked),'overflow_findings':findings,
                'outputs':final,'audio':'none / silent','remote_requests':len(network_blocked),
                'human_visual_review':'not recorded by exporter','full_playback_review':'not recorded by exporter',
                'claims_verified':False,'note':'Original editable starter. Geometry checks do not certify taste, accessibility, factual claims or motion pacing.'}
        if receipt.exists() and not overwrite:raise MediaError(f'Report exists: {receipt}; asset was exported but report not overwritten')
        receipt.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        return report
    finally:shutil.rmtree(tempdir,ignore_errors=True)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','export']);p.add_argument('--config',required=True);p.add_argument('--out',required=True);p.add_argument('--browser');p.add_argument('--overwrite',action='store_true');a=p.parse_args(argv)
    try:
        result=build(a.config,a.out,a.overwrite) if a.action=='build' else export(a.config,a.out,a.browser,a.overwrite)
        print(json.dumps(result,indent=2));return 0
    except (MediaError,OSError,ValueError,subprocess.SubprocessError) as exc:print(f'ERROR: {exc}',file=sys.stderr);return 2
    except Exception as exc:
        # Browser errors vary by optional Playwright version. Do not claim success.
        print(f'EXPORT ERROR ({type(exc).__name__}): {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
