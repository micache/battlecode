# Live pilot status — 16 October 2026

17 October update: gamma is provisioned as a third isolated **Codex** lane,
after the owner corrected the initial Claude request. All lanes use
`gpt-6.1-sol` with high reasoning and hourly improvement, including unchanged
feedback. Gamma's native device login and three-map validity baseline completed;
this is not yet a claim of completed model improvement cycles for gamma.
Completed match working trees are now losslessly archived; raw replay/statistics
and canonical source evidence remain retained. See [active training](HOURLY_TRAINING.md).

The first new beta/gamma attempts failed before reading their task files because
the cancelled Claude setup installed a system Bubblewrap that shadowed Codex's
bundled helper. Services were stopped, the added package removed, and native
task-read/workspace-write/mailbox-write/outside-write-denial probes passed.
No directory permissions or sandbox boundaries were relaxed. Both original
attempts and their unchanged source hashes are preserved in
[the repair evidence](../evidence/blaxel/native-codex-sandbox-restored.json).
Their next attempts retain the original hourly clocks, not immediate retries.
Blocked attempts do not establish that bootstrap documents were reviewed.

[The post-restart snapshot](../evidence/blaxel/three-codex-live-restored.json)
records all four services alive without unit restarts, scheduling unpaused,
fresh heartbeats, no service error/disk-pressure flag, and all three native
model configurations set to `gpt-6.1-sol` / `high`. Completed matches advanced
from 286 to 296 across independent operator requests after launch. Alpha was
awaiting evaluation; beta/gamma were resumed and idle until their hourly slots.
The snapshot is historical evidence, not a real-time status endpoint. Physical
VM reboot persistence and gamma's first successful improvement remain unverified.

Latest maintenance: native official contest login succeeded; the owner now
authorizes guarded official publishing and unranked exploration. Historical
training panels, every-fifth-cycle exploration, bounded full suites, external
metadata feedback and a fail-closed official selection monitor are implemented.
Actual official mutations remain blocked by missing policy/interface evidence,
not by lack of owner authorization. See [the integration record](OFFICIAL_AUTOMATION.md).

Fresh-session continuity is documented in [worker memory](WORKER_MEMORY.md):
bounded structured history, all-outcome result retention, exact accepted versus
evaluated source identities, own-attempt recovery pointers and readable compiler
diagnostics. Fresh conversations are retained; no claim of lossless model memory.

The arena is deployed on Blaxel `banabolabs/battlecode-arena` (4 CPU, 8192 MB
RAM, 8192 MB persistent volume). All three owners completed native ChatGPT logins;
the repository deploy key is installed. Alpha and beta have each
completed two publication/evaluation cycles. **Formal readiness is not
yet certified**, for the explicit limits below. No synthetic/manual task is
counted as a Codex improvement cycle.

Setup/status/start/pause/stop commands: [Blaxel operations](../ops/BLAXEL.md).
Standard persistent-VM systemd units remain under `ops/systemd/`; Blaxel uses
its managed keep-alive process and root-owned unit supervisor instead.

## Completed real evidence

Reports are preserved under [evidence/blaxel](../evidence/blaxel/). Original
sealed match artifacts and replays remain on the server.

- Two complete official starter games, reviewed against the official replay
  viewer's final frame: round 1448, submitted gems A=1012/B=814, no bot faults.
  Match IDs `e19df34bf0a753702aa503d34adda2b6e1c61f75c8e92fea19de1779b24baa82`
  and `be2289273a96df1584e32cac156ca37442eb496527fa97f712aa6401f6038b57`.
  Deterministic repetitions, not independent strategic samples.
- Alpha baseline commit `c0cebd720fcd55e2bbb51d57dd2c398889d4071e` and beta
  baseline `0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9` passed the three-map,
  both-side wiring suite. Full evaluation/match identities are in
  `pilot-identities.json`. Identical source/engine/map games are reused and
  viewed from both sides; they are not extra independent matches.
- Real tie-to-Team-B, deliberate trap versus fuel suspension, truncation versus
  wall timeout, recall/tribute timing, capture occupancy, ranged allowance,
  altar approach and hidden-obstruction diagnostics are in
  `diagnostic-review.json`. The first hidden probe reproduced nothing; a later
  corners-map probe passed the obstruction/reveal/fallback assertions.
- `host-isolation.json` records native Codex sandbox success, separate owner
  UID/GID and private-home enforcement, denied root API/protected writes, and
  actual networkless rootless container memory/CPU/PID limits.
- `restart-service.json` and `restart-supervisor.json` record successful
  SIGKILL recovery with accepted baselines preserved. `volume-remount.json`
  records unchanged database/config bytes and owner metadata after remount.
  A consistent SQLite backup restored with integrity/foreign-key checks.

## Pending and explicit limits

- Two actual Codex cycles per original lane (alpha/beta) are complete in `live-cycles.json` and
  `live-evaluations.json`, with frozen suites, real commits and match IDs:
  alpha `4922166cd44fa0bc1291cf9ccd9b05125cfcb84a`, then
  `a27105b001a30fab44c2ed4485f4e2888e25fdb7`; beta
  `02ab89d1e111f8c75f726004ee54346f5e7e4d8a`, then
  `d93aa34394a38b0b4fc3681e0b3bafa363665c85`.
  Both first experiments scored 4/6 (+1/6 over incumbent); both second ideas
  scored 2/6 (-1/6). These are three-map observations, not full-gate promotions.
  The native loop had 34 completed saved games at this checkpoint, including
  starter, smoke and evaluation runs; cached case views are not independent
  games. The initial two-publication cap is removed for continued operation.
  `arena acceptance-report` honestly remains `verified: false` because the
  full readiness evidence below is not certified. No synthetic cycles count.
- The first live alpha invocation stopped because feedback exposed a raw
  artifact path without explaining the development-evidence mailbox. The
  handoff now supplies exact `arena-client ... slice` commands and omits private
  artifact paths. The stopped attempt remains preserved, not counted as a cycle.
- Process recovery and API-client disconnection were observed; physical VM
  reboot and literal SSH-disconnect persistence are not certified. Blaxel
  archive/unarchive returned 403 because the workspace lacks that preview
  feature (`provider-archive.json`); no permission denial was bypassed.
- C++ runtime capacities, winning threshold, round limit and fuel behavior have
  real evidence. The complete cross-language runtime profile is not measured;
  the engine lock therefore honestly retains `effective_profile: null`.
- Organizer AGENTS.md and event participation/AI/official-platform policies are
  still missing. No contest-parity or official-automation certification.
- Daily database snapshots/manifests do not constitute a complete off-host
  replay backup. Disk pressure pauses new work; automatic destructive pruning
  is not enabled. The 8 GB volume is a bounded pilot, not unlimited storage.

Automatic champion promotion remains disabled. Three-map evaluations are
provisional: the unchanged full nine-map, three-distinct-frozen-opponent gate,
matched incumbent comparison and head-to-head, reliability/readiness and all
score/holdout thresholds remain required before enabling promotion. Official
submissions/challenges, API billing and cross-account failover remain disabled.
