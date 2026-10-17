# Gamma operational notes

## task-da79c8f66fb941c29528f7a27187478f — one Jungle opening emblem

- Identity verified: bot/gamma; HEAD/input
  1592c7696a7e1a7551c6fe5a78d6e2f91aca4a1d. All six source files matched
  accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d and trusted file
  hashes before edits. Base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  Initial dirty bot.cpp was the trusted restore, not unfinished work. Accepted
  source remains in Git and the trusted external snapshot. Latest published
  candidate has a completed evaluation; none awaits evaluation.
- Engine/SDK 2.1.6; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Documentation/header hashes unchanged and verified.
- Playbook C, farming/recovery cost and item value. Hypothesis: buying one Jungle
  emblem before resuming Power purchases in the same chosen stat should reduce
  camp damage and deaths, increasing submitted gems versus accepted source.
  Jungle trades one shard of stat growth for 30% less camp damage at five shards.
  Cap Jungle purchases at one emblem because duplicate family passives do not
  stack. Keep existing stat selection, RNG draws and all turn priorities fixed.
- Falsifiable prediction: before owning the selected Jungle emblem, buy at most
  the missing shards toward its SDK combine count; after completion, buy Power
  with remaining gold that same turn. Preserve partial progress across visits
  via actual inventory. Never buy a second Jungle emblem. On matched development
  cases expect lower mean monsterDamageTaken/deaths and higher submitted gems;
  equal/lower tribute does not support the strategic benefit. Wins govern
  promotion. No gain measured by this worker.
- Mechanism references: GameRules.md 278-304, BOT_REFERENCE.md section 4;
  C++ cambc.h item_type Jungle/Power metadata and item_count/can_buy/buy contracts.
  Passive begins only at emblem completion. No hidden-unit reads or shared state.
- Previous recall gate evaluation
  40f171343d76128d49fd4fd610af8cb651ade0bde55444b3f2640c9e2ed6a6f4:
  INCONCLUSIVE, provisional-three-map-wiring, 13W/11L, delta 0.375,
  zero faults/missing/unknown reliability. Evaluated commit is HEAD above, source
  f89c3f951116f0908f9170c310996bde0e8077ce892748efc11d8cc1ed12400c;
  it differs from accepted edit-start. Collision/A development losses:
  40dc88184b6f0ecbd4ed7fa801f376ef35a8bb01f7fc7e55b3ca2f065ec02eca,
  round 1219, 836 vs 1012 tribute, six deaths; and
  dbb0a72d52fa4f8cd3a127276cb023f0a3580c17db507f716e76d75b62ae52b4,
  round 1124, 762 vs 1034 tribute, four deaths. Both zero faults.
  Team A took 12,560 and 16,620 cumulative monster damage respectively, and
  spent 3,990 / 3,720 gold. This motivates mitigation; totals do not locate
  interruptions or prove a cause of death. Complete bounded final.json slices
  saved in jungle-opening-evidence.json. Both exports say engineVersion 0.0.1
  while trusted CLI/SDK is 2.1.6; metadata discrepancy remains unresolved.
- Prior spawn recovery and Power-stat experiments already exist; this tests a new
  item-family opening rather than repeating them. No other past patch imported.
- Focused validation: `python3 experiments/gamma/check_jungle_opening.py`,
  PASSED, exit 0; jungle-opening-source-check.json. Verifies exact shop-only
  bot.cpp patch, unchanged draft/RNG/dispatcher, stat-preserving inventory cap,
  and 45,015 finite arithmetic cases. Source/arithmetic checks only, not engine
  simulation. `git diff --check` PASSED, exit 0.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0; source
  2ed65cd1577a4731dc4706f184e838cd899e5550af669036ebcd363b20f1b10e.
  Report: .agent/check-task-da79c8f66fb941c29528f7a27187478f.json;
  reference check:task-da79c8f66fb941c29528f7a27187478f:2ed65cd1577a4731dc4706f184e838cd899e5550af669036ebcd363b20f1b10e.
  Two smoke match IDs supplied; completion, scores and fuel headroom were not
  supplied and are unknown. READY_FOR_EVAL means a valid checked candidate,
  not a measured improvement.
- Uncertainty: one fewer shard of stat growth can slow clearing or weaken champion
  fights. Camp mitigation cannot prevent enemy damage/stuns, and the existing
  spawn-healing omission/recall behavior remain. Final export engineVersion has
  historically differed from trusted CLI/SDK; no runtime parity claimed.
- Next: supervisor evaluates the exact checked candidate against accepted source
  on frozen development cases. If unsupported, inspect recovery/damage traces
  before another item-policy refinement. No worker evaluation/publication.

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
