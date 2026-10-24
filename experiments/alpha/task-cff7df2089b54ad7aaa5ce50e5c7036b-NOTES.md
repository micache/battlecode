# Current experiment: task-cff7df2089b54ad7aaa5ce50e5c7036b

## Identity and status
- Alpha, bot/alpha; input HEAD 3e5bc9fe97c646b940fd5266ce8710708c769f84.
  Edit commit 046f1c3a41fe746c65c0982d06062623200fa931, base source
  07022bad764ef37711c5afeddb10a434a0d5f9c5581e519f8bb575ced706fca2.
  All nine initial source files byte-matched edit_commit. HEAD-relative bot.cpp
  and missing camp_focus.h were trusted preparation, not interrupted work.
  Latest candidate evaluated; no pending work or recovered patch.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e stays in Git,
  outside this transaction. Prior NOTES archived by task-8dbeeaaf... ID.
- Engine/SDK 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
  suite published-17-release-225-v1. Unchanged documents: compact reference,
  playbooks B/C/D/E/F/G, RESEARCH/organizer limits and relevant C++/SDK vision,
  attack/range and allowance contracts consulted. Installed SDK SHA256 verified
  ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
  Organizer page is a download hub; full event-policy/production parity unknown.

## One falsifiable hypothesis
Earlier disengagement from clearly unfavourable visible fights increases matched
development win rate over the edit base. Unchanged or lower win rate falsifies
this prediction. Boss deaths, bag loss and submitted gems diagnose the mechanism;
collection and fuel diagnose regressions. This is an unmeasured source/rules
hypothesis, not a traced explanation of any particular death.

## Evidence and decision
- Prior camp-focus experiment: evaluation 7bf00779e54a677aca1f27aace3e649723c9c120ee10a49d0f5f5aa17d8b3f8b
  measures 3e5bc9fe / a66053e075bb40f86561f53a77318cf06511304c9a1fb2ca6334ff413c93d1ba,
  NOT this edit base or new candidate. Development 81W/31L, matched base delta
  -0.0267857 over 56 side pairs. Protected-champion 94W/42L is separate.
  No faults/missing/unknown. Do not reapply lowest-health camp focus.
- Exact edit-base self-play, boss 192daa8e / d10ae8b4 on collision:
  B loss 7ab0ae9f13ad085d8b35c0de8f9a993cb70f9535242e2810e9c37b74bb8493ed,
  round 636, own tribute/collection 286/520 vs 1014/1094; deaths 20 vs 2,
  bag loss 234 vs 58. A loss 3a3e10bacf382beb4bc58b0a42f742e8949af6adf45c4a7b8e5d0e2b1389bdac,
  round 893, own tribute/collection 572/726 vs 1020/1020; deaths 17 vs 0,
  bag loss 132 vs 0. Both completed, no faults or fuel suspensions.
  These establish severe mortality, not the first bad encounter or causal action.
- Latest evaluated source also loses without mortality: corners A loss
  09b121517d2b15bbccfea15aa33b60fe718885fb2f4eaecf0292e68b4a327bfd,
  round 555 vs gamma ecbc8203 / ff511c52; own tribute/collection 732/804 vs
  1080/1284, own deaths zero. This candidate does not fix all objective deficits.
- Contrasting wins: latest evaluated source wins stampede 8/8 across both sides.
  Aggregate only, no invented win trace or claim that local strength caused them.
- Frozen manifest cfc0e709...24d44ca and all six source file sets hash-verified.
  Boss drafts Vendetta/Varg/Ryth first, claims groups, scores value/work routes,
  builds farming emblems, banks at 30/near altars, estimates local hp*Strength,
  and engages/chases or flees by power ratio. Gamma uses selective nearby PvP,
  cheap finishes, no chase. Those strategy differences are source observations,
  not proof of official-opponent behavior or isolated component gains.
- Base attacks any visible enemy in range before banking, and healthy champions
  skip recovery scans. Range/movement exclusion can consume an escape turn.
  Chosen change estimates a clear disadvantage BEFORE attacking and completes
  the existing exposure-aware recovery. This differs from rejected PvP target
  focus, low-health recall thresholds and draft/item or farming route changes.
- Keep prior negative/deferred camp focus, Jungle, gem preference, group routing,
  capture/deference/follow-through, banking/batching, resupply, AoE, dash/teleport.

## Candidate policy
- skirmish.h: trigger only off own spawn, outside channels/recovery. Use current
  personally visible living champions within five tiles, hp*max(1,Strength).
  Self contributes exactly once; exclude self from ally enumeration. Retreat
  when allied power < 0.80 enemy power and an enemy is within four tiles.
- At most 16 champions per side; stop scans below 65000 fuel. Partial scans do
  not force early recovery. Most no-enemy turns use only a native mask check.
  No hidden live reads, remembered enemy positions, or automatic ally vision.
- Set private recovering/disengaging flags before combat. Reuse the existing
  shield, exposure-first legal step, fresh postmove observation, quiet recall,
  and spawn healing completion. Reset both flags on death/full spawn recovery.
- For disengagement only, enemy exposure range is max(basic range + movement,4)
  to avoid immediate recall in potential spell range. Exposure damage remains
  raw Strength, not predicted spell damage. Ordinary low-health recovery keeps
  its prior model. Camps and all farming behavior remain unchanged.
- Keep draft/stat RNG, items, camp rotation, ordinary fight selection, bank/lock
  policy, channel preservation, four shared round bytes and official turn yield.
  No new team-memory protocol; all added state is private to one champion.
- Risks: hp*Strength misses range, focus/spells, shields, passives, mitigation,
  allied intentions and hidden units. Forced sorties can abandon useful capture,
  tribute or kill windows; distant support can be overrated. Recall may still be
  interrupted by pursuit. Scan guard is planning reserve, not measured headroom.

## Checks and next step
- Embedded constexpr regressions compile through the trusted wrapper: equal
  trades stay, outnumbered fights retreat, local support restores balance,
  distant support is excluded, a nearby enemy is required, exact 0.80 stays.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Source 9b5dc61043e4c4c3f35d5d8d55a58060ac69475e383b11f19bcfc2694bb820a5.
  Report .agent/check-task-cff7df2089b54ad7aaa5ce50e5c7036b.json inspected and
  saved under this task's -bot-check.json; check-report returned the same result.
  Smoke IDs f53c399a7b5e6cc65610e8a581548381f3673e7ca79ff4e2e5d721ff5463554a
  and 4019d6062b974415d2c1a0c20a035f575a3ea944162c62c4aee661d6a083de4d.
  First smoke summary reports COMPLETED, zero faults/codes/fuel suspensions.
  Wrapper summary omits candidate side/opponent source; no competitive attribution
  is made. It does not establish branch coverage or normal-turn fuel headroom.
- git diff --check PASSED, exit 0. Exact file hashes saved in decision JSON;
  no source edits after trusted check. Compact game summaries saved by task ID.
- READY_FOR_EVAL, with no strength claim. Supervisor compares checked source to
  edit base and protected champion on matched maps/both sides. Reject unchanged
  or lower matched win rate. Inspect boss mortality/bags/submissions and broad
  collection/fuel before changing thresholds. No agents, tournament invocation,
  commit/push, publication, official actions, or waiting for evaluation.
