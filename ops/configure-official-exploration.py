#!/usr/bin/env python3
"""Stopped-service owner-authorized v6 exploration; never changes live submissions."""
import json
import os
from pathlib import Path
import sqlite3
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, lock, read_json, require
from arena.config import load


def main():
    require(os.geteuid() == 0, 'administrator required')
    path = Path('/etc/battlecode/arena.json')
    config = read_json(path)
    with lock(Path(config['root']) / 'state/service.lock'), lock(Path(config['root']) / 'model.lock'):
        with sqlite3.connect('file:' + config['root'] + '/state/arena.sqlite?mode=ro', uri=True) as db:
            row = db.execute('SELECT source_hash FROM revisions WHERE bot_id=? AND commit_sha=?',
                             ('alpha', '82a14a04f0e6b68aac8a7e879d305b1a886b857c')).fetchone()
        require(row and row[0] == '6e362fd7cce836975fa615bc8b936109235fd320def63703761366586efabc25',
                'reviewed v6 source is not registered')
        require(config['engine']['version'] == '2.2.5', 'reviewed official CLI required')
        atomic_json(path.with_name('arena.before-official-' + str(time.time_ns()) + '.json'), config, 0o600)
        config['official']['challenges'] = True
        config['official_exploration'] = {
            'enabled':True, 'owner_authorized':True, 'interface':'cambc-225-match-groups',
            'team_id':'87bb1c13-b46d-4c4f-ad8c-e9284054dcd6',
            'submission_id':'a2f2ee53-88b2-4821-b06d-ac630b9d7eae', 'bot_id':'alpha',
            'source_commit':'82a14a04f0e6b68aac8a7e879d305b1a886b857c', 'source_hash':row[0],
            'package_sha256':'d0e68d104b39864bff29be34603f0a23552daf2c3d2d70769baf59ec2070f00f',
            'interval_seconds':72, 'max_outstanding':50, 'share_feedback':True,
            'archive_budget_bytes':256*1024**2, 'feedback_budget_bytes':128*1024**2,
            'authorization':'Owner 19 October: use selected v6 C++; utilize shared 50/hour unranked allowance.',
            'limits':'No uploads, activation, private opponent files, paid fallback or contest-compliance certification.'}
        atomic_json(path, config, 0o644)
        load(path)
        print(json.dumps({'enabled':True, 'target_groups_per_hour':50,
                          'submission_id':config['official_exploration']['submission_id'],
                          'services_started':False, 'uploads_or_activation':False}))


if __name__ == '__main__':
    main()
