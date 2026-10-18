# Current experiment: task-a0e8129eb70343e8a3e378cc10c964be

## Identity and status
- Bot alpha, branch bot/alpha; input HEAD 0b61a3d4f68afab876f551d852202c983703aa28.
- Edit commit 2e82fe1839be5b90390f1c625c0f1f2ec8df7cb5; base source
  eee9346f25577fc3fee419a27bfe416ba0d3b21f9405cca9ac02b24401873133.
  All seven starting files matched edit_commit byte-for-byte. Initial tracked
  differences are trusted preparation, not unfinished work. No patch recovered.
- Latest candidate finished INCONCLUSIVE evaluation; self-play pending matches
  are separate. Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e
  remains in Git. Prior operational notes archived as task-ce64d208150c47a39aaaad25caf3695a.md.
- Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Installed C++ header SHA256 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d verified.
- Routine unchanged-document iteration: compact reference, playbooks B/C/E/F,
  research and organizer ledger, capture rules and relevant C++ navigation/state
  APIs/installed binding consulted. Organizer download hub is not full event-policy
  review; production parity and additional automation policies remain unknown.

## One hypothesis
Prioritizing nearby cleared camps with local collector deference will increase
matched development win rate over the edit base. Unchanged or lower win rate
falsifies this prediction. Collection/tribute and paired-win rounds diagnose the
mechanism. This is an unmeasured rules/source deduction, not a traced loss cause.

## Evidence and decision
- Latest evaluation 3a0d6ab081fe17e2c57f886e47cfc10a0bbdd3c0fa5c41dc2a799d7ee83c3e2d
  measures commit 0b61a3d / source 7a14708a701b4c911b6ec7d9b06a9f379f7bb70018cfc2090cdf906fb45e9ae1,
  NOT the current edit base. 42W/6L, zero faults/missing/unknown reliability;
  matched delta -0.0625 versus edit base across 24 side-paired cases. Optional
  economic recall/field/death shopping did not advance. Do not reapply it.
- Latest-source Expanse A loss 5a49997413c53b1ba3097f2a7eb395bda474e2c14d797e92d771d69f0e2c14cf
  versus frozen alpha 6af1685b / source 87b9be4549dd0ee3a3038907bcfb86b79cfb2d33f344f8749d9532a8e6382e01:
  round 762, tribute 938 vs 1042, zero deaths or champion combat. Cassi did
  16,710 monster damage with zero collected gems. Complete final saved in this
  task's -5a499974-final.json. This suggests inspecting damage-to-reward conversion;
  it does not prove Cassi abandoned captures or that a routing fault caused defeat.
- Exact-base Expanse A loss d31442e3ba9ab8a798d54fa0191c157ebfc43386d4292e2c85a81e8db475b20c,
  evaluation 089fa436cc9f5a5b0108459554430b05581849083c8235228c59e16c52b7b587:
  round 762, 920 vs 1042 tribute, no deaths/combat. Saved previous task final remains
  canonical. That evaluation also has 45W/3L; retain its working combat against
  beta/gamma/starter rather than changing composition or attacking priority.
- Frozen manifest 5d4b65ad199f4bbd1d3d9dc64aad43aba26fa1537cdcbb8847f166ada921e37e
  and all four source sets hash-verified. Current beta d2d57274 and gamma 1b34f42a
  use deterministic melee drafts, group selection and farming item passives.
  Gamma skips rewards already occupied by an ally; beta focuses a chosen group.
  Both incorporate recovery/shopping and hostile-lock clearing. These sources
  differ from older beta/gamma revisions in the development evaluation. Their
  self-play wins are not evidence that any one policy caused improvement.
- Our base attacks any in-range camp before selecting capture movement, so nearby
  rewards can lose priority to fresh attacks. Capture requires five-round occupancy,
  extra allies do not speed it, and leaving resets it (GameRules.md 191-207).
- Prior global reward priority failed (task-fc527578bbbf42f5be88544f50e93a50).
  New rationale: restrict detours to three actual walking steps and defer to a
  collector rather than pulling every champion toward any visible reward.
  Keep negative findings for fixed draft/Strength, shard family, banking priority,
  40-gem batching, spawn-heal-only, broad AoE scoring, dashes and focus fire.

## Candidate policy
- bot.cpp only: before camp attacks, inspect at most 16 local visible groups,
  respecting a 45,000-fuel scan reserve. Group state is queried only when a spawn
  tile is currently visible within Chebyshev radius three. Hidden state is unused.
- Hold if already standing on a cleared group's spawn. Otherwise skip a cleared
  group occupied by a visible ally. Use a fresh blocked board and bounded reachable
  mask to admit only free spawn goals within three walking steps.
- For an unoccupied nearby reward, defer to a visible, alive, empty-bag, nonchanneling
  ally above retreat health if geometrically closer; ties use the engine handle.
  Ally movement budgets are not treated as intent. At most six ally handles scanned
  per local group; Cassi/Issac remain separate bodies. Deference is recomputed each
  turn, not a persistent claim or assumption of shared vision.
- Delegated local spawn tiles are excluded from ordinary farm navigation for this
  turn. No extra shared memory, cached enemy/ally records or altered scheduling.
  Existing four-byte shared round logging remains unchanged; no new protocol.
- If no usable local reward/movement, retain ordinary camp attacks and routing.
  Draft/stat RNG, items, retreat, combat, altar locks, banking, channels and
  dispatcher/yield all match edit base. No action after the new collection move.

## Validation, risks and next step
- python3 experiments/alpha/check_local_capture.py PASSED, exit 0;
  report task-a0e8129eb70343e8a3e378cc10c964be-source-check.json. Checks visibility,
  local free/reachable goals, ordering, deference/exclusion, scan bounds, yield,
  and that all other executable behavior matches edit base. Source checks only.
- git diff --check PASSED, exit 0. Trusted check details appended below.
- Risks: geometrically closer allies may have longer routes, be busy fighting, or
  select another reward; deference can delay collection. Multiple incumbents can
  still split a capture. Local priority can delay profitable attacks or invite
  contests. The three-step path bound does not bound five-round capture time.
  Additional scans can reduce planning fuel; reserve is not measured headroom.
- No comparative games or causal capture/action diagnostics collected for this
  candidate. EngineVersion 0.0.1 in finals is distinct from CLI 2.1.6; relationship
  remains unknown. Deterministic repeats are not independent evidence.
- Next: supervisor evaluates exact checked source against edit base and protected
  champion on varied maps/both sides, comparing matched win rate, collection,
  tribute and paired-win completion rounds. If weaker, inspect deferred/duplicated
  capture timing before widening the radius or adding persistent claims.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact checked source
  9943e525d46b664dc01dffaacf5ee853c77127c062dfefccd57458cea0e36580.
  Report .agent/check-task-a0e8129eb70343e8a3e378cc10c964be.json;
  check:task-a0e8129eb70343e8a3e378cc10c964be:9943e525d46b664dc01dffaacf5ee853c77127c062dfefccd57458cea0e36580.
  Smoke IDs 381da85b6232c5b87775a6b808428772461299e87de444ed817f5b10ca7ce54c
  and 068d5558eb3ee259b095ba3e2d0fd589dc003c5679c8a513e12080cda9d47004.
  Actual local report inspected; it supplies no detailed runtime/fuel diagnostics.
  IDs/exit alone do not prove completed full games or local capture branch coverage.
  Source-file hashes reverified unchanged after the final check. READY_FOR_EVAL;
  no commit, publication, tournament run, official action or strength claim.
