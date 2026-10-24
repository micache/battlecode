# Operational summary

## task-d5524e96f0774fd18033d72a0dbb68c5 — bounded frontier farming

Identity: beta, bot/beta; input/HEAD e44d887e638d764250ac6c829a1df7430c0dd78e.
Actual edit base and protected champion: 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9;
base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six prepared source files independently matched feedback.handoff edit-start
hashes; the dirty initial tree was trusted preparation, not interrupted work.
No pending beta candidate: latest e44d887e / 4fcc082c was evaluated REJECTED.
Preserved prepared.patch, identity-check.json and prior-NOTES.md in this task's
directory; accepted source remains in Git. Do not treat HEAD scores as starter
scores. Prior notes retain older negative findings and exact source identities.

Hypothesis: replacing global terrain ranking with a bounded, persistent frontier
search will increase matched wins and submitted gems over e44d887e and the trusted
starter, restore collection on zero-activity maps, and avoid increasing own fuel
suspensions or faults. No win/submission gain, continued zero collection on those
maps, or new reliability failures falsifies this prediction. Not yet measured.

Evidence motivating this experiment:
- Evaluation 89523553d2d2ce5c493488aa037307ae71cf46c9f6967e54f60b5c99987a9f9e:
  e44d887e / 4fcc082c, full pool 218W/182L, rejected; development 203W/167L.
  Development map breakdown includes 0/10 on 00ambush and 01corridors.
- 00ambush/A loss 3f4c965d978cb76b9fb2d93da6f358df047ec4c978a75e462b03aeb14ae4ee60:
  completed round 1697, 0:1024 submitted; all five own champions zero collection,
  gold, damage and deaths; zero own faults and suspensions. Opponent unknown here.
- 00ambush/B loss 14f7d5bba885d54eff3756c400fde6119e18f040aee721d6aa6b731dbfbc253f:
  completed round 1734, 0:1032 own:opponent submissions, zero own earned gold,
  collection, deaths, faults and suspensions; 440 own monster damage.
- 00split/B loss 00217cc7eeb3a94d761c79e8009c10e7292e554046c00620e754345368f44f2d,
  versus frozen boss 4feab379: completed round 1064, 946:1027 own:opponent
  submissions, 22 own deaths and 96 bag loss, zero own suspensions/faults.
  This is a separate combat limitation, not proof of the nonprogress mechanism.
Full summaries saved by match ID. Final statistics do not reconstruct decisions.
The global terrain planner plus expensive all-group ranking before live scans
is a source-grounded possible cause of legal nonprogress, not a traced cause.

Chosen policy and current capabilities:
- Explicitly reuse our own e44d887e draft, build, combat, capture, banking and
  recovery policy from the starter edit base, then replace objective scheduling.
  Roster Varg/Vendetta/Tavi/Ryth/Marcella truncated to actual team size; legal
  ability sequencing, Jungle/Monster/Durability then Power, Tavi field investment,
  useful channel preservation, five-round capture hold, spawn healing hold,
  30-gem/near-altar banking and recall remain coupled working components.
- Rank at most 32 new static group records per refresh, keep four best geometric
  frontiers, retain a persistent ranking cursor. No full terrain-ranking field,
  all-group sort, or map-sized rank vector. Cache expires after eight rounds or
  displacement over six. Stop ranking below 55k remaining fuel.
- Live checks: two rotating groups first, then up to four retained local groups;
  at most six total, or exactly one while committed. Advance the exploration
  cursor only after fuel allows the queued check to begin. Exhaustion of scan
  reserve preserves intent instead of claiming an invalid target.
- Fresh visibility gates lifecycle and unit-state reads. Group visibility uses
  static spawn membership rather than an allocated whole-board intersection.
  Long observed respawns receive a bounded retry exclusion.
- Movement still uses reusable terrain/occupancy-aware routes and refreshes
  blockers after movement/reveal. Keep normal fuel settings, 45k scan/search
  reserves, 18k action-loop reserve and bounded movement retries.
- Diagnostic ready/farm/yield lines only every 100 rounds; private state only,
  no draft/live shared memory writes. main.cpp still always calls end_turn.

Frozen opponent study: manifest e1421f49, six sources; inspected shared boss
4feab379 / ea15ef0f / f4b4f65e config, draft and objective scoring/selection.
It uses melee reset/AoE picks, travel refresh, helper claims, squad feasibility,
30-gem banks, 150-gold reinvestment and target hysteresis. Keep our existing
private farming policy; this experiment tests an alternative bounded local
frontier search rather than importing that whole controller. Cooperative claims
may help monster-only maps but do not directly explain zero-activity losses;
combat improvements remain a separate next experiment. Previous strict cash
camp caps and repeated draft-only changes remain rejected, per archived notes.

Rules/SDK unchanged: handoff gameplay_review_required=false and documentation
unchanged. Consulted compact reference, playbooks B/C/D/E/F/G, research ledger,
organizer reconciliation, installed C++ group/visibility/distance-field contracts.
CLI 3.0.5; engine lock ac2b5ad200d0df54380e94f82b1a327dd0407202533325808c8bf3af26c56136;
suite published-40-release-305-v1. SDK identity remains pinned by brief/entry.
Organizer Markdown hub does not establish every event policy or production parity.

Validation (all artifacts in this task directory):
- Source-contract regression ran red on starter and on uncapped geometric
  ranking; final PASSED/0. It checks bounded ranking/live checks, persistent
  cursor update after fuel gate, rotation precedence, deferral, visibility and
  private state. This is not engine execution. C++ static assertions exercise
  cursor wrap, cache expiry, bank and movement-deferral boundaries.
- Exact command for all three builds:
  bot-check --owner-config /var/lib/battlecode-volume/config/beta.json
  Initial FAILED/1, source 9ca8c9e8: inherited assertion hardcoded six-round
  expiry after policy moved to eight. Fixed the assertion to use plan_lifetime.
  Saved check-initial.json. Intermediate PASSED/0, source 15feb845,
  check-intermediate.json; two completed smoke wins, zero own faults/suspensions.
- Final PASSED/0, source
  c9c933a21b50bd9e01ca1dfdaca7bd290b0259e8cd51bc7c59ad340853232c11;
  check-final.json. No source changes afterward; final-source-files.json records
  per-file hashes. Final regression PASSED/0; frontier-regression.txt.
- Final smoke A 9484a7a3747570985a23425c8b7b65c3423ded785fbb913542f99ba8e48a7aa8:
  COMPLETED, own win round 1026, 1015:4 submitted.
  Final smoke B d4cff1665a50a4f0d74b099963c007f0f45153ba32d6ea96de0849deeca3d1fb:
  COMPLETED, own win round 1033, 1005:22 submitted.
  Both zero own faults, suspensions, deaths and bag loss; final-smoke-{a,b}.json.
  Same 41x41 map hash 6e3c67956080f8da5a0042e68ea481189cd6f61061a742a8be0354a9ea5c5620;
  map name and opponent revision unknown. Bounded log slices saved separately;
  observed yield samples retain >47k fuel but do not certify all-turn minima.
- git diff --check PASSED/0; diff-check.txt.

Uncertainty: smoke covers a small fixture, not the 100x100 nonprogress cases;
zero-activity mechanism remains unproven. Smoke timing is mixed versus e44d887e
(925/A, 1031/B), and the final capped rank version is slower than intermediate
(1004/A, 943/B). Those are source-specific diagnostics, not independent samples
or competitive improvement. Geometric scoring risks maze detours, delayed new
frontiers and excessive commitment; monster rally and collision combat are still
limitations. Do not promote from smoke alone.
Next: supervisor evaluates exact checked source against starter, e44d887e and
frozen boss on matched maps/sides under unchanged gates; prioritize collection
and stage logs on 00ambush/01corridors, then broad wins and reliability. If
nonprogress remains, use stage evidence to isolate initialization/live-scan/route
cost. If throughput recovers but boss losses persist, investigate combat/rally.
No agents, commits, pushes, official actions, tournament polling or promotion.
