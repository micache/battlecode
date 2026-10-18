"""Runs only in the credential-free bootstrap image."""
import hashlib
import importlib.metadata
from pathlib import Path
import sys


EXPECTED = "47c4d2d78ba29e7ef8c4633845f26659ece968c9424409a300a9ea4b89e7eaa2"
distribution = importlib.metadata.distribution("cambc")
if distribution.version != '2.2.5':
    raise SystemExit('unreviewed cambc distribution')
matches = []
for item in distribution.files:
    path = Path(distribution.locate_file(item))
    if path.is_file() and path.stat().st_size == 95698040:
        if hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED:
            matches.append(path)
if len(matches) != 1:
    raise SystemExit("official distributed binary hash/size mismatch")
print(EXPECTED)
