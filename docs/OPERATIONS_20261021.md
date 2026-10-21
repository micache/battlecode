# Frozen build-cache recovery — 21 October

Installed fix: `e2fbf2eb3a5c765b0fbb7b1026f44283da37c5a1`.
Managed server process: `arena-cache-recovered-20261021` (keep-alive,
restart-on-failure, maximum five restarts). Existing users, logins, source
branches, engine lock, map pool, hourly coding cadence and evaluation gates
are unchanged. No owner login or administrator action is currently needed.

## Cause and fix

The build LRU pinned queued/running match inputs, but not every build referenced
by an active evaluation's frozen suite. Alpha's development-base build was
removed before its screen stage needed it. `frozen_build()` then raised a missing
`bot.wasm` error on every tick, preventing later evaluations and games advancing.

- Retention now pins the candidate, incumbent, development base and every
  opponent build in every active suite, including not-yet-queued stages.
- Missing frozen caches are rebuilt from their immutable source and the pinned
  toolchain. Both original side-A and side-B WASM hashes must match before the
  restored cache is published under its original build ID. Cache log hashes may
  differ; executable bytes may not. Frozen SQLite build records, match IDs,
  suite hashes and source revisions are not rewritten.
- Queued matches check/recover their recorded build inputs before incrementing
  the attempt count. A missing disposable cache does not consume a game retry.
- Existing changed binaries are not silently replaced. A failed reproducibility
  check is journaled and stops automatic recompilation pending operator review;
  interrupted recovery is bounded to two attempts. Partial cache directories
  are preserved under `.damaged-<build-id>-<timestamp>`, not discarded.

## Verified on the real server

Services were paused/stopped before upgrading. All ten active frozen builds were
checked, and missing build
`90e6bc3818a17196189cc90e18b38d9843819058b5d5800bf17e0c5017691ce8`
was restored. Both executables matched their recorded SHA-256 exactly:
`11d8ee0347fa9d5a0fac05b894000602912466b2c02399e3d1ef38e2fd95224d`.
The preserved source is alpha commit
`046f1c3a41fe746c65c0982d06062623200fa931`.

Alpha evaluation `7bf00779e54a677aca1f27aace3e649723c9c120ee10a49d0f5f5aa17d8b3f8b`
advanced from smoke to screen and then full-pool promotion stage. Its original
suite hash is unchanged; automatic champion promotion remains disabled.
The private arena resumed at 02:49 UTC. Saved completion manifests were verified
for five subsequent full games, including
`3250471029e3cbb209f72b8a82dc30e0447e26242ba2d93ed2756bf68267aa02`
and `dc436f2a55920514e5a26984fdccdf327c01ef89015fb56619c00c498fd82d17`.
All five completed with zero bot faults, the same pinned engine lock, and no
fuel or round overrides. The completed-game counter increased from 14,137 to
14,149 at the first saved verification. All five units had zero restarts, no
service error, and no disk-pressure stop. Pending evaluations must finish before
their respective lanes receive the next hourly coding opportunity.

Local validation: 152 tests passed with
`python3 -m unittest discover -s tests -q`; compileall and `git diff --check`
passed. These include future-stage retention, missing-cache recovery, exact
binary preservation, changed-binary rejection and pre-attempt repair regressions.
Synthetic tests are not presented as real match evidence.

Evidence:

- `evidence/blaxel/cache-recovery-20261021.json`
- `evidence/blaxel/cache-recovery-live-verification-20261021.json`

The separate outside-challenge lane remains source-change guarded: the team
changed its live upload after the approved beta submission. This is not cleared
by cache repair, and it does not block private matches or coding. A new outside
source mapping requires owner direction and source verification. No upload or
activation was performed. Physical reboot persistence remains unverified.
