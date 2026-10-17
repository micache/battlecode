"""Focused two-phase archive tests; no network, accounts, inference or real games."""
import importlib.util
import json
from pathlib import Path
import shutil
from unittest.mock import patch, Mock

from test_arena import Harness, PROJECT
from arena.common import ArenaError, read_json
from arena.engine import seal_artifacts, verify_artifacts
from arena.offload import prepare, acknowledge, finish_cleanup
from arena.storage import archive_projects

spec = importlib.util.spec_from_file_location('offload_local', PROJECT / 'ops/offload-local.py')
operator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator)


class OffloadTests(Harness):
    def test_transient_read_retry_never_retries_permission_denial_or_writes(self):
        client = Mock()
        client.request.side_effect = [RuntimeError('synthetic connection loss'), {'status':'completed'}]
        with patch.object(operator.time, 'sleep'):
            self.assertEqual(operator.safe_get(client, '/process/existing-id', 'https://test'), {'status':'completed'})
        self.assertTrue(all(call.args[0] == 'GET' for call in client.request.call_args_list))
        client.reset_mock()
        client.request.side_effect = operator.APIError(403, 'synthetic denial')
        with self.assertRaises(operator.APIError):
            operator.safe_get(client, '/process/existing-id', 'https://test')
        self.assertEqual(client.request.call_count, 1)

    def setup_plan(self):
        self.establish()
        job = self.arena.db.one("SELECT * FROM match_jobs WHERE state='COMPLETED' LIMIT 1")
        old = Path(job['artifact'])
        (old / 'project').mkdir()
        (old / 'project/source.cpp').write_bytes(b'int main() {}')
        (old / 'artifacts').mkdir()
        (old / 'artifacts/replay.repl26a').write_bytes(b'original replay')
        (old / 'artifacts/final.json').write_bytes(b'{"original":"statistics"}')
        seal_artifacts(old, job['id'], job['attempt_count'], json.loads(job['result']))
        archive_projects(self.arena)
        job = self.arena.db.one('SELECT * FROM match_jobs WHERE id=?', (job['id'],))
        plan = prepare(self.arena, keep_recent=0)
        local = self.path / 'operator/batches'
        local.mkdir(parents=True)
        target = local / (plan['batch_id'] + '.tar')
        shutil.copyfile(plan['archive_path'], target)
        self.assertTrue(operator.verify_batch(target, plan))
        receipt = {'batch_id':plan['batch_id'], 'archive_sha256':plan['archive_sha256'],
                   'archive_root':str(local.parent), 'verified':True, 'fsynced':True}
        return job, plan, receipt, old, target

    def test_prepare_never_deletes_and_unverified_ack_never_deletes(self):
        job, plan, receipt, old, _ = self.setup_plan()
        self.assertTrue((Path(job['artifact']) / 'project.zip').is_file())
        self.assertEqual(prepare(self.arena)['batch_id'], plan['batch_id'])
        for invalid in (dict(receipt, verified=False), dict(receipt, archive_sha256='0'*64)):
            with self.assertRaises(ArenaError):
                acknowledge(self.arena, invalid)
        self.assertTrue((Path(job['artifact']) / 'project.zip').is_file())

    def test_ack_preserves_online_evidence_and_original_manifest_with_aliases(self):
        job, plan, receipt, legacy, _ = self.setup_plan()
        old = Path(job['artifact'])
        done = acknowledge(self.arena, receipt)
        new = Path(self.arena.db.one('SELECT artifact FROM match_jobs WHERE id=?', (job['id'],))['artifact'])
        self.assertTrue(old.is_symlink())
        self.assertTrue(legacy.is_symlink())
        self.assertEqual((legacy / 'artifacts/final.json').read_bytes(), b'{"original":"statistics"}')
        self.assertEqual((new / 'artifacts/replay.repl26a').read_bytes(), b'original replay')
        self.assertFalse((new / 'project.zip').exists())
        self.assertEqual(verify_artifacts(new, job['id'], job['attempt_count']), json.loads(job['result']))
        self.assertEqual(read_json(new / 'project-offload.json')['original_completion']['files']['project.zip'],
                         plan['entries'][0]['files']['project.zip']['sha256'])
        self.assertEqual(acknowledge(self.arena, receipt), done)
        self.assertIsNone(self.arena.db.get('offload_pending'))
        self.assertFalse(Path(plan['archive_path']).exists())
        archive_projects(self.arena)  # Ordinary maintenance understands offloaded worktrees.

    def test_crash_after_pointer_publication_preserves_then_recovers_originals(self):
        job, plan, receipt, _, _ = self.setup_plan()
        with patch('arena.offload.remove_redundant', side_effect=OSError('synthetic crash')):
            with self.assertRaises(OSError):
                acknowledge(self.arena, receipt)
        self.assertTrue((Path(job['artifact']) / 'project.zip').exists())
        acknowledge(self.arena, receipt)
        self.assertTrue(Path(job['artifact']).is_symlink())

    def test_corrupt_local_download_cannot_be_verified(self):
        job, plan, receipt, _, target = self.setup_plan()
        with target.open('r+b') as stream:
            stream.write(b'CORRUPT')
        with self.assertRaisesRegex(ArenaError, 'checksum mismatch'):
            operator.verify_batch(target, plan)
        self.assertTrue((Path(job['artifact']) / 'project.zip').exists())

    def test_default_keeps_recent_matches_and_plan_control_has_durable_response(self):
        job, plan, receipt, _, _ = self.setup_plan()
        acknowledge(self.arena, receipt)
        self.assertFalse(prepare(self.arena)['entries'])
        from arena.common import atomic_json
        response_id = 'c' * 32
        atomic_json(self.arena.root / 'control' / ('request-'+response_id+'.json'),
                    {'operation':'offload-plan', 'response_id':response_id})
        self.arena.consume_control()
        self.assertTrue(read_json(self.arena.root / 'public/offload/operator-results' / (response_id+'.json'))['ok'])
