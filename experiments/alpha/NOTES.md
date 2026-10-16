# Current experiment: task-5ff630fce5d04a3b94b1dc4cff40d615

## Identity and prior work
- Bot alpha, branch bot/alpha, input revision a27105b001a30fab44c2ed4485f4e2888e25fdb7.
- Engine/SDK 2.1.6; suite pilot-wiring-v1.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e.
- Base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry source matched accepted_snapshot/src exactly (diff -r exit 0).
  Initial tracked modifications are the supervisor's accepted-source restoration,
  as confirmed by arena/worker.py make_attempt, not interrupted work.
- Prior candidate f3a7e2da713bbe6b7c03d3d99cbcc8301e45040386668fbdefc44da4e1e012da
  has completed evaluation, INCONCLUSIVE; it is not pending. Prior notes archived
  as task-c2c7bf3ea00b414a866765a00628b958.md.

## One hypothesis: playbook C, recovery cost
Keeping an injured champion on allied spawn through turn end will prevent
immediate departure after recall from skipping spawn healing. Falsifiable
invariant: after shopping on spawn, health below maximum returns before all
movement, enemy attacks, banking and farming; the dispatcher then end_turn()s.
Expected evaluation effect: fewer repeated low-health recall trips, improving
productive uptime. Win-rate improvement remains unproven.

## Evidence and implementation
- Supplied evaluation 1547e017ef91e36ce01cb35729db66ad6a46c87dcc24df7a7a18bc7bdad505a1
  evaluates the previous candidate at input revision, not this edited source.
  Six candidate observations, zero reported faults, two wins and four losses.
- Collision A, match 3f219304b791f4bdcf5a2a4d49edbcea093392bbb5e48d6dcb2da58962b680e0:
  candidate submitted 660 vs 1034, deaths 20.
- Collision B, match 2245195074781d07ca5b6a23f7b4124f4012fa89b6fc43c2d840dded3e553899:
  candidate submitted 660 vs 1012, deaths 39.
- These aggregates motivate recovery work but do not prove this mechanism caused
  those losses. Recall traces and counts are unknown; no raw private artifacts read.
- Accepted source shops on spawn then can immediately move away, including on
  recall arrival. Added only the post-shop injured-spawn early return in bot.cpp.
- GameRules.md 122 and 373-375 specify turn-start recall arrival and turn-end heal.
  Matching C++ cambc.h health()/max_health() query current state. No new API used.
- Source documentation hashes match RESEARCH.md; routine relevant-section review.
- Existing channel preservation, 35% recall threshold, draft, banking, routing,
  shared memory and item choices retained. Accepted snapshot remains untouched.
- Dispatcher still reaches end_turn() on normal return and caught exceptions.

## Validation and limitations
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
- PASSED, exit 0; checked source hash:
  1907882027b38f8e7efdf4127f06e1a7fa5fec4ed7d613f26d28c29f2927e2dd.
- Local report: .agent/check-task-5ff630fce5d04a3b94b1dc4cff40d615.json.
- Trusted report reference (not opened directly):
  /srv/battlecode/checks/task-5ff630fce5d04a3b94b1dc4cff40d615/1907882027b38f8e7efdf4127f06e1a7fa5fec4ed7d613f26d28c29f2927e2dd/report.json.
- Wrapper smoke IDs: 8758b60b843632177fb857859cc96546cdb34ec874a36514b3fc898481737d35
  and 25e325ef6c7b59b534af71da0aa5d8538dd63aabc95d903ab7b27d53138db0c3.
  Final statistics were not inspected; IDs alone do not prove completed games.
- git diff --check passed. Source review confirms the post-shop guard precedes
  every movement branch; full-health champions retain existing behavior.
- No tournament evaluation or strength claim. Deterministic repeats are not
  independent evidence. Existing debug logging and fuel headroom are unmeasured.
- Risk: waiting for even a small health deficit costs a turn and delays banking;
  expected benefit depends on actual frequency of incomplete spawn recovery.
- Next: supervisor evaluates this exact candidate against accepted source;
  compare submitted gems, outcomes and recovery traces if available.
- Separate organizers' AGENTS.md remains unavailable, as recorded in RESEARCH.md.
