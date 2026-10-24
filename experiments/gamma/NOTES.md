# Gamma operational notes

## task-fb147fa32a584508b58c80f102eede3a — keep farming after melee defense

- Exploration; bot/gamma, input3bbf4cb6, actual edit f01d496c / source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting files matched edit commit. Prepared three-file restoration
  was intentional; no incomplete worker patch. Latest own candidate evaluated,
  not pending. Accepted champion1a0675ca remains outside this edit transaction.
- Hypothesis: preserving melee movement after defensive hits, with lower visible
  contact pressure as a shortest-path tie breaker, increases matched wins AND
  mean tribute over this edit base without new own faults or fuel suspensions.
  Nonpositive win/tribute gain or new reliability failures falsifies it.
  This is an UNMEASURED rules/source deduction, not a replay-proven cause.

## Evidence and decision

- Latest evaluation fdd951e7, source6c103723/commit3bbf4cb6: INCONCLUSIVE,
  319W/81L overall, no faults. Matched development delta vs edit base -0.0027027
  over185 side pairs; development292W/78L, bag loss65.91, deaths8.06. These
  scores evaluate arrival-aware returns, NOT today's restored source/candidate.
- Completed supplied loss69831575, A/00ambush, that later source: tribute393
  vs1020, collection581 vs1036, own deaths6, bag loss151, faults/suspensions0.
  Loss3ca1274b, B/00collision, same source: tribute916 vs1093, collection1246
  vs1196, deaths14 vs3, own bag loss330, faults/suspensions0. Opponent revisions
  UNKNOWN. Full compact summaries saved as continuation-loss-<prefix>.json.
  Finals distinguish collection and conversion losses, not their per-turn causes.
- Contrasting exact-base completed smoke wins0c7c1562(A) and0dcbf59c(B) from
  reachable-final-smoke-{a,b}.json: tribute1008/52 and1001/12, both sides zero
  faults/suspensions. Map hash6e3c6795; opponent revisions/map names UNKNOWN.
  These show legal throughput on the base, not a controlled strategy contrast.
- Source bottleneck: successful defensive fight returned from play_turn even
  when a melee champion still had its move. Frozen boss ea15ef0f/f4b4f65e
  actively chases favorable contacts (radius4), trades in range and retreats
  below local-power parity. Constantly stopping to trade can cost farm turns.
- All six frozen source file sets match manifest26e69a47. Relevant boss combat
  inspected; alpha82a14a04 uses timed rotations, beta7cab9b0f reset farming and
  capital-aware gold valuation. No opponent private state read. Source policies
  are deductions, not evidence of their exact actions in the supplied losses.
- Deferred: repeat arrival/cooldown timing after near-zero matched regression;
  generic gem reweighting, harder camp vetoes, live claims or damage ranking
  after earlier negative findings. Prior notes preserved in archive/task-597*.

## Candidate policy and contracts

- Keep Varg/Vendetta/Ryth/Marcella/Heart, existing items,24-gem/near/winning/
  deadline banking,40% retreat,98% spawn healing, capture completion and channels.
- Defensive hit/reset is opportunistic: keep walking available, then continue
  normal farm selection. Return if dead or movement unavailable. Suppress
  movement-exclusive damage spells in the pre-walk defensive sequence and its
  pre-walk farm call; normal post-walk fight may cast if no movement happened.
  Read actual allowances/readiness after actions. No chase or new pursuit goal.
- Walk and dash retain strict distance progress and shortest-distance priority.
  Among ties only, minimize fresh visible basic pressure: strength*2 in attack
  range, strength*1 within range+1, else0. Snapshot <=6 contacts after visibility
  and health checks; recompute after hidden obstruction retry. No cached enemy
  positions or allied vision. A safer but longer step cannot override progress.
- Below28k fuel at movement entry, omit optional contact snapshots; zero risk
  recovers the original deterministic distance tie order. Planning45k/action18k
  and distance65k reserves unchanged. No new field or live shared-memory writes;
  GA/v1 draft layout remains bounded. Main always calls official end_turn.
- Six compiled helper assertions cover distance priority, safer/worse ties,
  nonprogress rejection, longer-safe rejection and unreachable rejection.
  New sparse log mode contact-farm marks continued defense turns for evaluation.
- Compact reference, playbooks B/C/D/F, relevant melee/movement/ability API and
  installed C++ contracts consulted. SDK894229e1; CLI3.0.5/engine1.0.3,
  lockac2b5ad2, suitepublished-40-release-305-v1. Unchanged full-review handoff.
  Organizer download hub is not full event-policy or production-parity review.

## Validation, risks and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, exact source8fb6844e3453e6ba8ff2b811355d8283689f8f02153dabe0ae825a9b148c424d.
  Report.agent/check-task-fb147fa32a584508b58c80f102eede3a.json; canonical
  check-report saved in continuation-check.json. No source edits after check.
- Smoke a0fd1a1a: completed round1015, tribute A1007/B81. Smoke07428179:
  completed round939, tribute A8/B1041. Both sides zero faults/suspensions
  in both games. Engine1.0.3/fcb6c3e8,41x41/map hash6e3c6795. Map name,
  opponent revision and candidate-side attribution UNKNOWN in compact report;
  these are validity checks only. Full summaries in continuation-smoke.json.
- git diff --check PASSED. Six helper assertions compiled in the checked build.
  Per-file final hashes, check identities and decision: continuation-evidence.json.
- Risks: leaving a favorable trade can forgo kills/camp denial; deferring an
  exclusive spell lowers burst. Basic-range pressure omits enemy spells and
  hidden reinforcement, and extra snapshot calls may consume fuel. Equal-path
  ties cannot solve long detours. Comparative strength remains unmeasured.
- Next: supervisor evaluates exact checked source against edit base, protected
  champion and frozen opponents under unchanged gates; compare wins/tribute,
  collection, deaths, bag loss and reliability. Inspect contact-farm progress
  before adjusting combat or pursuit. No publication/submission by this worker.
