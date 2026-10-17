# Gamma operational notes

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
