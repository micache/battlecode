#!/usr/bin/env python3
"""Compact live-loop status; no credential files or raw model output."""
import json
from pathlib import Path

state = json.loads(Path('/srv/battlecode/public/status.json').read_text())
report = {key: state[key] for key in ('heartbeat', 'paused', 'service_error', 'workers', 'matches', 'disk')}
report['acceptance'] = json.loads(Path('/srv/battlecode/public/acceptance.json').read_text())
report['attempts'] = {}
for worker in state['workers']:
    if not worker['task_id']:
        continue
    directory = Path('/home/bc-' + worker['id']) / 'attempts/supervisor' / worker['task_id']
    item = {'task_id': worker['task_id']}
    if (directory / 'outcome.json').exists():
        item['outcome'] = json.loads((directory / 'outcome.json').read_text())
    log = directory / 'stdout.log'
    if log.exists():
        with log.open(errors='replace') as stream:
            events = sum(1 for _ in stream)
        item.update(events=events, last_log_write=log.stat().st_mtime)
    report['attempts'][worker['id']] = item
print(json.dumps(report, indent=2))
