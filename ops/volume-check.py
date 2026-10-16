#!/usr/bin/env python3
"""Stopped-service unmount/remount drill; never reads credential contents."""
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, lock, read_json, require
from arena.colab_sandbox import process_identity

require(os.geteuid() == 0, 'administrator required')
data = Path('/var/lib/battlecode-volume')
supervisor = read_json(data / 'supervisor/supervisor.json')['identity']
require(process_identity(supervisor['pid']) != supervisor, 'stop services first')
# Acquiring and then releasing both locks confirms there is no active writer.
# Do not keep file descriptors on the filesystem while unmounting it.
with lock(data / 'arena/state/service.lock'), lock(data / 'arena/model.lock'):
    pass
paths = [data / 'config/arena.json', data / 'arena/state/arena.sqlite']
before = {str(p.relative_to(data)): file_hash(p) for p in paths}
users = {p.name: {'uid': p.stat().st_uid, 'gid': p.stat().st_gid, 'mode': p.stat().st_mode & 0o777}
         for p in (data / 'homes').iterdir() if p.is_dir()}
os.sync()
subprocess.run(['umount', str(data)], check=True)
try:
    require(not data.is_mount(), 'filesystem did not unmount')
finally:
    subprocess.run(['python3', '/opt/battlecode/ops/blaxel-volume.py'], check=True)
after = {str(p.relative_to(data)): file_hash(p) for p in paths}
after_users = {name: {'uid': (data/'homes'/name).stat().st_uid, 'gid': (data/'homes'/name).stat().st_gid,
                       'mode': (data/'homes'/name).stat().st_mode & 0o777} for name in users}
passed = before == after and users == after_users
atomic_json(data / 'arena/acceptance/volume-remount.json', {'verified': passed, 'before': before, 'after': after,
    'homes_before': users, 'homes_after': after_users, 'credential_contents_read': False,
    'vm_reboot_verified': False}, 0o644)
require(passed, 'persistent bytes or ownership changed; keep services stopped')
print('Persistent database/config bytes and owner UID/GID/modes survived unmount/remount.')
