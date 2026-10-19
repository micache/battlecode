# Operational summary

## task-b117f31ca086427583ad098da9e76b71 — observed-danger recovery routes

Hypothesis: with the existing 45% retreat trigger, danger-first recovery steps
and complete-observation recall guards improve matched wins/submitted gems by
reducing deaths and bag loss. No win gain, lower submissions, or increased
faults/suspension falsifies it. Recovery-path cause and gains remain unmeasured.
Decision, exact evidence and risks: this task directory's decision.md/evidence.json.

Identity: beta / bot/beta; HEAD/input 61d59667cf33c7c552390485c5bee5c1119d73ba;
trusted edit 50a0d7d5ecbd99c70536b4c71c54e404f2daa2b1 / source
6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
All six files matched edit Git blobs and trusted per-file hashes at entry.
Prepared bot.cpp/bot.h changes and absent camp_rotation.h are intentional
relative to HEAD. Prior task PUBLISHED/evaluated; no unpublished candidate
awaits evaluation. Accepted champion 0ca5c04e remains in trusted Git/snapshot.
No agents, commits, publication, official actions or comparative evaluation run.
Prior operational notes archived through task-7c1e0776bcb74ea29892049a3c08c5e2.

Latest evaluation 21682124 measured 61d59667/e05d7dfc (cooldown shortlist), NOT
this edit/new candidate. INCONCLUSIVE/full-map-pool, 114W/22L; development delta
+0.008929 over 56 side pairs, with collision/eight/interlock/lanes/stampede drops.
Its development window: 93W/19L, no own faults; mean deaths 1.928571, bag loss
38.5. Latest ambush A 0d9103e2: 600:1076 submitted, one death. Collision A
loss a2831c57: nine deaths, 154 bag loss, 770:1004 submitted, zero own faults
or suspension. Corners/fragment each 4W/0L per side, individual win IDs unknown.
Same-edit-source ambush B c52237a0: round 873, 1148 collected, 908:1020
submitted, two deaths, 240 bag loss, zero own faults/suspension; exact opponent
revision unknown in compact record. Final stats do not establish recovery deaths.

Frozen manifest 96440df1 inspected. Alpha 046f1c3a/07022bad recovery module
uses raw visible basic damage, range-edge depth, then home distance. Adapt
that compatible ordering, retain beta's trigger instead of importing alpha's
35%/70% entry rules. Older beta d2d57274/7daa9117 matches baseline recovery.
Gamma ecbc8203/ff511c52 uses melee-first, reachable reward/time routes, each-bag
banking and shopping recall. Arena sources are not official-opponent evidence.

Current strategy: Varg/Tavi/Ryth/Vendetta/Marcella; Jungle Strength, Monster
Strength, Durability Health, Power Strength. Independent captures, each-bag
banking, full spawn healing, altar locks and guarded route dashes. New recovery:
- Only after original recovery entry; no extra scans on healthy farming turns.
- At most 32 visible live threats; awake damaging camps only. Enemy basic range
  + base movement envelope is conservative, especially for ranged champions.
- Score ordinary one-step choices plus staying by total raw basic damage,
  weighted depth inside ranges, then home route distance. Adjacent free spawn
  takes priority because it heals this turn end. Keep useful active shield.
- Quiet complete observation starts recall immediately. Refresh after movement
  and hidden-blocker reveal; at most two attempts. Partial scan never certifies
  quiet. No recovery dash; healthy travel dashes remain unchanged.
- Scan reserve 45k, field admission 55k, action reserve 18k. Native free-spawn
  field; geometric home tie-break when field fuel unavailable. No live team bytes.
- recovery_policy.h constexpr fixtures compile overlapping-range, plateau,
  danger-versus-home and equal-risk tie decisions. Generic dormant-camp farming
  caution retained; stale comment claiming SDK lacks awake state corrected.
Only bot.cpp and added recovery_policy.h differ from edit. bot.h is restored,
and camp_rotation.h absent, as prepared. No source edits after final check.

Risks: hidden/spell damage, target selection and mitigation unmodeled; asleep
camps may wake later. Risk descent can reach a terrain local minimum; geometric
fallback/lost recovery dashes may delay healing. Existing entry threshold can
still admit lethal volleys. Actual action coverage/fuel headroom unmeasured.
Gold-only loops remain. Previous negatives retained: cooldown ablation +0.008929;
gold penalty +0.044643 with regressions; full scheduler +0.041667 with interlock
regression; combat retargeting -0.041667; healthy shopping/banking detours zero
gain; isolated draft/items/shield/harvest circuits have no established gain.

Engine 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
suite published-17-release-225-v1. Docs unchanged per trusted handoff. Consulted
compact reference, RESEARCH, organizer record, relevant Playbooks B/C/D/F/G,
handbook movement/camp/channel and C++ field API/installed SDK live-state,
awake/restrictions/shield/movement contracts. SDK SHA256
ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
Organizer hub does not certify all policy or production parity; ward::owner
remains absent in installed header and unused.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
first FAILED/1 on a4d7d743 (unsigned/int64 min mismatch); diagnostic saved as
check-initial-failed.json. Cast corrected, then same exact command PASSED/0 on
72275bc2ad79fed78c0456f8bfe83d2fd5dccd24ef10bcee1c492adb64968e67.
Local report .agent/check-task-b117f31ca086427583ad098da9e76b71.json;
exact-source check-report PASSED/0 saved in this task directory. Smoke IDs
77fe0dc792cf8bc104d34f9b5c53e39778d9bbe625eba2b4932509dcd9490a3b and
3cb775d2ee0040407749e56155415acf7991559c036ed654665ccad0a9134773;
own stdout slices exit 0/empty (smoke-a/b.json). No claim of completed games,
measured coverage, zero suspensions or strategic gain from smoke success.
Compile includes recovery decision fixtures. `git diff --check` PASSED/0;
report diff-check.txt. No additional tournament or repeated unchanged checks.

Next: supervisor evaluates exact checked source against 50a0d7d5/6d66a77f
on matched development maps, both sides and frozen opponents. Prioritize wins
and submissions; check deaths/bag loss/faults/suspension. Protect existing wins,
inspect ambush B/collision A recovery traces if available. Full promotion gate
still applies. Gold-loop routing remains the next separate candidate if this
recovery mechanism fails to affect wins.
