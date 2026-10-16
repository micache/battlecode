#!/usr/bin/env python3
"""Save actual local check output without claiming any real-engine acceptance."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from arena.common import atomic_json, atomic_bytes, file_hash, tree_manifest


def main():
    checks = [
        ("unit-tests", [sys.executable, "-W", "error::ResourceWarning", "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("python-compile", [sys.executable, "-m", "compileall", "-q", "arena", "ops", "tests"]),
        ("shell-syntax", ["bash", "-n", "ops/install.sh", "ops/prepare-engine.sh", "ops/as-arena.sh"]),
        ("arena-help", [sys.executable, "-m", "arena.cli", "--help"]),
        ("client-help", [sys.executable, "-m", "arena.client", "--help"]),
        ("systemd-verify", ["systemd-analyze", "verify", "ops/systemd/battlecode-arena.service",
                            "ops/systemd/battlecode-worker@alpha.service", "ops/systemd/battlecode-worker@beta.service",
                            "ops/systemd/battlecode-backup.service", "ops/systemd/battlecode-backup.timer"]),
    ]
    results = []
    env = dict(os.environ, ARENA_TEST_EVIDENCE_DIR=str(ROOT / "evidence/validation"))
    for name, args in checks:
        process = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=60, env=env)
        output = process.stdout + process.stderr
        path = ROOT / "evidence/validation" / (name + ".txt")
        atomic_bytes(path, output)
        blocked = name == "systemd-verify" and b"Operation not permitted" in output
        status = "PASSED" if process.returncode == 0 else "BLOCKED" if blocked else "FAILED"
        results.append({"name": name, "command": args, "exit_code": process.returncode,
                        "status": status, "report_path": str(path.relative_to(ROOT)), "sha256": file_hash(path)})
        print(f"{name}: {status}")
    manifest = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "python": sys.version, "checks": results,
                "engine_tests": "NOT RUN: cambc/SDK/maps and functional rootless container runtime unavailable",
                "host_acceptance": "NOT RUN: SSH blocked before connection; no owner logins",
                "source_hashes": {str(path.relative_to(ROOT)): file_hash(path)
                                  for base in ("arena", "ops", "tests", "schemas", "config")
                                  for path in (ROOT / base).rglob("*") if path.is_file() and "__pycache__" not in path.parts}}
    atomic_json(ROOT / "evidence/local-validation.json", manifest)
    return int(any(row["status"] == "FAILED" for row in results))


if __name__ == "__main__":
    sys.exit(main())
