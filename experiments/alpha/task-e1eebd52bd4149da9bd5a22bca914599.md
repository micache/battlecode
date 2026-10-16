# Current experiment: task-e1eebd52bd4149da9bd5a22bca914599

## Identity and prior work
- Bot alpha, branch bot/alpha, engine/SDK 2.1.6, suite pilot-wiring-v1.
- Accepted/input commit: c0cebd720fcd55e2bbb51d57dd2c398889d4071e.
- Base source: 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Clean worktree at entry; working source and preserved accepted snapshot hashes matched.
- Previous bootstrap note: pinned official C++ starter after two reviewed full games;
  baseline was pending at that time, with no improvement claim.
- Supplied feedback b98bf9c37503e3505a4f6134c510a978c0e243655b8b9b217c251dc9b310b096
  now marks that baseline ACCEPTED; no unevaluated prior patch was present.

## Hypothesis (playbook C: recovery policy)
Holding an injured champion on allied spawn until turn end will prevent the
accepted policy from leaving immediately after recall, allowing full spawn
healing before its next departure. Falsifiable invariant: after spawn shopping,
health < max_health implies no movement, combat, banking or farming that turn.
Expected strategic effect: fewer low-health departures and repeated recalls;
matched evaluation may show lower deaths and higher tribute, but neither is proven.

## Evidence and change
- Feedback reports zero bot faults over six cases, three wins and three losses.
- Source revision above: collision B, match
  2ea55d897829d837d2d71c66198c5e67dd6991fd3c1217ca8471d7c5a158a6cc:
  36 deaths, 814 submitted gems, opponent 1012.
- corners B, aa5eee7c876f7b4eb4d80cdb77aa81321c8a3795fa7cb2c68d188a54e2b76be0:
  16 deaths, 110 submitted, opponent 1020.
- elkring A, 169e3d8697903fa0ff9301f2f6e0c9648e8f61019d631a68a2964eb4e3756b76:
  43 deaths, 324 submitted, opponent 1008.
- These final aggregates do not establish recall as the cause of those losses.
- Source inspection: play_turn shopped on spawn and immediately continued routing,
  while recall excludes at_spawn. This permits a low-health recall arrival to leave
  before healing. GameRules.md lines 122 and 373-375 specify turn-end healing.
- Matching installed C++ cambc.h provides float health/max_health and spawn_region.
- Only bot.cpp changed: after spawn shopping, return if health < max_health.
  main.cpp still calls end_turn after this return. No new parameters or shared state.

## Validation and uncertainty
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
- Result PASSED, exit 0; wrapper returned two smoke match IDs.
- Candidate source: 65c8c92fcea5bb2a17bc9476695a4aaff8a9ee9d2a7666dc88ba4843ec27e4b7.
- Local report: .agent/check-task-e1eebd52bd4149da9bd5a22bca914599.json.
- Trusted report reference (not opened directly):
  /srv/battlecode/checks/task-e1eebd52bd4149da9bd5a22bca914599/65c8c92fcea5bb2a17bc9476695a4aaff8a9ee9d2a7666dc88ba4843ec27e4b7/report.json.
- git diff --check passed before trusted check completion.
- No tournament evaluation or improvement claim. Exact recall frequency, fuel
  headroom and low-health departure counts are unavailable from supplied feedback.
- Next: supervisor evaluates this exact candidate against the accepted baseline;
  inspect recall/departure traces if the recovery change fails to improve outcomes.
- Separate organizers' AGENTS.md remains unavailable per RESEARCH.md.
