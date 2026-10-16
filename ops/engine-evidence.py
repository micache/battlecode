"""Runs only in the credential-free bootstrap image."""
import hashlib
import importlib.metadata
from pathlib import Path
import sys


EXPECTED = "e2a641bab3c9ec3b80d595c2956e6dbb115959b039617efb14e554617bf0d08c"
distribution = importlib.metadata.distribution("cambc")
matches = []
for item in distribution.files:
    path = Path(distribution.locate_file(item))
    if path.is_file() and path.stat().st_size == 95129344:
        if hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED:
            matches.append(path)
if len(matches) != 1:
    raise SystemExit("official distributed binary hash/size mismatch")
print(EXPECTED)
