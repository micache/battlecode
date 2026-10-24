# Operational summary

## task-8bd01624b8814e63a95493b659f733e3 — bounded terrain-aware opportunity selection

Identity: beta, branch bot/beta; HEAD/input 265974a75ad16dfc067077c15e5acf01264d2be1.
Edit base 863825b744eb21ee366370c9b1919ce73210d9d4 / source
c9c933a21b50bd9e01ca1dfdaca7bd290b0259e8cd51bc7c59ad340853232c11.
Protected champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 unchanged.
Seven source files matched trusted edit hashes and snapshot. Initial differences
from HEAD (bot.cpp and removed harvest headers) were trusted preparation, not
unfinished work. Latest prior candidate was evaluated; nothing pending/recovered.
Prior operational notes remain in Git HEAD and prior experiment artifacts.

Hypothesis: local terrain-distance ranking and periodic long-route retargeting
will increase matched wins and tribute over c9c933a2 without new faults or fuel
suspensions. Nonpositive win/tribute gain or new reliability failures falsifies it.
This is a source-grounded, unmeasured mechanism, not a traced cause of losses.

Evidence: latest candidate 94c44565 / commit 265974a7, evaluation 51ca17d1,
240W/160L INCONCLUSIVE; development comparison against edit base +0.008108.
Mean collection 630.63, tribute 572.36, own faults/suspensions zero.
- 00ambush/A c71597cce908daf0bda7e0ee46063bd904c57919d63c17816d531fbbf2a66021:
  lost round 1932, 555:1007 tribute, 625:1063 collection, 7686:7146 earned gold.
- 00ambush/A b0f2c2b667f3a05f7863663ede71793a1abac3e74ee63c2f4230f26bea32c52a:
  lost round 2000, 793:942 tribute despite 14:5 kills and 9990:5278 earned gold.
- Contrasting 00ambush/B cd4363ae4199e8a614ddd5aea5a0f3ce1ea93eef7c7dc7c16f9e45529f88e280:
  lost round 1908, 253:1010 tribute, zero bag loss, 191 carried. Opponent
  revisions unknown. Compact metrics saved in this task's evidence.json.
A sparse loss log tail shows legal movement and >38k sampled yield fuel;
it does not establish that route selection caused the defeat.
Base smoke wins 9484a7a3/A and d4cff166/B remain contrasting reliability fixtures
in task-d5524e96 artifacts, not controlled comparisons to the new smoke games.

Frozen manifest 63177560 (six sources); inspected shared boss 4feab379 /
ea15ef0f / f4b4f65e config, draft and objective/navigation routines. It uses
terrain distances, periodic review, hysteresis, squad feasibility/claims,
30-gem banks and kit-specific builds. Adapted terrain cost and target review
only. Frozen sources do not establish official opponent behavior.

Changes:
- policy.h: 24-step local terrain horizon, 16-round target review, advisory
  travel-cost function with explicit unreached and stale-origin handling.
- bot.h/bot.cpp: private cached static terrain field, eight-round/six-tile
  expiry, 65k fuel gate. Use its costs in bounded ranking/live candidate scores;
  distant/unreached groups remain eligible. Fall back to geometry when stale.
- Review retains current group first with existing 1.25 hysteresis, then rotating
  exploration/local shortlist. Still at most six live checks and 32 new static
  ranking records. Deferred scans preserve intent; current capture hold wins.
- routing_test.h: compile-time maze-detour preference, unreached/distant goals,
  stale origin, expiry and backward-round regressions. No runtime test overhead.
- Existing roster, build, gold weighting, bank/channel/recovery, action validation,
  occupancy-aware movement and intentional yield remain. No shared-memory writes.

Validation (artifacts in experiments/beta/task-8bd01624b8814e63a95493b659f733e3):
Exact command: bot-check --owner-config /var/lib/battlecode-volume/config/beta.json
- Red FAILED/1, check-red.json / source 04990ed9: expected missing travel_steps
  and review_target functions before implementation.
- Final PASSED/0, check-final.json and check-report.json; source
  d9bfba2674753a72207f1e30f0798629ff96a107b7814d1c4d2d2ad7641eb902.
- Smoke A d0270f2c3d514947cf61481816239a056c3f69791c5b140df9fae93a7704b75d:
  COMPLETED win round 1037, 1050:6 submitted, zero own deaths/bag loss.
- Smoke B f4c82c8a4bf087183525b6f12d8bbd42b0241780e2065437488080068a5084eb:
  COMPLETED win round 1010, 1008:40 own:opponent tribute, zero own deaths/bag loss.
Both zero own faults/suspensions. Full normalized summaries saved. Own frontier
logs confirm A/B assignment. Sparse yield samples include 32,824 remaining fuel,
not a certified all-turn minimum. Same 41x41 map hash 6e3c6795, observed seed
17615240315955964814; map name/opponent source unknown. No seed flag used.
- git diff --check PASSED/0; final-source-files.json pins checked source files.
No source changes after final trusted check. Final review in review.md.

Uncertainty: smoke times versus base fixtures are mixed, and fixture opponent
identity is not established; no speedup or tournament-strength claim. Local
horizon cannot fully price distant maze detours; stale-origin and anchor costs
are estimates. Repeated field lookups may cost more fuel on dense maps; periodic
review may cause route churn. Monster-only rally/combat/build balance unresolved.
Rejected this cycle: item-aware gold weighting (prior strict gold restrictions
failed), squad protocol (separate coordination experiment), full-map ranking
(previous fuel/stalling risk), repeating the latest clear/reset candidate.
Rules/SDK unchanged per handoff; matching header SHA256 verified. Consulted
compact reference, relevant playbooks/API/SDK distance methods and evidence limits.
Organizer download hub does not establish all event policies or production parity.

Next: supervisor evaluates exact checked candidate against edit base/protected
champion and frozen opponents on matched maps/sides under unchanged gates. Compare
wins, tribute, collection, route churn and fuel; prioritize constrained maps.
No commits, pushes, agents, official submissions or comparative evaluation here.
