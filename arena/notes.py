"""Bounded per-experiment note edits; historical files stay in the Git parent."""
import base64
from pathlib import Path

from .common import require, safe_relative


SUFFIXES = {'.md', '.json', '.txt', '.patch', '.py', '.cpp', '.cc', '.cxx', '.h', '.hpp'}


def generated(name):
    return '__pycache__' in Path(name).parts or Path(name).suffix in ('.pyc', '.pyo')


def decode_edits(notes, deleted=()):
    require(isinstance(notes, dict) and isinstance(deleted, (list, tuple)), 'invalid experiment edits')
    require(len(notes) + len(deleted) <= 128, 'oversized experiment edit transaction')
    decoded = {}
    for name, data in notes.items():
        safe_relative(name)
        require(Path(name).suffix in SUFFIXES and isinstance(data, str) and len(data) <= 350000,
                'unexpected/oversized experiment artifact')
        decoded[name] = base64.b64decode(data, validate=True)
        require(len(decoded[name]) <= 256 * 1024, 'oversized experiment artifact')
    require(sum(map(len, decoded.values())) <= 1024 * 1024, 'oversized experiment edit bytes')
    require(len(set(deleted)) == len(deleted), 'duplicate experiment deletion')
    for name in deleted:
        safe_relative(name)
        require(Path(name).suffix in SUFFIXES and name not in notes, 'invalid experiment deletion')
    return decoded


def encode_edits(attempt, bot, changed_paths):
    attempt = Path(attempt)
    prefix = f'experiments/{bot}/'
    notes, deleted = {}, []
    for path in changed_paths:
        if not path.startswith(prefix):
            continue
        name = path[len(prefix):]
        if generated(name):
            continue  # Checkpoints retain bytecode; it is not publication data.
        target = attempt / path
        if target.is_file():
            notes[name] = base64.b64encode(target.read_bytes()).decode()
        else:
            require(not target.exists(), 'non-file experiment edit')
            deleted.append(name)
    decode_edits(notes, deleted)  # Fail locally before sending an invalid payload.
    return notes, deleted


def apply_edits(root, notes, deleted=()):
    """Apply explicit edits inside the clean publisher clone, not an owner home."""
    root = Path(root)
    require(not root.is_symlink(), 'experiment root symlink forbidden')
    require(not any(p.is_symlink() for p in root.rglob('*')), 'experiment symlink forbidden')
    for name in deleted:
        target = root / safe_relative(name)
        require(not target.exists() or target.is_file(), 'experiment deletion must name a file')
        target.unlink(missing_ok=True)
        # Allow an explicitly emptied directory to become a file later.
        parent = target.parent
        while parent != root and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent
    root.mkdir(parents=True, exist_ok=True)
    for name, data in notes.items():
        target = root / safe_relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
