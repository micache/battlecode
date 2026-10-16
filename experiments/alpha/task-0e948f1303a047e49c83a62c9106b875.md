# Current experiment: task-0e948f1303a047e49c83a62c9106b875

## Identity and prior work
- Bot alpha; branch bot/alpha; input revision 0ebf4aca292834ac245dad18b6affad7192c69dd.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e.
- Base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK 2.1.6; suite pilot-wiring-v1; envelope engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Entry HEAD and branch match envelope. Entry source matches accepted_snapshot/src
  exactly (diff -r exit 0). Existing tracked delta restores accepted source rather
  than carrying the previous candidate's spawn-healing guard.
- Previous candidate 1907882027b38f8e7efdf4127f06e1a7fa5fec4ed7d613f26d28c29f2927e2dd
  has completed evaluation, INCONCLUSIVE; no pending evaluation identified.
- Prior notes preserved in task-5ff630fce5d04a3b94b1dc4cff40d615.md.

## One hypothesis: playbook C, banking priority
Prioritizing banking over opportunistic enemy attacks while carrying gems will
reduce combat-induced banking delays and increase submitted gems. Falsifiable
behavioral invariant: after existing channel/safety guards, a carrier enters the
banking branch and returns before enemy targeting, including beside an unlocked
altar. Champions without gems still attack before farming. Evaluation prediction:
mean submitted gems exceeds the accepted bot on matched development cases.

## Evidence and implementation
- Supplied evaluation 59ce52b467043bd14b15846b6425fc536b01f01a8591b6098de10c56778c45a1:
  previous candidate 4 wins/2 losses, zero reported bot faults, provisional three-map
  coverage. It does not evaluate the source produced by this task.
- Collision B, 25e325ef6c7b59b534af71da0aa5d8538dd63aabc95d903ab7b27d53138db0c3:
  candidate submitted 858 vs 1012; deaths 36; round 1438.
- Elkring A, bfbf3cd6165a9d9458132cfc77209e5cba36307f4573f651175f44cf9ac25854:
  candidate submitted 504 vs 1008; collected 612 vs 1170; round 996.
- Both use candidate input revision against opponent source equal to base source.
  Aggregates establish objective deficits, not the causal frequency of delayed
  banking. Combat traces, bag loss and per-turn damage are unknown.
- Accepted source attacks the first in-range enemy and returns before considering
  tribute. Moved that unchanged enemy loop after the carrier banking branch;
  updated the priority comment in bot.h. No other behavioral change from base.
- Channels, recall, altar lock filtering, navigation, draft and farming unchanged.
  Dispatcher still yields after normal return or caught exception.
- GameRules.md 217-241: only tributed gems score; damage does not cancel tribute.
  Installed C++ cambc.h submit_gems returns void; has_altar_lock checks visibility
  internally. No new API or extra runtime queries introduced.
- Documentation hashes match RESEARCH.md; compact reference and relevant SDK/rules
  reviewed. Organizers' separate AGENTS.md remains unavailable.

## Validation, uncertainty and next action
- Focused Python source invariant check PASSED, exit 0: bank branch precedes enemy
  loop, submit and movement paths return, non-carriers retain combat before farming.
- git diff --check PASSED, exit 0.
- Trusted wrapper result recorded below when complete.
- Risk: carriers forgo useful defensive attacks or kills that would secure their
  route; existing all-altars-locked behavior can leave them idle. No strength claim.
- Next: supervisor evaluates this exact checked source against accepted source;
  compare submitted gems and outcomes. Banking-delay telemetry remains unknown.
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; source hash
  0e56af7ea1530234b68be56d4cac56ffe8470646b663e89a2c11e8fab4ad023d.
- Local report: .agent/check-task-0e948f1303a047e49c83a62c9106b875.json.
- Trusted report reference (not directly opened):
  /srv/battlecode/checks/task-0e948f1303a047e49c83a62c9106b875/0e56af7ea1530234b68be56d4cac56ffe8470646b663e89a2c11e8fab4ad023d/report.json.
- Wrapper smoke IDs: 956e6de8e2854f8a99475029f6e967d55209de0a59779b96b84a24fcc307a6f5,
  c9c9068ad320aabe886cb5523a44a88a5c5cb79c7e01197bfd7b2d7140094fbd.
  Final statistics not inspected; no completed-game or performance claim from IDs.
