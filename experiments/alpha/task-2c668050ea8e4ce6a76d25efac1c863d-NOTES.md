# Current experiment: task-2c668050ea8e4ce6a76d25efac1c863d

## Identity and status
- Alpha, bot/alpha; HEAD/input 27f6a3b5a11e07188672d830decd2d49d61e498d.
- Edit 5f73d0787014e3f712d0eb6234f088fee489b4d8 / source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  All eight starting source files byte-matched edit commit. Deleted
  camp_navigation.h and camp_rotation.h changes from HEAD were preparation.
- Latest candidate 27f6a3b5 / a665435f completed INCONCLUSIVE evaluation; none
  awaiting evaluation. Protected c0cebd720fcd55e2bbb51d57dd2c398889d4071e stays in Git.
  Prior notes archived as task-73a204dcf7c2439ba03fc9f074bb101f-NOTES.md.
- CLI/SDK 3.0.5, lock ac2b5ad2...c56136, published-40-release-305-v1.
  Trusted handoff says documents unchanged. Compact reference, playbooks B/C/D/E/F,
  research/organizer ledger and relevant current C++/SDK item/stat/ability sections
  consulted. Organizer hub is not a review of all policies; parity limits remain.

## One hypothesis
Replacing randomly locked Power-shard stats with kit-aware marginal sustainable-
damage allocation and completed spawn healing increases matched wins and collected
gems over ba646c6e. Unchanged or lower matched wins falsify the prediction.
This is an unmeasured rules/source hypothesis, not a demonstrated causal diagnosis.

## Evidence and choice
- Evaluation e1465dc0...14e80e measures 27f6a3b5 / a665435f, NOT current base.
  Full 228W/172L, zero faults/missing/unknown reliability. Development-base delta
  -0.0054054 over 185 side pairs. Do not reapply the live-approach routing trial.
- Later-source ambush A loss 7e62891491257a8791774fa409aa1498d4006bc6a2bae57ca456132459ae14d0:
  round 1727, tribute 585/1043, collection 585/1080, own deaths 20, enemy kills 5;
  own camp damage taken 55195 vs 4310 champion damage taken. Own faults/fuel
  suspensions zero. Summary: Ren Focus build, 8 deaths, 36 collected, no PvP damage.
- Later-source ambush B loss b818808203c2859d85fd64b628c9af59a2d0dcfab52615072e9990a56da4f3ac:
  round 1888, own tribute 673 vs 1027, own collection 761, own deaths 16, enemy
  kills 1; camp damage taken 67920 vs 2414 champion damage taken. Own faults and
  suspensions zero. Summary: Focus Vendetta 9 deaths, 55 collected. These establish
  camp mortality, not that shopping choices caused the losses. No action trace.
- Contrasting same-candidate development aggregates: pilgrimage 10/10 wins,
  stampede 9/10, starfish 9/10. Preserve random draft and successful base combat.
- Frozen manifest 8db6184d...28499 and all six source sets hash-verified. Inspected
  boss ea15ef0f / f4b4f65e: fixed draft, Jungle/Monster/Power Strength, group routing,
  spawn healing; gamma f01d496c / 54c19acf: staged equipment and spawn healing.
  Arena sources are not proof of runtime or official behavior. No private notes.
- Earlier first-Jungle, fixed roster/Strength, economic recall/dead/field shopping,
  spawn-heal-only, focus, deference and broad disengagement remain negative or
  deferred. This changes stat allocation from actual kit/growth and current stats;
  it does not repeat a fixed composition, fixed stat or new item family.

## Candidate policy
- New equipment_policy.h: local greedy Power-shard simulation maximizing
  effective health * estimated stationary damage-per-round squared. Speed is
  weighted twice, survival once. Three SDK growth values; actual current stats.
- Price basics plus attack-reset rate and used camp-target damage/CC/AoE modifiers
  divided by configured cooldowns. AoE/basic splash assume 1.5 targets; shield
  survival credit is half its Focus scaling. Ren assumes one incoming basic/round;
  Ryth Health also adds SDK passive Strength. Do not price unused dash damage or
  Willow healing as self sustain. These workload assumptions are not measurements.
- Include fifth Power shard's extra growth point. Use SDK cost/combine count and
  current item residues. At most 64 local choices, then three can_buy/buy batches.
  Shop only at spawn as before; entry reserve 45k, purchase reserve 28k. No new
  recall trigger, dead/field shopping, item family, shared bytes or hidden reads.
- Retain base stat RNG draw as equal-score preference, preserving RNG consumption.
  After shopping, stay on spawn if injured and allow existing stationary champion
  combat before yielding. Health purchases on spawn heal their increment instantly
  (rules line 323); turn-end healing restores the remaining earlier injury.
- Draft, ordinary combat, farming/rotation, banking, locks, retreat threshold,
  movement, four shared round bytes and exception-safe official yield retain base.

## Checks and next step
- Initial trusted build FAILED exit 1: incorrect passive constant namespace;
  saved -initial-bot-check.json. Fixed to installed SDK passive_abilities.
- Intermediate trusted check PASSED exit 0, source 0fe81b3f...54a1bc1;
  saved -intermediate-bot-check.json, superseded by the final source below.
- Embedded constexpr checks: offense for reset kit, health after high offense,
  Focus when kit growth supports it, Ryth Health/Strength coupling, fifth-shard
  completion bonus, zero budget, invalid combine count and 64-purchase bound.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED exit 0. Exact checked source
  dd7c6c996f40dd12888dd3e3d6e877bdf574fbd3bb16a19060260f2c33931599.
  Actual report .agent/check-task-2c668050ea8e4ce6a76d25efac1c863d.json;
  saved copy task-2c668050-bot-check.json. No source edits after this check.
- Final exact-source smokes 9cf086d7...ad919 and ccfc1c64...dc5f0c both
  COMPLETED, zero faults and suspensions on both sides. Full summaries saved as
  task-2c668050-final-smoke-{0,1}.json. Map hash 6e3c6795...5620. Check does not
  identify candidate side/opponent version; scores are not attributed as wins.
  These deterministic smoke games are not independent competitive evidence.
- Source comparison against actual edit base PASSED: only bot.cpp, bot.h and
  equipment_policy.h differ. Removed intended shop integration to verify all
  remaining bot.cpp policy is byte-identical. Hashes recorded in -source-check.json.
  Initial HEAD-relative camp header changes are preparation, not this candidate.
  git diff --check PASSED. READY_FOR_EVAL means valid, not proven stronger.
- Risks: safe clusters may prefer pure damage; movement/target contention and burst
  are unmodeled; partial emblems, delayed purchases and extra healing can lose tempo;
  linked twin death is unmodeled. No measured all-map shop fuel headroom or strength.
- Next: supervisor evaluates exact checked candidate against edit base and protected
  champion across matched maps/sides/opponents. Compare wins, collection/tribute,
  camp deaths and reliability; reject nonpositive matched gains. No agents,
  tournament invocation, publication, commit/push or official submission.
