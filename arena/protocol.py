"""Mailbox payloads never contain commands or arbitrary host paths to execute."""
import base64
from pathlib import Path

from .common import identity, require, safe_relative, sha, tree_manifest


MAX_MESSAGE_BYTES = 2 * 1024 * 1024


def encode_source(directory):
    directory = Path(directory)
    files = tree_manifest(directory)
    return {name: base64.b64encode((directory / name).read_bytes()).decode() for name in files}


def decode_source(payload):
    require(isinstance(payload, dict) and 0 < len(payload) <= 128, "invalid source envelope")
    files = {}
    for name, encoded in payload.items():
        safe_relative(name)
        require(Path(name).suffix in (".cpp", ".cc", ".cxx", ".h", ".hpp"), "unapproved source file")
        require(isinstance(encoded, str) and len(encoded) <= 350000, "oversized encoded source")
        try:
            files[name] = base64.b64decode(encoded, validate=True)
        except ValueError as exc:
            raise ValueError("invalid source encoding") from exc
        require(len(files[name]) <= 256 * 1024, "oversized source file")
    require(sum(map(len, files.values())) <= 1024 * 1024, "oversized source tree")
    return files, identity({name: sha(data) for name, data in sorted(files.items())})


def save_source(files, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        target = directory / safe_relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
