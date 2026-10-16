#!/usr/bin/env python3
"""Pin the installed official CLI; install public host trust. No owner login."""
import os
from pathlib import Path
import pwd
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_bytes, atomic_json, file_hash, read_json, require

require(os.geteuid() == 0, 'administrator required')
binary = '/usr/local/bin/codex'
expected = '399ff69c431c066e40de318fba45c2b07f45a76b19939d247ee4828fc70c4215'
require(file_hash(binary) == expected, 'review official CLI binary update before pinning')
config = read_json('/etc/battlecode/arena.json')
for bot in config['workers']:
    path = Path(f'/etc/battlecode/{bot}.json')
    owner = read_json(path)
    owner.update(codex_executable=binary, codex_sha256=expected)
    atomic_json(path, owner, 0o644)
    user = pwd.getpwnam(owner['linux_user'])
    runtime = Path(user.pw_dir) / '.runtime'
    runtime.mkdir(mode=0o700, exist_ok=True)
    os.chown(runtime, user.pw_uid, user.pw_gid)
arena = pwd.getpwnam('bc-arena')
known = Path(arena.pw_dir) / '.ssh/known_hosts'
host = b'github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl\n'
if known.exists():
    require(known.read_bytes() == host, 'preserve existing host trust; inspect before changing')
else:
    atomic_bytes(known, host, 0o600)
    os.chown(known, arena.pw_uid, arena.pw_gid)
print('CLI pinned; owner login remains manual; existing credentials unchanged.')
