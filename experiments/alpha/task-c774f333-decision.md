# Kit-aware farming draft: one bounded candidate

Hypothesis: ranking legal draft picks by the existing kit-aware farming model,
including opening Power growth and linked twins, increases matched wins and
tributed gems over dd7c6c99; nonpositive matched win gain falsifies it.

Evidence: exploration task, unchanged SDK/docs. Latest 643bcf70 / 3a354ce7
had 275W/125L full evaluation and +0.03243243 development delta over this edit
base, not a measurement of today's source. Earlier kit-aware allocator on this
base improved development wins; random composition remains untouched since it.
Ambush B f559889f (later Jungle source) completed at round 1825: own tribute
859 vs 1021, camp damage 62696 vs 11692; own faults/suspensions zero. This
supports mortality/throughput concerns, not a causal draft diagnosis. Contrasting
latest-source pilgrimage/stampede/starfish aggregate wins each 10/10. Do not
pool sources or infer target actions from summaries.

Alternatives considered: per-turn Vendetta chains rejected because cooldown
resets do not restore cast allowance; aggro control deferred because handbook
individual/group wake wording conflicts; repeated routing/focus/banking trials
have negative evidence. Chosen: draft economics, not another item-family trial.
Earlier fixed melee/random-stat packages failed; this differs by reusing actual
kit/growth allocation that subsequently improved the base. This is still an
unmeasured rules/source prediction and could repeat the roster regression.

Design: share the current shop model construction without changing its formulas.
Score every released pick as equal-weight H*D^2 at base and after five optimally
allocated Power shards. Sum body values, halve linked twins for two death
exposures (policy assumption); treat them as one pick and two designs. Include
Heart of Ruin, but price only abilities current combat uses. Do not price dash,
bonus income, mobility, support healing or missing-health damage. Deterministic
seeded tie order; exclude already selected picks; respect map-dependent team
size. Cache twelve immutable scores on the first draft turn. Keep hello-world
draft memory for existing play logging; no new shared protocol.

Plan: write a source-contract regression and see missing-policy failure; extract
equipment model; add pure opening-score/legal-selection functions and compile-time
edge cases; integrate draft; run focused contract and trusted bot-check; inspect
completed smoke reliability; record checked source/report and compact notes.
Only bots/alpha and experiments/alpha are edited. No agents/commit/publication.

Risks: static scores may lose range/mobility/composition diversity, overprice
stationary splash, shields and late investments, or undervalue support/economy.
No map/opponent-specific tuning. Strength must be measured by supervisor.
