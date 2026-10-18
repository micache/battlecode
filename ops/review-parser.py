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
from arena.statistics import read_current, unsigned


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
    current = config['engine']['version'] == '2.2.5'
    if current:
        read_current(stats)
        match = stats['match']
        round_number = match['roundsStarted']
        outcome = match['outcome']
    else:
        require(stats['schemaVersion'] == 2 and stats['engineVersion'] == '0.0.1' and stats['engineVersionPacked'] == 65536,
                'unreviewed engine statistics schema')
        round_number, outcome = stats['round'], stats['outcome']
    require(outcome in ('teamA','teamB') and not inspected.get('errors'), 'outcome/replay review failed')
    require(any(item.get('aria', '').startswith('Seek timeline') and item.get('value') == item.get('max')
                and int(item.get('max') or 0) >= round_number for item in inspected['inputs'] if item.get('aria')),
            'review must show the fully indexed final frame')
    require(str(round_number) in inspected['body'], 'final round absent from replay review')
    for team in stats['teams']:
        require(f"{unsigned(team['submittedGems']):,}" in inspected['body'], 'submitted gems disagree with replay')
    diagnostics = {}
    for name in ('idle-tie', 'crash', 'fuel'):
        files = sorted((Path(config['root']) / 'acceptance/real-fixtures').glob(f'{name}-*/run/artifacts/final.json'))
        require(files, f'actual {name} fixture missing')
        actual = files[-1]
        data, process = read_json(actual), read_json(actual.parent / 'process-result.json')
        if current:
            actual_faults, measurements, suspensions = read_current(data)
            final_round, final_outcome = data['match']['roundsStarted'], data['match']['outcome']
            by_side = measurements['bot_faults_by_side']['value']
            require(by_side == ({'A':6000, 'B':0} if name == 'crash' else {'A':0, 'B':0}),
                    f'{name}: unverified fault attribution')
            if name == 'fuel':
                require(suspensions is not None and suspensions > 0, 'fuel suspension event fixture missing')
            if name == 'idle-tie':
                require(all(v == 0 for key in ('submitted_gems','lifetime_earned_gold','champion_kills')
                            for v in measurements[key]['value'].values()), 'not a complete tie')
        else:
            final_round, final_outcome = data['round'], data['outcome']
            require(data['botFaults'] == [6000, 0] if name == 'crash' else data['botFaults'] == [0, 0],
                    f'{name}: unverified fault attribution')
            if name == 'idle-tie':
                require(all(team['submittedGems'] == 0 for team in data['teams']) and
                        all(c['earnedGold'] == c['kills'] == 0 for c in data['champions']), 'not a complete tie')
        require(process['returncode'] == 0 and not process['timeout'] and final_round == 2000,
                f'{name}: incomplete real-engine diagnostic')
        require(final_outcome == 'teamB', f'{name}: unexpected diagnostic outcome')
        diagnostics[name] = {'path':str(actual), 'sha256':file_hash(actual)}
    contract = {'protocol_version':1, 'statistics_schema':'cambc-225-json-v1' if current else 'cambc-216-v2',
        'engine_sha256':config['engine']['binary_sha256'], 'fixture_path':str(fixture),
        'fixture_sha256':file_hash(fixture), 'reviewed_by':'arena_implementer; saved official visualizer final frame',
        'replay_agreement_verified':True, 'completion_mode':'final_statistics_contract',
        'winner_pointer':'/match/outcome' if current else '/outcome',
        'winner_values':{'teamA':'A','teamB':'B'}, 'reason_pointer':None,
        'metric_pointers':{'round':'/match/roundsStarted' if current else '/round'},
        'bot_fault_patterns':[], 'fault_detection_verified':True,
        'fuel_suspension_patterns':[],
        'truncated_patterns':['truncated: round', 'Statistics require a game outcome'],
        'review_evidence':{'replay':str(replay),'replay_sha256':file_hash(replay),
                           'review':str(review),'review_sha256':file_hash(review), 'diagnostics':diagnostics},
        'created':time.time()}
    atomic_json(config['parser_contract'], contract, 0o644)
    print(json.dumps(contract, indent=2))


if __name__ == '__main__':
    main()
