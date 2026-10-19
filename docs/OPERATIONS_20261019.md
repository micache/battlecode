# 19 October recovery and beta exploration handoff

Installed runtime: `c332df20361a5ad40834622baf2e54ce51f43d33`.
Managed Blaxel process: `arena-stable-beta-20261019`, keep-alive and
restart-on-failure enabled. No new administrator command or owner login is
currently required. Physical reboot persistence remains unverified.

The private arena was resumed, stopped for upgrades, then resumed again.
Saved deployment evidence records fresh completed games after restart, all five
supervised units, and the retained source/evaluation identities. Alpha and beta
are awaiting evaluations; gamma was resumed after its blocked task. Games run
continuously between hourly coding opportunities.

## Faults corrected

- A synchronous `bot-check` selected older tournament jobs before its own smoke
  pair. It could drain hundreds of games without normal rolling maintenance,
  hold the coding task open, and exhaust storage. Checks now run their exact two
  games first and perform rolling cleanup before building.
- A disk-write failure left an unfinished attempt marked `RUNNING`. A new tick
  now recovers orphaned synchronous attempts, and another match cannot start
  beside an unreconciled attempt. A regression injects ENOSPC while sealing.
- Match `a1501e756131617f2c9adaec1559bed283fbc19c7e116420cd82cf4667211c74`
  was recovered with services stopped. Attempt 1 is retained as infrastructure
  failure, without an invented winner. Attempt 2 completed normally.
- Gamma task `task-9c55d0328faf44f1945faa1770eac277` remains a blocked
  historical result, not a published or evaluated candidate. Its patch, notes,
  source and final result were preserved. A trusted infrastructure finding
  explains the fixed check failure in its next task's history.
- The outside browser helper previously stopped locally on a submission change
  without notifying the server. Actual mismatch facts now reach the server
  before new creations; unmatched games are quarantined, not relabeled.
- Explicit native read-command throttles honor Retry-After with at least a
  60-second durable wait. Unknown creation outcomes still require reconciliation.

Validation: `python3 -m unittest discover -s tests -q` passed 147 tests;
`python3 -m compileall -q arena ops tests` passed. Synthetic checks are not
represented as real game evidence.

## Owner-selected submission

Upload `artifacts/submissions/beta-7cab9b0f.zip`. It contains beta commit
`7cab9b0f6b948b0ea0b3b284425a3501c564d16b`, source hash
`fd5e25543653c9a8774346212b3f689927a9dd489b1ba2373a1edd0889bf63aa`.
Its existing saved full evaluation is 115 wins / 21 losses across 17 maps,
both sides against four frozen opponents. This is a manual submission candidate,
not a leaderboard guarantee or automatic champion promotion.

At the last source observation, selected submission v12 was a different source;
the arena did not change it. Outside play waits for the exact beta source to be
selected. It then targets up to 50 five-game series per hour against the rotating
top-25 panel, subject to shared quota/readiness and saved source proofs. Five
verified v6 losses against #1 are already shared with all three bots. Two series
that actually used a different upload are quarantined as `SOURCE_CHANGED`.

The source-proof timer is enabled on this operator machine. Outside creations
stop when its proof is stale; private games do not depend on it. This computer
must remain online with a valid approved browser login for outside source proofs.
Uploads and activation are still disabled; only the owner uploads the beta ZIP.

Evidence:

- `evidence/blaxel/beta-exploration-deployment-20261019.json`
- `evidence/blaxel/official-exploration-handoff-20261019.json`
- `evidence/blaxel/submission-beta-7cab9b0f-20261019.json`

Setup/status/pause/stop commands remain in `docs/UNRANKED_EXPLORATION.md`.
