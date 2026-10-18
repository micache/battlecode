#!/usr/bin/env python3
"""Record observed C++ default budgets/settings from the saved idle fixture.

No other language's budget is claimed measured. Does not enable promotion.
Run as bc-arena, stopped, before starter/parser qualification and evaluations.
"""
import fcntl
import json
import os
from pathlib import Path
import re
import sys
import time
import zipfile

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, read_json, require
from arena.engine import PROFILE
from arena.statistics import read_current


def main():
    config = read_json('/etc/battlecode/arena.json')
    root = Path(config['root'])
    require(os.geteuid() == (root / 'state').stat().st_uid, 'run as bc-arena')
    with (root / 'state/service.lock').open('r') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        target = root / 'acceptance/cpp-profile-225.json'
        require(not target.exists(), 'profile already recorded; inspect instead of overwriting')
        paths = sorted((root / 'acceptance/real-fixtures').glob('idle-tie-*/run/artifacts/final.json'))
        require(paths, 'run the new idle-tie fixture first')
        stats_path = paths[-1]
        read_current(read_json(stats_path))
        pattern = rb'PROFILE draft=(\d) call=(\d) round=(\d+) max_rounds=(\d+) winning_gems=(\d+) draft_bytes=(\d+) live_bytes=(\d+) remaining_fuel=(\d+)'
        observations = []
        replay = next(stats_path.parent.glob('*.repl26a'))
        with zipfile.ZipFile(replay) as archive:
            for side in ('a', 'b'):
                data = archive.read('team-' + side + '.stdout')
                require(len(data) <= 1024**2, 'profile stdout exceeds bound')
                for values in re.findall(pattern, data):
                    draft, call, round_number, rounds, gems, draft_bytes, live_bytes, fuel = map(int, values)
                    require((rounds, gems, draft_bytes, live_bytes) == (2000, 1000, 1024, 8),
                            'observed runtime settings differ from current rules')
                    target_fuel = (1000000 if draft else 200000) if call == 0 else 100000
                    require(target_fuel * .8 <= fuel <= target_fuel, 'default C++ fuel budget differs')
                    observations.append({'side':side, 'draft':bool(draft), 'call':call,
                                         'round':round_number, 'fuel_after_startup':fuel,
                                         'expected_turn_budget':target_fuel})
        require({(o['draft'],o['call']) for o in observations} == {(True,0),(True,1),(False,0),(False,1)},
                'first and subsequent draft/play observations required')
        profile = dict(PROFILE, fuel_multipliers={'cpp':1})
        record = {'at':time.time(), 'effective_profile':profile, 'observations':observations,
                  'settings_observed':{'max_rounds':2000,'winning_gems':1000,'draft_bytes':1024,'live_bytes':8},
                  'statistics':{'path':str(stats_path),'sha256':file_hash(stats_path)},
                  'replay':{'path':str(replay),'sha256':file_hash(replay)},
                  'unmeasured_languages':['rust','ocaml','python'],
                  'scope':'C++ lanes only. Fuel is read after startup overhead, not an exact pre-entry counter. '
                          'Full-run defaults, no fuel or round overrides. This is not a production configuration dump.'}
        atomic_json(target, record, 0o644)
        lock = read_json(config['engine_lock'])
        require(lock['version'] == '2.2.5' and lock.get('build_mode') == 'release', 'new release toolchain required')
        lock.update(effective_profile=profile, profile_evidence={'path':str(target),'sha256':file_hash(target)})
        atomic_json(config['engine_lock'], lock, 0o644)
        print(json.dumps({'profile':str(target),'observations':len(observations),'languages_measured':['cpp']}))


if __name__ == '__main__':
    main()
