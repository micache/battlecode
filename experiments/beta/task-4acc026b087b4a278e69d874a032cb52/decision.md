# Bounded local harvest circuits

Bottleneck hypothesis: the base submits every bag before seeking another group,
so short, safe nearby harvests can require repeated altar trips. This is a
source/rules deduction, not a proven cause in the supplied loss traces.

Chosen policy: preserve the base roster, builds, zero-bag target ranking, combat
and recovery. Small healthy carriers may collect fully observed, non-damaging,
positive-gem groups within six Chebyshev tiles and six estimated extra bank-trip
tiles. Estimated travel + clearing + capture must fit the remaining 24-round
budget. At >=96 gems, <75% health, a visible enemy within eight tiles, immediate
camp exposure, a winning bag, or the endgame reserve, commit to banking. Once
committed, do not resume farming until the bag is empty. Immediate adjacent
submission remains preferred; safe in-progress capture occupancy is preserved.
No hidden live state, opponent-specific map routes, randomness or shared writes.

Falsifiable prediction: compared with d2d57274/source 7daa9117 on matched maps,
sides and frozen opponents, short safe circuits improve submitted gems per
completed round and wins, with no increase in deaths or stranded bags. Reject
if the extra clearing/delay worsens wins or bag conversion, or if fuel suspension
increases. Longer channels are a risk, not a claimed channel-efficiency gain.

Evidence scope:
- Evaluation 8874fe2cae89ba66b875b2082e00e01e0257b80aaf09fa757c1c5f24f9cd0178:
  development 43W/5L in 48 completed games of the exact edit source, zero faults.
  Lanes aggregate contrast: A 4W/0L, B 4W/0L. Individual winning match IDs were
  not supplied; no per-turn causal comparison is inferred.
- Collision loss 35a896c482526b964ff9dfbfa6d79461021f3494e7fb9d1106bf6311acc0a975,
  beta A vs frozen alpha 6af1685b/source 87b9be45: round 684, submitted 176 vs
  1012, deaths 13 vs 3. Reverse-side loss
  5f8eb6f279d9e66464f9c21f475bcede83dbbc40e6282fd8534579c5a3cc1595:
  beta B, round 740, submitted 418 vs 1034, deaths 9 vs 1. These motivate
  restrictive safety gates, not a claim that delayed banking fixes combat.
- Self-play corners loss
  1ec0801d0d9c8709490ea3a3afe88f4add3494c28266ff9bdcb1681364cabd72:
  beta B vs alpha 0b61a3d4/source 7a14708a, round 444, A won. B's five
  champion records in the exported final slices have zero deaths and modest
  production, consistent with a throughput question. Full B total was cut
  off by the bounded slice and is not reconstructed here. This opponent source
  is not in the frozen manifest and was not accessed. All use current own source.
- Frozen manifest 345bc0171ed5d4cb6d7d3c4b7ed1f44565f7a2aeb1570ee83fbebe4d25bea74c:
  inspected gamma 1b34f42a/source 3ce565f6 (value/time routing, timestamped
  respawn memory, durable melee roster, every-bag banking, 300-gold shop recall),
  and alpha 6af1685b/source 87b9be45 (independent attack/cast allowances,
  nearest-camp union, random draft/build, enemy-first combat, every-bag banking).
  The circuit differs from both; no private worker state was used.

Alternatives: broad batching would risk larger losses in the collision games;
cloning gamma routing would reduce strategic diversity and combine too many
mechanisms. Rejected earlier weak-camp-first, shield-only and isolated item/draft
changes remain negative findings in prior notes/experiments.

Mechanics checked: current BOT_REFERENCE, Playbooks B/C/F, GameRules channel and
capture sections; installed pinned header global_submitted_gems, settings,
camp state and movement contracts. Documentation/SDK hashes unchanged from the
recorded full audit; no full unrelated export reread. Production parity remains
unknown; official older uncontrolled observations were not used as scores.

Validation: trusted bot-check compilation also evaluates thirteen constexpr
boundary regressions for admission and forced banking. These check actual pure
policy functions, not navigation, visibility implementation or game performance.
Supervisor owns matched comparative evaluation; no candidate improvement claimed.
