# Current experiment: task-4133354c587642a699e191721aab2290

## Identity and prior work
- Bot alpha, bot/alpha; input HEAD 6a57e28391e9cb003ce0b20c09e7f3a46ca19153.
- Edit commit bf616d85ce50cbb69c611788b2fc1660dbd465a2; source
  0c91f9bf05bff0bfbf70eb1a00633ec2699e650db57a1dcda0316055df93dd26.
  All six initial source files matched this edit commit. Initial bot.cpp diff
  from HEAD was trusted preparation, not unfinished work.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git/
  accepted snapshot outside this transaction. No commits, publication or agents.
- Eight supplied recent tasks are PUBLISHED; latest evaluation INCONCLUSIVE,
  not awaiting evaluation. Pending continuous self-play is separate.
- Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Entry, relevant document hashes, installed C++
  header hash and frozen opponent manifest hash verified; see -decision.json.
- Changed-document review: current handbook, C++ API, installed header, compact
  reference, RESEARCH, organizer ledger and playbooks A/C/D/E/F reviewed.
  Material contracts: is_ready() omits movement exclusivity; valid_tiles is range
  only; group state needs visible spawn geometry; allied locks permit tribute;
  capture needs uninterrupted occupancy; recall arrival needs spawn turn end.
  Export includes camp lifecycle helpers absent from pinned header; use visible
  health, not those helpers. Historical policy/production-parity limits remain.
  Organizer Agents.md is a download hub, not a separate policy certification.

## One hypothesis: ability-assisted capture rotation
Fixed farming composition, legal ability sequencing and capture-aware routing
will increase matched development win rate over the edit source above.
Unchanged or lower win rate falsifies this hypothesis. Submitted/collected gems
per completed round, deaths and wasted travel diagnose the mechanism.
This is a rules/source-grounded exploration candidate, not a measured improvement.

## Evidence and bottleneck
- Latest evaluation bcbcd9f7f6a58d66e6c96708d4ebb36c332c3120d6742a4d1eec181ddbf0bde6
  evaluates HEAD/source 30783869b2a0e1af115e136a2bccea88b4b1b14b0ee0d688382cef8033fd5842,
  NOT this edit base: development 26W/22L, zero faults/noncompleted/unknown;
  full evaluation 40W/32L INCONCLUSIVE. Distinct revisions are not pooled.
- Collision A losses 461b2c6737323f728c57e638998a4c218403a6db4e53043793a6eca19f8ced5f
  and 4fb603bc4452ab0d11bb76474faa399fe4d9d47b502b3ec2090dffd5487cdc40:
  submitted 836 vs 1012 and 762 vs 1034; collected 880 vs 1188 and 806 vs 1100;
  deaths 6 vs 28 and 4 vs 8; both sides zero faults. Opponent revision for these
  individual failure records is unknown. These final aggregates motivate an
  economy race hypothesis, not a claim about particular stalled turns.
- Contrasting supplied development window, same evaluated source: expanse/A
  4W/0L; timing and turn-level causes unknown. Summary saved in -decision.json.
- Frozen manifest: beta 6450f600... adds a unit spell after basics, suppressing
  spells after walking; gamma e9704a21... retreats before low-health recall;
  starter 144ab5a9... uses stationary recall; alpha bf616d85... is our edit base.
  All use random composition/stat buying and nearest-group farming. None of
  these inspected policies explicitly scores capture routes or uses attack resets.
  Source strategies, not proof of runtime behavior or official opponents.
- Base audit: deliberate but random legal picks; no abilities; random stat
  purchases can buy Focus on non-damaging kits; nearby enemy attacks preempt
  banking; camp occupancy is implicit; no ownership or persistent respawn memory.
  Existing native navigation and recall retreat remain useful building blocks.

## Integrated policy and parameters
- Draft Varg, Vendetta, Ryth, then Vesper and Tavi for 4/5-pick maps; complete
  unique fallback roster and queried team size. Splash, kill resets and tank
  clearing are coupled to the ability and item policy; no linked-death bodies.
- Basics first, refresh life/visibility, then best damage/AoE or attack reset,
  with another legal basic after reset. Shield below 70% health when no damaging
  cast chosen. Check readiness, categories, ranges, restrictions and explicit
  walked/exclusive flags. Bounded AoE aims only at a visible target.
- Cache static group metadata privately; score reward versus travel, remaining
  health/Strength, nearby helpers and incoming camp damage. Soft group-index
  ownership costs 8 turns outside role; current target discount 6. Monoliths
  add 80 travel-cost units below 200 Strength without two visible helpers,
  retaining an only-income fallback. No ally vision or hidden live-state reads.
- Prioritize current cleared-group occupancy before banking; lowest visible
  allied ID collects, others rotate. Contest defenders attack without chasing
  off-group targets. Skip visible respawns, remember observed deadline as an
  uncertain prediction, and vacate captured tiles. Three failed progress turns
  defer that target for 8 rounds; observations still determine current state.
- Bank every nonzero bag; refresh and submit after movement, clear hostile
  locks with attack availability, permit allied locks. No 40-gem batching.
- Buy first five Jungle Strength, then five Monster Strength, then bulk Power
  Strength. Passives once, no unbounded gold loop; shop dead/on spawn, Tavi in
  field. Preserve 35% retreat recall; remain on spawn until healed at turn end.
- Free approach goals only; no occupied camp roots. At most two movement
  attempts after hidden obstruction reveal. Native fields, 18k planning reserve,
  early loop exit and cheap no-action yield remain; no fuel override.
- No draft/live memory protocol or random priorities. Private role from allied
  handle order; sparse end-turn fuel samples on turns 1–8 and every 128 turns.

## Validation and limitations
- python3 experiments/alpha/check_farming_policy.py PASSED, exit 0; source-only
  contracts and final per-file hashes in this task's -source-check.json.
- git diff --check PASSED, exit 0.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  final PASSED, exit 0; exact source
  c171145d743854536081bda47395cf3e263fb29cfe25a5c5ddb85a962adadbc7.
  Report .agent/check-task-4133354c587642a699e191721aab2290.json;
  reference check:task-4133354c587642a699e191721aab2290:c171145d743854536081bda47395cf3e263fb29cfe25a5c5ddb85a962adadbc7.
  Smoke IDs 7b67d63672e6d677f7f7d2ba04d2fbe5bd6a4fada4129411d3d36f3bf9a9d2c5
  and 589598e050c5b4a530178bee61ffb36f0b973693684c1f3cb3abed4c438c2a75.
  Two earlier intermediate sources passed before review repairs; final check is
  authoritative. No bot source edits after final check.
- Optional first-check smoke log/final export denied: only this lane's development
  evidence can be exported. Saved -smoke-export.json; no alternate route/retry.
  No claim of completed smoke games, branch coverage or measured fuel headroom.
- Fuel reserve is a policy guard, not a measured guarantee. Static initialization
  and one native path calculation can exceed a guard; stale-resume risk remains.
- Scoring uses Chebyshev travel estimates; native routing can reveal detours.
  Soft roles do not guarantee distributed camps. Nearby allies may be banking,
  not helping. AoE can awaken additional camps; melee composition can lose PvP.
  High-damage group recovery and solo-monolith fallback remain unmeasured.
- Prior negatives retained in archived task-2cc... NOTES: 40-gem batching had
  poor outcomes; isolated Strength buying and earlier small priority fixes were
  inconclusive. This couples Strength to selected basic/reset kits and sustain,
  rather than claiming a repeated stat-only experiment already worked.
- Next: supervisor evaluates exact checked source versus development edit base
  and protected champion on both sides/multiple maps. Compare wins, submitted
  gems per round, deaths and farming distribution. If throughput fails, obtain
  bounded development traces for target travel/capture and fuel samples.
