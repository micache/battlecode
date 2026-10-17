# Operational summary

## task-65061b8e709444da8c979245d01553c9 — fund basic attacks instead of unused spells

Playbook C (item value). Hypothesis: redirecting the existing Focus shopping
slot to Strength, while retaining Health builds and the original RNG sequence,
will increase basic-attack damage and reduce farming time for those builds in
the accepted policy, which never casts abilities.
Falsifiable expectation: selected build indices 0/1 buy Power Strength shards;
index 2 still buys Power Health. The same gold/count/permission guard applies.
Every non-shopping decision and RNG call remains identical to accepted source.
Expected strategic benefit: faster clears and more useful attack damage;
clear speed, survival, and win-rate effects require supervisor evaluation.

Identity: beta; bot/beta; task-65061b8e709444da8c979245d01553c9.
HEAD/input: 6450f60028bac2047cddd8cb8be0710823d583d3.
Accepted edit start: 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9;
source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source file hashes and accepted Git blobs match supplied handoff.
Initial bot.cpp diff from HEAD is trusted restoration of accepted, not this
experiment. Accepted Git/snapshot preserves baseline outside edit transaction.
Latest task is evaluated/PUBLISHED, not pending. Prior interrupted recovery
remains in experiments/beta/recovery/task-40d0fac06d944338a6ad7b95d26248c1/.
Previous operational notes archived through task-22caf7462e2948bb8845e85c3489e69a.
Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. C++ header hash matches supplied
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Reviewed documentation hashes unchanged. Separate organizer AGENTS.md remains
unavailable. Relevant supplied rules and installed item/shop contracts consulted.

Development context: evaluation e45758b294b67c2628adb9cc19e7739c188f6d9dfb570283e7988dad30cd56b3,
commit 6450f60028bac2047cddd8cb8be0710823d583d3, source
0c8c6de101ec85fcad250ef308157891de39e173751780d4e7b117285a73e5a1,
INCONCLUSIVE/provisional-three-map-wiring, 19W/5L, zero recorded faults/missing.
Representative losses, both side A:
32ab393f7995e4359617fc4f1ab81dece28c104fba189f4eea2cb852c918ddfd (corners),
ca5e1fa20362978daeb63303b6475007e9aca84e9637b2eb2929d7e88b6da6cf (elkring).
These evaluate the spell candidate, NOT the restored accepted source or this
candidate. Source-supported failure: accepted buy_items can repeatedly select
Power Focus shards, but no accepted path casts an ability. Final-stat slice
for the elkring loss was bounded/truncated; no completed aggregate was derived.
No turn-level evidence establishes shopping as the cause of those losses.

Contracts: GameRules.md:245–259 (Strength basic damage / Focus spells),
280–302 (30-gold shards, growth stats, five shards make Power emblem),
727–762 (Ren retaliation scales with Focus). C++ cambc.h:1449–1459,
3550–3564 item names, growth and shop/count permissions.

Implementation: remap only the Focus entry of buy_items' three-slot array to
Power Strength. Preserve initialization's random_number(3) call, build indices,
Health selection, purchase guard, all tactics, draft, channels, and turn yield.
This is an independent itemization experiment against accepted; the previous
spell implementation is not included.

Validation: inline Python comparison against accepted Git blobs passed, exit 0.
Report: experiments/beta/task-65061b8e709444da8c979245d01553c9/shopping-diff-check.txt.
All source files match accepted except the one array-entry substitution and
its comment; no new runtime trace or strategic improvement is established.
`git diff --check` passed, exit 0.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
passed, exit 0, for exact source
3b7c5e96f4c06df6f9cbb6905f1f35474d5b0a4ba7c7e03e54da511fbe8288fe.
Report: .agent/check-task-65061b8e709444da8c979245d01553c9.json.
Reference: check:task-65061b8e709444da8c979245d01553c9:3b7c5e96f4c06df6f9cbb6905f1f35474d5b0a4ba7c7e03e54da511fbe8288fe.
Smoke IDs: 0af0f3dfddfbe9da1edba22721168cf3bf1be90936d087b00270842722e812ac,
7d3dfeb144b7500b44f3688568c6f57fef62d436114e3fa5c70a3720220bdf41.
Report does not expose completed-game outcomes or measured fuel headroom;
wrapper success alone does not demonstrate strategic improvement.
Remaining uncertainty: Ren loses incremental Focus retaliation; Strength may
change attack/kill timing and future farming routes. Health and Strength builds
may perform differently by champion/map. Do not combine this experiment with a
future spell policy without a new evaluation. No measured fuel headroom or
strategic gain yet.
Next: supervisor evaluates the exact checked source against accepted; compare
farming throughput, survival, and submitted gems for former Focus builds.
