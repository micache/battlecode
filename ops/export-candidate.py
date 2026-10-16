#!/usr/bin/env python3
"""Package an immutable evaluated source using cambc bundle. Never uploads."""
import argparse
import json
from pathlib import Path
import re
import sqlite3
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, lock, require, tree_hash
from arena.config import load
from arena.engine import OfficialEngine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bot', required=True)
    parser.add_argument('--commit', required=True)
    args = parser.parse_args()
    require(re.fullmatch(r'[a-f0-9]{40}', args.commit), 'full immutable commit required')
    config = load('/etc/battlecode/arena.json')
    require(args.bot in config['workers'], 'unregistered bot')
    root = Path(config['root'])
    with lock(root / 'export.lock'):
        with sqlite3.connect('file:' + str(root / 'state/arena.sqlite') + '?mode=ro', uri=True) as db:
            db.row_factory = sqlite3.Row
            revision = db.execute('SELECT * FROM revisions WHERE bot_id=? AND commit_sha=?', (args.bot,args.commit)).fetchone()
            require(revision, 'source must already be ingested')
            evaluation = db.execute('SELECT * FROM evaluations WHERE revision_id=? AND finished IS NOT NULL ORDER BY created DESC LIMIT 1',
                                    (revision['id'],)).fetchone()
            require(evaluation, 'completed evaluation required')
            metrics = json.loads(evaluation['metrics'])
            require(not metrics['missing'] and not metrics['fault_matches'] and not metrics['unknown_reliability'],
                    'candidate has incomplete or unverified reliability evidence')
            suite = json.loads(evaluation['suite'])
        source = Path(revision['snapshot']) / 'src'
        require(tree_hash(source) == revision['source_hash'], 'immutable source changed')
        engine = OfficialEngine(config)
        label = args.bot + '-' + args.commit
        work = root / 'export-work' / label
        output = root / 'public/exports' / label
        require(not output.exists() and not work.exists(), 'export exists or was interrupted; inspect rather than overwrite')
        work.parent.mkdir(exist_ok=True)
        output.mkdir(parents=True)
        engine.prepare_project(work, {'side-a': source})
        package = output / (label + '.zip')
        process = engine.execute(work, output, ['bundle', 'side-a', '--output', '/output/' + package.name],
                                 60, 'bc-export-' + args.commit[:24])
        require(process['returncode'] == 0 and not process['timeout'] and package.is_file(), 'bundle failed; output preserved')
        package.chmod(0o644)
        manifest = {'bot':args.bot, 'commit':args.commit, 'source_hash':revision['source_hash'],
                    'package':str(package), 'package_sha256':file_hash(package),
                    'engine_version':engine.lock['version'], 'engine_sha256':engine.lock['engine_sha256'],
                    'sdk_cpp_sha256':engine.lock['sdk_cpp_sha256'], 'evaluation_id':evaluation['id'],
                    'coverage':suite['coverage'], 'wins':metrics['wins'], 'losses':metrics['losses'],
                    'common_opponent_delta':metrics['common_opponent_delta'], 'created':time.time(),
                    'official_upload_performed':False, 'contest_compliance_certified':False,
                    'note':'Source ZIP for owner review/manual upload. Provisional local results are not a full promotion gate.'}
        atomic_json(output / 'manifest.json', manifest, 0o644)
        print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
