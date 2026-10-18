# Current experiment: task-9d1d883be978493496b41980e19b63d4

## Identity and handoff
- Bot alpha, branch bot/alpha; input HEAD 82a14a04f0e6b68aac8a7e879d305b1a886b857c.
  Edit commit 5f73d0787014e3f712d0eb6234f088fee489b4d8; base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  All eight entry source files byte-matched edit_commit. Two HEAD differences
  were trusted preparation, not incomplete work. Latest candidate evaluated;
  pending self-play is separate. Accepted c0cebd720fcd55e2bbb51d57dd2c398889d4071e
  remains preserved in Git. Prior NOTES archived under task-0648f2bdbcf046cfb9be1812a8247adb.md.
- Engine/SDK 2.1.6, historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  Installed C++ header SHA256 verified:
  90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
  Routine unchanged-doc iteration: compact reference, playbooks B/C/D/F,
  research/organizer ledger and relevant action/capture/SDK contracts consulted.
  Organizer page is a download hub; additional policy/production parity limits persist.

## One falsifiable hypothesis
Same-turn capture follow-through on freshly cleared, directly attacked camp
groups increases matched development win rate over this edit base. Unchanged or
lower win rate falsifies the prediction. Earlier capture occupancy, collection,
tribute and paired-win rounds diagnose the mechanism. This is an unmeasured
rules/source deduction; no supplied turn trace proves the gap caused any loss.

## Evidence and decision
- Latest evaluation 6a4e7bd9e736b1bf4f7c133785b6fb5e07daad9d1cb178aafe5959d49ee90584
  measures HEAD / source 6e362fd7cce836975fa615bc8b936109235fd320def63703761366586efabc25,
  NOT this edit base: 43W/5L, zero faults/missing/unknown reliability, INCONCLUSIVE.
  Matched development-base delta +0.0208333 (24 side-paired cases), separate from
  protected-champion delta +0.7708333. Its arrival-aware routing is not reapplied.
- Exact-base self-play expanse B loss
  3f478d46eee36d087f8b2cbba0a3cb82fe2c7f9a108d13894acba6d008317542:
  opponent db8b69148809f2d7872142d5e5bdffdf071f7c32; round 536; alpha
  collected/tributed 982/982 vs enemy tribute 1020; no deaths/kills/combat,
  faults [0,0]. Another exact-base expanse B loss
  31763b8d24b91d7aaff9869d5316b86f17fbdc808a2dbb9f9176194d5718a79e:
  opponent 27dedf6219cbf10a44f92bbe76d1a328f1d8adab; round 534;
  982/982 vs 1032; again no deaths/kills/combat, faults [0,0]. Full finals
  saved as this task's -base-expanse-B-loss.json and -base-expanse-B-gamma-loss.json.
  These are noncombat throughput losses, not evidence of unbanked endgame bags.
- Contrasting latest-evaluation aggregates: collision B 4/4 wins;
  elkring/interlock/lanes 8/8 each. Preserve successful combat policy. Distinct
  source/opponent revisions are not pooled with the exact-base self-play games.
- Frozen manifest SHA256 f3ffa55f5754775b490eba2cb53aae4882a5dd41c7a283423125f20e92867821;
  all four source sets hash-verified. Beta uses persistent group clearing,
  Varg/Tavi/Ryth draft and farming passives; gamma uses melee draft, value/cost
  routing, collector deference and respawn memory. Both clear hostile locks.
  Their farming returns after combat without using a remaining capture move.
  Historical alpha/starter retain nearest-group farming. Source observations
  do not establish official-opponent behavior or runtime causality.
- Rules allow melee basic plus ordinary walking; capture phases precede champion
  turns. Stepping onto the newly cleared group this turn can start its timer one
  phase earlier. Current farm_camps instead returns after every successful fight.
- Prior banking priority/arrival/batching, fixed draft/stat, local/global
  pre-combat capture/deference, AoE, focus fire, dashes and economic resupply
  remain negative/deferred. This experiment changes action follow-through,
  not route selection or pre-combat priorities. Decision details saved as -decision.json.

## Candidate policy and limits
- camp_rotation.h adds a private three-target combat trace. Record immutable
  camp spawn positions after basic, successful offensive cast and follow-up
  basic. Every successful cast, including defensive casts, records its movement
  exclusion monotonically. No shared-memory change or persistent live-state cache.
- After initial camp combat only, a living champion with can_move and no recorded
  movement-exclusive cast may seek capture. Match only groups containing a
  directly attacked spawn (at most three). Read state only with current personal
  spawn visibility and a nearby candidate. Require reward_available now.
- If already on a selected spawn, stay. Otherwise refresh blockers after combat,
  intersect visible spawn goals with free tiles reachable using the actual base
  move speed, and attempt one ordinary move. Preserve route lock placement.
  No path search, second move, post-move attack, hidden state or extra collector
  election is added. No move if no qualifying group, low fuel or blocked goals.
- Existing 45,000 planning/18,000 action guards retained. Live group queries are
  limited by three recorded targets; geometry scan has a fuel stop. Blockers and
  reachability are computed only for an actual cleared-group opportunity.
  Static initialization still scales with map groups as in the base.
- Combat scoring/order, draft/RNG, builds, banking, recall, channels, ordinary
  routing, cooldown memory, shared bytes and intentional yield remain edit-base.
- Risks: one-tile follow-through can increase exposure or split an existing
  collector's reward; splash-only clears of untargeted groups are missed;
  immediate post-hit group-state availability/opportunity frequency and fuel
  headroom are unmeasured. Ranged/basic and movement-exclusive spell finishes
  often have no move, so expected benefit is limited to eligible sequences.

## Checks and next step
- python3 experiments/alpha/check_capture_followthrough.py PASSED, exit 0:
  all 14 integration/scope invariants; report is this task's -source-check.json.
  Pure trace static_assert scenarios compiled in the trusted check: no targets,
  basic-only/compatible reset, dead/no-move cases, exclusive cast despite a live
  movement flag, monotonic exclusion, three-target capacity and preserved origin.
  These are safety scenarios/source checks, not engine branch-coverage evidence.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Checked source 889cd3f658a9a3ad14a454d818654613b1056199ae6e95a71524790f9130d37a.
  Actual report inspected: .agent/check-task-9d1d883be978493496b41980e19b63d4.json;
  check:task-9d1d883be978493496b41980e19b63d4:889cd3f658a9a3ad14a454d818654613b1056199ae6e95a71524790f9130d37a.
  Smoke IDs a6dffcdb88b2d16a1bcabcd66b797ab3ac5c17890c2dcc27b8238ea808b24ac6
  and a622251e0688a8d1e7474d581546b07f40a35af834ead2c743728559883bc585.
  Summary has no full-game/fuel/coverage diagnostics; no competitive gain claimed.
  Source file hashes unchanged after check; git diff --check passed.
- Historical finals report engineVersion 0.0.1, distinct from CLI/SDK 2.1.6;
  relationship unknown. Deterministic reruns are not independent evidence.
- READY_FOR_EVAL. Supervisor compares exact checked source against edit base and
  protected champion across maps/both sides. If weaker/unchanged, inspect actual
  post-clear moves, capture start rounds and ally duplication before extending
  follow-through to AoE-only groups or longer travel. No tournament evaluation,
  commit, push, official submission or agent spawning performed.
