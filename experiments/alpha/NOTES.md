# Current experiment: task-948295a129604524b9b1896c11b5d8ef

## Identity and starting point
- Bot alpha, branch bot/alpha; input HEAD 7f6637f1ef75c76db72aa244f80342016439ae06.
  Edit commit 5f73d0787014e3f712d0eb6234f088fee489b4d8; base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  All eight starting source files byte-matched edit_commit. Initial HEAD differences
  are trusted preparation. Recent tasks are PUBLISHED; latest candidate evaluated.
  Pending self-play is separate. No unfinished patch recovered or reapplied.
- Protected accepted c0cebd720fcd55e2bbb51d57dd2c398889d4071e stays in Git.
  Previous operational notes archived as task-9d1d883be978493496b41980e19b63d4.md.
- Engine/SDK 2.1.6; suite historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  Matching installed C++ header SHA256 verified:
  90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
  Unchanged-doc routine: current skill/instructions, compact reference, playbooks
  B/C/D/F, evidence ledgers and relevant SDK visibility/state/navigation sections
  consulted. Organizer download hub is not a complete event-policy review.

## One falsifiable hypothesis
Approaching visible survivors of an occupied, still-alive camp group increases
matched development win rate over the edit base. Unchanged or lower win rate
falsifies this prediction. Fewer idle occupied-spawn turns, more complete group
clears/collections and earlier tribute diagnose the mechanism. This is an
unmeasured rules/source deduction; no supplied action trace establishes that
these stalls occurred in a named loss.

## Evidence and decision
- Latest evaluation 3c97dd6a36245b5cad4b69dd706a53975e9c397ce90e090184b956d151019de5
  measures HEAD / source 889cd3f658a9a3ad14a454d818654613b1056199ae6e95a71524790f9130d37a,
  NOT the edit base. INCONCLUSIVE, 40W/8L, zero faults/missing/unknown reliability;
  matched development-base delta -0.0416667 across 24 side-paired cases.
  Prior same-turn capture follow-through is not reapplied. Base comparison differs
  from protected-champion delta +0.7083333.
- Latest-source expanse A loss
  32d66986b3e015bed273a1ce61e609cba45837e8c5cdd4749533eaca2af11afe:
  versus gamma 1b34f42a / source 3ce565f6, round 455; collected/tributed 942/942
  versus enemy 1116/1008, no champion deaths/kills, faults A/B 0/0. This is a
  noncombat throughput deficit, not evidence of unbanked alpha gems or a stall.
- Latest-source corners A loss
  b7a380aacb9b192cb732b58a4b4a42586c67dd9c7ebc0e270ab06437cade7038:
  round 399, collected/tributed 624/602 versus enemy 1066/1018, alpha zero deaths
  and three kills, faults A/B 0/0. Kills alone did not win the objective race.
- Contrasting development wins: latest source collision and elkring each 8/8.
  Preserve combat sequencing rather than pooling distinct source revisions.
  Exact metric summaries and identities are saved in this task's -decision.json.
- Base move_towards_closest returns immediately if goals contain self. Farm goals
  contain all eligible spawn tiles even for alive groups. A farmer on a defeated
  member's spawn cannot approach a surviving member outside its current range.
  Capture requires EVERY member dead (GameRules.md 191-207); standing on a spawn
  while alive members remain does not advance capture.
- Frozen manifest SHA256 841d3edacd8caee76f51c49fc7290092885057aa68d04421ecc08e30c01be131;
  all five source sets hash-verified. Inspected beta 9f7ae1c8's Varg/Tavi/Ryth draft,
  persistent group clearing/live approaches, farming passives and recovery/banking.
  Inspected gamma 1b34f42a's melee draft, cost/value routing, live approaches versus
  reward spawn goals, collector deference and respawn observations. Transfer only
  the alive-versus-cleared target distinction, without their composition or economy.
  These sources do not prove runtime causality or official-opponent behavior.
- Banking priority/arrival/batching, global/local capture priority, fixed draft/stat,
  economic resupply, broad AoE, focus fire and dashes remain negative/deferred.
  Cost-aware global route selection is broader than this concrete stall and deferred.

## Candidate policy and limits
- Only bot.cpp and camp_rotation.h change relative to the edit base. Keep random
  draft/stat builds, enemy-first independent combat, any-bag banking, spawn/dead
  altar locks, cooldown memory and exception-safe intentional yield unchanged.
- After ordinary camp combat does nothing, compute normal camp goals. If self is
  already on an eligible goal, inspect only the group containing that spawn.
  Current personal spawn visibility precedes its fresh group.state() query.
- A reward_available or respawning group supplies no approach goals: preserve its
  existing hold. Only a currently alive group may supply targets. Read each member's
  live health/position only after is_visible(); do not pursue hidden/static targets.
- Build attack-range approaches to visible living members of the occupied group.
  Filter fresh blockers so no occupied monster seeds this new navigation. Reuse the
  normal pathfinder once. After a successful walk, refresh combat targets with the
  existing walked=true guard against movement-exclusive abilities.
- Require available move/basic and no move/attack restrictions. At most 16 members
  inspected; scan/action planning stops at the existing 45,000 fuel reserve. No
  extra shared bytes, persistent target state or second movement attempt. Existing
  18,000 combat reserve remains. Fuel headroom is not measured.
- Risks: closing distance may increase exposure/contests; unseen members or members
  after the bounded scan are not pursued. Trigger frequency and competitive effect
  are unknown. This does not repair every live-group stall or route-selection issue.

## Checks and next step
- python3 experiments/alpha/check_occupied_group.py PASSED, exit 0; report
  experiments/alpha/task-948295a129604524b9b1896c11b5d8ef-source-check.json.
  Nine source isolation/safety checks cover unchanged other policy/cooldown state,
  visibility/lifecycle guards, free goals, fresh walked combat and bounded work.
  Initial checker falsely matched "static" in a comment; corrected the checker.
  These are source checks, not runtime branch coverage or a fuel/strength result.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Exact checked source:
  397bef3cd295ec597e604a9e7e19c9a7fff08702a45c70d4b071ea303fcdc78c.
  Actual report inspected: .agent/check-task-948295a129604524b9b1896c11b5d8ef.json;
  check:task-948295a129604524b9b1896c11b5d8ef:397bef3cd295ec597e604a9e7e19c9a7fff08702a45c70d4b071ea303fcdc78c.
  Smoke IDs a2e015e6b5a6c562e05bd651514755ea6955499542b6752c2c1f48c0c4742d54
  and 047963c0c13264b480b74a1694e4142b9b680afef13d10bf6c5747da07a0767b.
  Summary contains no full-game/fuel/branch diagnostics. IDs alone do not prove
  completed competitive games, occupied-spawn branch coverage or improvement.
- Source file hashes reverified unchanged after check; git diff --check PASSED.
  No tournament evaluation, commit, push, agent spawning, official submission or
  promotion performed. READY_FOR_EVAL means a valid candidate, not a strength claim.
- Next: supervisor evaluates the exact checked source against edit base and protected
  champion across maps and both sides. If weaker/unchanged, inspect actual occupied-
  spawn stalls and approach moves before broadening pursuit or changing route costs.
