#!/usr/bin/env python3
"""Trusted starter publication, only after both real starter games are validated."""
import json
import argparse
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import ArenaError, atomic_json, lock, read_json, require, run, tree_hash
from arena.config import load
from arena.gitstore import commit_id, git, ingest, source_files
from arena.operations import ensure_starter_reference
from arena.service import Arena
from arena.protocol import decode_source, encode_source, save_source


def local_bootstrap(path):
    """One-time operator handoff using native local Git authentication, not owner credentials."""
    exported = read_json(path)
    files, source_hash = decode_source(exported['source'])
    require(source_hash == exported['source_hash'] and exported['starter_games']['verified'] and
            exported['sdk_cpp_sha256'] == '90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d',
            'unverified starter export')
    base = exported['infrastructure_commit']
    directory = Path(tempfile.mkdtemp(prefix='battlecode-starter-publication-'))
    repository = 'git@github.com:micache/battlecode.git'
    git(directory, 'init')
    git(directory, 'remote', 'add', 'origin', repository)
    git(directory, 'fetch', 'origin', base)
    results = []
    for bot in ('alpha','beta'):
        branch = f'bot/{bot}'
        existing = git(directory, 'ls-remote', '--heads', 'origin', f'refs/heads/{branch}')
        if existing:
            results.append({'bot':bot,'commit':existing.split()[0],'preserved_existing':True})
            continue
        git(directory, 'checkout', '-b', branch, base)
        save_source(files, directory / 'bots' / bot / 'src')
        notes = directory / 'experiments' / bot / 'NOTES.md'
        notes.parent.mkdir(parents=True)
        notes.write_text('# Bootstrap\n\nPinned official C++ starter, after two reviewed full games. Baseline pending; no improvement claim.\n')
        git(directory, 'add', '--', f'bots/{bot}', f'experiments/{bot}')
        git(directory, '-c','user.name=Battlecode bootstrap','-c','user.email=arena@localhost',
            'commit','-m',f'Bootstrap {bot} from reviewed official C++ starter')
        commit = commit_id(directory,'HEAD')
        atomic_json(directory / f'bootstrap-{bot}-intent.json',{'branch':branch,'commit':commit,'source_hash':source_hash})
        print(json.dumps({'before_push':commit,'branch':branch,'checkpoint':str(directory)}),flush=True)
        require(not git(directory,'ls-remote','--heads','origin',f'refs/heads/{branch}'),'remote branch appeared; preserve checkpoint')
        git(directory,'push','origin',f'HEAD:refs/heads/{branch}')
        results.append({'bot':bot,'commit':commit,'source_hash':source_hash})
        # Keep handoff records outside the next branch's working tree.
        (directory / f'bootstrap-{bot}-intent.json').rename(directory / '.git' / f'bootstrap-{bot}-intent.json')
    print(json.dumps({'bootstrap':results,'checkpoint':str(directory)},indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', action='store_true')
    parser.add_argument('--from-export')
    args=parser.parse_args()
    if args.from_export:
        local_bootstrap(args.from_export)
        return
    config = load("/etc/battlecode/arena.json")
    with lock(Path(config["root"]) / "state/service.lock"):
        arena = Arena(config)
        require(arena.db.get("starter_verified", False), "run/review complete starter games first")
        if args.export:
            payload={'source':encode_source(arena.root / 'starter/src'),
                     'source_hash':tree_hash(arena.root / 'starter/src'),
                     'infrastructure_commit':config['infrastructure_commit'],
                     'sdk_cpp_sha256':arena.adapter().lock['sdk_cpp_sha256'],
                     'starter_games':read_json(arena.root / 'acceptance/starter-check.json')}
            target=arena.root / 'acceptance/official-starter-export.json'
            atomic_json(target,payload,0o644)
            print(json.dumps({'exported':str(target)}))
            return
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
