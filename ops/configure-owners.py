#!/usr/bin/python3
"""Operator acknowledgement after owners manually authenticate distinct accounts.

Only native login status is inspected. Credential contents are never opened.
Workers remain paused until the operator resumes each lane through its mailbox.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, read_json, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--confirm-distinct-owner-accounts', action='store_true', required=True)
    args = parser.parse_args()
    require(os.geteuid() == 0 and args.confirm_distinct_owner_accounts, 'administrator confirmation required')
    path = Path('/etc/battlecode/arena.json')
    config = read_json(path)
    modes = {}
    for bot in config['workers']:
        owner = read_json(f'/etc/battlecode/{bot}.json')
        require(file_hash(owner['codex_executable']) == owner['codex_sha256'], 'CLI pin mismatch')
        result = subprocess.run(['runuser', '-l', f'bc-{bot}', '-c', '/usr/local/bin/codex login status'],
                                capture_output=True, text=True, timeout=30)
        status = result.stdout + result.stderr
        require(result.returncode == 0 and 'chatgpt' in status.lower() and 'api key' not in status.lower(),
                f'{bot}: manual ChatGPT login required')
        modes[bot] = 'ChatGPT; distinct-account pairing attested by operator, not read from auth cache'
        config['workers'][bot].update(enabled=True, owner_confirmed=True)
    config['limits'].setdefault('published_cycles_per_bot', 2)
    atomic_json(path, config, 0o644)
    print(json.dumps({'owner_modes': modes, 'published_cycles_per_bot': config['limits']['published_cycles_per_bot'],
                      'worker_resume': 'explicit arena-client resume required'}, indent=2))


if __name__ == '__main__':
    main()
