# Bounded combat retargeting

Hypothesis: selecting useful damage/finishes across the current camp group or
eligible visible threats, then refreshing targets after each basic/cast, will
increase clearing and defensive combat efficiency and submitted gems. Matched
win/throughput regression or more deaths/fuel suspension falsifies the policy.
This mechanism is a source/rules deduction, not an observed per-turn diagnosis.

Edit base: d2d57274232ca7cead5bacf650d6f51fd5b3bc3d, source 7daa9117.
All six source files matched its blobs at entry; the absent HEAD farm_policy.h
and prepared modifications were intentional. No incomplete unpublished work.
Protected accepted champion 0ca5c04e remains preserved in Git.

Latest measured source ec6ad44a (27dedf62) is different: evaluation 858f5f0f,
35W/13L, zero faults; matched edit-base delta +0.041667 with interlock regression.
Its collision losses 19bdaff9 (A, round 627) and 774bf8fc (B, round 899)
submitted 132 and 788, with 7 and 8 deaths. Contrasting development win
b6788e49 (A, round 573; map and own exact source unknown in supplied
final statistics) submitted 1030 with zero deaths. This ID is listed under the
same evaluation in development-selection evidence, not necessarily the candidate.
Saved full final
statistics are hindsight, not runtime inputs; they do not prove a combat cause.
Raw final files report engineVersion 0.0.1; pinned runner/SDK is 2.1.6. Do not
interpret that embedded field as proof of official parity.

Frozen alpha 6af1685b / source 87b9be45 retargets after a cast and compares
capped damage with reset attacks. Gamma 1b34f42a / 3ce565f6 focuses one target
and observed camp deadlines. Beta retains its group routing, farming roster,
shield, banking and recovery. Adopt alpha's compatible refreshed-action idea,
not its random roster/stat build, enemy-first policy or rich logging.

Source bottleneck: fight(target) returns immediately when a basic kills that
target; its reset attack cannot select a surviving neighbor, and spells are
scored on one arbitrarily ordered target. Varg splash can also invalidate that
target. A fresh candidate scan after each action can use remaining allowances
without changing route strategy or presuming a kill grants extra casts.

Policy: bounded 16-target scans; one initial basic, at most one successful cast
(including the existing shield), then a fresh basic if the engine allows it.
Score capped effective damage plus half an attack's value for a finish; include
observed Varg splash and AoE damage. Reset must have a fresh in-range target.
Check current availability/restrictions, visibility/health and movement exclusion.
No movement after successful combat; no same-turn capture or chase expansion.
No new shared memory. Reserve 18k fuel for completion; abandon optional scans
below 30k and retain the current cheap legal fallback.

Rejected: reapply cooldown/path ranking (small measured gain with map regression),
repeat harvest circuits (zero matched gain), change draft/items or banking at
the same time (prior isolated variants did not establish additive gains).
Risk: more live queries, finish/splash ranking may split damage, scan caps can
omit targets; shield still competes with reset. Supervisor compares matched
wins, submitted/collected gems, deaths and available fuel telemetry.
