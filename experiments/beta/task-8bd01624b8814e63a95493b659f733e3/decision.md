# Bounded terrain-aware opportunity selection

Hypothesis: local terrain-distance ranking and periodic long-route retargeting will increase matched wins and tribute over c9c933a2 without new faults or fuel suspensions. Nonpositive win/tribute gain or new reliability failures falsifies it.

Evidence: latest 94c44565 (not edit base) evaluation 51ca17d1 had 240W/160L; development comparison to c9c933a2 only +0.008108. Zero own faults/suspensions, mean collection 630.63 and tribute 572.36. 00ambush/A c71597cc lost 555:1007 tribute with 625:1063 collection; b0f2c2b6 lost 793:942 despite 14:5 kills and 9990:5278 gold. Contrasting 00ambush/B cd4363ae lost 253:1010 with zero bag loss and 191 carried. Exact identities/metrics in evidence.json; opponent revision unknown. Aggregates motivate throughput work but do not prove routing caused these losses.

Source deduction: edit base ranks by Chebyshev anchor distance and retains any feasible target indefinitely. Frozen boss 4feab379 / ea15ef0f / f4b4f65e computes terrain distances, rejects unreachable objectives, reconsiders targets periodically and uses hysteresis. Adapt only terrain cost and retargeting; do not copy full-map scans, shared claims, roster, economy or combat.

Alternatives: item-aware gold weighting risks repeating prior strict gold restrictions; squad rally is valuable on monster-only maps but requires separate coordination. Choose route opportunity selection with a bounded 24-step terrain field and a 16-round target review. Unreached local tiles get a lower-bound cost, never a false unreachable verdict. Preserve normal movement's fresh occupancy checks.

Plan:
1. Add compile-time behavioral regressions for local route costs, stale estimates, target-review expiry and score preference for a nearby detour versus a reachable camp. Run red trusted check.
2. Implement private bounded terrain field cache and score integration in policy.h, bot.h and bot.cpp. Keep six live candidates, 32 static ranking candidates, current-target hysteresis and intentional yield. Target review changes ordering, never authorizes an action.
3. Run final bot-check, inspect exact-source compilation and both smoke outcomes. Record limitations and compact notes. No publication, agents or tournament polling.

Risks: extra field cost, churn at expiry, distant camps delayed by the local bound, and transient occupancy ignored during ranking. Field is advisory static terrain only; real routes still enforce current blockers. Tests cannot establish improved tournament strength.
