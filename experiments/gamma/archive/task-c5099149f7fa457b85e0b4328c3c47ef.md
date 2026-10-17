# Gamma operational notes

## task-c5099149f7fa457b85e0b4328c3c47ef — carrier banking priority

- Identity verified: `bot/gamma`, HEAD/input
  `524b799376d7de344bf6c12c3135149d116adfd8`; all six source files matched
  trusted accepted edit-start hashes before edits. Base source
  `9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`,
  accepted commit `1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d` remains in Git
  and the trusted accepted snapshot outside this edit transaction.
- No candidate awaits evaluation. Previous attack-reset experiment was REJECTED
  in `cadbbc35adcf7ff4481fcd593999336ca855f867bdd537ce08ec9c8c3de2f967`:
  28W/44L, matched delta -0.0277778, zero faults/missing/unknown reliability.
  Its source `fa3daecd898c0a5b98a4028f5368b4507e5db55bd9a7900c752a7769e1f480c7`
  is distinct from this edit-start. Spawn recovery was INCONCLUSIVE, 27W/27L.
  Older complete notes preserved under `archive/<task-id>.md`.
- Playbook C. Hypothesis: in-range enemy attacks starve carriers' banking turns;
  banking before optional combat should increase submitted gems without new bot
  faults. Source reproducer: an actionable carrier above the recall threshold,
  with a visible attackable enemy, always attacks/returns before the bank branch
  in accepted code. This affects melee too; ranged attacks also consume movement.
- Falsifiable prediction: such carriers enter the existing altar submission/route
  branch without attacking enemies, while empty-handed champions retain combat
  priority over farming. In matched frozen development cases against accepted
  source, expect higher mean submitted gems and no new bot faults. Equal/lower
  tribute does not support this prediction; actual win rate decides promotion.
- Motivation: completed collision/B loss
  `ca7e4b31883572c867b44da80416f729d61085b4de83bc85156dac899d9ed2df`, round
  1212, 770 collected / 528 submitted, 37 body deaths, zero bot faults; collision/A
  loss `247d9521604af60c6894232443c96ea5d684045d039221388cbe1fd1c99868a8`,
  round 1049, 616 collected / 550 submitted, 16 body deaths, zero bot faults.
  Both evaluate previous attack-reset commit/source above, NOT the accepted code
  now being edited. The second identical collision/B summary is not counted as
  independent evidence. Saved supplied metrics: `banking-priority-evidence.json`.
  These totals motivate conversion work; no trace proves the hypothesized cause.
- Change: move the existing enemy-attack loop after the complete carried-gem
  banking branch. Preserve low-health recall, ongoing-channel guards, bank route,
  lock handling, farming, legal attack checks and official dispatcher yield.
  No new state, thresholds, API calls or path searches. Update header priority comment.
- Source regression: `python3 experiments/gamma/check_banking_priority.py`, exit 0;
  `banking-priority-source-check.json`. Accepted code reproduces combat-before-bank;
  candidate satisfies carrier priority, bank-body preservation, channel guards,
  and official yield. Source invariants only, not an engine scenario. Whitespace
  check `git diff --check` also passed, exit 0.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact candidate source
  `df0f1c4aa044b72a668977305c5d9f7e2d70f0b6c22bdb1f9308ee823bbab6e3`.
  Report `.agent/check-task-c5099149f7fa457b85e0b4328c3c47ef.json`;
  reference `check:task-c5099149f7fa457b85e0b4328c3c47ef:df0f1c4aa044b72a668977305c5d9f7e2d70f0b6c22bdb1f9308ee823bbab6e3`.
  Two smoke match IDs supplied; no scores, game completion, or fuel telemetry
  inferred. READY_FOR_EVAL; no worker-run tournament or measured strategic gain.
- Uncertainty: no bag-loss, interruption or per-turn trace is available. Giving up
  an attack may let an enemy kill a carrier or block its approach; channels can
  still be interrupted by stun/death/locks. Known existing all-locked/blocked
  route behavior is unchanged. No claim of strategic improvement before evaluation.
- Next: supervisor evaluates this exact checked source versus accepted on frozen
  development cases. If unsupported, inspect blocked altar approaches before
  considering a separate route/fallback experiment.

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
