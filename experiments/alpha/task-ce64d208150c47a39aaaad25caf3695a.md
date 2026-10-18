# Current experiment: task-ce64d208150c47a39aaaad25caf3695a

## Identity and status
- Bot alpha, bot/alpha; HEAD/input/edit commit 2e82fe1839be5b90390f1c625c0f1f2ec8df7cb5.
- Base source eee9346f25577fc3fee419a27bfe416ba0d3b21f9405cca9ac02b24401873133.
  All seven entry source files matched trusted hashes; initial tree clean.
- Latest candidate evaluation completed INCONCLUSIVE, not awaiting evaluation.
  Self-play pending games are separate. No unfinished patch recovered/applied.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
  Prior notes archived as task-a625d4c1125a40d08a86a8eb89ddb56a.md.
- Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. SDK header and opponent manifest/source hashes verified.
- Unchanged documentation, routine iteration: compact reference, playbooks B/C/F,
  research and organizer ledger, relevant recall/shop/capture rules, C++ API and
  matching installed SDK inspected. Organizer hub is not full policy review;
  production parity and additional participation/automation policies remain unknown.

## One hypothesis
Legal field/death shopping and quiet empty-bag resupply at 300 gold reduce
completion rounds on paired development wins without lowering matched win rate.
Unchanged/increased paired-win rounds or lower win rate falsifies this hypothesis.
This is an unmeasured rules/source deduction, not a traced cause of the losses.

## Evidence and decision
- Evaluation 089fa436cc9f5a5b0108459554430b05581849083c8235228c59e16c52b7b587
  measures this edit base: 45W/3L, zero faults/missing/unknown reliability. Against
  development base 6af1685b, matched win-rate delta +0.0625 over 24 side-paired cases.
  All three losses are against frozen alpha 6af1685b / source 87b9be45... .
- Expanse A loss d31442e3ba9ab8a798d54fa0191c157ebfc43386d4292e2c85a81e8db475b20c:
  round 762, 920 vs 1042 tribute; no champion combat or deaths on either side.
- Interlock B loss e13df8ea410ce488d7c6b742864facadb23fd58a6f9329f4ea07902cf5f21256:
  round 541, 590 vs 1020 tribute; eight candidate deaths. Type 8 is Willow,
  not Tavi: no Tavi-specific evidence is inferred from this record.
- Lanes B loss f853ed6f646d40a2d6b01a335119b79ec8b2e9d0be1ca68e9df38a43cd4dd4c0:
  round 464, 836 vs 1008 tribute; one candidate death, no champion combat.
  Complete finals saved as this task's three -final.json files; all botFaults [0,0].
  Final engineVersion 0.0.1 is not the CLI version; relationship remains unknown.
- Contrasting wins: current source won all 24 unique self-play input cells against
  two named revisions in the brief; 225 repeats are not independent games.
  Mean unspent gold 909.0833/team across those 24 cells motivates conversion work.
  Individual winning IDs/trips/purchase timing are unavailable in supplied summary.
- Current and frozen alpha source buy shards only at spawn and recall only for
  low health. All frozen sources retain random builds and nearest-group farming;
  alpha has independent ability casts but no altar-control consumables. Relevant
  alpha source inspected; all four manifest sources hash-verified. Source observations
  do not establish opponents' per-turn decisions or official-opponent behavior.
- Handbook permits Tavi field shards and dead shopping; 300 gold buys ten shards,
  two Power emblems. Gold-based recall is distinct from failed shard-family,
  fixed-draft/stat, global capture, banking/batching and spawn-heal-only tests.

## Candidate policy and safeguards
- Keep random draft/stat family, combat, retreat, altar control, farming and routes.
  Same shard quantities and SDK can_buy guard; offer purchases wherever legal.
  Spawn/death locks still take precedence over shards. No extra shop travel for Tavi.
- After retreat/combat/banking, recall only with empty bag and >=300 gold, off spawn,
  able to move, no visible enemy champions, no visible positive-strength living camp
  whose attack range includes us, and no cleared group under our current position.
- Never inspect a group's live state unless occupying its spawn tile; no hidden
  enemy state/cache, shared memory additions or vision-sharing assumption.
- Private next_resupply_round throttles attempts to once per 40 rounds; deadline is
  stored before recall. Interrupted/invalid optional recalls resume ordinary play;
  low-health emergency retreat has its original independent priority/threshold.
- Existing channels return before purchases. Camp threat scan capped at 16 and all
  scans abandon optional work below 18,000 fuel. Normal runtime settings unchanged;
  that reserve is a planning guard, not measured headroom. Dispatcher still yields.

## Validation and uncertainty
- python3 experiments/alpha/check_economic_resupply.py PASSED, exit 0; report
  task-ce64d208150c47a39aaaad25caf3695a-source-check.json. Source contracts verify
  channel/order guards, visibility/capture safety, retry deadline, unchanged purchase
  arithmetic/combat/farming/other executable files and official yield. Not engine coverage.
- git diff --check PASSED. Trusted final check details appended below.
- Risks: five-tick recall plus return travel may cost more than the added stats;
  field Health raises maximum without healing; visibility cannot rule out hidden
  interruption. New routes/earlier purchases can change combat and scheduling RNG.
  No comparative evaluation, exact resupply frequency or fuel headroom measured.
- Next: supervisor compares exact checked source with edit base and protected
  champion on varied maps/both sides, using win rate and paired-win completion rounds.
  If slower, inspect recall frequency/travel and branch coverage before tuning thresholds.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact source 7a14708a701b4c911b6ec7d9b06a9f379f7bb70018cfc2090cdf906fb45e9ae1.
  Report .agent/check-task-ce64d208150c47a39aaaad25caf3695a.json; trusted reference
  check:task-ce64d208150c47a39aaaad25caf3695a:7a14708a701b4c911b6ec7d9b06a9f379f7bb70018cfc2090cdf906fb45e9ae1.
  Smoke match IDs 7ade61f48674664036cc461628a9d3dba34e6896ea72911b2f27e0884bd0d66f
  and 332a3dcd077dcd9d53ad7445dbe184ca4d49aa75416612a4ce0a4061178a1309.
  Report supplies no detailed action/fuel diagnostics; smoke IDs alone do not
  establish completed games or optional resupply coverage. First pre-cooldown check
  also passed (source 8a04b5ac...), but only the above source is the final candidate.
- No bot source changes after the final check. READY_FOR_EVAL, no strength claim,
  commit, publication, tournament run or official action.
