# Current experiment: task-60546c3a86fa400bb632346db8815d8c

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD a5ab224c3fe72bc9feb762d976c6058ca905a72b.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK 2.1.6; suite pilot-wiring-v1; envelope engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Branch and HEAD match task. Entry source exactly matched accepted_snapshot/src
  (diff -r exit 0); worker.py make_attempt restores accepted source at startup.
- Preserved entry tracked diff in task-60546c3a86fa400bb632346db8815d8c-entry.patch.
  Prior notes archived in task-0e948f1303a047e49c83a62c9106b875.md.
- Previous banking-priority candidate source
  0e56af7ea1530234b68be56d4cac56ffe8470646b663e89a2c11e8fab4ad023d
  completed evaluation INCONCLUSIVE; no pending candidate identified.

## One hypothesis: playbook C, item value and farming economy
Redirecting the former Focus power-shard build to Strength will improve basic
attack camp clearing and subsequent gem income because the policy casts no active
abilities. Falsifiable source invariant: build indices 0/1 buy Strength and index 2
buys Health, using the unchanged random_number(3) draw and purchase legality guard.
Evaluation prediction: higher mean collected gems than the accepted bot on matched
development cases; submitted gems and outcomes check whether extra income converts.

## Evidence and implementation
- Supplied evaluation 64d2bd09b993111371fe7fa209382a408be4ee874fd37496f972a6b6f3dbbf97:
  previous candidate at input HEAD had 2 wins/4 losses and zero reported bot faults.
  Coverage is provisional three-map wiring; it does not evaluate this new source.
- Corners B, 73a3820f4d5f4c7246646350de1c772c03733c5eaa4f18e08450f3e973d89857:
  previous candidate collected 230 vs 1014, submitted 146 vs 1014, deaths 16 vs 5;
  completed round reported as 396.
- Collision A, 956e6de8e2854f8a99475029f6e967d55209de0a59779b96b84a24fcc307a6f5:
  previous candidate collected 814 vs 1122, submitted 660 vs 1034, round 1264.
- Both cases use candidate revision 0e5cc8e75f19491f8c9dce2fd50c12e06f26231692a5204e0dca9ae18f7c2fbf
  versus opponent source equal to base. These income deficits motivate the change
  but do not prove item choice caused the losses. Per-build clear times are unknown.
- Accepted source assigns a persistent three-way build then spends available gold
  on Strength/Focus/Health Power shards; runtime source has no ability-cast calls.
- Replaced only the Focus array entry with Strength, retaining the same RNG draw,
  purchase quantity and can_buy guard. Updated comments in bot.cpp and bot.h.
  Executable source delta from accepted is exactly this item replacement.
- GameRules.md 280-303: Strength increases basic damage; shards use champion stat
  growth; Power emblems grant six shards of the selected stat. Matching installed
  C++ cambc.h item declarations and can_buy(item,count) contract reviewed.
- Documentation export hashes match RESEARCH.md. Compact reference and relevant
  handbook/SDK sections consulted; separate organizers' AGENTS.md still missing.

## Validation, uncertainty and next action
- Source invariant check PASSED, exit 0; saved report
  task-60546c3a86fa400bb632346db8815d8c-source-check.json. Confirms only executable
  delta, preserved build RNG draw, purchase legality and unchanged dispatcher/draft.
- git diff --check PASSED, exit 0.
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; checked source hash
  24f016d952f46c984bfb2eeff620bbfb78aa5a47a6b72d7893acbf616baeb79f.
- Local report: .agent/check-task-60546c3a86fa400bb632346db8815d8c.json.
- Trusted report reference (not directly opened):
  /srv/battlecode/checks/task-60546c3a86fa400bb632346db8815d8c/24f016d952f46c984bfb2eeff620bbfb78aa5a47a6b72d7893acbf616baeb79f/report.json.
- Wrapper smoke IDs: 602dc2b7c5479c9706f8f2ea0c779d05088fe16f7e9d0881cc354059ff39c7be,
  da11077d227246d4779e4e4b367a938b39e6a0ad57eb7a8b6aa66e0f04a6d83f.
  Finals not inspected; IDs alone do not establish completed full games or gains.
- No strength claim. Ren's Focus-based retaliation can benefit without active casts;
  losing that scaling may hurt. More basic damage may also increase unwanted combat.
  Full runtime fuel headroom, build-specific performance and capture timing unknown.
- Supervisor should evaluate this exact candidate versus accepted source, comparing
  collected/submitted gems and outcomes. Next idea only after evaluation: inspect
  build-specific camp clearing if this item substitution fails.
