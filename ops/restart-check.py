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
from arena.operations import idle_workload

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--unit', choices=['arena', 'supervisor'], default='arena')
parser.add_argument('--allow-paused-queue', action='store_true',
                    help='Preserve an idle queued workload during a globally paused restart drill')
args = parser.parse_args()
require(os.geteuid() == 0, 'administrator required')
root = Path('/var/lib/battlecode-volume/supervisor')
state = Path('/srv/battlecode/public/status.json')
before = read_json(state)
require(all(w['state'] != 'RUNNING' for w in before['workers']), 'finish model tasks first')
if args.allow_paused_queue:
    require(before['paused'], 'queued-work drill requires a globally paused arena')
    require(not any(m['state'] == 'RUNNING' for m in before['matches']), 'finish active matches first')
else:
    require(all(w['paused'] for w in before['workers']), 'pause owners first')
    require(not any(m['state'] in ('RUNNING', 'QUEUED') for m in before['matches']), 'finish matches first')


database = '/srv/battlecode/state/arena.sqlite'
frozen_workload = idle_workload(database) if args.allow_paused_queue else None
old = read_json(root / (args.unit + '.json'))['identity']
require(process_identity(old['pid']) == old, 'stale process identity')
target = Path('/srv/battlecode/acceptance') / (fresh_id('restart') + '.json')
report = {'unit': args.unit, 'before': before, 'old_identity': old, 'verified': False,
          'frozen_workload': frozen_workload,
          'vm_reboot_verified': False, 'intervention': 'SIGKILL exact validated process identity'}
atomic_json(target, report, 0o644)
os.kill(old['pid'], signal.SIGKILL)
deadline = time.monotonic() + 45
while time.monotonic() < deadline:
    time.sleep(1)
    current = read_json(root / (args.unit + '.json'))['identity']
    after = read_json(state)
    if current != old and process_identity(current['pid']) == current and after['heartbeat'] > before['heartbeat']:
        preserved_workload = idle_workload(database) if args.allow_paused_queue else None
        report.update(new_identity=current, after=after,
                      recovered_workload=preserved_workload,
                      verified=([b['accepted_revision'] for b in before['bots']] ==
                                [b['accepted_revision'] for b in after['bots']] and not after['service_error'] and
                                frozen_workload == preserved_workload and
                                (not args.allow_paused_queue or after['paused'])))
        break
atomic_json(target, report, 0o644)
print(target)
require(report['verified'], 'restart not verified; inspect saved report and supervisor logs')
