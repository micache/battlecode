# Current experiment: task-c2c7bf3ea00b414a866765a00628b958

## Identity and prior work
- Bot alpha, branch bot/alpha; engine/SDK 2.1.6; suite pilot-wiring-v1.
- Input HEAD: 4922166cd44fa0bc1291cf9ccd9b05125cfcb84a.
- Accepted commit: c0cebd720fcd55e2bbb51d57dd2c398889d4071e.
- Base source: 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry source matched accepted_snapshot/src exactly (diff -r exit 0).
  Initial tracked diff is the supervisor's accepted-source restoration, confirmed
  by arena/worker.py make_attempt; it is not an interrupted experiment.
- Prior candidate 65c8c92fcea5bb2a17bc9476695a4aaff8a9ee9d2a7666dc88ba4843ec27e4b7
  was evaluated INCONCLUSIVE, not pending. Its notes are archived in
  task-e1eebd52bd4149da9bd5a22bca914599.md; accepted snapshot remains untouched.

## Hypothesis (playbook C: objective, economy, banking)
Prioritizing banking over opportunistic enemy attacks while carrying gems will
remove combat-induced banking delays. Falsifiable invariant: after channel and
recovery handling, every carrier executes the banking branch before any enemy
attack selection. Expected evaluation effect: more submitted gems and fewer
unconverted bags; strategic improvement is unproven.

## Evidence and change
- Supplied evaluation 639e91c9e7c215e00382562c3362bbcafc029683ce06cae70ac3dbdc491d8abf
  evaluates the prior candidate, not this working source; six candidate games,
  zero reported bot faults, four wins, two losses, INCONCLUSIVE overall.
- Prior candidate collision B: match
  7f9a575ca7dcaab8d4ccabb77f368fbaea727bdfc7be9c70f1fef6ce689dd29c,
  submitted 858 vs 1012, deaths 36 vs 20.
- Prior candidate elkring A: match
  4ed66a84a804e708f235c3e490323f1c89a6cc1a8066ac237314c1277ecee5df,
  collected 612, submitted 504, carried 36; opponent submitted 1008.
- These aggregates motivate conversion work but do not prove combat caused losses.
  Bag loss and channel interruption metrics are unavailable.
- Accepted bot.cpp returned after any in-range enemy attack before checking bag.
  The same enemy can therefore repeatedly defer banking, including at an altar.
- Moved that existing enemy loop below the existing banking branch; updated bot.h
  priority comment. No thresholds, routing, draft, recall or shared-state changes.
- GameRules.md 217-223: only tribute scores; ordinary damage does not cancel it.
  Installed C++ cambc.h submit_gems returns void; existing call contract retained.
- Main dispatcher still yields via end_turn after return or exception.

## Validation and uncertainty
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
- PASSED, exit 0; candidate source:
  f3a7e2da713bbe6b7c03d3d99cbcc8301e45040386668fbdefc44da4e1e012da.
- Local report: .agent/check-task-c2c7bf3ea00b414a866765a00628b958.json.
- Trusted report reference (not opened directly):
  /srv/battlecode/checks/task-c2c7bf3ea00b414a866765a00628b958/f3a7e2da713bbe6b7c03d3d99cbcc8301e45040386668fbdefc44da4e1e012da/report.json.
- Wrapper returned smoke IDs 3f219304b791f4bdcf5a2a4d49edbcea093392bbb5e48d6dcb2da58962b680e0
  and 2245195074781d07ca5b6a23f7b4124f4012fa89b6fc43c2d840dded3e553899.
  No final metrics inspected; these IDs alone do not prove completed full games.
- git diff --check passed.
- Source inspection confirms the banking branch returns before enemy selection.
- No tournament evaluation, improvement claim, or independent repeated samples.
- Risk: refusing a useful defensive attack or kill may expose a carrier to death;
  low-health recall still precedes banking. Exact delay counts remain unknown.
- Next: supervisor evaluates this exact candidate against the accepted source;
  compare submitted gems and outcomes on both sides, then investigate traces.
- Separate organizers' AGENTS.md remains unavailable per RESEARCH.md.
