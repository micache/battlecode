# Gamma operational notes

## task-8b7a2f9424dc42e5adc6086e0634544a — useful power builds

- Identity verified: bot/gamma; HEAD/input b4c6815c3368a346fbe3cffd6d9dc8cfbba20fa2.
  All six source files match accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d;
  base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  Accepted source is preserved in Git and the trusted snapshot outside this edit.
  No candidate awaits evaluation; latest banking priority was INCONCLUSIVE,
  evaluation 8cb1fe12a6df7508e0d93a91aa99c1c5895a86d453417fcc8bd8021f0e35e2cf,
  8W/16L, provisional three-map coverage, zero faults/missing/unknown reliability.
  Its source df0f1c4aa044b72a668977305c5d9f7e2d70f0b6c22bdb1f9308ee823bbab6e3
  differs from this accepted edit-start. Older notes are archived by task ID.
- Playbook C, item value for the current action policy. Hypothesis: redirecting
  the Focus-only power build to Strength improves farming and submitted gems,
  because this policy uses basic attacks and never casts a Focus-scaled ability.
  Prediction: the old Focus choice buys Strength, the other two choices and RNG
  draw count stay identical; no Focus purchases occur. Matched development mean
  camp damage and submitted gems should rise with zero new faults. Equal/lower
  tribute does not support the strategic prediction; wins determine promotion.
- Observed failure: collision/B loss
  b6f042dc013f0e9c024e9eb7f6c2b3171f37678326572a3cbe0619be03c0eb33,
  round 1352, 660 vs 1012 submitted, zero bot faults. Champion 4 bought 36
  Power Focus shards (1080g), champion 5 bought 32 (960g); inventory slots 8/9
  identify Focus in the pinned C++ enum. They submitted 242/176 with 11/8 deaths.
  Earlier collision/A loss d27e7d44946f0f250584f0ff8d7af5d89596fbf63e8f4ab952be57ebac7bc241,
  round 1264, 660 vs 1034 submitted, zero faults, had no candidate Focus buyer:
  it is a control observation, not proof all losses share this cause.
  Both matches evaluate commit b4c6815c3368a346fbe3cffd6d9dc8cfbba20fa2,
  source df0f1c4aa044b72a668977305c5d9f7e2d70f0b6c22bdb1f9308ee823bbab6e3;
  neither evaluates this edit-start/candidate. Saved power-build-*-evidence.json
  came from complete final.json slices; no independent repeated games counted.
- Source/rules mechanism: accepted and evaluated policies contain no ability cast;
  GameRules.md lines 245-259 and 278-304 define Strength basic damage, Focus spell
  scaling, and Power's stat-only bonus. No passive converts these Focus purchases
  into basic damage or health. This is wasted spend under the current policy;
  final totals alone do not prove it caused the losses.
- Patch: replace only shop choice 1 (Focus) with Strength; keep random(3),
  choice 0 Strength, choice 2 Health, buying guards/counts and all turn logic.
  Effective deterministic policy weights: 2/3 Strength, 1/3 Health. No new search,
  thresholds, shared state, API calls, ability use or fuel settings.
- Source invariant: `python3 experiments/gamma/check_power_build.py`, exit 0;
  power-build-source-check.json. Reproduces accepted Focus choice, verifies only
  that choice changes, RNG/buy guards stay identical, other five files match
  accepted, and the policy still has no cast. Source check only, not a game.
  `git diff --check` passed, exit 0; saved in the same report.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Candidate source
  ed64236caac6ed68611f7044742fe7b31f563c56a10c9e523793fd94315413df.
  Report: .agent/check-task-8b7a2f9424dc42e5adc6086e0634544a.json;
  reference check:task-8b7a2f9424dc42e5adc6086e0634544a:ed64236caac6ed68611f7044742fe7b31f563c56a10c9e523793fd94315413df.
  Wrapper supplied two smoke match IDs; no scores/completion/fuel headroom
  inferred from those IDs. READY_FOR_EVAL, no measured strategic gain.
- Uncertainty: faster clearing can alter routes/encounters; stronger attacks do
  not guarantee survival or wins. Final exports label engineVersion 0.0.1 while
  the trusted CLI/SDK identity is 2.1.6; preserve this discrepancy without claiming
  runtime parity or changing infrastructure. Supervisor can reconcile metadata.
  Deferred locked-altar routing lacks a demonstrated instance in these matches.
- Next: supervisor evaluates exact checked source
  against accepted on frozen development cases. No worker tournament/publication.

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
