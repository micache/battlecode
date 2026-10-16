#!/usr/bin/env python3
"""POSIX filesystem on a provider volume whose virtiofs ignores guest chown.

Formats ONLY a newly-created, named image file. Never formats a device or an
existing image. Initial migration refuses authenticated homes and retains all
original directories. Subsequent starts only remount the same filesystem.
"""
import os
from pathlib import Path
import shutil
import subprocess

IMAGE = Path('/persist/battlecode-data.ext4')
DATA = Path('/var/lib/battlecode-volume')


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def main():
    if os.geteuid() != 0 or not Path('/persist').is_mount():
        raise RuntimeError('root and mounted Blaxel volume required')
    created = False
    if not IMAGE.exists():
        if shutil.disk_usage('/persist').free < 7 * 1024**3:
            raise RuntimeError('insufficient space for the 7 GiB POSIX filesystem')
        with IMAGE.open('xb') as stream:
            stream.truncate(7 * 1024**3)
            stream.flush()
            os.fsync(stream.fileno())
        created = True
        run('mkfs.ext4', '-m', '0', '-L', 'battlecode-arena', str(IMAGE))
    DATA.mkdir(mode=0o755, exist_ok=True)
    if not DATA.is_mount():
        # Mount refuses unformatted/partial images; they are preserved for recovery.
        run('mount', '-o', 'loop,nodev,nosuid', str(IMAGE), str(DATA))
    DATA.chmod(0o711)
    marker = DATA / '.initial-migration-complete'
    if not marker.exists():
        for name in ('bc-arena', 'bc-alpha', 'bc-beta'):
            home = Path('/persist/homes') / name
            if (home / '.codex').exists() or (home / '.ssh/id_ed25519').exists():
                raise RuntimeError('authenticated original home requires owner-directed migration')
        for name in ('config', 'arena', 'homes'):
            source, destination = Path('/persist') / name, DATA / name
            if source.exists():
                if destination.exists():
                    raise RuntimeError('partial migration retained; inspect before continuing')
                shutil.copytree(source, destination)
        marker.write_text('Initial unauthenticated setup copied; originals retained under /persist.\n')
    for target, old, new in [('/etc/battlecode', '/persist/config', DATA / 'config'),
                             ('/srv/battlecode', '/persist/arena', DATA / 'arena'),
                             *((f'/home/{name}', f'/persist/homes/{name}', DATA / 'homes' / name)
                               for name in ('bc-arena', 'bc-alpha', 'bc-beta'))]:
        link = Path(target)
        if not link.exists() and not link.is_symlink():
            # Fresh first installation: homes are created by useradd in blaxel-host.py.
            if str(target).startswith('/home/') and not new.exists():
                continue
            new.mkdir(mode=0o755, parents=True, exist_ok=True)
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(new, target_is_directory=True)
            continue
        if link.is_symlink() and link.resolve() == Path(old):
            link.unlink()
            link.symlink_to(new, target_is_directory=True)
        elif not (link.is_symlink() and link.resolve() == new):
            raise RuntimeError(f'preserve unexpected link: {target}')
    print({'filesystem': str(DATA), 'created': created, 'image': str(IMAGE), 'originals_retained': True})


if __name__ == '__main__':
    main()
