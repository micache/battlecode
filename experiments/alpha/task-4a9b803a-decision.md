# Tavi field reinvestment — one candidate

Task task-4a9b803aa850407e9f95fe4001ff478b; alpha.
Edit 1f5e71f3111c5a492a20f4aaf0bbd3bd0c6fff97 / dd7c6c99;
input b6350143 / aaa73e40 is the evaluated support trial, not this edit.

Hypothesis: Immediate kit-aware offensive Power purchases on Tavi's ordinary
field turns increase matched wins and tribute over the edit base. Nonpositive
matched win gain falsifies it. Spending, collection and Tavi deaths diagnose the
mechanism. This is an unmeasured rules/source deduction.

Evidence: latest evaluation adeb13b3...6800 has development-base delta 0 over
185 side pairs, full 263W/137L, no faults/missing/unknown. Development unspent gold
averages 1280.3162/team over 370 games. In completed 00ambush B loss
7a107cc7...1558, b6350143 / aaa73e40, Tavi ends with 509 gold, 237 collected and
one death; own tribute 789 versus 1013. This establishes unused gold, not the
turns on which field buys would have changed the result. Contrasting same-source
development stampede/starfish/pilgrimage each win 10/10; retain their ordinary
draft, routes, combat and banking. A loss has no causal counterfactual here.

Frozen manifest cd19ca2b...d59b and all six source sets verified. Boss
ea15ef0f / f4b4f65e shops with staged Jungle/Monster/Power, supports early,
selects fixed Vendetta/Varg/Ryth first, uses group claims and explicit capture,
and banks at 30/near an altar. Our change uses only the rule-supported remote
shop permission, retaining our own kit-aware Power allocation. No inference
about official opponents or hidden runtime state.
Frozen beta 7cab9b0f / fd5e2554 uses Varg/Tavi/Ryth first, purchases through
can_buy on every turn, and excludes Tavi from economic recall. Transfer only
that compatible no-trip field reinvestment; do not copy its item families,
fixed composition or risk-priced group/economy routing. Frozen alpha still
shops only on spawn; gamma adds dead/spawn shopping and economic recall.

Alternatives rejected: another support/draft/item-family package; economic
recall trips; repeated capture/routing/focus/dash experiments. Historical
ce64d208 tested field/death shopping plus 300-gold resupply on an older random
stat allocator and different engine context. Here no trips/death shopping change,
and field Health is excluded explicitly because it gives no immediate healing.

Implementation/check plan:
1. Add a regression contract for field eligibility after channel/death guards.
2. Extend the pure allocator with a default-on Health eligibility flag; compile
   semantic cases for disabled Health, completion bonuses and bounded purchases.
3. Run field shop only for a living, unchanneled remote-shop champion outside
   spawn, using existing fuel gates and SDK can_buy per bulk purchase.
4. Preserve spawn shopping, healing, all nonshop policy and official yielding;
   run the trusted bot-check on the exact final source and inspect its report.

Risks: offense-only field buying delays durable Health until spawn; early spending
can change fights/routes adversely; extra SDK work can consume fuel; random draft
may omit Tavi from smokes. No draft changes to force branch coverage, no claim
of improvement without supervisor evaluation.
