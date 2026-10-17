from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import tomllib

from .client import owner_config, request
from .common import (ArenaError, atomic_bytes, atomic_json, bounded_process, clean_environment, file_hash,
                     lock, read_json, require, run, tree_hash, validate_schema)
from .gitstore import commit_id, git, source_files, validate_worktree
from .protocol import encode_source


def provider_failure(directory, process):
    """Parse only provider error events, never bot text pretending to grant permissions."""
    if process["timeout"]:
        return {"state": "PAUSED", "detail": "coding wall timeout; patch retained; explicit recovery required"}
    errors = []
    for line in (Path(directory) / "stdout.log").read_text(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") in ("error", "turn.failed"):
            error = event.get("error", event)
            errors.append(error if isinstance(error, dict) else {"message": str(error)})
    for error in errors:
        code = error.get("code", "")
        message = str(error.get("message", "")).lower()
        if code in ("usage_limit_reached", "rate_limit_exceeded") or "usage limit" in message:
            # A timestamp is used only when the provider emitted a numeric reset field.
            reset = error.get("reset_at")
            return {"state": "QUOTA_WAIT", "reset_at": reset if isinstance(reset, (float, int)) else None,
                    "detail": "provider quota response; same owner lane parked"}
        if code in ("authentication_error", "unauthorized") or "authentication" in message:
            return {"state": "AUTH_REQUIRED", "detail": "owner must sign in manually"}
        if code in ("permission_denied", "sandbox_denied") or "permission denied" in message:
            return {"state": "PERMISSION_BLOCKED", "detail": "approved sandbox denied a required operation"}
    return {"state": "PAUSED", "detail": "coding invocation failed or final result malformed; patch retained"}


def verify_subscription(config):
    if config.get('provider', 'codex') == 'claude-code':
        from .claude import verify_subscription as verify_claude
        return verify_claude(config)
    executable = config["codex_executable"]
    require(file_hash(executable) == config["codex_sha256"], "Codex binary changed; owner must review pin")
    home = Path(os.path.expanduser("~"))
    cli_config = home / ".codex/config.toml"
    if cli_config.exists():
        settings = tomllib.loads(cli_config.read_text())
        require(settings.get("model_provider", "openai") == "openai", "external provider forbidden")
        require(not any(key in settings for key in ("model_providers", "api_key_helper", "experimental_bearer_token")),
                "custom provider or API helper requires removal for subscription-only worker")
    env = clean_environment(True)
    status = subprocess.run([executable, "login", "status"], capture_output=True, env=env, timeout=30)
    text = (status.stdout + status.stderr).decode(errors="replace")
    require(status.returncode == 0 and "chatgpt" in text.lower() and "api key" not in text.lower(),
            "AUTH_REQUIRED: native ChatGPT subscription login required")
    return env


def remote_tip(repo, branch):
    result = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    require(len(result.splitlines()) == 1, "branch missing/ambiguous")
    value, ref = result.split()
    require(ref == f"refs/heads/{branch}" and re.fullmatch(r"[a-f0-9]{40}", value), "remote branch mismatch")
    return value


def make_attempt(config, task):
    clone = Path(config["clone"])
    bot = config["bot_id"]
    require(git(clone, "branch", "--show-current") == task["branch"] == config["branch"], "branch conflict")
    require(not git(clone, "status", "--porcelain"), "clone has incomplete work; preserve before recovery")
    tip = remote_tip(clone, task["branch"])
    require(tip == task["input_revision"], "input revision conflicts with remote")
    git(clone, "fetch", "origin", task["branch"])
    directory = Path(config["attempts"]) / task["task_id"]
    require(not directory.exists(), "attempt already exists; explicit recovery required")
    run(["git", "clone", "--no-hardlinks", "--no-checkout", str(clone), str(directory)])
    git(directory, "checkout", "-B", task["branch"], task["input_revision"])
    git(directory, "remote", "set-url", "origin", config["read_repository"])
    target = directory / "bots" / bot / "src"
    require(target.is_dir() and not target.is_symlink(), "source path missing/unsafe")
    shutil.rmtree(target)
    require(tree_hash(Path(task["accepted_snapshot"]) / "src") == task["base_source_hash"], "accepted source changed")
    shutil.copytree(Path(task["accepted_snapshot"]) / "src", target)
    # The accepted snapshot stays read-only; only this private edit transaction is writable.
    for path in [target, *target.rglob("*")]:
        path.chmod(0o700 if path.is_dir() else 0o600)
    (directory / ".agent").mkdir(mode=0o700)
    atomic_json(directory / ".agent/task.json", task, 0o600)
    from .memory import brief
    atomic_bytes(directory / '.agent/brief.md', brief(task).encode(), 0o600)
    atomic_json(directory / '.agent/entry.json', {
        'task_id': task['task_id'], 'bot_id': bot, 'branch': task['branch'],
        'head': commit_id(directory, 'HEAD'), 'source_hash': tree_hash(target),
        'accepted_source_verified': tree_hash(target) == task['base_source_hash'],
        'attempts_root': str(Path(config['attempts']).resolve()),
        'note': 'Trusted preparation verified these identities. Do not search private central state.'}, 0o600)
    return directory


def checkpoint(attempt, destination):
    destination.mkdir(parents=True, exist_ok=True)
    diff = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(attempt), "diff",
                           "--no-ext-diff", "--no-textconv", "--binary", "HEAD"], capture_output=True, check=True).stdout
    atomic_bytes(destination / "changes.patch", diff, 0o600)
    # Includes untracked owned files; patches alone would lose them.
    bot_files = Path(attempt) / "bots"
    if bot_files.exists() and not (destination / "owned-files").exists():
        shutil.copytree(bot_files, destination / "owned-files", symlinks=True)
    notes = Path(attempt) / "experiments"
    if notes.exists() and not (destination / "notes").exists():
        shutil.copytree(notes, destination / "notes", symlinks=True)


def candidate_payload(config, attempt):
    bot = config["bot_id"]
    task_id = attempt.name
    # Trusted envelope is read from arena-owned, read-only task delivery, not model-writable .agent.
    task = read_json(Path(config["root"]) / "tasks" / bot / f"{task_id}.json")
    require(git(attempt, "branch", "--show-current") == task["branch"] == config["branch"], "wrong publication branch")
    require(commit_id(attempt, "HEAD") == task["input_revision"], "worker committed or changed HEAD")
    result = read_json(attempt / ".agent" / f"final-{task_id}.json")
    validate_schema(result, read_json(Path(config["infrastructure"]) / "schemas/worker-result.schema.json"))
    require(result["task_id"] == task_id and result["bot_id"] == bot and
            result["base_source_hash"] == task["base_source_hash"], "worker result identity conflict")
    actual_paths = validate_worktree(attempt, bot)
    require(result["outcome"] == "READY_FOR_EVAL" and actual_paths, "no valid proposed edit")
    source = encode_source(attempt / "bots" / bot / "src")
    notes = encode_source(attempt / 'experiments' / bot)
    # Generated Python bytecode is ignored by Git too; retain it in private checkpoints, not publication.
    notes = {name: data for name, data in notes.items()
             if '__pycache__' not in Path(name).parts and Path(name).suffix not in ('.pyc', '.pyo')}
    return {'task_id': task_id, 'result': result, 'source': source, 'notes': notes}


def publish_attempt(config, attempt, owner=None):
    payload = candidate_payload(config, attempt)
    task_id = payload['task_id']
    # A second, trusted smoke check ignores any model claim that checks passed.
    source = payload['source']
    report = request(config, "check", {"task_id": task_id, "source": source})
    require(report["state"] == "PASSED", "trusted candidate check failed")
    # The arena owns the sole GitHub write credential and creates a clean commit itself.
    return request(config, 'publish', dict(payload, owner=owner))


def perform_task(config, task):
    task_id = task["task_id"]
    private = Path(config["attempts"]) / "supervisor" / task_id
    private.mkdir(parents=True, exist_ok=True, mode=0o700)
    outcome_file = private / "outcome.json"
    if outcome_file.exists():
        return read_json(outcome_file)
    attempt = Path(config["attempts"]) / task_id
    if attempt.exists():
        # Never replay an interrupted model call or ambiguous Git push.
        checkpoint(attempt, private / "checkpoint")
        outcome = {"task_id": task_id, "state": "PAUSED", "detail": "interrupted prior attempt; inspect preserved patch and remote tip"}
        atomic_json(outcome_file, outcome, 0o600)
        return outcome
    try:
        env = verify_subscription(config)
        attempt = make_attempt(config, task)
        final = attempt / ".agent" / f"final-{task_id}.json"
        prompt = (f"ROLE: bot_worker. Perform exactly one task from .agent/task.json. Follow AGENTS.md, "
                  f"read .agent/brief.md, .agent/entry.json, own NOTES.md and current source first. "
                  "The complete .agent/task.json is for targeted lookup, not a mandatory bulk dump. "
                  "On unchanged routine iterations, do not reread entire rules/API/SDK or all playbooks. "
                  f"Use bot-check --owner-config {config['owner_config_path']} "
                  "for trusted checks. Save one falsifiable hypothesis and compact notes. "
                  "Do not commit, push, start agents, wait for evaluations, or invoke official submissions. "
                  "Return the supplied worker-result schema and stop.")
        if config.get('provider', 'codex') == 'claude-code':
            from .claude import command
            args = command(config, attempt, prompt)
        else:
            args = [config["codex_executable"], "-a", "never", "exec", "--sandbox", "workspace-write", "--json",
                    "--add-dir", str(Path(config["root"]) / "inbox" / config["bot_id"]),
                    "-c", 'forced_login_method="chatgpt"', "-c", 'model_provider="openai"',
                    "--output-schema", str(Path(config["infrastructure"]) / "schemas/worker-result.schema.json"),
                    "-o", str(final), prompt]
            if config.get("model"):
                args[-1:-1] = ["--model", config["model"]]
        process = bounded_process(args, attempt, private, 1200, env=env)
        checkpoint(attempt, private / "checkpoint")
        claude_failure = None
        if config.get('provider', 'codex') == 'claude-code':
            from .claude import finish
            claude_failure = finish(private, process, final)
        if claude_failure:
            outcome = dict(claude_failure, task_id=task_id)
        elif process["returncode"] or process["timeout"] or not final.exists():
            outcome = dict(provider_failure(private, process), task_id=task_id)
        else:
            result = read_json(final)
            validate_schema(result, read_json(Path(config["infrastructure"]) / "schemas/worker-result.schema.json"))
            require(result["task_id"] == task_id and result["bot_id"] == config["bot_id"] and
                    result["base_source_hash"] == task["base_source_hash"], "malformed final identity")
            validated_result = result
            if result["outcome"] == "READY_FOR_EVAL":
                outcome = publish_attempt(config, attempt)
            else:
                outcome = {"task_id": task_id, "state": "NO_CHANGE" if result["outcome"] == "NO_CHANGE" else "PAUSED",
                           "detail": result.get("blocked_reason")}
    except (ArenaError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        if attempt.exists():
            checkpoint(attempt, private / "checkpoint")
        outcome = {"task_id": task_id, "state": "AUTH_REQUIRED" if "AUTH_REQUIRED" in str(exc) else "PAUSED", "detail": str(exc)}
    if "process" in locals():
        from .usage import usage_summary
        provider = config.get('provider', 'codex')
        prefix = 'claude' if provider == 'claude-code' else 'codex'
        if provider == 'claude-code':
            from .claude import usage_summary
        outcome["invocation"] = {"provider": provider, "binary_sha256": config[prefix + "_sha256"],
                                  **process, "raw_path": str(private),
                                  'efficiency_profile': 'brief-v1', 'usage': usage_summary(private / 'stdout.log'),
                                  "stdout_sha256": file_hash(private / "stdout.log"),
                                  "stderr_sha256": file_hash(private / "stderr.log")}
    if 'validated_result' in locals():
        outcome['worker_result'] = validated_result
    atomic_json(outcome_file, outcome, 0o600)
    return outcome


def serve(config_path):
    config = owner_config(config_path)
    config["owner_config_path"] = str(Path(config_path).resolve())
    Path(config["attempts"]).mkdir(parents=True, exist_ok=True, mode=0o700)
    with lock(Path(config["attempts"]) / "worker.lock"):
        while True:
            task_directory = Path(config["root"]) / "tasks" / config["bot_id"]
            for path in sorted(task_directory.glob("task-*.json")):
                receipt = Path(config["attempts"]) / "supervisor" / path.stem / "delivered.json"
                if receipt.exists():
                    continue
                status = request(config, "status", timeout=60)["worker"]
                if status["task_id"] != path.stem or status["state"] != "RUNNING":
                    continue
                # A kernel lock also enforces the global model limit independently of task messages.
                with lock(Path(config["root"]) / "model.lock", blocking=True):
                    outcome = perform_task(config, read_json(path))
                response = request(config, "worker-finished", outcome, timeout=120)
                atomic_json(receipt, response, 0o600)
            time.sleep(5)
