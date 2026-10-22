"""Runs only in the credential-free bootstrap image."""
import hashlib
import importlib.metadata
from pathlib import Path
import sys


EXPECTED = "9967da2e981897f70ed4bacb187e73103bb6ca728baecb275e071fbb220a6fff"
distribution = importlib.metadata.distribution("cambc")
if distribution.version != '3.0.5':
    raise SystemExit('unreviewed cambc distribution')
matches = []
for item in distribution.files:
    path = Path(distribution.locate_file(item))
    if path.is_file() and path.stat().st_size == 99284768:
        if hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED:
            matches.append(path)
if len(matches) != 1:
    raise SystemExit("official distributed binary hash/size mismatch")
print(EXPECTED)
