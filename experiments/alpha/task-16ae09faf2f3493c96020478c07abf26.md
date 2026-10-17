# Current experiment: task-16ae09faf2f3493c96020478c07abf26

## Identity and prior work
- Bot alpha; branch bot/alpha; HEAD/input 2922097615b8a32c91fbd02096fab41896c7623c.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry identity, branch/HEAD and all six accepted source files verified. Initial
  diff is trusted restoration, not unfinished work. Accepted Git snapshot remains
  outside this transaction. Prior NOTES archived as task-33024ab941b8430ebfe7042ed223ad18.md.
- Latest candidate evaluated INCONCLUSIVE, not pending; eight supplied recent
  tasks PUBLISHED. Historical recovery artifacts retained; none applied here.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Documentation and installed C++ header hashes match unchanged handoff manifest.
  Consulted compact reference, RESEARCH.md, playbook C and relevant rules/SDK.
  Separate organizers' AGENTS.md remains absent and unreviewed.

## One hypothesis: playbook C, batch small banking trips
Requiring at least 40 carried gems before travelling to an altar, except when
this bag could reach the team's winning total, while preserving immediate tribute
beside an unlocked altar, will increase mean submitted gems versus accepted source
on matched development cases. Unchanged or decreased submission falsifies this
prediction. Compare collection, deaths, carried gems and outcomes for opportunity cost.

## Evidence and change
- Latest evaluation 52ac2f31210d8284b6d609b1f341d6ac8cff27a9e85123ce7b69638acca52217
  covers commit 2922097615b8a32c91fbd02096fab41896c7623c / source
  d08f6defabd911f8664dac894f139d683dcc31c686186d5dbb56c3b1f9b12202,
  NOT accepted edit start. Development 12W/12L, zero faults/missing/unknown;
  means 915.4167 collected and 852.3333 submitted gems. Provisional coverage.
- Collision B loss 304869219d5bacf44c7bd462d9927586991f1462250e6a2cac4702bddf9d23e2,
  that evaluated source: round 1151, 990 collected, 880 submitted, 12 deaths,
  no carried gems; A submitted 1012, outcome teamA, botFaults [0,0]. Complete
  final.json reconstructed from two bounded slices and saved in this task's
  -collision-final.json. Also supplied collision A loss
  56c6124966b3835826dadd2075bef552c1c160cc2decf687435c23147889c86e.
- Aggregate metrics do not establish trip frequency or the cause of either loss.
  Reproducible source behavior: every positive bag enters altar travel before
  farming; split camp rewards can trigger a trip for a small bag. Batching tests
  travel overhead, distinct from prior combat-priority and tribute-on-arrival tests.
- Single source change: keep existing immediate unlocked-altar tribute loop;
  gate its travel/return on bag >=40 or bag + allied submitted >= SDK winning_gems.
  Smaller nonwinning bags fall through to unchanged farming. No parameter sweep.
- Parameter 40 batches ordinary 22/24/36-gem rewards rather than mandating a trip
  after one such reward; opportunistic adjacent tribute remains available.
- Enemy-attack priority, recall, shopping, navigation, channels, draft, shared
  memory and five other source files remain accepted-identical. No new live
  hidden information or private state. Winning exception uses public team score.
- SDK cambc.h 113,4156-4163: engine-configured winning_gems and
  global_submitted_gems(team). Rules GameRules.md 215-230: carried gems do not
  score, bags can be stolen, tribute duration and current-bag completion.

## Validation and uncertainty
- python3 experiments/alpha/check_bank_batching.py --report
  experiments/alpha/task-16ae09faf2f3493c96020478c07abf26-source-check.json
  PASSED, exit 0: extracted scalar predicate covers 39/40 boundary, decisive bags
  and alternate SDK winning totals; source contracts cover adjacent tribute,
  farming fallthrough, channels and unchanged other sources. Not C++ runtime coverage.
- git diff --check PASSED, exit 0; reviewed accepted-relative source diff.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact checked source
  bda6b99d4eafb07fc4069caca6abba24dd3c668024f994bd9fa4c9a02717da62.
  Local report .agent/check-task-16ae09faf2f3493c96020478c07abf26.json;
  reference check:task-16ae09faf2f3493c96020478c07abf26:bda6b99d4eafb07fc4069caca6abba24dd3c668024f994bd9fa4c9a02717da62.
  Smoke IDs 08394f160e857d71f278eb061fb15bd53ddbac0bbdd2d7e6ac0bbccaa87cc4ff
  and cb5847a2a71338d1e8d031bac3e1b9b68dea20c02dd72a61e5be3e0579350a9a.
  Smoke finals/action logs uninspected; no full-game or branch-coverage claim.
  No bot source changed after the trusted check. READY_FOR_EVAL; no strength claim,
  publication, tournament evaluation or official action.
- Risks: larger lost bags, longer channels, waiting on farming without a reachable
  camp, and small bags stranded at round limit. Winning-total exception avoids
  withholding a potentially decisive bag but does not account for teammates'
  current channels. No threat-aware batching or timeout exception is added.
- Exact trip frequency, fuel headroom and runtime branch coverage remain unknown.
- final.json engineVersion 0.0.1 / packed 65536 differs in format from trusted
  CLI/SDK 2.1.6; its relationship to CLI version is unknown. Slice has no lock ID.
- Next: supervisor evaluates exact checked source against accepted, comparing
  submitted/collected gems, deaths, carried gems and outcomes. If submission
  fails to improve, obtain trip/bag-loss traces before changing this threshold.
