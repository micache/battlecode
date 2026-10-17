# Operational summary

## task-5f975ba1d49946e4ad80ce19a9aa7fb1 — occupy camp after final hit

Playbook C (capture throughput). Hypothesis: using movement still available
immediately after the last basic hit on a camp group to occupy that same cleared
group removes one idle approach turn and starts capture earlier. Falsifiable
expectation: after a stationary successful camp attack, an alive champion with
movement available queries fresh visible group state; only reward-available
groups trigger movement toward their own spawn tiles. Already occupying a spawn
tile holds position. Living/hidden/respawning groups and unavailable movement
retain the old return. No second movement is added after a walking attack.

Identity: beta; bot/beta; HEAD/input
348eaa1827e918ec86d345831e2ad3409f5bc645. Accepted edit start
0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; base source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source files matched accepted Git blobs before editing. Initial diff
from HEAD is the trusted restoration of accepted source, not unfinished work.
Accepted Git/supplied snapshot preserve baseline outside this transaction.
Engine/SDK 2.1.6; lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation unchanged per handoff; relevant
reference/rules/SDK sections consulted. Organizer AGENTS.md remains absent.

Latest task-5321a305ac964ce0a15f05e08b7cc449 is PUBLISHED and evaluated, not
pending. Its notes are archived in archive/through-task-5321a305ac964ce0a15f05e08b7cc449.md.
Paused task-8f47664e32194d58986ac9ee549f9482 had infrastructure failure before
reads and unchanged source; earlier recovery artifacts remain preserved.
Reviewed prior capture experiments: task-3b818b28bcb04cca83683548f6c579dc
prioritized ANY cleared group BEFORE camp attacks. This experiment only follows
a successful stationary attack with movement toward THAT newly cleared group;
it retains target order and never defers a currently available camp attack.
No repeated spawn-healing, collector-routing, or spell hypothesis.

Evidence: evaluation
41729874d91f8eb231b3333bc6b60406bd357968e914759709dda6da758c8cd6,
commit 348eaa1827e918ec86d345831e2ad3409f5bc645, source
024ec4553ece7e6085c27b673697af98c49bbfa4adfd6f4c7fee0bb1333b837f:
INCONCLUSIVE/provisional-three-map-wiring; 8W/16L, zero reported faults,
missing or unknown reliability. Collision losses:
c8faac47a9d06c8753c9007d74e3ed92e0ed1f68247e3c85b2fa2bc9584a7e30 (B),
9e687ddb773972ff40211ab6753378d0b3f786fd18fd26a99a0ab40f1daea8e3 (A).
Development means: 721.58 collected, 604.92 submitted gems, 29.08 deaths.
These evaluate the tribute-arrival candidate, NOT this restored accepted source.
They motivate objective throughput; they do not prove missed captures caused
losses. No bot/engine failure is evidenced in this feedback. Source reproduction:
first in-range camp attack unconditionally returns from farm_camps, even after
a last hit leaves movement available and a free cleared spawn one step away.

Contracts: GameRules.md:191-205 and BOT_REFERENCE.md:35-39,59-61: capture
requires uncontested occupancy; extra collectors do not accelerate it; ranged
movement and basic attacks share allowance. Installed cambc.h:3001-3002 exposes
camp_group as static identity lookup; 4301-4345 defines reward_available as all
camps defeated, and requires current spawn visibility for state(). 3441-3442
can_move queries live availability. Existing movement helper filters current
blocking tiles and holds if already on a goal. No dead camp health read needed.

Implementation: only bot.cpp differs from accepted (11 insertions, 1 deletion).
After a successful initial camp attack, check current survival/movement, load
that camp's static group identity, gate its fresh state on current spawn
visibility, then approach its spawn tiles only when reward_available. Existing
movement helper holds on a spawn tile and filters blockers. No post-walk
continuation, shared state, PRNG calls, or new search algorithm.

Focused check: `python3 experiments/beta/check_last_hit_capture.py` PASSED,
exit 0; report task-5f975ba1d49946e4ad80ce19a9aa7fb1/last-hit-capture-invariant.txt.
It checks action/survival/movement/visibility/state/group-target guards and the
unconditional return; rejects accepted source and eight unsafe mutations;
removing the branch addition exactly restores accepted source. Initial check
failed because of an extra parenthesis in its regex; corrected the checker,
with no bot-source correction. This is a source invariant, not engine simulation.
`git diff --check` PASSED, exit 0.
Trusted command:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; exact source
091246b8a132f0c4e9df4762186e7d7e7ce1f3033f2826bd398629b96b101deb.
Local report: .agent/check-task-5f975ba1d49946e4ad80ce19a9aa7fb1.json.
Reference: check:task-5f975ba1d49946e4ad80ce19a9aa7fb1:091246b8a132f0c4e9df4762186e7d7e7ce1f3033f2826bd398629b96b101deb.
Smoke IDs:
8e644e40e1c6960381b4376244f8384159fe59e44a326afd52264532f190df67,
74e98d54da7d8af5271f5550e39e6c6d1127b9abb6273164a2fc08eb94269198.
Wrapper success establishes trusted compilation/smoke validation. Local summary
has no game completion fields or per-turn trace; no measured capture timing,
fuel headroom, full-game result or strength improvement is claimed.
Uncertainty: no per-turn capture or movement trace is supplied. Benefit depends
on residual movement, reachable cleared tiles, contest and later occupancy;
earlier occupancy can expose the champion or duplicate another collector.
Next: supervisor evaluates the exact checked candidate against accepted;
compare collected/submitted gems and last-hit-to-occupancy delay if available.
