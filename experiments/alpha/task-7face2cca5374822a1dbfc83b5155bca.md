# Current experiment: task-7face2cca5374822a1dbfc83b5155bca

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD db854271fc4f1c1d075af3ec55ceadcca4c69c7c.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry identity, branch, HEAD, all six source-file hashes, documentation and
  installed C++ header hash match the trusted envelope. Entry diff is the supplied
  restoration from latest candidate to accepted source, not unfinished new work.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest candidate evaluated INCONCLUSIVE, not pending. Prior notes archived as
  task-adc0e4b46bef4259b242f5d17c07a43b.md. Older recovered work remains preserved;
  no recovery applied. Accepted Git snapshot remains outside this transaction.
- Routine iteration: compact reference, RESEARCH.md, playbook D and relevant
  handbook/SDK sections read. Separate organizers' AGENTS.md remains absent.

## One hypothesis: playbook D, lethal enemy spells
Using a ready direct-damage spell when its target-specific SDK damage prediction
is lethal to a visible enemy in range will increase mean champion kills versus
accepted source on matched development cases. Unchanged or decreased mean kills
falsifies this prediction. Compare submitted gems, deaths and outcomes to assess
whether those kills help the objective.

## Evidence and change
- Evaluation 5e09e06049bf37ce6fe0f87c48e8d33817237eb134c9fe5c8a45e64dd1704e65:
  commit db854271fc4f1c1d075af3ec55ceadcca4c69c7c; source
  ea2cdb8e32b90b6be32b2f2d3775b35eb5461619eb465e6f62bc9ed952ac22b3,
  NOT the accepted edit start. 8W/16L, matched delta 0.125, zero faults/missing.
- Collision B loss 3779a5cad389dccec52bc67023d5bb36f66bfe5fb68adcb81d5c45193631bd50:
  35 deaths, 14 kills, 902 collected, 660 submitted vs 1012, round 1311.
- Collision A loss bfeb0d087ac3c3fa9ce447508b9ccac19d9b057165350bb8e859684abb823e3c:
  19 deaths, 5 kills, 484 collected, 352 submitted vs 1012, round 880.
  Both report zero bot faults on both sides. These are strategic losses with no
  identified engine failure. Supplied evidence saved in this task's -evidence.json.
- Neither final aggregates nor existing logs establish lethal spell opportunities.
  Source reproducibly never casts, even when a ready spell could finish an enemy
  outside basic range or overcome a shield. Kill rewards include the victim's bag.
- Add one bounded helper before enemy basics, after existing channel/recall guards.
  Scan visible living enemies and exactly two SDK ability slots. Require direct
  damage kind, readiness, enemy target permission, range and target-specific
  predicted health loss >= current health; attempt at most one cast, then return.
  Successful cast ends the turn; False/no opportunity uses existing basic/bank/farm
  fallback. No movement precedes the helper, so walking-exclusive spells are safe.
- Unlike previous camp-damage/reset trials, this changes only enemy finishing;
  camps never receive spells, and nonlethal enemies do not trigger a cast.
  No new state, memory, RNG, thresholds or draft changes.
- GameRules.md 259-266, 361: one successful cast, visible unit targets, kill rewards.
  cambc.h 3161-3204: range alone does not prove legality; 3276-3279 and 3821-3827:
  target-specific damage includes mitigation/shields and caps at health.
  3861-3867: readiness checks cooldown and can_cast; use(champion) returns bool.

## Validation and uncertainty
- git diff --check PASSED, exit 0. Accepted-relative source review: only the
  finishing helper and its pre-combat call in bot.cpp; other five files unchanged.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact checked source
  6f074a287b029d03848eb2ad3aef1ad7f11d5b5977f1a28f87d9f3edd21fe549.
  Report: .agent/check-task-7face2cca5374822a1dbfc83b5155bca.json.
  Reference: check:task-7face2cca5374822a1dbfc83b5155bca:6f074a287b029d03848eb2ad3aef1ad7f11d5b5977f1a28f87d9f3edd21fe549.
  Smoke IDs 7556dd966a8808cc42b054b9da773ca523fe4db4fdef7095372e1c47e4f3ba2c
  and 6f4c771f407c85689f920dd38d7c9c0a6f368e91c75703d9d591511c0e72081f.
  Finals/action logs not inspected; IDs alone prove neither completed games nor
  finisher branch coverage. No tournament evaluation or strength gain claimed.
- READY_FOR_EVAL; source unchanged after trusted check; no publication performed.
- Opportunity frequency, cast branch coverage and fuel headroom remain unknown.
  Killing can expose Ren retaliation or linked-death effects; spending a turn on
  a kill may delay banking or capture. The damage query is a prediction, not a
  measured kill assertion. Only direct damage kinds are considered.
- Next: supervisor evaluates the exact checked source against accepted, comparing
  champion kills, submitted gems, deaths and outcomes. If kills do not increase,
  inspect opportunity coverage before expanding spell use.
