"""Trusted GitHub publisher. Owners and coding processes need no GitHub write credential."""
from pathlib import Path
import time

from .common import atomic_json, identity, require, run, safe_relative, sha, tree_hash
from .gitstore import commit_id, git, source_files, validate_worktree
from .protocol import decode_source, save_source


def publish(arena, bot, task, source, notes):
    expected = task["input_revision"]
    branch = task["branch"]
    config = arena.config
    files, source_hash = decode_source(source)
    # Notes and source-level regression/reference fixtures are data, never build recipes.
    import base64
    decoded_notes = {}
    require(isinstance(notes, dict) and len(notes) <= 128, "oversized experiment history")
    for name, data in notes.items():
        safe_relative(name)
        require(Path(name).suffix in (".md", ".json", ".txt", ".patch", ".py", ".cpp", ".cc", ".cxx", ".h", ".hpp")
                and len(data) <= 350000,
                "unexpected/oversized experiment artifact")
        decoded_notes[name] = base64.b64decode(data, validate=True)
    require(sum(map(len, decoded_notes.values())) <= 1024 * 1024, "oversized notes")
    def remote_tip():
        result = git(config["mirror"], "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
        require(len(result.splitlines()) == 1, "branch missing/ambiguous")
        tip, ref = result.split()
        require(ref == f"refs/heads/{branch}", "wrong branch")
        return tip
    require(remote_tip() == expected, "non-fast-forward conflict; preserve patch and pause")
    directory = arena.root / "publication" / task["task_id"]
    require(not directory.exists(), "publication checkpoint exists; reconcile instead of retrying")
    directory.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--no-hardlinks", "--no-checkout", config["mirror"], str(directory)])
    git(directory, "checkout", "-B", branch, expected)
    git(directory, "remote", "set-url", "origin", config["repository_url"])
    import shutil
    for prefix, decoded in ((f"bots/{bot}/src", files), (f"experiments/{bot}", decoded_notes)):
        target = directory / prefix
        if target.exists():
            shutil.rmtree(target)
        save_source(decoded, target)
    actual_paths = validate_worktree(directory, bot)
    require(actual_paths and tree_hash(directory / "bots" / bot / "src") == source_hash, "publication source mismatch")
    git(directory, "add", "--", f"bots/{bot}/src", f"experiments/{bot}")
    git(directory, "-c", "user.name=Battlecode publisher", "-c", "user.email=arena@localhost",
        "commit", "-m", f"{bot}: {task['task_id']}")
    commit = commit_id(directory, "HEAD")
    require(git(directory, "rev-parse", "HEAD^") == expected, "publication parent mismatch")
    require(identity({name: sha(data) for name, data in source_files(directory, commit, bot).items()}) == source_hash,
            "committed source differs from checked candidate")
    # Persist the exact commit BEFORE the non-idempotent external operation.
    arena.db.execute("UPDATE tasks SET published_commit=? WHERE id=?", (commit, task["task_id"]))
    atomic_json(directory / "publication-intent.json", {"task_id": task["task_id"], "commit": commit,
                "expected_tip": expected, "branch": branch, "source_hash": source_hash, "created": time.time()})
    require(remote_tip() == expected, "remote writer conflict; preserve normal commit")
    git(directory, "push", "origin", f"HEAD:refs/heads/{branch}")
    return {"task_id": task["task_id"], "state": "PUBLISHED", "commit": commit,
            "source_hash": source_hash, "actual_changed_paths": actual_paths}


def recover_publication(arena, bot, payload):
    """Operator-only, stopped-service repair of the known pre-push artifact bug.

    Never reuse this for auth/quota failures, conflicts or ambiguous pushes.
    Source is checked again; no model invocation or old outcome overwrite.
    """
    import json
    from .supervisor import check_source, handle_request, trusted_task
    task, envelope = trusted_task(arena, bot, payload['task_id'])
    worker = arena.db.one('SELECT * FROM workers WHERE id=?', (bot,))
    lane = arena.db.one('SELECT * FROM bots WHERE id=?', (bot,))
    require(arena.db.get('paused', True), 'pause scheduling before operator recovery')
    require(task['state'] == 'PAUSED' and worker['state'] == 'PAUSED' and worker['task_id'] == task['id']
            and worker['detail'] == 'unexpected/oversized experiment artifact', 'not the known recoverable publisher failure')
    require(task['published_commit'] is None and not (arena.root / 'publication' / task['id']).exists(),
            'publication intent exists; reconcile remote, never retry blindly')
    require(envelope['engine_lock_hash'] == arena.adapter().lock_hash and
            envelope['base_source_hash'] == lane['accepted_source_hash'] and
            envelope['input_revision'] == lane['latest_tip'], 'recovery inputs changed')
    require(payload['result'] == json.loads(task['result']) and payload['result']['outcome'] == 'READY_FOR_EVAL',
            'preserved native result mismatch')
    _, source_hash = decode_source(payload['source'])
    old_check = arena.db.get(f"check:{task['id']}:{source_hash}")
    require(old_check and old_check['state'] == 'PASSED', 'no exact-source previously passed candidate')
    arena.db.put(f"operator-publication-recovery:{task['id']}", {'at': time.time(), 'old_state': task['state'],
                 'source_hash': source_hash, 'infrastructure_commit': arena.config['infrastructure_commit'],
                 'model_invocations': 0, 'reason': 'preserve valid native candidate after artifact allowlist repair'})
    arena.db.execute("UPDATE tasks SET state='DISPATCHED' WHERE id=?", (task['id'],))
    arena.db.execute("UPDATE workers SET state='RUNNING' WHERE id=?", (bot,))
    try:
        check = check_source(arena, bot, payload)
        require(check['state'] == 'PASSED', 'fresh exact-source validation failed')
        publication = handle_request(arena, bot, {'operation': 'publish', 'payload': payload})
        handle_request(arena, bot, {'operation': 'worker-finished', 'payload': publication})
        return dict(publication, operator_recovery=True, new_model_invocations=0)
    except Exception as exc:
        arena.db.execute("UPDATE workers SET state='PAUSED',detail=? WHERE id=?", (str(exc), bot))
        raise  # Keep DISPATCHED/PUBLICATION_APPROVED and any intent for explicit reconciliation.
