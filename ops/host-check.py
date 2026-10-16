#!/usr/bin/env python3
"""Root-only isolation checks. Never opens owner credentials."""
import json
import os
from pathlib import Path
import pwd
import subprocess
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, read_json, require

require(os.geteuid() == 0, 'administrator required')
config = read_json('/etc/battlecode/arena.json')
checks = {}
for bot in config['workers']:
    user = pwd.getpwnam(f'bc-{bot}')
    home = Path(user.pw_dir)
    canary = home / '.arena-isolation-canary'
    if not canary.exists():
        canary.write_text('Non-secret permission test. Retained for repeatable checks.\n')
        os.chown(canary, user.pw_uid, user.pw_gid)
        canary.chmod(0o600)
    require(home.stat().st_uid == user.pw_uid and home.stat().st_mode & 0o777 == 0o700, 'home isolation failed')
    own = subprocess.run(['runuser', '-u', user.pw_name, '--', 'test', '-r', str(canary)]).returncode == 0
    foreign = [other for other in config['workers'] if other != bot]
    denied = all(subprocess.run(['runuser', '-u', f'bc-{other}', '--', 'test', '-r', str(canary)]).returncode != 0
                 for other in foreign)
    api = subprocess.run(['runuser', '-u', user.pw_name, '--', 'curl', '--noproxy', '*', '-fsS',
                          '--max-time', '3', 'http://127.0.0.1:8080/health'], capture_output=True).returncode != 0
    protected = all(subprocess.run(['runuser', '-u', user.pw_name, '--', 'test', '-w', path]).returncode != 0
                    for path in ['/run/docker.sock', '/srv/battlecode/state', '/srv/battlecode/repos/source.git',
                                 '/etc/battlecode/arena.json', '/opt/battlecode/arena'])
    sandbox = subprocess.run(['runuser', '-l', user.pw_name, '-c', '/usr/local/bin/codex sandbox -- /bin/true'],
                             capture_output=True, timeout=30).returncode == 0
    checks[bot] = {'own_canary_readable': own, 'other_owner_denied': denied, 'local_root_api_denied': api,
                   'protected_writes_denied': protected, 'native_codex_sandbox': sandbox}
image = read_json(config['engine_lock'])['image_id']
probe = """import json, pathlib, socket
p=pathlib.Path('/sys/fs/cgroup')
s=socket.socket(); s.settimeout(1)
try: s.connect(('1.1.1.1',443)); external=True
except OSError: external=False
print(json.dumps({'memory':(p/'memory.max').read_text().strip(), 'pids':(p/'pids.max').read_text().strip(),
 'cpu':(p/'cpu.max').read_text().strip(), 'external_network':external,
 'owner_home':pathlib.Path('/home/bc-alpha').exists(), 'docker_socket':pathlib.Path('/run/docker.sock').exists()}))
"""
result = subprocess.run(['python3', '/opt/battlecode/ops/as-arena.py', 'podman', '--cgroup-manager=cgroupfs',
    'run', '--rm', '--pull=never', '--network=none', '--read-only', '--cap-drop=ALL',
    '--security-opt=no-new-privileges', '--memory=128m', '--pids-limit=32', '--cpus=.5', image,
    'python3', '-c', probe], capture_output=True, text=True, timeout=60)
require(result.returncode == 0, 'container probe failed: ' + result.stderr[-1000:])
container = json.loads(result.stdout)
passed = all(all(row.values()) for row in checks.values()) and container == {
    'memory': '134217728', 'pids': '32', 'cpu': '50000 100000', 'external_network': False,
    'owner_home': False, 'docker_socket': False}
target = Path(config['root']) / 'acceptance/host-isolation.json'
atomic_json(target, {'verified': passed, 'checked_at': time.time(), 'owners': checks, 'container': container,
                    'credential_contents_read': False}, 0o644)
print(json.dumps({'path': str(target), 'verified': passed}))
require(passed, 'isolation check failed; keep workers disabled')
