# Current experiment: task-b8b7c1c541fe484ab309e4dbec9b507b

## Identity and recovery
- Bot alpha; branch bot/alpha; input HEAD 9c798b72454402253b836cc9e19c6acadd657e53.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Entry branch/HEAD, all six source files against accepted commit, and SDK header
  verified; see this task's -identity.json. Entry diff from HEAD is the trusted
  restoration to accepted source. Existing Git snapshots preserve that baseline.
- Latest camp-reset evaluation af490775e94f281cfb6a4e0222804c31d44871e1a8184d57bf5fd517833d4eb2
  is REJECTED, not pending: 22W/32L, matched delta -0.0185185, zero faults.
  It evaluates source 3b7a9a65316fc22332da1e1b23910b91e6edea765ddd570beb2a60e4d8882377,
  commit equal to input HEAD, revision 500edc8401c2ef7a44fe62fdbafa55eed1c24f164a24d3dbe42b774f30811c90.
- Prior NOTES archived by experiment ID. Interrupted spawn-heal experiment
  task-d64d418366c1460d8577433cfbaf6b8d already has preserved recovered notes and
  changes in this directory. Inspected both and its exact own-attempt paths:
  old bot-check artifact is empty; final result absent per prior recovery.
  No trusted successful check/evaluation identified for that experiment.
  Recover its minimal behavioral change only; no attack-reset or item change.

## One hypothesis: playbook C, recall recovery
Holding an injured champion on allied spawn through turn-end healing will reduce
mean champion deaths versus accepted source on matched development cases.
Falsifier: mean deaths does not decrease. Compare submitted gems and outcomes to
check whether survival offsets the one-turn delay. Source invariant: after
shopping, an injured spawn occupant returns before combat, banking or farming;
full-health and away-from-spawn behavior retain accepted policy.

## Evidence and change
- Development loss 7a8f7341cdecb35c237bfe8e5b9c2dc36f7372ff7d91017ce56c70fa1b117517,
  collision A: 25 deaths, 946 submitted vs 1012, round 1602, zero faults.
- Development loss 36fc17ba0abdcd46bc29ede9586266d7c9e5c027ac2edf6e157d38705e01a012,
  collision B: 42 deaths, 836 submitted vs 1012, round 1423, zero faults.
  Both are from the evaluated source/revision above, not the new edit. These
  losses motivate survival work; missed-heal counts and causality are unknown.
- Accepted source shops at spawn and then can immediately route toward gems or
  camps. Recall completion clears the channel at turn start, passing its guard.
- GameRules.md 122, 369-375 and BOT_REFERENCE.md section 3: healing requires
  remaining on spawn through turn end. Installed C++ header health/max_health
  queries are live; spawn_region(team::ally) supplies the allied spawn mask.
- Added one injured-at-spawn return after shopping. Requeries health after Health
  purchases. main.cpp retains unconditional official end_turn after play_turn.
  No new state, loops, threshold, memory, draft, item or fuel-budget changes.
- Documentation manifest unchanged; consulted playbook C and relevant handbook,
  compact reference and SDK sections, plus RESEARCH.md evidence limits.
  Separate organizers' AGENTS.md remains unavailable and unreviewed.

## Validation and uncertainty
- python3 experiments/alpha/check_spawn_heal.py PASSED, exit 0; report
  task-b8b7c1c541fe484ab309e4dbec9b507b-source-check.json. Verifies ordering,
  exact accepted-source delta, unchanged other source and retained turn yield.
  These are source invariants, not runtime measurements.
- git diff --check PASSED, exit 0.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact checked source
  4b1ee918038011be24888b3b8e918831c1451e45a07ba9e518647afa93f3e21b.
  Report: .agent/check-task-b8b7c1c541fe484ab309e4dbec9b507b.json; preserved as
  this task's -bot-check.json. Trusted reference:
  check:task-b8b7c1c541fe484ab309e4dbec9b507b:4b1ee918038011be24888b3b8e918831c1451e45a07ba9e518647afa93f3e21b.
- Wrapper smoke IDs ed38b033e118c5f0a7115f9d597661d96e7b00cf2e0dd1064b29a791977c20b5
  and 8df7f25e3468f68262ee025bdad88aed139ccb4c4ba9539212ddbe9e60a1f220.
  Finals not inspected; IDs alone do not prove full-game completion or gains.
- Outcome READY_FOR_EVAL. No tournament evaluation or publication invoked.
- Runtime recall frequency, branch coverage and fuel headroom remain unknown.
  Camp choice, linked-body deaths and interrupted recalls can dominate survival.
  Waiting while injured may delay banking; no improvement claim before evaluation.
- Next: supervisor evaluates the exact checked candidate against accepted source.
  If mortality does not improve, inspect interrupted recalls in development logs.
