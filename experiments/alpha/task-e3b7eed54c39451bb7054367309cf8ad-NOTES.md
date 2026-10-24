# Current experiment: task-e3b7eed54c39451bb7054367309cf8ad

## Identity and status
- Alpha / bot/alpha; input HEAD 3dcf8559f994e64bdbe383448fdd6e4c6677e11a.
  Actual edit commit 5f73d0787014e3f712d0eb6234f088fee489b4d8; base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
- Initial eight source files byte-matched edit_commit. HEAD-relative changes and
  missing recovery.h/skirmish.h are trusted preparation, not interrupted work.
  Latest published candidate was evaluated. No pending evaluation was polled.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
  Prior notes preserved under task-cff7df...-NOTES.md. No source backup needed.
- Task strategy.phase=foundation; context/brief mode=exploration. Built a coherent
  farming vertical slice from this older source and current rules.
- CLI 3.0.5, bundled engine 1.0.3; lock ac2b5ad2...c56136;
  suite published-40-release-305-v1. Matching SDK header hash verified:
  894229e17d886358719abb70cac9ab5993263a0c05bf7df14fc48fa04a8336d3.
- Changed-document review: current full rules, reference, C++ export audit views,
  matching installed header, playbooks A/C/D/E/F/G, RESEARCH and organizer ledger.
  Current source/document hashes and material findings saved in decision JSON.
  Organizer page is a download hub; full policy/production parity remain unknown.

## One hypothesis and falsifier
A fixed Strength farming composition with committed, risk-priced whole-group
clearing and capture will increase matched development wins over edit base
ba646c6e. Unchanged or lower win rate falsifies the prediction. Higher submitted
and collected gems and fewer camp deaths would support the mechanism; faults and
fuel suspension diagnose regressions. The edit-base bottleneck is a source/rules
deduction, unmeasured by the older-source losses below.

## Evidence and audit
- Evaluation 2baf2f19...6507f8 measures 3dcf8559 / 9b5dc610, NOT this edit base:
  protected comparison 206W/194L; development 191W/179L; matched base delta
  -0.059459 over 185 side pairs. Zero faults/missing/unknown. Do not interpret
  its +0.3525 protected delta as improvement over the development base.
- Latest evaluated side A 01fracture loss 61a5b358...6039: completed round 1638;
  tribute 288 vs 1024, collection 358 vs 1054, deaths 29 vs 11; own monster
  damage taken 53350 vs champion damage taken 700. Own faults/suspensions zero.
- Latest evaluated side B 01fracture loss 391ad9d1...70e3: completed round 2000;
  tribute 846 vs 984, collection 897 vs 1073, deaths 24 vs 14; faults and
  suspensions zero. Final summaries are saved, not causal per-turn traces.
- Contrast: same evaluation's 00stampede candidate fraction 1.0 over five pairs.
  Aggregate only; no invented win trace or statement that one tactic caused it.
- Manifest 562c68fe...373fee and all six frozen source file sets hash-verified.
  Current boss ea15ef0f / f4b4f65e: Vendetta/Varg/Ryth, value/work group routing,
  claims, Jungle/Monster builds, bank at 30/nearby, local-power PvP. Beta 7cab9b0f
  uses Varg/Tavi/Ryth, group value penalties and dashes. Source ideas, not proof
  of official behavior. Old comments about lock hits/SDK visibility are stale.
- Base lacks value/work routes, committed clearing, explicit capture priority,
  sensible stat/kit coupling, dead shopping, Tavi field shopping and reliable
  spawn healing. Prior PvP disengagement regressed its own development base;
  do not simply retune that threshold or reapply narrow camp target-focus.

## Candidate policy
- Legal deterministic picks: Vendetta, Varg, Marcella, Tavi, Vesper (up to actual
  map draft size). Complete one Jungle Strength emblem, then Power Strength.
  Shop on spawn/dead; Tavi shops in the field. No random stats or RNG routes.
- Cache immutable group metadata; prepare at most 16 members/turn. Observe the
  selected group and up to 12 rotating groups with personally visible spawns.
  Cooldowns retain exact observed round/expiry; hidden reward state is not truth.
- Scan at most 64 group candidates and 128 member geometry samples/candidate.
  Score (8*gems + gold weight*gold) / ((path distance + estimated clear + 7)
  * (1 + 2*estimated damage/current health)). Gold weight 1 below Strength 100,
  else .3. Use SDK base health/strength/camp multiplier and completed Jungle.
  Splash estimate 1.6; reset allowance average 1.125; risk factor .55. Heuristics,
  not engine combat predictions. Soft risk penalty avoids infeasible-only idling.
- Retain route with 1.25 score bonus; after dealing damage, commit to the visible
  live group until clearing, recovery or blockage. Restrict camp basics/casts to
  this group; preserve existing combat legality and fresh target selection.
- Finish capture before new fights/banking while on the current reward region.
  Skip fresh rewards already occupied by a visible ally. Cooling groups are
  excluded; moving to another target/bank vacates their respawn region.
- Use free approach/capture tiles, dynamic occupancy and at most one movement
  retry after refreshing a hidden-blocker reveal. Blocked target retries after 6.
  Score paths ignore temporary units; actual movement includes them.
- Keep prompt banking; adjacent tribute before incidental PvP, and recheck after
  moving to bank. Recovery starts at 35%, persists to spawn, waits there to 95%.
  Quiet zero-bag sorties recall to spend 150 gold; Tavi does not need this trip.
- Planning reserve 42000; observations 58000; metadata 70000; combat 18000;
  navigation 22000. Guards are planning budgets, not measured minimum headroom.
- No writable team or draft memory used. Private state only; main still catches
  failures and intentionally reaches official end_turn. Locks unchanged.
- Risk: work uses full static HP; no rich teammate reservations/opening roles;
  group duplication persists; capture priority may defer a useful bank; distant
  geometry samples may miss entrances. PvP and mobility remain limited. Large
  layouts need several metadata turns. Combined policy has no isolated ablation.

## Checks and handoff
- Initial source 2e89c0a1...7af4e passed bot-check, exit 0. Interim smoke summary
  belongs only to that source. Review then added explicit group commitment and
  bounded metadata preparation; initial wrapper facts saved separately.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; source a309a76d56574ef4e5ac1c8d3ff06865710e0d280967f9a2cea3a940c23cc000.
  Report .agent/check-task-e3b7eed54c39451bb7054367309cf8ad.json, copied to this
  task's -bot-check.json. No bot source edits after that check.
- Final smoke ab4eacb6...933372 and e5b22e37...6a68bfa each report COMPLETED,
  zero bot faults and zero fuel suspensions. Saved final-smoke-0/1 summaries link
  exact source. Wrapper omits candidate-side/opponent-source metadata; no matchup
  strength attribution. Smoke does not prove branch coverage or all-map headroom.
- Constexpr checks compile: throughput favors less work/risk and greater value;
  inherited cooldown tests enforce exact expiry and zero-timer occupancy semantics.
- git diff --check PASSED, exit 0. Final file hashes, branch/HEAD and exact-source
  smoke references reverified after all bot edits; no normal-fuel override.
- Next: supervisor compares this exact checked source to edit base and protected
  champion on matched maps/both sides, monitoring wins/submissions/collection,
  camp mortality, faults and fuel. Reject no win gain. Then consider visible
  worker deference or more precise remaining group work if diagnostics warrant it.
- READY_FOR_EVAL is validity only. No agents, commit/push, tournament invocation,
  publication, official action, account changes or waiting for evaluation.
