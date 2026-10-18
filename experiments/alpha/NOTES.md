# Current experiment: task-4a36c64286504efea17aa49a4a94b17f

## Identity and prior work
- Bot alpha, branch bot/alpha; input ce9555420d862badc57ae3a90aaaa3f8e3556882.
- Edit commit bf616d85ce50cbb69c611788b2fc1660dbd465a2; base source
  0c91f9bf05bff0bfbf70eb1a00633ec2699e650db57a1dcda0316055df93dd26.
  All six entry files match that edit commit. Initial HEAD-relative modifications
  are trusted preparation, not unfinished work. Identity audit: -decision.json.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e preserved in Git
  outside this transaction. Prior operational NOTES are retained at input HEAD;
  detailed prior experiment record is task-4133354c587642a699e191721aab2290.md.
- Latest candidate evaluated INCONCLUSIVE, not awaiting evaluation. Pending
  continuous self-play is separate. No agents, commits, publication or evaluation.
- Engine/SDK 2.1.6; historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Documentation unchanged; full-review basis task-4133354c587642a699e191721aab2290.
  This iteration consulted compact reference, RESEARCH, organizer ledger,
  relevant combat/economy/execution playbooks, handbook combat/roster sections,
  ability API and matching installed C++ declarations. SDK/manifest hashes verified.
  Organizer Agents page is a download hub; policy and production-parity limits remain.

## One hypothesis: use independent combat allowances
Using independent basic/cast allowances, attack resets and useful defensive casts
will increase matched development win rate over the edit base. Unchanged or lower
win rate falsifies the hypothesis. Damage, collected/submitted gems per round,
deaths and fault rate diagnose the mechanism. This is an unmeasured candidate.

## Evidence and decision
- Evaluation d912e1c8c8bdfa01f9d989884f921680ef1491ef4a4038f06dd51663adbab5aa
  evaluates source c171145d743854536081bda47395cf3e263fb29cfe25a5c5ddb85a962adadbc7
  at input HEAD, NOT our edit base. Development 8W/16L; zero faults/missing/unknown.
  Collision and corners each 0W/8L; contrasting elkring 8W/0L across both sides.
- Collision A loss 7b67d63672e6d677f7f7d2ba04d2fbe5bd6a4fada4129411d3d36f3bf9a9d2c5:
  round 1285, submitted 754 vs 1010, collected 928 vs 1076, deaths 5 vs 32.
- Collision B loss 589598e050c5b4a530178bee61ffb36f0b973693684c1f3cb3abed4c438c2a75:
  round 1364, submitted 938 vs 1002, collected 1082 vs 1068, deaths 4 vs 10.
  Both have zero faults on both sides. Final aggregates do not establish particular
  wasted turns. Individual opponent revision is unknown in supplied failure rows.
  Evidence/metrics saved in this task's -evidence.json; no holdout evidence used.
- Frozen manifest 88c4221b7785f1d801c437b33c8cc99323d917433f0f2caa8170cb409f20af50:
  beta 6450f600 uses post-basic unit spells, disables spells after walking;
  gamma e9704a21 matches our retreat/basic policy; starter 144ab5a9 recalls
  stationary; frozen alpha bf616d85 matches this edit base. Sources/hash-checked;
  all retain random draft/stats and nearest-group farming. These are arena-source
  observations, not assertions about runtime traces or official opponents.
- Base has no casts despite random Focus purchases and kits with independent
  damage/reset allowances. This source-grounded bottleneck needs no inferred trace.
- Prior fixed-draft/Strength/capture-route experiment was map-specific; do not
  transplant its many coupled changes. Retain the base's draft, purchases, movement,
  banking and retreat policy while testing generic abilities on its actual roster.
  Earlier poor 40-gem batching and inconclusive stat-only experiments stay rejected.

## Candidate policy
- Only bot.cpp differs from edit commit; other five source files verified unchanged.
- One ordinary basic first. Then compare useful damage from available unit/ground
  spells against the extra basic supplied by a reset. Use self cast for reset;
  never ask a range-less reset for valid_tiles. Requery targets after each action.
- Unit casts check target category, visibility, health, range, cooldown and cast
  restrictions. AoE centers only on visible units; no unexplored ground search.
  Actual CC earns a small deterministic PvP preference of 20 damage-score units.
- If no damaging cast consumed allowance after a basic, Varg shields below 75%
  health; Willow heals a visible other ally missing at least half the raw heal.
  No dash policy. Basic attack choice remains the first visible in-range target.
- Walking is tracked explicitly on post-move farming calls. Exclude incompatible
  spells after movement; any pre-move combat action returns before navigation.
- Maximum 16 targets per scan, two ability slots; 18,000 fuel planning reserve.
  Skip further path planning at the reserve; always reach main's official yield.
  Cast-only turns are admitted by the early action guard. No fuel overrides.
- Existing active channels, random build/draft, 35% retreat, banking, navigation,
  priority and shared-memory traffic preserved. No new shared/private protocol.

## Validation and uncertainty
- Source audit passed: entry/edit identity, installed SDK hash, all frozen opponent
  hashes, five unchanged source files, and unchanged noncombat policy blocks.
  See -decision.json for per-file hashes and manual action-contract review.
- git diff --check PASSED, exit 0.
- Initial intermediate bot-check PASSED, exit 0; source 916eee01205f2a15ca93bd7642d62f6f42eca563714b51e18841d2ec53400fcb.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact source
  87b9be4549dd0ee3a3038907bcfb86b79cfb2d33f344f8749d9532a8e6382e01.
  Report .agent/check-task-4a36c64286504efea17aa49a4a94b17f.json;
  reference check:task-4a36c64286504efea17aa49a4a94b17f:87b9be4549dd0ee3a3038907bcfb86b79cfb2d33f344f8749d9532a8e6382e01.
  Smoke IDs 041c8f60d32f3abfa222959cbd0d02a0409aa1620b98fede1bf116e3d240d16d
  and 99c7a98342fcd8106780f301c865da9dd19e5ea941f020e6c60870e93cbff6f0.
  No source edits after final check. Completion/coverage not inferred from IDs.
- No new implementation-mirroring tests; wrapper supplies compile/runtime smoke.
- Measured win-rate improvement, branch coverage and fuel headroom remain unknown.
  Reserve is a policy guard, not a guarantee against one expensive native call.
- Expanded spell range can delay banking; AoE can wake other camps. Reset scoring
  ignores armor/splash; defensive casts are fallbacks after damage. At the reserve,
  a follow-up basic may be skipped. Random nondamaging Focus builds, implicit camp
  capture, spawn-heal departure and occupied-goal navigation remain inherited risks.
- Next: supervisor evaluates the final exact checked source against edit base and
  protected champion across maps/both sides. Compare wins and objective throughput;
  inspect bounded combat/fuel traces if a regression needs causal diagnosis.
