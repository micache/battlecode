#!/usr/bin/env python3
"""Await the owner-promised beta upload; never upload or select a live bot."""
import argparse
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review-throttle-stop', action='store_true',
                        help='Explicit operator review of the saved read-command HTTP 429 stop')
    args = parser.parse_args()
    require(os.geteuid() == 0, 'administrator required')
    path = Path('/etc/battlecode/arena.json')
    config = read_json(path)
    with lock(Path(config['root']) / 'state/service.lock'), lock(Path(config['root']) / 'model.lock'):
        with sqlite3.connect('file:' + config['root'] + '/state/arena.sqlite?mode=ro', uri=True) as db:
            row = db.execute('SELECT source_hash FROM revisions WHERE bot_id=? AND commit_sha=?',
                             ('beta', '7cab9b0f6b948b0ea0b3b284425a3501c564d16b')).fetchone()
        require(row and row[0] == 'fd5e25543653c9a8774346212b3f689927a9dd489b1ba2373a1edd0889bf63aa',
                'reviewed beta source is not registered')
        require(config['engine']['version'] == '2.2.5', 'reviewed official CLI required')
        atomic_json(path.with_name('arena.before-official-' + str(time.time_ns()) + '.json'), config, 0o600)
        config['official']['challenges'] = True
        config['official_exploration'] = {
            'enabled':True, 'owner_authorized':True, 'interface':'cambc-225-match-groups',
            'team_id':'87bb1c13-b46d-4c4f-ad8c-e9284054dcd6',
            'submission_id':None, 'bot_id':'beta', 'awaiting_submission':True, 'require_selection_proof':True,
            'source_commit':'7cab9b0f6b948b0ea0b3b284425a3501c564d16b', 'source_hash':row[0],
            'package_sha256':'60f87536a78dde37ceed1d26311865fd8bc4e64a703416fa44d566c22da39abd',
            'shared_sources':[{'bot_id':'alpha','submission_id':'a2f2ee53-88b2-4821-b06d-ac630b9d7eae',
                'source_commit':'82a14a04f0e6b68aac8a7e879d305b1a886b857c',
                'source_hash':'6e362fd7cce836975fa615bc8b936109235fd320def63703761366586efabc25'}],
            'interval_seconds':72, 'max_outstanding':50, 'share_feedback':True,
            'archive_budget_bytes':256*1024**2, 'feedback_budget_bytes':128*1024**2,
            'authorization':'Owner 19 October: I will submit the prepared beta ZIP; use beta afterward. Shared 50/hour allowance.',
            'limits':'No uploads, activation, private opponent files, paid fallback or contest-compliance certification.'}
        atomic_json(path, config, 0o644)
        load(path)
        state_path = Path(config['root']) / 'official-exploration/state.json'
        if args.review_throttle_stop and state_path.exists():
            state = read_json(state_path)
            detail = state.get('blocked') or ''
            require('Public API is busy' in detail and 'HTTP 429' in detail,
                    'only the reviewed busy-API throttle stop may be cleared here')
            require(not any(read_json(p)['state'] == 'UNKNOWN' for p in
                    state_path.parent.glob('requests/*/record.json')), 'ambiguous creation needs reconciliation')
            owner = state_path.stat()
            state['reviewed_stop'] = {'at':time.time(), 'detail':detail,
                                     'action':'Expired 2-second read throttle reviewed; await exact beta source.'}
            state.update(blocked=None, official_retry_at=time.time()+60)
            atomic_json(state_path, state, 0o600)
            os.chown(state_path, owner.st_uid, owner.st_gid)
        print(json.dumps({'enabled':True, 'target_groups_per_hour':50,
                          'submission_id':config['official_exploration']['submission_id'],
                          'services_started':False, 'uploads_or_activation':False}))


if __name__ == '__main__':
    main()
