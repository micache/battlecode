#!/usr/bin/env python3
"""Controlled service crash drill. Refuses active matches or model tasks."""
import argparse
import os
from pathlib import Path
import signal
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, fresh_id, read_json, require
from arena.colab_sandbox import process_identity

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--unit', choices=['arena', 'supervisor'], default='arena')
args = parser.parse_args()
require(os.geteuid() == 0, 'administrator required')
root = Path('/var/lib/battlecode-volume/supervisor')
state = Path('/srv/battlecode/public/status.json')
before = read_json(state)
require(all(w['paused'] and w['state'] != 'RUNNING' for w in before['workers']), 'pause owners first')
require(not any(m['state'] in ('RUNNING', 'QUEUED') for m in before['matches']), 'finish matches first')
old = read_json(root / (args.unit + '.json'))['identity']
require(process_identity(old['pid']) == old, 'stale process identity')
target = Path('/srv/battlecode/acceptance') / (fresh_id('restart') + '.json')
report = {'unit': args.unit, 'before': before, 'old_identity': old, 'verified': False,
          'vm_reboot_verified': False, 'intervention': 'SIGKILL exact validated process identity'}
atomic_json(target, report, 0o644)
os.kill(old['pid'], signal.SIGKILL)
deadline = time.monotonic() + 45
while time.monotonic() < deadline:
    time.sleep(1)
    current = read_json(root / (args.unit + '.json'))['identity']
    after = read_json(state)
    if current != old and process_identity(current['pid']) == current and after['heartbeat'] > before['heartbeat']:
        report.update(new_identity=current, after=after,
                      verified=([b['accepted_revision'] for b in before['bots']] ==
                                [b['accepted_revision'] for b in after['bots']] and not after['service_error']))
        break
atomic_json(target, report, 0o644)
print(target)
require(report['verified'], 'restart not verified; inspect saved report and supervisor logs')
