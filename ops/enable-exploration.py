#!/usr/bin/env python3
"""Enable frozen historical panels and bounded full evaluations while stopped."""
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, lock, read_json, require

require(os.geteuid() == 0, 'administrator required; stop services first')
path = Path('/etc/battlecode/arena.json')
config = read_json(path)
with lock(Path(config['root']) / 'state/service.lock'), lock(Path(config['root']) / 'model.lock'):
    atomic_json(path.with_name(f'arena.before-exploration-{time.time_ns()}.json'), config, 0o600)
    config['exploration'] = {'every_published_cycles': 5}
    config['evaluation'].update(historical_opponents=True, full_evaluation=True,
                                suite_version='historical-panels-v1')
    # No weakened thresholds, automatic promotion, official mutations, billing or auth changes.
    atomic_json(path, config, 0o644)
print(json.dumps({'historical_opponents': True, 'full_evaluation': True,
                  'max_full_checks_per_bot_per_day': 2, 'exploration_every_published_cycles': 5,
                  'automatic_promotion': config['evaluation']['automatic_promotion'],
                  'official': config['official'], 'services_started': False}))
