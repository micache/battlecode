from __future__ import annotations

import json
import os
from pathlib import Path
import random
import shutil
import time

from .common import (ArenaError, atomic_json, file_hash, fresh_id, identity, lock, read_json,
                     require, tree_hash, validate_schema)
from .db import Database
from .engine import OfficialEngine, PROFILE, seal_artifacts, verify_artifacts
from .evaluate import export_feedback, summarize
from .gitstore import ingest, poll


TERMINAL = ("COMPLETED", "BOT_FAULT", "INFRA_ERROR", "TIMEOUT", "TRUNCATED", "CANCELLED")


class Arena:
    def __init__(self, config, engine=None):
        self.config = config
        self.root = Path(config["root"])
        self.db = Database(self.root / "state/arena.sqlite")
        self.db.initialize(config)
        self.engine = engine
        for name in ("matches", "evaluations", "feedback", "inbox", "outbox", "tasks", "backups", "public", "control"):
            (self.root / name).mkdir(parents=True, exist_ok=True)

    def adapter(self):
        if self.engine is None:
            self.engine = OfficialEngine(self.config)
        return self.engine

    def freeze_maps(self):
        manifest = read_json(self.config["map_manifest"])
        maps = {}
        for item in manifest["maps"]:
            path = Path(self.config["maps"]) / (item["name"] + ".map26a")
            require(file_hash(path) == item["sha256"], f"map hash mismatch: {item['name']}")
            maps[item["name"]] = {"name": item["name"], "hash": item["sha256"], "path": str(path)}
        require(set(maps) == set(self.config["evaluation"]["development_maps"] +
                                self.config["evaluation"]["holdout_maps"]), "map pool mismatch")
        return maps

    def build(self, revision_id):
        revision = self.db.one("SELECT * FROM revisions WHERE id=?", (revision_id,))
        require(revision, "unknown revision")
        require(tree_hash(Path(revision["snapshot"]) / "src") == revision["source_hash"], "source hash changed")
        build = self.adapter().prepare_bot(revision["snapshot"], revision_id)
        self.db.execute("INSERT OR IGNORE INTO builds VALUES(?,?,?,?,?,?,?,?)",
                        (build["build_id"], revision_id, revision["source_hash"], build["lock_hash"],
                         "VALID", build["artifact"], build["wasm_sha256"], json.dumps(build)))
        return build

    def queue_match(self, a, b, map_info, repetition=None):
        spec = {"a_build": a["build_id"], "b_build": b["build_id"],
                "a_snapshot": a["snapshot"], "b_snapshot": b["snapshot"],
                "a_source_hash": a["source_hash"], "b_source_hash": b["source_hash"],
                "map_name": map_info["name"], "map_hash": map_info["hash"], "map_path": map_info["path"],
                "engine_lock_hash": self.adapter().lock_hash, "seed": None,
                "round_override": None, "fuel_override": None,
                "settings_hash": identity(self.adapter().lock.get("effective_profile")),
                "verification_repetition": repetition}
        # Host paths are not semantic input identities.
        job_id = identity({k: v for k, v in spec.items() if not k.endswith("snapshot") and k != "map_path"})
        spec["job_id"] = job_id
        self.db.execute("INSERT OR IGNORE INTO match_jobs(id,spec,state,created) VALUES(?,?,'QUEUED',?)",
                        (job_id, json.dumps(spec), time.time()))
        return job_id

    def run_one_match(self, job_id=None):
        if self.db.get("adapter_paused", False):
            return False
        job = (self.db.one("SELECT * FROM match_jobs WHERE state='QUEUED' AND id=?", (job_id,)) if job_id else
               self.db.one("SELECT * FROM match_jobs WHERE state='QUEUED' ORDER BY created LIMIT 1"))
        if not job:
            return False
        number = job["attempt_count"] + 1
        base = self.root / "matches" / job["id"]
        base.mkdir(parents=True, exist_ok=True)
        temporary = base / f".attempt-{number}"
        final = base / str(number)
        require(not temporary.exists() and not final.exists(), "attempt already exists; reconcile first")
        with self.db.transaction():
            self.db.execute("UPDATE match_jobs SET state='RUNNING',attempt_count=? WHERE id=?", (number, job["id"]))
            self.db.execute("INSERT INTO match_attempts VALUES(?,?,'RUNNING',?,?,NULL)",
                            (job["id"], number, str(final), time.time()))
        temporary.mkdir()
        atomic_json(temporary / "spec.json", json.loads(job["spec"]))
        try:
            result = self.adapter().run_match(json.loads(job["spec"]), temporary)
        except (ArenaError, OSError, ValueError) as exc:
            result = {"protocol_version": 1, "state": "INFRA_ERROR", "completed": False, "winner": None,
                      "bot_faults": None, "fuel_suspensions": None, "metrics": {}, "terminal_reason": None,
                      "detail": str(exc)}
        seal_artifacts(temporary, job["id"], number, result)
        temporary.rename(final)
        self.finish_match(job["id"], number, final)
        return True

    def finish_match(self, job_id, number, directory):
        result = verify_artifacts(directory, job_id, number)
        require(result["state"] in TERMINAL, "invalid adapter state")
        parser_pending = result.get("detail") == "statistics parser has no reviewed real-engine fixture"
        retry = result["state"] in ("INFRA_ERROR", "TIMEOUT") and not parser_pending and number <= self.config["limits"]["infra_retries"]
        with self.db.transaction():
            self.db.execute("UPDATE match_attempts SET state=?,finished=? WHERE job_id=? AND number=?",
                            (result["state"], time.time(), job_id, number))
            self.db.execute("UPDATE match_jobs SET state=?,result=?,artifact=? WHERE id=?",
                            ("QUEUED" if retry else result["state"], json.dumps(result), str(directory), job_id))
            if result["state"] in ("INFRA_ERROR", "TIMEOUT") and not retry:
                self.db.put("adapter_paused", {"job": job_id, "detail": result.get("detail"), "attempt": number})

    def recover(self):
        # Called under the global service lock after systemd has killed the old cgroup.
        self.adapter().recover_containers()
        for job in self.db.all("SELECT * FROM match_jobs WHERE state='RUNNING'"):
            number = job["attempt_count"]
            base = self.root / "matches" / job["id"]
            final, temp = base / str(number), base / f".attempt-{number}"
            if not final.exists() and (temp / "completion.json").exists():
                verify_artifacts(temp, job["id"], number)
                temp.rename(final)
            if (final / "completion.json").exists():
                self.finish_match(job["id"], number, final)
                continue
            result = {"protocol_version": 1, "state": "INFRA_ERROR", "completed": False, "winner": None,
                      "bot_faults": None, "fuel_suspensions": None, "metrics": {}, "terminal_reason": None,
                      "detail": "interrupted service attempt; preserved, no outcome scored"}
            temp.mkdir(exist_ok=True)
            seal_artifacts(temp, job["id"], number, result)
            temp.rename(final)
            self.finish_match(job["id"], number, final)
        # Re-export idempotently if a crash separated commit from feedback publication.
        for evaluation in self.db.all("SELECT * FROM evaluations WHERE finished IS NOT NULL AND metrics IS NOT NULL"):
            export_feedback(self.db, self.config, evaluation)
        self.db.put("recovered_at", time.time())

    def start_evaluation(self, revision_id):
        revision = self.db.one("SELECT * FROM revisions WHERE id=?", (revision_id,))
        require(revision and revision["state"] == "PENDING", "revision not pending")
        bot = self.db.one("SELECT * FROM bots WHERE id=?", (revision["bot_id"],))
        require(not self.db.one("SELECT id FROM evaluations WHERE bot_id=? AND state='EVALUATING'", (bot["id"],)),
                "one evaluation per bot")
        try:
            candidate = self.build(revision_id)
            incumbent = self.build(bot["accepted_revision"]) if bot["accepted_revision"] else None
            # Configured immutable history plus a pinned starter; never a moving opponent branch.
            opponent_ids = list(dict.fromkeys([self.db.get("starter_revision")] + self.config["evaluation"]["opponent_revision_ids"]))
            require(opponent_ids and all(opponent_ids), "pinned starter opponent missing")
            opponents = {rid: self.build(rid) for rid in opponent_ids}
        except ArenaError as exc:
            suite = {"engine_lock_hash": self.adapter().lock_hash, "opponents": {}, "maps": {},
                     "coverage": "provisional-three-map-wiring", "gate": self.config["evaluation"]}
            evaluation_id = identity({"revision": revision_id, "build_failure": str(exc), "suite": suite})
            self.db.execute("INSERT OR IGNORE INTO evaluations VALUES(?,?,?,?,?,?,'EVALUATING','smoke',NULL,?,NULL)",
                            (evaluation_id, bot["id"], revision_id, bot["accepted_revision"], identity(suite),
                             json.dumps(suite), time.time()))
            evaluation = self.db.one("SELECT * FROM evaluations WHERE id=?", (evaluation_id,))
            metrics = summarize([], self.config["evaluation"], [], False)
            metrics.update(build_error=str(exc), missing=["build: no games ran"])
            self.finish_evaluation(evaluation, metrics, "BUILD_FAILED")
            return evaluation_id
        maps = self.freeze_maps()
        full = self.config["evaluation"]["automatic_promotion"]
        if full:
            count = self.db.one("SELECT count(*) AS n FROM evaluations WHERE bot_id=? AND stage='promotion' AND created>?",
                                (bot["id"], time.time() - 86400))["n"]
            require(count < 2, "daily promotion-check cap reached")
        suite = {"protocol_version": 1, "version": self.config["evaluation"]["suite_version"],
                 "engine_lock_hash": self.adapter().lock_hash, "maps": maps,
                 "opponents": {rid: {"build_id": build["build_id"], "source_hash": build["source_hash"],
                                      "commit": self.db.one("SELECT commit_sha FROM revisions WHERE id=?", (rid,))["commit_sha"]}
                               for rid, build in opponents.items()},
                 "coverage": "full-nine-map" if full else "provisional-three-map-wiring",
                 "candidate_build": candidate["build_id"], "incumbent_build": incumbent["build_id"] if incumbent else None,
                 "gate": self.config["evaluation"], "config_hash": self.config["config_hash"]}
        suite["effective_profile"] = self.adapter().lock.get("effective_profile")
        suite["infrastructure_commit"] = self.config["infrastructure_commit"]
        evaluation_id = identity({"revision": revision_id, "suite": suite})
        with self.db.transaction():
            self.db.execute("INSERT OR IGNORE INTO evaluations VALUES(?,?,?,?,?,?,'EVALUATING','smoke',NULL,?,NULL)",
                            (evaluation_id, bot["id"], revision_id, bot["accepted_revision"], identity(suite),
                             json.dumps(suite), time.time()))
            self.db.execute("UPDATE revisions SET state='EVALUATING' WHERE id=?", (revision_id,))
        directory = self.root / "evaluations" / evaluation_id
        atomic_json(directory / "suite.json", suite)
        self.add_cases(evaluation_id, candidate, incumbent, opponents, maps, [self.config["evaluation"]["screen_maps"][0]], "smoke")
        return evaluation_id

    def add_cases(self, evaluation_id, candidate, incumbent, opponents, maps, names, stage):
        with self.db.transaction():
            for name in names:
                for rid, opponent in opponents.items():
                    for role, build in (("candidate", candidate), ("incumbent", incumbent)):
                        if not build:
                            continue
                        for side in ("A", "B"):
                            a, b = (build, opponent) if side == "A" else (opponent, build)
                            job_id = self.queue_match(a, b, maps[name])
                            self.db.execute("INSERT OR IGNORE INTO evaluation_cases VALUES(?,?,?,?,?,?,?)",
                                            (evaluation_id, job_id, side, role, name, rid, stage))

    def evaluation_cases(self, evaluation_id):
        cases = self.db.all("SELECT c.*,j.result,j.artifact,j.state FROM evaluation_cases c "
                            "JOIN match_jobs j ON j.id=c.job_id WHERE c.evaluation_id=?", (evaluation_id,))
        for case in cases:
            case["result"] = json.loads(case["result"]) if case["result"] else None
        return cases

    def advance_evaluations(self):
        for evaluation in self.db.all("SELECT * FROM evaluations WHERE state='EVALUATING'"):
            cases = self.evaluation_cases(evaluation["id"])
            suite = json.loads(evaluation["suite"])
            if suite["engine_lock_hash"] != self.adapter().lock_hash:
                for case in cases:
                    self.db.execute("UPDATE match_jobs SET state='CANCELLED' WHERE id=? AND state='QUEUED'", (case["job_id"],))
                metrics = summarize(cases, suite["gate"], self.config["evaluation"]["holdout_maps"], False)
                metrics["version_change"] = "engine lock changed; old cases retained and evaluation not promoted"
                self.finish_evaluation(evaluation, metrics, "INCONCLUSIVE")
                continue
            if any(case["state"] in ("QUEUED", "RUNNING") for case in cases):
                continue
            metrics = summarize(cases, suite["gate"], self.config["evaluation"]["holdout_maps"], False)
            if metrics["missing"] or metrics["fault_matches"]:
                self.finish_evaluation(evaluation, metrics, "REJECTED" if metrics["fault_matches"] else "INCONCLUSIVE")
                continue
            stage = evaluation["stage"]
            full = suite["coverage"] == "full-nine-map"
            if stage == "smoke" or (stage == "screen" and full):
                next_stage = "screen" if stage == "smoke" else "promotion"
                names = self.config["evaluation"]["screen_maps"] if next_stage == "screen" else list(suite["maps"])
                candidate = self.build(evaluation["revision_id"])
                incumbent = self.build(evaluation["incumbent_id"]) if evaluation["incumbent_id"] else None
                opponents = {rid: self.build(rid) for rid in suite["opponents"]}
                self.add_cases(evaluation["id"], candidate, incumbent, opponents, suite["maps"], names, next_stage)
                if next_stage == "promotion" and incumbent:
                    # Head-to-head is reliability/diagnostic evidence, not common-opponent score.
                    self.add_head_to_head(evaluation, candidate, incumbent, suite["maps"])
                self.db.execute("UPDATE evaluations SET stage=? WHERE id=?", (next_stage, evaluation["id"]))
                continue
            if not evaluation["incumbent_id"]:
                # A provisional baseline needs validity, not an improvement over nothing.
                state = "ACCEPTED" if not metrics["unknown_reliability"] else "INCONCLUSIVE"
            else:
                metrics = summarize(cases, suite["gate"], self.config["evaluation"]["holdout_maps"], full)
                state = metrics["decision"] if full else "INCONCLUSIVE"
            self.finish_evaluation(evaluation, metrics, state)

    def add_head_to_head(self, evaluation, candidate, incumbent, maps):
        with self.db.transaction():
            for name, item in maps.items():
                for side in ("A", "B"):
                    a, b = (candidate, incumbent) if side == "A" else (incumbent, candidate)
                    job_id = self.queue_match(a, b, item)
                    self.db.execute("INSERT OR IGNORE INTO evaluation_cases VALUES(?,?,?,?,?,?,?)",
                                    (evaluation["id"], job_id, side, "head-to-head", name,
                                     evaluation["incumbent_id"], "promotion"))

    def finish_evaluation(self, evaluation, metrics, state):
        suite = json.loads(evaluation["suite"])
        if state == "ACCEPTED" and evaluation["incumbent_id"]:
            readiness = self.db.get("readiness", {})
            expected_case_count = 9 * 2 * len(suite["opponents"])
            if not (readiness.get("private_arena_ready") and readiness.get("competition_parity_verified")
                    and readiness.get("engine_lock_hash") == suite["engine_lock_hash"]
                    and suite["engine_lock_hash"] == self.adapter().lock_hash
                    and suite.get("infrastructure_commit") == self.config["infrastructure_commit"]
                    and suite["coverage"] == "full-nine-map" and len(suite["opponents"]) >= 3
                    and metrics["paired_cases"] == expected_case_count // 2
                    and len({o["source_hash"] for o in suite["opponents"].values()}) >= 3):
                state = "INCONCLUSIVE"
                metrics["promotion_blocker"] = "full validated gate needs readiness and three distinct fixed opponents"
        metrics["decision"] = state
        with self.db.transaction():
            if state == "ACCEPTED":
                revision = self.db.one("SELECT * FROM revisions WHERE id=?", (evaluation["revision_id"],))
                update = self.db.execute("UPDATE bots SET accepted_revision=?,accepted_source_hash=? "
                                         "WHERE id=? AND accepted_revision IS ?",
                                         (revision["id"], revision["source_hash"], evaluation["bot_id"], evaluation["incumbent_id"]))
                if update.rowcount != 1:
                    state = "INCONCLUSIVE"
                    metrics["decision"] = state
                    metrics["promotion_blocker"] = "incumbent compare-and-swap conflict"
            self.db.execute("UPDATE evaluations SET state=?,metrics=?,finished=? WHERE id=?",
                            (state, json.dumps(metrics), time.time(), evaluation["id"]))
            self.db.execute("UPDATE revisions SET state=? WHERE id=?", (state, evaluation["revision_id"]))
            self.db.execute("UPDATE workers SET state=CASE WHEN paused THEN 'PAUSED' ELSE 'IDLE' END "
                            "WHERE id=? AND state='WAITING_EVALUATION'", (evaluation["bot_id"],))
        export_feedback(self.db, self.config, self.db.one("SELECT * FROM evaluations WHERE id=?", (evaluation["id"],)))

    def status(self):
        feedback_ages = {}
        for bot in self.config["workers"]:
            latest = self.root / "feedback" / bot / "latest.json"
            feedback_ages[bot] = (time.time() - read_json(latest)["summary"]["created"]) if latest.exists() else None
        return {"protocol_version": 1, "timestamp": time.time(),
                "paused": self.db.get("paused", True), "adapter_paused": self.db.get("adapter_paused", False),
                "readiness": self.db.get("readiness", {}), "workers": self.db.all("SELECT * FROM workers"),
                "bots": self.db.all("SELECT * FROM bots"),
                "matches": self.db.all("SELECT state,count(*) AS count FROM match_jobs GROUP BY state"),
                "evaluations": self.db.all("SELECT id,bot_id,revision_id,state,stage FROM evaluations ORDER BY created DESC LIMIT 10"),
                "disk": {"free": shutil.disk_usage(self.root).free,
                         "artifact_bytes": sum(p.stat().st_size for p in (self.root / "matches").rglob("*") if p.is_file())},
                "heartbeat": self.db.get("heartbeat"), "feedback_age_seconds": feedback_ages,
                "service_error": self.db.get("service_error"), "disk_pressure": self.db.get("disk_pressure", False),
                "official_enabled": False}

    def export_status(self):
        status = self.status()
        atomic_json(self.root / "public/status.json", status, 0o644)
        from .operations import acceptance_report
        acceptance_report(self)
        return status

    def step(self):
        from .supervisor import consume_messages, dispatch_tasks
        self.consume_control()
        consume_messages(self)
        self.db.put("heartbeat", time.time())
        status = self.export_status()
        pressure = (status["disk"]["free"] < self.config["limits"]["minimum_free_bytes"] or
                    status["disk"]["artifact_bytes"] >= self.config["limits"]["artifact_budget_bytes"])
        self.db.put("disk_pressure", pressure)
        if self.db.get("paused", True) or pressure:
            return
        self.advance_evaluations()
        for bot in self.config["workers"]:
            state = self.db.one("SELECT * FROM bots WHERE id=?", (bot,))
            if time.time() >= state["next_poll"] and self.db.get("starter_verified", False):
                try:
                    poll(self.db, self.config, bot)
                    self.db.execute("UPDATE bots SET last_poll=?,poll_failures=0,next_poll=? WHERE id=?",
                                    (time.time(), time.time() + 60 + random.uniform(0, 6), bot))
                except ArenaError as exc:
                    failures = state["poll_failures"] + 1
                    self.db.execute("UPDATE bots SET poll_failures=?,next_poll=? WHERE id=?",
                                    (failures, time.time() + min(3600, 60 * 2 ** min(failures, 6)), bot))
                    self.db.put(f"git_error:{bot}", str(exc))
            pending = self.db.one("SELECT id FROM revisions WHERE bot_id=? AND state='PENDING' ORDER BY created DESC LIMIT 1", (bot,))
            if pending and not self.db.one("SELECT id FROM evaluations WHERE bot_id=? AND state='EVALUATING'", (bot,)):
                self.start_evaluation(pending["id"])
        self.run_one_match()
        self.advance_evaluations()
        dispatch_tasks(self)

    def consume_control(self):
        for path in sorted((self.root / "control").glob("request-*.json")):
            message = read_json(path)
            operation = message["operation"]
            if operation in ("start", "pause"):
                self.db.put("paused", operation == "pause")
            elif operation == "adapter-resume":
                self.db.put("adapter_paused", False)
            elif operation == "backup":
                from .operations import backup
                backup(self)
            elif operation == "compact":
                from .operations import compact
                compact(self)
            else:
                raise ArenaError("invalid operator command")
            path.rename(path.with_suffix(".done"))
        # A timed-out/missing worker is parked, never reassigned to another owner.
        for worker in self.db.all("SELECT * FROM workers WHERE state='RUNNING'"):
            task = self.db.one("SELECT * FROM tasks WHERE id=?", (worker["task_id"],))
            if task and time.time() - task["created"] > 2700:
                with self.db.transaction():
                    self.db.execute("UPDATE tasks SET state='INTERRUPTED' WHERE id=?", (task["id"],))
                    self.db.execute("UPDATE workers SET state='PAUSED',paused=1,detail=? WHERE id=?",
                                    ("worker delivery deadline exceeded; preserve and reconcile attempt", worker["id"]))

    def serve(self):
        with lock(self.root / "state/service.lock"):
            self.recover()
            while True:
                try:
                    self.step()
                    self.db.put("service_error", None)
                except (ArenaError, OSError) as exc:
                    self.db.put("service_error", str(exc))
                    self.export_status()
                time.sleep(2)
