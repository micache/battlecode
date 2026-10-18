# Current experiment: task-844841b0ef694b819a6ab2fcf1a89387

## Identity and status
- Alpha, bot/alpha; input HEAD cf1c7574dc04a9bb94004b1424ce470f8e243eae.
  Edit commit 5f73d0787014e3f712d0eb6234f088fee489b4d8; base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  All eight starting files byte-matched edit commit. Initial HEAD differences
  were preparation; no incomplete work recovered. Latest candidate evaluated;
  pending continuous self-play is separate. Accepted c0cebd720fcd55e2bbb51d57dd2c398889d4071e
  remains protected in Git. Previous NOTES remain at input HEAD.
- Engine/SDK 2.1.6; historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  Installed header matches 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
  Routine unchanged-document review: compact reference, playbooks B/C/D/E/F,
  evidence ledgers and relevant group/visibility/path API/SDK. Organizer page is
  a download hub; production parity and complete event-policy review remain uncertified.

## One hypothesis
Selecting a camp group by reachable travel and expected work per reward BEFORE
camp combat, and restricting clearing to that group, increases matched development
win rate over this edit base. Unchanged or lower win rate falsifies it. Lower camp
damage per collected gem, higher collection/tribute and paired-win finish rounds
are mechanism diagnostics. This is an unmeasured source/rules deduction, not a
traced explanation of any named loss.

## Evidence and decision
- Evaluation 85a3d036a4d7c0de454b6974fcf8a653fa76bff1da8f109d332619a086fe9d20
  evaluates cf1c7574 / source 9df96ffb3b9509b40f5a93ae59c9b7cbd1b48dde6e8f8580a1f3f29b0c021dd9,
  NOT today's edit base: INCONCLUSIVE, 43W/5L, zero faults/missing/unknown.
  Matched edit-base delta +0.020833 across 24 side-paired cases; champion delta
  +0.770833 is a separate comparison. Latest-source corners and elkring each
  won 8/8 panel games; preserve the existing combat/composition policy.
- Expanse B loss 2f5f185824799a6aaadad90c6b74230e710b56184abca3ab7cc33585b3b1c7a4:
  round 493; collection/tribute 952/928 vs 1008/1008; no deaths, kills, champion
  damage or faults. Camp damage 41610 vs 27600. Opponent revision 54338dc8,
  gamma 1b34f42a / source 3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565
  from the evaluation manifest. Complete final saved under this task ID.
- Collision A loss bd4e101feaaf5d97c12a8637a5c8ef36cd9eaa9ec8ee1bf4c1f57bf6ea50a398:
  round 718, collection/tribute 592/490 vs 1004/1004, deaths 4/2, kills 2/4,
  faults [0,0]. Opponent match revision unknown from supplied summary/final.
  Complete final saved. Do not assume every loss is a farming-only race.
- Manifest SHA256 22e14f787aee81812226f343e1d462dde4c4c3668f245de95098e8c21be7ae8f;
  all six frozen file sets hash-verified. Inspected beta 9f7ae1c8 and gamma
  63d05e37, plus expanse opponent gamma 1b34f42a. They select groups before
  clearing, use remaining visible HP/design estimates and committed routes;
  gamma also prices reward/work. Their melee drafts, shopping, collector
  deference and selective PvP differ from ours and were not copied.
- Previous route-only candidate still attacked any in-range camp BEFORE choosing
  a route. This can preempt cheap work and explains why coupling selection and
  combat is a distinct test despite its small matched gain. Finals alone do not
  identify actual attacked groups or prove that this mechanism caused a loss.
- Prior spawn-heal-only, banking/batching/arrival, draft/stat, resupply, broad AoE,
  focus-fire, travel-dash and global/local deference trials remain negative/deferred.
  No repeated isolated fix was reapplied. Reused the prior measured routing
  implementation, with explicit group ownership of this turn's combat.

## Candidate policy
- camp_rotation.h returns goals plus the selected group's immutable spawn mask.
  Rank travel/clearing/capture/tribute time per gems + 0.12 * gold. Use one native
  forward distance field and at most eight shortlisted groups, sixteen members
  each. Force the previous group into the shortlist for fresh remaining-work
  evaluation; multiply its score by 0.90. Hold current cleared-group occupancy.
- Group state requires current personal spawn visibility. Hidden member health
  uses full design HP as an uncertain estimate; no hidden live state or allied
  vision. Existing observed cooldown expiry is retained. Reward observations are
  usable only in their observation round. Remove known movement blockers.
- bot.cpp plans BEFORE attacking camps. Filter fresh camp handles by selected
  immutable spawn identity for basics, spell aim points and reset follow-ups.
  After movement, rebuild combat handles even on False/reveal, and mark actual
  walking to disallow exclusive casts. Do not walk after a successful cast.
  Incidental splash can still hit other groups; no new splash scoring.
- Start richer routing above 65000 fuel; stop scans at 45000. If no selected route
  or insufficient fuel, retain unfocused base combat and nearest eligible spawns.
  Combat reserve stays 18000. These reserves are not measured headroom.
- Draft/stat RNG, all play_turn priorities, champion combat scoring, shopping,
  retreat, banking, locks, four-byte shared-round protocol and official yield
  remain unchanged. No new shared bytes or fuel overrides.

## Checks, risks and next action
- python3 experiments/alpha/check_group_first.py PASSED, exit 0; report
  experiments/alpha/task-844841b0ef694b819a6ab2fcf1a89387-source-check.json.
  Checks target isolation, precombat planning, fresh postmove observations, exact
  unchanged combat policy apart from the filter, and unchanged other systems.
  These are source invariants, not engine branch coverage.
- Seven route-cost static_assert contracts and the existing cooldown contracts
  compiled in the trusted build. Includes cheap detour versus nearby wolf and
  finishing a heavily damaged committed group. Not full engine scenarios.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Checked source 822811f4c9664771c56f9d52d120cd9ed1dcd83b9de3f76c5d1b10e892ed5f1c.
  Report .agent/check-task-844841b0ef694b819a6ab2fcf1a89387.json inspected locally
  and through exact-source check-report. Smoke IDs:
  df41f9af3178f8cceaf593deb89db60e3bce75e08d01223df8f75e0fdf3db27b,
  8c17c88aa67a44ca5e2c8e614c5c8183f7382a795f31010f90f746b0f5d60dad.
  Summary exposes no detailed runtime/fuel diagnostics; IDs alone do not establish
  full-game completion, group-selection branch coverage or competitive strength.
- git diff --check PASSED, exit 0. Bot sources were unchanged after check start;
  this task's decision JSON records their file hashes and the checked identity.
- Risks: spending planning fuel before every camp fight; ignoring dangerous nearby
  camps; imperfect basic-only clear estimates; duplicated team routes/captures;
  unseen obstacles and shortlist omissions; choosing a different group can abandon
  damaged work despite commitment. No claim of improvement before evaluation.
- READY_FOR_EVAL. Supervisor compares this exact checked source with edit base and
  protected champion across maps and both sides. Inspect group choices/fuel if it
  regresses before changing score weights. No agents, tournament evaluation,
  commit, push, publication, official submission or promotion performed.
