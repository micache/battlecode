# Selective completed Jungle investment

Goal: improve objective throughput while preserving the successful kit-aware Power allocator.
Hypothesis: Comparing a complete kit-aware Jungle bundle against the same-cost Power plan increases matched wins and collected gems over dd7c6c99. Nonpositive matched win gain falsifies the prediction.

Evidence: same-source ambush losses 740998dc (A) and c1483af5 (B): 22/12 own deaths, camp damage 65055/68880 versus champion damage 8540/900. These totals motivate mitigation but do not establish purchase causality. Prior random-stat partial Jungle trial lost 1/112 matched games on another base/engine. This uses current marginal kit scoring and requires immediate completion; no random stat lock or partial investment. Boss ea15ef0f and gamma f01d496c buy Jungle and other farming emblems; their full policies are not copied.

Alternatives: leave Power-only (preserves demonstrated gain but ignores mitigation); replay fixed Jungle-first (negative prior result); selective complete-bundle comparison (chosen). Do not add Monster, routing, recall or draft changes.

Plan:
1. Add a focused source contract that fails before integration; preserve prior notes.
2. Extend equipment_policy.h with a bounded three-stat bundle selector. Compare effective health times sustained damage squared after Jungle with the original Power planner for exactly the bundle cost. Use a conservative 80% camp-exposure assumption, so Jungle contributes 1/(1-.8*.3) to effective health. Require >5% model advantage. No passive stacking.
3. Snapshot inventory; recognize any Jungle stat emblem, determine missing shards from SDK combine count/cost, can_buy full bundle, refresh gold/inventory, then use unchanged Power allocator. At most one Jungle buy plus three Power buys.
4. Compile constexpr cases using bot-check, inspect complete smoke summaries/reliability. Run source contracts and diff check. Update compact notes.

Risks: workload/model and 80% camp exposure are assumptions. Instant bundle requirement may delay protection forever on frequent small shops. Jungle loses one stat point relative to Power. H*D^2 does not model burst/tempo/path contention. Extra shop work needs normal-fuel smoke validation.

Ruling: user-directed bounded worker workflow takes precedence over generic approval, worktree, commit and agent-review steps. Only owned paths change; no agents or publication.
