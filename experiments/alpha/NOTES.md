# Current experiment: task-8dbeeaaf739e428597d05685211480df

## Identity and status
- Alpha, bot/alpha; input HEAD 60001c32ba5c5a08b45e6f46fb65a2b8dda50cc1.
  Edit commit 046f1c3a41fe746c65c0982d06062623200fa931; base source
  07022bad764ef37711c5afeddb10a434a0d5f9c5581e519f8bb575ced706fca2.
  All nine starting source files byte-matched edit_commit. HEAD-relative source
  changes were trusted preparation, not interrupted work. Latest candidate was
  evaluated; no pending candidate. No old patch recovered or reapplied.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e stays in Git
  outside this transaction. Prior notes archived as task-f8007f1...-NOTES.md.
- Engine/SDK 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
  suite published-17-release-225-v1. Documents unchanged; compact reference,
  playbooks, RESEARCH/organizer evidence limits, camp/action rules and relevant
  C++/installed SDK camp visibility, attack-mask and ability contracts consulted.
  Installed SDK SHA256 ee131e29...b72e264 verified. Organizer page is a download
  hub; full event-policy review and official production parity are not claimed.

## One falsifiable hypothesis
Concentrating camp basics, resets and nearby offensive casts on the lowest-health
legal camp increases matched development win rate over the edit base. Unchanged
or lower win rate falsifies this prediction. Collection/tribute, camp damage per
collected gem and paired-win rounds diagnose the mechanism. This is an unmeasured
source/rules deduction, not a traced cause of any match loss.

## Evidence and decision
- Evaluation 83be320a...24434012b0f measures 60001c32 / source 1d7d75b3...fbd39a,
  NOT today's edit base. Jungle trial: development 83W/29L versus base 84W/28L;
  matched delta -0.00892857 over 56 side-paired cases. Faults/missing/unknown zero.
  Protected champion comparison 97W/39L is separate. Jungle is not reapplied.
- Ambush B loss 1978eeda51cfe6bab26e01b0be8e3f7288bdb334a94af819c69e83556bdcb750:
  same evaluated source versus frozen alpha 6af1685b / 87b9be45...e6382e01,
  round 1091, collection/tribute 942/942 vs 1140/1034; own deaths zero,
  camp damage done/taken 107045/28998 vs 66900/33875; no PvP/faults/suspensions.
  More clearing damage with fewer collected gems motivates throughput inspection;
  it does not prove target selection, capture abandonment or retreat timing.
- Pilgrimage B loss 043803a51bc2b5068c47ab0508364668989dc139cecee73260fce594935c2b70:
  same evaluated source versus gamma ecbc8203 / ff511c52...061671; round 1140,
  own collection/tribute 1056/560 vs 1468/1036; 496 carried, own deaths one vs 11,
  own PvP damage 15625.7 vs 1958; no faults/suspensions. This is also a banking/
  combat-distraction weakness; the camp policy does not claim to fix that mechanism.
- Contest A loss 224ebda89909e06578b64ebda632b16fda476550fec277d50ec4723f03a676cf:
  same evaluated source versus the same frozen gamma; round 2000, tribute 200/400,
  deaths 33/18. Different combat-heavy regime. Complete summaries saved by task ID.
- Contrasting development wins: fragment and stampede each 8/8 across both sides,
  at the same evaluated source. Aggregate evidence only; no invented win traces.
- Frozen manifest d71a6c73...e9273 verified. Relevant beta 7cab9b0f / fd5e2554
  and gamma ecbc8203 / ff511c52 file sets hash-verified and source inspected.
  Gamma picks the lowest-health camp within its selected group; its melee draft,
  value/cost routing, passives and selective PvP are not copied. Beta also commits
  to groups and uses farming passives/recovery. Arena sources do not prove official
  opponent behavior or causal gains from one component.
- Base basics take the first in-range camp; its spell scorer can prefer a healthier
  victim's larger useful damage over finishing the next basic's wounded victim.
  Static camps cannot escape; focusing remaining HP can remove camp bodies sooner.
  This differs from rejected PvP focus, broad AoE/finish bonuses and group-first
  routing. It adds no group state queries, route scoring or new splash search.
- Keep prior negative/deferred draft/stat/items, capture/deference/follow-through,
  banking/batching, recall/resupply, broad AoE, PvP focus, dash and teleport trials.

## Candidate policy and limits
- camp_focus.h selects the lowest positive health among at most 16 personally
  visible in-range camps; exact ties preserve engine order. No hidden live reads.
- Every camp basic and reset follow-up uses a fresh selection. After the initial
  basic/splash, refresh the basic-range survivor and restrict offensive cast/reset
  aim to it. No survivor retains existing longer-range spell selection. Splash
  can still hit other camps; no ally-vision assumptions or across-turn handles.
- Keep the existing 18000 fuel guard, action legality and postmovement refresh.
  The selector adds bounded scans; that guard is not measured fuel headroom.
- Eight other source files remain byte-identical to edit_commit. Draft/stat RNG,
  shops, recovery, routes/cooldown memory, PvP, banking/locks, four shared round
  bytes and official yield keep the edit-base policy. No new shared protocol.
- Risks: wounded camps can belong to less useful groups; kills alone do not earn
  rewards; focusing can lose splash/useful damage or wake another group. Extra
  scans can cost turns under fuel pressure. Group capture/banking problems remain.

## Checks and next step
- Trusted build compiles a selection contract: later wounded camp beats earlier
  healthy camp; zero/dead health is excluded; equal-health ties stay stable;
  reselect after death chooses the next survivor. Not an engine scenario test.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0; exact source a66053e075bb40f86561f53a77318cf06511304c9a1fb2ca6334ff413c93d1ba.
  Report .agent/check-task-8dbeeaaf739e428597d05685211480df.json inspected;
  saved copy task-8dbeeaaf739e428597d05685211480df-bot-check.json.
  Smoke IDs ebb95790106b70ff619d7683e470d1a7a1af8c334a63ebb11e5c6fb76ee81a4e
  and 5d0f6f99597ee4042cd15f85a60977520b826f592b2e27e002dbe4acec4b87e4.
  Build/smoke success does not establish completed full games, focus branch
  coverage, normal-turn headroom or competitive strength. No source edit afterward.
- git diff --check PASSED, exit 0. Decision JSON records exact file hashes,
  evidence limits, parameters and risk. READY_FOR_EVAL, with no strength claim.
- Next: supervisor evaluates exact checked source against edit base and protected
  champion on varied maps/both sides. Reject unchanged/lower matched win rate;
  inspect target choices and camp-damage/collection efficiency before broadening.
  No agents, tournament evaluation, commit/push, publication or official action.
