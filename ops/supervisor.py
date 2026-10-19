#!/usr/bin/python3
"""Root-owned process supervision for hosts without systemd.

Each unit wrapper is a subreaper. It kills all adopted descendants before a
restart, including the separately-sessioned match/model processes.
"""
import argparse
import ctypes
import json
import os
from pathlib import Path
import pwd
import resource
import signal
import subprocess
import sys
import time

sys.path.insert(0, "/opt/battlecode")
from arena.common import atomic_json, lock, read_json, require
from arena.colab_sandbox import process_identity

ROOT = Path("/run/battlecode-supervisor")
SCRIPT = "/opt/battlecode/ops/supervisor.py"
UNITS = ("arena", "alpha", "beta")
stopping = False


def stop_signal(*_):
    global stopping
    stopping = True


def parent_death_signal():
    # Unit wrappers must clean up even if the managed top-level process is SIGKILLed.
    parent = os.getppid()
    ctypes.CDLL(None, use_errno=True).prctl(1, signal.SIGTERM, 0, 0, 0)
    if parent == 1 or os.getppid() != parent:
        os._exit(1)


def descendants(parent):
    rows = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
            rows[int(entry.name)] = int(fields[1])
        except (FileNotFoundError, ProcessLookupError):
            pass
    result = set()
    while True:
        added = {pid for pid, ppid in rows.items() if ppid in result | {parent}} - result
        if not added:
            return result
        result.update(added)


def terminate_children():
    # Includes orphans reparented here by PR_SET_CHILD_SUBREAPER.
    for pid in descendants(os.getpid()):
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if not pid:
                time.sleep(0.05)
        except ChildProcessError:
            return
    require(not descendants(os.getpid()), "old descendants remain; refusing another writer")


def unit(name):
    ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0)  # PR_SET_CHILD_SUBREAPER
    operator = name in ('arena', 'exploration')
    user = pwd.getpwnam('bc-arena' if operator else f'bc-{name}')
    args = ([sys.executable, '/opt/battlecode/ops/run-official-exploration.py'] if name == 'exploration' else
            ['/usr/local/bin/arena', 'serve'] if name == 'arena' else
            ['/usr/local/bin/arena', 'worker', '--owner-config', f'/etc/battlecode/{name}.json'])
    env = {"HOME": user.pw_dir, "USER": user.pw_name, "LOGNAME": user.pw_name,
           "PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8",
           "XDG_RUNTIME_DIR": "/run/battlecode-arena" if operator else f"{user.pw_dir}/.runtime"}
    restarts = 0
    history = []
    def identity():
        parent = os.getppid()
        if read_json('/etc/battlecode/arena.json').get('deployment', {}).get('mode') == 'blaxel':
            group = '/sys/fs/cgroup/battlecode-arena/service' if operator else f'/sys/fs/cgroup/battlecode-workers/{name}'
            Path(group, 'cgroup.procs').write_text(str(os.getpid()))
        if not operator:
            resource.setrlimit(resource.RLIMIT_FSIZE, (256*1024**2, 256*1024**2))
            resource.setrlimit(resource.RLIMIT_NOFILE, (512,512))
            resource.setrlimit(resource.RLIMIT_CORE, (0,0))
        os.setgroups(os.getgrouplist(user.pw_name, user.pw_gid))
        os.setgid(user.pw_gid)
        os.setuid(user.pw_uid)
        ctypes.CDLL(None, use_errno=True).prctl(1, signal.SIGKILL, 0, 0, 0)
        if os.getppid() != parent:
            os._exit(1)
    while not stopping:
        with (ROOT / f"{name}.log").open("ab") as log:
            child = subprocess.Popen(args, env=env, cwd="/opt/battlecode", preexec_fn=identity,
                                     umask=0o027, start_new_session=True, stdout=log, stderr=log)
            started = time.monotonic()
            while not stopping and child.poll() is None:
                atomic_json(ROOT / f"{name}.json", {"unit": name, "identity": process_identity(child.pid),
                            "wrapper": process_identity(os.getpid()), "heartbeat": time.time(),
                            "restarts": restarts, "history": history[-20:]}, 0o600)
                if name == 'arena' and time.monotonic() - started > 1800:
                    try:
                        heartbeat = read_json('/srv/battlecode/public/status.json').get('heartbeat') or 0
                    except (OSError, ValueError):
                        heartbeat = 0
                    if time.time() - heartbeat > 1800:
                        atomic_json(ROOT / 'watchdog.json', {'unit': name, 'at': time.time(),
                                    'reason': 'scheduler heartbeat stale for over 30 minutes',
                                    'action': 'terminate descendants and restart; preserve attempts'}, 0o600)
                        break
                time.sleep(1)
            history.append({"pid": child.pid, "exit": child.poll(), "at": time.time()})
            terminate_children()
            child.wait()
        if stopping:
            break
        restarts += 1
        # No rapid infinite crash loop: retain evidence and stop this wrapper.
        if len(history) >= 5 and history[-1]["at"] - history[-5]["at"] < 60:
            raise RuntimeError(f"{name}: start-rate limit; inspect {ROOT / (name + '.log')}")
        time.sleep(5)


def serve():
    ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0)
    with lock(ROOT / "supervisor.lock"):
        children = []
        try:
            for name in UNITS:
                children.append(subprocess.Popen([sys.executable, SCRIPT, "unit", "--name", name],
                                                  start_new_session=True, preexec_fn=parent_death_signal))
            atomic_json(ROOT / "supervisor.json", {"identity": process_identity(os.getpid()),
                        "started": time.time(), "reboot_persistence_verified": False}, 0o600)
            while not stopping:
                require(all(child.poll() is None for child in children), "unit wrapper failed; inspect private logs")
                time.sleep(1)
        finally:
            for child in children:
                if child.poll() is None:
                    child.send_signal(signal.SIGTERM)
            for child in children:
                child.wait(timeout=15)
            terminate_children()


def alive(record):
    return record and process_identity(record["pid"]) == record


def main():
    global ROOT, UNITS
    require(os.geteuid() == 0, "administrator command required")
    config = read_json('/etc/battlecode/arena.json')
    mode = config.get('deployment', {}).get('mode')
    require(mode in ('temporary-colab', 'blaxel'), 'non-systemd deployment profile required')
    UNITS = ('arena', *config['workers'], *(['exploration'] if config['official']['challenges'] else []))
    if mode == 'blaxel':
        ROOT = Path('/var/lib/battlecode-volume/supervisor')
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["start", "serve", "unit", "status", "stop", "restart"])
    parser.add_argument("--name", choices=UNITS)
    args = parser.parse_args()
    ROOT.mkdir(mode=0o700, exist_ok=True)
    signal.signal(signal.SIGTERM, stop_signal)
    signal.signal(signal.SIGINT, stop_signal)
    record = read_json(ROOT / "supervisor.json") if (ROOT / "supervisor.json").exists() else {}
    running = alive(record.get("identity"))
    if args.command in ("stop", "restart") and running:
        os.kill(record["identity"]["pid"], signal.SIGTERM)
        deadline = time.monotonic() + 25
        while alive(record["identity"]) and time.monotonic() < deadline:
            # A detached, fully reaped supervisor can linger as a zombie under Colab PID1.
            state = Path(f"/proc/{record['identity']['pid']}/stat")
            if state.exists() and state.read_text().rsplit(")", 1)[1].split()[0] == "Z":
                break
            time.sleep(0.2)
        require(not any(alive(read_json(ROOT / f"{name}.json").get("identity")) for name in UNITS
                        if (ROOT / f"{name}.json").exists()), "service did not stop")
        running = False
    if args.command in ("start", "restart"):
        if not running:
            with (ROOT / "supervisor.log").open("ab") as log:
                child = subprocess.Popen([sys.executable, SCRIPT, "serve"], stdin=subprocess.DEVNULL,
                                         stdout=log, stderr=log, start_new_session=True)
            print(json.dumps({"started_pid": child.pid, "temporary": True, "reboot_persistence_verified": False}))
        else:
            print(json.dumps({"already_running": True}))
    elif args.command == "serve":
        serve()
    elif args.command == "unit":
        unit(args.name)
    else:
        print(json.dumps({"running": running, "supervisor": record,
                          "units": {name: read_json(ROOT / f"{name}.json") for name in UNITS
                                    if (ROOT / f"{name}.json").exists()}}, indent=2))


if __name__ == "__main__":
    main()
