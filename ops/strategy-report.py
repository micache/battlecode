#!/usr/bin/env python3
"""Read-only report of cumulative edit bases, independent of champion pointers."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import identity, read_json
from arena.development import select_base
from arena.service import Arena


class Ledger:
    def __init__(self, path):
        self.connection = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
        self.connection.row_factory = sqlite3.Row

    def all(self, sql, values=()):
        return [dict(row) for row in self.connection.execute(sql, values)]

    def one(self, sql, values=()):
        row = self.connection.execute(sql, values).fetchone()
        return dict(row) if row else None

    def get(self, key, default=None):
        row = self.one('SELECT value FROM meta WHERE key=?', (key,))
        return json.loads(row['value']) if row else default


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='/etc/battlecode/arena.json')
    args = parser.parse_args()
    config = read_json(args.config)
    db = Ledger(Path(config['root']) / 'state/arena.sqlite')
    try:
        lock = read_json(config['engine_lock'])
        arena = SimpleNamespace(db=db, config=config,
                                adapter=lambda: SimpleNamespace(lock=lock, lock_hash=identity(lock)))
        arena.freeze_maps = lambda: Arena.freeze_maps(arena)
        report = {}
        for bot in config['workers']:
            revision, audit = select_base(arena, bot)
            report[bot] = {'commit': revision['commit_sha'] if revision else None,
                           'source_hash': revision['source_hash'] if revision else None,
                           'selection': {k: v for k, v in audit.items() if k != 'advances'},
                           'advances': [{k: v for k, v in a.items() if k != 'evidence'}
                                        for a in audit.get('advances', [])],
                           'recent_task_bases': [{'task_id': row['id'],
                                                  'source_hash': json.loads(row['envelope'])['base_source_hash']}
                                                for row in db.all('SELECT id,envelope FROM tasks WHERE bot_id=? '
                                                                   'ORDER BY created DESC LIMIT 3', (bot,))]}
        print(json.dumps(report, indent=2))
    finally:
        db.connection.close()


if __name__ == '__main__':
    main()
