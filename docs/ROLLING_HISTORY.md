# On-server rolling history

22 October extension: keep only the newest three unchanged, successfully
published generated publication/worker checkouts per lane. Verify completion
and immutable source identity first, journal deletion, and retain push intents,
commits, result/usage records, patches and notes. Dirty, partial or failed work
is not removed. The worker handles only its own generated attempt directory;
credentials and other home contents are never targets. Routine raw evidence
from obsolete engine suites no longer pins an entire old full evaluation after
migration; scores, identities and compact lessons remain. See TOOLCHAIN_305.md.

The owner selected oldest-first local retention on 18 October 2026, replacing
the laptop offloader. The server does not need the operator machine to remain
online to maintain match-history space. The old offload timer is disabled;
already downloaded local archives are preserved, not deleted.

## Kept

- Source commits/snapshots, branches, strategy notes, rules and SDK pins.
- Normalized match results, exact commit/build/map identities, evaluation
  summaries and compact feedback. Old raw deletions have explicit ledger records.
- Raw evidence for active evaluations, current accepted champions, each lane's
  latest evaluation and latest full evaluation, its current development base,
  recent representative failures and the two most recent exported candidates.
- Parser/settings/bootstrap fixtures and at least the newest 120 completed games.
- The newest twelve successful compiler caches, plus caches pinned by queued,
  running or active-evaluation matches. Missing older caches rebuild on demand.
- Three local database backups after subsequent successful backups.

## Discarded

Per-match build workspaces/project ZIPs duplicate the immutable source and shared
compiler cache. The arena removes these after completion, while preserving the
replay/statistics/log bytes in a newly sealed compact attempt. Historical path
aliases remain valid. Interrupted compactions recover before another deletion.

When raw artifacts approach 768 MiB or free space falls within 256 MiB of the
configured minimum reserve, the arena deletes the **oldest unprotected completed
match directories**. It aims for 75% of the artifact budget and an additional
768 MiB above the minimum free reserve. Per-step work is bounded; maintenance
continues even while the normal disk safeguard has paused new games.

Raw replays/logs/statistics removed this way are **permanently discarded**, not
offloaded or recoverable from the server. A retirement transaction records the
original seal hash and retained result hash before clearing the raw artifact
pointer. Restart finishes an interrupted deletion. No game is reclassified as a
loss or erased from score/history tables merely because its raw files expired.
Requests for expired raw diagnostics report that they are unavailable.

This is a rolling **match/build** history policy, not permission to delete Linux
homes, owner credentials, source repositories or arbitrary directories. The disk
guard remains a last resort if protected evidence or unrelated storage fills the
volume. The policy does not make metadata/source storage infinitely large.

## Operations

Installation/update and enabling the policy require stopped arena/worker services:

```bash
python3 /opt/battlecode/ops/supervisor.py stop
python3 /opt/battlecode-source/ops/upgrade.py
python3 /opt/battlecode/ops/configure-retention.py
```

Restart using the deployment's managed keep-alive supervisor, then submit the
ordinary `arena start` control command. The configuration helper retires any
unused prepared offload bundle, without deleting original match data. The sole
arena writer performs ongoing cleanup; no model invocation is needed. New
offload requests are rejected while rolling history is enabled.

`arena status` exposes `rolling_history`: current free space, raw bytes, reclaimed
bytes, retired raw-game count and the last batch of discarded compiler caches.
The evidence/retirement ledger remains in SQLite; it is not another service.

Live deployment: runtime `7c2e76d6e80b4353efd906c6047f80ec4e91606e`.
[Saved evidence](../evidence/blaxel/rolling-history-live-20261018.json) records
the disk guard clearing, free space rising from about 1.0 GB to 3.9 GB, seven
new completed games, and beta's next native improvement job running. It verifies
retained artifact seals and parser-fixture bytes, and confirms that a retired
raw match still has its normalized result. At that snapshot 768 oldest routine
raw match directories had been permanently removed. 106 local tests passed.
