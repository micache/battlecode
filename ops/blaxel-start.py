#!/usr/bin/env python3
"""Managed keep-alive entry point: remount persistent state before services start."""
import os
from pathlib import Path
import subprocess
import sys

if os.geteuid() != 0:
    raise SystemExit('administrator required')
root = Path(__file__).resolve().parent
for script in ('blaxel-volume.py', 'blaxel-host.py'):
    subprocess.run([sys.executable, str(root / script)], check=True)
os.execv(sys.executable, [sys.executable, str(root / 'supervisor.py'), 'serve'])
