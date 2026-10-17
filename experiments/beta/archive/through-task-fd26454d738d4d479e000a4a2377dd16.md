# Operational summary

## task-fd26454d738d4d479e000a4a2377dd16 — one Jungle emblem before Power

Playbook C (item value). Hypothesis: completing one Jungle emblem in the existing
chosen stat before buying Power shards reduces incoming camp damage by 30%,
reducing farming deaths/recall pressure and improving collected/submitted gems.
Falsifiable policy expectation: buy only the missing Jungle shards up to one
emblem; once owned, buy no more Jungle shards and resume baseline Power shopping.
When enough gold remains after completion, buy Power shards on the same turn.
The chosen stat and PRNG sequence remain unchanged.

Identity: beta; bot/beta; task-fd26454d738d4d479e000a4a2377dd16.
HEAD/input d188b69f212ec06e245fadf5fded4014895f4027.
Accepted edit start 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six current source files matched accepted Git blobs before editing; Git and
the trusted accepted snapshot preserve that baseline. Initial diff from HEAD is
accepted-source restoration. Engine/SDK 2.1.6, lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Installed header SHA256 matched handoff
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Documentation unchanged per handoff. Separate organizer AGENTS.md is absent.

Latest candidate task-911f8f886a814670b1be3cbd00d28b33 is PUBLISHED/evaluated,
not awaiting evaluation. Prior paused work remains preserved as described in
archived notes; no unfinished patch was applied or discarded. Previous operational
summary archived under archive/through-task-911f8f886a814670b1be3cbd00d28b33.md.
Prior hypotheses in supplied history/archives were inspected; no Jungle-shopping
experiment is recorded there. Existing spawn-recovery fixes were already tried.

Evidence: evaluation 47a9db4891a456de4438c8208e739b10fceba47ca2d289c23b1a203e75cadf40,
commit d188b69f212ec06e245fadf5fded4014895f4027, source
bb36a8534fcffa5fed63040a010a4149ddf21061ff20d32601a753e874096b77:
INCONCLUSIVE/provisional-three-map-wiring, 6W/18L, zero faults/missing/unknown.
Collision loss a0fce2951d8808d370e2d3461597876224d1691acec89e908e317b8c658738b1,
side B: 36 deaths, 990 collected, 814 submitted gems.
Collision loss 2e5024c5e697c8be7f6948a91b50a02e656950d61a1e4689ad522480e2f2a61a,
side A: 15 deaths, 462 collected, 352 submitted gems.
These strategic losses evaluate the collector-filter candidate, not accepted or
this experiment. No bot/arena failure is evidenced. Death causes, recall counts
and per-turn damage are unavailable. Aggregate deaths do not prove a camp-damage
cause. Reproducible accepted-source pattern: buy_items buys only Power shards,
so every farmer permanently lacks the Jungle passive.

Contracts: GameRules.md:286–303: five matching shards automatically combine;
Jungle reduces camp damage 30%; Power instead grants one extra stat shard.
BOT_REFERENCE.md section 4: duplicate family passives do not stack.
Installed cambc.h:2171–2204: item metadata includes combination count/result;
3550–3563: can_buy validates shop/affordability; 3604–3611: item_count indexed by
item type; 3643–3649: buy accepts an equipment count.

Implementation: buy_items inspects current inventory and SDK combination metadata.
Before the existing Power purchase, cap Jungle purchases at the remaining shard
count only if no resulting emblem is owned. Both purchases retain nonzero count
and can_buy guards. Power shopping re-reads gold after Jungle spending. No new
persistent state or shared-memory writes; field decisions and RNG unchanged.

Focused validation: `python3 experiments/beta/check_jungle_shopping.py` passed,
exit 0. Report: task-fd26454d738d4d479e000a4a2377dd16/jungle-shopping-invariant.txt
(relative to this directory). It checks the single-emblem/missing-shard cap,
affordability and permission guards, unchanged chosen stat, preserved Power
shopping and all other source against accepted blobs. Accepted and six guard/cap/
stat mutations are rejected. This is a source invariant, not an engine simulation.
`git diff --check` passed, exit 0.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; exact source
a31a67e3aa3738afd7d36e4fc99d490081d3c2ba599bc8701c2c0cf70a5697b1.
Report: .agent/check-task-fd26454d738d4d479e000a4a2377dd16.json.
Reference: check:task-fd26454d738d4d479e000a4a2377dd16:a31a67e3aa3738afd7d36e4fc99d490081d3c2ba599bc8701c2c0cf70a5697b1.
Smoke match IDs:
f10b4986278786c29c5e9c9e213cffd38f12b53e1b0c48adaffdc2bdf61c329b,
d35d680ffe05d58149ff26dfa898276ce6f87ddc7da36f32a2e05111105b3055.
Wrapper PASSED establishes trusted validation, not completed-game outcomes,
measured fuel headroom, purchase traces or strategic improvement.
Uncertainty: sacrificing one Power bonus shard may weaken combat/clear speed;
Focus builds still lack spell use. Early deaths may precede the 150-gold emblem.
No measured change in damage, recall pressure, fuel headroom or win rate yet.
Next: supervisor validates/evaluates the exact checked source against accepted;
compare deaths, collected/submitted gems and recall pressure if telemetry permits.
