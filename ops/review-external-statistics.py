#!/usr/bin/env python3
"""Stopped-service reconciliation of one reviewed outside statistics-format stop.

Does not change the local engine, authorize new builds, or clear access stops.
"""
import argparse
import gzip
import json
import os
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, lock, read_json, require
from arena.statistics import read_external


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request-id', required=True)
    parser.add_argument('--map-manifest', type=Path,
                        help='Reviewed outside map pool; never changes the local scoring pool')
    args = parser.parse_args()
    require(os.geteuid() == 0, 'administrator required; stop services first')
    require(re.fullmatch('[a-f0-9]{32}', args.request_id), 'canonical request ID required')
    config = read_json('/etc/battlecode/arena.json')
    root = Path(config['root'])
    with lock(root/'state/service.lock'), lock(root/'model.lock'):
        maps = None
        if args.map_manifest:
            require(args.map_manifest.resolve().is_relative_to(Path(config['infrastructure'])/'evidence'),
                    'trusted infrastructure map manifest required')
            maps = read_json(args.map_manifest)['maps']
            require(len({m['name'] for m in maps})==len(maps) and
                    all(m['role'] in ('development','holdout') and re.fullmatch('[a-f0-9]{64}',m['sha256']) for m in maps),
                    'reviewed outside map names, roles and hashes required')
        directory = root/'official-exploration/requests'/args.request_id
        record, metadata = read_json(directory/'record.json'), read_json(directory/'metadata.json')
        require(record['state'] == 'COLLECTING' and metadata['group']['status'] == 'finished',
                'finished, source-verified outside collection required')
        own = next(s for s in metadata['group']['sides'] if s['teamId'] == config['official_exploration']['team_id'])
        require(own['submissionId'] == record['submission_id'], 'outside source differs')
        reviewed = []
        for path in sorted(directory.glob('*-statistics.json.gz')):
            stats = json.loads(gzip.decompress(path.read_bytes()))
            read_external(stats)
            if maps is not None:
                require(any(m['sha256']==stats['match']['mapHash'] for m in maps),
                        'outside map bytes absent from reviewed pool')
            mid = path.name.removesuffix('-statistics.json.gz')
            match = next(m for m in metadata['matches'] if m['id'] == mid)
            winner = next(s for s in match['sides'] if s['result'] == 'win')
            require(match['rounds'] == stats['match']['roundsStarted'] and
                    stats['match']['outcome'] == 'team'+winner['side'].upper() and
                    all(int(t['submittedGems']) == next(s['score'] for s in match['sides']
                        if s['side'].upper() == t['team'][-1]) for t in stats['teams']),
                    'official metadata disagrees with statistics')
            reviewed.append({'match_id':mid,'statistics_sha256':file_hash(path),
                             'engine':stats['match']})
        require(reviewed, 'saved reviewed statistics required')
        state_path = root/'official-exploration/state.json'
        state = read_json(state_path)
        expected_stop = ('official map bytes are absent from the frozen pool; retain and review'
                         if maps is not None else 'unreviewed engine build or metric semantics')
        require(state.get('blocked') == expected_stop,
                'only this exact reviewed format stop may be cleared')
        require(not any(read_json(p)['state'] == 'UNKNOWN' for p in directory.parent.glob('*/record.json')),
                'unknown creation requires reconciliation')
        receipt = {'at':time.time(),'request_id':args.request_id,'reviewed':reviewed,
                   'source_commit':record['source_commit'],'submission_id':record['submission_id'],
                   'replay_bundle_sha256':file_hash(directory/'replays.zip'),
                   'local_engine_parity_verified':False,'authentication_or_unknown_stops_cleared':False}
        if maps is not None:
            before = Path('/etc/battlecode/arena.before-external-maps-'+str(time.time_ns())+'.json')
            atomic_json(before,config,0o600)
            config['official_exploration']['map_manifest'] = str(args.map_manifest)
            atomic_json('/etc/battlecode/arena.json',config,0o644)
            receipt['outside_map_manifest'] = {'path':str(args.map_manifest),'sha256':file_hash(args.map_manifest)}
        label = 'external-statistics-map-review' if maps is not None else 'external-statistics-review'
        atomic_json(root/('public/'+label+'-20261021.json'), receipt, 0o644)
        owner = state_path.stat()
        state.update(blocked=None, reviewed_statistics=receipt)
        atomic_json(state_path, state, 0o600)
        os.chown(state_path, owner.st_uid, owner.st_gid)
        print(json.dumps(receipt))


if __name__ == '__main__':
    main()
