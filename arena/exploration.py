"""Owner-approved outside play through the official CLI, never a private API.

This sidecar has its own file journal. Central SQLite is read-only; imports use
the arena's existing single-writer mailbox. It cannot upload or activate bots.
"""
from collections import Counter
from contextlib import contextmanager
import base64
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import time
import uuid
import zipfile

from .common import ArenaError, atomic_bytes, atomic_json, canonical, file_hash, identity, read_json, require
from .statistics import read_current


class CLIError(ArenaError):
    pass


def timestamp(value):
    return datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def quota_wait(data, now):
    quota = data['quota']
    require(type(quota['limit']) is int and type(quota['used']) is int and
            0 <= quota['used'] <= quota['limit'], 'unknown official quota schema')
    if not data['ready']:
        return now + 60
    if quota['used'] < quota['limit']:
        return now
    return max(now + 5, timestamp(quota['resetsAt']) + 2) if quota.get('resetsAt') else now + 60


class NativeCLI:
    """Only the distributed CLI sees its existing native competition session."""
    def __init__(self, config, root):
        self.config, self.root = config, Path(root)
        self.image = read_json(config['engine_lock'])['image_id']

    def recover(self):
        result = subprocess.run(['podman','--cgroup-manager=cgroupfs','ps','-a','--filter',
                                 'label=battlecode-owner=official-exploration','--format','{{.Names}}'],
                                capture_output=True,text=True,timeout=20,check=True)
        for name in result.stdout.splitlines():
            require(re.fullmatch('bc-outside-[a-f0-9]{24}',name), 'unexpected official container identity')
            subprocess.run(['podman','--cgroup-manager=cgroupfs','rm','-f',name],
                           capture_output=True,timeout=20,check=True)

    def run(self, args, output=None):
        allowed = (args[:1] == ['ladder'] or args[:2] in (
            ['match-groups', 'quota'], ['match-groups', 'create'], ['match-groups', 'show'],
            ['match-groups', 'download'], ['matches', 'summary']))
        require(allowed, 'outside-play CLI command is not allowlisted')
        name = 'bc-outside-' + uuid.uuid4().hex[:24]
        command = ['podman', '--cgroup-manager=cgroupfs', 'run', '--name', name,
                   '--label', 'battlecode-owner=official-exploration',
                   '--rm', '--pull=never', '--network=host', '--read-only', '--cap-drop=ALL',
                   '--security-opt=no-new-privileges', '--pids-limit=128', '--memory=512m', '--cpus=1',
                   '--tmpfs', '/tmp:rw,nosuid,nodev,size=128m',
                   '--volume', '/var/lib/battlecode-volume/official-auth:/auth:rw',
                   '--env', 'HOME=/auth', '--env', 'XDG_CONFIG_HOME=/auth/config',
                   '--env', 'XDG_CACHE_HOME=/auth/.cache']
        if output is not None:
            output = Path(output)
            output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            require(output.resolve().is_relative_to(self.root.resolve()), 'outside output escaped its store')
            command += ['--volume', str(output.parent) + ':/output:rw']
            args = args + ['--output', '/output/' + output.name]
        try:
            result = subprocess.run(command + [self.image, 'cambc'] + args,
                                    capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired as exc:
            subprocess.run(['podman', '--cgroup-manager=cgroupfs', 'rm', '-f', name],
                           capture_output=True, timeout=20)
            raise CLIError('official CLI timeout; creation outcome must be reconciled') from exc
        if result.returncode:
            raise CLIError(result.stderr[-2000:] or 'official CLI failed without diagnostics')
        return json.loads(result.stdout) if '--json' in args and output is None else result.stdout


def compact_statistics(stats):
    faults, metrics, suspensions = read_current(stats)
    # Preserve measured events with round/position, not speculative loss causes.
    significant = []
    for event in stats['events']:
        if event['kind'] not in ('gemLoss', 'death', 'fuelExhausted'):
            continue
        for entry in event['entries']:
            significant.append({'kind':event['kind'], 'owner':event['owner'], **entry})
    significant.sort(key=lambda e: (-int(e.get('value', '0')), e.get('timestamp', {}).get('round', 0)))
    return {'match':stats['match'], 'teams':stats['teams'], 'champions':stats['champions'],
            'diagnostics':stats['diagnostics'], 'metrics':metrics, 'bot_faults':faults,
            'fuel_suspensions':suspensions, 'representative_events':significant[:12],
            'event_selection':'Largest recorded gem-loss/death/fuel events; not a causal diagnosis. '
                              'Full original timelines/events remain in the retained official archive.'}


def shared(config, metadata):
    policy = config.get('official_exploration', {})
    return bool(policy.get('enabled') and policy.get('share_feedback') and
                metadata.get('submission_id') == policy.get('submission_id') and
                metadata.get('source_commit') == policy.get('source_commit') and
                metadata.get('source_hash') == policy.get('source_hash'))


class Explorer:
    def __init__(self, config, cli=None):
        self.config = config
        self.policy = config['official_exploration']
        self.root = Path(config['root']) / 'official-exploration'
        self.root.mkdir(exist_ok=True, mode=0o700)
        self.cli = cli or NativeCLI(config, self.root)
        if cli is None:
            self.cli.recover()
        self.state_path = self.root / 'state.json'
        self.state = read_json(self.state_path) if self.state_path.exists() else {
            'sequence':0, 'next_create':0, 'created':0, 'imported_games':0, 'blocked':None}
        self.reconcile_records()

    @contextmanager
    def db(self):
        db = sqlite3.connect('file:' + self.config['root'] + '/state/arena.sqlite?mode=ro', uri=True)
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    def save(self):
        atomic_json(self.state_path, self.state, 0o600)

    def records(self):
        return sorted((self.root / 'requests').glob('*/record.json'),
                      key=lambda p: read_json(p)['created_at'])

    def reconcile_records(self):
        records = [read_json(p) for p in self.records()]
        self.state['created'] = max(self.state['created'], sum(bool(r.get('group_id')) for r in records))
        for record in records:
            self.state['next_create'] = max(self.state['next_create'], record['created_at'] + 72)
            if record['state'] == 'UNKNOWN':
                self.state['blocked'] = 'Unknown creation: inspect request ' + record['request_id'] + '; never retry blindly'
        self.save()

    def validate_source(self):
        with self.db() as db:
            row = db.execute('SELECT * FROM revisions WHERE bot_id=? AND commit_sha=?',
                             (self.policy['bot_id'], self.policy['source_commit'])).fetchone()
        require(row and row['source_hash'] == self.policy['source_hash'], 'official source mapping changed')

    def adopt_first(self):
        """Adopt the one manually requested native-CLI pilot, never recreate it."""
        first = self.root / 'first-request.json'
        if not first.exists():
            return
        old = read_json(first)
        require(old['state'] == 'CREATED', 'first official creation requires reconciliation')
        gid = str(uuid.UUID(old['response']['groupId']))
        path = self.root / 'requests' / gid / 'record.json'
        if path.exists():
            return
        atomic_json(path, {'request_id':gid, 'group_id':gid, 'state':'QUEUED',
                    'created_at':old['created_at'], 'next_poll':0, 'opponent_id':old['opponent'],
                    'opponent_rank':old['opponent_rank'], 'opponent_name':old['response']['teamName'],
                    'source_commit':old['source_commit'], 'submission_id':old['expected_submission'],
                    'source_hash':old['source_hash'], 'bot_id':'alpha'}, 0o600)
        self.state['sequence'] = max(1, self.state['sequence'])
        self.reconcile_records()

    def create(self, now):
        if now < self.state['next_create'] or self.state.get('blocked'):
            return
        pending = [read_json(p) for p in self.records() if read_json(p)['state'] in ('QUEUED', 'COLLECTING')]
        if len(pending) >= self.policy.get('max_outstanding', 50):
            return
        quota = self.cli.run(['match-groups', 'quota', '--json'])
        require(quota['team']['id'] == self.policy['team_id'], 'competition team changed; stop outside play')
        self.state['quota'] = quota['quota']
        wait = quota_wait(quota, now)
        if wait > now:
            self.state['next_create'] = wait
            self.save()
            return
        ladder_path = self.root / 'ladder.json'
        if not ladder_path.exists() or now - ladder_path.stat().st_mtime >= 3600:
            atomic_json(ladder_path, self.cli.run(['ladder', '--limit', '25', '--json']), 0o600)
        opponents = [t for t in read_json(ladder_path)['teams'] if t['teamId'] != self.policy['team_id']]
        require(opponents, 'empty opponent panel')
        opponent = opponents[self.state['sequence'] % len(opponents)]
        rid = uuid.uuid4().hex
        path = self.root / 'requests' / rid / 'record.json'
        record = {'request_id':rid, 'state':'UNKNOWN', 'created_at':time.time(), 'next_poll':0,
                  'opponent_id':opponent['teamId'], 'opponent_rank':opponent['rank'],
                  'opponent_name':opponent['name'], 'source_commit':self.policy['source_commit'],
                  'submission_id':self.policy['submission_id'], 'source_hash':self.policy['source_hash'],
                  'bot_id':self.policy['bot_id']}
        # This intent is durable BEFORE the non-idempotent command is issued.
        atomic_json(path, record, 0o600)
        try:
            response = self.cli.run(['match-groups', 'create', opponent['teamId'], '--json'])
            record.update(group_id=str(uuid.UUID(response['groupId'])), state='QUEUED', response=response)
            atomic_json(path, record, 0o600)
        except Exception:
            self.state['blocked'] = 'Unknown creation: inspect request ' + rid + '; never retry blindly'
            self.save()
            raise
        self.state.update(sequence=self.state['sequence'] + 1, created=self.state['created'] + 1,
                          next_create=record['created_at'] + max(72, self.policy.get('interval_seconds', 72)))
        self.save()

    def import_payload(self, payload):
        bot = payload.get('source_bot_id', self.policy['bot_id'])
        with self.db() as db:
            old = db.execute('SELECT metadata FROM external_matches WHERE official_id=?',
                             (payload['official_match_id'],)).fetchone()
        if old:
            metadata = json.loads(old['metadata'])
            require(all(metadata.get(k) == payload[k] for k in ('source_commit', 'submission_id', 'source_hash')),
                    'official match was imported under a different source')
            return True
        rid = 'request-' + identity({'operation':'import-external', 'bot':bot, 'payload':payload})[:32]
        inbox = Path(self.config['root']) / 'inbox' / bot / (rid + '.json')
        response = Path(self.config['root']) / 'outbox' / bot / (rid + '.json')
        if response.exists():
            reply = read_json(response)
            require(reply['ok'], reply.get('error', 'official evidence import failed'))
            return True
        if not inbox.exists():
            require(not inbox.with_suffix('.consumed').exists(), 'import consumed without receipt; reconcile')
            atomic_json(inbox, {'protocol_version':1, 'id':rid, 'bot_id':bot,
                               'operation':'import-external', 'payload':payload}, 0o640)
        return False

    def collect(self, path, now):
        record = read_json(path)
        if record['state'] not in ('QUEUED', 'COLLECTING') or record.get('next_poll', 0) > now:
            return
        directory = path.parent
        saved = directory / 'metadata.json'
        if record['state'] == 'QUEUED':
            if not saved.exists():
                # The current CLI's normalized `show --json` omits submission IDs.
                # Read-only browser attestation supplies the real own-team mapping;
                # a configured/expected source must never be passed off as measured.
                data = self.cli.run(['match-groups', 'show', record['group_id'], '--json'])
                require(data['groupId'] == record['group_id'] and
                        all(m['kind'] == 'unranked' for m in data['matches']), 'unexpected CLI group schema')
                record.update(next_poll=now + 60, awaiting_source_proof=True)
                atomic_json(path, record, 0o600)
                return
            data = read_json(saved)
            group = data['group']
            require(data['myTeamId'] == self.policy['team_id'] and group['kind'] == 'unranked' and
                    group['id'] == record['group_id'],
                    'official group identity/type changed')
            own = next(s for s in group['sides'] if s['teamId'] == self.policy['team_id'])
            require(own['submissionId'] == record.get('submission_id', self.policy['submission_id']),
                    'Team selected a different submission; stop challenges rather than overwrite it')
            if group['status'] not in ('finished', 'error'):
                record['next_poll'] = now + 60
                atomic_json(path, record, 0o600)
                return
            if group['status'] == 'error':
                record.update(state='PLATFORM_ERROR', detail='Unfinished/error series is not a strategic loss')
                atomic_json(path, record, 0o600)
                return
            record['state'] = 'COLLECTING'
            atomic_json(path, record, 0o600)
        data = read_json(saved)
        replay = directory / 'replays.zip'
        if not replay.exists():
            self.cli.run(['match-groups', 'download', record['group_id']], output=replay)
        require(replay.is_file() and zipfile.is_zipfile(replay), 'official replay download incomplete')
        done = []
        for match in data['matches']:
            require(match['status'] == 'finished', 'unfinished match cannot supply completed-game evidence')
            mid = str(uuid.UUID(match['id']))
            payload_path = directory / (mid + '-import.json')
            if not payload_path.exists():
                raw = directory / (mid + '-statistics.json')
                packed = raw.with_suffix('.json.gz')
                if packed.exists():
                    stats = json.loads(gzip.decompress(packed.read_bytes()))
                else:
                    if not raw.exists():
                        self.cli.run(['matches', 'summary', mid, '--json'], output=raw)
                    require(raw.stat().st_size <= 64 * 1024**2, 'official statistics exceed the reviewed bound')
                    stats = read_json(raw)
                    atomic_bytes(packed, gzip.compress(raw.read_bytes(), mtime=0), 0o600)
                    raw.unlink()  # Generated download now has a lossless canonical representation.
                payload = self.payload(data, match, record, stats, replay, packed)
                atomic_json(payload_path, payload, 0o600)
            done.append(self.import_payload(read_json(payload_path)))
        if all(done):
            record.update(state='IMPORTED', imported_at=now, games=len(done),
                          awaiting_source_proof=False, replay_sha256=file_hash(replay))
            self.state['imported_games'] += len(done)
        else:
            record['next_poll'] = now + 5
        atomic_json(path, record, 0o600)
        self.save()

    def payload(self, data, match, record, stats, replay, packed):
        own = next(s for s in match['sides'] if s['teamId'] == self.policy['team_id'])
        enemy = next(s for s in match['sides'] if s['teamId'] != self.policy['team_id'])
        winners = [s for s in match['sides'] if s['result'] == 'win']
        require(len(winners) == 1, 'ambiguous official match outcome')
        compact = compact_statistics(stats)
        require(compact['match']['outcome'] == 'team' + winners[0]['side'].upper(),
                'official metadata and statistics disagree')
        require(match['rounds'] == stats['match']['roundsStarted'] and all(
                compact['metrics']['submitted_gems']['value'][side['side'].upper()] == side['score']
                for side in match['sides']), 'official round/gem totals disagree with statistics')
        maps = read_json(self.config['map_manifest'])['maps']
        canonical_map = next((m['name'] for m in maps if m['sha256'] == stats['match']['mapHash']), None)
        require(canonical_map, 'official map bytes are absent from the frozen pool; retain and review')
        # The official raw replay and statistics stay on this server under rolling retention.
        observation = {'official_match_id':match['id'], 'group_id':record['group_id'],
            'source_commit':record['source_commit'], 'source_hash':record['source_hash'],
            'submission_id':record['submission_id'], 'own_side':own['side'].upper(),
            'outcome':winners[0]['side'].upper(), 'map_name':canonical_map, 'official_map_name':match['map'],
            'official_patch':match['patchId'], 'opponent_version':enemy.get('version'),
            'opponent_team_id':record['opponent_id'], 'opponent_rank_at_request':record['opponent_rank'],
            'rounds':match['rounds'], 'own_tributed_gems':own['score'], 'opponent_tributed_gems':enemy['score'],
            'own_draft_ids':own['draft'], 'opponent_draft_ids':enemy['draft'],
            'own_bot_faults':compact['metrics']['bot_faults_by_side']['value'][own['side'].upper()],
            'raw_archive':{'replay_bundle_sha256':file_hash(replay), 'statistics_gzip_sha256':file_hash(packed),
                           'statistics_sha256':hashlib.sha256(gzip.decompress(packed.read_bytes())).hexdigest()},
            'limits':['Uncontrolled outside game; not a local promotion score or a causal diagnosis.',
                      'Own submitted source is pinned; it may differ from this worker\'s edit base.',
                      'Opponent private source/logs are unavailable; unknown versions remain unknown.',
                      'Post-game observations are not omniscient live runtime inputs.']}
        files = {'observations.json':canonical(observation), 'final.json':canonical(compact)}
        require(all(len(v) < 700000 for v in files.values()), 'compact outside evidence unexpectedly large')
        return {**{k:observation[k] for k in ('official_match_id', 'source_commit', 'source_hash',
                'submission_id', 'own_side', 'outcome', 'map_name', 'official_patch', 'opponent_version',
                'opponent_team_id', 'opponent_rank_at_request', 'own_bot_faults')},
                'official_group_id':record['group_id'],
                'source_bot_id':record['bot_id'],
                'official_raw_statistics':{'request_id':record['request_id'],
                    'file':packed.name, 'stored_sha256':file_hash(packed),
                    'original_sha256':hashlib.sha256(gzip.decompress(packed.read_bytes())).hexdigest(),
                    'original_bytes':len(gzip.decompress(packed.read_bytes()))},
                'files':{name:base64.b64encode(value).decode() for name,value in files.items()}}

    def prune(self):
        # Only imported, reproducible download copies; journals/IDs and central feedback survive.
        budget = self.policy.get('archive_budget_bytes', 256 * 1024**2)
        files = [p for p in (self.root / 'requests').rglob('*') if p.is_file()]
        total = sum(p.stat().st_size for p in files)
        for path in self.records():
            if total <= budget:
                break
            record = read_json(path)
            if record['state'] != 'IMPORTED' or record['created_at'] > time.time() - 3600:
                continue
            remove = [p for p in path.parent.iterdir() if p.name != 'record.json' and p.is_file()]
            removed = sum(p.stat().st_size for p in remove)
            record['raw_retired'] = {'at':time.time(), 'reason':'oldest-first rolling archive budget',
                                     'files':{p.name:file_hash(p) for p in remove}}
            atomic_json(path, record, 0o600)
            for item in remove:
                item.unlink()
            total -= removed
            if total <= budget:
                break
        records = self.records()
        for path in records[:-2000]:
            record = read_json(path)
            if not record.get('raw_retired') or record['created_at'] > time.time() - 7 * 86400:
                continue
            with (self.root / 'retired-groups.jsonl').open('ab') as stream:
                stream.write(canonical(record) + b'\n')
                stream.flush()
                os.fsync(stream.fileno())
            path.unlink()
            path.parent.rmdir()

    def step(self):
        now = time.time()
        self.validate_source()
        require(self.policy.get('enabled') and self.config['official']['challenges'], 'outside play disabled')
        status_path = Path(self.config['root']) / 'public/status.json'
        arena_status = read_json(status_path) if status_path.exists() else {'paused':True}
        self.state['private_arena_paused'] = arena_status.get('paused', True)
        if not self.state.get('blocked'):
            if (self.state['private_arena_paused'] or arena_status.get('service_error') or
                    shutil.disk_usage(self.root).free <= self.config['limits']['minimum_free_bytes']):
                self.state['next_create'] = max(self.state['next_create'], now + 60)
            else:
                self.create(now)
            due = [p for p in self.records() if read_json(p)['state'] in ('QUEUED', 'COLLECTING') and
                   read_json(p).get('next_poll', 0) <= now]
            if due:
                self.collect(min(due, key=lambda p:read_json(p)['created_at']), now)
        self.prune()
        self.publish_status()

    def publish_status(self):
        records = [read_json(p) for p in self.records()]
        report = {'heartbeat':time.time(), 'enabled':self.policy['enabled'],
                  'source_commit':self.policy['source_commit'], 'submission_id':self.policy['submission_id'],
                  'target_groups_per_hour':50, 'games_per_group':5, 'uses_shared_team_quota':True,
                  'uploads_or_activation':False, **self.state,
                  'states':dict(Counter(r['state'] for r in records)),
                  'latest_groups':[{'id':r.get('group_id'), 'opponent_rank':r['opponent_rank'],
                                    'state':r['state']} for r in sorted(records, key=lambda r:r['created_at'])[-5:]]}
        atomic_json(Path(self.config['root']) / 'public/official-exploration.json', report, 0o644)
        atomic_json(Path(self.config['root']) / 'public/official-pending.json', {
            'team_id':self.policy['team_id'], 'submission_id':self.policy['submission_id'],
            'source_commit':self.policy['source_commit'],
            'requests':[{'request_id':r['request_id'], 'group_id':r['group_id']} for r in records
                        if r['state'] == 'QUEUED' and r.get('group_id')]}, 0o644)
