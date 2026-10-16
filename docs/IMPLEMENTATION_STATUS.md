# Live pilot status — 16 October 2026

The arena is deployed on Blaxel `banabolabs/battlecode-arena` (4 CPU, 8192 MB
RAM, 8192 MB persistent volume). Both owners completed native ChatGPT logins;
the repository deploy key is installed. Actual model improvement jobs have
started. **Final acceptance is not yet complete.** No synthetic/manual task is
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

- Two actual published Codex improvement/evaluation cycles per lane are still
  pending. `arena acceptance-report` is authoritative; it retains real task,
  source commit and match identities and will not count operator bootstraps.
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
