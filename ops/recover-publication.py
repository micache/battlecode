#!/usr/bin/env python3
"""Recover a valid candidate after the known experiment-artifact publisher bug.

Run as root with services stopped. Capture runs under its owner; the central
writer runs as bc-arena. No Codex invocation or credential-cache access.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import lock, read_json, require

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bot', required=True)
parser.add_argument('--task-id', required=True)
parser.add_argument('--mode', choices=('operator', 'capture', 'apply'), default='operator')
args = parser.parse_args()
config = read_json('/etc/battlecode/arena.json')
require(args.bot in config['workers'], 'unregistered bot')
import re
require(re.fullmatch('task-[a-f0-9]{32}', args.task_id), 'invalid task ID')
script = '/opt/battlecode/ops/recover-publication.py'
common = ['python3', script, '--bot', args.bot, '--task-id', args.task_id]
if args.mode == 'operator':
    require(os.geteuid() == 0, 'administrator required; stop services first')
    user = config['workers'][args.bot]['linux_user']
    payload = subprocess.check_output(['runuser', '-u', user, '--', *common, '--mode', 'capture'], text=True)
    subprocess.run(['python3', '/opt/battlecode/ops/as-arena.py', *common, '--mode', 'apply'],
                   input=payload, text=True, check=True)
elif args.mode == 'capture':
    from arena.client import owner_config
    from arena.worker import candidate_payload
    owner = owner_config('/etc/battlecode/' + args.bot + '.json')
    print(json.dumps(candidate_payload(owner, Path(owner['attempts']) / args.task_id)))
else:
    from arena.config import load
    from arena.publisher import recover_publication
    from arena.service import Arena
    require(os.geteuid() != 0, 'central writer must be non-root')
    with lock(Path(config['root']) / 'state/service.lock'), lock(Path(config['root']) / 'model.lock'):
        arena = Arena(load('/etc/battlecode/arena.json'))
        result = recover_publication(arena, args.bot, json.load(sys.stdin))
        arena.export_status()
        print(json.dumps(result))
