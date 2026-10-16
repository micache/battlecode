#!/bin/bash
# Run as bc-arena during explicit network-enabled maintenance, before starting services.
set -euo pipefail
cd /opt/battlecode/ops
# Trusted bootstrap only; match/build execution below always uses network=none.
podman --cgroup-manager=cgroupfs build --network=host --tag battlecode-toolchain:2.1.6 --file Containerfile .
arena_image_id=$(podman image inspect --format '{{.Id}}' battlecode-toolchain:2.1.6)
mkdir -p /srv/battlecode/repos/official-template /srv/battlecode/maps/pool-2026a-216
podman run --rm --pull=never --network=none "$arena_image_id" tar -C /opt/project --exclude='.cambc' -cf - . | tar -C /srv/battlecode/repos/official-template -xf -
cp -n /srv/battlecode/repos/official-template/maps/*.map26a /srv/battlecode/maps/pool-2026a-216/
podman run --rm --pull=never --network=none "$arena_image_id" python3 -c 'import json,subprocess; print(json.dumps({"packages":subprocess.check_output(["dpkg-query","-W"],text=True)}))' > /srv/battlecode/locks/compiler-record.json
arena register-toolchain --image-id "$arena_image_id" --template /srv/battlecode/repos/official-template --compiler-record /srv/battlecode/locks/compiler-record.json
