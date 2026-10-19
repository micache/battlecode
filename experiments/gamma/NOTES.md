# Gamma operational notes

## task-2ecb2c23987f429987e000036c718854 — bounded farming planner

- Refinement; one candidate. Branch bot/gamma, HEAD/input
  bf1faccc8aa1c733641d7e02e20f53740d4bedd8. Actual edit commit
  ecbc8203fd2ef0696ef7784c8b39528bb182ad7b; base source
  ff511c52577a0f42c5e17329423aaa100b0317ddcaf037f8b2ba59b808061671.
  All six initial source files matched this edit commit. Initial bot.cpp/bot.h
  differences from HEAD were the trusted restoration, not unfinished work.
  Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains outside
  this edit transaction. Latest candidate evaluation completed; nothing pending.
  Prior notes preserved in archive/task-d0408f5c94104b45803559ea6f03050a.md.
- Hypothesis: bounded value-ranked farming scans with committed and rotating
  probe slots reduce fuel suspensions and increase matched development win rate
  versus ff511c52 without new bot faults. No win-rate gain, no suspension
  reduction on affected maps, or any new bot fault falsifies the hypothesis.
  Actual wins and unchanged promotion gates determine selection.

## Policy and implementation

- Keep Varg/Vendetta/Marcella/Ryth/Tavi draft, Jungle Strength, Monster Strength,
  one Durability Health then Power Strength; bank every positive bag, 35% retreat,
  98% spawn healing, safe 300-gold recall, route locks and existing combat.
- Base planner scans in static map order until 30k fuel remains, then still needs
  movement, refreshed observations and combat. Repeated SDK goal-distance reads
  and group/camp queries can consume action headroom; a truncated scan also
  favors map-prefix groups. This phase attribution is a SOURCE deduction, not
  a measured phase-resolved fuel trace.
- Cache group center and initial design health once. Rank using geometric travel,
  initial health/current Strength and the existing gems + 0.12*gold value.
  This is an uncertain design estimate, not hidden live health or reward state.
- At most 12 full live group evaluations: committed group first, one rotating
  probe next, then best estimated value/time ranks with index tie-breaking.
  Probe advances once per planning invocation, not during channels/captures.
  It prevents permanent shortlist exclusion if sufficient scan fuel remains;
  a probe can still be skipped when the fuel guard ends the scan.
- Retain exact reachable travel/remaining health/reward scoring, 0.85 commitment
  hysteresis, respawn observations, monolith exclusion, ally collector avoidance,
  capture occupancy and post-capture vacating. These apply to checked candidates.
- Start/continue optional planning only with >=55k fuel. Recheck after the global
  field. Below that, use the existing bounded eight-camp local combat fallback.
  No movement/combat/banking rewrite, new global search, shared memory or fuel
  override. The old 30k planning constant is otherwise unchanged.
- farm_plan.h contains compile-time tests of the ACTUAL scheduler: empty/zero
  limit, committed priority, wrapped probes, deterministic ties and exhaustive
  sizes 1..16 checking bounded unique valid indices and probe inclusion.

## Evidence and limits

- Evaluation 2775caccb0d3126bed349be93be239a810579e530cd3c0e09d928f5dd9242628
  evaluated bf1faccc/c44b1194, not this edit base/candidate. 104W/32L, no faults;
  development-only 85W/27L and matched development-base delta 0 over 56 pairs.
  The capture-entry experiment was not selected; it is not bundled here.
- That candidate's Ambush B loss
  931f11543f64fc2ece50f22c77d3e83dd2f61782b014c7f592acbda489736b2c:
  round821, 774 vs1018 tribute, 11 vs4 body deaths, four own fuel suspensions,
  zero faults. The saved first log-page sampled minimum is 70. Opponent
  revision is unknown from the slice; no per-turn scan cost is established.
- Same-source Collision A loss
  e66d414eafd3b3e140ed0275bbe8c9606a6cbe25a3e7e4920e6804c6f5f0bec2:
  556 vs1020 tribute, seven deaths, 216 bag loss, no faults/suspensions.
  Thus fuel is not a universal explanation of strategic losses.
- Exact-base Ambush A loss 46169b0b3c07969ecdaaf079e30dc16aa4d64b59d28ae87ae0549d0709cbe3ec
  was round935, 960 vs1010 tribute, eight deaths and one own suspension per
  prior capture-entry-matches.json. Fresh first-log excerpt samples minimum1362.
- Contrasting exact-base Collision A smoke win 41c22e31989d7f3134bb2f4da0afdcc16f151d72d994fd90a6b1f14dff082ff0:
  round716, 1028 vs66 tribute, no faults/suspensions; altar-control-smoke.json.
  Different matches/opponents are not controlled performance comparisons.
- Frozen manifest be88f510fbf6c082914cc7f49f49db1c4fa5cffd0be20cff0b3a68c25a95ed0c:
  inspected and hash-verified beta7cab9b0f/fd5e2554 and alpha82a14a04/6e362fd7.
  Beta's Varg/Tavi/Ryth build uses 12-group geometric shortlisting, recovery,
  shields/dashes and route locks; its economy penalty is a separate policy.
  Alpha uses random draft/Power stats, bounded combat and timed camp rotation.
  Adapt only bounded live evaluation, preserving gamma's exact value scoring
  and adding rotating coverage. Frozen source is policy evidence, not runtime.
- Prior target-aware combat, claims, threat-aware banking, protected transit and
  Ryth draft changes were not selected. Do not repeat without changed evidence.
- Details: bounded-farming-evidence.json; isolation: bounded-farming-source-review.json.
  Routine unchanged-doc iteration: BOT_REFERENCE, playbooks B/C/D/F/G,
  RESEARCH/organizer ledger, C++ group/field contracts and installed SDK reviewed.
  SDK SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264
  verified; engine2.2.5/lock0cabb3c7; suite published-17-release-225-v1.
  Organizer download hub is not complete policy review; production parity unknown.

## Checks, risks and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json: PASSED,
  exit0, exact source 72b489b0df56d0d7dcd842db50deac20ddf82c065c3001ea9f6d0b943d6fc944.
  Report .agent/check-task-2ecb2c23987f429987e000036c718854.json. Compile-time
  scheduler assertions passed in the trusted build. No source changed after launch.
- git diff --check: PASSED, exit0. Manual source isolation/safety audit passed.
- Both completed Collision smokes (mapHash ebfcace1, engine build d7e29ae3)
  have zero faults/suspensions on BOTH sides. A b3aa8806: 1064 vs66 tribute,
  round730; B bdd68fd8: 1066 vs198 tribute, round884. Own logs contain no
  bot-error/suspension markers; sampled minimum remaining fuel 33711/33659.
  Full summaries/logs: bounded-farming-smoke.json. Opponent revisions unknown;
  smoke wins and headroom do not establish matched strategic improvement.
- Risks: initial-health/geometric rank misses partially cleared or distant free
  rewards until probed; narrow routes invalidate the estimate. A higher reserve
  may use the local fallback too often. One large group or path query can still
  exhaust fuel; a 12-group cap is not a proof of headroom on every map.
- Next: supervisor evaluates this checked source against ff511c52 on matched
  development maps/sides/opponents. Compare wins, tribute, fuel suspensions,
  idle/stale turns and collection; include both Ambush and zero-suspension
  Collision controls. If throughput regresses, inspect shortlist exclusions and
  fallback frequency before changing combat or increasing candidate count.
