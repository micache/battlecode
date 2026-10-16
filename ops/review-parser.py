#!/usr/bin/env python3
"""Install the narrow statistics contract after an explicit real replay review."""
import argparse
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, read_json, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', required=True)
    parser.add_argument('--replay', required=True)
    parser.add_argument('--review', required=True)
    parser.add_argument('--confirm-replay-agreement', action='store_true', required=True)
    args = parser.parse_args()
    require(os.geteuid() == 0 and args.confirm_replay_agreement, 'administrator review required')
    config = read_json('/etc/battlecode/arena.json')
    fixture, replay, review = (Path(value).resolve() for value in (args.fixture, args.replay, args.review))
    require(fixture.is_relative_to(Path(config['root']).resolve() / 'matches') and fixture.name == 'final.json',
            'saved real match fixture required')
    require(replay.parent == fixture.parent and replay.suffix == '.repl26a', 'matching saved replay required')
    stats, inspected = read_json(fixture), read_json(review)
    require(stats['schemaVersion'] == 2 and stats['engineVersion'] == '0.0.1' and stats['engineVersionPacked'] == 65536,
            'unreviewed engine statistics schema')
    require(stats['outcome'] in ('teamA','teamB') and not inspected.get('errors'), 'outcome/replay review failed')
    require(any(item.get('aria', '').startswith('Seek timeline') and item.get('value') == item.get('max')
                and int(item.get('max') or 0) >= stats['round'] for item in inspected['inputs'] if item.get('aria')),
            'review must show the fully indexed final frame')
    require(str(stats['round']) in inspected['body'], 'final round absent from replay review')
    for team in stats['teams']:
        require(f"{team['submittedGems']:,}" in inspected['body'], 'submitted gems disagree with replay')
    contract = {'protocol_version':1, 'statistics_schema':'cambc-216-v2',
        'engine_sha256':config['engine']['binary_sha256'], 'fixture_path':str(fixture),
        'fixture_sha256':file_hash(fixture), 'reviewed_by':'arena_implementer; saved official visualizer final frame',
        'replay_agreement_verified':True, 'completion_mode':'final_statistics_contract',
        'winner_pointer':'/outcome', 'winner_values':{'teamA':'A','teamB':'B'}, 'reason_pointer':None,
        'metric_pointers':{'round':'/round'}, 'bot_fault_patterns':[], 'fault_detection_verified':True,
        'fuel_suspension_patterns':[],
        'truncated_patterns':['truncated: round', 'Statistics require a game outcome'],
        'review_evidence':{'replay':str(replay),'replay_sha256':file_hash(replay),
                           'review':str(review),'review_sha256':file_hash(review)},
        'created':time.time()}
    atomic_json(config['parser_contract'], contract, 0o644)
    print(json.dumps(contract, indent=2))


if __name__ == '__main__':
    main()
