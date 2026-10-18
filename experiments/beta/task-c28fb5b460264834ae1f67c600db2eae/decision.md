# Respawn-aware reachable camp scheduling

Task task-c28fb5b460264834ae1f67c600db2eae, beta, bot/beta.
Input/HEAD aa89dd9b284e35125c9e218d79a6e0c7ae380183; trusted edit commit
 d2d57274232ca7cead5bacf650d6f51fd5b3bc3d / source
7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
All six source files byte-matched the edit commit on entry; differences from HEAD
were trusted preparation, including removal of circuit_policy.h. The protected
champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in Git. Latest
candidate completed evaluation; pending continuous self-play is not a pending
unpublished experiment. No recovery or publication is needed.

## Decision
Bottleneck: geometric camp ranking forgets observed cooldowns and ignores path
length, capture overhead and reward ratios. This is a source/rules deduction,
not a traced cause of any loss. Choose a bounded, reachable reward-per-time
scheduler, retaining the baseline farming roster, combat, bank-each-bag policy,
shopping, channel preservation and full spawn recovery. Falsifiable hypothesis:
remembered cooldowns plus reachable travel/clearing/capture estimates increase
submitted gems and matched wins, especially corners. Regression in matched wins
or throughput, or increased suspension, falsifies it.

Why now: evaluated harvest circuits (aa89dd9b / source 7a4e377b) tied the edit
base in 24 same-input side-paired cases (delta 0.0). Its 33W/15L and zero faults
against the protected champion are a different comparison. Corners was 3W/5L;
lanes and interlock were each 7W/1L. Collision losses ac40ab67 (beta A, round
684, 13 deaths, 352 collected/176 submitted) and c886ab82 (beta B, round 740,
9 deaths, 594/418) show survival weaknesses too, but no trace attributes those
deaths to routes. Full identities and final metrics are in development-evidence.
Today's edit source is not aa89dd9b and has no new comparative result.

Frozen manifest 5f1d852bc02f2028f069e4a0a444450add0da587ca0596044e410e399a645d8d:
gamma 1b34f42a / source 3ce565f6 stores observed respawn deadlines, computes
reachable value/time and banks each bag. Its compatible observation discipline
motivates the adaptation. Beta retains its own bounded geometric shortlist,
roster Varg/Tavi/Ryth/Vendetta/Marcella and existing item/combat/recovery policy;
it does not adopt gamma's melee-first draft or monolith exclusion. Alpha
6af1685b / source 87b9be45 uses random roster/stats, enemy-first combat and a
nearest-camp union with no respawn memory. No private opponent state accessed.

## Implementation
- Cache a lower-bound respawn deadline only after a visible group-state query.
  Filter still-cooling observations before the 12-group shortlist. Expiry means
  unknown, not asserted alive; blocked spawns can delay respawning further.
- One native forward distance field per farming decision uses current terrain
  and visible occupants. Score only free reachable goals: actual attack rings,
  cleared capture spawns, or unseen spawns requiring scouting. Visible empty
  spawns of hidden camps do not masquerade as useful scouting goals.
- Cost is ceil(path tiles / base move speed) + health/Strength + capture_time+1;
  value is gems + 0.12*gold. Multiply by 0.85 for route commitment and 1.35 for
  visible allied congestion. Unknown health uses static design estimates.
- Preserve own capture occupancy and a single visible collector. Continue to
  use the baseline cheap geometric shortlist before live queries. Temporarily
  defer unreachable entries for 12 rounds so they cannot monopolize all slots.
- No new field below 65k remaining fuel; scan stops at 45k, action planning
  reserves 18k. Do not score partially inspected groups. A bounded visible-camp
  combat fallback yields normally. Existing move helper has two reveal retries;
  selected-group combat refreshes visibility even after a failed reveal move.
- If no work is selected, vacate a collected spawn, including gold-only captures.
- Pure policy header has ten compile-time lifecycle/ranking regression cases.
  Existing integrated source invariants continue to cover channel, capture,
  observation, free-root, reset, recovery and deliberate-draft contracts.

Rejected: repeating the harvest experiment after zero matched gain; changing the
roster/items without evidence; blanket weak-camp/monolith filtering (historical
isolated variants failed to establish additive gains); and speculative enemy
avoidance without action traces. Survival routing remains a separate next idea.

## Limits and validation
Engine 2.1.6, lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Current docs unchanged; consulted BOT_REFERENCE,
RESEARCH, organizer record, Playbooks B/C/F, handbook camp lifecycle and pinned
C++ distance-field/camp-state contracts. SDK SHA256
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Organizer page is a download hub; additional policy and production parity remain
unverified. No new online sources or official actions used.

Risks: extra field/query fuel, conservative clear estimates, the bounded shortlist
missing better distant groups, dynamic allied blockers, unseen enemies and
cooldowns delayed beyond the observed lower bound. Checks and smoke completion
cannot establish comparative strategic gain. Exact final check is recorded in
NOTES.md; supervisor evaluates once and applies the separate champion gate.
