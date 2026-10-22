# Current-game maintenance: CLI 3.0.5

The official 22 October release is pinned by wheel SHA256
`7715601375ef767d51817fb245fade3ee01a38073bd84449898b82e610d37e46`
and Linux executable SHA256
`9967da2e981897f70ed4bacb187e73103bb6ca728baecb275e071fbb220a6fff`.
A completed local starter probe reports bundled engine 1.0.3, build
`fcb6c3e881c453fb7fcb1ce852ff0a6f10c9e3a199126a000df05b427f4ba41f`,
readable format 1.0 / metric semantics 1. This does not relabel production 1.0.1
or prior local 0.0.3 games. Local parsers require the exact contract's engine;
outside observations retain their actual engine and map identities separately.

Fresh official `init --yes` produced 40 published maps. Their bytes are frozen
in `evidence/map-pool-305.json`; both sides on every map remain mandatory for
full qualification. `00monolith`, `00packs`, `00rows` are reserved. Automatic
promotion, official upload and activation remain disabled. The team boss stays
the same immutable own source, compiled anew for this toolchain. All workers
receive the current rules, C++ export/header hashes and shared boss packet. The
first published strategy task on a changed engine returns to foundation mode.

Changed balance includes Golem, Heart of Ruin, camp rewards/ranges, kill gold,
several passives/spells, five-hit altar locks and ten-turn ward recharge.
`move_towards` now treats a blocked target as free for pathfinding but still
rejects landing there; choose a legal approach tile. `ward::owner` and new
vision/distance-field methods are present. All 134 exported error name/number
pairs match the installed header. Fresh downloads are byte-preserved in
`sources/`; prior exports remain in Git. The Python export was fetched for
provenance but is not a C++ worker's required reading.

## Stopped-service upgrade

Use the normal owner-approved maintenance procedure; no credential copying.
Wait for a running model to finish before stopping the supervisor. Capture
preserves the measured development base and newest source for each lane,
configuration, old locks and a consistent database backup. Activation and
rebaseline are deliberate, non-overwriting operations: reconcile receipts
before retrying an interrupted step.

```sh
python3 /opt/battlecode/ops/as-arena.py arena pause
python3 /opt/battlecode/ops/supervisor.py stop
git -C /opt/battlecode-source pull --ff-only origin main
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode-source/ops/toolchain-transition.py capture --target 3.0.5
python3 /opt/battlecode-source/ops/upgrade.py
python3 /opt/battlecode/ops/as-arena.py bash /opt/battlecode/ops/prepare-engine.sh
python3 /opt/battlecode/ops/toolchain-transition.py activate --target 3.0.5
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/run-fixtures.py --name idle-tie
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/record-cpp-profile.py
python3 /opt/battlecode/ops/as-arena.py arena starter-check
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/run-fixtures.py --name crash
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/run-fixtures.py --name fuel
```

The first starter probe has no parser contract and is not qualification. Inspect
its exact replay in the official visualizer at the final frame. Then:

```sh
python3 /opt/battlecode/ops/review-parser.py --fixture EXACT_FINAL_JSON --replay EXACT_REPLAY --review SAVED_VISUALIZER_REVIEW --confirm-replay-agreement
python3 /opt/battlecode/ops/as-arena.py arena starter-check
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/toolchain-transition.py rebaseline --target 3.0.5
```

Run mechanics/hidden-obstruction and truncated/timeout diagnostics under the
new engine as well; keep unknown telemetry unknown. Rebaseline ends obsolete
evaluations as version-change INCONCLUSIVE, cancels only unstarted old-engine
jobs, preserves their suites/results/source commits, and queues new evaluations.
Start the managed `ops/blaxel-start.py` process, then `as-arena.py arena start`.
Normal status/pause/stop commands remain unchanged. New full suites must finish
before any current-engine submission-readiness claim.

If the server browser lacks WebGL2, download the exact saved replay and review
it on the operator machine using the same pinned official CLI. Do not replace
the official viewer with a guessed replay decoder. `inspect-replay.cjs` accepts
operator-only `ARENA_REVIEW_PLAYWRIGHT` (Node package path) and
`ARENA_REVIEW_CHROMIUM` (optional executable path). Use a fresh browser context,
verify the served replay SHA256, seek the fully indexed final frame, and retain
both JSON and screenshot. Copy that JSON back as the explicit `--review` file;
`review-parser.py` still verifies the exact replay hash, final round and scores.
The 22 October server replay was successfully reviewed this way after server
Chromium reported WebGL2 unavailable, including with SwiftShader enabled.

Before resuming new suites, verify process recovery while globally paused with
`python3 /opt/battlecode/ops/restart-check.py --allow-paused-queue`.
It refuses active models/matches, kills only the validated arena process, and
requires a new healthy heartbeat with unchanged queued specifications, attempts,
terminal results and accepted revisions. This is process recovery, not proof of
physical VM reboot persistence.

## Bounded storage

Rolling maintenance also retires completed publication Git checkouts beyond
the newest three per lane, only after verifying the published commit is in the
mirror and the checkout has no unknown edits. Push intents and compact retirement
receipts remain. Each worker independently retires its unchanged published
attempt clones beyond the newest three, retaining result/usage, patch and notes;
failed/interrupted or edited work is never discarded. Old-engine routine raw
games stop pinning an entire obsolete full suite after migration. Source commits,
normalized scores and compact lessons remain; no offloading is used.
