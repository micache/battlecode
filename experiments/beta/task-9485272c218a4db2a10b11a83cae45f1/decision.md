# Economic shopping returns

Bottleneck: the edit base only recalls for equipment when below 80% health,
with an empty bag and at least 150 gold. Healthy non-Tavi farmers can therefore
retain multiple permanent upgrades indefinitely. This is a source/rules
hypothesis, not a traced cause of a particular defeat.

Hypothesis: allow healthy, safe, empty-bag non-Tavi farmers to recall with at
least 300 gold when terrain distance back to the current location fits a bounded
absence budget. Converting these batches into equipment will improve submitted
gems and matched wins over 9f7ae1c8 / b4e969c7. Falsifier: no matched win gain,
lower submitted gems, or increased faults/fuel suspension. Lower unspent gold
alone is not success.

Evidence and limits:
- Latest evaluation be4e11d0 measures 70df708b / f3a34040, not our edit base:
  42W/6L, zero faults; matched development-base delta 0.0 across 24 pairs.
  Lanes/interlock were all wins in both versions, so unnecessary shopping can
  regress an already effective policy. Full identity/comparison: evidence.json.
- Latest corners loss 3c5583fc, A vs gamma 1b34f42a / 3ce565f6, round 408:
  704 submitted, 834 collected, three deaths, 540 gold unspent. Marcella alone
  held 420 gold after earning 740. Final statistics cannot show when it became
  spendable, whether a safe recall existed or whether extra items would win.
- Latest expanse loss 56b94c0b, B vs the same gamma, round 493: 858/928,
  no deaths or champion damage taken, only 210 gold unspent (Ryth 190).
  The saved edit-base expanse loss 39a7bc8f has identical final totals. This
  candidate may not affect that case; composition/rotation remain hypotheses.
- Historical contrasting win b6788e499d20fca9766f4075be19301f06142fa66aa53f716283d46658e9f937,
  A, round 573: 1030/1052, no deaths, 750 gold unspent. Map and exact own/opponent
  source unknown in the saved artifact; not controlled evidence for today's code.
  It shows that unspent gold need not prevent winning. Artifact remains in
  experiments/beta/task-490c542467de4fe282d89f6170644b21/.
- Self-play stays source-separated: edit base 19W/5L and detours 15W/9L across
  24 unique inputs each. Repeats are not independent evidence. No causal route
  or economic trace inferred from these records.

Frozen manifest c5cb5e9c7c1526a84a350ea6b371198cd86b24b6483dff6bc4851d8d76a0aed7:
gamma 1b34f42a / 3ce565f6 uses Varg/Vendetta/Marcella, safe empty-bag recalls
at 300 gold independent of health, reward/cost farming and legal lock clearing.
Its healthier field-to-shop policy fits our existing permanent Strength build.
Transfer only that economic idea; retain our composition, items, combat,
banking, routes and farming ranking. Shared source is not official-opponent
code or proof of runtime shopping. Other manifest entries retained unchanged.

Policy:
- Existing 150-gold injured shopping return remains, now with explicit movement
  restriction, off-spawn and reward-occupancy guards.
- Both shopping paths defer to banking, emergency recovery and an occupied
  reward-available group. Tavi never takes equipment-only returns.
- Healthy return requires >=300 gold, no visible exposure, >=45k planning fuel.
  Budget walking rounds = min(24, gold/15 - base recall ticks - 1), floored at 0.
  Thus 300 gold permits 14 walking rounds with the pinned five-tick recall.
- Geometric lower-bound rejection precedes one terrain-only distance field,
  capped at walking budget times actual base speed. Unreachable/over-budget
  locations do not trigger a trip. Require >=18k remaining fuel before recall.
- The healthy branch sets no recovery latch: if damage cancels its channel,
  next turn can reconsider economics instead of forcing a long walk home.
  Successful recall uses existing shopping and end-of-turn spawn healing.
- No live shared memory, hidden-state cache, extra movement/cast or new logs.

Risks: budget is a deterministic heuristic, not a measured payoff model.
Nearest spawn may not be the actual recall landing; units and future threats
are omitted from static distance. Capture guard protects an ongoing reward,
not a nearly cleared group. Returning late in the objective race can cost wins.
Hidden enemies or a moving camp can interrupt recall. The extra field has a
fuel gate and distance cap, not measured worst-case suspension-free headroom.

Alternatives rejected for this invocation: another banking threat planner after
zero matched gain; another combat-retarget rewrite after its earlier regression;
repeating the previously tested reward/cost scheduler. Expanding draft or a live
team reservation protocol would confound this economic mechanism. Revisit
rotation/composition separately if safe shopping does not improve actual wins.
