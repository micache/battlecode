# Current experiment: task-315eeea3b0ae4c8d84088c2b74fa0b33

## Identity and status
- Alpha / bot/alpha. Input HEAD 2cb76e5dc2fea3032e450e80603c2f3613d107a6.
- Actual edit commit 5f73d0787014e3f712d0eb6234f088fee489b4d8; base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  All eight starting files byte-matched edit commit. HEAD-relative source changes,
  including missing group_farming.h, were trusted preparation, not unfinished work.
- Latest published candidate already evaluated; no evaluation polled. Protected
  champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
- Previous notes preserved as task-e3b7eed54c39451bb7054367309cf8ad-NOTES.md.
- CLI 3.0.5 / bundled engine 1.0.3; lock ac2b5ad2...c56136;
  suite published-40-release-305-v1. SDK header hash 894229e1...6d3 verified.
- Routine unchanged documents: handoff says no full re-review required; current
  relevant hashes match its reviewed basis task-e3b7eed5. Consulted compact
  reference, playbooks C/D/E/F/G, RESEARCH, organizer ledger, item/recovery/draft
  rules and applicable C++ API/installed SDK sections. No unrelated Python review.
  Organizer page is a download hub; complete policy/production parity unverified.

## Hypothesis and decision
A deliberate melee-reset roster with kit-matched Jungle/Strength purchases and
completed recovery/reinvestment increases matched development wins over ba646c6e.
Unchanged or lower win rate falsifies this prediction. Higher collection/tribute,
fewer camp deaths and prompt spending support the mechanism; faults/suspensions
are regression diagnostics. The edit-base bottleneck is a rules/source deduction,
not a demonstrated cause from a current-source action trace.

- Base chooses random champion/stat combinations, buys equipment only alive at
  spawn, and leaves spawn immediately after recall without its turn-end heal.
  Damage/recall interruption can therefore repeat before recovery is complete.
- Chosen policy is a focused composition/economy slice of sustainable farming,
  preserving the base routes. Repeating the full later group-routing overhaul
  would entangle routing/capture changes with its observed map regressions.
- Evaluation 6180f815...6d40e measures 2cb76e5d / a309a76d, NOT today's edit base:
  310W/90L full evaluation; development 292W/78L across 370 games, +0.208108
  versus ba646c6e over 185 side pairs. Collision candidate .4 vs base .6,
  fragment .6 vs .9, yellow-brick-road .2 vs .3. Contrasting aggregate wins:
  lost-world 1.0 vs .3 and fracture 1.0 vs .5, five side pairs each.
- Later-source side A collision loss c4ba842d...dbc3: completed round 1453,
  tribute 507 vs 1042, collection 621 vs 1130, deaths 32 vs 3. Own zero faults
  and suspensions; opponent one suspension. Final totals do not explain turns.
- Later-source side A ambush loss 9aa46ee0...c0a9: completed round 1732,
  tribute 999 vs 1042, deaths 10 vs 8; own monster damage taken 31944 vs 14604.
  Own zero faults/suspensions. No assertion this narrow loss had the same cause.
- Later-source side B gold-rush loss 00375fbe...b038: completed round 2000,
  tribute 649 vs 891, deaths 37 vs 11; zero faults/suspensions. Opponent ecbc8203
  / ff511c52 per supplied example. Full summaries saved under this task prefix.
- Frozen manifest 7e9c3d46...870 and all six file sets hash-verified. Shared boss
  ea15ef0f / f4b4f65e uses Vendetta/Varg/Ryth, risk/value group selection, claims,
  Jungle/Monster then Power builds, bank thresholds and local-power combat.
  Beta 7cab9b0f / fd5e2554 uses Varg/Tavi/Ryth, staged farming builds, group
  economy penalties, collector deference and dashes. These source ideas are
  hypotheses, not proof of live/official play. No private worker state read.
- Import only the compatible build/recovery ideas; keep Marcella third and base
  navigation/combat. Earlier broad disengagement, camp-focus and local capture
  experiments remain negative findings, not automatically reapplied policies.

## Candidate policy
- Deterministic legal unique picks: Varg, Vendetta, Marcella, Ryth, Tavi, respecting
  actual 3–5 draft size. Four melee reset kits can walk then attack. No draft bytes.
- One Jungle emblem: Health for Ryth's bonus-health passive, Strength otherwise.
  Then Power Strength indefinitely. Purchases cap at missing shards, respecting
  SDK cost/combine count and can_buy. No repeated Jungle passive purchases.
- Buy during death and at spawn; Tavi additionally buys equipment in the field.
  Existing lock purchasing/placement remains; no new item family/lock behavior.
- Below 35% health, commit to recovery across interrupted recalls. Walk home
  before recall as in base. Stay on spawn through turn end until fully healed.
  Death resets recovery. Channel early returns remain before live action changes.
- Empty-bag resupply with >=150 gold and <80% health, no visible enemy champion
  or awake camp; Tavi excluded. Reinvestment is coupled to useful healing rather
  than healthy sorties. Personal vision only; no predictive hidden-state reads.
- Removed unused shared-round logging/writes and hello-world draft message. No
  writable shared/draft protocol; recovery is per-instance private state.
- Base nearest-group routing, cooldown memory, bank-any-bag, enemy-first combat,
  casting/target selection, action guards, lock logic, priority RNG and official
  end_turn remain. Source equality verified for unchanged navigation/combat/farm
  sections and main/camp_rotation/altar_control/draft.h/random.h files.

## Checks and limitations
- Host harness compile attempted with g++ -std=c++20 -Wall -Wextra -pedantic
  experiments/alpha/check_sortie_policy.cpp -o /tmp/alpha-sortie-policy-test:
  FAILED exit 127, no host g++. Standalone harness retained, not executed.
- Trusted wrapper red check FAILED exit 1 as expected, three static assertions
  against empty purchase/recovery implementations. Saved -red-check.json.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED exit 0. Exact source
  64b2bce6becad2db579f134d576e8d62b53061b3658cb612338884bb142d7e1e.
  Report .agent/check-task-315eeea3b0ae4c8d84088c2b74fa0b33.json;
  copied to this task's -bot-check.json. No bot edits after this check.
- Compile-time scenarios now pass: partial emblem across visits, affordability,
  completed-emblem exclusion, saturated counts; interrupted recall commitment,
  spawn heal wait, full-heal release, economic recall and death reset.
- Exact-source smoke 03ca2f12...f05c and ef7738ef...8fc7 each COMPLETED, zero
  bot faults and zero fuel suspensions. Full normalized summaries saved. Wrapper
  omits candidate-side/opponent metadata; no competitive score attribution.
- git diff --check passed exit 0. Final source file hashes and identity saved in
  -decision.json. No measured all-map fuel headroom or tournament strength claim.
- Risks: melee opening may duplicate labor; Ryth Health delays clear damage;
  resupply costs travel; nearest-group routing/capture duplication remain.
- READY_FOR_EVAL. Supervisor compares exact checked source against ba646c6e and
  protected champion across matched maps/sides/opponents, inspecting wins,
  tribute, collection, mortality, healing, spending and fuel. Reject no win gain;
  next isolate group commitment/deference only if measured routing losses remain.
- No agents, commits, push, tournament run, official submission or promotion.
