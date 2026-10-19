import json
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch

from test_arena import Harness
from arena.common import ArenaError, atomic_json, bounded_process, read_json
from arena.engine import seal_artifacts, verify_artifacts
from arena.operations import acceptance_report, compact, ensure_starter_reference, import_external
from arena.supervisor import handle_request


class OperationsTests(Harness):
    def test_disk_error_cannot_leave_an_orphan_running_beside_new_games(self):
        self.establish()
        starter = self.arena.build(self.arena.db.get('starter_revision'))
        job = self.arena.queue_match(starter, starter, self.arena.freeze_maps()['collision'], repetition='disk-error')
        self.arena.db.put('paused',True)
        with patch('arena.service.seal_artifacts',side_effect=OSError(28,'No space left on device')):
            with self.assertRaises(OSError):
                self.arena.run_one_match(job)
        self.assertEqual(self.arena.db.one('SELECT state FROM match_jobs WHERE id=?',(job,))['state'],'RUNNING')
        with self.assertRaisesRegex(ArenaError,'needs recovery'):
            self.arena.run_one_match()
        self.arena.step()
        row = self.arena.db.one('SELECT * FROM match_jobs WHERE id=?',(job,))
        self.assertEqual(row['state'],'QUEUED')
        self.assertEqual(row['attempt_count'],1)
        self.assertFalse(json.loads(row['result'])['completed'])
        self.assertIsNone(json.loads(row['result'])['winner'])
        self.assertTrue((Path(row['artifact'])/'spec.json').exists())

    def test_bot_check_runs_its_two_games_before_older_evaluation_backlog(self):
        import base64
        from arena.supervisor import check_source, new_task
        self.establish()
        starter = self.arena.build(self.arena.db.get('starter_revision'))
        map_info = self.arena.freeze_maps()['collision']
        older = [self.arena.queue_match(starter, starter, map_info, repetition='older-'+str(i))
                 for i in range(5)]
        self.engine.calls.clear()
        task = new_task(self.arena,'alpha')
        report = check_source(self.arena,'alpha', {'task_id':task['task_id'],
            'source':{'main.cpp':base64.b64encode(b'synthetic priority candidate').decode()}})
        self.assertEqual(report['state'],'PASSED')
        self.assertEqual(len(self.engine.calls),2)
        self.assertEqual({r['job_id'] for r in self.engine.calls},set(report['matches']))
        self.assertTrue(all(self.arena.db.one('SELECT state FROM match_jobs WHERE id=?',(job,))['state']=='QUEUED'
                            for job in older))

    def smoke_fixture(self, bot='alpha', map_name='collision'):
        import base64
        from arena.supervisor import check_source, new_task
        self.establish()
        task = new_task(self.arena, bot)
        self.config['evaluation']['screen_maps'] = [map_name]
        report = check_source(self.arena, bot, {'task_id':task['task_id'],
                    'source':{'main.cpp':base64.b64encode(b'synthetic smoke candidate').decode()}})
        jobs = report['matches']
        for job in jobs:
            row = self.arena.db.one('SELECT * FROM match_jobs WHERE id=?', (job,))
            artifacts = Path(row['artifact']) / 'artifacts'
            artifacts.mkdir(exist_ok=True)
            (artifacts / 'bot-a.stdout.log').write_text('trusted smoke diagnostic')
            (artifacts / 'bot-b.stdout.log').write_text('other side smoke diagnostic')
            (artifacts / 'final.json').write_text('{"synthetic":true}')
        key = f"check:{task['task_id']}:{report['source_hash']}"
        return task, jobs[0], key, report

    def test_own_smoke_slice_without_evaluation_membership(self):
        _, job, _, _ = self.smoke_fixture()
        self.assertFalse(self.arena.db.one('SELECT job_id FROM evaluation_cases WHERE job_id=?', (job,)))
        result = handle_request(self.arena, 'alpha', {'operation':'slice',
                                'payload':{'match_id':job, 'file':'bot-a.stdout.log', 'limit':7}})
        self.assertEqual(result['text'], 'trusted')
        self.assertEqual(result['match_id'], job)

    def test_another_lane_cannot_export_smoke_by_guessing_id(self):
        _, job, _, _ = self.smoke_fixture()
        with self.assertRaisesRegex(ArenaError, 'development evidence'):
            handle_request(self.arena, 'beta', {'operation':'slice', 'payload':{'match_id':job}})

    def test_smoke_report_does_not_grant_holdout_access(self):
        _, job, _, _ = self.smoke_fixture(map_name='monolith')
        with self.assertRaisesRegex(ArenaError, 'development evidence'):
            handle_request(self.arena, 'alpha', {'operation':'slice', 'payload':{'match_id':job}})

    def test_smoke_report_must_match_trusted_task_and_actual_source(self):
        _, job, key, report = self.smoke_fixture()
        for field, value in [('bot_id','beta'), ('task_id','unknown'), ('source_hash','f'*64), ('matches',[])]:
            with self.subTest(field=field):
                self.arena.db.put(key, dict(report, **{field:value}))
                with self.assertRaisesRegex(ArenaError, 'development evidence'):
                    handle_request(self.arena, 'alpha', {'operation':'slice', 'payload':{'match_id':job}})

    def test_latest_smoke_evidence_survives_rolling_retention(self):
        from arena.retention import protected_jobs
        from arena.supervisor import new_task
        _, job, _, _ = self.smoke_fixture()
        self.assertIn(job, protected_jobs(self.arena))
        new_task(self.arena, 'alpha')
        self.assertIn(job, protected_jobs(self.arena))

    def test_smoke_recovery_verifies_access_and_preserves_blocked_history(self):
        import runpy
        from test_arena import PROJECT
        resolve = runpy.run_path(str(PROJECT / 'ops/resolve-smoke-pauses.py'))['resolve']
        task, _, _, _ = self.smoke_fixture()
        reason = 'Trusted checks passed, but smoke-log export was denied by the evidence gate.'
        result = json.dumps({'outcome':'BLOCKED', 'blocked_reason':reason})
        self.arena.db.execute("UPDATE tasks SET state='PAUSED',result=? WHERE id=?", (result,task['task_id']))
        self.arena.db.execute("UPDATE workers SET state='PAUSED',paused=0,detail=? WHERE id='alpha'", (reason,))
        self.arena.db.put('paused', True)
        receipt = resolve(self.arena, 'alpha')
        self.assertEqual(len(receipt['probes']), 6)
        self.assertEqual(self.arena.db.one("SELECT state FROM workers WHERE id='alpha'")['state'], 'IDLE')
        old = self.arena.db.one('SELECT * FROM tasks WHERE id=?', (task['task_id'],))
        self.assertEqual(old['state'], 'PAUSED')
        self.assertEqual(old['result'], result)
        self.assertIsNone(old['published_commit'])
        self.assertTrue(resolve(self.arena, 'alpha')['already_resolved'])

    def test_smoke_recovery_does_not_resume_other_permission_or_auth_failures(self):
        import runpy
        from test_arena import PROJECT
        resolve = runpy.run_path(str(PROJECT / 'ops/resolve-smoke-pauses.py'))['resolve']
        task, _, _, _ = self.smoke_fixture()
        reason = 'Owner must log in again'
        self.arena.db.execute("UPDATE tasks SET state='PAUSED',result=? WHERE id=?",
                              (json.dumps({'outcome':'BLOCKED','blocked_reason':reason}),task['task_id']))
        self.arena.db.execute("UPDATE workers SET state='PAUSED',paused=0,detail=? WHERE id='alpha'", (reason,))
        self.arena.db.put('paused', True)
        with self.assertRaisesRegex(ArenaError, 'not the known'):
            resolve(self.arena, 'alpha')
        self.assertEqual(self.arena.db.one("SELECT state FROM workers WHERE id='alpha'")['state'], 'PAUSED')

    def test_daily_backup_uses_only_service_writer_even_while_paused(self):
        from unittest.mock import patch
        self.config['limits']['backup_interval_seconds'] = 86400
        self.arena.db.put('paused', True)
        with patch('arena.operations.backup') as backup:
            self.arena.step()
            self.arena.step()
        backup.assert_called_once_with(self.arena)
        self.assertGreater(self.arena.db.get('last_backup_at'), 0)

    def test_independent_starter_does_not_replace_existing_lanes(self):
        import shutil
        alpha = self.commit("alpha", "existing nonstarter bot")
        shutil.copytree(Path(alpha["snapshot"]) / "src", self.root / "starter/src")
        self.arena.db.put("starter_verified", True)
        reference = ensure_starter_reference(self.arena)
        self.assertEqual(ensure_starter_reference(self.arena), reference)
        row = self.arena.db.one("SELECT * FROM revisions WHERE id=?", (reference,))
        self.assertEqual(row["bot_id"], "starter")
        self.assertEqual(len(row["commit_sha"]), 40)
        self.assertEqual(self.arena.db.one("SELECT latest_tip FROM bots WHERE id='alpha'")["latest_tip"], alpha["commit_sha"])

    def test_acceptance_never_counts_synthetic_or_manual_cycles(self):
        self.establish()
        report = acceptance_report(self.arena)
        self.assertFalse(report["verified"])
        self.assertEqual(report["cycles"], {"alpha": [], "beta": []})

    def test_holdout_slice_is_denied(self):
        alpha, beta = self.establish()
        build = self.arena.build(alpha["id"])
        job = self.arena.queue_match(build, build, self.arena.freeze_maps()["monolith"])
        evaluation = self.arena.db.one("SELECT id FROM evaluations LIMIT 1")["id"]
        self.arena.db.execute("INSERT INTO evaluation_cases VALUES(?,?, 'A','candidate','monolith',?,'promotion')", (evaluation, job, beta["id"]))
        with self.assertRaisesRegex(ArenaError, "development evidence"):
            handle_request(self.arena, "alpha", {"operation": "slice", "payload": {"match_id": job}})

    def test_external_replay_import_has_real_id_and_source_hash(self):
        alpha, _ = self.establish()
        directory = self.root / "external-inbox/alpha"
        directory.mkdir(parents=True)
        (directory / "sample.repl26a").write_bytes(b"SYNTHETIC EXTERNAL REPLAY")
        payload = {"official_match_id": "synthetic-official-id", "source_commit": alpha["commit_sha"],
                   "submission_id": "synthetic-submission", "outcome": "UNKNOWN", "staged_replay": "sample.repl26a"}
        result = import_external(self.arena, "alpha", payload)
        metadata = read_json(Path(result["artifact"]) / "metadata.json")
        self.assertIsNone(metadata["opponent_version"])
        self.assertFalse(metadata["controlled_local_evidence"])
        self.assertTrue(metadata["file_sha256"])
        with self.assertRaises(ArenaError):
            import_external(self.arena, "alpha", payload)

    def test_compression_preserves_verified_bytes(self):
        import gzip
        alpha = self.commit("alpha", "one")
        build = self.arena.build(alpha["id"])
        job = self.arena.queue_match(build, build, self.arena.freeze_maps()["collision"])
        self.arena.run_one_match()
        row = self.arena.db.one("SELECT * FROM match_jobs WHERE id=?", (job,))
        directory = Path(row["artifact"])
        (directory / "record.repl26a").write_bytes(b"synthetic replay" * 1000)
        seal_artifacts(directory, job, 1, json.loads(row["result"]))
        self.arena.db.execute("UPDATE match_jobs SET created=0 WHERE id=?", (job,))
        result = compact(self.arena)
        self.assertEqual(len(result["compressed_replays"]), 1)
        with gzip.open(result["compressed_replays"][0], "rb") as replay:
            self.assertEqual(replay.read(), b"synthetic replay" * 1000)
        new_path = self.arena.db.one("SELECT artifact FROM match_jobs WHERE id=?", (job,))["artifact"]
        verify_artifacts(new_path, job, 1)
        self.assertTrue(directory.is_symlink())
        self.assertEqual(directory.resolve(), Path(new_path).resolve())

    def test_bounded_child_timeout_retains_process_evidence(self):
        output = self.path / "child-evidence"
        result = bounded_process([sys.executable, "-c", "import time; time.sleep(30)"], self.path, output, 0.05)
        self.assertTrue(result["timeout"])
        self.assertLess(result["elapsed_seconds"], 6)
        self.assertTrue((output / "process.json").exists())
