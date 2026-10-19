# Operational summary

## task-a1b6ecd47a594170978ab675dab36d4a — capital-aware gold farming

Hypothesis: after 300 gold of cash/equipment, penalizing zero-gem groups in both
shortlist and final ranking improves matched wins and submitted gems by ending
low-value gold loops. Falsified by no win gain, lower submitted gems, or increased
deaths/faults/fuel suspension. Source-supported mechanism; no per-turn proof.
Decision and compact provenance: this task's decision.md and evidence.json.

Identity: beta / bot/beta; HEAD/input/edit 50a0d7d5ecbd99c70536b4c71c54e404f2daa2b1;
base source 6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
Clean initial tree; all six source files matched trusted edit-start SHA256s.
Prior task PUBLISHED and evaluated; pending self-play is for already evaluated
source, not an unpublished candidate. Protected champion 0ca5c04e stays in its
trusted snapshot/Git. No recovery needed; prior notes archived through 6be48cfa.

Evaluation ca52f5346e5be88ad045a11e49e274f650ddd46b6c39ec568cdfb3ec63d051c3
measured this edit base, not this new candidate. INCONCLUSIVE full-map-pool;
development window 92W/20L, zero own faults/suspensions/missing/unknown. Matched
development-base delta +0.053571 over 56 side pairs is separate from promotion.
- Ambush A loss 394a1869ad4eb7b01d5405e7a0b3bc891a59597a60a9b9c7067106c3f24ef2c0:
  round 795, 394:1014 submitted; own zero deaths/bag loss/suspension. Ryth 1137
  and Marcella 945 earned gold, zero gems each; Tavi also zero collected.
- Ambush B loss c52237a027f5a328bb557adb7b5dd02852753d41ac11b5e1f4b6ff98d67ae39b:
  round 873, 908:1020 submitted, 1148 collected, 240 bag loss, two deaths.
  Tavi 685 earned gold / 36 collected gems / 19245.5 camp damage.
- Pilgrimage A loss 0349d0394a8f790182452c9ff77a894e65a709a96ddb0e112334954d4766f920:
  round 719, 272:1044 submitted, no own deaths/bag loss/suspension. Tavi/Ryth
  zero collected, 770/700 earned gold. Opponent gamma 1b34f42a / 3ce565f6 per
  trusted brief. Exact ambush opponent revision unknown from summary alone.
- Contrasting wins: collision/corners/fragment each 4W/0L per side in development;
  current-source self-play ambush 2W/0L versus 2dcd14cf (not independent reruns).
Final-statistics summaries are saved; they do not prove exact turn decisions.

Frozen manifest 7a7333e8: inspected gamma 1b34f42a / 3ce565f6 full farming,
shopping/bank/combat/draft: melee-first, value/time, observed respawns, 300-gold
shopping recalls and each-bag banking. Older frozen beta d2d57274 / 7daa9117
shares the current geometric scoring. New policy uses capital-dependent value,
retains beta's low-cost shortlist, and does not import gamma's whole scheduler.

Current policy retained: Varg/Tavi/Ryth/Vendetta/Marcella, Jungle Strength,
Monster Strength, Durability Health, Power Strength; bank each bag, heal fully
at spawn, group capture, altar locks and guarded route-directed dashes.
New economy_policy.h: 300 capital threshold; zero-gem penalty +90, bounded
regardless of capital. Seven constexpr boundary/ranking checks compile with bot.
Cash + purchased shards/emblems counts Tavi spending, with Power emblems valued
at five paid shards rather than six stat points. Four equipment lines only;
no full item-cost scan. Same penalty in shortlist and final score avoids bounded
scan starvation. Standing available-group capture still returns before scoring.
Gold remains eligible fallback. No extra pathfinding or shared memory writes.

Risks: reduced growth, longer/dangerous gem travel; capped penalty may still be
insufficient on distant maps. Initial bootstrap/capture/banking/recovery preserved.
Broader scheduler/circuit/shopping changes not restored. Prior negative findings:
healthy shopping/banking detours zero matched gain; combat retargeting -0.041667;
reachable scheduler +0.041667 with interlock regression; harvest circuits zero
established gain; isolated arrival/item/draft/shield gains unestablished.

Engine 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
suite published-17-release-225-v1. Required refreshed handbook/C++ export, matching
installed SDK, compact reference, research/organizer record and playbooks reviewed.
Header SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
ward::owner documented but absent in installed SDK; unused. Organizer download
hub does not establish all event policies or production parity.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0, checked source fd5e25543653c9a8774346212b3f689927a9dd489b1ba2373a1edd0889bf63aa.
Report .agent/check-task-a1b6ecd47a594170978ab675dab36d4a.json, copied to this
task's check-report.json; seven new constexpr assertions compiled. Trusted
smokes 6f60c8376afad3556c34627165f69206b130d5287e76a36e78b126ab6dc689ef and
c3c31deeae93806b17b896e5941cb0423108d161f34c9fafd1b4f0a991dbc4c8.
Smoke validity does not establish completed competitive games, improved wins,
actual policy coverage or measured fuel headroom. No source edits after check.
`git diff --check` PASSED/0; saved diff-check.txt.
Existing source-contract suite PASSED/0; invariants.txt covers channel, spawn,
capture, observation, legal roots, bounded retries, spell exclusions and resets;
seven unsafe mutations rejected. This is not a gameplay/fuel measurement.

Next: supervisor evaluates checked candidate against 50a0d7d5 / 6d66a77f on
matched development maps/sides/opponents. Prioritize wins/submitted gems and
per-champion gem participation on ambush/pilgrimage; guard collision/corners/
fragment wins, deaths and suspension. Promotion remains a separate full gate.
