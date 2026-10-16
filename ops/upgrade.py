#!/usr/bin/python3
"""Stopped-service code upgrade; preserves configuration, credentials and state."""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

source = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(source))
from arena.common import atomic_bytes, atomic_json, file_hash, read_json, require


def main():
    require(os.geteuid() == 0, "administrator required; stop all services first")
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    require(not subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip(),
            "commit changes before installing")
    handles = []
    for path in ('/srv/battlecode/state/service.lock', '/srv/battlecode/model.lock'):
        existed = Path(path).exists()
        handle = open(path, 'a')
        if not existed:
            parent = Path(path).parent.stat()
            os.fchown(handle.fileno(), parent.st_uid, parent.st_gid)
            os.fchmod(handle.fileno(), 0o660)
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        handles.append(handle)
    old = Path('/opt/battlecode')
    previous = (old / 'INFRASTRUCTURE_COMMIT').read_text().strip()
    require(previous != revision, 'already installed')
    backup = Path('/opt') / f'battlecode.previous-{previous}'
    stage = Path('/opt') / f'battlecode.staging-{revision}'
    require(not backup.exists() and not stage.exists(), 'preserve/reconcile existing upgrade copy')
    stage.mkdir(mode=0o755)
    for name in ('arena', 'ops', 'schemas', 'config', 'sources', 'evidence', 'docs'):
        shutil.copytree(source / name, stage / name, ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('AGENTS.md', 'ARENA.md', 'AUTH_AND_OPERATIONS.md', 'BOT_REFERENCE.md', 'PROMPTS.md',
                 'PLAYBOOKS.md', 'RESEARCH.md', 'RULES_CHECKLIST.md', 'pyproject.toml', '.gitignore'):
        shutil.copyfile(source / name, stage / name)
    atomic_bytes(stage / 'INFRASTRUCTURE_COMMIT', (revision + '\n').encode(), 0o644)
    old.rename(backup)
    stage.rename(old)
    config = read_json('/etc/battlecode/arena.json')
    config['infrastructure_commit'] = revision
    atomic_json('/etc/battlecode/arena.json', config, 0o644)
    lock = read_json(config['engine_lock'])
    if lock.get('isolation') == 'bubblewrap-watchdog-v1':
        lock['recipe_sha256'] = file_hash(old / 'arena/colab_sandbox.py')
        uid, gid = Path(config['engine_lock']).stat().st_uid, Path(config['engine_lock']).stat().st_gid
        atomic_json(config['engine_lock'], lock, 0o644)
        os.chown(config['engine_lock'], uid, gid)
    print(json.dumps({'installed': revision, 'previous_code_retained': str(backup),
                      'state_and_credentials': 'unchanged', 'services_started': False}))


if __name__ == '__main__':
    main()
