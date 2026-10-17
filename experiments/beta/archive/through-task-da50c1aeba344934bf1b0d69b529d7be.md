# Operational summary

## task-da50c1aeba344934bf1b0d69b529d7be — bypass living Monolith groups

Playbook C (farming cost/risk). Hypothesis: excluding Monolith-containing
camp groups from basic attacks and travel until visibly cleared should reduce
costly farming attempts and improve collected/submitted gems. Falsifiable
invariant: neither stationary nor post-movement farming attacks any member
of those groups; unknown/alive/respawning Monolith groups supply no goals,
while visible reward-available ones remain capturable. Other groups retain
existing attack order/routing. This is group-level because all members must
die before any reward can be captured. No claim of measured benefit yet.

Identity: beta; bot/beta; task-da50c1aeba344934bf1b0d69b529d7be.
HEAD/input d7a41c2ee29b421e252ec28c09acce91f371b1bb; accepted edit start
0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; base source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source files matched accepted Git blobs before editing. Initial diff
is trusted restoration, not unfinished work. Accepted Git/supplied snapshot
preserves baseline. Previous task PUBLISHED and evaluated, not pending;
prior recovery artifacts preserved. Prior notes archived through task-5f975ba1d49946e4ad80ce19a9aa7fb1.
Engine/SDK 2.1.6; lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation unchanged per handoff; compact
reference, relevant Playbook C/rules and installed C++ contracts consulted.
Separate organizer AGENTS.md remains absent.

Context: evaluation
6340e6381455fa3f1e731f7cf3bf6ee3b67aa3cfbb6dcd52cbf5eaff98cfabe2,
commit d7a41c2ee29b421e252ec28c09acce91f371b1bb, source
091246b8a132f0c4e9df4762186e7d7e7ce1f3033f2826bd398629b96b101deb:
INCONCLUSIVE/provisional-three-map-wiring; 5W/19L, zero reported faults,
missing or unknown reliability. Collision losses:
4e075b7382faa63834ef0327d3cc2df34395c83a8999813234c57b8d936a98a2 (A),
fbbc56c8f68c326bf4603d909378f21e8d690129e13bdc6900c9cd23f801b491 (B).
Development means: 29.04 deaths, 673.42 collected and 509.25 submitted gems.
These evaluate the last-hit candidate, NOT restored accepted/current source.
A final.json slice for the A loss was bounded/truncated: no complete team
aggregate or Monolith-specific cause derived. No bot/engine failure evidenced.
Source reproduces unconditional in-range camp attacks and all-group routing;
there is no type/cost/risk eligibility check. Monolith presence/fight frequency
in those matches is unknown; this is a source/rules-supported exploration.

Contracts: GameRules.md:169-206: Monolith has 20,000 HP/200 Strength,
versus Wolf 1,350/20 and Elk 2,400/60; grouped rewards require all members
dead and uncontested occupancy. Installed cambc.h:2988-3000: kind and spawn
position are stored public metadata, not hidden live state. 4310-4374:
group membership/spawn tiles are immutable metadata; state() requires current
spawn visibility; reward_available means all members defeated.

Implementation: bot.cpp adds one lazily cached bitboard built solely from
static map group membership/type/spawn metadata. All tiles of every group with
a Monolith are marked. Both farming attack loops skip marked camp spawns.
Routing skips those groups unless their current visible state is
reward_available. Short-circuit visibility protects hidden live state reads.
Existing non-Monolith targeting/order, movement, banking, recall, shops,
channels, draft, shared memory, PRNG and turn yield remain unchanged.

`python3 experiments/beta/check_monolith_groups.py` PASSED, exit 0.
Report: task-da50c1aeba344934bf1b0d69b529d7be/monolith-groups-invariant.txt.
Source invariants cover both attack paths, group-wide exclusion, visibility
short-circuit, cleared-group exception and cached metadata-only classification;
accepted baseline and five unsafe mutations rejected. Removing this policy
restores accepted source exactly; all other source files match accepted.
This check does not execute game behavior. `git diff --check` PASSED, exit 0.
Trusted command:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; exact candidate source
55d70a726fed2422dac95fb0ce87a701fc6a81be3bbb473fa1fa57e2495ce48f.
Local report: .agent/check-task-da50c1aeba344934bf1b0d69b529d7be.json.
Reference: check:task-da50c1aeba344934bf1b0d69b529d7be:55d70a726fed2422dac95fb0ce87a701fc6a81be3bbb473fa1fa57e2495ce48f.
Smoke IDs:
0f23dea12ace530187b7b147545cf45352b060bafbc5e03f851943370128addf,
0bb352b7edcc6a49b3b87db090d61b13a59594202cfda05a88aca1d14178ff02.
Wrapper success establishes trusted compilation/smoke validation. The local
summary provides no completed-game outcomes or engagement/fuel trace; it does
not establish improved farming, reduced deaths or strength.
Uncertainty: exclusion can surrender valuable 200-gem rewards, miss a nearly
dead Monolith or an ally-assisted clear, and send champions farther away.
It does not prevent incidental splash damage or walking through danger.
No full-game, fuel headroom or improved-strength claim.
Next: supervisor evaluates exact checked source against accepted, comparing
collected/submitted gems and deaths; inspect Monolith engagement if available.
