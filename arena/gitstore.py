from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

from .common import (ArenaError, atomic_json, clean_environment, file_hash, identity, require,
                     run, safe_relative, sha, tree_hash)


def git(repo, *args):
    return run(["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
                "-C", repo, *args])


def commit_id(repo, ref):
    value = git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    require(re.fullmatch(r"[a-f0-9]{40}", value), "full SHA-1 commit required")
    return value


def owned_path(bot, path):
    safe_relative(path)
    return path.startswith(f"bots/{bot}/src/") or path.startswith(f"experiments/{bot}/")


def source_files(repo, commit, bot):
    require(re.fullmatch(r"[a-f0-9]{40}", commit), "immutable commit required")
    prefix = f"bots/{bot}/src/"
    entries = git(repo, "ls-tree", "-r", "-z", commit, "--", f"bots/{bot}")
    result = {}
    for entry in entries.split("\0"):
        if not entry:
            continue
        header, path = entry.split("\t", 1)
        mode, kind, object_id = header.split()
        safe_relative(path)
        require(path.startswith(prefix), "only C++ src files allowed in bot package")
        require(mode == "100644" and kind == "blob", "symlinks/executables/submodules forbidden")
        require(Path(path).suffix in (".cpp", ".h", ".hpp", ".cc", ".cxx"), "unexpected dependency/file")
        size = int(git(repo, "cat-file", "-s", object_id))
        require(size <= 256 * 1024, "source file too large")
        data = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", object_id],
                              capture_output=True, check=True, env=clean_environment(True)).stdout
        result[path[len(prefix):]] = data
    require(result and len(result) <= 128 and sum(map(len, result.values())) <= 1024 * 1024,
            "empty/oversized source")
    return result


def validate_delta(repo, previous, candidate, bot):
    if previous:
        require(subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", previous, candidate],
                               capture_output=True).returncode == 0, "branch rewound/diverged")
        for path in git(repo, "diff", "--name-only", "--no-renames", previous, candidate).splitlines():
            require(owned_path(bot, path), f"out-of-scope change: {path}")


def ingest(db, config, bot, commit):
    mirror = config["mirror"]
    state = db.one("SELECT * FROM bots WHERE id=?", (bot,))
    require(state, "unregistered bot")
    require(commit_id(mirror, commit) == commit, "commit identity conflict")
    existing = db.one("SELECT * FROM revisions WHERE bot_id=? AND commit_sha=?", (bot, commit))
    if existing:
        return existing
    previous = state["latest_tip"] or config["infrastructure_commit"]
    validate_delta(mirror, previous, commit, bot)
    files = source_files(mirror, commit, bot)
    source_hash = identity({path: sha(data) for path, data in sorted(files.items())})
    revision_id = identity({"bot": bot, "commit": commit})
    destination = Path(config["root"]) / "snapshots" / revision_id
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        temp = Path(tempfile.mkdtemp(prefix=".snapshot-", dir=destination.parent))
        for name, data in files.items():
            target = temp / "src" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        atomic_json(temp / "identity.json", {"commit": commit, "source_hash": source_hash, "bot": bot,
                                           "infrastructure_commit": config["infrastructure_commit"]})
        temp.rename(destination)
        for target in destination.rglob("*"):
            target.chmod(0o550 if target.is_dir() else 0o440)
        destination.chmod(0o550)
    require(tree_hash(destination / "src") == source_hash, "snapshot hash mismatch")
    with db.transaction():
        # Running revisions are retained; only unstarted older revisions are superseded.
        db.execute("UPDATE revisions SET state='SUPERSEDED' WHERE bot_id=? AND state='PENDING'", (bot,))
        db.execute("INSERT INTO revisions VALUES(?,?,?,?,?,?,?,?,?,?)",
                   (revision_id, bot, commit, source_hash, state["accepted_source_hash"], None,
                    str(destination), config["infrastructure_commit"],
                    "NO_CHANGE" if state["accepted_source_hash"] == source_hash else "PENDING", time.time()))
        db.execute("UPDATE bots SET latest_tip=? WHERE id=?", (commit, bot))
    return db.one("SELECT * FROM revisions WHERE id=?", (revision_id,))


def poll(db, config, bot):
    branch = config["workers"][bot]["branch"]
    git(config["mirror"], "fetch", "--no-tags", "origin", f"refs/heads/{branch}:refs/remotes/origin/{branch}")
    commit = commit_id(config["mirror"], f"refs/remotes/origin/{branch}")
    revision = ingest(db, config, bot, commit)
    if git(config["mirror"], "rev-parse", "--is-bare-repository") == "true":
        git(config["mirror"], "update-ref", f"refs/heads/{branch}", commit)
    return revision


def diff_paths(repo):
    tracked = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-only", "--no-renames", "HEAD").splitlines()
    untracked = git(repo, "ls-files", "--others", "--exclude-standard").splitlines()
    return sorted(set(tracked + untracked))


def validate_worktree(repo, bot):
    paths = diff_paths(repo)
    for name in paths:
        require(owned_path(bot, name), f"out-of-scope worker edit: {name}")
        path = Path(repo) / name
        require(not path.is_symlink(), "worker symlink forbidden")
        if path.exists():
            require(path.is_file() and path.stat().st_size <= 256 * 1024, "oversized/nonregular edit")
    require(len(paths) <= 256, "too many changed paths")
    for prefix in (f"bots/{bot}/src", f"experiments/{bot}"):
        root = Path(repo) / prefix
        require(not root.is_symlink(), "owned directory is a symlink")
        for item in root.rglob("*"):
            require(not item.is_symlink(), "owned subtree symlink forbidden")
    return paths
