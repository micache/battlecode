import base64
import contextlib
import json
from pathlib import Path
import re
import shutil
import sqlite3
import time

from .common import (ArenaError, atomic_json, file_hash, identity, read_json, require, run,
                     tree_hash, tree_manifest)
from .engine import PROFILE, normalize_result
from .protocol import save_source


def register_toolchain(config, image_id, template, compiler_record, profile_record=None):
    require(isinstance(image_id, str) and re.fullmatch(r'(sha256:)?[a-f0-9]{64}', image_id), 'immutable image ID required')
    image_id = 'sha256:' + image_id.removeprefix('sha256:')
    inspected = run(["podman", "image", "inspect", "--format", "{{.Id}}", image_id])
    require('sha256:' + inspected.removeprefix('sha256:') == image_id,
            "image must already be installed at immutable ID")
    version = run(["podman", "run", "--rm", "--pull=never", "--network=none", image_id, "cambc", "--version"])
    require(version == "cambc " + config['engine']['version'], "engine version mismatch")
    binary_hash = run(["podman", "run", "--rm", "--pull=never", "--network=none", image_id,
                       "python3", "/opt/engine-evidence.py", "binary-hash"])
    require(binary_hash == config["engine"]["binary_sha256"], "distributed engine hash mismatch")
    require(Path(template).is_dir(), "export official /opt/project template first")
    # The template comes from a trusted image; it includes the official build recipes, never a bot branch's scripts.
    manifest = tree_manifest(template)
    require("sdk/cpp/cambc.h" in manifest, "matching installed C++ SDK missing")
    lock = {"protocol_version": 1, "version": config['engine']['version'], "engine_sha256": binary_hash,
            "image_id": image_id, "project_template": str(Path(template).resolve()),
            "template_sha256": tree_hash(template), "sdk_cpp_sha256": file_hash(Path(template) / "sdk/cpp/cambc.h"),
            "compiler_versions": compiler_record, "language": "cpp", "effective_profile": None,
            "recipe_sha256": file_hash(Path(config["infrastructure"]) / "ops/Containerfile"),
            "created": time.time()}
    if config['engine']['version'] == '2.2.5':
        lock['build_mode'] = 'release'
    if profile_record:
        profile = profile_record['effective_profile']
        expected = dict(PROFILE, fuel_multipliers={'cpp': 1})
        require(profile in (PROFILE, expected), "runtime profile differs; review rules update")
        evidence = profile_record["evidence"]
        require(file_hash(evidence["path"]) == evidence["sha256"], "runtime profile evidence missing/changed")
        lock["effective_profile"] = profile_record["effective_profile"]
        lock["profile_evidence"] = evidence
    atomic_json(config["engine_lock"], lock)
    return lock


def starter_snapshot(arena):
    # An upgrade must not silently reuse a prior CLI's starter implementation.
    if arena.adapter().lock.get('version') == '2.2.5':
        return arena.root / 'starters' / arena.adapter().lock_hash
    return arena.root / 'starter'


def starter_check(arena, normalize_only=False):
    from .engine import seal_artifacts
    root, db = arena.root, arena.db
    engine = arena.adapter()
    snapshot = starter_snapshot(arena)
    if not snapshot.exists():
        shutil.copytree(Path(engine.lock["project_template"]) / "bots/side-a/src", snapshot / "src")
    build = engine.prepare_bot(snapshot, "official-starter")
    map_info = arena.freeze_maps()[arena.config["evaluation"]["screen_maps"][0]]
    require(not normalize_only or engine.lock.get('version') != '2.2.5',
            'run fresh reviewed starter games; do not relabel initial unreviewed attempts')
    parser_revision = ':' + identity(engine.contract) if engine.lock.get('version') == '2.2.5' else ''
    jobs = [arena.queue_match(build, build, map_info, repetition=f"starter-side-{side}{parser_revision}")
            for side in ("A", "B")]
    # Two acceptance runs are explicitly recorded as deterministic repetitions, not independent samples.
    if normalize_only:
        for job_id in jobs:
            job = db.one("SELECT * FROM match_jobs WHERE id=?", (job_id,))
            require(job["artifact"], "starter run artifacts missing")
            old = Path(job["artifact"])
            result = normalize_result(old / "artifacts", engine.contract, engine.lock["engine_sha256"])
            # Review creates a new normalization record; raw engine evidence is unchanged.
            atomic_json(root / "acceptance" / f"reviewed-{job_id}-{job['attempt_count']}.json", result)
            db.execute("UPDATE match_jobs SET state=?,result=? WHERE id=?", (result["state"], json.dumps(result), job_id))
    else:
        # A parser review can be pending during these first real source-project runs.
        for job_id in jobs:
            if db.one("SELECT state FROM match_jobs WHERE id=?", (job_id,))["state"] == "QUEUED":
                was_paused = db.get("adapter_paused", False)
                db.put("adapter_paused", False)
                arena.run_one_match(job_id)
                if was_paused:
                    db.put("adapter_paused", was_paused)
    results = [db.one("SELECT * FROM match_jobs WHERE id=?", (job,)) for job in jobs]
    verified = all(row["result"] and json.loads(row["result"])["state"] == "COMPLETED" and
                   json.loads(row["result"]).get("bot_faults") == 0 for row in results)
    db.put("starter_verified", verified)
    db.put('starter_engine_lock_hash', engine.lock_hash if verified else None)
    if verified:
        db.put("adapter_paused", False)
    report = {"verified": verified, 'engine_lock_hash': engine.lock_hash,
              'starter_snapshot': str(snapshot), "matches": [{"match_id": row["id"], "artifact": row["artifact"],
               "state": row["state"]} for row in results], "independent_samples": False,
              "parser_review_required": not bool(engine.contract)}
    atomic_json(root / "acceptance/starter-check.json", report)
    return report


def register_starter(arena, revision_id):
    require(arena.db.get("starter_verified", False), "complete starter games must be verified first")
    row = arena.db.one("SELECT * FROM revisions WHERE id=?", (revision_id,))
    require(row, "starter revision must be a real ingested commit")
    expected = tree_hash(starter_snapshot(arena) / 'src')
    require(row["source_hash"] == expected, "baseline differs from pinned official starter")
    arena.db.put("starter_revision", revision_id)
    return row


def ensure_starter_reference(arena):
    """Preserve starter independently of both lanes, including when existing bots are supplied."""
    require(arena.db.get("starter_verified", False), "starter games must be verified first")
    snapshot = starter_snapshot(arena)
    previous = arena.db.get('starter_revision')
    if previous:
        row = arena.db.one('SELECT source_hash FROM revisions WHERE id=?', (previous,))
        if row['source_hash'] == tree_hash(snapshot / 'src'):
            return previous
    from .gitstore import git
    directory = arena.root / 'repos' / ('official-starter-reference-' + tree_hash(snapshot / 'src')[:16])
    require(not directory.exists(), "interrupted starter reference exists; preserve/reconcile before retry")
    directory.mkdir(parents=True)
    git(directory, "init", "-b", "reference/official-starter")
    shutil.copytree(snapshot / 'src', directory / "bots/starter/src")
    git(directory, "add", "--", "bots/starter/src")
    git(directory, "-c", "user.name=Battlecode starter reference", "-c", "user.email=arena@localhost",
        "commit", "-m", "Pinned official C++ starter reference")
    commit = git(directory, "rev-parse", "HEAD")
    source_hash = tree_hash(snapshot / 'src')
    for path in [snapshot / 'src', *(snapshot / 'src').rglob('*')]:
        path.chmod(0o550 if path.is_dir() else 0o440)
    revision_id = identity({"repository": str(directory), "commit": commit, "source_hash": source_hash})
    with arena.db.transaction():
        arena.db.execute("INSERT INTO bots(id,branch,latest_tip) VALUES('starter','reference/official-starter',?) "
                         "ON CONFLICT(id) DO UPDATE SET latest_tip=excluded.latest_tip", (commit,))
        arena.db.execute("INSERT INTO revisions VALUES(?,'starter',?,?,NULL,'official-starter',?,?,'ACCEPTED',?)",
                         (revision_id, commit, source_hash, str(snapshot),
                          arena.config["infrastructure_commit"], time.time()))
        arena.db.put("starter_revision", revision_id)
    return revision_id


def verify_readiness(arena, evidence_path):
    evidence = read_json(evidence_path)
    lock = arena.adapter().lock
    require(evidence.get("engine_lock_hash") == arena.adapter().lock_hash, "readiness identity mismatch")
    require(evidence.get("effective_profile") == PROFILE, "effective engine profile not verified")
    require(lock.get("effective_profile") == PROFILE, "register measured settings in engine lock first")
    needed = ("parser_replay_agreement", "complete_tie_team_b", "fuel_suspension", "channel_completion",
              "ranged_allowances", "capture_occupancy", "hidden_obstruction", "safe_approach_tiles",
              "credential_isolation", "network_isolation", "ssh_disconnect", "service_restart")
    require(all(evidence.get("checks", {}).get(key) for key in needed), "required real host/engine fixtures missing")
    for name, item in evidence["checks"].items():
        require(isinstance(item, dict) and Path(item["path"]).is_file() and file_hash(item["path"]) == item["sha256"],
                f"missing readiness artifact: {name}")
    require(arena.db.get("starter_verified", False), "starter checks pending")
    # Readiness is bound to this exact engine, map pool and infrastructure, not a blanket future assertion.
    report = {"private_arena_ready": True,
              "competition_parity_verified": bool(evidence.get("event_review_complete") and
                 evidence["checks"].get("organizer_agents") and evidence["checks"].get("event_policy_review")),
              "official_automation_verified": False, "engine_lock_hash": arena.adapter().lock_hash,
              "evidence_sha256": file_hash(evidence_path), "config_hash": arena.config["config_hash"]}
    arena.db.put("readiness", report)
    return report


def acceptance_report(arena):
    cycles = {}
    for bot in arena.config["workers"]:
        rows = arena.db.all("SELECT t.id AS task_id,t.published_commit,r.source_hash,e.id AS evaluation_id,e.state "
                            "FROM tasks t JOIN revisions r ON r.experiment_id=t.id JOIN evaluations e ON e.revision_id=r.id "
                            "WHERE t.bot_id=? AND t.state='PUBLISHED' AND e.finished IS NOT NULL ORDER BY e.created", (bot,))
        provider = arena.config['workers'][bot].get('provider', 'codex')
        rows = [row for row in rows if arena.db.get(f"task-origin:{row['task_id']}") == provider and
                arena.db.get(f"invocation:{row['task_id']}", {}).get("provider") == provider]
        for row in rows:
            row["matches"] = [case["job_id"] for case in arena.db.all(
                "SELECT DISTINCT c.job_id FROM evaluation_cases c JOIN match_jobs j ON j.id=c.job_id "
                "WHERE c.evaluation_id=? AND j.state='COMPLETED'", (row["evaluation_id"],))]
        cycles[bot] = rows
    readiness = arena.db.get("readiness", {})
    verified = (arena.db.get("starter_verified", False) and all(len(rows) >= 2 for rows in cycles.values())
                and readiness.get("private_arena_ready", False))
    report = {"protocol_version": 1, "verified": verified, "starter_games": arena.db.get("starter_verified", False),
              "cycles": cycles, "readiness": readiness, "official_enabled": False,
              "infrastructure_commit": arena.config["infrastructure_commit"], "created": time.time()}
    atomic_json(arena.root / "public/acceptance.json", report, 0o644)
    return report


def compact(arena, days=14):
    import gzip
    import os
    protected = set()
    for evaluation in arena.db.all("SELECT * FROM evaluations WHERE state='ACCEPTED' OR state='EVALUATING'"):
        protected.update(row["job_id"] for row in arena.db.all("SELECT job_id FROM evaluation_cases WHERE evaluation_id=?",
                                                              (evaluation["id"],)))
    for evaluation in arena.db.all("SELECT metrics FROM evaluations WHERE metrics IS NOT NULL"):
        protected.update(item["match_id"] for item in json.loads(evaluation["metrics"]).get("representative_failures", []))
    changed = []
    from .engine import seal_artifacts, verify_artifacts
    for job in arena.db.all("SELECT * FROM match_jobs WHERE state='COMPLETED' AND created<?", (time.time() - days * 86400,)):
        if job["id"] in protected or json.loads(job["spec"]).get("verification_repetition"):
            continue
        directory = Path(job["artifact"])
        if directory.name.endswith("-compressed"):
            continue
        result = verify_artifacts(directory, job["id"], job["attempt_count"])
        require(directory.resolve().parent == (arena.root / "matches" / job["id"]).resolve(), "unexpected artifact path")
        size = sum(path.stat().st_size for path in directory.rglob("*") if path.is_file())
        require(shutil.disk_usage(arena.root).free > size + arena.config["limits"]["minimum_free_bytes"], "compression needs free staging space")
        final = directory.with_name(directory.name + "-compressed")
        stage = directory.with_name(".compress-" + directory.name)
        require(not stage.exists(), "interrupted compression retained; inspect staging copy")
        require(not final.exists(), "completed compression retained; reconcile database pointer")
        shutil.copytree(directory, stage)
        for replay in stage.rglob("*.repl26a"):
            compressed = replay.with_suffix(replay.suffix + ".gz")
            temporary = compressed.with_suffix(compressed.suffix + ".pending")
            with replay.open("rb") as source, gzip.open(temporary, "wb") as target:
                shutil.copyfileobj(source, target)
            with gzip.open(temporary, "rb") as restored, replay.open("rb") as original:
                import hashlib
                a, b = hashlib.sha256(), hashlib.sha256()
                for data in iter(lambda: restored.read(1024 * 1024), b""):
                    a.update(data)
                for data in iter(lambda: original.read(1024 * 1024), b""):
                    b.update(data)
                require(a.digest() == b.digest(), "replay compression verification failed")
            os.replace(temporary, compressed)
            replay.unlink()
            changed.append(str(final / compressed.relative_to(stage)))
        seal_artifacts(stage, job["id"], job["attempt_count"], result)
        stage.rename(final)
        verify_artifacts(final, job["id"], job["attempt_count"])
        with arena.db.transaction():
            arena.db.execute("UPDATE match_jobs SET artifact=? WHERE id=?", (str(final), job["id"]))
            arena.db.execute("UPDATE match_attempts SET artifact=? WHERE job_id=? AND number=?",
                             (str(final), job["id"], job["attempt_count"]))
        archive_record = final / 'project-archive.json'
        if archive_record.exists():
            previous = read_json(archive_record)['previous_directory']
            require(previous == Path(previous).name, 'unsafe legacy artifact alias')
            alias = directory.parent / previous
            if alias.is_symlink():
                require(alias.resolve() == directory.resolve(), 'legacy artifact alias changed')
                pending_alias = alias.with_name('.alias-' + alias.name)
                require(not pending_alias.exists() and not pending_alias.is_symlink(), 'interrupted alias update; inspect')
                pending_alias.symlink_to(final.name, target_is_directory=True)
                os.replace(pending_alias, alias)
        def writable_retry(function, path, error):
            Path(path).parent.chmod(0o700)
            Path(path).chmod(0o700)
            function(path)
        shutil.rmtree(directory, onerror=writable_retry)
        directory.symlink_to(final.name, target_is_directory=True)
    return {"compressed_replays": changed, "recovery": "gzip -dk FILE.repl26a.gz; bytes preserved"}


def import_external(arena, bot, payload):
    official_id = payload["official_match_id"]
    require(isinstance(official_id, str) and 0 < len(official_id) <= 200, "official match ID required")
    require(payload.get("source_commit") and payload.get("submission_id"), "immutable own submission mapping required")
    source = arena.db.one("SELECT id FROM revisions WHERE bot_id=? AND commit_sha=?", (bot, payload["source_commit"]))
    require(source, "unknown source commit")
    require(payload.get("outcome") in ("A", "B", "UNKNOWN"), "external outcome must be explicit")
    directory = arena.root / "external" / identity(official_id)
    files = payload.get("files", {})
    require(len(files) <= 8 and (files or payload.get("staged_replay")), "original files or staged replay required")
    from .common import safe_relative
    decoded = {}
    for name, data in files.items():
        safe_relative(name)
        require(len(data) < 1024 * 1024, "attachment too large; operator must stage larger replay separately")
        decoded[name] = base64.b64decode(data, validate=True)
    require(not directory.exists(), "external ID already imported; inspect existing evidence")
    save_source(decoded, directory)
    if payload.get("staged_replay"):
        import os
        import stat
        name = payload["staged_replay"]
        safe_relative(name)
        require("/" not in name and name.endswith(".repl26a"), "staged replay must be one plain filename")
        staged = arena.root / "external-inbox" / bot / name
        fd = os.open(staged, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            info = os.fstat(fd)
            require(stat.S_ISREG(info.st_mode) and 0 < info.st_size <= 1024 ** 3, "invalid staged replay")
            require(shutil.disk_usage(arena.root).free > info.st_size + arena.config["limits"]["minimum_free_bytes"], "disk pressure")
            with os.fdopen(fd, "rb", closefd=False) as source, (directory / name).open("wb") as target:
                shutil.copyfileobj(source, target)
        finally:
            os.close(fd)
    metadata = {k: v for k, v in payload.items() if k != "files"}
    metadata["opponent_version"] = metadata.get("opponent_version")
    metadata["controlled_local_evidence"] = False
    metadata["file_sha256"] = tree_manifest(directory)
    atomic_json(directory / "metadata.json", metadata)
    arena.db.execute("INSERT INTO external_matches VALUES(?,?,?,?)",
                     (official_id, json.dumps(metadata), str(directory), time.time()))
    return {"official_match_id": official_id, "artifact": str(directory), "controlled_local_evidence": False}


def backup(arena):
    directory = arena.root / "backups" / str(time.time_ns())
    directory.mkdir(parents=True)
    arena.db.backup(directory / "arena.sqlite")
    atomic_json(directory / "manifest.json", {"database_sha256": file_hash(directory / "arena.sqlite"),
                "config_hash": arena.config["config_hash"], "engine_lock": read_json(arena.config["engine_lock"]),
                "artifact_manifests": {str(p.relative_to(arena.root)): file_hash(p)
                                       for p in (arena.root / "matches").rglob("completion.json")}})
    if arena.config['limits'].get('rolling_history',False):
        # Retain three successful local DB backups; source and live state are
        # outside these exact numeric backup directories.
        backups = sorted((p for p in (arena.root/'backups').iterdir()
                          if p.is_dir() and not p.is_symlink() and p.name.isdigit()
                          and (p/'arena.sqlite').is_file() and (p/'manifest.json').is_file()), key=lambda p:p.name)
        from .storage import remove_redundant
        for previous in backups[:-3]:
            remove_redundant(previous)
    return {"backup": str(directory), "separate_volume_copy": "operator must copy database, manifest and referenced artifact trees"}


def restore_drill(database, destination):
    require(not Path(destination).exists(), "restore destination must be new")
    with contextlib.closing(sqlite3.connect(database)) as source, contextlib.closing(sqlite3.connect(destination)) as target:
        source.backup(target)
        require(target.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "restore integrity failed")
        require(not target.execute("PRAGMA foreign_key_check").fetchall(), "restore foreign keys failed")
        tables = target.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    return {"restored_copy": str(destination), "tables": tables, "integrity": "ok", "activated": False}
