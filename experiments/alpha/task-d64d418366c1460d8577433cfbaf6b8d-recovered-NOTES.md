# Current experiment: task-d64d418366c1460d8577433cfbaf6b8d

## Identity and prior work
- Bot alpha, branch bot/alpha, input HEAD 4b6483b0e91df11262fb6d8b42ab2667778e1571.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK 2.1.6; suite pilot-wiring-v1; canonical engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Entry source equals accepted_snapshot/src. worker.py make_attempt intentionally
  restores accepted source; the initial tracked diff is preserved in
  task-d64d418366c1460d8577433cfbaf6b8d-entry.patch. Identity report saved alongside.
- Prior notes archived as task-60546c3a86fa400bb632346db8815d8c.md.
- Previous item-change candidate source
  24f016d952f46c984bfb2eeff620bbfb78aa5a47a6b72d7893acbf616baeb79f
  completed evaluation INCONCLUSIVE. No pending candidate identified. This new
  experiment starts from accepted source, without the prior Strength substitution.

## One hypothesis: playbook C, recall recovery
Holding an injured champion on allied spawn until turn-end healing will prevent
premature low-health departures after recall, improving survival and submitted
gems. Falsifiable invariant: after shopping, an actionable injured champion already
on allied spawn returns before combat, banking or farming; a full-health champion
and away-from-spawn behavior remain unchanged. Evaluation prediction: lower mean
champion deaths than the accepted bot on matched development cases; compare
submitted gems and outcomes to measure whether survival offsets the extra wait.

## Evidence and implementation
- Supplied evaluation e525c2d2f15f5b4d23774ef05a6f1d02f4c1a921e98c20ec650995eb28799f1b:
  previous candidate 4 wins/2 losses, mean deaths 25, zero reported bot faults.
  Coverage is provisional-three-map-wiring. Saved task feedback in this directory.
- Corners B, match 60f5b94e1c1c0035738a5bf80fe4ba22bec7b8e0e0c267b9b4b09c1f27b34a82:
  previous candidate deaths 17, submitted 658 vs 1020, round 648.
- Elkring A, match e75cb9a38791770ab6434d597066d0f4cfbec4232911e35f500d2855be3e3109:
  previous candidate deaths 45, submitted 792 vs 1026, round 1115.
- Both cases use candidate revision
  a1ebb71a3144494723f622be61da10ca05f071b5be0af966c9ae14144b12bcec,
  commit equal to input HEAD, versus opponent source equal to base. These are
  strategic-loss evidence, not proof that missed healing caused the deaths.
- Accepted play_turn shops on spawn, then can immediately move toward gems/camps.
  Recall completion is no longer channeling, so it passes the channel guard.
- GameRules.md 122, 369-375: recall arrives at owner turn start; healing occurs at
  turn end, requiring remaining on spawn. Matching installed C++ cambc.h confirms
  live health()/max_health() and allied spawn mask contracts; spawn_healing is an
  engine setting. Documentation export hashes still match RESEARCH.md.
- Added only an injured-at-spawn early return after shopping in bot.cpp. Fresh
  health/max_health queries include any Health-item purchase. main.cpp already
  yields after play_turn returns, including exception fallback. No new state,
  loops, shared-memory layout, policy thresholds or fuel overrides.
- Separate organizers' AGENTS.md is still unavailable, not reviewed.

## Validation, uncertainty and next action
- Identity check PASSED, exit 0; task-d64d418366c1460d8577433cfbaf6b8d-identity.json.
- Source invariants PASSED, exit 0; command:
  PYTHONPATH=. python3 experiments/alpha/task-d64d418366c1460d8577433cfbaf6b8d-source-check.py
  Report: task-d64d418366c1460d8577433cfbaf6b8d-source-check.json.
- Candidate source: 4b1ee918038011be24888b3b8e918831c1451e45a07ba9e518647afa93f3e21b.
- Trusted compilation/smoke and whitespace checks: pending below.
- No improvement claim. The final-statistics slices inspected were bounded;
  recall counts, missed-heal frequency, runtime branch coverage and fuel headroom
  remain unknown. Full-health waiting is avoided, but any injured spawn occupant
  waits (including after shopping), which can delay banking by a turn. Linked-body
  deaths, interrupted recalls, camp choice and combat can dominate mortality.
- Supervisor should evaluate this exact candidate against accepted source. Next
  idea only after evaluation: inspect repeated interrupted recalls if survival
  does not improve. No tournament evaluation or publication performed here.
