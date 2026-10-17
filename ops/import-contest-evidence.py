#!/usr/bin/env python3
"""Map downloaded own-team games to a verified ZIP and import compact evidence.

Raw bundles remain in the private local download archive. The running arena's
normal owner mailbox is the only database writer. No coding jobs are triggered.
"""
import argparse
import base64
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import shlex
import sys
import time
import zipfile
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import atomic_json, canonical, file_hash, identity, read_json, require, slug
from ops.blaxel import Client, CREDENTIALS


def prepare(root, manifest, submission_id):
    """Never infer that a filename/version alone identifies our source."""
    source = root / 'submissions' / (submission_id + '.zip')
    require(file_hash(source) == manifest['package_sha256'], 'uploaded ZIP differs from local source package')
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and all(n.startswith('src/') for n in names), 'unexpected source archive')
        source_hash = identity({n.removeprefix('src/'):hashlib.sha256(archive.read(n)).hexdigest() for n in names})
        require(source_hash == manifest['source_hash'], 'source subtree hash differs from manifest')
    history = read_json(root / 'history-complete.json')
    team = history['team_id']
    selected, excluded = [], []
    for path in sorted((root / 'groups').glob('*/metadata.json')):
        data = read_json(path)
        group = data['group']
        require(data['myTeamId'] == team, 'metadata team mismatch')
        own = next(s for s in group['sides'] if s['teamId'] == team)
        if own.get('submissionId') != submission_id:
            continue
        download = path.parent / 'download.json'
        if group['status'] != 'finished' or not download.exists():
            excluded.append({'group':group['id'], 'status':group['status'], 'bundle_available':download.exists()})
            continue
        receipt = read_json(download)
        bundle = Path(receipt['path'])
        require(bundle.resolve().parent == path.parent.resolve(), 'bundle outside its group directory')
        require(file_hash(bundle) == receipt['sha256'], 'downloaded bundle checksum changed')
        selected.append((data, receipt))
    counts = Counter()
    payloads = []
    for data, receipt in selected:
        group = data['group']
        counts['series'] += 1
        counts['series_wins' if group['winnerTeamId'] == team else 'series_losses'] += 1
        with zipfile.ZipFile(receipt['path']) as outer:
            for match in data['matches']:
                require(match['status'] == 'finished', 'unfinished game in finished series')
                own = next(s for s in match['sides'] if s['teamId'] == team)
                enemy = next(s for s in match['sides'] if s['teamId'] != team)
                winners = [s for s in match['sides'] if s['result'] == 'win']
                require(len(winners) == 1, 'missing/ambiguous authoritative winner')
                counts['games'] += 1
                counts['wins' if own['result'] == 'win' else 'losses'] += 1
                member = f"{match['position']:02d}-{match['id']}.zip"
                require(outer.namelist().count(member) == 1, 'original game archive missing/duplicated')
                require(outer.getinfo(member).file_size < 2 * 1024**2, 'game bundle unexpectedly large')
                raw = outer.read(member)
                own_name = 'team-' + own['side'] + '.stdout'
                with zipfile.ZipFile(io.BytesIO(raw)) as game:
                    require(sum(i.file_size for i in game.infolist()) < 16 * 1024**2, 'game archive unexpectedly large')
                    require('replay.repl26a' in game.namelist(), 'original replay missing')
                    stdout = game.read(own_name) if own_name in game.namelist() else b''
                    hashes = {n:hashlib.sha256(game.read(n)).hexdigest() for n in game.namelist()}
                # Only known literal messages are extracted; binary markers are not decoded.
                messages = re.findall(rb'draft: hello world\n|shared round: [0-9]+\n', stdout)
                stdout_report = {'raw_bytes':len(stdout), 'raw_sha256':hashlib.sha256(stdout).hexdigest(),
                    'known_message_count':len(messages),
                    'literal_excerpt':[m.decode().rstrip() for m in messages[:3]+messages[-3:]],
                    'limitation':'Binary timeline markers omitted. Shared-round values are not authoritative game rounds.'}
                summary_path = root / 'summaries' / (match['id']+'.json')
                summary = read_json(summary_path) if summary_path.exists() else None
                observation = {'official_match_id':match['id'], 'group_id':group['id'],
                    'source_commit':manifest['commit'], 'source_hash':source_hash,
                    'submission_id':submission_id, 'uploaded_zip_sha256':manifest['package_sha256'],
                    'own_side':own['side'].upper(), 'outcome':winners[0]['side'].upper(),
                    'map_name':match['map'], 'map_id':match['mapId'], 'official_patch':match['patchId'],
                    'rounds':match['rounds'], 'own_tributed_gems':own['score'],
                    'opponent_tributed_gems':enemy['score'], 'own_draft_ids':own['draft'],
                    'opponent_draft_ids':enemy['draft'], 'reported_own_bot_error':own.get('botError'),
                    'opponent_version':enemy.get('version'), 'stdout':stdout_report,
                    'official_summary':summary,
                    'limits':['Uncontrolled external observation of this OLD submitted revision, not current working code.',
                        'Opponent source/version is unknown unless explicitly supplied by the platform.',
                        'Official patch 0.0.3 differs from pinned local embedded engine 0.0.1; no parity claim.',
                        'New official maps are not automatically added to the frozen evaluation suite.',
                        'No verified binary fuel/replay decoder: fuel suspensions and behavioral causes remain unknown.',
                        'A null exposed botError is not proof of zero fuel suspensions.',
                        'No draw inference from tied gem scores; use the authoritative winner.'],
                    'raw_archive':{'local_bundle':receipt['path'], 'bundle_sha256':receipt['sha256'],
                        'game_member':member, 'game_sha256':hashlib.sha256(raw).hexdigest(), 'member_sha256':hashes}}
                files = {'observations.json':canonical(observation),
                         'match-metadata.json':canonical({'group':group,'match':match,'myTeamId':team}),
                         'stdout.log':canonical(stdout_report)}
                if summary is not None:
                    files['final.json'] = canonical(summary)
                payloads.append({'official_match_id':match['id'], 'submission_id':submission_id,
                    'source_commit':manifest['commit'], 'source_hash':source_hash,
                    'own_side':own['side'].upper(), 'outcome':winners[0]['side'].upper(),
                    'map_name':match['map'], 'opponent_version':enemy.get('version'),
                    'official_group_id':group['id'], 'official_patch':match['patchId'],
                    'uploaded_zip_sha256':manifest['package_sha256'],
                    'files':{n:base64.b64encode(blob).decode() for n,blob in files.items()}})
    require(payloads, 'no completed, downloaded games for the mapped submission')
    # Report three readable examples. The arena, not mailbox arrival order,
    # independently selects its bounded development-map loss handoff.
    development = {'collision','corners','elkring','expanse','interlock','lanes'}
    examples = []
    for payload in reversed(payloads):
        if (payload['outcome'] != payload['own_side'] and payload['map_name'] in development and
                payload['map_name'] not in {p['map_name'] for p in examples}):
            examples.append(payload)
        if len(examples) == 3:
            break
    payloads = [p for p in payloads if p not in examples] + examples
    return payloads, {'source_commit':manifest['commit'], 'source_hash':source_hash,
        'submission_id':submission_id, 'verified_uploaded_zip_sha256':manifest['package_sha256'],
        'counts':dict(counts), 'excluded_series':excluded,
        'history_snapshot_at':history['observed_at'], 'representative_match_ids':[p['official_match_id'] for p in examples]}


# Executed as the bot owner, not root. Only the existing arena writer imports.
REMOTE = '''import base64,json,sys,time,zlib
from pathlib import Path
sys.path.insert(0,'/opt/battlecode')
from arena.client import owner_config
from arena.common import atomic_json,identity,read_json,require
bot=sys.argv[1]; config=owner_config('/etc/battlecode/'+bot+'.json'); root=Path(config['root'])
payloads=json.loads(zlib.decompress(base64.b64decode(sys.argv[2])))
responses=[]
for payload in payloads:
 rid='request-'+identity({'operation':'import-external','bot':bot,'payload':payload})[:32]
 target=root/'inbox'/bot/(rid+'.json'); response=root/'outbox'/bot/(rid+'.json')
 if not response.exists() and not target.exists():
  require(not target.with_suffix('.consumed').exists(),'consumed request missing response; reconcile')
  atomic_json(target,{'protocol_version':1,'id':rid,'bot_id':bot,'operation':'import-external','payload':payload},0o640)
 responses.append((payload['official_match_id'],rid,response))
deadline=time.monotonic()+150
while not all(p.exists() for _,_,p in responses):
 require(time.monotonic()<deadline,'import pending; preserve request IDs and reconcile')
 time.sleep(1)
print(json.dumps([{'official_match_id':mid,'request_id':rid,'response':read_json(p)} for mid,rid,p in responses]))
'''


def apply(root, bot, payloads):
    credentials = read_json(CREDENTIALS)
    client = Client(credentials['key'], credentials['workspace'])
    endpoint = client.endpoint()
    directory = root / 'imports'
    directory.mkdir(exist_ok=True, mode=0o700)
    # Bounded argv. Durable process intent is saved before every non-retried POST.
    batches, batch = [], []
    for payload in payloads:
        encoded = base64.b64encode(zlib.compress(canonical(batch+[payload]))).decode()
        if len(encoded) > 90000 and batch:
            batches.append(batch)
            batch = []
        batch.append(payload)
        require(len(base64.b64encode(zlib.compress(canonical(batch)))) <= 90000, 'single compact game too large')
    if batch:
        batches.append(batch)
    for batch in batches:
        key = identity({'bot':bot,'payloads':batch})
        path = directory / (key+'.json')
        if path.exists():
            state = read_json(path)
        else:
            state = {'process':'official-import-'+key[:24], 'submitted_at':time.time(),
                     'official_match_ids':[p['official_match_id'] for p in batch], 'complete':False}
            atomic_json(path, state, 0o600)
            encoded = base64.b64encode(zlib.compress(canonical(batch))).decode()
            args = ['runuser','-u','bc-'+bot,'--','python3','-c',REMOTE,bot,encoded]
            client.request('POST','/process',{'command':shlex.join(args),'name':state['process'],
                'waitForCompletion':False,'keepAlive':True,'timeout':180},base=endpoint)
        if state['complete']:
            continue
        deadline = time.monotonic()+190
        while True:
            result = client.request('GET','/process/'+state['process'],base=endpoint)
            if result['status'] in ('completed','failed','killed','stopped'):
                break
            require(time.monotonic()<deadline, 'named import process pending; reconcile same process')
            time.sleep(3)
        state['result'] = result
        atomic_json(path,state,0o600)
        require(result.get('exitCode') == 0, 'named import failed; inspect saved process result')
        output = result['stdout']
        # API process logs encode line breaks literally on this host.
        if output.endswith('\\n'):
            output = output[:-2]
        responses = json.loads(output)
        require(all(r['response']['ok'] for r in responses), 'arena rejected evidence; inspect saved responses')
        state.update(complete=True,responses=responses)
        atomic_json(path,state,0o600)
        print(json.dumps({'imported_games':len(responses),'receipt':str(path)}),flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--downloads',type=Path,default=Path.home()/'.local/share/battlecode-contest-downloads')
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--submission-id',required=True)
    parser.add_argument('--apply',action='store_true')
    args = parser.parse_args()
    manifest = read_json(args.manifest)
    bot = slug(manifest['bot'])
    payloads, report = prepare(args.downloads,manifest,args.submission_id)
    atomic_json(args.downloads/('mapped-'+args.submission_id+'.json'),report,0o600)
    print(json.dumps(report),flush=True)
    if args.apply:
        apply(args.downloads,bot,payloads)


if __name__ == '__main__':
    main()
