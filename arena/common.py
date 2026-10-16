from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import tempfile
import time
import uuid


class ArenaError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ArenaError(message)


def slug(value):
    require(isinstance(value, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", value), "invalid slug")
    return value


def sha(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def identity(value):
    return sha(canonical(value))


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    with Path(path).open() as stream:
        return json.load(stream)


def atomic_bytes(path, data, mode=0o640):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        sync_directory(path.parent)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def sync_directory(path):
    fd = os.open(path, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_json(path, data, mode=0o640):
    atomic_bytes(path, canonical(data) + b"\n", mode)


def safe_relative(value):
    path = PurePosixPath(value)
    require(value and not path.is_absolute() and ".." not in path.parts and "\\" not in value
            and str(path) == value and not any(ord(c) < 32 for c in value), "unsafe relative path")
    return path


def tree_manifest(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), f"missing/unsafe tree: {root}")
    result = {}
    for path in sorted(root.rglob("*")):
        require(not path.is_symlink(), f"symlink forbidden: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = file_hash(path)
        else:
            require(path.is_dir(), "nonregular tree entry")
    return result


def tree_hash(root):
    return identity(tree_manifest(root))


def fresh_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex}"


@contextlib.contextmanager
def lock(path, blocking=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        except BlockingIOError as exc:
            raise ArenaError(f"single writer already active: {path}") from exc
        yield


def clean_environment(owner=False):
    # An allowlist, not a blacklist of today's token variable names.
    keys = ["PATH", "LANG", "LC_ALL", "TZ", "XDG_RUNTIME_DIR"]
    if owner:
        keys += ["HOME", "USER", "LOGNAME", "SSH_AUTH_SOCK"]
    env = {key: os.environ[key] for key in keys if key in os.environ}
    env.update({"GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1"})
    return env


def run(args, cwd=None, timeout=60, env=None):
    try:
        proc = subprocess.run([str(x) for x in args], cwd=cwd, env=env or clean_environment(True),
                              capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ArenaError(f"command unavailable/timed out: {args[0]}: {type(exc).__name__}") from exc
    require(proc.returncode == 0, f"command failed ({proc.returncode}): {args[0]}: "
            + proc.stderr.decode(errors="replace")[-1500:])
    return proc.stdout.decode().strip()


def bounded_process(args, cwd, output, timeout, env=None):
    """A whole process group is killed on timeout; raw output is always retained."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    started = time.time()
    with (output / "stdout.log").open("wb") as out, (output / "stderr.log").open("wb") as err:
        process = subprocess.Popen([str(x) for x in args], cwd=cwd, env=env or clean_environment(),
                                   stdout=out, stderr=err, start_new_session=True)
        atomic_json(output / "process.json", {"pid": process.pid, "started": started,
                                             "argv": [str(x) for x in args]})
        timed_out = False
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                code = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                code = process.wait()
            # The leader may exit on TERM while a grandchild ignores it.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        finally:
            # Reap stragglers in the task's group even when its leader exits normally.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    return {"returncode": code, "timeout": timed_out, "started": started,
            "finished": time.time(), "elapsed_seconds": time.time() - started}


def validate_schema(value, schema, location="$"):
    """Deliberately small validator for the checked-in protocol schemas (no remote refs)."""
    types = {"object": dict, "array": list, "string": str, "integer": int,
             "number": (int, float), "boolean": bool, "null": type(None)}
    expected = schema.get("type")
    if expected:
        names = expected if isinstance(expected, list) else [expected]
        require(any(isinstance(value, types[name]) and not
                    (isinstance(value, bool) and name in ("integer", "number")) for name in names),
                f"{location}: wrong type")
    if "enum" in schema:
        require(value in schema["enum"], f"{location}: invalid enum")
    if isinstance(value, str):
        require(len(value) >= schema.get("minLength", 0), f"{location}: too short")
        if "pattern" in schema:
            require(re.search(schema["pattern"], value), f"{location}: invalid pattern")
    if isinstance(value, dict):
        require(set(schema.get("required", [])) <= value.keys(), f"{location}: missing fields")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            require(value.keys() <= properties.keys(), f"{location}: unexpected fields")
        for key, sub in properties.items():
            if key in value:
                validate_schema(value[key], sub, f"{location}.{key}")
    if isinstance(value, list):
        require(len(value) >= schema.get("minItems", 0), f"{location}: too few items")
        for index, item in enumerate(value):
            validate_schema(item, schema.get("items", {}), f"{location}[{index}]")
