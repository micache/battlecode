# Sustainable farming sortie experiment

Identity: alpha, task-315eeea3b0ae4c8d84088c2b74fa0b33, edit 5f73d078 / ba646c6e.

Hypothesis: A deliberate melee-reset roster with kit-matched Jungle/Strength
purchases and completed recovery/reinvestment increases matched development win
rate over ba646c6e. Unchanged or lower win rate falsifies the prediction.
Mechanism diagnostics: tribute, collection, camp deaths, spent gold, healing and
fuel suspensions. These are source/rules deductions, not traced loss causes.

Decision: choose a focused economy/composition slice over either repeating the
entire later group-routing overhaul or retuning PvP disengagement. The later
2cb76e5d/a309a76d candidate gained +0.208108 against this base over 185 side pairs,
but collision fell .6 to .4 and fragment .9 to .6. Its 310W/90L full evaluation
is not a measurement of current source. Earlier disengagement/focus experiments
remain negative findings. Keep nearest-group routing, cooldown memory and combat
selection fixed, to preserve base advantages while isolating sustainable sorties.

Policy: Varg, Vendetta, Marcella, Ryth, Tavi (3–5 legal unique picks). One Jungle
emblem (Health on Ryth, Strength otherwise), then Power Strength. Shop on spawn,
while dead, and on legal Tavi field turns. Recall at <35% health and remain
committed to returning until full spawn healing. Empty-bag quiet resupply at
150+ gold and <80% health, excluding Tavi; no enemy or awake camp in personal
vision. No shared protocol, changed fuel or hidden-state query.

Implementation/check plan:
1. Compile-time scenarios for capped purchases and latched recovery.
2. Wire deterministic draft, staged shop and committed recovery into base loop.
3. Run bot-check at normal settings; inspect exact-source diagnostics and save.
4. Review diff, keep compact notes, return one candidate for supervisor evaluation.

Risk: melee opening can cluster workers; Health delays Ryth damage, resupply can
cost travel, nearest-group targeting and capture duplication remain limitations.
No full tournament, publication, agent delegation or promotion in this invocation.
