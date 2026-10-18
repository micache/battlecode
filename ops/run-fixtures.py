#!/usr/bin/python3
"""Serial real-engine diagnostics, separate from scoring and owner tasks."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, identity, lock, read_json, require, tree_hash
from arena.config import load
from arena.engine import OfficialEngine, normalize_result, seal_artifacts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', choices=['idle-tie', 'crash', 'fuel', 'truncated', 'timeout', 'mechanics', 'hidden'], required=True)
    parser.add_argument('--map', choices=['collision','corners','elkring'], default='collision')
    args = parser.parse_args()
    config = load('/etc/battlecode/arena.json')
    root = Path(config['root'])
    with lock(root / 'state/service.lock'):
        engine = OfficialEngine(config)
        directory = root / 'acceptance/real-fixtures' / (args.name + '-' + str(time.time_ns()))
        directory.mkdir(parents=True)
        source_a = Path('/opt/battlecode/fixtures') / ('idle' if args.name in ('idle-tie', 'truncated', 'timeout') else args.name)
        source_b = Path('/opt/battlecode/fixtures/idle')
        for name, source in [('a', source_a), ('b', source_b)]:
            if args.name == 'mechanics':
                source=Path(engine.lock['project_template']) / 'bots/side-a'
            elif args.name == 'hidden':
                source=Path('/opt/battlecode/fixtures/hidden')
            shutil.copytree(source, directory / name)
            if args.name == 'mechanics':
                shutil.copyfile('/opt/battlecode/fixtures/mechanics/src/main.cpp', directory / name / 'src/main.cpp')
            elif args.name == 'hidden' and name=='b':
                shutil.copyfile('/opt/battlecode/fixtures/hidden/blocker.h', directory / name / 'src/role.h')
        spec = {'a_snapshot': str(directory / 'a'), 'b_snapshot': str(directory / 'b'),
                'a_source_hash': tree_hash(directory / 'a/src'), 'b_source_hash': tree_hash(directory / 'b/src'),
                'engine_lock_hash': engine.lock_hash, 'fixture': args.name,
                'infrastructure_commit': config['infrastructure_commit'],
                'map_path': config['maps'] + '/' + args.map + '.map26a',
                'round_override': 1 if args.name == 'truncated' else None, 'fuel_override': None,
                'wall_timeout_override':0.05 if args.name == 'timeout' else None}
        spec['map_hash'] = file_hash(spec['map_path'])
        spec['job_id'] = identity(spec)
        atomic_json(directory / 'spec.json', spec)
        if args.name in ('truncated', 'timeout'):
            project, output = directory / 'project', directory / 'artifacts'
            engine.prepare_project(project, {'side-a': directory / 'a/src', 'side-b': directory / 'b/src'})
            shutil.copyfile(spec['map_path'], project / 'frozen.map26a')
            output.mkdir()
            command = ['run', 'side-a', 'side-b', '--map', '/work/frozen.map26a', '--out-dir', '/output',
                       '--statistics', '/output/final.json']
            if engine.lock['version'] == '2.2.5':
                command += ['--release', '--json']
            if args.name == 'truncated':
                command += ['--rounds', '1']
            engine.execute(project, output, command, 0.05 if args.name == 'timeout' else 300,
                           'bc-match-' + spec['job_id'][:24])
            result = normalize_result(output, engine.contract, engine.lock['engine_sha256'])
        else:
            result = engine.run_match(spec, directory / 'run')
        atomic_json(directory / 'review.json', {'result': result, 'not_scoring_evidence': True,
                    'note': 'Inspect raw diagnostics and replay before adding parser patterns.', 'spec': spec})
        seal_artifacts(directory, spec['job_id'], 1, result)
        print(json.dumps({'fixture': args.name, 'match_id': spec['job_id'], 'path': str(directory), 'result': result}, indent=2))


if __name__ == '__main__':
    main()
