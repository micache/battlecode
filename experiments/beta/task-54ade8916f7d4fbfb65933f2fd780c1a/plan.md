# Bounded clear-and-capture action economy
Goal: turn available kill resets, melee movement and completed clears into earlier captures.
Evidence: edit base c9c933a2 has measured farming but poor gem conversion in supplied 00ambush losses. Its source returns immediately after fight(), even after a last kill. This source-grounded mechanism is not proven by aggregate scores.
Alternatives considered: changing gold weighting risks repeating rejected cash-cap experiments; periodic frontier reranking risks extra route churn and fuel. Keep both unchanged for this candidate.
Policy: at most six combat progress steps, one movement phase, fresh reward and target observations every phase, at least 30k fuel before another phase. Attempt capture after a final kill even at the action cap. Keep channels, existing draft/build/target ranking, visibility gates, movement and banking semantics.
Files: add SDK-independent harvest.h turn controller; use it in bot.cpp; add compile-time behavior fixtures in this experiment directory. No live shared memory.
Checks: fixtures fail on missing controller, then compile against actual controller; trusted bot-check final build/smoke; diff hygiene. Risks: extra calls may consume reserve, melee approach may expose units; no comparative evaluation here.
Steps:
- [x] Write and run behavior fixtures for kill-reset chains, post-move refresh, immediate capture, no retry on stalled actions, fuel cutoff and bounded nonterminating progress.
- [x] Implement controller and bind to current SDK combat/navigation using fresh observations.
- [x] Run fixtures, trusted bot-check and inspect saved diagnostics.
- [x] Update compact notes and return one result; no publication or evaluation polling.
