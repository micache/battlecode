#!/usr/bin/env python3
"""Trusted operator mailbox, not another SQLite writer. No credentials are read."""
import argparse
import base64
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, read_json, require

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('operation', choices=['offload-plan', 'offload-ack'])
parser.add_argument('--request-id', required=True)
parser.add_argument('--payload', default='e30=')
args = parser.parse_args()
require(re.fullmatch('[a-f0-9]{32}', args.request_id), 'invalid request ID')
root = Path('/srv/battlecode')
result = root / 'public/offload/operator-results' / (args.request_id + '.json')
path = root / 'control' / ('request-' + args.request_id + '.json')
if not result.exists() and not path.exists() and not path.with_suffix('.done').exists():
    import json
    payload = json.loads(base64.b64decode(args.payload, validate=True))
    atomic_json(path, {'operation':args.operation, 'response_id':args.request_id, 'payload':payload})
deadline = time.monotonic() + 600
while not result.exists() and time.monotonic() < deadline:
    time.sleep(1)
require(result.exists(), 'request pending; preserve its ID and reconcile rather than issue a new request')
print({'result_path':str(result), 'ok':read_json(result)['ok']})
