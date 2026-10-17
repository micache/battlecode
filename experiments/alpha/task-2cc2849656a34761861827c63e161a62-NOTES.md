# Current experiment: task-2cc2849656a34761861827c63e161a62

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD a44593ce5cdc7b25e78ede877054adddbf57af6c.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry, branch/HEAD, six source files and documentation/SDK hashes verified.
  Initial diff is trusted accepted-source restoration. Accepted Git snapshot
  preserves source outside this transaction. Prior NOTES archived by prior task ID.
- Eight supplied recent tasks PUBLISHED; latest evaluation INCONCLUSIVE, not pending.
  Continuous self-play pending matches are separate, not a pending candidate evaluation.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Routine iteration: compact reference, RESEARCH.md, playbook C and relevant rules/
  installed SDK sections consulted. Organizers' separate AGENTS.md remains absent.

## One hypothesis: playbook C, threat-gated recall retreat
Moving once toward allied spawn before low-health recall only when a visible,
living, positive-strength enemy champion or camp has us in basic-attack range
will reduce mean champion deaths versus accepted source on matched development
cases. Unchanged or increased deaths falsifies this prediction. Compare submitted/
collected gems and outcomes for objective cost; do not pool distinct source revisions.

## Evidence and change
- Latest evaluation 349b6a5ff5e62585ae2c55e35935d6a9e1a355c73429f6ddcc283f59a3c411da
  is for commit a44593ce5cdc7b25e78ede877054adddbf57af6c / source
  bda6b99d4eafb07fc4069caca6abba24dd3c668024f994bd9fa4c9a02717da62,
  NOT accepted edit start. Development 1W/23L, zero faults/missing/unknown;
  mean deaths 23.875, collected 646.0833, submitted 319.6667. Provisional coverage.
- Collision A loss 08394f160e857d71f278eb061fb15bd53ddbac0bbdd2d7e6ac0bbccaa87cc4ff
  and collision B loss cb5847a2a71338d1e8d031bac3e1b9b68dea20c02dd72a61e5be3e0579350a9a
  belong to that evaluated source. Complete A-loss final reconstructed from two
  bounded slices and saved as this task's -collision-final.json: round 1391,
  teamB win, botFaults [0,0]; A 638 submitted / 982 collected, summed champion
  records 22 deaths; B 1034 submitted / 1166 collected, 36 deaths. B is accepted
  opponent source per supplied evaluation provenance. Linked champion death
  counters need care. Neither aggregate mortality nor this final proves interruptions.
- Prior unconditional-retreat evaluation 1304894436dcf2cdb4d134cbbd15c66c9071c59b1eeec55aa44bd1ddc02b9d94
  for source 0c91f9bf05bff0bfbf70eb1a00633ec2699e650db57a1dcda0316055df93dd26
  was 18W/6L with mean deaths 3.2083 (prior task notes). Prior retry-only source
  d08f6defabd911f8664dac894f139d683dcc31c686186d5dbb56c3b1f9b12202
  had 12W/12L development and separate 14W/4L self-play. These are motivation,
  not current-source measurements or controlled causal proof.
- Reproducible accepted behavior: actionable low-health turns away from spawn
  recall while stationary, including turns in visible damaging units' basic range.
  Damage cancels recall. Refinement gates the prior retreat mechanism on current
  visible threats, preserving initial stationary recalls at apparently safe positions.
- Single bot.cpp change: visibility-first live threat query, one bounded existing
  navigation call toward spawn if threatened, then own-position refresh before recall.
  Zero-strength resource clusters do not trigger retreat. Failed movement retains
  recall fallback; walking arrival yields through turn end for healing.
- No private state, shared memory, draft, attack priority, banking, shopping,
  35% threshold or runtime-setting changes; five other sources remain identical.
- Rules GameRules.md 122,270-274,369-375: recall damage interruption and timing.
  SDK cambc.h 2920-2960: common unit visibility/live queries, attack_tiles is
  geometric and ignores attack availability; 3661-3665: self-only void recall.

## Validation and uncertainty
- python3 experiments/alpha/check_threat_recall.py PASSED, exit 0; report
  experiments/alpha/task-2cc2849656a34761861827c63e161a62-source-check.json.
  Contracts verify visibility-first live queries, unchanged threshold/channel guard,
  one threat-gated move, refreshed arrival, failed-move recall fallback, official
  yield, and accepted-identical source outside the focused change. Source-only.
- git diff --check PASSED, exit 0; accepted-relative diff reviewed.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0. Exact checked source
  30783869b2a0e1af115e136a2bccea88b4b1b14b0ee0d688382cef8033fd5842.
  Report .agent/check-task-2cc2849656a34761861827c63e161a62.json;
  reference check:task-2cc2849656a34761861827c63e161a62:30783869b2a0e1af115e136a2bccea88b4b1b14b0ee0d688382cef8033fd5842.
  Smoke IDs 79fc6742c6b1dddcfc1464c3593d3e2d0a17df6f8b7d100ab2bf87dcd4a57e11
  and fabd2fa43fadaaed0ead885648b44a5335537390c9d434c54743badab70c5673.
  Smoke finals/action logs uninspected; no completed-game or branch-coverage claim.
  No source edits after trusted check. READY_FOR_EVAL, no strength claim,
  publication, tournament evaluation or official action.
- Threat test ignores spells, enemy movement, unseen attackers and camp aggro;
  range does not prove an attack. Spawn-directed paths can approach danger or fail.
  This tests progress before recall, not guaranteed escape or fewer interruptions.
- Accepted post-recall early departure remains a separate risk. No additional
  healing behavior or persistent retry state is bundled into this experiment.
- Actual branch coverage, recall interruptions and fuel headroom remain unknown.
- Final exports engineVersion 0.0.1 / packed 65536; relationship to trusted CLI/SDK
  2.1.6 is unknown. Slice carries no engine lock, so no mismatch inferred.
- Next: supervisor evaluates exact checked source versus accepted, comparing
  deaths, submitted/collected gems and outcomes. If deaths fail to decrease,
  obtain bounded recall interruption traces before further retreat variants.
