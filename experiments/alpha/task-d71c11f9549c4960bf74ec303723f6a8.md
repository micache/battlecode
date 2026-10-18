# Current experiment: task-d71c11f9549c4960bf74ec303723f6a8

## Identity and status
- Bot alpha, branch bot/alpha; clean entry and edit commit/input
  6af1685b849ad23ee9eaadb1a8de18742318d87b; base source
  87b9be4549dd0ee3a3038907bcfb86b79cfb2d33f344f8749d9532a8e6382e01.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
  No unfinished patch at entry. Latest candidate evaluated INCONCLUSIVE, not pending;
  pending continuous self-play is separate. No agents, commits or publication.
- Engine/SDK 2.1.6, historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Unchanged documentation hashes verified; full-review basis task-4a36c64286504efea17aa49a4a94b17f.
  Read compact reference, research/organizer limits, relevant economy/combat/
  execution playbooks, handbook AoE/capture/kit sections, ability API and installed
  C++ declarations. Installed header hash matches brief. Organizer page is a
  download hub; event-policy/production-parity limits remain explicit.
- Previous operational notes archived as task-4a36c64286504efea17aa49a4a94b17f.md.

## One hypothesis
Area- and finish-aware ability scoring will reduce mean completion round on matched development cases won by both versions without lowering matched win rate; unchanged/increased rounds or a win-rate regression falsifies the hypothesis.
This is an unmeasured rules/source deduction. Win rate remains the safety gate;
rounds are a throughput diagnostic in the currently saturated development panel.

## Evidence and choice
- Evaluation 3886f315a6fa4f70cd6f34957d02d043f053cdc101399dad9c36674b6e892f84
  measures this exact edit source. Supplied development summary: 48W/0L, zero
  faults/missing/unknown; mean round 557.229, submitted 1012.792, deaths 1.125.
  Distinct continuous self-play inputs: 24W/0L, mean round 538.083. Repeated games
  are not independent. No current-source loss example or turn trace is supplied;
  no causal claim about particular wasted casts or holdout details.
- Frozen manifest d6cf7c9195fdb55a481b00dc2c1220066fc4127f81ab0368a94a3b5dafaa1f89
  and all four source sets verified. Beta 6450f600 uses basic plus one unit spell;
  gamma e9704a21 and starter 144ab5a9 use basics only; frozen alpha 6af1685b is
  the edit source. All retain positional random draft/stats, nearest-camp farming
  and immediate banking. They are arena source observations, not runtime traces.
- Incumbent scores only primary AoE damage, ignoring additional visible victims;
  generic raw spell damage also ignores champion shields/mitigation. Its max-useful-
  damage score can prefer a nonlethal hit over a valuable finishing cast.
- Prior global capture priority has negative evidence (task-fc527... / evaluation
  59f8b837...); fixed draft/Strength and 40-gem batching also remain rejected.
  Vendetta's kill passive refreshes cooldowns, not the one-cast allowance; no
  unsupported same-turn cast chain added. Repeated spawn-heal-only ideas deferred.

## Candidate policy
- Changed only combat ability scoring in bot.cpp; added combat_scoring.h.
  Basic target ordering, draft, item choices, capture/travel, banking/retreat,
  channels, defensive fallback, shared memory and official yield remain unchanged.
- Snapshot at most 16 visible living same-category targets AFTER the first basic.
  Score direct and AoE damage capped at current health. For champions use the
  SDK's target-specific predicted health loss; for camps use raw damage capped
  at health. No hidden live reads or persistent target observations.
- AoE aims only at those visible unit positions, counts victims within the kit's
  Chebyshev radius including victims outside cast range, and counts primary once.
  Score all candidates from a frozen observation set; no actions during scoring.
- Deterministic finish bonus: camp 20, champion 100 damage-score units. PvP control
  remains worth 20 per affected target. Reset comparison uses the same finish
  bonus on its estimated extra basic; actual follow-up retains first-target policy.
- At most two slots, 16 targets and 16x16 pure distance comparisons per slot;
  preserve 18,000-fuel reserve and requery target/readiness before action.
  No fuel override. Eight compile-time scoring regressions are included in the
  actual bot translation unit (central/edge/isolated splash, overkill, finish,
  shielded zero damage, control-only value and dead-target exclusion).

## Validation and remaining uncertainty
- Entry/documentation/SDK/opponent hashes and five unchanged source files verified;
  decision and evidence limits saved in this task's -decision.json.
- git diff --check PASSED, exit 0 (before trusted check).
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Exact checked source:
  b87639faa949861e2afb04cf863943dae3ea1ad95c3b58999fe1bd456c31e4fd.
  Report .agent/check-task-d71c11f9549c4960bf74ec303723f6a8.json;
  reference check:task-d71c11f9549c4960bf74ec303723f6a8:b87639faa949861e2afb04cf863943dae3ea1ad95c3b58999fe1bd456c31e4fd.
  Approved check-report agrees. Reports expose summary only, no detailed compiler/
  runtime diagnostics. Eight included compile-time assertions passed in this build.
  Smoke IDs bdd2187b40888491e9653c9985212ba99cef37f4bcf1e331d0aab9cd9dc73a27
  and 8ca40a0d2f73e1f9c89ff778a4ec84cc6b0f9e46d70e73becd469c566f9f7b6a.
  IDs/exit alone are not a full-game completion or improvement claim.
- Final git diff --check PASSED, exit 0; no bot-source changes after trusted check.
- No tournament evaluation run here. Improvement, ability branch coverage and fuel
  headroom are unknown. The reserve is a guard, not measured headroom.
- Risks: scoring cost may defer casts; extra AoE can awaken other camp groups;
  raw camp/basic damage ignores mitigation/item-specific effects, and reset
  prediction remains approximate. AoE scores only the current combat category,
  not allies or other categories; off-unit optimal centers are not searched.
- Next: supervisor compares exact checked candidate with edit base and protected
  champion across maps and both sides. Reject lower win rate; inspect paired win
  completion rounds and objective throughput before accepting a speed claim.
