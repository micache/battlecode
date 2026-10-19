#!/usr/bin/env python3
"""Read-only source proofs from the approved browser; no credential export or contest writes."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shlex
import sys
import time
from urllib.parse import quote
import uuid
import zipfile
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import atomic_json, canonical, identity, lock, read_json, require
from ops.blaxel import Client, CREDENTIALS

ORIGIN = 'https://2026a.battlecode.co.uk'
SAVE = '''import base64,json,sys,zlib
sys.path.insert(0,'/opt/battlecode')
from arena.common import read_json
from arena.exploration import save_source_proofs
print(json.dumps({'attested_groups':save_source_proofs(read_json('/etc/battlecode/arena.json'),
 json.loads(zlib.decompress(base64.b64decode(sys.argv[1]))))}))
'''


def archive_source_hash(data):
    require(len(data) <= 5 * 1024**2, 'source archive exceeds platform limit')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        files = [v for v in archive.infolist() if not v.is_dir()]
        require(files and sum(v.file_size for v in files) <= 16 * 1024**2, 'unbounded source archive')
        require(len({v.filename for v in files}) == len(files), 'duplicate archive member')
        roots = set()
        for entry in files:
            path = PurePosixPath(entry.filename)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in entry.filename,
                    'unsafe archive member')
            require('src' in path.parts, 'unexpected non-source file; review package')
            roots.add(path.parts[:path.parts.index('src') + 1])
        require(len(roots) == 1, 'ambiguous source root')
        prefix = '/'.join(next(iter(roots))) + '/'
        return identity({v.filename.removeprefix(prefix):hashlib.sha256(archive.read(v)).hexdigest()
                         for v in files})


def deliver(client, endpoint, root, batch):
    key = identity(batch)
    intent = root / (key + '-intent.json')
    name = 'official-source-proof-' + key[:24]
    if not intent.exists():
        atomic_json(intent, {'process':name, 'created':time.time(), 'batch':batch}, 0o600)
        encoded = base64.b64encode(zlib.compress(canonical(batch))).decode()
        require(len(encoded) < 90000, 'source-proof batch too large')
        client.request('POST', '/process', {'command':shlex.join([
            'python3','/opt/battlecode/ops/as-arena.py','python3','-c',SAVE,encoded]),
            'name':name, 'waitForCompletion':False, 'keepAlive':True, 'timeout':0}, base=endpoint)
    result = client.request('GET', '/process/' + name, base=endpoint)
    until = time.monotonic() + 20
    while result['status'] == 'running' and time.monotonic() < until:
        time.sleep(2)
        result = client.request('GET', '/process/' + name, base=endpoint)
    if result['status'] == 'running':
        return False
    require(result['status'] == 'completed' and result['exitCode'] == 0,
            'source-proof transfer failed; reconcile ' + name)
    atomic_json(intent.with_suffix('.done.json'), {'process':name, 'completed':time.time()}, 0o600)
    return True


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
        if stop.exists():
            require(args.resume_after_review, 'review attestation-stop.json before resuming')
            stop.rename(root / ('attestation-stop-reviewed-' + str(time.time_ns()) + '.json'))
        credentials = read_json(CREDENTIALS)
        client = Client(credentials['key'], credentials['workspace'])
        endpoint = client.endpoint()
        # Reconcile unfinished transfers before making another browser request.
        for intent in sorted(root.glob('*-intent.json')):
            if intent.with_suffix('.done.json').exists():
                continue
            saved = read_json(intent)
            if 'batch' in saved:
                require(deliver(client, endpoint, root, saved['batch']), 'previous transfer still pending')
        pending = json.loads(client.request('GET', '/filesystem/' + quote(
            '/srv/battlecode/public/official-pending.json', safe=''), base=endpoint, raw=True))
        receipts = root / 'receipts'
        receipts.mkdir(mode=0o700, exist_ok=True)
        wanted = [v for v in pending['requests'] if not (receipts / (v['group_id'] + '.json')).exists()]
        proofs = []
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                str(Path.home() / '.local/share/battlecode-contest-browser'), headless=True)
            try:
                def get(path):
                    response = context.request.get(ORIGIN + path, timeout=60000)
                    if response.status in (401,403,429):
                        atomic_json(stop, {'status':response.status, 'retry_after':response.headers.get('retry-after'),
                                          'at':time.time()}, 0o600)
                    require(response.ok, 'source-proof access stop: HTTP ' + str(response.status))
                    return response
                listing = get('/api/v1/submissions').json()
                require(listing['team']['id'] == pending['team_id'], 'browser and native CLI teams differ')
                selected = listing.get('selected') or listing.get('active')
                require(selected, 'no selected team submission')
                sid = str(uuid.UUID(selected['id']))
                cached = root / ('submission-' + sid + '.json')
                if not cached.exists():
                    data = get('/api/v1/submissions/' + sid + '/archive').body()
                    atomic_json(cached, {'submission_id':sid, 'source_hash':archive_source_hash(data),
                        'package_sha256':hashlib.sha256(data).hexdigest()}, 0o600)
                selection = {**read_json(cached), 'team_id':pending['team_id'], 'observed_at':time.time()}
                for item in wanted[:args.max_groups]:
                    uuid.UUID(item['group_id'])
                    data = get('/api/v1/match-groups/' + item['group_id']).json()
                    require(data['myTeamId'] == pending['team_id'], 'source-proof team mismatch')
                    own = next(s for s in data['group']['sides'] if s['teamId'] == data['myTeamId'])
                    expected = item.get('submission_id', pending['submission_id'])
                    if data['group']['status'] not in ('finished','error') and own['submissionId'] == expected:
                        continue
                    group = {k:data['group'][k] for k in ('id','kind','status','sides','winnerTeamId')}
                    matches = [{k:m[k] for k in ('id','position','status','map','mapId','patchId','rounds','sides')}
                               for m in data['matches']]
                    proofs.append({**item, 'metadata':{'myTeamId':data['myTeamId'], 'group':group, 'matches':matches}})
            finally:
                context.close()
        batch = {'selection':selection, 'proofs':proofs}
        complete = deliver(client, endpoint, root, batch)
        if complete:
            for item in proofs:
                atomic_json(receipts / (item['group_id'] + '.json'), {
                    'group_id':item['group_id'], 'metadata_sha256':identity(item['metadata']),
                    'verified_at':time.time()}, 0o600)
        status = {'heartbeat':time.time(), 'new_source_proofs':len(proofs), 'transferred':complete,
                  'selected_submission_id':selection['submission_id'],
                  'target_source_selected':selection['source_hash'] == pending['source_hash']}
        atomic_json(root / 'status.json', status, 0o600)
        print(json.dumps(status))


if __name__ == '__main__':
    main()
