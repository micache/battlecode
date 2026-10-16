"""Run ONLY inside the game sandbox; contains no credentials."""
import errno
import json
import os
from pathlib import Path
import resource
import socket

assert os.geteuid() != 0
assert len(os.sched_getaffinity(0)) == 1
for path in ('/home/bc-alpha', '/home/bc-beta', '/home/bc-arena/.ssh', '/home/bc-arena/.codex',
             '/etc/battlecode', '/srv/battlecode/state', '/run/battlecode-colab'):
    assert not Path(path).exists(), path
assert not any('TOKEN' in key or 'API_KEY' in key for key in os.environ)
assert not list(Path('/proc').iterdir()), 'host process filesystem must not be exposed'
try:
    socket.create_connection(('1.1.1.1', 443), timeout=1)
    raise AssertionError('network reachable')
except OSError as exc:
    assert exc.errno in (errno.ENETUNREACH, errno.EACCES, errno.EPERM), str(exc)
for path in ('/toolchain/write-test', '/usr/write-test', '/write-test'):
    try:
        Path(path).touch()
        raise AssertionError('trusted tree writable')
    except OSError as exc:
        assert exc.errno in (errno.EROFS, errno.EACCES), str(exc)
assert resource.getrlimit(resource.RLIMIT_FSIZE) == (268435456, 268435456)
assert resource.getrlimit(resource.RLIMIT_NPROC) == (128, 128)
print(json.dumps({'isolation_checks': 'passed', 'uid': os.getuid(),
                  'affinity': sorted(os.sched_getaffinity(0)), 'network': 'ENETUNREACH/denied',
                  'fsize': resource.getrlimit(resource.RLIMIT_FSIZE),
                  'nproc': resource.getrlimit(resource.RLIMIT_NPROC),
                  'home_credentials': 'not mounted', 'reboot_persistence_verified': False}))
