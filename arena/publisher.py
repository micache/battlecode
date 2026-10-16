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
    # Notes may be markdown/JSON, but never execute as build recipes.
    import base64
    decoded_notes = {}
    require(isinstance(notes, dict) and len(notes) <= 128, "oversized experiment history")
    for name, data in notes.items():
        safe_relative(name)
        require(Path(name).suffix in (".md", ".json", ".txt", ".patch", ".py") and len(data) <= 350000,
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
