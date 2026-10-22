#!/bin/bash
# Trusted network-enabled maintenance only. Stage; never switch live configuration.
set -euo pipefail
cd "$(dirname "$0")"
arena_version=3.0.5
arena_stage=/srv/battlecode/toolchains/cambc-305
test ! -e "$arena_stage"
podman --cgroup-manager=cgroupfs build --network=host --tag battlecode-toolchain:$arena_version --file Containerfile .
arena_image_id=$(podman image inspect --format '{{.Id}}' battlecode-toolchain:$arena_version)
mkdir -p "$arena_stage/template"
podman run --rm --pull=never --network=none "$arena_image_id" tar -C /opt/project --exclude='.cambc' -cf - . | tar -C "$arena_stage/template" -xf -
podman run --rm --pull=never --network=none "$arena_image_id" python3 -c 'import json,subprocess; print(json.dumps({"packages":subprocess.check_output(["dpkg-query","-W"],text=True)}))' > "$arena_stage/compiler-record.json"
podman image inspect --format '{{.Id}}' "$arena_image_id" > "$arena_stage/image-id.txt"
chmod a+rx /srv/battlecode/toolchains "$arena_stage"
chmod -R a+rX "$arena_stage/template"
echo "Staged CLI $arena_version at $arena_stage; live configuration and old toolchain unchanged."
if test "${1:-}" = --register; then
  arena register-toolchain --image-id "$arena_image_id" --template "$arena_stage/template" --compiler-record "$arena_stage/compiler-record.json"
fi
