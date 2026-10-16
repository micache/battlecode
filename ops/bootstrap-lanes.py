#!/usr/bin/env python3
"""Trusted starter publication, only after both real starter games are validated."""
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, "/opt/battlecode")
from arena.common import ArenaError, lock, require, run
from arena.config import load
from arena.gitstore import commit_id, git, ingest, source_files
from arena.operations import ensure_starter_reference
from arena.service import Arena


def main():
    config = load("/etc/battlecode/arena.json")
    with lock(Path(config["root"]) / "state/service.lock"):
        arena = Arena(config)
        require(arena.db.get("starter_verified", False), "run/review complete starter games first")
        ensure_starter_reference(arena)
        mirror = Path(config["mirror"])
        if not mirror.exists():
            run(["git", "clone", "--mirror", config["repository_url"], str(mirror)])
        results = []
        for bot, worker in config["workers"].items():
            remote = git(mirror, "ls-remote", "--heads", "origin", f"refs/heads/{worker['branch']}")
            if not remote:
                directory = Path(tempfile.mkdtemp(prefix=f"bootstrap-{bot}-", dir=Path(config["root"]) / "repos"))
                git(directory, "init")
                git(directory, "remote", "add", "origin", config["repository_url"])
                git(directory, "fetch", "origin", config["infrastructure_commit"])
                git(directory, "checkout", "-b", worker["branch"], config["infrastructure_commit"])
                shutil.copytree(arena.root / "starter/src", directory / "bots" / bot / "src")
                notes = directory / "experiments" / bot / "NOTES.md"
                notes.parent.mkdir(parents=True)
                notes.write_text("# Bootstrap\n\nPinned official C++ starter. Baseline pending; no improvement claim.\n")
                git(directory, "add", "--", f"bots/{bot}", f"experiments/{bot}")
                git(directory, "-c", "user.name=Battlecode bootstrap", "-c", "user.email=arena@localhost",
                    "commit", "-m", f"Bootstrap {bot} from pinned official C++ starter")
                git(directory, "push", "origin", f"HEAD:refs/heads/{worker['branch']}")
            git(mirror, "fetch", "origin", f"refs/heads/{worker['branch']}:refs/remotes/origin/{worker['branch']}")
            revision = ingest(arena.db, config, bot, commit_id(mirror, f"refs/remotes/origin/{worker['branch']}"))
            git(mirror, "update-ref", f"refs/heads/{worker['branch']}", revision["commit_sha"])
            results.append({"bot": bot, "commit": revision["commit_sha"], "revision": revision["id"]})
        print(json.dumps({"baselines_pending": results}, indent=2))


if __name__ == "__main__":
    main()
