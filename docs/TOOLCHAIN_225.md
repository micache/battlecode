# Current-game upgrade: CLI 2.2.5

The official PyPI x86-64 wheel is hash-pinned in
`ops/engine-requirements.txt`. Its distributed executable is also hash-checked.
The embedded engine identifies itself as 0.0.3, build
`d7e29ae3546357b011419c764204b7b9e2232bdb1b07868250c6b35d4c18d2a5`:
the same patch as the saved owner-team official matches. Qualification uses
`build --release` and `run --release --json`, default fuel, no round override,
and all 17 freshly published maps on both sides. Three existing reserved maps
remain hidden from worker diagnostics. No daily counter can downgrade a full
evaluation. Source/opponent commits, map bytes and toolchain are frozen.

Old engine results are historical, not current qualification. All source,
notes, commit IDs and old evaluation identities survive the transition.
`summary.json` provides small per-champion evidence; large original statistics
and replay bundles remain canonical under rolling retention.

Current JSON statistics include timelines/events and are much larger than the
old format. Retention losslessly gzips large `final.json` files while removing
redundant project worktrees. It verifies their original content hash before
publishing the sealed compact attempt; `arena-client ... --file final.json`
still returns verified uncompressed slices. Parser/bootstrap files stay raw.
Replay bundles and compact results are unchanged. Oldest-first retirement still
applies, with no offloading. Evaluation stages load their exact frozen build
records after a code-only restart, rather than compiling new inputs mid-suite.

Deployed runtime: `bbfd0d517a57dcaa12338581c550661886f3bb53`, 19 October.
The managed supervisor is `arena-current-game-225-storage-supervisor-20261019`.
Real gzip/readback, owner-mailbox access, frozen-build and resumed-match evidence
is linked from [implementation status](IMPLEMENTATION_STATUS.md). PyPI was
rechecked that day: 2.2.5 remains current and the x86 wheel hash is unchanged.

The owner's new GameRules.md is byte-identical to the prior export. The new
C++ export is preserved byte-for-byte at `sources/BotAPICpp.md`. Its error enum
matches all 134 installed name/number pairs. **Upstream gap:** ward::owner is
documented but absent from the 2.2.5 header; workers must not call it. Do not
invent imports or patch the official SDK to conceal this discrepancy.

## Stopped-service deployment

Pause through the arena mailbox; let the active coding task finish. Check all
workers are no longer RUNNING before stopping. Commands below run on the server
as administrator unless wrapped with as-arena. No owner credential is copied.

```sh
python3 /opt/battlecode/ops/as-arena.py arena pause
python3 /opt/battlecode/ops/supervisor.py stop
git -C /opt/battlecode-source pull --ff-only origin main
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode-source/ops/toolchain-transition.py capture
python3 /opt/battlecode-source/ops/upgrade.py
python3 /opt/battlecode/ops/as-arena.py bash /opt/battlecode/ops/prepare-engine.sh
python3 /opt/battlecode/ops/toolchain-transition.py activate
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/run-fixtures.py --name idle-tie
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/record-cpp-profile.py
python3 /opt/battlecode/ops/as-arena.py arena starter-check
```

Staging is intentionally non-overwriting: if it was already performed, inspect
`/srv/battlecode/toolchains/cambc-225` and skip that command. Capture/activation
also refuse ambiguous retries. The first starter probe has no parser contract;
its unrecognized normalization is preserved, not presented as a passed game.
Run crash and fuel fixtures, inspect the new starter replay at its final frame
with the official visualizer, then install the reviewed parser:

```sh
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/run-fixtures.py --name crash
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/run-fixtures.py --name fuel
python3 /opt/battlecode/ops/review-parser.py --fixture EXACT_FINAL_JSON --replay EXACT_REPLAY --review SAVED_VISUALIZER_REVIEW --confirm-replay-agreement
python3 /opt/battlecode/ops/as-arena.py arena starter-check
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/toolchain-transition.py rebaseline
```

The second starter check runs fresh games bound to the reviewed parser;
it does not rewrite old unrecognized attempts. Rebaseline measures preserved
development sources against the new frozen environment before worker dispatch.
Start the persistent managed `ops/blaxel-start.py` process via the operator
client, then `as-arena.py arena start`. Status: `arena status` or the public
status JSON. Pause: `arena pause`. Stop: `ops/supervisor.py stop`.

The C++ settings/budgets observer records 2000 rounds, 1000 tributed gems,
1024/8-byte memories, and first/subsequent draft/play fuel observations. Other
languages are explicitly unmeasured and unused. A matching engine build does
not prove identical opponents, pairing, leaderboard rating, or an undisclosed
production settings override. Official matches are five-map series; our
17-map both-side benchmark is broader, not a reproduction of a particular
series. Automatic promotion and official mutations remain disabled.
