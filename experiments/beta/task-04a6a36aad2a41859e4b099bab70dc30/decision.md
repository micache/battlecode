# Bounded objective routing

Hypothesis: reusing terrain routes and amortizing global objective ranking in the
previous farming policy improves matched wins/submitted gems over trusted starter
9e804e3e, and reduces fuel suspensions relative to measured cc05fd9d. No matched
win gain, lower submissions, or unchanged/increased suspensions falsifies it.

Evidence: cc05fd9d / c6bdbe58, evaluation 47319140: development 214W/156L,
mean 3.619 own suspensions. 00ambush/B 2b2c02f: 947:1011 submissions,
21 own suspensions, no faults. This supports wasted-turn investigation; it does
not establish that fuel explains every loss. 00collision/A 69d69c76: 505:1013,
26 deaths and zero own suspensions; combat remains a separate limitation.

Alternatives considered: a shared rally protocol addresses monster-only stalls
but not expensive work on every turn; combat avoidance addresses collision but
not broad navigation costs. Choose bounded reusable planning, preserving the
previous candidate's coherent farm/capture/build/bank systems as an explicit
transfer from our own evaluated source, rather than repeating its experiment.
Frozen boss 4feab379 reuses distance work and retargets periodically. Transfer
that principle, retaining this lane's private knowledge and conservative risk.

Implementation plan:
1. Reuse own c6bdbe58 foundation helpers/roster, preserving accepted Git source.
2. Cache static travel ranking for six turns / six tiles, while checking current
   target state, occupants, health and action legality each turn. A committed
   target gets a single-candidate fast path; global scans are fuel-gated.
3. Reuse an occupancy-aware route to unchanged goal masks. Filter actual steps
   using fresh occupancy. A blocked descending route gets a fuel-gated rebuild
   with current blockers; no cached state authorizes an action. A legal local
   repair prototype regressed smoke throughput and was replaced before handoff.
4. Compile policy boundary regressions with bot-check; inspect exact-source
   build/smoke report, record uncertainty and hand off for matched evaluation.

Risks: six-turn ranking can miss a new opportunity; static routes can need local
repair around camps/units. Smoke cannot establish dense-map fuel or win gain.
No changes to fuel/settings/opponents, no shared-memory writes, no agents.
