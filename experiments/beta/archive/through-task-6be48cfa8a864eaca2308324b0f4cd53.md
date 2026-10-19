# Operational summary

## task-6be48cfa8a864eaca2308324b0f4cd53 — route-directed dash travel

Hypothesis: appending safe two-tile route-directed dashes to ordinary walking
improves farming/banking throughput and matched wins versus 9f7ae1c8 / b4e969c7.
No win gain, lower submitted gems, or increased deaths, faults or suspension
falsifies it. Unmeasured rules/source deduction; no turn trace proves dash waste.
Decision, precise evidence and validation artifacts: this task's directory.

Identity: beta / bot/beta; input HEAD 672874bb459ad66bfc3e03b3ff7f96a9160fbf56;
trusted edit 9f7ae1c88a1bd0d5d62ed7713956efd40c95be33; base source
b4e969c76d293beb3fdfd75251814a80cb81d2e147e64ee34f5d7feedcdbb1a1.
All six files matched trusted edit_start hashes and edit Git blobs before editing.
Prepared bot.cpp/bot.h differences from HEAD were intentional, not unfinished work.
Prior task PUBLISHED/evaluated; no unpublished candidate awaits evaluation.
Protected champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in trusted
Git/snapshot. Previous operational notes archived through task-9485272c.
No agents, commit, push, official action or comparative tournament invocation.

Evidence: evaluation e0a46ae1b03695e4ac5bbf113845cae78b46141dd5d73dde477974176787d6b4
measured 672874bb / 1afc2983, not today's edit/new source: 42W/6L, zero reported
faults/missing/unknown reliability, INCONCLUSIVE/development-six-map. Matched
edit-base delta 0.0 on 24 pairs; +0.75 protected-champion delta is separate.
- Corners 6adb00fb, A vs gamma 1b34f42a / 3ce565f6, round 409: own 658
  submitted / 766 collected vs 1032/1032; one death each. Five picks includes
  Vendetta; throughput concern, not a traced dash cause.
- Collision c9171081, A, round 875: 872/1026 vs 1012/1100, eight own deaths.
  Exact opponent source unknown in compact failure record. Three picks have no
  dash; this change is not expected to solve that loss.
- Contrasting current wins: interlock and lanes each 8W/0L across both sides;
  individual winning match IDs/action traces unavailable in supplied summary.
Full IDs, provenance and supplied authoritative compact metrics: evidence.json.
Offline final slices are hindsight only; no omniscient state is a runtime input.

Frozen manifest ab20635b: inspected gamma 1b34f42a / 3ce565f6 draft and full
farmer: durable melee-first roster, reward/time routes, observed respawn memory,
300-gold shopping recalls, each-bag banking and lock clearing. Its move helper
also omits dashes despite Vendetta second. Alpha 5f73d078 / ba646c6e relevant
movement/combat sections omit dash. New policy is a distinct rules deduction;
shared arena code does not establish official opponents' behavior.

Current strategy: Varg/Tavi/Ryth/Vendetta/Marcella; Jungle Strength,
Monster Strength, Durability Health, then Power Strength. Independent group
farming/capture, bank each bag, full spawn healing, opportunistic altar locks.
No live shared-memory protocol. New dash_along_route runs after normal walking:
- Actual ready ground dash, range >=2, compatible with walking; alive, cast
  allowance, no channel or move/cast restriction. Ordinary move is retained.
- Reuse original route field; refresh blockers and visibility after walking.
  Eight compass candidates only, each a straight two-step fully visible path.
  Both intermediate and landing are free of terrain/units/reservations. No holes,
  bent paths or blind jumps; range mask alone never authorizes a destination.
- Require finite distance values and >=2 route steps gained. Fixed compass tie
  order, minimum remaining distance. At goal or one step away, preserve cast.
- Reject landing within visible live enemy basic range +1. Camps can remain
  legitimate farming approaches; hidden enemies/spells are not ruled safe.
- >=45k fuel to start; >=30k before cast. One attempt even on hidden-blocker
  reveal. After success refresh altar-lock placement; caller refreshes combat.
- Seven compiled boundary assertions reject no progress, reversal and unreachable
  field values. No new distance field or group scan. Cheap walking fallback.
Draft, items, combat, camp ranking, recovery, bank policy and end_turn preserved.
Only bot.cpp differs from edit source; bot.h difference from HEAD is restoration.

Risks: cast spent on travel can delay reset clearing. Vendetta monster-kill cooldown
refresh may mitigate but is unmeasured. Strict path/visibility/fuel filters may
limit coverage. Partial field is a ranking estimate after moving, not current
occupancy. Fuel thresholds are not measured headroom. No expected gain for
three-pick rosters; they incur a small dispatch cost. Hidden threats remain.

Engine 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1; pinned C++ header SHA256
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Docs unchanged per trusted handoff; consulted compact BOT_REFERENCE, RESEARCH,
organizer record, Playbooks B/C/D/F/G and relevant handbook/C++ API/installed
header movement, dash, restrictions, channel, bounds and distance-field contracts.
Organizer hub review does not certify all event policies or production parity.

Final-source validation (no bot-source edits afterward):
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0, source 6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
Report .agent/check-task-6be48cfa8a864eaca2308324b0f4cd53.json;
reference check:task-6be48cfa8a864eaca2308324b0f4cd53:6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
Exact-source check-report independently returned PASSED/0, saved check-report.json.
Own-side smoke stdout exports exited 0 and contain zero bytes: smoke-a/b.json.
Smoke IDs b6dee446b6687e67b919b5ca8c9ebcd5be5f68dcfb52725d99f50c84299cc1d1
and 291b302e769984d83eeb5f2332e55a75d84946c6fec562c291614f0936fdcb02.
Compilation includes all seven progress assertions. Smoke success/empty logs do
not establish complete competitive games, actual dash coverage, no suspensions,
measured fuel headroom or strategic gains. `git diff --check` PASSED/0; saved
as diff-check.txt. Only source change from edit base is bot.cpp.

Prior negative findings retained: healthy shopping and banking detours zero
matched gain; combat retargeting -0.041667; reachable cooldown scheduler +0.041667
with interlock regression; harvest circuits zero established gain. Isolated
arrival-tribute/item/draft/shield changes did not establish additive gains.
No rejected system or healthy-shopping policy silently restored.

Next: supervisor evaluates exact checked source against 9f7ae1c8 on matched maps,
both sides and frozen opponents. Compare wins/submitted gems first, then larger-
draft Vendetta contribution, deaths and available fuel telemetry. If dash use is
rare, inspect fuel/path admission before broadening range or changing roster.
Development continuation still requires the full champion promotion gate.
