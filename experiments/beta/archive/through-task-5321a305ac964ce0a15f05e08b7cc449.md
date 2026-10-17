# Operational summary

## task-5321a305ac964ce0a15f05e08b7cc449 — tribute on arrival

Playbook C (banking). Hypothesis: starting tribute immediately after a successful
banking move reaches an unlocked altar removes one idle owner turn per eligible
arrival, improving banking throughput. Falsifiable expectation: on an unobstructed
arrival with gems and an unlocked altar in range, the channel starts in that turn,
rather than on the next turn. Failed moves, distant arrivals and locked altars
must not trigger a submission. No change to pre-movement combat/recall priority.

Identity: beta; bot/beta; task-5321a305ac964ce0a15f05e08b7cc449.
HEAD/input 3b2d729de06f1a67aed3f4870f712b9414b9353e.
Accepted edit start 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source files matched accepted Git blobs before editing. Existing Git and
trusted accepted snapshot preserve the baseline; initial diff from HEAD is the
trusted accepted-source restoration, not unfinished worker edits.
Engine/SDK 2.1.6; lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation unchanged per handoff; routine targeted
SDK/API reads only. Separate organizer AGENTS.md remains absent.

Prior task-fd26454d738d4d479e000a4a2377dd16 is PUBLISHED and evaluated, not
awaiting evaluation. Paused task-8f47664e32194d58986ac9ee549f9482 is recorded as
infrastructure failure before task reads, source unchanged; no patch to recover.
Earlier recovery artifacts remain preserved. Previous notes archived under
archive/through-task-fd26454d738d4d479e000a4a2377dd16.md. Reviewed recent history
and archive hypotheses: immediate tribute BEFORE combat was tried; this change
only removes the idle arrival turn AFTER a banking move.

Evidence: evaluation
527828ed31cb19579d6997cecb66dcb8198379c696d2cb5389516d31f1fb2377,
commit 3b2d729de06f1a67aed3f4870f712b9414b9353e, source
a31a67e3aa3738afd7d36e4fc99d490081d3c2ba599bc8701c2c0cf70a5697b1:
INCONCLUSIVE/provisional-three-map-wiring, 10W/14L, zero faults/missing/unknown.
Collision losses: 49dab264af762594507b5a104a3fabf5d50326a5ad8219f911feb71caf291186
(side A) and 3fb8148e98431f4a4021a3cd6e055319b3a80d8509849235eafa14bf3824c970
(side B). Aggregate development means: 816.33 collected, 657.33 submitted gems.
These evaluate the Jungle-shopping candidate, not this restored accepted source.
Both final.json slices expose zero faults; their default slices are incomplete,
so no additional final totals or game completion inferred from them. The supplied
evaluation reports completed games. Losses motivate throughput work but do not
prove arrival delays caused them. Reproducible source defect: accepted banking
calls move_towards_closest(goals), then unconditionally returns without tribute.

Contracts: GameRules.md:116,223-230 permits movement before starting a channel;
starting-turn end ticks tribute. BOT_REFERENCE.md sections 3/6 require refreshed
observations after moving. Installed cambc.h:3687-3694 submit_gems returns void;
3728-3732 move_towards can fail without reaching its destination. No can_submit
helper is exposed. Existing channel/death/action guards remain in place.

Implementation: after successful banking movement, iterate static altar tiles,
query current me.position() and current has_altar_lock(), then submit once and
return if in SDK submission range. The failed/distant/locked fallback still yields.
No new state, shared-memory writes, PRNG calls or routing changes. bot.h remains
the prepared accepted restoration (it differed from input HEAD before this task).

Focused check: `python3 experiments/beta/check_arrival_tribute.py` PASSED, exit 0.
Report: task-5321a305ac964ce0a15f05e08b7cc449/arrival-tribute-invariant.txt.
Checks successful-movement gating, fresh position/range/lock checks, single-submit
return, unchanged behavior elsewhere; rejects accepted source and five mutations.
This is a source invariant, not engine simulation. `git diff --check` PASSED,
exit 0.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; checked source
024ec4553ece7e6085c27b673697af98c49bbfa4adfd6f4c7fee0bb1333b837f.
Report: .agent/check-task-5321a305ac964ce0a15f05e08b7cc449.json.
Reference: check:task-5321a305ac964ce0a15f05e08b7cc449:024ec4553ece7e6085c27b673697af98c49bbfa4adfd6f4c7fee0bb1333b837f.
Smoke match IDs:
e75d5e439838e1ed0b1929d390c6be4964353f6b5d8cd4517103503f2fc42571,
c8faac47a9d06c8753c9007d74e3ed92e0ed1f68247e3c85b2fa2bc9584a7e30.
Wrapper PASSED establishes trusted compilation/smoke validation, not completed
full games or measured channel timing/strategic improvement.
Uncertainty: no per-turn arrival/channel trace is available; engine smoke cannot
establish improved throughput or win rate. Earlier starts also change combat
exposure and may lock movement one turn sooner. Same-turn tribute after ranged
movement is not separately traced by the smoke summary. No fuel-headroom measurement claimed.
Next: validate the focused patch, then supervisor evaluates the exact checked
source against accepted; compare submitted gems and arrival-to-tribute delay if
telemetry permits.
