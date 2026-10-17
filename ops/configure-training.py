#!/usr/bin/env python3
"""Stopped-service training cadence/storage configuration, never owner auth."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, lock, read_json, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--interval-seconds', type=int, default=3600)
    args = parser.parse_args()
    require(os.geteuid() == 0, 'administrator required; stop services first')
    require(args.interval_seconds >= 60, 'interval must be at least one minute')
    path = Path('/etc/battlecode/arena.json')
    config = read_json(path)
    root = Path(config['root'])
    with lock(root / 'state/service.lock'), lock(root / 'model.lock'):
        config['limits'].update(improvement_interval_seconds=args.interval_seconds,
                                archive_completed_projects=True)
        atomic_json(path, config, 0o644)
    print(json.dumps({'interval_seconds':args.interval_seconds, 'completed_project_archiving':True,
                      'concurrency_and_promotion_gate':'unchanged', 'services_started':False}))


if __name__ == '__main__':
    main()
