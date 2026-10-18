# Route-directed dash travel

Task task-6be48cfa8a864eaca2308324b0f4cd53; beta / bot/beta.
Input HEAD 672874bb459ad66bfc3e03b3ff7f96a9160fbf56; edit commit
9f7ae1c88a1bd0d5d62ed7713956efd40c95be33; base source
b4e969c76d293beb3fdfd75251814a80cb81d2e147e64ee34f5d7feedcdbb1a1.
All six source files byte-matched edit Git blobs and trusted edit_start hashes.
The initial differences from HEAD were prepared source restoration, not unfinished
work. Prior task is PUBLISHED and evaluated. Protected champion remains preserved
in trusted Git/snapshot. No source recovery, agents, publication or evaluation run.

## Decision
Bottleneck: move_to only walks; no current bot path calls a dash ability. Vendetta
is the fourth pick, so larger drafts leave a mobility tool idle. Only transit
phases are changed. Hypothesis: appending safe route-directed two-tile dashes to
ordinary walking increases farming/banking throughput and matched wins versus
9f7ae1c8. No win gain, lower submitted gems, or increased deaths, bot faults or
fuel suspension falsifies it. This is an unmeasured source/rules deduction;
no per-turn loss trace establishes wasted dashes as the cause.

Latest evaluated source 1afc2983 / 672874bb: 42W/6L, zero faults, INCONCLUSIVE;
matched development-base delta 0.0 on 24 side pairs. Protected-champion delta
+0.75 is a separate comparison. Loss 6adb00fb (corners, A vs gamma
1b34f42a / 3ce565f6, round 409): 658 submitted / 766 collected vs 1032/1032,
one death each. It has five picks, including Vendetta, and motivates a throughput
experiment, not a causal dash claim. Collision c9171081 (A, opponent exact source not supplied in the compact
failure record, round 875) has 872/1026 vs 1012/1100 and eight own deaths. Its three
picks have no dash; this candidate is not expected to fix that loss. Expanse also
has three picks in saved historical evidence; do not infer draft size from area.
Contrasting current evaluation wins are aggregate interlock and lanes: each 8W/0L,
both sides. No individual winning IDs or action traces supplied. Evidence.json
preserves latest source identity and authoritative compact metrics.

Frozen manifest ab20635b: gamma 1b34f42a / 3ce565f6 inspected in full for draft,
routes, clear/capture, banking, items, recall and combat. It drafts Vendetta
second, ranks reward/time with observed cooldown memory, shops at 300 gold,
banks after walking and clears locks; its movement helper only walks. It also
leaves dashes unused. Alpha 5f73d078 / ba646c6e relevant movement/combat sections
likewise omit dash. This candidate uses a distinct rules-based mobility idea,
not an assumption about official opponents. No private worker state accessed.

Rejected: repeating healthy shopping or banking detours after zero matched gain;
a second reward/time routing rewrite after only +0.041667 and interlock regression;
another combat retargeter after -0.041667; adding a roster change to expand dash
coverage without controlled evidence. Earlier harvest/item/shield/draft findings
remain in archived notes.

## Implementation and invariants
- Walk using the existing free-approach field and bounded reveal retry first.
  At goal, retain the cast for existing combat; at >=2 remaining route tiles,
  consider one dash along the same field. No extra distance field or camp scan.
- Only an actual dash with ground target, range >=2, ready cast and movement-
  compatible metadata. Require alive, no channel, no move/cast restriction.
- Examine exactly eight straight two-step candidates. Landing in bounds proves
  the intermediate is in bounds. Both tiles must be currently visible and free
  of walls, holes, altars, enemy spawn, visible units and teleport reservations.
  Deliberately forgo hole crossings and bent paths; range alone is not legality.
- Landing must reduce the existing field by >=2, with finite origin/destination.
  Choose least remaining distance, ties by fixed compass order. Seven compiled
  assertions cover progress, arrival, reversal and unreachable boundaries.
- Reject landing in any visible live enemy basic attack range +1. This guard does
  not prove safety from spells, hidden units or future movement. Camps remain
  legitimate farming approaches under the existing strategy.
- Start at >=45k fuel, recheck >=30k before cast. One attempt, even a false hidden
  blocker reveal. Successful dash refreshes altar-lock placement. Farm caller
  refreshes live camps before combat; banking/recovery return through old paths.
- Draft/items/target ranking/recovery thresholds/channel policy/live memory and
  explicit end_turn unchanged from the edit base. No shared-memory writes.

Risks: cast spent on travel delays attack reset; Vendetta's monster-kill refresh
may mitigate but is not measured. Partial route field and strict straight/visible
filters reduce coverage. Fuel gates may skip all farm dashes and are not measured
headroom. A dash sees new blockers; old field is used only as a ranking estimate,
never to authorize a landing. Camp danger and hidden enemies remain possible.
Three-pick rosters will have no mobility gain, only a small helper dispatch cost.

## Rules and validation
Routine iteration; documentation unchanged per trusted handoff. Consulted compact
BOT_REFERENCE, RESEARCH, organizer record, Playbooks B/C/D/F/G, handbook movement,
shared cast allowance, Vendetta dash/reset and channel sections; matching installed
C++ header ability_dash, restrictions, use(vec2), valid_tiles, distance_field and
map bounds contracts; relevant C++ API sections. Engine 2.1.6, lock 00c70d6c,
suite historical-panels-v1; SDK SHA256
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Organizer page is a download hub, not certification of all event policies or
production parity. Compile/smoke evidence will be recorded in NOTES.md. Supervisor
owns matched comparative evaluation and the full champion promotion gate.
