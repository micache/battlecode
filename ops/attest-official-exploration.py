#!/usr/bin/env python3
"""Read-only own-team source proofs from the owner's approved browser.

CLI 2.2.5 show JSON omits submission IDs. Never guess that an outside game ran
the configured source: attest it from the actual own-team metadata. No cookies,
headers, passwords or auth caches leave this machine. No contest writes.
"""
import argparse
import base64
import json
from pathlib import Path
import re
import shlex
import sys
import time
from urllib.parse import quote
import uuid
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import atomic_json, canonical, identity, lock, read_json, require
from ops.blaxel import Client, CREDENTIALS


SAVE = '''import base64,json,sys,zlib,uuid
from pathlib import Path
sys.path.insert(0,'/opt/battlecode')
from arena.common import atomic_json,read_json,require
config=read_json('/etc/battlecode/arena.json'); policy=config['official_exploration']
root=Path(config['root'])/'official-exploration/requests'; count=0
for item in json.loads(zlib.decompress(base64.b64decode(sys.argv[1]))):
 rid=item['request_id']; uuid.UUID(rid)
 require('/' not in rid and len(rid) in (32,36),'invalid request identifier')
 directory=root/rid; record=read_json(directory/'record.json'); data=item['metadata']
 require(data['myTeamId']==policy['team_id'] and data['group']['id']==record['group_id'], 'source-proof team/group mismatch')
 own=next(s for s in data['group']['sides'] if s['teamId']==policy['team_id'])
 require(own['submissionId']==policy['submission_id'],'different submission actually played; do not attribute it to the pinned bot')
 target=directory/'metadata.json'
 if target.exists():require(read_json(target)==data,'finished source proof changed; reconcile')
 else:atomic_json(target,data,384)
 count+=1
print(json.dumps({'attested_groups':count}))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-groups', type=int, default=10)
    parser.add_argument('--resume-after-review', action='store_true')
    args = parser.parse_args()
    require(0 < args.max_groups <= 50, 'bounded source-proof count required')
    root = Path.home() / '.local/share/battlecode-exploration'
    root.mkdir(mode=0o700, exist_ok=True)
    with lock(root / 'attestation.lock'):
        stop = root / 'attestation-stop.json'
        require(not stop.exists() or args.resume_after_review,
                'source-proof adapter stopped; review attestation-stop.json before resuming')
        credentials = read_json(CREDENTIALS)
        client = Client(credentials['key'], credentials['workspace'])
        endpoint = client.endpoint()
        pending = json.loads(client.request('GET', '/filesystem/' + quote(
            '/srv/battlecode/public/official-pending.json', safe=''), base=endpoint, raw=True))
        receipts = root / 'receipts'
        receipts.mkdir(mode=0o700, exist_ok=True)
        wanted = []
        for item in pending['requests']:
            uuid.UUID(item['group_id'])
            if not (receipts / (item['group_id'] + '.json')).exists():
                wanted.append(item)
        proofs = []
        from playwright.sync_api import sync_playwright
        if wanted:
            with sync_playwright() as playwright:
                context = playwright.chromium.launch_persistent_context(
                    str(Path.home() / '.local/share/battlecode-contest-browser'), headless=True)
                try:
                    for item in wanted[:args.max_groups]:
                        response = context.request.get('https://2026a.battlecode.co.uk/api/v1/match-groups/' +
                                                       item['group_id'], timeout=60000)
                        if response.status in (401,403,429):
                            atomic_json(stop, {'status':response.status, 'retry_after':response.headers.get('retry-after'),
                                              'at':time.time(), 'group':item['group_id']}, 0o600)
                        require(response.ok, 'source-proof access stop: HTTP ' + str(response.status))
                        data = response.json()
                        require(data['myTeamId'] == pending['team_id'], 'browser and native CLI teams differ')
                        own = next(s for s in data['group']['sides'] if s['teamId'] == data['myTeamId'])
                        if own['submissionId'] != pending['submission_id']:
                            atomic_json(stop, {'at':time.time(), 'group':item['group_id'],
                                'expected_submission':pending['submission_id'], 'actual_submission':own['submissionId'],
                                'action':'Different team upload; stop source attribution, never overwrite its selection.'}, 0o600)
                            raise RuntimeError('a different submission played; review source mapping')
                        if data['group']['status'] not in ('finished','error'):
                            continue
                        # No signed URLs, personal profile, eligibility or opponent private logs.
                        group = {k:data['group'][k] for k in ('id','kind','status','sides','winnerTeamId')}
                        matches = [{k:m[k] for k in ('id','position','status','map','mapId','patchId','rounds','sides')}
                                   for m in data['matches']]
                        proofs.append({**item, 'metadata':{'myTeamId':data['myTeamId'], 'group':group, 'matches':matches}})
                finally:
                    context.close()
        if not proofs:
            print(json.dumps({'new_source_proofs':0, 'pending':len(wanted)}))
            return
        key = identity(proofs)
        intent = root / (key + '-intent.json')
        name = 'official-source-proof-' + key[:24]
        if not intent.exists():
            atomic_json(intent, {'process':name, 'groups':[v['group_id'] for v in proofs], 'created':time.time()}, 0o600)
            encoded = base64.b64encode(zlib.compress(canonical(proofs))).decode()
            require(len(encoded) < 90000, 'source-proof batch too large')
            client.request('POST', '/process', {'command':shlex.join([
                'python3','/opt/battlecode/ops/as-arena.py','python3','-c',SAVE,encoded]),
                'name':name, 'waitForCompletion':False, 'keepAlive':True, 'timeout':0}, base=endpoint)
        result = client.request('GET', '/process/' + name, base=endpoint)
        until = time.monotonic() + 20
        while result['status'] == 'running' and time.monotonic() < until:
            time.sleep(2)
            result = client.request('GET', '/process/' + name, base=endpoint)
        # A later timer reconciles this same named process. Never repeat its POST.
        if result['status'] != 'completed':
            require(result['status'] == 'running', 'source-proof copy failed; reconcile saved process intent')
            print(json.dumps({'process':name, 'pending':True}))
            return
        require(result['exitCode'] == 0, 'source-proof copy failed; inspect saved process')
        for item in proofs:
            atomic_json(receipts / (item['group_id'] + '.json'), {
                'group_id':item['group_id'], 'submission_id':pending['submission_id'],
                'source_commit':pending['source_commit'], 'metadata_sha256':identity(item['metadata']),
                'process':name, 'verified_at':time.time()}, 0o600)
        atomic_json(root / 'status.json', {'heartbeat':time.time(), 'new_source_proofs':len(proofs),
                                          'groups':[v['group_id'] for v in proofs]}, 0o600)
        print(json.dumps({'new_source_proofs':len(proofs)}))


if __name__ == '__main__':
    main()
