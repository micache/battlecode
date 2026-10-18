# Current experiment: task-0648f2bdbcf046cfb9be1812a8247adb

## Identity and status
- Bot alpha; branch bot/alpha; HEAD/input/edit commit
  5f73d0787014e3f712d0eb6234f088fee489b4d8; base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  Entry source matched all eight edit-commit files byte-for-byte; clean working
  tree, no incomplete work. Latest candidate has completed evaluation; pending
  self-play is separate. Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e
  still exists in Git. Previous notes archived as task-cf106a770c3345388063fa3eee68243f.md.
- Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Pinned installed C++ header SHA256 verified:
  90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
- Routine unchanged-document iteration, as recorded in trusted handoff. Consulted
  compact reference, playbooks B/C/F, research/organizer ledger, relevant camp
  phase/respawn rules and C++ API/SDK state/static-layout/movement contracts.
  Organizer page is a download hub; production parity/event-policy limits persist.

## One hypothesis
Arrival-aware cooldown eligibility increases matched development win rate over
this edit base. Unchanged or lower win rate falsifies this prediction. Reduced
post-expiry return delay, collection/tribute and paired-win finish rounds diagnose
its mechanism. This is an unmeasured rules/source deduction: no supplied action
trace proves late return travel caused any named loss.

## Evidence and decision
- Evaluation 20a057f89ee416439f7dd9ee3785bcb7cb8201fe7a2a6304f0e6447988135050
  measures this exact edit base: 42W/6L, zero faults/missing/unknown reliability,
  INCONCLUSIVE. Matched previous-development-base delta +0.083333 across 24
  side-paired cases, distinct from the +0.75 protected-champion comparison.
- Exact-base expanse A loss 7cf8782a52a3d2793758c0d9f8f04589e372a85314adf75093ceb66e33eaefb0
  vs gamma 1b34f42a / source 3ce565f6: round 455, tribute/collection 998/998
  vs 1008/1116, no champion combat or deaths, faults [0,0]. Throughput race;
  no unbanked alpha bag explains this loss. Full final saved as this task's
  -expanse-loss-final.json.
- Exact-base collision A loss 34af65daf805731f34cb049ed09102ca4a2f2e131ce8e0227f6dc2d8dc2a732a
  vs beta d2d57274 / source 7daa9117: round 933, tribute 726 vs 1004, deaths
  8 vs 6, faults [0,0]. Full final saved as -collision-loss-final.json.
  Preserve successful combat: the same evaluation has collision B 4/4 wins,
  corners/elkring/interlock 8/8 each, versus expanse 5/8. These are aggregates,
  not action traces. EngineVersion 0.0.1 in finals differs from CLI 2.1.6;
  their relationship remains unknown.
- Frozen manifest SHA256 77dc7e180cfb28e14f94896bc4a9016e9f788de6f624e675d61973d05b08747c;
  all four source sets hash-verified. Beta uses persistent group selection and
  farming draft/items. Gamma uses value/cost routing, collector deference and
  expiring respawn memory, but excludes cooldowns regardless of travel distance.
  Historical alpha and starter route toward nearest groups. These are source
  observations, not evidence of runtime causality or official opponent behavior.
- Edit base's respawn memory improved development coverage, but excludes a group
  until expiry even if reaching it would take longer than its remaining timer.
  Extend that mechanism conservatively rather than importing a different route
  scorer. Prior local/global capture/deference, draft/stat, shard-family, economic
  recall/field/death shopping, banking/batching, broad AoE, travel-dash and focus
  fire experiments remain negative/deferred; none is reapplied.

## Candidate policy
- camp_rotation.h: cache each group's immutable spawn bounding rectangle once.
  Its Chebyshev distance is a LOWER bound to any spawn. For positive remembered
  timers, include a group when now + max(0, ceil(distance / walk_speed) - 1)
  reaches its remembered earliest round. The first move is this round, after
  respawns; subtracting one prevents entering a still-cooling spawn one round early.
- Unknown/expired observations retain base eligibility. A freshly seen zero timer
  still excludes this round regardless of distance; it indicates blocked
  occupancy, not a positive respawn schedule. Fresh alive/reward observations
  clear memory exactly as before. No prediction claims hidden camps are alive.
- Use the same base movement speed as both navigation paths; no dash/teleport
  policy added. Walls, irregular group shapes and blocked paths can lengthen a
  trip, so the geometric bound deliberately misses some useful early departures.
  Existing nearest-goal pathfinding still decides actual route and legal movement.
- Private per-instance geometry only; no extra live group queries, shared bytes
  or inferred ally vision. Existing 16-observation/45,000-fuel limits retained;
  extra per-cooling-group arithmetic is constant. No new search/scan each turn.
  Initialization still scales with static layout. Runtime fuel impact unmeasured.
- bot.cpp changes only the explanatory farming comment. Executable draft/stat,
  combat, channels, banking, captures, recovery, locks and yield remain edit-base.

## Checks, risks and next step
- python3 experiments/alpha/check_arrival_rotation.py PASSED, exit 0; report
  task-0648f2bdbcf046cfb9be1812a8247adb-source-check.json. Verifies unchanged other
  executable policy/observer, visibility, static metadata, budgets, memory and yield.
- Trusted compilation includes prior temporal tests and new static_asserts:
  exact-deadline versus one-round-early arrivals, speed two, zero distance/speed,
  zero-timer/unknown handling, rectangle bounds, and 2,000 coordinate/timer cases
  proving admitted fastest walks do not enter either tested spawn before deadline.
  Pure policy invariants; no engine timing fixture or branch-coverage claim.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Exact checked source
  6e362fd7cce836975fa615bc8b936109235fd320def63703761366586efabc25.
  Actual report inspected: .agent/check-task-0648f2bdbcf046cfb9be1812a8247adb.json;
  check:task-0648f2bdbcf046cfb9be1812a8247adb:6e362fd7cce836975fa615bc8b936109235fd320def63703761366586efabc25.
  Smoke IDs f3da9e07a23bd2822b35465aac73076e5587bdcf5f0ab59c7ee75934ef65c302
  and 4c628d417b3456531f269f59bd5258a5bec07355798eed6f2ec156fd0e1e1cce.
  Summary gives no full-game, fuel or coverage diagnostics; passing is not proof
  of competitive improvement. All source file hashes unchanged after check.
- Risks: earlier returns may reduce exploration/crowd allies; blockers can postpone
  respawn beyond a remembered deadline; rectangular bounds can miss useful trips;
  additional initialization/arithmetic consumes unmeasured fuel. No measured gain.
- READY_FOR_EVAL. Supervisor compares checked candidate against edit base and
  protected champion across maps/both sides. If weaker, inspect return delays,
  early spawn occupancy and duplicate trips before changing geometry or routing.
  No comparative tournament, commit, publication or official submission performed.
