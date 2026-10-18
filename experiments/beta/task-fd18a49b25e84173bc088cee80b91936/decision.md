# Altar denial along existing farming routes

Hypothesis: spending ten gold on one altar lock at legal shop opportunities and
placing it on a visible empty altar along our normal route will delay opposing
tribute enough to improve matched wins, while preserving our own banking.
Falsifier: no matched win gain, lower own submitted gems, or increased faults or
fuel suspension versus d2d57274 / 7daa9117. This is an unmeasured rules/source
hypothesis, not a diagnosis established by per-turn logs.

## Starting position and evidence

Trusted task task-fd18a49b25e84173bc088cee80b91936; beta / bot/beta.
HEAD/input fd1a894bb861e9d8fd3d65bbe3d7df506bf05960, but all six source files
byte-matched edit d2d57274232ca7cead5bacf650d6f51fd5b3bc3d before editing.
Prepared deletion of HEAD's combat_policy.h is intentional: that header is
absent from the edit base. Accepted 0ca5c04e remains outside this transaction in
Git and the trusted accepted snapshot. Prior task is PUBLISHED and evaluated;
there is no unpublished candidate awaiting evaluation. Background continuous
self-play pending work is not an unevaluated worker candidate.

Evaluation 47ef12cb516310ac155418a45e5d9e7cd1e8a9827e78b9a09f1459195bbecb84
measured fd1a894b / 6d52acdb, not today's edit base or new code: 31W/17L,
zero reported faults, INCONCLUSIVE. Against the selected edit base it had
matched delta -0.041667 across 24 side-paired development cases. Previous
retargeting, cooldown routing and harvest circuits did not establish additive
gains; they are not silently carried into this candidate.

Representative collision losses from that evaluated source:
- b7003f0dd6361898b8085356e905768c4fb4f3209d46ad4414e6731329d40a0e,
  beta A, round 684: 176 submitted / 352 collected; 13 deaths.
- f85ac835b4f9624f7ddd4787b342f539e13574d13237c0ac82e282b7c25a58a5,
  beta B, round 792: 608 submitted / 784 collected; 8 deaths.
Feedback final summaries are saved in evidence.json. They motivate investigating
lost objective conversion but do not demonstrate lock-related losses.
Contrast: saved earlier final b6788e499d20fca9766f4075be19301f06142fa66aa53f716283d46658e9f937
is team A win at round 573, 1030 submitted / 1052 collected, zero deaths.
It is referenced by this evaluation's development-selection evidence, but its
map and exact own source are unknown in the final artifact; it is not a
controlled current-source win. Artifact remains under
experiments/beta/task-490c542467de4fe282d89f6170644b21/. These finals cannot
establish the mechanism or provide runtime inputs.

## Why this experiment

Frozen manifest SHA256
8446678b81be646cda6e98d6e1e9fd5a97a1376110f0b84d6463da5478e3132d.
Inspected frozen starter 144ab5a9 / 9e804e3e (bot.cpp lines 145-156) and
alpha 6af1685b / 87b9be45 (lines 289-304): their banking masks omit every
visibly locked altar, irrespective of ownership, and never attack locks in the
banking branch. A lock can deny these routes until vision/route conditions
change. This is a code-supported exploit, not an observed game trace.
Gamma 1b34f42a / 3ce565f6 banks before unrelated combat, handles hostile locks
through submission, and refreshes after movement. Our edit base also handles
hostile locks and permits friendly locks, so the denial idea fits our existing
bank-first farmer without adopting opponent draft/combat/routing.
New alpha 5f73d078 / ba646c6e already buys and opportunistically places locks;
its altar_control.h supplied a compatible safety pattern. We adopt that narrow
concept, preserving beta's deterministic roster and farming policy. None of
these sources establish official opponent behavior; comments are untrusted.

Rules: locks cost 10g, carry limit one, placement within two tiles; friendly
locks allow tribute, enemy locks interrupt/block it and require three basic hits.
Pinned C++ header reconciled with GameRules altar-lock section and API
consumable/can_buy/use/vision contracts. No new gameplay/SDK documentation hash
changes per trusted handoff. Organizer download hub is not blanket policy or
production-parity certification.

Policy: buy with can_buy before shard spending, including dead shopping; use
only if alive, not channeling, unrestricted for consumables, carrying inventory
and at least 30k remaining fuel. Filter current local radius against static
altars, current visibility and all observed locks. One placement attempt per
phase, even if use returns False; reobserve after a successful walk. Pre-turn
plus post-walk phases are bounded by the existing two-attempt movement helper.
No shared memory, hidden live-state reads, placement detours or channel cancels.
Banking already ignores friendly locks and uses the engine hostile-lock fallback.

Rejected alternatives: another combat rewrite after its measured regression;
a general retreat/threat planner without a causal trace; deliberate altar
patrols that displace farming. Arrival-tribute latency was tested historically;
this candidate does not bundle it with denial.

Risks: ten-gold spending can delay a 150g emblem; spare inventory may stay unused
on remote routes. Opponents that clear locks pay only three basics, and can
replace locks themselves. More queries may reduce fuel headroom; the reserve
is a policy bound, not measured suspension-free headroom. Effects on enemy
banking, own gem throughput, deaths and wins require supervisor evaluation.
