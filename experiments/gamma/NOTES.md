# Gamma operational notes

## task-5adc36237ef7478dbc56f4b20a760fb5 — live camp goals

- Identity: bot/gamma; HEAD/input 9c632dd4030be0ec09e840918cf9ea453653b6f7.
  All six edit-start source files match accepted commit
  1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d, base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  The initial dirty bot.cpp is the trusted accepted-source restore, not unfinished
  work. Accepted code remains preserved in Git and the trusted external snapshot.
  Recent published candidates have completed evaluations; none awaits evaluation.
  The old PAUSED infrastructure-only task reports source unchanged and no patch.
  Documentation manifest is unchanged; prior full review remains recorded below.
- Playbook C, farming-route clearing versus capture. Hypothesis: excluding known
  empty spawn tiles from visible alive groups' navigation goals prevents standing
  indefinitely on a killed member's tile while another member remains out of
  attack range, increasing collected and submitted gems without new faults.
  Falsifiable prediction: a current empty spawn tile is not a goal for an alive
  group; living and unseen member tiles remain goals. Cleared reward groups keep
  all capture tiles; respawning groups remain excluded. Matched development
  collected/submitted gems should rise; equal/lower totals do not support the
  strategic prediction. Tournament wins still determine promotion.
- Source reproduction: farm_camps unions all group spawn tiles, including cleared
  members of alive groups; move_towards_closest returns immediately when standing
  on any goal. A melee champion at the empty end of a three-member cardinal line,
  with the far survivor two tiles away, cannot attack it and never approaches.
  This is a source-derived reproducible state, not an observed replay trace.
- Development context: collision/A losses
  719b261369cbe24fdba443e9f8e08820a1ea18e365565d67d0db46af7eee8578
  (round 1021, 352 vs 1012 tribute) and
  7d946f6572419308162551e024461f8ef0ee2ad7fa6755fa53d2c7f323cd8681
  (round 1676, 924 vs 1012 tribute), both zero faults. Both evaluate commit
  9c632dd4030be0ec09e840918cf9ea453653b6f7, source
  ed64236caac6ed68611f7044742fe7b31f563c56a10c9e523793fd94315413df,
  not this accepted edit-start. Complete final.json slices are saved in
  camp-goals-evidence.json. These show the economy gap, not this stall's frequency
  or cause. Evaluation 0bda0ce76d13bef869cecac6b1ea77e8bb4f92992240af6d80a4947440a29657
  is INCONCLUSIVE / provisional-three-map-wiring, 14W/10L, no faults/missing/unknown.
- Patch: query group state only after spawn visibility, omit respawning
  groups, filter alive groups to visible camp occupancy plus unseen spawn tiles.
  Preserve reward capture goals, hidden-group exploration and all other policies.
  No additional path search, shared memory, abilities, thresholds or fuel override.
- Validation: `python3 experiments/gamma/check_camp_goals.py`, exit 0,
  camp-goals-source-check.json. Exact accepted-source comparison confirms only
  the live-group goal block changes; other five source files are unchanged.
  Finite-set fixtures reproduce the old three-member-line stop and check living,
  unseen, reward, respawn and fully hidden goals; no SDK/engine simulation claimed.
  `git diff --check` passed, exit 0, recorded in the same report.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Candidate source
  f81809bac3396a11e5b2c612862f3d0430f2d0bb1f6ea33d212239291f54350c.
  Report: .agent/check-task-5adc36237ef7478dbc56f4b20a760fb5.json;
  reference check:task-5adc36237ef7478dbc56f4b20a760fb5:f81809bac3396a11e5b2c612862f3d0430f2d0bb1f6ea33d212239291f54350c.
  Wrapper supplied two smoke match IDs; no score, completion or fuel headroom
  inferred from these IDs. READY_FOR_EVAL, no measured strategic gain.
- Uncertainty: occurrence in these matches and strategic gain remain unmeasured.
  Final exports say engineVersion 0.0.1 versus trusted CLI/SDK 2.1.6, as previously
  recorded; no runtime parity claim. Separate organizers' AGENTS.md is unavailable.
- Next: supervisor evaluates exact checked source against accepted on frozen
  development cases. If the goal fix does not improve farming, collect bounded
  decision telemetry before trying another navigation policy. No worker
  tournament, publication, submission or evaluation waiting.

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
