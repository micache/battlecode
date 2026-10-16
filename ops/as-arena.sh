#!/bin/bash
set -euo pipefail
exec sudo -u bc-arena env XDG_RUNTIME_DIR=/run/battlecode-arena "$@"
