#!/usr/bin/env python3
"""Administrator-only, non-destructive installation. Never authenticates an owner."""
import argparse
import grp
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import sys


def command(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def install(source, revision, persistent_ack, dry=False, temporary_colab=False, blaxel=False):
    required = ("python3", "git", "runuser", "useradd", "groupadd") + (
        ("bwrap", "prlimit") if temporary_colab else (("podman",) if blaxel else ("podman", "systemctl")))
    missing = [tool for tool in required if not shutil.which(tool)]
    if missing:
        raise RuntimeError("administrator must install: " + ", ".join(missing))
    if dry:
        return {"dry_run": True, "source": str(source), "revision": revision,
                "users": ["bc-arena", "bc-alpha", "bc-beta"], "root": "/srv/battlecode",
                "services_started": False, "owner_login": "manual, after users exist"}
    if os.geteuid() != 0:
        raise RuntimeError("administrator command required: run with sudo")
    if not temporary_colab and not blaxel and Path("/proc/1/comm").read_text().strip() != "systemd":
        raise RuntimeError("host PID 1 is not systemd; use a persistent systemd VM for this acceptance")
    if not persistent_ack and not temporary_colab:
        raise RuntimeError("select/mount persistent /srv storage, then pass --ack-persistent-volume")
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11+ required")
    if Path("/opt/battlecode").exists() or Path("/etc/battlecode/arena.json").exists():
        raise RuntimeError("installation already exists; preserve it and follow documented upgrade/rollback")
    from provision import provision_users
    provision_users()
    # Rootless Podman requires subordinate IDs and a working user namespace. No privileged socket is used.
    if not temporary_colab and not any(line.startswith("bc-arena:") for line in Path("/etc/subuid").read_text().splitlines()):
        raise RuntimeError("administrator must allocate non-overlapping subuid/subgid ranges for bc-arena; then continue setup manually")
    destination = Path("/opt/battlecode")
    destination.mkdir(mode=0o755)
    for name in ("arena", "ops", "schemas", "config", "sources", "evidence", "docs", "fixtures", "skills"):
        shutil.copytree(source / name, destination / name, ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("AGENTS.md", "CLAUDE.md", "ARENA.md", "AUTH_AND_OPERATIONS.md", "BOT_REFERENCE.md", "PROMPTS.md",
                 "PLAYBOOKS.md", "RESEARCH.md", "RULES_CHECKLIST.md", "pyproject.toml", ".gitignore"):
        shutil.copyfile(source / name, destination / name)
    (destination / "INFRASTRUCTURE_COMMIT").write_text(revision + "\n")
    arena_uid = pwd.getpwnam("bc-arena").pw_uid
    read_gid = grp.getgrnam("bc-read").gr_gid
    runtime = Path("/run/battlecode-arena")
    runtime.mkdir(exist_ok=True)
    os.chown(runtime, arena_uid, read_gid)
    runtime.chmod(0o700)
    root = Path("/srv/battlecode")
    if blaxel and root.is_symlink():
        root.resolve().mkdir(parents=True, exist_ok=True)
    root.mkdir(parents=True, exist_ok=True)
    os.chown(root, arena_uid, read_gid)
    root.chmod(0o750)
    for name in ("state", "repos", "builds", "matches", "evaluations", "feedback", "inbox", "outbox", "tasks",
                 "backups", "public", "control", "locks", "maps", "snapshots", "checks", "acceptance", "external-inbox"):
        directory = root / name
        directory.mkdir(exist_ok=True)
        os.chown(directory, arena_uid, read_gid)
        directory.chmod(0o700 if name in ("state", "control", "backups", "inbox", "outbox", "tasks",
                                         "matches", "evaluations", "builds", "checks", "acceptance") else 0o750)
    # Inbox/outbox/tasks parents must be traversable, but directory listings remain private.
    for name in ("inbox", "outbox", "tasks", "external-inbox"):
        (root / name).chmod(0o711)
    for bot in ("alpha", "beta"):
        group_id = grp.getgrnam(f"bc-{bot}").gr_gid
        for name in ("inbox", "outbox", "tasks", "feedback", "external-inbox"):
            directory = root / name / bot
            directory.mkdir(exist_ok=True)
            os.chown(directory, arena_uid, group_id)
            directory.chmod(0o2770 if name in ("inbox", "external-inbox") else 0o2750)
    model_lock = root / "model.lock"
    model_lock.touch(exist_ok=False)
    os.chown(model_lock, 0, read_gid)
    model_lock.chmod(0o660)
    etc = Path("/etc/battlecode")
    etc.mkdir(mode=0o755, exist_ok=True)
    config = json.loads((source / "config/pilot.json").read_text())
    config["infrastructure_commit"] = revision
    if temporary_colab:
        config["deployment"] = {"mode": "temporary-colab", "reboot_persistence_verified": False,
                                "sandbox": "bubblewrap-watchdog-v1"}
        config["repository_url"] = "git@github.com:micache/battlecode.git"
    if blaxel:
        if not Path('/persist').is_mount():
            raise RuntimeError('Blaxel persistent /persist volume must be mounted')
        for directory in (root, etc, Path('/home/bc-arena'), Path('/home/bc-alpha'), Path('/home/bc-beta')):
            if directory.stat().st_dev != Path('/var/lib/battlecode-volume').stat().st_dev:
                raise RuntimeError(f'{directory} is not on the persistent volume')
        config['deployment'] = {'mode': 'blaxel', 'reboot_persistence_verified': False,
                                'sandbox': 'rootless-podman', 'volume': 'battlecode-arena-data'}
        config['repository_url'] = 'git@github.com:micache/battlecode.git'
        config['limits']['artifact_budget_bytes'] = 3 * 1024**3
        config['limits']['minimum_free_bytes'] = 1024**3
        config['limits']['backup_interval_seconds'] = 86400
    (etc / "arena.json").write_text(json.dumps(config, indent=2) + "\n")
    (etc / "arena.json").chmod(0o644)
    for bot in ("alpha", "beta"):
        owner = {"protocol_version": 1, "bot_id": bot, "linux_user": f"bc-{bot}", "branch": f"bot/{bot}",
                 "root": str(root), "infrastructure": str(destination), "read_repository": config["mirror"],
                 "clone": f"/home/bc-{bot}/battlecode", "attempts": f"/home/bc-{bot}/attempts",
                 "codex_executable": f"/home/bc-{bot}/.local/bin/codex", "codex_sha256": None, "model": None}
        (etc / f"{bot}.json").write_text(json.dumps(owner, indent=2) + "\n")
    for executable, module, function in (("arena", "arena.cli", "main"), ("arena-client", "arena.client", "main"),
                                         ("bot-check", "arena.client", "check_main")):
        target = Path("/usr/local/bin") / executable
        content = f"#!/usr/bin/python3\nimport sys\nsys.path.insert(0, '/opt/battlecode')\nfrom {module} import {function}\nsys.exit({function}())\n"
        if target.exists():
            if target.read_text() != content or target.stat().st_uid != 0:
                raise RuntimeError(f"refusing to overwrite existing command: {target}")
        else:
            target.write_text(content)
        target.chmod(0o755)
    for path in (source / "ops/systemd").glob("*"):
        if blaxel:
            continue
        target = Path("/etc/systemd/system") / path.name
        if target.exists():
            raise RuntimeError(f"refusing to overwrite existing unit: {target}")
        shutil.copyfile(path, target)
    if not temporary_colab and not blaxel:
        command("systemctl", "daemon-reload")
    return {"installed": True, "revision": revision, "services_started": False,
            "next": "Follow /opt/battlecode/ops/OPERATIONS.md: prepare engine, starter checks, branches, owner logins."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--ack-persistent-volume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--temporary-colab", action="store_true",
                        help="Explicitly opt into ephemeral storage and process supervision; no reboot guarantee")
    parser.add_argument("--blaxel", action="store_true", help="Persistent Blaxel volume and non-systemd supervisor")
    args = parser.parse_args()
    try:
        source = Path(args.source).resolve()
        revision = command("git", "-c", f"safe.directory={source}", "-C", str(source), "rev-parse", "HEAD")
        if command("git", "-c", f"safe.directory={source}", "-C", str(source), "status", "--porcelain"):
            raise RuntimeError("commit infrastructure changes before installation")
        if args.blaxel and args.temporary_colab:
            raise RuntimeError('choose exactly one deployment profile')
        print(json.dumps(install(source, revision, args.ack_persistent_volume, args.dry_run,
                                 args.temporary_colab, args.blaxel), indent=2))
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"installed": False, "error": str(exc)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
