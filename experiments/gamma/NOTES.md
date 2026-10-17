# Gamma operational notes

## task-804d38a081924ff980942fe625d276d1 — attack resets

- Identity: branch `bot/gamma`, input HEAD
  `be3946bb49293a4dd646c243717a6a8bf7502204`; all six edit-start files match
  accepted `1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d`, source
  `9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`.
  Accepted code remains in Git and the trusted accepted snapshot. Initial dirty
  bot.cpp is the supervisor's accepted-source restoration, not unfinished work.
- Prior spawn-recovery candidate was evaluated: evaluation
  `5dc9194a4d7f6c82e015731b478722e72ee5429d5757b29f76dd602698bd2943`,
  INCONCLUSIVE, 27W/27L, zero recorded faults, full-nine-map coverage. No candidate
  awaits evaluation. This experiment starts from accepted code, not that candidate.
- Playbook D. Hypothesis: unused attack-reset abilities waste safe follow-up
  damage, prolong camp clears and fights, and delay gem conversion. Spending one
  ready reset after a basic attack on a surviving target should improve tribute.
- Falsifiable prediction: when a visible target survives an in-range basic and
  a self-targeted reset is ready, attempt one reset and take a legal second basic.
  Never cast on a killed/hidden target; at most one cast and two basics per helper.
  In matched development games versus accepted source, expect higher mean
  submitted gems with no new bot faults. Equal/lower tribute does not support
  the predicted objective gain; win rate remains the promotion criterion.
- Evidence: two completed collision/B losses for the PRIOR candidate/source
  `439fcfcda990dec5af8bda61db4076330daf5725f267fc75f6a2a71faf55bb97`:
  `0c4dfc600b817143ab95be0c00a632821a34e9b91873ad7ec26aa4e79ac1bae8`
  (round 1438, 858 submitted, 36 body deaths), and
  `ca90f18339461552e38df68f2aab898148c28f068cbabe6500fc288810b58ee4`
  (round 1158, 528 submitted, 31 body deaths). Both record zero bot faults.
  Final slices and candidate-only metrics: `attack-reset-evidence.json`.
  Linked Cassi/Issac deaths are counted per body here, not inferred team kills.
  These losses motivate the work; they do not prove unused resets caused them.
- Source mechanism: accepted attack helper returns after one basic; no ability
  casts exist. Handbook attack economy and reset sections establish self-targeted,
  walk-compatible resets. Matching SDK: `is_ready()` checks cooldown and live
  can_cast; `is_attack_reset()` uses cached metadata; `use()` casts untargeted.
  The compact docs are unchanged, so no full rules/API/SDK reread was needed.
- Change: extend only the existing champion/camp attack helper. Skip killed or
  hidden targets, select a ready self-targeted reset in slot order, cast once,
  revalidate allowance/visibility/health/range, and attack once more. No new
  persistent state, loops over targets, drafting, navigation or channel changes.
- Source check: `python3 experiments/gamma/check_attack_reset.py`, exit 0;
  `attack-reset-source-check.json`. Checks visibility-before-live-state ordering,
  post-cast legality, finite actions and official yield. Source invariants only,
  not an engine combat fixture. `git diff --check` passed.
- First trusted build failed, exit 1, because `ability_slots` is private; corrected
  the loop to use public `abilities()`. Failed source
  `fe16248771ad422843b55421df16fcba56943c1f6502fb6d1b80358cfc3d4795`;
  preserved report `attack-reset-check-initial.json`. Source invariants and
  whitespace check pass again after the correction.
- Trusted recheck: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact candidate source
  `fa3daecd898c0a5b98a4028f5368b4507e5db55bd9a7900c752a7769e1f480c7`.
  Report `.agent/check-task-804d38a081924ff980942fe625d276d1.json`;
  reference `check:task-804d38a081924ff980942fe625d276d1:fa3daecd898c0a5b98a4028f5368b4507e5db55bd9a7900c752a7769e1f480c7`.
  Two smoke match IDs supplied; no scores, completion or fuel telemetry inferred.
  READY_FOR_EVAL; no measured strategic improvement or worker-run tournament.
- Uncertainty: no per-turn ability/fuel trace; conserving resets for another
  target might be better. Final JSON's internal engineVersion is `0.0.1`, recorded
  verbatim, while the trusted task pins CLI/SDK 2.1.6. No runtime-version inference.
  Next: supervisor evaluates exact source versus accepted on frozen development
  cases; if unsupported, inspect objective delay before adding more ability types.

## task-7e4eb7d70e1d48658283dd9ac19bfb0a — spawn recovery

- Base: accepted/input commit `1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d`,
  source `9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`.
  Branch and all six source file hashes match the trusted handoff. Accepted code
  remains in Git and the task's accepted snapshot, outside this edit transaction.
- Prior task `task-f17bcd1d3dad4df8a50a2eaef40fb82d`: inspected its exact notes,
  final result and empty checkpoint patch. It failed before task reads; the trusted
  infrastructure finding confirms unchanged source. No candidate awaits evaluation.
- Playbook C, recovery cost in the farming/banking route.
- Hypothesis: leaving spawn injured after recall wastes recovery and encourages
  short low-health excursions or repeated recalls. Waiting on spawn while injured
  should reduce champion deaths and increase submitted gems on the frozen loss cases.
- Falsifiable prediction: an actionable, injured champion on allied spawn shops,
  yields without moving, and resumes the existing policy once fully healed.
  Development comparison should lower mean deaths below the accepted 28.0 and
  raise mean submitted gems above 714.67 over the same six cases; otherwise the
  expected strategic gain is unsupported. No measured improvement yet.
- Evidence: evaluation `f49c7fcaa2a555312128aa5dc806f4c9737d51fc9a1975e2bf19afc0177a958f`
  evaluated the base source: 3 wins / 3 losses, zero recorded bot faults.
  Collision B `be7a20ffb7ecec8faa5301faa76682357f1bcdc5098eb827d37caf47afed7c13`:
  36 deaths, 814 submitted gems, round 1448. Corners B
  `aab197827373931960687193e6155be9c43ae29f2d7ee7a902b891d16ce81052`:
  16 deaths, 110 submitted gems, round 522. Both use the base revision above.
  These motivate recovery work but do not establish the cause of those deaths.
  Bounded collision stdout contains shared-round logs, not health/position traces.
- Source mechanism: the accepted spawn branch only shopped, then proceeded to
  combat/banking/farming immediately. GameRules.md, Death/recall & recovery, says
  recall arrives at turn start and healing needs spawn occupancy through turn end.
- Change: after shopping on spawn, return while health is below maximum. The
  existing dispatcher then calls official end_turn(). No persistent state needed.
  Existing early returns preserve ongoing channels and handle dead/stunned turns.
- Source regression: `python3 experiments/gamma/check_spawn_recovery.py`, exit 0;
  report `experiments/gamma/spawn-recovery-source-check.json`. It reproduces the
  accepted source's missing guard, verifies the candidate guard precedes tactical
  actions, and checks the dispatcher retains official yield. This is a source
  invariant, not a runtime recall/healing fixture. `git diff --check` passed.
- Trusted validation: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`
  passed, exit 0. Exact candidate source:
  `439fcfcda990dec5af8bda61db4076330daf5725f267fc75f6a2a71faf55bb97`.
  Report `.agent/check-task-7e4eb7d70e1d48658283dd9ac19bfb0a.json`;
  reference `check:task-7e4eb7d70e1d48658283dd9ac19bfb0a:439fcfcda990dec5af8bda61db4076330daf5725f267fc75f6a2a71faf55bb97`.
  Wrapper lists two smoke match IDs but supplies no scores, completion or fuel
  telemetry here; no such metrics inferred. No tournament evaluation run by this
  worker. READY_FOR_EVAL; supervisor owns comparison, publication and promotion.
- Uncertainty: no available per-turn trace proves recall churn in these matches;
  extra recovery turns may delay a tribute or block an ally's spawn. Interrupted
  recalls and unsafe recall initiation are unchanged. Next idea, only after this
  evaluation: diagnose recall interruption if deaths remain high.

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
