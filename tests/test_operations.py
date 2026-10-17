import json
from pathlib import Path
import subprocess
import sys
import time

from test_arena import Harness
from arena.common import ArenaError, atomic_json, bounded_process, read_json
from arena.engine import seal_artifacts, verify_artifacts
from arena.operations import acceptance_report, compact, ensure_starter_reference, import_external
from arena.supervisor import handle_request


class OperationsTests(Harness):
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
