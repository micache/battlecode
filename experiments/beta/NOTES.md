# Operational summary

## task-911f8f886a814670b1be3cbd00d28b33 — avoid joining existing collectors

Playbook C (capture routing). Hypothesis: excluding visible cleared camp groups
already occupied by another ally from farming destinations will reduce redundant
collectors and redirect travel toward other work, increasing collection throughput.
Falsifiable expectation: a reward-available group with a visible allied occupant
is excluded if self is outside it; if self is already on that group's spawn
tiles, it stays eligible. Alive and unseen groups retain baseline eligibility;
visible respawning groups remain excluded. Extra collectors do not speed capture.

Identity: beta; bot/beta; task-911f8f886a814670b1be3cbd00d28b33.
HEAD/input 0515c6eedc284ee280eba92ff60de115e5096b51.
Accepted edit start 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9;
source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source files matched accepted Git blobs before editing. Initial diff
from HEAD is trusted accepted-source restoration. Accepted Git/snapshot preserves
the baseline outside this edit transaction. SDK 2.1.6; engine lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Installed cambc.h hash matched handoff
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Documentation review unchanged per handoff; separate organizer AGENTS.md absent.

Latest task-65061b8e709444da8c979245d01553c9 is evaluated/PUBLISHED, not pending.
Older interrupted task-40d0fac06d944338a6ad7b95d26248c1 remains preserved under
recovery/. Exact task-8f47664e32194d58986ac9ee549f9482 notes, final and checkpoint
patch were inspected in own attempts_root; it failed before task reads and its
patch is preparation's baseline restoration. No unfinished implementation was
applied or removed. Originals remain preserved. Previous notes archived through
task-65061b8e709444da8c979245d01553c9.

Development context: evaluation
055158fab5b971e85fb158276f837a954d763ba34f31d09cd57dee1cb9cd2480,
commit 0515c6eedc284ee280eba92ff60de115e5096b51, source
3b7c5e96f4c06df6f9cbb6905f1f35474d5b0a4ba7c7e03e54da511fbe8288fe:
INCONCLUSIVE/provisional-three-map-wiring, 14W/10L, zero recorded faults/missing.
Relevant losses, both collision side A:
6cf9be91b3711bdeecc0e1a58651c0b2a1267e5adfa124ed69de24badd7e23ef,
3318d4fc583dff84ec5cf6cbb91fda29d0cdc4a130917c218c26feed68ea32a9.
Those games evaluate the Strength-shopping candidate, not accepted or this patch.
These are strategic losses; no bot/arena failure is evidenced. Aggregate stats
do not establish duplicate collection or its causal contribution to these losses.
The reproducible source pattern is that every nonrespawning group's spawn tiles
are offered to every nearby farmer, even with an existing allied collector.
No turn-level duplicate-collector frequency is available.

History lookup: prior task-3b818b28bcb04cca83683548f6c579dc prioritized all visible
cleared groups before attacks. Its source
c35aa333ec97f25235b09630777b16febbac86cd80423946d2065bb2321ccf02 was INCONCLUSIVE
(3W/3L, delta 0, six games) in evaluation
7721495cdd3613a1c77199c86b3914bb44195ed363c06f9421cc40bd7fb4b5f4.
This experiment instead filters already-served destinations in accepted routing;
it does not repeat that capture-priority patch. Duplicate collectors were an
explicit unresolved concern in that experiment's archived notes.

Contracts: GameRules.md:191–205, BOT_REFERENCE.md:59–61: uncontested spawn
occupancy completes capture; extra allies do not accelerate it. Installed
cambc.h:4301–4346: reward_available means all camps defeated, and group.state
requires at least one visible spawn. cambc.h:4117–4123: champion_tiles(team::ally) supplies only current
visible allied occupancy.

Implementation: cache current visible allied champion tiles minus self in
farm_camps. Inside the existing visibility gate, skip reward-available groups
with another allied occupant unless self is already on that group's spawn.
Preserve hidden-group exploration, respawn exclusion, existing collector
destinations, attacks, movement fallback, channels, shopping, RNG and end_turn.
No new thresholds, shared-memory writes, or persistent reservations.

Focused validation: `python3 experiments/beta/check_capture_routing.py` passed,
exit 0. Report: task-911f8f886a814670b1be3cbd00d28b33/capture-routing-invariant.txt
(relative to this directory). Source invariant rejects accepted source and five
guard mutations; checks every other source region/file against accepted blobs.
It does not simulate engine capture or prove strategic benefit.
`git diff --check` passed, exit 0.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
passed, exit 0, exact source
bb36a8534fcffa5fed63040a010a4149ddf21061ff20d32601a753e874096b77.
Report: .agent/check-task-911f8f886a814670b1be3cbd00d28b33.json.
Reference: check:task-911f8f886a814670b1be3cbd00d28b33:bb36a8534fcffa5fed63040a010a4149ddf21061ff20d32601a753e874096b77.
Smoke match IDs:
d1a6d08bcb524a8e9e39b14eb1ef37977c08a91b24201a935d11cc4631664b31,
a0fce2951d8808d370e2d3461597876224d1691acec89e908e317b8c658738b1.
The compact check report does not expose completed-game outcomes or measured
fuel headroom. PASSED establishes wrapper validation, not strategic improvement.

Uncertainty: unknown frequency and value of redundant arrivals; current visible
occupancy is not a persistent reservation. If the ally leaves, the destination
becomes eligible on the next observation. A contested group may benefit from
reinforcement; distant unseen allies cannot be coordinated. If self and another
ally are already collecting together, neither is forced to abandon progress.
The earlier attack-first farming policy is retained. Fuel headroom, capture
timings, collected/submitted gems and strategic gains remain unmeasured.
Next: supervisor evaluates exact checked source against accepted; compare
collection throughput and submitted gems, with collector counts if available.
