# Current experiment: task-c774f333829146d98d61007f25d7165e

## Identity and status
- Alpha / bot/alpha. Input/HEAD 643bcf708dd9236d6c4dbd240104ae418095b5ff.
- Actual edit commit 1f5e71f3111c5a492a20f4aaf0bbd3bd0c6fff97, source
  dd7c6c996f40dd12888dd3e3d6e877bdf574fbd3bb16a19060260f2c33931599.
  All nine starting source files byte-matched edit commit. HEAD-relative removal
  of the later Jungle experiment was trusted preparation, not interrupted work.
  Latest evaluation is complete; no candidate awaiting evaluation.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e preserved in Git.
  Prior latest NOTES archived at task-3d6485a995384e9c9fdd47134d1df792-NOTES.md.
- CLI/SDK 3.0.5, lock ac2b5ad2...c56136; published-40-release-305-v1.
  Unchanged docs per handoff: consulted compact reference, playbooks B/C/D/E/F,
  research/organizer limits and targeted rules/API/installed C++ design contracts.
  Organizer hub is not a review of all policies; parity limits remain explicit.

## One falsifiable hypothesis
Kit-aware farming draft selection using opening Power growth increases matched
wins and tribute over dd7c6c99. Nonpositive matched win gain falsifies it.
This is an unmeasured source/rules prediction, not a proven draft diagnosis.

## Evidence and decision
- Latest 15cb2761...0692b evaluated 643bcf70 / 3a354ce7, NOT today's edit base:
  275W/125L full suite, faults/missing/unknown zero; development delta +0.03243243
  over 185 side pairs vs this base. Earlier Power allocator gained +0.08648649
  against its own prior base. Do not conflate either with champion promotion.
- Later-source ambush B loss f559889ffeacc0401839c065cd71b0dd8ff64e51ec508f9b5049b0ccc5e282f3:
  completed round 1825, own tribute/collection 859 vs 1021; own camp damage taken
  62696 vs 11692, own champion damage taken 1675; own deaths 10 vs 7. Own faults
  and fuel suspensions zero (opponent suspensions 9). Vendetta: 4 deaths/55 gems;
  Ryth: 3 deaths/78 gems; Vesper: 1 death/381 gems. These results also warn that
  stationary draft scores may undervalue ranged economy. No causal action trace.
  Saved full summary task-c774f333-loss-b-summary.json. Initial --limit requests
  were rejected by CLI parsing; proper offset pagination recovered this summary.
- Contrasting latest-source development pilgrimage/stampede/starfish each 10/10
  over both sides (brief aggregates, no individual win trace inferred).
- Frozen manifest 102bd8a7...a295d and all six source sets hash-verified. Inspected
  shared boss ea15ef0f / f4b4f65e draft/config, combat and route scoring: fixed
  Vendetta/Varg/Ryth first; Jungle/Monster/Power builds; group work/risk/claims,
  30-gem banking and recovery. These are source strategies, not official behavior.
  Our model independently selects the same three opening farmers in smoke;
  broad strength versus that boss remains unknown. No private state accessed.
- Prior fixed melee/random-stat packages were negative. This trial changes the
  rationale: actual kit/growth scoring is shared with the subsequently successful
  allocator, rather than a fixed roster/stat guess. Still risks repeating a loss.
- Rejected: same-turn Vendetta chains (kills reset cooldowns, not cast allowance);
  aggro-control assumption (group/individual wake wording unresolved). Earlier
  routing, focus/AoE, banking, deference, dashes and economic recall remain negative
  or deferred. Latest selective Jungle showed a development gain but is not on
  this edit base and is not silently reapplied. See task-c774f333-decision.md.

## Candidate policy
- Extract existing shop model into equipment_model.h without formula changes.
  Draft reads immutable champion designs and base stats; shop supplies live self
  stats exactly as before. H * estimated sustained damage squared, AoE 1.5,
  shield credit 0.5, kit modifiers/growth, original Power allocation all retained.
- Score all twelve released picks at base and after five locally optimal Power
  shards; sum the two values with equal weight. SDK combine count gives the
  fifth-shard bonus correctly. Include Heart of Ruin; only currently used combat
  abilities are priced (no speculative dash/missing-health damage credit).
- Cassi/Issac is one pick, two physical design scores. Sum them, then apply fixed
  0.5 linked-survival credit for two death exposures. This is an assumption.
- Cache twelve scores on the enlarged first draft turn. Later turns scan twelve
  entries; exclude own picks and respect SDK team_size. Seeded cyclic tie-break.
  No camp/map reconstruction, opponent-state reads, new shared bytes or routes.
- Hello-world draft memory and official exception-safe yield remain. Existing
  combat, farming, banking, recovery, shop timing and RNG in play retain base.

## Checks and limits
- Source contract initially FAILED as expected: draft still chooses a uniformly
  random pick. Then python3 experiments/alpha/check_kit_draft.py PASSED exit 0.
  This checks integration, not runtime strategy. Pure semantic cases compiled in
  trusted build: equal scores, unavailable top pick, all twelve unique legal
  selections, exhausted pool, growth improvement, invalid combine, sixth point.
- Source comparison PASSED: bot.cpp changes only model extraction; extracted
  model body matches base after variable rename; every other old source besides
  draft.cpp byte-identical to edit commit. task-c774f333-source-check.json.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED exit 0. Exact checked source
  57b163e2dbd68672164422bbd617bd280dc120b09ec2761d3bc331a6464b3b35.
  Report .agent/check-task-c774f333829146d98d61007f25d7165e.json;
  owned copy task-c774f333-bot-check.json. No source edits after check.
- Smokes d9d490ba75ce614610e0096b70abf3183de5611d0c45243a3d80325ee7d2ccb4
  and dc1b86652c9d960d8227c5435234db0fe970600feb8254a9dc3c9d3ab31c67dd:
  both COMPLETED, zero faults and fuel suspensions on both sides. Map hash
  6e3c6795...5620. Full summaries task-c774f333-smoke-{0,1}.json. Candidate
  side/opponent revision not explicit in wrapper; no competitive win attribution.
  Same deterministic inputs are not independent performance trials.
- git diff --check PASSED. Trusted check is scoped bot suite; arena infrastructure
  tests are not bot verification and were not invoked. No agents, commit/push,
  evaluation polling, tournament or official submission invoked.
- Main risk: static survival/clear scoring ignores mobility, range, map topology,
  bonus income and support value, and may converge on the boss's opening roster.
  Model shield/splash exposure and twin hazard are unmeasured. All-map reliability
  and five-pick selection quality remain to be evaluated.
- Next: supervisor compares exact checked source against edit base, protected
  champion and frozen opponents under unchanged gates. Assess matched wins,
  tribute/collection, mortality and reliability; reject nonpositive win gain.
  READY_FOR_EVAL means a valid candidate, not proven stronger.
