import argparse
import json
import os
from pathlib import Path
import pwd
import sys
import time

from .common import ArenaError, atomic_json, fresh_id, read_json, require
from .protocol import encode_source


def owner_config(path):
    config = read_json(path)
    require(pwd.getpwuid(os.getuid()).pw_name == config["linux_user"], "owner/Linux user mismatch")
    return config


def request(config, operation, payload=None, timeout=1100):
    request_id = fresh_id("request")
    root = Path(config["root"])
    message = {"protocol_version": 1, "id": request_id, "bot_id": config["bot_id"],
               "operation": operation, "payload": payload or {}}
    atomic_json(root / "inbox" / config["bot_id"] / f"{request_id}.json", message, 0o640)
    response = root / "outbox" / config["bot_id"] / f"{request_id}.json"
    until = time.monotonic() + timeout
    while time.monotonic() < until:
        if response.exists():
            data = read_json(response)
            require(data["ok"], data.get("error", "request failed"))
            return data["result"]
        time.sleep(1)
    raise ArenaError(f"request pending/unknown; preserve ID {request_id}, inspect status before retry")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Owner mailbox client; never writes central SQLite")
    parser.add_argument("--config", default="/etc/battlecode/owner.json")
    parser.add_argument("operation", choices=["status", "feedback", "history", "check-report", "slice", "external-slice", "pause", "resume", "claim", "release", "publish", "import-external"])
    parser.add_argument("--owner")
    parser.add_argument("--attempt")
    parser.add_argument("--metadata")
    parser.add_argument("--match-id")
    parser.add_argument('--task-id')
    parser.add_argument('--source-hash')
    parser.add_argument("--file", default="stderr.log")
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args(argv)
    try:
        config = owner_config(args.config)
        if args.operation == "publish":
            from .worker import publish_attempt
            require(args.attempt, "--attempt required")
            result = publish_attempt(config, Path(args.attempt), args.owner)
            request(config, "worker-finished", result)
        elif args.operation == "import-external":
            require(args.metadata, "--metadata required")
            result = request(config, args.operation, read_json(args.metadata))
        elif args.operation in ("slice", "external-slice"):
            require(args.match_id, "--match-id required")
            result = request(config, args.operation, {"match_id": args.match_id, "file": args.file, "offset": args.offset})
        elif args.operation == 'history':
            result = request(config, 'history', {'task_id': args.task_id, 'offset': args.offset})
        elif args.operation == 'check-report':
            require(args.task_id and args.source_hash, '--task-id and --source-hash required')
            result = request(config, 'check-report', {'task_id': args.task_id, 'source_hash': args.source_hash})
        else:
            payload = {"owner": args.owner} if args.owner else {}
            require(args.operation not in ("claim", "release") or args.owner, "--owner required")
            result = request(config, args.operation, payload)
            if args.operation == "claim":
                from .worker import make_attempt
                Path(config["attempts"]).mkdir(parents=True, exist_ok=True, mode=0o700)
                attempt = Path(config["attempts"]) / result["task"]["task_id"]
                result["attempt"] = str(attempt if attempt.exists() else make_attempt(config, result["task"]))
        print(json.dumps(result, indent=2))
    except (ArenaError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1
    return 0


def check_main(argv=None):
    parser = argparse.ArgumentParser(description="Approved exact-source build and both-side smoke wrapper")
    parser.add_argument("--owner-config", required=True)
    parser.add_argument("--task", default=".agent/task.json")
    args = parser.parse_args(argv)
    try:
        config = owner_config(args.owner_config)
        task = read_json(args.task)
        require(task["bot_id"] == config["bot_id"], "bot-check identity mismatch")
        directory = Path.cwd() / "bots" / task["bot_id"] / "src"
        result = request(config, "check", {"task_id": task["task_id"], "source": encode_source(directory)})
        report = Path(".agent") / f"check-{task['task_id']}.json"
        result['report_path'] = str(report)
        atomic_json(report, result, 0o600)
        print(json.dumps(dict(result, local_report_path=str(report))))
        return result["exit_code"]
    except (ArenaError, OSError, ValueError) as exc:
        print(json.dumps({"state": "BLOCKED", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
