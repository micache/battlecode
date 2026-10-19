# Current experiment: task-a32cd5b120d14daba1589d8ca4560ff1

## Identity and status
- Alpha, bot/alpha. HEAD/input c2f99412bc40526f1cf83b0ae91d64110766fbdd;
  edit commit 046f1c3a41fe746c65c0982d06062623200fa931, source
  07022bad764ef37711c5afeddb10a434a0d5f9c5581e519f8bb575ced706fca2.
  All nine starting files byte-matched the trusted edit commit. Prepared bot.cpp
  and removed route_teleport.h differ from HEAD because the teleport trial lost
  against this development base; those differences are not unfinished edits.
  Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
- Latest candidate evaluated, no pending evaluation. Earlier task-758e6444 quota
  checkpoint is empty, its notes match base, final absent; original paths intact.
- Engine/SDK 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
  suite published-17-release-225-v1. Documentation unchanged. Consulted compact
  reference, playbooks C/D/F/G, RESEARCH/organizer limits and relevant C++/SDK
  distance-field, item purchase-value, camp spawn and group-reward declarations.
  Organizer page is a download hub; no additional policy/parity certification.
- Previous operational notes archived as task-5da9c09daeab4e33839a785c51b5c1a8-NOTES.md.

## One hypothesis
After 300 gold of cash plus equipment, preferring eligible gem-bearing camp
groups within twelve extra path steps and applying the same filter to camp combat
increases matched development win rate over this edit base. Unchanged or lower
win rate falsifies this prediction. Collection/tribute and time spent on gold-only
camp cycles are mechanism diagnostics. This is an unmeasured rules/source deduction;
final statistics do not establish the cause of any particular lost game.

## Evidence and decision
- Latest evaluation c8ca92a9...89e6 measures c2f99412 / source 0ef30884...4fd6,
  not today's edit base. Development 80W/32L vs base 84W/28L, matched delta
  -0.0357143 over 56 side-paired cases; faults/missing/unknown zero. Teleport
  trial is not reapplied. Champion comparison 94W/42L is separate.
- Exact-base continuous self-play: 0W/5L, collection/tribute means 346/271.2,
  earned gold 1935.2, deaths 0.6, faults/fuel suspensions zero. Three games
  face gamma ecbc8203, two beta 61d59667; source revisions are not pooled.
  Examples: collision B a0cad9ca...bbe93 and collision A be23d074...0a71a vs
  gamma. Requested first summary is retired/unavailable; no turn trace inferred.
- Later-source ambush B loss 55684e0a...04439: own collection/tribute 990/942
  vs 1140/1034, deaths zero, PvP damage zero, round 1091, faults zero.
  Ambush A loss c89c456b...7f06d: own collection/tribute 712/712 vs 1052/1052,
  deaths zero, round 755, faults zero. These support throughput concerns only.
- Contrasting exact-base development aggregate: fragment and stampede each 8/8
  wins; collision 6/8, ambush 4/8. No per-turn causal claims from aggregates.
- Frozen manifest 42620aaa...9eb verified, all file hashes matched. Inspected
  gamma ecbc8203 / ff511c52 (melee farmers, passives, cost/value routing,
  selective PvP) and beta 7cab9b0f / fd5e2554 (300-capital soft penalty for
  gold-only groups). This beta revision is not a proven opponent in named losses.
  Its opportunity-cost idea fits our gem objective, but its whole scorer does not
  transfer: broad ranked/group-first route experiments previously regressed.
- Retain negative/deferred findings for fixed draft/stats/items, recall/resupply,
  banking/batching/arrival, capture/deference/follow-through, broad AoE, focus-fire,
  dashes, arrival cooldown, ranked/group-first and teleport trials. This trial
  adds a bounded gold-only preference rather than repeating those policies.

## Candidate policy
- economy_route.h: 300 cash + actual equipment purchase-value threshold, including
  combined Power emblems of any of the three existing stat lines. Consumable
  spending is excluded. No new shopping, stat or draft choice.
- camp_rotation.h caches immutable gem-bearing spawn geometry once. Mixed groups
  stay eligible; the existing private cooldown observations filter both masks.
  No hidden live state, new team memory, target reservation or enemy cache.
- Before camp combat, and only with >=60k fuel, compare nearest eligible ordinary
  spawn distance with nearest eligible gem-bearing spawn distance. Two native
  fields use existing free/occupied-camp goal semantics. Gem field expansion is
  capped at ordinary distance +12. Prefer gems within that bound, else run the
  base farm/combat policy. No reachable gems means fallback, not idle exclusion.
- Any current eligible spawn occupancy bypasses preference, preserving base
  capture behavior even on gold-only groups. No new group state scan or commitment.
- Selected gem policy restricts basic/reset/direct-spell aim points to those
  group spawns. Splash can still hit adjacent gold camps. Reuse the chosen field
  for movement, refresh occupancy before moving and live targets after arrival.
- Fuel gates: entry 60k, second native field 40k, movement 28k; existing combat
  reserve 18k and 16-target cap. Below reserve use base fallback or yield.
- Recovery, PvP, banking/locks, draft/stat RNG, channel guards, four-byte
  shared-round protocol and exception-safe official turn yield retain base policy.

## Checks, uncertainty and next step
- Seven embedded constexpr contracts cover bootstrap boundary, exact detour
  boundary, overlong detour, existing occupancy and unreachable routes.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0, source f9b70535ec37a82250e8507a7ffaff7df204a2bc51ccee064a75c08e2421d657.
  Report .agent/check-task-a32cd5b120d14daba1589d8ca4560ff1.json; saved copy
  experiments/alpha/task-a32cd5b120d14daba1589d8ca4560ff1-bot-check.json.
  Smoke IDs 46b51738f873cba2824a483e8b0e8bf57be063e131183a0a3b896c262e022c7a
  and 108a02926ee746347938d875a5a299acdd86e624d3ca221856d20ce06c39999c.
  The wrapper summary establishes compilation/smoke success, not complete-game
  outcomes, economic branch coverage or normal-turn fuel headroom. All final
  source file hashes match the precheck decision snapshot; no later source edits.
- READY_FOR_EVAL; no comparative tournament invoked.
- git diff --check PASSED, exit 0.
- Risks: gem groups may be harder or riskier than gold; extra fields consume
  fuel; hidden cooldowns remain uncertain; partial gold clears away from spawn
  may be abandoned. No measured mechanism, branch coverage or strength claim.
- Supervisor should evaluate exact checked source against development base and
  protected champion across maps/both sides. If win rate fails to improve, reject;
  inspect gold-only cycles, collection, travel and fuel before changing detour.
  No agents, comparative evaluation, publication, commit/push or official action.
