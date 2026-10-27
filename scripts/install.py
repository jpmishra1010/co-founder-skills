#!/usr/bin/env python3
"""Offline, conservative installer for Co-founder skills (Python 3.10+)."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MARKER = '.co-founder-install.json'
OWNER = 'co-founder-skill-pack'

class InstallError(ValueError):
    pass

def no_links(path: Path) -> None:
    """Reject symlinks / junctions in existing path components, before resolving."""
    p = path.absolute()
    for part in [p, *p.parents]:
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise InstallError(f'Refusing linked path: {part}')

def hashes(path: Path) -> dict[str, str]:
    result = {}
    no_links(path)
    if not path.is_dir():
        raise InstallError(f'Expected directory: {path}')
    for item in sorted(path.rglob('*')):
        no_links(item)
        if item.is_file() and item.name != MARKER:
            if '__pycache__' in item.parts or item.suffix == '.pyc':
                continue
            result[item.relative_to(path).as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result

def read_marker(target: Path) -> dict:
    no_links(target)
    marker = target / MARKER
    if not marker.is_file():
        raise InstallError(f'Unmanaged destination exists; refusing to replace it: {target}')
    try:
        data = json.loads(marker.read_text(encoding='utf-8'))
    except (ValueError, OSError) as exc:
        raise InstallError(f'Unreadable install marker: {target}') from exc
    if data.get('owner') != OWNER or not isinstance(data.get('files'), dict):
        raise InstallError(f'Unrecognized install marker: {target}')
    return data

def copy_clean(source: Path, dest: Path) -> None:
    no_links(source)
    for item in sorted(source.rglob('*')):
        no_links(item)
        if '__pycache__' in item.parts or item.suffix == '.pyc' or item.name == MARKER:
            continue
        rel = item.relative_to(source)
        out = dest / rel
        if item.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, out)
        else:
            raise InstallError(f'Unsupported source entry: {item}')

def backup(target: Path, backup_root: Path) -> Path:
    no_links(backup_root)
    backup_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest = backup_root / f'{target.name}-{stamp}'
    shutil.copytree(target, dest)
    return dest

def install_one(source: Path, target: Path, backup_root: Path, *, update=False,
                replace_modified=False, dry_run=False) -> str:
    source_hash = hashes(source)
    no_links(target)
    old = None
    if target.exists():
        old = read_marker(target)
        current = hashes(target)
        modified = current != old['files']
        if modified and not replace_modified:
            raise InstallError(f'Local edits detected: {target}. Back them up manually or use --update --replace-modified for a backed-up replacement.')
        if current == source_hash and not modified:
            return f'unchanged: {target}'
        if not update:
            raise InstallError(f'Different installed version: {target}. Review changes and rerun with --update.')
        if replace_modified and not update:
            raise InstallError('--replace-modified requires --update')
    if dry_run:
        return f'would {"update" if old else "install"}: {target}'
    target.parent.mkdir(parents=True, exist_ok=True)
    no_links(target.parent)
    temp = Path(tempfile.mkdtemp(prefix='.co-founder-staging-', dir=target.parent))
    try:
        copy_clean(source, temp)
        marker = {'owner': OWNER, 'version': (ROOT/'VERSION').read_text().strip(),
                  'installed_at': datetime.now(timezone.utc).isoformat(), 'files': source_hash}
        (temp/MARKER).write_text(json.dumps(marker, indent=2)+'\n', encoding='utf-8')
        if old:
            saved = backup(target, backup_root)
            shutil.rmtree(target)
        else:
            saved = None
        os.replace(temp, target)
        return f'{"updated" if old else "installed"}: {target}' + (f' (backup: {saved})' if saved else '')
    finally:
        if temp.exists():
            shutil.rmtree(temp)

def uninstall_one(target: Path, backup_root: Path, *, force=False, dry_run=False) -> str:
    no_links(target)
    if not target.exists():
        return f'not installed: {target}'
    marker = read_marker(target)
    modified = hashes(target) != marker['files']
    if modified and not force:
        raise InstallError(f'Local edits detected; leaving {target} intact. --force backs up then removes a managed installation.')
    if dry_run:
        return f'would back up and uninstall: {target}'
    saved = backup(target, backup_root)
    shutil.rmtree(target)
    return f'uninstalled: {target} (backup: {saved})'

def locations(host: str, scope: str, project: str | None, home: str | None):
    base = Path(project).expanduser().absolute() if scope == 'project' and project else Path(home).expanduser().absolute() if home else Path.home()
    if scope == 'project' and not project:
        raise InstallError('--project is required for project scope')
    no_links(base)
    if not base.is_dir():
        raise InstallError(f'Base directory must already exist: {base}')
    hosts = ['codex', 'claude'] if host == 'both' else [host]
    for h in hosts:
        parent = base / ('.agents' if h == 'codex' else '.claude')
        yield h, parent/'skills', parent/'.co-founder-backups'

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['install','uninstall','status'])
    p.add_argument('--host', choices=['codex','claude','both'], default='both')
    p.add_argument('--scope', choices=['user','project'], default='user')
    p.add_argument('--project')
    p.add_argument('--home', help='Explicit home directory override, useful for portable setups/tests')
    p.add_argument('--mode', choices=['lite','full'], default='lite', help='lite installs all workflows behind one entry; full also installs direct specialist entries')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--update', action='store_true')
    p.add_argument('--replace-modified', action='store_true')
    p.add_argument('--force', action='store_true', help='uninstall managed locally edited files only after backup')
    args = p.parse_args(argv)
    try:
        if args.replace_modified and not args.update:
            raise InstallError('--replace-modified requires --update')
        if args.force and args.action != 'uninstall':
            raise InstallError('--force is only for uninstall')
        names = ['co-founder']
        if args.mode == 'full':
            names += [f'co-founder-{n}' for n in json.loads((ROOT/'manifest.json').read_text())['specialists']]
        # Preflight all targets before any mutation, avoiding ordinary partial installs.
        locs = list(locations(args.host,args.scope,args.project,args.home))
        plans = [(ROOT/'skills'/name, dest/name, backups) for _, dest, backups in locs for name in names]
        for source,target,backups in plans:
            if args.action == 'install':
                install_one(source,target,backups,update=args.update,replace_modified=args.replace_modified,dry_run=True)
            elif args.action == 'uninstall':
                uninstall_one(target,backups,force=args.force,dry_run=True)
        for source,target,backups in plans:
            if args.action == 'install':
                print(install_one(source,target,backups,update=args.update,replace_modified=args.replace_modified,dry_run=args.dry_run))
            elif args.action == 'uninstall':
                print(uninstall_one(target,backups,force=args.force,dry_run=args.dry_run))
            else:
                if not target.exists(): print(f'not installed: {target}')
                else:
                    marker=read_marker(target)
                    print(f'{target}: version={marker.get("version","unknown")}; locally_modified={hashes(target)!=marker["files"]}')
        if args.action == 'install' and args.mode == 'lite':
            print('Lite includes all 13 workflows. Previously installed specialist wrappers are not removed; uninstall --mode full to remove them explicitly.')
        return 0
    except (InstallError,OSError,ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
