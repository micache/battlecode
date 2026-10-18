"""Synthetic engine fixtures exercise orchestration, never certify game-engine behavior."""
import base64
import contextlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tempfile
import time
import unittest

from arena.common import (ArenaError, atomic_json, file_hash, identity, lock, read_json,
                          tree_hash, validate_schema)
from arena.config import load
from arena.db import Database
from arena.engine import normalize_result, seal_artifacts, verify_artifacts
from arena.evaluate import summarize
from arena.gitstore import git, ingest
from arena.operations import restore_drill
from arena.protocol import decode_source, encode_source
from arena.service import Arena
from arena.supervisor import dispatch_tasks, handle_request, quota_delay
from arena.worker import provider_failure


PROJECT = Path(__file__).resolve().parent.parent
ENGINE_HASH = "e" * 64


def synthetic_contract():
    return {"protocol_version": 1, "engine_sha256": ENGINE_HASH, "reviewed_by": "SYNTHETIC TEST ONLY",
            "fixture_sha256": "f" * 64, "replay_agreement_verified": True,
            "winner_pointer": "/synthetic_winner", "winner_values": {"red": "A", "blue": "B"},
            "complete_pointer": "/synthetic_done", "complete_value": True,
            "reason_pointer": "/synthetic_reason", "metric_pointers": {"lifetime_gold": "/absent"},
            "bot_fault_patterns": ["TEST_TRAP"], "fault_detection_verified": True,
            "fuel_suspension_patterns": ["TEST_SUSPEND"]}


class FakeEngine:
    """No real compilation or games. Used exclusively by tests."""
    lock_hash = "f" * 64
    lock = {"effective_profile": None}

    def __init__(self, root):
        self.root = root
        self.calls = []
        self.failures = 0
        self.on_run = None

    def prepare_bot(self, snapshot, revision_id):
        source_hash = tree_hash(Path(snapshot) / "src")
        build_id = identity({"source": source_hash, "engine": self.lock_hash})
        artifact = self.root / "fake-builds" / build_id
        artifact.parent.mkdir(exist_ok=True)
        artifact.write_bytes(b"SYNTHETIC, NOT WASM")
        return {"build_id": build_id, "source_hash": source_hash, "snapshot": str(snapshot),
                "revision_id": revision_id, "lock_hash": self.lock_hash, "artifact": str(artifact),
                "wasm_sha256": file_hash(artifact)}

    def run_match(self, spec, output):
        self.calls.append(json.loads(json.dumps(spec)))
        if self.on_run:
            self.on_run(spec)
        if self.failures:
            self.failures -= 1
            raise ArenaError("synthetic infrastructure failure")
        return {"protocol_version": 1, "state": "COMPLETED", "completed": True,
                "winner": "B", "terminal_reason": "synthetic-side-B-fixture", "metrics": {},
                "bot_faults": 0, "fuel_suspensions": None, "detail": None}

    def recover_containers(self):
        pass


class Harness(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        self.repo = self.path / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "user.email", "test@localhost")
        (self.repo / ".gitignore").write_text(".agent/\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "test infrastructure")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self.root = self.path / "runtime"
        self.root.mkdir()
        self.config = read_json(PROJECT / "config/pilot.json")
        # Preserve the historical synthetic nine-map fixtures. Current real
        # seventeen-map coverage has its own regression below.
        self.config['evaluation'].update(full_evaluation=False, development_maps=[
            'collision','corners','elkring','expanse','interlock','lanes'])
        self.config['limits']['improvement_interval_seconds'] = 0  # Fast synthetic event-driven fixtures.
        self.config.update({"root": str(self.root), "mirror": str(self.repo), "infrastructure_commit": self.base,
                            "infrastructure": str(PROJECT), "maps": str(self.path / "maps"),
                            "map_manifest": str(self.path / "maps.json"), "config_hash": "c" * 64})
        self.maps = self.path / "maps"
        self.maps.mkdir()
        pool = []
        for name in self.config["evaluation"]["development_maps"] + self.config["evaluation"]["holdout_maps"]:
            path = self.maps / (name + ".map26a")
            path.write_text("SYNTHETIC MAP: " + name)
            pool.append({"name": name, "sha256": file_hash(path)})
        atomic_json(self.path / "maps.json", {"maps": pool})
        self.engine = FakeEngine(self.root)
        self.arena = Arena(self.config, self.engine)

    def tearDown(self):
        self.arena.db.connection.close()
        self.temp.cleanup()

    def commit(self, bot, policy, parent=None):
        branch = f"bot/{bot}"
        exists = subprocess.run(["git", "-C", str(self.repo), "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"]).returncode == 0
        git(self.repo, "checkout", branch) if exists else git(self.repo, "checkout", "-b", branch, parent or self.base)
        path = self.repo / "bots" / bot / "src/main.cpp"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(policy)
        notes = self.repo / "experiments" / bot / "NOTES.md"
        notes.parent.mkdir(parents=True, exist_ok=True)
        notes.write_text("Synthetic test policy: " + policy)
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "synthetic " + bot + policy)
        commit = git(self.repo, "rev-parse", "HEAD")
        return ingest(self.arena.db, self.config, bot, commit)

    def finish_all(self):
        for _ in range(500):
            self.arena.advance_evaluations()
            worked = self.arena.run_one_match()
            self.arena.advance_evaluations()
            if not worked:
                break
        else:
            self.fail("scheduler did not terminate")

    def establish(self):
        alpha = self.commit("alpha", "int main() {}")
        beta = self.commit("beta", "int main() {}")
        self.arena.db.put("starter_verified", True)  # Synthetic precondition, never deployed readiness.
        self.arena.db.put("starter_revision", alpha["id"])
        for row in (alpha, beta):
            self.arena.start_evaluation(row["id"])
            self.finish_all()
            self.assertEqual(self.arena.db.one("SELECT state FROM revisions WHERE id=?", (row["id"],))["state"], "ACCEPTED")
        return alpha, beta


class IngestionTests(Harness):
    def test_immutable_snapshot_and_supersession(self):
        first = self.commit("alpha", "one")
        second = self.commit("alpha", "two")
        self.assertEqual((Path(first["snapshot"]) / "src/main.cpp").read_text(), "one")
        self.assertEqual(self.arena.db.one("SELECT state FROM revisions WHERE id=?", (first["id"],))["state"], "SUPERSEDED")
        self.assertEqual(second["state"], "PENDING")
        self.assertEqual(ingest(self.arena.db, self.config, "alpha", second["commit_sha"])["id"], second["id"])

    def test_outside_owned_paths_rejected(self):
        row = self.commit("alpha", "one")
        (self.repo / "evaluator.py").write_text("bad")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "bad edit")
        with self.assertRaisesRegex(ArenaError, "out-of-scope"):
            ingest(self.arena.db, self.config, "alpha", git(self.repo, "rev-parse", "HEAD"))

    def test_symlink_and_unexpected_dependency_rejected(self):
        self.commit("alpha", "one")
        path = self.repo / "bots/alpha/src/secret.h"
        path.symlink_to("/etc/shadow")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "bad link")
        with self.assertRaisesRegex(ArenaError, "symlink"):
            ingest(self.arena.db, self.config, "alpha", git(self.repo, "rev-parse", "HEAD"))

    def test_notes_only_no_re_evaluation(self):
        alpha, _ = self.establish()
        git(self.repo, "checkout", "bot/alpha")
        (self.repo / "experiments/alpha/NOTES.md").write_text("notes only")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "notes only")
        row = ingest(self.arena.db, self.config, "alpha", git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(row["state"], "NO_CHANGE")


class SchedulerTests(Harness):
    def test_full_promotion_has_nine_maps_three_fixed_opponents_and_head_to_head(self):
        self.establish()
        history_a = self.commit("alpha", "historical policy a")
        history_b = self.commit("beta", "historical policy b")
        candidate = self.commit("alpha", "synthetic stronger oracle")
        self.config["evaluation"].update(automatic_promotion=True,
                                         opponent_revision_ids=[history_a["id"], history_b["id"]])
        self.arena.db.put("readiness", {"private_arena_ready": True, "competition_parity_verified": True,
                                        "engine_lock_hash": self.engine.lock_hash})
        original = self.engine.run_match
        def oracle(spec, output):
            result = original(spec, output)
            if spec["a_source_hash"] == candidate["source_hash"]:
                result["winner"] = "A"
            elif spec["b_source_hash"] == candidate["source_hash"]:
                result["winner"] = "B"
            return result
        self.engine.run_match = oracle
        eid = self.arena.start_evaluation(candidate["id"])
        self.finish_all()
        evaluation = self.arena.db.one("SELECT * FROM evaluations WHERE id=?", (eid,))
        self.assertEqual(evaluation["state"], "ACCEPTED")
        self.assertEqual(len(self.arena.evaluation_cases(eid)), 126)
        self.assertEqual(json.loads(evaluation["metrics"])["paired_cases"], 27)
        self.assertEqual(self.arena.db.one("SELECT accepted_revision FROM bots WHERE id='alpha'")["accepted_revision"], candidate["id"])

    def test_two_cycles_each_bot_and_feedback_bound_to_commits(self):
        self.establish()
        for cycle in (1, 2):
            for bot in ("alpha", "beta"):
                row = self.commit(bot, f"synthetic variant {cycle}")
                evaluation_id = self.arena.start_evaluation(row["id"])
                self.finish_all()
                summary = read_json(self.root / "feedback" / bot / "latest.json")["summary"]
                self.assertEqual(summary["candidate"]["commit"], row["commit_sha"])
                self.assertEqual(summary["evaluation_id"], evaluation_id)
                self.assertEqual(summary["decision"], "INCONCLUSIVE")
                self.assertEqual(summary["coverage"], "provisional-three-map-wiring")
                validate_schema(summary, read_json(PROJECT / "schemas/feedback.schema.json"))
        self.assertEqual(self.arena.db.one("SELECT count(*) AS n FROM evaluations")["n"], 6)

    def test_push_during_running_job_keeps_frozen_inputs(self):
        self.establish()
        candidate = self.commit("alpha", "old candidate")
        eid = self.arena.start_evaluation(candidate["id"])
        before = self.arena.db.one("SELECT spec FROM match_jobs WHERE state='QUEUED'")["spec"]
        newer = []
        def push(spec):
            self.engine.on_run = None
            newer.append(self.commit("alpha", "new candidate"))
        self.engine.on_run = push
        self.arena.run_one_match()
        self.assertIn(candidate["source_hash"], before)
        self.assertNotIn(newer[0]["source_hash"], before)
        self.assertEqual(self.arena.db.one("SELECT state FROM revisions WHERE id=?", (candidate["id"],))["state"], "EVALUATING")

    def test_cache_does_not_create_independent_samples(self):
        alpha, _ = self.establish()
        build = self.arena.build(alpha["id"])
        map_info = self.arena.freeze_maps()["collision"]
        first = self.arena.queue_match(build, build, map_info)
        count = len(self.engine.calls)
        self.assertEqual(self.arena.queue_match(build, build, map_info), first)
        self.assertFalse(self.arena.run_one_match())
        self.assertEqual(len(self.engine.calls), count)

    def test_failure_retries_once_then_pauses(self):
        row = self.commit("alpha", "one")
        build = self.arena.build(row["id"])
        job = self.arena.queue_match(build, build, self.arena.freeze_maps()["collision"])
        self.engine.failures = 3
        self.assertTrue(self.arena.run_one_match())
        self.assertTrue(self.arena.run_one_match())
        self.assertFalse(self.arena.run_one_match())
        self.assertTrue(self.arena.db.get("adapter_paused"))
        self.assertEqual(self.arena.db.one("SELECT attempt_count FROM match_jobs WHERE id=?", (job,))["attempt_count"], 2)

    def test_restart_reconciles_atomic_artifact_without_duplicate(self):
        row = self.commit("alpha", "one")
        build = self.arena.build(row["id"])
        job = self.arena.queue_match(build, build, self.arena.freeze_maps()["collision"])
        original = self.arena.finish_match
        self.arena.finish_match = lambda *args: None  # Crash after rename, before DB transaction.
        self.arena.run_one_match()
        self.arena.finish_match = original
        self.assertEqual(self.arena.db.one("SELECT state FROM match_jobs WHERE id=?", (job,))["state"], "RUNNING")
        self.arena.recover()
        self.arena.recover()
        self.assertEqual(len(self.engine.calls), 1)
        self.assertEqual(self.arena.db.one("SELECT state FROM match_jobs WHERE id=?", (job,))["state"], "COMPLETED")
        self.assertEqual(self.arena.db.one("SELECT count(*) AS n FROM match_attempts")["n"], 1)

    def test_backup_restore_includes_wal(self):
        self.establish()
        backup = self.path / "backup.sqlite"
        self.arena.db.backup(backup)
        report = restore_drill(backup, self.path / "restored.sqlite")
        self.assertEqual(report["integrity"], "ok")
        with contextlib.closing(sqlite3.connect(self.path / "restored.sqlite")) as target:
            self.assertEqual(target.execute("SELECT count(*) FROM evaluations").fetchone()[0], 2)

    def test_two_writer_lock_excluded(self):
        with lock(self.root / "state/service.lock"):
            with self.assertRaises(ArenaError):
                with lock(self.root / "state/service.lock"):
                    self.fail("second writer admitted")

    def test_quota_parks_only_one_owner(self):
        self.establish()
        for worker in self.config["workers"].values():
            worker.update(enabled=True, owner_confirmed=True)
        self.arena.db.execute("UPDATE workers SET state='IDLE',paused=0")
        dispatch_tasks(self.arena)
        alpha = self.arena.db.one("SELECT * FROM workers WHERE id='alpha'")
        beta_before = self.arena.db.one("SELECT * FROM workers WHERE id='beta'")
        handle_request(self.arena, "alpha", {"operation": "worker-finished", "payload": {
            "task_id": alpha["task_id"], "state": "QUOTA_WAIT", "reset_at": time.time() + 3600}})
        after = self.arena.db.one("SELECT * FROM workers WHERE id='alpha'")
        self.assertEqual(after["state"], "QUOTA_WAIT")
        self.assertGreater(after["next_run"], time.time() + 3590)
        self.assertEqual(self.arena.db.one("SELECT * FROM workers WHERE id='beta'"), beta_before)
        dispatch_tasks(self.arena)
        beta = self.arena.db.one("SELECT * FROM workers WHERE id='beta'")
        self.assertEqual(beta["state"], "RUNNING")
        self.assertNotEqual(beta["task_id"], alpha["task_id"])

    def test_no_change_feedback_consumed_once(self):
        self.establish()
        self.config["workers"]["alpha"].update(enabled=True, owner_confirmed=True)
        self.arena.db.execute("UPDATE workers SET state='IDLE',paused=0 WHERE id='alpha'")
        dispatch_tasks(self.arena)
        worker = self.arena.db.one("SELECT * FROM workers WHERE id='alpha'")
        handle_request(self.arena, "alpha", {"operation": "worker-finished", "payload": {
            "task_id": worker["task_id"], "state": "NO_CHANGE"}})
        dispatch_tasks(self.arena)
        self.assertEqual(self.arena.db.one("SELECT count(*) AS n FROM tasks")["n"], 1)

    def test_disk_pressure_pauses_new_work(self):
        self.config["limits"]["minimum_free_bytes"] = 2 ** 100
        self.arena.db.put("paused", False)
        self.arena.step()
        self.assertTrue(self.arena.db.get("disk_pressure"))
        self.assertFalse(self.engine.calls)

    def test_map_change_rejected(self):
        (self.maps / "collision.map26a").write_text("modified")
        with self.assertRaisesRegex(ArenaError, "map hash"):
            self.arena.freeze_maps()


class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        atomic_json(self.path / "process-result.json", {"timeout": False, "returncode": 0})
        (self.path / "stdout.log").write_text("")
        (self.path / "stderr.log").write_text("TEST_SUSPEND")
        (self.path / "synthetic.repl26a").write_bytes(b"NOT A REAL REPLAY")
        self.stats(done=True)

    def tearDown(self):
        self.temp.cleanup()

    def stats(self, done, winner="blue"):
        atomic_json(self.path / "final.json", {"synthetic_done": done, "synthetic_winner": winner,
                                              "synthetic_reason": "synthetic full tie"})

    def normalize(self, contract=True):
        return normalize_result(self.path, synthetic_contract() if contract else None, ENGINE_HASH)

    def test_absolute_team_b_and_fuel_not_crash(self):
        result = self.normalize()
        self.assertEqual(result["winner"], "B")
        self.assertEqual(result["state"], "COMPLETED")
        self.assertEqual(result["bot_faults"], 0)
        self.assertEqual(result["fuel_suspensions"], 1)
        self.assertFalse(result["metrics"]["lifetime_gold"]["available"])
        validate_schema(result, read_json(PROJECT / "schemas/match.schema.json"))

    def test_truncated_crash_timeout_and_malformed_distinct(self):
        self.stats(False)
        self.assertEqual(self.normalize()["state"], "TRUNCATED")
        (self.path / "stderr.log").write_text("TEST_TRAP")
        self.assertEqual(self.normalize()["state"], "BOT_FAULT")
        atomic_json(self.path / "process-result.json", {"timeout": True, "returncode": -15})
        self.assertEqual(self.normalize()["state"], "TIMEOUT")
        atomic_json(self.path / "process-result.json", {"timeout": False, "returncode": 0})
        (self.path / "final.json").write_text("{not json}")
        self.assertEqual(self.normalize()["state"], "INFRA_ERROR")

    def test_no_parser_or_draw_never_scored(self):
        self.assertEqual(self.normalize(False)["state"], "INFRA_ERROR")
        self.stats(True, "draw")
        self.assertEqual(self.normalize()["state"], "INFRA_ERROR")

    def test_artifact_corruption_detected(self):
        result = self.normalize()
        seal_artifacts(self.path, "test-job", 1, result)
        self.assertEqual(verify_artifacts(self.path, "test-job", 1), result)
        (self.path / "stdout.log").write_text("changed")
        with self.assertRaisesRegex(ArenaError, "checksum"):
            verify_artifacts(self.path, "test-job", 1)


class GateTests(unittest.TestCase):
    def cases(self, names, candidate_wins=True):
        cases = []
        for name in names:
            for role in ("candidate", "incumbent"):
                for side in ("A", "B"):
                    cases.append({"job_id": identity([name, role, side]), "candidate_side": side,
                                  "role": role, "map_name": name, "opponent": "frozen",
                                  "result": {"state": "COMPLETED", "completed": True, "bot_faults": 0,
                                             "winner": side if role == "candidate" and candidate_wins else ("B" if side == "A" else "A")}})
        return cases

    def test_full_gate_requires_holdout_and_complete_side_pairs(self):
        gate = {"minimum_gain": 0.05, "maximum_map_drop": 0.25}
        cases = self.cases(["dev", "holdout"])
        self.assertEqual(summarize(cases, gate, ["holdout"], True)["decision"], "ACCEPTED")
        cases[-1]["result"] = None
        self.assertEqual(summarize(cases, gate, ["holdout"], True)["decision"], "INCONCLUSIVE")
        self.assertNotEqual(summarize(self.cases(["dev"]), gate, ["holdout"], True)["decision"], "ACCEPTED")

    def test_unknown_reliability_blocks_promotion(self):
        cases = self.cases(["holdout"])
        cases[0]["result"]["bot_faults"] = None
        self.assertEqual(summarize(cases, {"minimum_gain": 0.05, "maximum_map_drop": 0.25}, ["holdout"], True)["decision"], "INCONCLUSIVE")


class ProtocolTests(unittest.TestCase):
    def test_path_traversal_and_size_limits(self):
        with self.assertRaises(ArenaError):
            decode_source({"../../escape.cpp": base64.b64encode(b"x").decode()})
        with self.assertRaises(ArenaError):
            decode_source({"Makefile": "eA=="})
        with self.assertRaises(ArenaError):
            decode_source({"large.cpp": "x" * 350001})

    def test_quota_backoff_uses_provider_reset(self):
        self.assertTrue(1800 <= quota_delay(0, now=0) <= 1830)
        self.assertTrue(14400 <= quota_delay(5, now=0) <= 14430)
        self.assertTrue(5000 <= quota_delay(0, reset_at=5000, now=0) <= 5030)

    def test_model_failure_not_successful_publication(self):
        with tempfile.TemporaryDirectory() as path:
            atomic_json(Path(path) / "stdout.log", {"type": "error", "error": {"code": "usage_limit_reached", "reset_at": 12345}})
            self.assertEqual(provider_failure(path, {"timeout": False})["state"], "QUOTA_WAIT")
            self.assertEqual(provider_failure(path, {"timeout": True})["state"], "PAUSED")

    def test_config_fails_closed_on_billing_and_official_actions(self):
        with tempfile.TemporaryDirectory() as path:
            config = read_json(PROJECT / "config/pilot.json")
            config["infrastructure_commit"] = "a" * 40
            file = Path(path) / "config.json"
            atomic_json(file, config)
            self.assertEqual(set(load(file)["workers"]), {"alpha", "beta"})
            config["billing"]["api_fallback"] = True
            atomic_json(file, config)
            with self.assertRaises(ArenaError):
                load(file)


if __name__ == "__main__":
    unittest.main()
