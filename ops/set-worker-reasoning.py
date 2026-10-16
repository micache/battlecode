#!/usr/bin/env python3
"""Pin native CLI defaults for future jobs; leave active jobs/auth untouched."""
import argparse
import json
import os
from pathlib import Path
import pwd
import re
import sys
import time
import tomllib

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_bytes, read_json, require


def pin_settings(text, model, effort):
    original = tomllib.loads(text)
    # Change only root keys, retaining project/profile tables and unrelated settings.
    lines = text.splitlines(keepends=True)
    boundary = next((i for i, line in enumerate(lines) if line.lstrip().startswith('[')), len(lines))
    head = ''.join(lines[:boundary])
    head = re.sub(r'(?m)^[ \t]*(?:model|model_reasoning_effort)[ \t]*=.*(?:\n|$)', '', head)
    updated = f'model = {json.dumps(model)}\nmodel_reasoning_effort = {json.dumps(effort)}\n' + head + ''.join(lines[boundary:])
    require(tomllib.loads(updated) == dict(original, model=model, model_reasoning_effort=effort),
            'unusual TOML layout; preserve config and edit explicitly')
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--effort', choices=['low', 'medium', 'high', 'xhigh', 'max'], required=True)
    parser.add_argument('--model', default='gpt-6.1-sol')
    args = parser.parse_args()
    require(os.geteuid() == 0, 'administrator required')
    config = read_json('/etc/battlecode/arena.json')
    for bot, lane in config['workers'].items():
        user = pwd.getpwnam(lane['linux_user'])
        directory = Path(user.pw_dir) / '.codex'
        require(directory.is_dir() and directory.stat().st_uid == user.pw_uid, 'owner CLI directory missing/mismatched')
        path = directory / 'config.toml'
        require(not path.is_symlink(), 'preserve unexpected config symlink')
        before = path.read_text() if path.exists() else ''
        updated = pin_settings(before, args.model, args.effort)
        if updated != before:
            backup = directory / f'config.before-arena-model-{time.time_ns()}.toml'
            atomic_bytes(backup, before.encode(), 0o600)
            os.chown(backup, user.pw_uid, user.pw_gid)
            atomic_bytes(path, updated.encode(), 0o600)
            os.chown(path, user.pw_uid, user.pw_gid)
        print(json.dumps({'bot': bot, 'model': args.model, 'reasoning_effort': args.effort,
                          'applies': 'next native CLI invocation', 'active_jobs_interrupted': False}))


if __name__ == '__main__':
    main()
