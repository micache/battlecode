import argparse
import json
from pathlib import Path
import sys

from .common import ArenaError, atomic_json, fresh_id, lock, read_json, require
from .config import load
from .service import Arena


def main(argv=None):
    parser = argparse.ArgumentParser(description="Trusted Battlecode arena operator")
    parser.add_argument("--config", default="/etc/battlecode/arena.json")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "serve", "status", "start", "pause", "adapter-resume", "backup", "compact", "acceptance-report", "tick"):
        sub.add_parser(name)
    starter = sub.add_parser("starter-check")
    starter.add_argument("--normalize-only", action="store_true")
    ingest_parser = sub.add_parser("ingest")
    ingest_parser.add_argument("bot")
    ingest_parser.add_argument("commit")
    register = sub.add_parser("register-starter")
    register.add_argument("revision_id")
    ready = sub.add_parser("verify-readiness")
    ready.add_argument("evidence")
    restore = sub.add_parser("restore-drill")
    restore.add_argument("database")
    restore.add_argument("destination")
    toolchain = sub.add_parser("register-toolchain")
    toolchain.add_argument("--image-id", required=True)
    toolchain.add_argument("--template", required=True)
    toolchain.add_argument("--compiler-record", required=True)
    toolchain.add_argument("--profile-record")
    worker = sub.add_parser("worker")
    worker.add_argument("--owner-config", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "worker":
            from .worker import serve
            serve(args.owner_config)
            return 0
        config = load(args.config)
        if args.command == "serve":
            Arena(config).serve()
            return 0
        if args.command == "status":
            # Read exported snapshot without creating another SQLite writer.
            result = read_json(Path(config["root"]) / "public/status.json")
        elif args.command == "acceptance-report":
            result = read_json(Path(config["root"]) / "public/acceptance.json")
        elif args.command in ("start", "pause", "adapter-resume", "backup", "compact"):
            # Commands are consumed by the one DB writer, including while globally paused.
            import time
            request_id = fresh_id("request")
            path = Path(config["root"]) / "control" / f"{request_id}.json"
            atomic_json(path, {"operation": args.command})
            deadline = time.monotonic() + 60
            while path.exists() and time.monotonic() < deadline:
                time.sleep(0.5)
            require(not path.exists(), f"operator command queued: {request_id}; start service to consume it")
            result = {"acknowledged": args.command, "request_id": request_id}
        else:
            with lock(Path(config["root"]) / "state/service.lock"):
                arena = Arena(config)
                from . import operations
                if args.command == "init":
                    result = arena.export_status()
                elif args.command in ("start", "pause"):
                    arena.db.put("paused", args.command == "pause")
                    result = arena.export_status()
                elif args.command == "adapter-resume":
                    arena.db.put("adapter_paused", False)
                    result = arena.export_status()
                elif args.command == "tick":
                    arena.step()
                    result = arena.export_status()
                elif args.command == "starter-check":
                    result = operations.starter_check(arena, args.normalize_only)
                elif args.command == "register-starter":
                    result = operations.register_starter(arena, args.revision_id)
                elif args.command == "ingest":
                    from .gitstore import ingest
                    result = ingest(arena.db, config, args.bot, args.commit)
                elif args.command == "verify-readiness":
                    result = operations.verify_readiness(arena, args.evidence)
                elif args.command == "backup":
                    result = operations.backup(arena)
                elif args.command == "restore-drill":
                    result = operations.restore_drill(args.database, args.destination)
                elif args.command == "register-toolchain":
                    result = operations.register_toolchain(config, args.image_id, args.template, read_json(args.compiler_record),
                                                          read_json(args.profile_record) if args.profile_record else None)
                else:
                    raise ArenaError("unsupported command")
        print(json.dumps(result, indent=2))
        return 0
    except (ArenaError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
