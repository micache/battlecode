#!/usr/bin/env python3
"""Export actual immutable identities from SQLite without another writer."""
import json
from pathlib import Path
import sqlite3
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, read_json

root = Path(read_json('/etc/battlecode/arena.json')['root'])
with sqlite3.connect('file:' + str(root / 'state/arena.sqlite') + '?mode=ro', uri=True) as db:
    db.row_factory = sqlite3.Row
    evaluations = []
    for item in db.execute('SELECT e.*,r.commit_sha,r.source_hash FROM evaluations e JOIN revisions r ON r.id=e.revision_id'):
        item = dict(item)
        for key in ('suite', 'metrics'):
            item[key] = json.loads(item[key]) if item[key] else None
        item['matches'] = [dict(row) for row in db.execute(
            'SELECT c.job_id,c.side,c.map_name,j.state,j.artifact FROM evaluation_cases c JOIN match_jobs j ON j.id=c.job_id WHERE c.evaluation_id=?',
            (item['id'],))]
        evaluations.append(item)
atomic_json(root / 'acceptance/pilot-identities.json', {'evaluations': evaluations,
    'note': 'Operator starter bootstraps are baselines, not Codex improvement cycles.'}, 0o644)
print(root / 'acceptance/pilot-identities.json')
