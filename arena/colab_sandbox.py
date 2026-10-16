"""Explicit temporary-Colab backend; never an automatic Podman fallback.

Namespaces/rlimits are kernel-enforced. Aggregate RSS, task count and writable
disk have a 100-ms watchdog, NOT cgroup hard limits; that limitation is recorded.
No host home, credential, network, socket or writable toolchain is mounted.
"""
from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess
import time

from .common import atomic_json, clean_environment, file_hash, require


LIMITS = {"rss_bytes": 2 * 1024**3, "disk_bytes": 1024**3, "tasks": 128,
          "file_bytes": 256 * 1024**2, "poll_seconds": 0.1, "cpu_cores": 1}


def process_identity(pid):
    try:
        # comm may contain spaces; starttime is field 22 after the closing ')'.
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return {"pid": pid, "start_ticks": int(fields[19]), "uid": Path(f"/proc/{pid}").stat().st_uid}
    except (FileNotFoundError, ProcessLookupError):
        return None


def group_usage(group):
    rss, tasks, cpu = 0, 0, 0.0
    tick = os.sysconf("SC_CLK_TCK")
    for path in Path("/proc").iterdir():
        if not path.name.isdigit():
            continue
        try:
            fields = (path / "stat").read_text().rsplit(")", 1)[1].split()
            # Both session and process group are accepted: bwrap starts a new session.
            if int(fields[2]) != group and int(fields[3]) != group:
                continue
            rss += int(fields[21]) * os.sysconf("SC_PAGE_SIZE")
            tasks += int(fields[17])
            cpu += (int(fields[11]) + int(fields[12])) / tick
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            pass
    return rss, tasks, cpu


def disk_usage(paths):
    total = 0
    for root in paths:
        for path in Path(root).rglob("*"):
            try:
                if path.is_file() and not path.is_symlink():
                    total += path.stat().st_size
            except FileNotFoundError:
                pass
    return total


def arguments(toolchain, project, output, command):
    cpu = min(os.sched_getaffinity(0))
    return ["taskset", "--cpu-list", str(cpu), "prlimit", "--nproc=128:128", "--nofile=512:512",
            "--fsize=268435456:268435456", "--core=0:0", "--cpu=600:600", "--",
            "bwrap", "--unshare-all", "--die-with-parent", "--cap-drop", "ALL", "--clearenv",
            "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib64", "/lib64", "--dir", "/proc", "--dev", "/dev",
            "--bind", str(Path(project).resolve() / ".sandbox-tmp"), "/tmp",
            "--dir", "/home/bc-arena",
            "--ro-bind", str(toolchain), "/toolchain",
            "--dir", "/home/bc-arena/.cache", "--ro-bind", str(Path(toolchain) / "cache"),
            "/home/bc-arena/.cache/cambc", "--bind", str(Path(project).resolve()), "/work",
            "--bind", str(Path(output).resolve()), "/output", "--chdir", "/work",
            "--setenv", "HOME", "/home/bc-arena", "--setenv", "USER", "bc-arena",
            "--setenv", "PATH", "/toolchain/bin:/usr/bin:/bin", "--setenv", "LANG", "C.UTF-8",
            "--setenv", "DOTNET_PROCESSOR_COUNT", "1", "--setenv", "CMAKE_BUILD_PARALLEL_LEVEL", "1",
            "--remount-ro", "/",
            "--", *command]


def execute(toolchain, project, output, command, timeout):
    output = Path(output)
    (Path(project) / ".sandbox-tmp").mkdir(exist_ok=True)
    args = arguments(toolchain, project, output, command)
    started = time.time()
    reason = None
    peak_rss = peak_tasks = peak_disk = 0
    cpu = 0.0
    with (output / "stdout.log").open("wb") as out, (output / "stderr.log").open("wb") as err:
        child = subprocess.Popen(args, cwd=project, env=clean_environment(), stdout=out, stderr=err,
                                 start_new_session=True)
        atomic_json(output / "process.json", {**process_identity(child.pid), "started": started, "argv": args})
        try:
            scan_at = 0
            while child.poll() is None:
                rss, tasks, cpu = group_usage(child.pid)
                peak_rss, peak_tasks = max(peak_rss, rss), max(peak_tasks, tasks)
                if time.monotonic() >= scan_at:
                    peak_disk = max(peak_disk, disk_usage((project, output)))
                    scan_at = time.monotonic() + 0.5
                if time.time() - started > timeout:
                    reason = "wall_timeout"
                elif rss > LIMITS["rss_bytes"]:
                    reason = "aggregate_rss_watchdog"
                elif tasks > LIMITS["tasks"]:
                    reason = "aggregate_tasks_watchdog"
                elif peak_disk > LIMITS["disk_bytes"]:
                    reason = "writable_disk_watchdog"
                if reason:
                    break
                time.sleep(LIMITS["poll_seconds"])
        finally:
            # Killing bwrap's PID-namespace init kills ALL sandbox descendants,
            # including programs which make their own session/process group.
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            code = child.wait()
    result = {"returncode": code, "timeout": reason == "wall_timeout", "limit_reason": reason,
              "started": started, "finished": time.time(), "elapsed_seconds": time.time() - started,
              "resources": {"peak_sampled_rss_bytes": peak_rss, "peak_sampled_tasks": peak_tasks,
                            "peak_sampled_disk_bytes": peak_disk, "last_sampled_live_cpu_seconds": cpu},
              "isolation": "bubblewrap-watchdog-v1", "limits": LIMITS,
              "limitations": ["aggregate limits are sampled, not cgroup-hard", "ephemeral Colab storage"]}
    atomic_json(output / "process-result.json", result)
    return result


def validate(config, lock):
    require(config.get("deployment", {}).get("mode") == "temporary-colab", "Colab backend requires explicit opt-in")
    root = Path(lock["toolchain"])
    require(root == Path("/opt/battlecode-toolchain") and root.stat().st_uid == 0 and
            not root.stat().st_mode & 0o022, "root-owned read-only toolchain required")
    for path, digest in lock["tool_hashes"].items():
        candidate = root / path
        require(candidate.resolve().is_relative_to(root) and file_hash(candidate) == digest,
                "pinned Colab tool changed")
    require(file_hash(root / "bin/cambc") == lock["engine_sha256"], "engine binary mismatch")
