#!/usr/bin/env python3
"""Change the pilot's publication cap with services stopped. 'none' continues."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, lock, read_json, require

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('limit', help='positive publications per bot, or none')
args = parser.parse_args()
require(os.geteuid() == 0, 'administrator required; stop services first')
limit = None if args.limit == 'none' else int(args.limit)
require(limit is None or limit > 0, 'positive limit or none required')
path = Path('/etc/battlecode/arena.json')
config = read_json(path)
with lock(Path(config['root']) / 'state/service.lock'), lock(Path(config['root']) / 'model.lock'):
    config['limits']['published_cycles_per_bot'] = limit
    atomic_json(path, config, 0o644)
print(json.dumps({'published_cycles_per_bot': limit, 'services_started': False,
                  'invocation_wall_limit_seconds': 1200, 'billing_and_quota_policy': 'unchanged'}))
