#!/usr/bin/env python3
"""Stopped-service migration: retain validated old finals and build diagnostics.

Run as administrator. Reads only exact registered task artifacts, never auth caches.
Database mutation is delegated to bc-arena, preserving SQLite/WAL ownership.
Original task files, patches, notes and check reports remain unchanged.
"""
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import lock, read_json, require, validate_schema
from arena.config import load
from arena.db import Database
from arena.engine import BuildError


def recover(config, finals):
    root = Path(config['root'])
    with lock(root / 'state/service.lock'), lock(root / 'model.lock'):
        db = Database(root / 'state/arena.sqlite')
        schema = read_json(Path(config['infrastructure']) / 'schemas/worker-result.schema.json')
        recovered, unavailable, diagnostics = [], [], []
        for bot in config['workers']:
            for task in db.all('SELECT * FROM tasks WHERE bot_id=? AND result IS NULL', (bot,)):
                result = finals.get(task['id'])
                if result is None:
                    unavailable.append(task['id'])
                    continue
                validate_schema(result, schema)
                envelope = json.loads(task['envelope'])
                require(result['task_id'] == task['id'] and result['bot_id'] == bot and
                        result['base_source_hash'] == envelope['base_source_hash'], 'historical identity mismatch')
                db.execute('UPDATE tasks SET result=? WHERE id=? AND result IS NULL',
                           (json.dumps(result), task['id']))
                recovered.append(task['id'])
        for row in db.all("SELECT key,value FROM meta WHERE key LIKE 'check:%'"):
            report = json.loads(row['value'])
            if not report.get('report_reference'):
                report['report_reference'] = row['key']
                db.put(row['key'], report)
            detail = report.get('detail', '')
            if report.get('diagnostics') or not detail.startswith('BUILD_FAILED: '):
                continue
            output = Path(detail.removeprefix('BUILD_FAILED: '))
            if not (output.parent.parent == root / 'builds' and re.fullmatch('[a-f0-9]{64}', output.parent.name)
                    and output.name in ('output', 'output-b') and (output / 'process-result.json').is_file()):
                continue
            process = read_json(output / 'process-result.json')
            if 'returncode' not in process:
                continue
            failure = BuildError(output, process, output.name)
            report['diagnostics'] = failure.diagnostics
            report['detail'] = str(failure)
            report['diagnostics_recovered_by_operator'] = True
            db.put(row['key'], report)
            diagnostics.append(row['key'])
        db.connection.close()
        return {'recovered_results': recovered, 'unavailable_final_results': unavailable,
                'recovered_diagnostics': diagnostics, 'original_artifacts_changed': False}


def collect(config):
    require(os.geteuid() == 0, 'administrator required; stop services first')
    finals = {}
    # Read-only task enumeration; only the delegated child writes central state.
    db = sqlite3.connect(f"file:{config['root']}/state/arena.sqlite?mode=ro", uri=True)
    for bot, settings in config['workers'].items():
        owner = read_json('/etc/battlecode/' + bot + '.json')
        require(owner['bot_id'] == bot and owner['linux_user'] == settings['linux_user'], 'owner mismatch')
        attempts = Path(owner['attempts']).resolve(strict=True)
        for (task_id,) in db.execute('SELECT id FROM tasks WHERE bot_id=? AND result IS NULL', (bot,)):
            require(re.fullmatch('task-[a-f0-9]{32}', task_id), 'unsafe task ID')
            path = attempts / task_id / '.agent' / f'final-{task_id}.json'
            require(path.resolve() == path, 'symlink in historical result path')
            if path.is_file():
                require(path.stat().st_size <= 65536, 'oversized historical result')
                finals[task_id] = read_json(path)
    db.close()
    return finals


if __name__ == '__main__':
    config = load('/etc/battlecode/arena.json')
    if sys.argv[1:] == ['--apply']:
        require(os.geteuid() != 0, 'SQLite writer must be non-root')
        print(json.dumps(recover(config, json.load(sys.stdin))))
    else:
        finals = collect(config)
        subprocess.run(['python3', '/opt/battlecode/ops/as-arena.py', 'python3',
                        '/opt/battlecode/ops/recover-worker-history.py', '--apply'],
                       input=json.dumps(finals), text=True, check=True)
