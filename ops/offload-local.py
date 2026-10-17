#!/usr/bin/env python3
"""Operator-side verified archive relay. Runs without any coding-model calls.

Only redundant project.zip worktrees leave the server. All gameplay evidence
remains online. An unavailable operator machine eventually triggers the normal
server disk guard; it never authorizes dropping an unacknowledged original.
"""
import argparse
import base64
import fcntl
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shlex
import shutil
import sys
import tarfile
import time
import uuid
import zipfile

REPOSITORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPOSITORY))
from arena.common import atomic_bytes, atomic_json, file_hash, identity, read_json, require
from ops.blaxel import APIError, Client, CREDENTIALS


def safe_get(client, path, endpoint, raw=False):
    """Only reads retry transport failures; never repeat POST or permission errors."""
    for attempt in range(3):
        try:
            return client.request('GET', path, base=endpoint, raw=raw)
        except APIError:
            raise
        except RuntimeError:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))


def verify_batch(path, plan):
    """Verify transport, original seals and every restored worktree member byte."""
    require(file_hash(path) == plan['archive_sha256'], 'downloaded archive checksum mismatch')
    with tarfile.open(path, 'r:*') as archive:
        members = archive.getmembers()
        expected = {'manifest.json'} | {e['job_id'] + '/' + name for e in plan['entries'] for name in e['files']}
        require(len(members) == len(expected) and {m.name for m in members} == expected and
                all(m.isfile() and not m.issym() and not m.islnk() for m in members), 'unexpected archive members')
        manifest = json.load(archive.extractfile('manifest.json'))
        require(manifest['entries'] == plan['entries'] and manifest['batch_id'] == plan['batch_id'] and
                identity(manifest['entries']) == plan['batch_id'], 'batch identity mismatch')
        for entry in plan['entries']:
            data = {}
            for name, expected_file in entry['files'].items():
                member = archive.getmember(entry['job_id'] + '/' + name)
                require(member.size == expected_file['size'] and member.size <= 48 * 1024**2, 'unexpected member size')
                data[name] = archive.extractfile(member).read()
                require(hashlib.sha256(data[name]).hexdigest() == expected_file['sha256'], 'archived file checksum mismatch')
            seal = json.loads(data['completion.json'])
            require(seal['job_id'] == entry['job_id'] and seal['attempt'] == entry['attempt'] and
                    seal['files']['project.zip'] == entry['files']['project.zip']['sha256'] and
                    seal['files']['project-archive.json'] == entry['files']['project-archive.json']['sha256'],
                    'original seal attribution mismatch')
            project = json.loads(data['project-archive.json'])
            hashes = {}
            with zipfile.ZipFile(io.BytesIO(data['project.zip'])) as restored:
                names = restored.namelist()
                require(len(names) == len(set(names)), 'duplicate project archive members')
                for name in names:
                    pure = PurePosixPath(name)
                    require(not pure.is_absolute() and '..' not in pure.parts and '\\' not in name, 'unsafe project member')
                    digest = hashlib.sha256()
                    with restored.open(name) as stream:
                        for block in iter(lambda: stream.read(1024**2), b''):
                            digest.update(block)
                    hashes[name] = digest.hexdigest()
            require(hashes == project['files'], 'restored worktree hashes differ')
    return True


class Relay:
    def __init__(self, directory):
        self.root = directory.resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        for name in ('batches', 'receipts'):
            (self.root / name).mkdir(exist_ok=True, mode=0o700)
        self.state_path = self.root / 'operator-state.json'
        self.state = read_json(self.state_path) if self.state_path.exists() else {}
        require(CREDENTIALS.stat().st_mode & 0o777 == 0o600 and not CREDENTIALS.is_symlink(), 'private operator credential required')
        config = read_json(CREDENTIALS)
        self.client = Client(config['key'], config['workspace'])
        self.endpoint = self.client.endpoint()

    def save(self):
        atomic_json(self.state_path, self.state, 0o600)

    def reconcile(self):
        pending = self.state.get('pending')
        if not pending:
            return
        deadline = time.monotonic() + 650
        while True:
            # A missing named process after an ambiguous POST requires inspection;
            # it is not permission to submit another administrative command.
            process = safe_get(self.client, '/process/' + pending['process'], self.endpoint)
            if process['status'] in ('completed', 'failed', 'killed', 'stopped'):
                break
            require(time.monotonic() < deadline, 'operator request still pending; next timer reconciles the same ID')
            time.sleep(3)
        import urllib.parse
        result_path = '/srv/battlecode/public/offload/operator-results/' + pending['request_id'] + '.json'
        data = safe_get(self.client, '/filesystem/' + urllib.parse.quote(result_path, safe=''), self.endpoint, raw=True)
        response = json.loads(data)
        if not response['ok']:
            self.state['pending'] = None
            self.save()
            raise RuntimeError('arena rejected offload request: ' + response['error'])
        require(process.get('exitCode') == 0, 'operator process failed; response preserved')
        result = response['result']
        if pending['operation'] == 'offload-plan':
            self.state['plan'] = result if result.get('batch_id') else None
        else:
            receipt = read_json(self.root / 'receipts' / (result['batch_id'] + '.json'))
            atomic_json(self.root / 'receipts' / (result['batch_id'] + '.json'), dict(receipt, server_acknowledgement=result), 0o600)
            self.state['plan'] = None
            self.state['last_completed'] = result
        self.state['pending'] = None
        self.save()

    def invoke(self, operation, payload=None):
        require(not self.state.get('pending'), 'reconcile existing request first')
        request_id = uuid.uuid4().hex
        name = 'offload-' + request_id
        encoded = base64.b64encode(json.dumps(payload or {}).encode()).decode()
        args = ['python3', '/opt/battlecode/ops/as-arena.py', 'python3', '/opt/battlecode/ops/offload-remote.py',
                operation, '--request-id', request_id, '--payload', encoded]
        self.state['pending'] = {'process':name, 'request_id':request_id, 'operation':operation}
        self.save()  # Unknown creation outcomes reconcile by this durable name.
        self.client.request('POST', '/process', {'command':shlex.join(args), 'name':name, 'waitForCompletion':False,
                            'keepAlive':True, 'timeout':700}, base=self.endpoint)
        self.reconcile()

    def download_and_acknowledge(self):
        plan = self.state['plan']
        batch = plan['batch_id']
        require(len(batch) == 64 and all(c in '0123456789abcdef' for c in batch), 'invalid server batch ID')
        archive_name = Path(plan['archive_path']).name
        require(archive_name in (batch + '.tar', batch + '.tar.xz'), 'unexpected archive name')
        target = self.root / 'batches' / archive_name
        if not target.exists():
            require(shutil.disk_usage(self.root).free > plan['archive_size'] + 2 * 1024**3, 'local archive storage reserve reached')
            import urllib.parse
            expected_path = '/srv/battlecode/public/offload/' + archive_name
            require(plan['archive_path'] == expected_path and plan['archive_size'] <= 48 * 1024**2, 'unexpected download target')
            data = safe_get(self.client, '/filesystem/' + urllib.parse.quote(expected_path, safe=''), self.endpoint, raw=True)
            require(len(data) == plan['archive_size'] and hashlib.sha256(data).hexdigest() == plan['archive_sha256'],
                    'transport checksum/size mismatch; remote originals retained')
            atomic_bytes(target, data, 0o600)  # File and directory fsynced before acknowledgement.
        verify_batch(target, plan)
        receipt = {'batch_id':batch, 'archive_sha256':plan['archive_sha256'], 'archive_root':str(self.root),
                   'verified':True, 'fsynced':True, 'verified_at':time.time()}
        atomic_json(self.root / 'receipts' / (batch + '.json'), {'receipt':receipt, 'plan':plan}, 0o600)
        self.invoke('offload-ack', receipt)
        print(json.dumps({'batch':batch, 'matches':len(plan['entries']), 'offloaded_project_bytes':plan['project_bytes']}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=Path.home() / '.local/share/battlecode-arena-archive')
    parser.add_argument('--max-batches', type=int, default=8)
    args = parser.parse_args()
    args.archive.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (args.archive / 'relay.lock').open('a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Another archive relay is already running.')
            return
        try:
            relay = Relay(args.archive)
            relay.reconcile()
            for _ in range(args.max_batches):
                if not relay.state.get('plan'):
                    relay.invoke('offload-plan')
                if not relay.state.get('plan'):
                    break
                relay.download_and_acknowledge()
            atomic_json(args.archive / 'status.json', {'ok':True, 'checked_at':time.time(),
                        'last_completed':relay.state.get('last_completed'), 'archive_root':str(relay.root)}, 0o600)
        except Exception as exc:
            atomic_json(args.archive / 'status.json', {'ok':False, 'checked_at':time.time(),
                        'error':str(exc), 'remote_originals':'Never deleted without prior verified local acknowledgement.'}, 0o600)
            raise


if __name__ == '__main__':
    main()
