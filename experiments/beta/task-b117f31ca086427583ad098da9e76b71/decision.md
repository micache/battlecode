# Recovery escape routing

Hypothesis: at the unchanged 45% retreat trigger, ranking recovery steps by
observed incoming basic damage before home distance, and recalling only after a
complete quiet observation, improves matched wins and submitted gems by reducing
deaths and lost bags. No win gain, lower submissions, or increased bot faults or
fuel suspensions falsifies it. Recovery-path causality is unmeasured.

## Evidence and choice

Trusted edit 50a0d7d5 / 6d66a77f matches all six source files and recorded per-file
SHA256s; HEAD 61d59667 is the later cooldown experiment, intentionally restored
by preparation. Prior task is PUBLISHED/evaluated, no unpublished candidate is
waiting. Accepted champion 0ca5c04e remains in its trusted Git/snapshot.

Compact metrics and exact identities: evidence.json. Same-edit-source ambush B
loss c52237a0 (round 873) had 1148 collected, 908 submitted, two deaths and 240
lost gems, zero own faults/suspension. Opponent revision unknown in this compact
record. Latest evaluated 61d59667/e05d7dfc collision A loss a2831c57 had nine
deaths, 154 lost gems and 770:1004 submitted, no own faults/suspension. This is
NOT an evaluation of today's edit. Latest ambush A 0d9103e2 instead had just one
death and 600:1076 submitted: objective routing also remains a separate problem.
Contrasting latest-candidate corners and fragment each won 4/4 on both sides;
individual winning IDs unavailable. Final statistics establish losses and risk,
not a traced death during recovery or the new candidate's gain.

The baseline always follows a shortest spawn route before deciding whether it
can recall. It can step deeper into visible attack ranges while already weak;
its generic exposed() also treats asleep camps as active recall threats.
Gold-camp penalties and full reachable/cooldown scheduling had small or zero
matched gains with map regressions; those systems are not restored. A narrowly
scoped recovery upgrade protects existing throughput and tests a new mechanism.

Frozen manifest 96440df1 (six public arena sources) inspected: alpha
046f1c3a/07022bad recovery.h and recover() use summed observed basic damage,
range-edge depth and home distance. Adapt that compatible escape ordering, but
retain beta's 45% trigger and healthy decisions rather than alpha's 35%/70%
threshold rules. Older beta d2d57274/7daa9117 source uses the same original
shortest-home recovery. Gamma ecbc8203/ff511c52 uses reachable value/time farming,
melee-first draft, each-bag banking and shopping recall; do not clone its farmer.
No private state, credentials or official-opponent source consulted.

## Candidate

- Changes only recovery dispatch in bot.cpp and new recovery_policy.h; bot.h
  remains byte-identical to edit. Generic farming posture is unchanged.
- Maximum 32 visible live threats. Camps must be awake and damaging. Enemy
  envelope is current basic range + base move speed (conservative for ranged).
- Rank up to nine one-step tiles including staying: raw incoming basics, weighted
  distance from range edge, then shortest free spawn path. Free adjacent spawn
  wins because healing occurs at this turn end. Visible occupancy is refreshed.
- A complete zero-basic-damage observation starts recall immediately, avoiding
  an unnecessary step into new danger. After a move or hidden-blocker reveal,
  rebuild the observation before recall. At most two movement attempts.
- Shield an exposed recovering Varg without replacing an existing shield. No
  recovery dash: escape steps use the ordinary move allowance only.
- Scan reserve 45k; at most one native home field per attempt, admitted at 55k;
  action reserve 18k. If routing fuel is unavailable, geometric spawn distance
  breaks equal-danger ties. Partial scans never certify a quiet recall.
- Header constexpr fixtures cover overlapping threats, damage plateaus, moving
  away from home to reduce danger, equal-risk home progress and damage dominance.
- No shared-memory protocol, drafting, camp ranking, item or bank changes.

## Limits and next measurement

Raw basics ignore mitigation, shields, target selection, spells and hidden units.
Sleeping camps can be awakened by another unit later. A quiet observation is an
estimate, not a safety guarantee. One-step risk descent can get trapped behind
terrain; geometric fallback and lost recovery dashes can delay healing. The
unchanged trigger may still permit death before recovery. Fuel reserves are
policy parameters, not measured headroom. Zero-gem farming remains unresolved.

Supervisor should compare exact checked source against 50a0d7d5/6d66a77f on
matched development maps, both sides and frozen opponents, with wins/submissions
primary and deaths/bag loss/faults/suspension as mechanism/regression checks.
Protect existing corners/fragment/collision performance; inspect ambush B and
collision A if action traces become available. No comparative evaluation,
publication, agents, commits, official action or promotion performed here.

Rules consulted: compact reference, RESEARCH and organizer record; Playbooks
B/C/D/F/G; GameRules movement, camp wake/capture and channel sections; C++
distance-field export and installed 2.2.5 camp state, restrictions, shield and
movement contracts. SDK SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
The installed SDK DOES expose is_awake(); the stale baseline comment saying
otherwise was corrected. Organizer hub is not a certification of all policy or
production parity. No full unchanged exports were reread.
