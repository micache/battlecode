"""Bounded trusted toolchain download on an authorized Colab host. Runs no bot."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path("/content/battlecode-bootstrap")
REPOSITORY = Path("/content/battlecode")


def main():
    ROOT.mkdir(exist_ok=True)
    state = {"started": time.time(), "steps": []}
    steps = [
        ["apt-get", "update", "-qq"],
        ["apt-get", "install", "-y", "python3.12-venv", "bubblewrap", "build-essential", "cmake", "curl", "xz-utils", "unzip"],
        ["/usr/bin/python3.12", "-m", "venv", str(ROOT / "tool-venv312")],
        [str(ROOT / "tool-venv312/bin/python"), "-m", "pip", "install", "--only-binary=:all:", "--require-hashes",
         "-r", str(REPOSITORY / "ops/engine-requirements.txt")],
        [str(ROOT / "tool-venv312/bin/cambc"), "--version"],
        [str(ROOT / "tool-venv312/bin/cambc"), "init", "--yes", str(ROOT / "official-project")],
    ]
    try:
        for index, args in enumerate(steps):
            state["current"] = args
            (ROOT / "bootstrap-state.json").write_text(json.dumps(state, indent=2))
            with (ROOT / f"bootstrap-{index}.log").open("wb") as log:
                process = subprocess.run(args, cwd=REPOSITORY, stdout=log, stderr=subprocess.STDOUT,
                                         timeout=600, env=dict(os.environ, DEBIAN_FRONTEND="noninteractive"))
            state["steps"].append({"argv": args, "exit_code": process.returncode, "log": str(log.name)})
            if process.returncode:
                raise RuntimeError(f"bootstrap step {index} failed; inspect {log.name}")
        state["status"] = "COMPLETE"
    except Exception as exc:
        state.update(status="BLOCKED", error=str(exc))
    state["finished"] = time.time()
    (ROOT / "bootstrap-state.json").write_text(json.dumps(state, indent=2))
    print(json.dumps(state, indent=2))
    return int(state["status"] != "COMPLETE")


if __name__ == "__main__":
    sys.exit(main())
