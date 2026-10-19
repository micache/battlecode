# Current experiment: task-f8007f1eff324236b2f54153b5affd75

## Identity and status
- Alpha, bot/alpha. Input HEAD 13f9acc517f0c9728fe2ad6f9dda30cbfc446e92;
  edit commit 046f1c3a41fe746c65c0982d06062623200fa931, source
  07022bad764ef37711c5afeddb10a434a0d5f9c5581e519f8bb575ced706fca2.
  All nine starting source files byte-matched edit_commit. Initial bot.cpp,
  camp_rotation.h and removed economy_route.h differences from HEAD were trusted
  preparation, not unfinished edits. Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e
  stays outside this transaction. Latest candidate evaluated; no pending candidate.
- Prior empty task-758e6444 quota checkpoint was already audited in retained notes;
  no patch is reapplied. Previous operational notes archived as
  task-a32cd5b120d14daba1589d8ca4560ff1-NOTES.md.
- Engine/SDK 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
  suite published-17-release-225-v1. Documentation unchanged. Consulted compact
  reference, economy/combat/navigation playbooks, RESEARCH/organizer limits,
  item rules and C++/SDK inventory, combine and purchase contracts. SDK hash
  ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264 verified.
  Organizer page is a download hub; no full-policy or production-parity claim.

## One hypothesis
Completing one Jungle emblem in the unchanged chosen stat, and applying its camp
mitigation to recovery estimates, increases matched development win rate over the
edit base. Unchanged or lower win rate falsifies this prediction. Collection,
tribute, camp damage and recovery travel/turns (if available) diagnose mechanism.
This is an unmeasured rules/source deduction, not a traced explanation of a loss.

## Evidence and decision
- Latest evaluation adeab4d2...5c27 measures 13f9acc5 / source f9b70535...1d657,
  not today's edit base. Development 80W/32L vs base 84W/28L; delta -0.0357143
  across 56 side-paired cases. Faults/missing/unknown zero. The gem-priority trial
  is not reapplied. Protected champion comparison 92W/44L is separate.
- That later source lost ambush A b678a0b0...4fecf at round 803: collection/tribute
  890/890 vs 1052/1052, own deaths zero, camp damage taken 23440, faults zero.
  Ambush B 66d59bb2...1a493a: round 805, own collection/tribute 678/678 vs
  1186/1080, deaths zero, camp damage taken 26120, faults zero. Final totals
  support throughput concerns but do not count recovery turns or prove causality.
- Contrasting latest-source development: fragment and stampede each 8/8 wins.
  These are map aggregates, not turn traces. Distinct sources are not pooled.
- Retrieved supplied representative ambush A loss 901380a8...47883 summary:
  completed B win, round 836, own tribute 962 vs 1090, camp damage taken 24720,
  deaths one, faults/fuel suspensions zero. Our Ryth alone took 8200 camp damage
  and received 7475 healing. Feedback context names f9b70535; summary does not
  independently expose a source revision. Saved summary/decision preserve limits.
- Frozen manifest 82e283d5...8e7bf: all six source sets hash-verified. Inspected
  gamma ecbc8203 / ff511c52 and beta 7cab9b0f / fd5e2554. Both buy Jungle and
  Monster Strength before later scaling; selective PvP, group routes and melee
  drafting differ from ours. Transfer only first Jungle protection in our stat.
- Jungle costs the same 150 gold as Power, but trades one extra stat-growth point
  for 30% less camp damage. This can extend healthy sorties without fewer deaths.
  Earlier ce955542 broad draft/Jungle+Monster/capture rewrite was inconclusive
  and not selected. New rationale isolates one family without changing draft/stat
  and couples it to the current recovery model. It is not a reapplication of the
  earlier roster/routing policy. Camp exposure and opponent design are evidence;
  no controlled win improvement is claimed.
- Retain negative/deferred banking, capture/deference/follow-through, recall/shop
  resupply, focus-fire/AoE, draft/stat, route scoring, dash and teleport findings.

## Candidate policy
- farming_equipment.h maps the existing stat index Strength/Focus/Health to Jungle
  shards. At the existing live spawn shop, buy only the shards needed to finish
  one emblem, then return to the original Power line with any remaining gold.
  Use SDK price/combine metadata, can_buy, and fresh inventory after combination.
  At most two equipment buy calls; no recursion, new shop visit or gold loop.
- All three Jungle emblem variants certify the same non-stacking passive; shards
  alone do not. No private state or new shared-memory layout.
- recovery.h scales only visible awake camps' observed Strength by 0.70 when our
  completed emblem exists. Champion threats remain unscaled; hidden state is
  never inspected. Still ignores shields/other mitigation, victim choice and spells.
- Existing 35% low-health floor, 70% scan threshold, two-volley margin, 32-threat
  cap and 45k/28k/18k fuel gates remain. Complete spawn recovery, channel guards,
  escape routing, combat and camp rotation keep the edit-base policy.
- Draft/stat RNG, locking, immediate banking, shopping locations and four-byte
  shared-round protocol stay unchanged. Power's lost growth point can slow damage;
  harmless cluster routes gain little; hidden threats and timing remain risks.

## Checks and next step
- Eleven embedded compile-time contracts check insufficient funds, split shopping,
  exact emblem completion, no overbuy/unsigned underflow, camp-only mitigation,
  a recovery-gate change and preservation of the low-health floor/enemy danger.
  These are pure invariants, not runtime branch coverage or engine simulations.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Checked source 1d7d75b300bf28176744437a80f6bcbc83da195b43a631ddad66a1bbf4fbd39a.
  Report .agent/check-task-f8007f1eff324236b2f54153b5affd75.json; saved copy
  task-f8007f1eff324236b2f54153b5affd75-bot-check.json.
  Smoke IDs 573cdb2f52dcd4cd7307a3ede4d4bfd0e027d570b8ab85db30e468d9888a2dd4
  and eee2e5c8ea813bbcb5cc373a23eee492f6b460e26b963281e561cc5046a1dcae.
  Report establishes build/smoke success, not full-game completion, purchase or
  recovery branch coverage, normal-turn fuel headroom or competitive strength.
- git diff --check PASSED, exit 0. No source edits after the trusted check.
  Decision JSON records final source file hashes, parameters and evidence.
- READY_FOR_EVAL. Supervisor should compare this exact source with edit base and
  protected champion across maps and both sides. Reject unchanged/lower matched
  win rate; inspect collection, camp damage and recovery time before further item
  changes. No agents, tournament evaluation, commit/push, publication or official action.
