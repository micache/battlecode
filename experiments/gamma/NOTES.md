# Gamma operational notes

## task-53dae71709bd49f58e9741404bfa9d54 — retreat before recall

- Identity: bot/gamma; HEAD/input 458bca7f7d892178c2defffbede7305af4d2a0b7;
  accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d, source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  All six edit-start files match accepted Git blobs and entry.json. The initial
  bot.cpp diff is the trusted accepted-source restore, not unfinished work.
  Accepted source remains preserved in Git and the trusted external snapshot.
  Recent published candidates have completed evaluations. Old PAUSED task has an
  unchanged-source infrastructure finding; no candidate awaits evaluation.
  Engine/SDK 2.1.6; suite historical-panels-v1; documentation unchanged.
- Playbook C, recall/recovery cost in the farming/banking route.
- Hypothesis: stationary low-health recall attempts can be interrupted repeatedly
  by incoming damage. Taking one spawnward step before each initiation makes
  retreat progress during such interruptions, reducing deaths and increasing
  submitted gems relative to the accepted policy on matched development cases.
- Falsifiable prediction: each actionable, low-health turn away from spawn attempts
  one existing legal spawnward movement before recall; after arrival it returns
  for spawn healing without starting recall. Existing channels remain untouched.
  If matched deaths do not decrease and submitted gems do not increase, the
  expected strategic gain is unsupported; wins still govern promotion.
- Source reproduction: the accepted low-health branch only calls recall and
  returns. With an awakened camp continually damaging the stationary champion,
  each interrupted initiation can repeat at the same position until death.
  This is a source/rules-derived scenario, not a traced event in the loss games.
  GameRules.md lines 270-274, 371-375: damage cancels recall, five owner turn-end
  ticks normally required; spawn arrival/healing timing also matters.
- Development context: evaluation
  2410874ef8c9177f24dcb39fe5a263a4cabc3f9a03a0f1b8949d7f9b8a3dbeb2
  is INCONCLUSIVE / provisional-three-map-wiring, 7W/17L, zero faults/missing/
  unknown reliability. Its source f81809bac3396a11e5b2c612862f3d0430f2d0bb1f6ea33d212239291f54350c
  at commit 458bca7f7d892178c2defffbede7305af4d2a0b7 differs from edit-start.
  Collision B loss 196ee225e7733f3aecb9bb5ae6624c50f383b0aeb459c8402bcb976abcf90c8f:
  36 deaths, 814 vs 1012 tribute, round 1448, zero faults.
  Collision A loss 8e661a794eb436adc3fdd40c92c055fb8f2ec5195c6ccff5dce217313b49a27b:
  15 deaths, 352 vs 1012 tribute, round 1021, zero faults.
  Complete final statistics saved in recall-step-evidence.json. These show losses
  and deaths, not the occurrence/frequency of interrupted recalls.
- Change: reuse move_towards_closest with allied spawn goals before low-health
  recall, then re-read position and skip recall if already on spawn. One movement
  attempt; failed/unavailable movement falls through to the existing recall.
  No new persistent state, thresholds, combat, build, draft or farming policy.
  This is distinct from the earlier spawn-wait experiment (439fcfcd..., evaluated
  INCONCLUSIVE) which waited after arrival but never retreated before recall.
- Validation: `python3 experiments/gamma/check_recall_step.py`, PASSED, exit 0;
  recall-step-source-check.json. Detects the accepted stationary initiation,
  requires one move before recall with fresh spawn-position guard, verifies all
  other code against accepted source, and preserves channel guards and dispatcher
  yield. Source invariant only; no engine behavior inferred. `git diff --check`
  PASSED, exit 0.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact candidate source
  3ddcabd550a7198b7553379a78a11ce62ece141f30dbbb772b36ef8257d2f769.
  Report: .agent/check-task-53dae71709bd49f58e9741404bfa9d54.json;
  reference check:task-53dae71709bd49f58e9741404bfa9d54:3ddcabd550a7198b7553379a78a11ce62ece141f30dbbb772b36ef8257d2f769.
  Wrapper supplied two smoke match IDs; no scores, completion or fuel headroom
  inferred from IDs alone. READY_FOR_EVAL; no measured strategic gain.
- Uncertainty: retreat can approach other threats, be blocked, or fail to escape
  before death; moving before a safe recall may cost fuel without benefit. The
  accepted start-on-spawn healing omission is unchanged. No per-turn trace or
  measured strength improvement. Final exports say engineVersion 0.0.1 versus
  trusted 2.1.6; runtime parity not claimed. Organizer AGENTS.md remains absent.
- Next: supervisor evaluates the exact checked candidate against accepted source
  on frozen development cases; if unsupported, collect bounded health/position/
  recall telemetry before another recovery-policy change.

## Bootstrap documentation review (2026-10-17)

Read the complete supplied GameRules.md, BotAPIPython.md, BOT_REFERENCE.md and
matching installed C++ cambc.h/imports.h; also RESEARCH.md and playbooks A/C.
Supplied documentation and header hashes match the trusted handoff:

| Source | SHA-256 |
| --- | --- |
| GameRules.md | `1c7fcf111d95b4734070f8f676cd50a48154feb0673de73a31c79845afa34732` |
| BotAPIPython.md | `3013fde86080e89ebf109357d4b8ca913babcb4592be542d92df0fadd542772f` |
| BOT_REFERENCE.md | `7d483da98c0360a9c9b186f46f9aa4408539c7c4be96682791f30b9d65c3829f` |
| C++ cambc.h (2.1.6) | `90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d` |

Reviewed profile: 1,000 tributed gems wins; at 2,000 rounds use tribute, lifetime
earned gold, champion kills, then B. SDK settings are engine-loaded, not evidence
that every executed suite uses handbook defaults. Draft has 3–5 picks; Cassi/Issac
have two bodies. Live memory is 8 team bytes; draft memory 1,024. Visibility gates
live state. Captures require uncontested occupancy; channels resolve at owner
turn start after their zero timer. Damage interrupts recall, not tribute/teleport.
Normal C++ fuel is 100k; exhaustion suspends execution. No fuel override added.
The separate organizers' AGENTS.md remains unavailable. Export example defects,
teleport-wall, monster-sleep and generic camp-range wording remain unresolved as
documented in BOT_REFERENCE.md; this experiment does not depend on those disputes.
