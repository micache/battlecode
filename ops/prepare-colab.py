#!/usr/bin/python3
"""Trusted, administrator-only bootstrap of the explicitly temporary pilot.

Run remote_bootstrap.py first. This copies only public SDK/compiler assets, never
an owner home or credential. It does not start services or authenticate owners.
"""
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import sys
import time

sys.path.insert(0, "/opt/battlecode")
from arena.common import atomic_bytes, atomic_json, file_hash, read_json, require, tree_hash, tree_manifest

BOOT = Path("/content/battlecode-bootstrap")
TOOLS = Path("/opt/battlecode-toolchain")
GITHUB_HOST = "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl\n"


def main():
    require(os.geteuid() == 0, "administrator required")
    config = read_json("/etc/battlecode/arena.json")
    require(config.get("deployment", {}).get("mode") == "temporary-colab", "explicit temporary installation required")
    require(not TOOLS.exists() and not Path(config["engine_lock"]).exists(), "preserve existing toolchain; do not overwrite")
    TOOLS.mkdir(mode=0o755)
    (TOOLS / "bin").mkdir()
    binaries = [p for p in (BOOT / "tool-venv312").rglob("*") if p.is_file() and p.stat().st_size == 95129344
                and file_hash(p) == config["engine"]["binary_sha256"]]
    require(len(binaries) == 1, "pinned official engine unavailable")
    shutil.copy2(binaries[0], TOOLS / "bin/cambc")
    (TOOLS / "bin/cambc").chmod(0o755)
    shutil.copytree("/root/.cache/cambc", TOOLS / "cache", symlinks=True)
    # Remove no user data: the new template is copied without generated build files.
    template = Path("/srv/battlecode/repos/official-template")
    template.mkdir()
    official = BOOT / "official-project"
    shutil.copytree(official / "sdk", template / "sdk")
    shutil.copytree(official / "cmake", template / "cmake")
    shutil.copyfile(official / "cambc.toml", template / "cambc.toml")
    for side in ("side-a", "side-b"):
        shutil.copytree(official / "bots/starter-cpp/src", template / "bots" / side / "src")
    maps = Path(config["maps"])
    maps.mkdir(parents=True)
    for item in read_json(config["map_manifest"])["maps"]:
        src = official / "maps" / (item["name"] + ".map26a")
        require(file_hash(src) == item["sha256"], "public map pool changed; explicit review required")
        shutil.copyfile(src, maps / src.name)
    tool_paths = ["bin/cambc", "cache/wasi-sdk-33/bin/clang-22", "cache/cmake-3.31.8-linux-x86_64/bin/cmake",
                  "cache/ninja-1.12.1-linux-x86_64/ninja"]
    hashes = {name: file_hash(TOOLS / name) for name in tool_paths}
    record = {}
    for name, relative in zip(("cambc", "clang", "cmake", "ninja"), tool_paths):
        result = subprocess.run([str(TOOLS / relative), "--version"], check=True, capture_output=True, text=True)
        record[name] = result.stdout.strip()
    lock = {"protocol_version": 1, "version": "2.1.6", "engine_sha256": config["engine"]["binary_sha256"],
            "isolation": "bubblewrap-watchdog-v1", "toolchain": str(TOOLS), "tool_hashes": hashes,
            "project_template": str(template), "template_sha256": tree_hash(template),
            "sdk_cpp_sha256": file_hash(template / "sdk/cpp/cambc.h"), "compiler_versions": record,
            "language": "cpp", "effective_profile": None,
            "recipe_sha256": file_hash("/opt/battlecode/arena/colab_sandbox.py"), "created": time.time(),
            "reboot_persistence_verified": False, "aggregate_limits": "sampled watchdog, not cgroup-hard"}
    # Protect all trusted toolchain bytes, including symlink targets copied inside this tree.
    for path in [TOOLS, *TOOLS.rglob("*")]:
        if not path.is_symlink():
            path.chmod((path.stat().st_mode & 0o555) | 0o444 if path.is_file() else 0o555)
    atomic_json(config["engine_lock"], lock, 0o644)
    arena = pwd.getpwnam("bc-arena")
    os.chown(config["engine_lock"], arena.pw_uid, arena.pw_gid)
    # Official public GitHub host key, checked against the published fingerprint.
    known = Path(arena.pw_dir) / ".ssh/known_hosts"
    require(not known.exists(), "preserve existing host trust configuration")
    atomic_bytes(known, GITHUB_HOST.encode(), 0o600)
    os.chown(known, arena.pw_uid, arena.pw_gid)
    for bot in ("alpha", "beta"):
        path = Path(f"/etc/battlecode/{bot}.json")
        owner = read_json(path)
        owner.update(codex_executable="/usr/local/bin/codex", codex_sha256=file_hash("/usr/local/bin/codex"))
        atomic_json(path, owner, 0o644)
        user = pwd.getpwnam(f"bc-{bot}")
        runtime = Path(user.pw_dir) / ".runtime"
        runtime.mkdir(mode=0o700, exist_ok=True)
        os.chown(runtime, user.pw_uid, user.pw_gid)
    atomic_json("/srv/battlecode/acceptance/toolchain-bootstrap.json", {"lock": lock, "template_files": tree_manifest(template)}, 0o644)
    print(json.dumps({"prepared": True, "engine_sha256": hashes["bin/cambc"], "record": record,
                      "reboot_persistence_verified": False}, indent=2))


if __name__ == "__main__":
    main()
