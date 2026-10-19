# Operational summary

## task-7c1e0776bcb74ea29892049a3c08c5e2 — cooldown-aware shortlist rotation

Hypothesis: excluding observed downtime and active route retries before the
bounded camp shortlist, with idle claimed-region evacuation, improves submitted
gems and matched wins. No win gain, lower submissions or increased deaths,
faults/fuel suspension falsifies it. Unmeasured source/rules mechanism.
Decision and exact provenance: this task directory's decision.md/evidence.json.

Identity: beta / bot/beta; input HEAD 7cab9b0f6b948b0ea0b3b284425a3501c564d16b;
trusted edit 50a0d7d5ecbd99c70536b4c71c54e404f2daa2b1 / source
6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
All six source files matched edit Git blobs and trusted per-file hashes.
Prepared bot.cpp changes and absent economy_policy.h were intentional relative
to HEAD, not lost work. Last task PUBLISHED/evaluated, no unpublished candidate
awaits evaluation. Protected champion 0ca5c04e remains in trusted Git/snapshot.
No agents, commit, publication, official action or comparative evaluation run.

Latest evaluation 3278166b measured 7cab9b0f / fd5e2554 (gold-camp penalty),
not this edit/new source: INCONCLUSIVE/full-map-pool, 115W/21L overall;
matched development delta +0.044643 over 56 side pairs, with collision/interlock
regressions. Development 97W/15L, zero own faults, mean suspension 0.321429.
The edit base was retained. Prior notes preserved in archive/through-task-a1b6*.

Same-source edit-base self-play (50a0d7d5 / 6d66a77f): 21W/17L over 38 unique
cells, no faults/suspensions; distinct from latest-candidate/promotion scores.
- ce4f287e6385fe4f1c6ac066a3bb30ca24c5fa9360016020e278455521223242:
  interlock A loss versus 7ed7e6a3; round 608; 810:1024 submitted, own 854
  collected, 1 death, 22 bag loss, no own faults/suspensions. Tavi 66 gems.
- 4413ca209096b67a12254a655846523d99faed73fba56333c3cd7b3a6f419bd9:
  fragment B loss versus 7ed7e6a3; round 558; 308:1003 submitted, own 366
  collected, 5 deaths, 58 bag loss, no own faults/suspensions.
- Contrasting same-source collision A/B each 2W/0L; individual win IDs unknown.
Compact summaries saved. Final statistics do not establish exact wasted turns.

Frozen manifest 163f4cf3 inspected: newer alpha 046f1c3a / 07022bad cooldown
module; newer gamma 63d05e37 / a4d664c8 full farmer/draft, melee-first,
value/time, observed respawns, each-bag banking and 300-gold shopping recall.
Adopt only their compatible timestamped observation discipline. Historical
self-play opponent 7ed7e6a3 is not equated with these frozen revisions.

Current policy: Varg/Tavi/Ryth/Vendetta/Marcella; Jungle Strength, Monster
Strength, Durability Health, then Power Strength. Independent group capture,
each-bag banking, full spawn healing, altar locks, guarded route dashes.
This candidate adds private per-group cooldown observations (no team bytes):
- Record only visible remaining timer. Positive expiry is an earliest possible
  respawn, not hidden live state; at expiry return to unknown/explorable.
- Zero/negative timer defers this observed round only; no presumed occupancy.
- Exclude observed cooldowns and active route retries BEFORE the 12-entry
  partial shortlist. Original geometric/reward ranking and scan reserves stay.
- Own reward occupancy overrides cached deferral before ranking. On no work,
  try one normal legal move off an occupied respawning region, allowing future
  respawn. Existing free-root movement and bounded obstruction retry apply.
No extra distance field or broad live-state scan. camp_rotation.h contains
compiled temporal boundary assertions. bot.cpp/bot.h are the only modified
existing edit-base sources; camp_rotation.h is added. No source edits after check.

Risks: altered routes, earlier exposure to unknown groups, one extra own-group
state query, remaining geometric-cap starvation; gold loops/combat deaths can
remain. No traced mechanism coverage or measured fuel headroom yet.
Prior negatives retained: full scheduler +0.041667 with interlock regression;
combat retargeting -0.041667; healthy shopping and banking detours zero matched
gain; harvest circuits/isolated draft/item/shield gains unestablished. This is
an isolated cooldown ablation, not restoration of that scheduler or penalty.

Engine 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
suite published-17-release-225-v1. Docs unchanged per trusted handoff, reviewed
at task-a1b6. Consulted compact reference, research/organizer record, Playbooks
B/C/F (and shared audit/evaluation guidance), camp handbook/API and installed
header camp_group state/timer/visibility contract. SDK SHA256
ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
Organizer hub does not certify all policy or production parity; ward::owner
remains absent in installed SDK and unused.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0 for source e05d7dfc0b99af0c3e7f7154858e09ce04eb23d472db8ed1ae5ec08b1c1078bf.
Report .agent/check-task-7c1e0776bcb74ea29892049a3c08c5e2.json;
exact-source check-report PASSED/0 saved in this task directory. Trusted smokes
b684c0fa83438bab9cd4e529bf9aec59165fe48c0b1363be1c6c9d20bc4d7900 and
333ca60c12a3156d285bf747fcef114f63d1aca678e6fa529318af0dde63d671;
own stdout slices exit 0/empty. This does not prove complete competitive games,
no suspension or improved wins. Temporal assertions compiled by trusted check.
Focused rotation contracts PASSED/0, five unsafe mutations rejected; existing
safety suite PASSED/0, seven mutations rejected. Reports rotation-contracts.txt
and invariants.txt. `git diff --check` PASSED/0, diff-check.txt. Source contracts
are not gameplay or fuel measurements.

Next: supervisor evaluates exact checked candidate against 50a0d7d5/6d66a77f
on matched development maps, both sides and frozen opponents. Prioritize wins
and submitted gems, protect collision, inspect interlock/fragment and Tavi gem
participation, guard deaths/faults/suspension. Promotion remains a full gate.
