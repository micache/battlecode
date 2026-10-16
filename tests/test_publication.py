"""Real local Git transport, synthetic engine/check results, no model or network calls."""
import json
import os
from pathlib import Path
from unittest.mock import patch

from test_arena import Harness, PROJECT
from arena.common import ArenaError, atomic_json, read_json, tree_hash
from arena.gitstore import git
from arena.supervisor import dispatch_tasks, handle_request
from arena.worker import make_attempt, publish_attempt


class PublicationTests(Harness):
    def setUp(self):
        super().setUp()
        self.establish()
        self.remote = self.path / "remote.git"
        self.remote.mkdir()
        git(self.remote, "init", "--bare")
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "--all", "origin")
        self.config["repository_url"] = str(self.remote)
        for settings in self.config["workers"].values():
            settings.update(enabled=True, owner_confirmed=True)
        self.arena.db.execute("UPDATE workers SET state='IDLE',paused=0")
        self.owner_configs = {}
        for bot in ("alpha", "beta"):
            clone = self.path / f"owner-{bot}"
            from arena.common import run
            run(["git", "clone", "--branch", f"bot/{bot}", str(self.remote), str(clone)])
            self.owner_configs[bot] = {"bot_id": bot, "branch": f"bot/{bot}", "root": str(self.root),
                                       "infrastructure": str(PROJECT), "attempts": str(self.path / f"attempts-{bot}"),
                                       "clone": str(clone), "read_repository": str(self.remote)}

    def envelope(self):
        dispatch_tasks(self.arena)
        worker = self.arena.db.one("SELECT * FROM workers WHERE state='RUNNING'")
        self.assertIsNotNone(worker)
        task = json.loads(self.arena.db.one("SELECT envelope FROM tasks WHERE id=?", (worker["task_id"],))["envelope"])
        return worker["id"], task

    def final_result(self, bot, task):
        return {"protocol_version": 1, "task_id": task["task_id"], "bot_id": bot,
                "base_source_hash": task["base_source_hash"], "outcome": "READY_FOR_EVAL",
                "hypothesis": "synthetic fixture only", "changed_paths": ["model's list is ignored"],
                "evidence": [], "tests": [], "blocked_reason": None, "next_action": "evaluate"}

    def request(self, config, operation, payload=None, **kwargs):
        return handle_request(self.arena, config["bot_id"], {"operation": operation, "payload": payload or {}})

    def test_two_published_cycles_per_lane_start_from_accepted_source(self):
        seen = {"alpha": 0, "beta": 0}
        commits = set()
        evidence = []
        with patch("arena.worker.request", self.request):
            for cycle in range(4):
                bot, task = self.envelope()
                config = self.owner_configs[bot]
                Path(config["attempts"]).mkdir(exist_ok=True)
                attempt = make_attempt(config, task)
                self.assertEqual(tree_hash(attempt / "bots" / bot / "src"), task["base_source_hash"])
                source = attempt / "bots" / bot / "src/main.cpp"
                source.write_text(f"synthetic {bot} candidate {seen[bot]} {cycle}")
                notes = attempt / "experiments" / bot / "NOTES.md"
                notes.write_text("synthetic experiment")
                atomic_json(attempt / ".agent" / f"final-{task['task_id']}.json", self.final_result(bot, task))
                publication = publish_attempt(config, attempt)
                commits.add(publication["commit"])
                self.assertEqual(len(publication["commit"]), 40)
                self.request(config, "worker-finished", publication)
                revision = self.arena.db.one("SELECT * FROM revisions WHERE bot_id=? AND commit_sha=?", (bot, publication["commit"]))
                self.assertEqual(revision["source_hash"], publication["source_hash"])
                self.arena.start_evaluation(revision["id"])
                self.finish_all()
                feedback = read_json(self.root / "feedback" / bot / "latest.json")["summary"]
                self.assertEqual(feedback["candidate"]["commit"], publication["commit"])
                evidence.append({"bot": bot, "commit": publication["commit"], "task_id": task["task_id"],
                                 "evaluation_id": feedback["evaluation_id"], "source_hash": publication["source_hash"],
                                 "cases": self.arena.evaluation_cases(feedback["evaluation_id"])})
                seen[bot] += 1
                # Let the other independent owner consume its feedback next.
                self.arena.db.execute("UPDATE workers SET paused=1 WHERE id=?", (bot,))
                other = "beta" if bot == "alpha" else "alpha"
                if seen[other] < 2:
                    self.arena.db.execute("UPDATE workers SET paused=0 WHERE id=?", (other,))
        self.assertEqual(seen, {"alpha": 2, "beta": 2})
        self.assertEqual(len(commits), 4)
        if os.environ.get("ARENA_TEST_EVIDENCE_DIR"):
            directory = Path(os.environ["ARENA_TEST_EVIDENCE_DIR"])
            directory.mkdir(parents=True, exist_ok=True)
            atomic_json(directory / "synthetic-cycles.json", {
                "synthetic_engine": True, "real_models_or_games": False,
                "note": "Actual temporary local Git commits; fake engine/checker. Not pilot acceptance.",
                "cycles": evidence})
            git(self.remote, "bundle", "create", str(directory / "synthetic-publication.bundle"), "--all")

    def test_malformed_identity_and_outside_edit_do_not_publish(self):
        bot, task = self.envelope()
        config = self.owner_configs[bot]
        Path(config["attempts"]).mkdir()
        attempt = make_attempt(config, task)
        result = self.final_result(bot, task)
        result["task_id"] = "stale-result"
        atomic_json(attempt / ".agent" / f"final-{task['task_id']}.json", result)
        with self.assertRaisesRegex(ArenaError, "identity"):
            publish_attempt(config, attempt)
        result["task_id"] = task["task_id"]
        atomic_json(attempt / ".agent" / f"final-{task['task_id']}.json", result)
        (attempt / "evaluation-thresholds.json").write_text("bad change")
        with self.assertRaisesRegex(ArenaError, "out-of-scope"):
            publish_attempt(config, attempt)

    def test_attempt_entry_attests_source_and_identifies_own_recovery_root(self):
        bot, task = self.envelope()
        config = self.owner_configs[bot]
        Path(config['attempts']).mkdir()
        attempt = make_attempt(config, task)
        entry = read_json(attempt / '.agent/entry.json')
        self.assertTrue(entry['accepted_source_verified'])
        self.assertEqual(entry['source_hash'], task['base_source_hash'])
        self.assertEqual(entry['head'], task['input_revision'])
        self.assertEqual(entry['attempts_root'], config['attempts'])

    def test_manual_handoff_retains_lease_and_uses_trusted_publication(self):
        bot = "alpha"
        handle_request(self.arena, bot, {"operation": "pause"})
        claim = handle_request(self.arena, bot, {"operation": "claim", "payload": {"owner": "alpha-laptop"}})
        task = claim["task"]
        self.assertEqual(handle_request(self.arena, bot, {"operation": "claim", "payload": {"owner": "alpha-laptop"}})["task"]["task_id"], task["task_id"])
        with self.assertRaisesRegex(ArenaError, "lease"):
            handle_request(self.arena, bot, {"operation": "resume"})
        config = self.owner_configs[bot]
        Path(config["attempts"]).mkdir()
        attempt = make_attempt(config, task)
        (attempt / "bots/alpha/src/main.cpp").write_text("manual synthetic candidate")
        atomic_json(attempt / ".agent" / f"final-{task['task_id']}.json", self.final_result(bot, task))
        with patch("arena.worker.request", self.request):
            publication = publish_attempt(config, attempt, owner="alpha-laptop")
        self.request(config, "worker-finished", publication)
        self.request(config, "release", {"owner": "alpha-laptop"})
        self.assertIsNone(self.arena.db.one("SELECT lease_owner FROM workers WHERE id='alpha'")["lease_owner"])
        self.assertEqual(self.arena.db.get(f"task-origin:{task['task_id']}"), "manual")
