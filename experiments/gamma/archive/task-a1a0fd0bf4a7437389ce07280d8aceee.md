# Gamma operational notes

## task-a1a0fd0bf4a7437389ce07280d8aceee — Varg opening draft

- Playbook E. Hypothesis: deliberately drafting Varg first gives the existing
  basic-attack policy a guaranteed splash attacker, improving grouped-camp
  clearing and increasing collected and submitted gems versus accepted source.
- Falsifiable policy prediction: first legal pick is Varg; later picks retain the
  existing random, nonduplicate selection. Each draft turn consumes one RNG draw
  as before, writes the same draft message and deliberately submits one pick.
  All map-dependent 3–5-pick drafts remain legal. Gameplay is unchanged.
- Objective prediction: matched mean collected and submitted gems must increase
  without new bot faults to support the mechanism; actual wins govern promotion.
  No improvement is claimed from source or smoke checks alone.
- Identity: task/entry match user; branch bot/gamma, HEAD/input
  c5c3f4d0e5d5a8b3f9a05ae29643008d6c60e83a. All six edit-start files match
  accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d and trusted hashes.
  Base 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  Initial dirty bot.cpp is the trusted accepted restore. Accepted Git/snapshot
  preserve the base. Latest candidate evaluated; no unfinished/pending candidate.
- Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Documentation unchanged per handoff. Compact
  reference, Playbook E and narrow roster/draft SDK sections consulted.
- Development context: evaluation
  322271ef54566a308ed0a314061debfb504f4872b7353c8394aaf57e78cdc1ee,
  INCONCLUSIVE / provisional-three-map-wiring, 8W/16L, matched delta 1/6,
  zero fault/missing/unknown-reliability matches. It evaluates HEAD above,
  source 44e3b60c784fbfa3466e5a3e580c089a9b460c7eaf638d9c7056d9e19b67c48c,
  not the accepted edit-start. Self-play pending counts are separate evidence.
- Two completed collision losses from that evaluated source, with no Varg picks:
  A b020dfa9636c4ff425032ef0dc0ed9259ea89b2b6fe4c3708f2bf143c1c28295:
  draft [Ryth, Marcella, Prism], round 870, 418 collected / 264 submitted,
  opponent 1012 submitted, both sides zero faults.
  B e5196c5fa551501a9e525d3db4e4094a50a285ae2692482c5701d2973334a029:
  draft [Cassi & Issac, Tavi, Prism], round 1047, 506 collected / 286 submitted,
  opponent 1034 submitted, both sides zero faults.
  Complete final exports, byte lengths verified, saved in varg-draft-evidence.json.
  These show economy losses and absent splash, not causality or stall frequency.
  Final engineVersion 0.0.1 differs from trusted CLI/SDK 2.1.6; unresolved.
- Source mechanism: accepted drafts randomly from all 11 choices and basic-only
  play makes at most one attack. GameRules.md Varg section specifies automatic
  Strength splash onto other enemies/camps within radius one, without hitting
  the primary twice. Installed header has draft Varg=9 / body Varg=10 and
  current_draft() returning completed picks. No damage formula recreated.
- This is the first draft-composition experiment in retained history; previous
  ability/shop/recall/banking changes are not combined. Gameplay remains accepted.
- Uncertainty: Varg may lose travel time as melee, splash needs clustered targets,
  replacing another pick may reduce total output, and random later compositions
  change when Varg is removed from their pool. Smoke cannot establish utility.
- Change: draft.cpp chooses Varg when completed ally picks are empty, otherwise
  selects the existing nonduplicate random fallback. The fallback RNG draw is
  still consumed on the first turn. No gameplay, state, memory layout, policy
  threshold, path search, abilities, item or fuel-setting changes.
- Regression: `python3 experiments/gamma/check_varg_draft.py`, PASSED, exit 0;
  varg-draft-source-check.json. Source isolation proves the unchanged available
  pool and checks all 9,032 legal histories up to the fifth pick with every
  fallback choice. Other five source files match accepted. This is a finite
  draft model/source check, not an engine draft fixture or fuel measurement.
  `git diff --check`, PASSED, exit 0.
- Trusted compilation/smoke:
  `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact checked source
  cf45a24a06fc9892ff1f777432b9dc90913169d58740bebac89385b657718f51.
  Report .agent/check-task-a1a0fd0bf4a7437389ce07280d8aceee.json;
  check:task-a1a0fd0bf4a7437389ce07280d8aceee:cf45a24a06fc9892ff1f777432b9dc90913169d58740bebac89385b657718f51.
  Smoke IDs 1b6c98c5c1d24797fa4b83f584beee9cc1a5903f1d5516d999c809ff4cc589ba
  and a9a93bc2feb7861abe6702c38d5eb3de9adb2a37437fefb8dfd6f7b84374d7f0.
  Completion, scores and fuel telemetry absent/unknown. No outcomes inferred.
  READY_FOR_EVAL means a checked candidate, not demonstrated improvement.
- Next: supervisor evaluates the checked cf45a24a source versus accepted on frozen
  development cases. If unsupported, inspect map-specific camp grouping before
  considering another composition. No worker publication, evaluation or agents.

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
