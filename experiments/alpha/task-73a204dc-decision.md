# One candidate: observed live-camp pursuit
Task task-73a204dcf7c2439ba03fc9f074bb101f, alpha.
Edit base 5f73d078 / ba646c6e; input HEAD 22dd72af / 64b2bce6 is a different source.

Hypothesis: Replacing freshly observed alive-group empty spawn goals with free
approach tiles to visible living members increases matched development wins and
collection over ba646c6e. Unchanged/lower win rate falsifies the hypothesis.

Mechanism: farm_camps first tries an in-range attack, then routes to the union of
static spawn tiles. move_towards_closest returns immediately if already on a goal.
After partial clearing or monster movement this can idle on a dead member's spawn.
This is an unmeasured source/rules deduction, not a proven cause of named losses.
Fresh reward groups retain all capture tiles; hidden/stale groups remain explorations.
Only cull when a living member of that group is positively observed and the bounded
live-target scan completed. No guessed hidden health/positions or persistent live cache.

Alternatives: broad group-value/commitment plus melee composition had prior gains
but map regressions and is not repeated. Previous capture deference and focus-fire
findings remain negative. This candidate repairs goal progress without changing
combat ordering, roster/build, banking, capture priority or ally deference.
Frozen boss ea15ef0f / f4b4f65e uses explicit live-group combat then capture and
value/risk routes; beta 7cab9b0f / fd5e2554 uses group/economy penalties. Transfer
only the compatible distinction between live pursuit and reward occupancy.

Risk: extra geometry/vision work; approach tiles may select a different group;
range-edge positioning may trade safety for clear speed. Unknown/hidden remnants
retain fallback static goals and can still stall. No improvement claim before evaluation.
Checks: compile-time synthetic cluster masks for partial clearing, reward retention,
unknown/stale retention and unrelated-group isolation; trusted bot-check and smoke.
Supervisor compares exact checked source with edit base and protected champion on
matched maps, sides, opponents; inspect collection/tribute and faults/suspensions.
