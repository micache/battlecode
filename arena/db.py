import contextlib
import json
from pathlib import Path
import sqlite3
import time

from .common import atomic_json, read_json, require


DDL = """
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS bots(
 id TEXT PRIMARY KEY, branch TEXT UNIQUE NOT NULL, accepted_revision TEXT,
 accepted_source_hash TEXT, latest_tip TEXT, last_poll REAL, poll_failures INTEGER DEFAULT 0,
 next_poll REAL DEFAULT 0);
CREATE TABLE IF NOT EXISTS revisions(
 id TEXT PRIMARY KEY, bot_id TEXT NOT NULL REFERENCES bots(id), commit_sha TEXT NOT NULL,
 source_hash TEXT NOT NULL, base_source_hash TEXT, experiment_id TEXT,
 snapshot TEXT NOT NULL, infrastructure_commit TEXT NOT NULL, state TEXT NOT NULL,
 created REAL NOT NULL, UNIQUE(bot_id,commit_sha));
CREATE TABLE IF NOT EXISTS builds(
 id TEXT PRIMARY KEY, revision_id TEXT NOT NULL REFERENCES revisions(id), source_hash TEXT NOT NULL,
 lock_hash TEXT NOT NULL, state TEXT NOT NULL, artifact TEXT, artifact_hash TEXT, detail TEXT);
CREATE TABLE IF NOT EXISTS evaluations(
 id TEXT PRIMARY KEY, bot_id TEXT NOT NULL REFERENCES bots(id), revision_id TEXT NOT NULL REFERENCES revisions(id),
 incumbent_id TEXT, suite_hash TEXT NOT NULL, suite TEXT NOT NULL, state TEXT NOT NULL,
 stage TEXT NOT NULL, metrics TEXT, created REAL NOT NULL, finished REAL,
 UNIQUE(revision_id,suite_hash));
CREATE TABLE IF NOT EXISTS match_jobs(
 id TEXT PRIMARY KEY, spec TEXT NOT NULL, state TEXT NOT NULL, attempt_count INTEGER DEFAULT 0,
 result TEXT, artifact TEXT, created REAL NOT NULL);
CREATE TABLE IF NOT EXISTS evaluation_cases(
 evaluation_id TEXT NOT NULL REFERENCES evaluations(id), job_id TEXT NOT NULL REFERENCES match_jobs(id),
 candidate_side TEXT NOT NULL, role TEXT NOT NULL, map_name TEXT NOT NULL, opponent TEXT NOT NULL,
 stage TEXT NOT NULL, PRIMARY KEY(evaluation_id,role,map_name,opponent,candidate_side));
CREATE TABLE IF NOT EXISTS match_attempts(
 job_id TEXT NOT NULL REFERENCES match_jobs(id), number INTEGER NOT NULL, state TEXT NOT NULL,
 artifact TEXT NOT NULL, started REAL NOT NULL, finished REAL, PRIMARY KEY(job_id,number));
CREATE TABLE IF NOT EXISTS workers(
 id TEXT PRIMARY KEY REFERENCES bots(id), state TEXT NOT NULL, paused INTEGER DEFAULT 1,
 task_id TEXT, lease_owner TEXT, heartbeat REAL, next_run REAL DEFAULT 0,
 quota_count INTEGER DEFAULT 0, last_feedback TEXT, detail TEXT);
CREATE TABLE IF NOT EXISTS tasks(
 id TEXT PRIMARY KEY, bot_id TEXT NOT NULL REFERENCES bots(id), envelope TEXT NOT NULL,
 state TEXT NOT NULL, created REAL NOT NULL, result TEXT, published_commit TEXT);
CREATE TABLE IF NOT EXISTS requests(
 id TEXT PRIMARY KEY, bot_id TEXT NOT NULL, operation TEXT NOT NULL, state TEXT NOT NULL, response TEXT);
CREATE TABLE IF NOT EXISTS external_matches(
 official_id TEXT PRIMARY KEY, metadata TEXT NOT NULL, artifact TEXT NOT NULL, created REAL NOT NULL);
CREATE TABLE IF NOT EXISTS training_rounds(
 id TEXT PRIMARY KEY, spec TEXT NOT NULL, state TEXT NOT NULL, created REAL NOT NULL, finished REAL);
CREATE TABLE IF NOT EXISTS training_cases(
 job_id TEXT PRIMARY KEY REFERENCES match_jobs(id), round_id TEXT NOT NULL REFERENCES training_rounds(id),
 a_bot TEXT NOT NULL REFERENCES bots(id), b_bot TEXT NOT NULL REFERENCES bots(id),
 a_revision TEXT NOT NULL REFERENCES revisions(id), b_revision TEXT NOT NULL REFERENCES revisions(id),
 map_name TEXT NOT NULL, input_identity TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS training_round_cases ON training_cases(round_id);
CREATE INDEX IF NOT EXISTS job_queue ON match_jobs(state,created);
CREATE INDEX IF NOT EXISTS revision_queue ON revisions(bot_id,state,created);
CREATE TABLE IF NOT EXISTS artifact_retirements(
 job_id TEXT PRIMARY KEY REFERENCES match_jobs(id), record TEXT NOT NULL, state TEXT NOT NULL);
"""


class Database:
    def __init__(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.connection = sqlite3.connect(path, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA busy_timeout=5000")
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.executescript(DDL)

    def execute(self, sql, values=()):
        return self.connection.execute(sql, values)

    def one(self, sql, values=()):
        row = self.execute(sql, values).fetchone()
        return dict(row) if row else None

    def all(self, sql, values=()):
        return [dict(row) for row in self.execute(sql, values).fetchall()]

    @contextlib.contextmanager
    def transaction(self):
        self.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.execute("COMMIT")
        except BaseException:
            self.execute("ROLLBACK")
            raise

    def get(self, key, default=None):
        row = self.one("SELECT value FROM meta WHERE key=?", (key,))
        return json.loads(row["value"]) if row else default

    def put(self, key, value):
        self.execute("INSERT INTO meta VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                     (key, json.dumps(value)))

    def initialize(self, config):
        for bot, worker in config["workers"].items():
            self.execute("INSERT OR IGNORE INTO bots(id,branch) VALUES(?,?)", (bot, worker["branch"]))
            self.execute("INSERT OR IGNORE INTO workers(id,state) VALUES(?,'PAUSED')", (bot,))
        self.put("official_enabled", False)

    def backup(self, destination):
        destination = Path(destination)
        require(not destination.exists(), "backup destination already exists")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with contextlib.closing(sqlite3.connect(destination)) as target:
            self.connection.backup(target)
            require(target.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "backup integrity")
        return str(destination)
