"""Official source-project adapter. Compiled-input mode is deliberately not inferred."""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import time

from .common import (ArenaError, atomic_json, bounded_process, file_hash, identity, read_json,
                     require, run, safe_relative, tree_hash, tree_manifest)


PROFILE = {
    "winning_submitted_gems": 1000, "max_rounds": 2000,
    "draft_memory_bytes": 1024, "shared_memory_bytes": 8,
    "base_fuel_per_turn": 100000,
    "fuel_multipliers": {"cpp": 1, "rust": 1, "ocaml": 5, "python": 25},
    "first_draft_turn_fuel_multiplier": 10, "first_champion_turn_fuel_multiplier": 2,
}


def pointer(document, path):
    require(isinstance(path, str) and (path == "" or path.startswith("/")), "JSON pointer required")
    for key in path.split("/")[1:]:
        key = key.replace("~1", "/").replace("~0", "~")
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def validate_contract(contract, engine_hash):
    require(contract.get("protocol_version") == 1 and contract.get("engine_sha256") == engine_hash,
            "parser/engine identity mismatch")
    require(contract.get("reviewed_by") and contract.get("fixture_sha256") and
            contract.get("replay_agreement_verified") is True, "real parser fixture review required")
    require(set(contract["winner_values"].values()) == {"A", "B"}, "absolute A/B mapping required")
    require(contract.get("winner_pointer") is not None, "authoritative outcome pointer required")
    mode = contract.get("completion_mode", "field_equals")
    require(mode in ("field_equals", "final_statistics_contract"), "unknown completion contract")
    if mode == "field_equals":
        require(contract.get("complete_pointer") is not None and contract.get("complete_value") is not None,
                "explicit authoritative completion field/value required")


def normalize_result(artifacts, contract, engine_hash):
    """Unknown output is INFRA_ERROR, never a guessed loss or a successful exit."""
    output = Path(artifacts)
    process = read_json(output / "process-result.json")
    result = {"protocol_version": 1, "state": "INFRA_ERROR", "completed": False,
              "winner": None, "terminal_reason": None, "metrics": {},
              "bot_faults": None, "fuel_suspensions": None, "detail": None}
    if process["timeout"]:
        return dict(result, state="TIMEOUT", detail="arena wall timeout")
    if contract is None:
        return dict(result, detail="statistics parser has no reviewed real-engine fixture")
    try:
        validate_contract(contract, engine_hash)
        # Only an explicitly reviewed diagnostic may identify a trap or forfeit.
        logs = "\n".join((output / name).read_text(errors="replace")[-65536:]
                         for name in ("stdout.log", "stderr.log") if (output / name).exists())
        faults = sum(len(re.findall(pattern, logs)) for pattern in contract.get("bot_fault_patterns", []))
        stats_path = output / "final.json"
        if not stats_path.exists():
            truncated = any(re.search(p, logs) for p in contract.get("truncated_patterns", []))
            return dict(result, state="BOT_FAULT" if faults else "TRUNCATED" if truncated else "INFRA_ERROR", bot_faults=faults,
                        detail="missing authoritative final statistics")
        stats = read_json(stats_path)
        completed = (True if contract.get("completion_mode") == "final_statistics_contract" else
                     pointer(stats, contract["complete_pointer"]) == contract["complete_value"])
        if not completed:
            return dict(result, state="BOT_FAULT" if faults else "TRUNCATED", bot_faults=faults,
                        detail="engine did not report authoritative completion")
        require(process["returncode"] == 0, "runner failed despite completion statistics")
        winner = contract["winner_values"].get(str(pointer(stats, contract["winner_pointer"])))
        require(winner in ("A", "B"), "unknown outcome/draw: rules discrepancy")
        replays = list(output.rglob("*.repl26a"))
        require(replays and all(p.stat().st_size > 0 for p in replays), "completed game missing replay")
        metrics = {}
        for name, path in contract.get("metric_pointers", {}).items():
            try:
                metrics[name] = {"available": True, "value": pointer(stats, path)}
            except (KeyError, IndexError, TypeError, ValueError):
                metrics[name] = {"available": False, "value": None}
        reason = pointer(stats, contract["reason_pointer"]) if contract.get("reason_pointer") else None
        suspensions = None
        if contract.get("fuel_suspension_patterns"):
            suspensions = sum(len(re.findall(p, logs)) for p in contract["fuel_suspension_patterns"])
        return dict(result, state="COMPLETED", completed=True, winner=winner, terminal_reason=reason,
                    bot_faults=faults if contract.get("fault_detection_verified") else None,
                    fuel_suspensions=suspensions, metrics=metrics)
    except (ArenaError, KeyError, TypeError, ValueError, IndexError, json.JSONDecodeError) as exc:
        return dict(result, detail=f"unrecognized engine result: {exc}")


def seal_artifacts(directory, job_id, attempt, result):
    directory = Path(directory)
    atomic_json(directory / "normalized.json", result)
    manifest = {"protocol_version": 1, "job_id": job_id, "attempt": attempt,
                "result": result, "files": tree_manifest(directory)}
    manifest["files"].pop("completion.json", None)
    atomic_json(directory / "completion.json", manifest)
    return manifest


def verify_artifacts(directory, job_id, attempt):
    directory = Path(directory)
    manifest = read_json(directory / "completion.json")
    require(manifest["job_id"] == job_id and manifest["attempt"] == attempt, "artifact attribution mismatch")
    actual = tree_manifest(directory)
    actual.pop("completion.json", None)
    require(actual == manifest["files"], "artifact checksum mismatch")
    require(read_json(directory / "normalized.json") == manifest["result"], "normalized result mismatch")
    return manifest["result"]


class OfficialEngine:
    def __init__(self, config):
        self.config = config
        self.lock = read_json(config["engine_lock"])
        self.lock_hash = identity(self.lock)
        require(self.lock["engine_sha256"] == config["engine"]["binary_sha256"] and
                self.lock["version"] == config["engine"]["version"], "engine pin mismatch")
        require(re.fullmatch(r"sha256:[a-f0-9]{64}", self.lock["image_id"]), "immutable local OCI image required")
        require(self.lock.get("compiler_versions") and self.lock.get("recipe_sha256"), "incomplete toolchain lock")
        require(tree_hash(self.lock["project_template"]) == self.lock["template_sha256"], "SDK/template changed")
        self.contract = read_json(config["parser_contract"]) if Path(config["parser_contract"]).exists() else None
        if self.contract:
            fixture = Path(self.contract["fixture_path"]).resolve()
            require(fixture.is_relative_to(Path(config["root"]).resolve() / "matches") and
                    fixture.name == "final.json" and file_hash(fixture) == self.contract["fixture_sha256"],
                    "parser contract must reference a saved matching real-engine statistics fixture")
            validate_contract(self.contract, self.lock["engine_sha256"])

    def container_args(self, project, output, name):
        require(Path(project).is_dir() and Path(output).is_dir(), "mounts must exist")
        return ["podman", "--cgroup-manager=cgroupfs", "run", "--name", name, "--pull=never", "--network=none", "--read-only",
                "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=128", "--memory=2g",
                "--cpus=1", "--ulimit=fsize=1073741824:1073741824", "--ulimit=nofile=512:512",
                "--tmpfs=/tmp:rw,size=256m", "--volume", f"{Path(project).resolve()}:/work:rw",
                "--volume", f"{Path(output).resolve()}:/output:rw", "--workdir=/work",
                self.lock["image_id"], "cambc"]

    def execute(self, project, output, arguments, timeout, name):
        args = self.container_args(project, output, name) + arguments
        try:
            process = bounded_process(args, project, output, timeout)
        finally:
            # Systemd kills the service cgroup; this also removes any surviving OCI container.
            import subprocess
            subprocess.run(["podman", "--cgroup-manager=cgroupfs", "rm", "-f", name], capture_output=True, timeout=30)
        atomic_json(Path(output) / "process-result.json", process)
        return process

    def prepare_project(self, destination, sources):
        require(not Path(destination).exists(), "attempt workspace already exists")
        shutil.copytree(self.lock["project_template"], destination)
        for side, source in sources.items():
            require(side in ("side-a", "side-b"), "invalid trusted recipe slot")
            target = Path(destination) / "bots" / side / "src"
            require(target.is_dir() and not target.is_symlink(), "official C++ template slot missing")
            shutil.rmtree(target)
            shutil.copytree(source, target)

    def prepare_bot(self, snapshot, revision_id):
        require(tree_hash(Path(snapshot) / "src"), "missing source")
        source_hash = tree_hash(Path(snapshot) / "src")
        build_id = identity({"source": source_hash, "language": "cpp", "engine_lock": self.lock_hash,
                             "infrastructure_commit": self.config["infrastructure_commit"],
                             "recipe": "official-source-v1"})
        directory = Path(self.config["root"]) / "builds" / build_id
        if (directory / "build.json").exists():
            saved = read_json(directory / "build.json")
            require(file_hash(directory / "output/bot.wasm") == saved["wasm_sha256"], "cached build changed")
            return saved
        directory.mkdir(parents=True, exist_ok=True)
        # Interrupted work is preserved; each preparation has a distinct attempt directory.
        work = directory / f"prepare-{time.time_ns()}"
        self.prepare_project(work, {"side-a": Path(snapshot) / "src"})
        output = directory / "output"
        output.mkdir(exist_ok=True)
        process = self.execute(work, output, ["build", "side-a", "--output", "/output/bot.wasm"],
                               self.config["limits"]["build_timeout_seconds"], f"bc-build-{build_id[:24]}")
        require(not process["timeout"] and process["returncode"] == 0 and (output / "bot.wasm").exists(),
                f"BUILD_FAILED: {output}")
        saved = {"build_id": build_id, "source_hash": source_hash, "revision_id": revision_id,
                 "lock_hash": self.lock_hash, "wasm_sha256": file_hash(output / "bot.wasm"),
                 "snapshot": str(snapshot), "artifact": str(output / "bot.wasm"),
                 "mode": "official-source-project; run may recompile; no compiled-input parity claim"}
        atomic_json(directory / "build.json", saved)
        return saved

    def run_match(self, spec, output):
        require(spec["engine_lock_hash"] == self.lock_hash, "match engine changed")
        require(file_hash(spec["map_path"]) == spec["map_hash"], "frozen map changed")
        for side in ("a", "b"):
            require(tree_hash(Path(spec[f"{side}_snapshot"]) / "src") == spec[f"{side}_source_hash"],
                    "frozen source changed")
        output = Path(output)
        output.mkdir(parents=True, exist_ok=True)
        project = output / "project"
        self.prepare_project(project, {"side-a": Path(spec["a_snapshot"]) / "src",
                                       "side-b": Path(spec["b_snapshot"]) / "src"})
        shutil.copyfile(spec["map_path"], project / "frozen.map26a")
        artifacts = output / "artifacts"
        artifacts.mkdir()
        self.execute(project, artifacts, ["run", "side-a", "side-b", "--map", "/work/frozen.map26a",
                                         "--out-dir", "/output", "--statistics", "/output/final.json"],
                     self.config["limits"]["match_timeout_seconds"], f"bc-match-{spec['job_id'][:24]}")
        return normalize_result(artifacts, self.contract, self.lock["engine_sha256"])

    def recover_containers(self):
        names = run(["podman", "--cgroup-manager=cgroupfs", "ps", "-a", "--format", "{{.Names}}"])
        for name in names.splitlines():
            if re.fullmatch(r"bc-(build|match)-[a-f0-9]{24}", name):
                run(["podman", "--cgroup-manager=cgroupfs", "rm", "-f", name])
