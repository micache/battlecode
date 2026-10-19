# One candidate: end-to-end gem-return routing

Hypothesis: after 150 gold of cash plus purchase-value equipment, giving gem
sources strict priority over gold-only groups and ranking by expected full
collection-to-tribute time will improve matched wins and submitted gems.
No win gain, lower submissions, or increased deaths/faults/fuel suspension
falsifies it. This mechanism is unmeasured on the new candidate.

Bottleneck: beta's additive distance/HP/reward score can repeatedly choose nearby
gold-only groups, especially with commitment priority. In the latest evaluated
72275bc2 recovery candidate, ambush A cfdfa2b7 ended 538:1008 submitted with no
own deaths, faults or suspension. Ryth earned 1504 gold and Marcella 1260, both
with zero collected gems. Ambush B 405a38f8 ended 696:1034, also zero own deaths;
Varg collected zero gems despite 1575 earned gold. Final statistics do not prove
exact routes. Source supports the gold-loop inference; recovery alone cannot
fix this death-free throughput loss. These are NOT evaluations of edit 6d66a77f
or today's source. Full match IDs/statistics and identity limits: evidence.json
and the saved summary slices. Opponent source revisions in these games unknown.
Contrasting aggregate successes: collision/corners/eight/swirl each 4W/0L per
side on 72275bc2. Individual win IDs unavailable. Preserve these in evaluation.

Chosen policy:
- Keep the original final scoring before 150 endowment, retaining startup income.
- Count cash and all four purchased shard/emblem lines, including Tavi spending.
- After bootstrap, gem groups have a strictly better tier both before shortlisting
  and during final selection. Gold remains fallback if no inspected gem candidate.
- Within that tier minimize (outbound Chebyshev distance + HP/(Strength*1.12)
  + six capture phases + nearest-altar lower-bound distance + ceil(gems/10)) / gems.
  Discount current commitment by 15%. Gold fallback uses gold*0.12 as value.
- Current commitment is refreshed first within its tier; occupied cleared groups
  keep capture regardless of tier. An existing gold target cannot outrank gems.
- Cache immutable yield, bank geometry and whole-group Monolith classification.
  Exclude live Monolith groups in objective mode because rate lacks damage risk;
  visible cleared rewards remain eligible. This avoids a new high-yield trap.
- Timestamp visible cooldowns; filter deadlines and route retries BEFORE the
  12-candidate shortlist. Deadlines expire and live state is then reobserved.
  Vacate captured spawn regions if no candidate remains. No shared-memory writes.
- Existing movement legality/retry/observation refresh, banking, recovery, combat,
  roster, shop build and intentional main-loop yield remain the edit-base policy.

Alternatives: last recovery routing has only +0.026786 matched development delta
and ambush regression; do not tune it again. A fixed +40 gold penalty after 300
capital was previously +0.044643 with regressions and no accepted advance. This
candidate changes shortlist tiers and full-trip rate, rather than increasing that
penalty. Prior full reachable scheduler gained +0.041667 but regressed interlock;
retain the existing native movement search rather than adding a full-map field.
Healthy shopping/bank detours and combat rewrite already lack supporting gains.

Frozen opponents: manifest f94b3422, six sources. Gamma ecbc8203/ff511c52 uses
Varg/Vendetta/Marcella/Ryth/Tavi; reachable reward/time routes, 0.12 gold value,
no live Monoliths, observed cooldowns, each-bag banking, core farming equipment,
health durability and shopping recalls. Adapt rate normalization and Monolith
safety, but keep beta's bounded shortlist and add bank-leg cost/strict gem tier.
Alpha 82a14a04/6e362fd7 has independent routing plus opportunistic locks and
bank-each-bag; beta 7cab9b0f/fd5e2554 supplies the prior additive-penalty contrast.
These are arena strategies, not evidence about private official opponents.

Risks: geometric distances can understate detours; hidden monsters use base HP.
The model omits ability cycles, retaliation, healing, contention, and altar locks.
Strict gems may skip valuable long-term income and concentrate allies. The 150
threshold and 1.12 clear multiplier are unmeasured policy parameters. Free reward
travel can still exceed estimate; 12 inspections and fuel cutoff can miss a
better group. Cooldown expiry is an observation estimate, not current truth.
New ranking/metadata cost and fuel headroom have not been measured in tournaments.
The endowment is not used as a scoring statistic or lifetime-earned-gold estimate.

Expected observable change: previously gold-only productive farmers collect and
submit gems; fewer zero-gem/high-gold champion finals, higher team submissions,
and more matched wins without extra deaths. Proxy gains alone do not establish
success. Supervisor compares final 4ba62e96 against trusted 6d66a77f on matched
maps/sides/opponents, protecting existing wins and using the full promotion gate.

Validation: final exact-source bot-check PASSED/0; compiled policy fixtures cover
bootstrap boundary, tiers, travel/clear/bank sensitivity, live/cleared Monoliths
and commitment. First a4b84b4d check also passed, then was superseded by Monolith
safety/commitment refresh/cached altar geometry changes. Both reports retained.
Own final smoke stdout slices are empty on both sides. Smoke success does not
establish completed competitive games, mechanism coverage, fuel headroom or gains.
