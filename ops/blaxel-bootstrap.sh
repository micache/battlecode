#!/bin/bash
# Root-only, explicit installation/recovery. No Codex login or model invocation.
set -euo pipefail
test "$(id -u)" = 0
cd /opt/battlecode-source
test -z "$(git status --porcelain)"
apk add --no-cache python3 py3-pip bash git openssh-client curl shadow util-linux \
  podman fuse-overlayfs slirp4netns nodejs npm iptables-legacy ca-certificates \
  e2fsprogs e2fsprogs-extra ripgrep
python3 ops/blaxel-volume.py
python3 ops/blaxel-host.py
if test ! -f /etc/battlecode/arena.json; then
  python3 ops/install.py --blaxel --ack-persistent-volume
elif test ! -f /opt/battlecode/INFRASTRUCTURE_COMMIT; then
  echo 'Persistent state exists, but trusted runtime is absent. Restore the recorded infrastructure revision; do not reset state.' >&2
  exit 1
elif test "$(cat /opt/battlecode/INFRASTRUCTURE_COMMIT)" != "$(git rev-parse HEAD)"; then
  python3 ops/upgrade.py
fi
if test ! -e /usr/local/bin/codex; then
  npm install --prefix /opt/battlecode-tools @openai/codex@0.163.0
  ln -s /opt/battlecode-tools/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex /usr/local/bin/codex
fi
python3 /opt/battlecode/ops/prepare-owners.py
if test ! -f /srv/battlecode/locks/engine.json; then
  python3 /opt/battlecode/ops/as-arena.py bash /opt/battlecode/ops/prepare-engine.sh
fi
python3 /opt/battlecode/ops/as-arena.py arena init
echo 'Installation ready, paused. Complete owner logins and review real starter games before starting workers.'
