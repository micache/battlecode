# Current experiment: task-a5122d9cf25141d1be9a54125ca913cc

## Identity and status
- Alpha / bot/alpha. HEAD/input d94b461d54f92fb73c58943f38e2d852ebb05d68.
- Actual edit 1f5e71f3111c5a492a20f4aaf0bbd3bd0c6fff97 / source
  dd7c6c996f40dd12888dd3e3d6e877bdf574fbd3bb16a19060260f2c33931599.
  All nine initial files byte-matched edit commit. HEAD-relative portfolio removal
  and shop restoration were trusted preparation, not interrupted worker edits.
- Latest candidate evaluated, no pending alpha work. Protected champion
  c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains outside this edit transaction.
- CLI/SDK 3.0.5, lock ac2b5ad2...c56136; published-40-release-305-v1.
  Handoff confirms unchanged documents/SDK, gameplay_review_required=false.
  Consulted compact reference, playbooks B/C/D/G, current support/channel rules,
  C++ export and installed header. Research/organizer limits retained: download
  hub is not review of all policies; no new claim about production parity.
- Previous notes archived as task-2fce257a4fde404bb76f9cf9e3c2ec2f-NOTES.md.

## One falsifiable hypothesis
Proactive exposure-aware self shields and efficient ally heals, independent of
successful combat, increase matched wins and tribute over dd7c6c99. Nonpositive
matched win gain falsifies the prediction. Deaths, shielding/healing and collection
are mechanism diagnostics. This is an unmeasured source/rules deduction.

## Evidence and decision
- Latest evaluation 75d4f10bb17a5965924089a1bc494ae542d9dab6fc80bdc37e1964131a5c0cb1
  evaluates d94b461d / f7e2d6b1, NOT current edit base: full 267W/133L, INCONCLUSIVE;
  development delta +0.01081081 versus this base across 185 side pairs. Zero
  fault/missing/unknown matches. Prior item portfolio not silently reapplied.
- Development loss fbf8281b2408ed033956519cb12a0dc03a8744637ec20bde800389c5ccba84e6,
  A / 00ambush, latest evaluated source above: completed round 1613, own camp
  damage taken 50952 versus 4300 champion damage, 18 deaths, collection/tribute
  585 versus opponent 1011. Own faults/suspensions zero; opponent suspensions 8.
  Willow healingDone 1692, own monster damage taken 12078, 49 collected; Ren
  9 deaths/17 collected. Saved complete compact summary under task prefix.
  No per-turn cast opportunity or counterfactual causal attribution is inferred.
- Contrasting same-source development aggregates: stampede 10/10, starfish 10/10,
  pilgrimage 9/10 across sides. Preserve ordinary combat, draft and routing.
- Second supplied loss 25b74d14...172eb2, A / 00ambush, same source: 49975 camp
  damage, 14 deaths, collection 892/1024, tribute 688/1024; 102 bag loss. This is
  additional exposure context, not proof that support timing caused the defeat.
- Verified frozen manifest e1078aead3487ac0fcfcfebe24aed1c09c92e980d68d3ace0ebf3e96ff230032
  and all six source sets. Inspected boss ea15ef0f / f4b4f65e draft/config,
  support_casts, group risk/combat/capture. It uses Vendetta/Varg/Ryth, camp passives,
  30-gem banking, early support and explicit capture. Transfer only early support
  timing, adapted to raw visible exposure, active-shield guard and heal efficiency.
  Frozen arena strategy is not evidence of official opponents' behavior.
- Rejected/deferred: another draft or item portfolio; repeated camp/PvP focus,
  AoE, route/capture/deference, banking, retreat, dash and recall packages. Earlier
  recovery trials included shields but coupled to broad retreat; this independently
  changes normal support casting and ally sustain without a retreat-state rewrite.

## Candidate policy
- support_policy.h: pure exposure/efficiency decisions and 12 constexpr contracts.
- Call proactive_support after spawn care/channel guards and before recovery,
  combat, banking and farming. Successful support does not itself end the turn.
  Only ready, unrestricted, walking-compatible abilities are used; retain separate
  basic and movement allowances. No self healing; no extra shared/private state.
- Self shield only with no active shield and positive raw visible basic exposure:
  personally visible awake camps or live enemies inside their current attack range.
  Require HP <85% or raw volley * SDK shield duration >=50% shield amount. Raw
  exposure is uncertain: it does not establish aggro, exact damage or future safety.
- Ally heal: visible, living nonself ally in SDK spell range outside allied spawn,
  HP <85%, useful heal >=50% SDK amount. Rank useful*(2-HP/maxHP), selecting highest.
  No detours to heal, no hidden allies or allied shared vision. Free spawn healing
  is not replaced with an ability. Healing can displace Willow's attack reset.
- Maximum 16 observations per support scan; 50k entry/38k scan reserves. Partial
  scans never certify safety. No fuel override or unbounded search.
- Removed the old acted-only support fallback. Everything else in fight(), shop,
  draft, navigation, camp rotation, banking/locks, retreat, RNG and official yield
  remains byte-identical to edit base, proven by source contracts.

## Checks and limits
- python3 experiments/alpha/check_proactive_support.py: observed FAILED exit 1
  before implementation (missing early support/header; old combat gate), PASSED
  exit 0 after. Six source integration/preservation contracts, not runtime proof.
  Report experiments/alpha/task-a5122d9c-source-check.json.
- Trusted compilation covers constexpr quiet/active-shield suppression, injured
  exposure, healthy exposure threshold, zero duration, dead/healthy heal rejection,
  efficiency boundary, urgency ranking and zero amount, plus existing Power tests.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED exit 0.
  Checked source aaa73e40bd670a517c874927769fc4a4bfb35fb1f24908ad69f10936bd684121.
  Report .agent/check-task-a5122d9cf25141d1be9a54125ca913cc.json; owned copy
  experiments/alpha/task-a5122d9c-bot-check.json. No source edits after check.
- Smokes f8284e29ccab730a4d90956bc61a99df1a5e002247ce36b8b9336cbd9aa066dc
  and 5f9654c58f9a522381e0a9d07e3f1f25575ce4cfbb0d8de6cd7ded3e4c7ded4a:
  both COMPLETED; zero faults/suspensions on both sides. Saved full summaries
  task-a5122d9c-smoke-{0,1}.json. Neither includes Varg/Willow, so runtime support
  branch coverage remains unmeasured. Wrapper does not identify candidate side or
  opponent revision explicitly; no competitive win attribution. Deterministic
  smokes are not independent evidence of strength.
- git diff --check PASSED. Self-review confirmed visibility-before-live reads,
  channel preservation, compatible movement, active-shield guard, no post-cast
  early turn return, bounded fuel and unchanged nonsupport source. No agents,
  commit/push, tournament polling or official actions. READY_FOR_EVAL means valid
  candidate, not measured improvement.
- Risks: early shields may displace efficient Varg resets; raw volleys overestimate
  actual targeting; heals may sacrifice finishing damage or go to allies that soon
  recall; max16 scan can miss a better ally; removed late fallback can miss allies
  revealed by movement; support scans consume fuel. Support kits were absent from
  the smokes. Broad strength and exact support fuel headroom remain unmeasured.
- Next: supervisor evaluates checked source against edit base/protected champion
  and frozen opponents under unchanged gates, comparing matched wins, tribute,
  collection, deaths, healing/shielding and reliability. Reject nonpositive gain.
