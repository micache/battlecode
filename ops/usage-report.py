#!/usr/bin/env python3
"""Read-only native CLI efficiency report; never reads owner credentials."""
import json
from pathlib import Path
import sqlite3
import time

config = json.loads(Path('/etc/battlecode/arena.json').read_text())
db = sqlite3.connect(f"file:{config['root']}/state/arena.sqlite?mode=ro", uri=True)
db.row_factory = sqlite3.Row
report = {'window_hours': 5, 'bots': {}, 'interpretation':
          'Observed token/output counts, not remaining subscription quota, dollars or proof of strategic gain.'}
for bot in config['workers']:
    rows = db.execute('SELECT id,state FROM tasks WHERE bot_id=? AND created>? ORDER BY created',
                      (bot, time.time() - 5 * 3600)).fetchall()
    totals = {}
    profiles = {}
    known = commands = output_bytes = 0
    for row in rows:
        value = db.execute('SELECT value FROM meta WHERE key=?', (f"invocation:{row['id']}",)).fetchone()
        invocation = json.loads(value[0]) if value else {}
        usage = invocation.get('usage', {})
        if usage.get('reported_tokens') is not None:
            known += 1
            for key, count in usage['reported_tokens'].items():
                totals[key] = totals.get(key, 0) + count
            profile = profiles.setdefault(invocation.get('efficiency_profile', 'unknown'),
                                          {'tasks_with_usage': 0, 'input_tokens_not_read_from_cache': 0, 'output_tokens': 0})
            profile['tasks_with_usage'] += 1
            for key in ('input_tokens_not_read_from_cache', 'output_tokens'):
                profile[key] += usage['reported_tokens'].get(key, 0)
        commands += usage.get('completed_command_events', 0)
        output_bytes += usage.get('command_output_bytes', 0)
    report['bots'][bot] = {'tasks': len(rows), 'published': sum(row['state'] == 'PUBLISHED' for row in rows),
                           'usage_known_tasks': known, 'usage_unknown_tasks': len(rows) - known,
                           'reported_tokens': totals or None, 'reported_command_events': commands,
                           'profiles': profiles,
                           'reported_command_output_bytes': output_bytes}
print(json.dumps(report, indent=2))
