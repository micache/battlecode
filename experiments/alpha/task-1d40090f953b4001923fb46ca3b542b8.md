# Current experiment: task-1d40090f953b4001923fb46ca3b542b8

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD
  8591c7594ad9fe756ce06c24a4f05aac146396e7.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry, branch/HEAD, all six source files, documentation manifest and installed
  C++ header verified; see this task's -identity.json. Entry diff is the trusted
  accepted-source restoration, not unfinished new work. Accepted Git snapshot
  remains outside the edit transaction. Prior NOTES archived by task ID.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest candidate evaluated INCONCLUSIVE, not pending. Recent supplied tasks
  are PUBLISHED; older interrupted patches and notes remain preserved.
- Routine iteration: compact reference, RESEARCH.md, playbook C and relevant
  handbook/API/SDK sections consulted. Documentation unchanged. Separate
  organizers' AGENTS.md remains absent and unreviewed.

## One hypothesis: playbook C, recovery under repeated interruption
Taking one legal movement toward allied spawn before starting a low-health
recall will reduce mean champion deaths versus accepted source on matched
development cases. Unchanged or increased mean deaths falsifies this prediction.
Compare submitted gems, collected gems and outcomes for objective cost.

## Evidence and focused change
- Evaluation 3dc2bcc29c39834e5af404996bcad4b036a5c1a6fc4883683dbbf390b6bc78e1:
  commit 8591c7594ad9fe756ce06c24a4f05aac146396e7; source
  6f074a287b029d03848eb2ad3aef1ad7f11d5b5977f1a28f87d9f3edd21fe549,
  NOT the accepted edit start. Development: 8W/16L, zero faults/missing/unknown.
- Collision B loss 6f4c771f407c85689f920dd38d7c9c0a6f368e91c75703d9d591511c0e72081f:
  36 deaths, 990 collected, 814 submitted vs 1012, round 1448.
- Collision A loss 892076973a47e2d94a09f203bb08947ea44973984a18e83a01bcb837e1cbe737:
  17 deaths, 572 collected, 418 submitted vs 1004, round 850.
  Supplied final metrics report zero bot faults on both sides in both games.
  Strategic losses, with no identified engine failure; saved in -evidence.json.
- Aggregate losses motivate survival work; neither final aggregates nor the
  partial final.json slice establish recall-interruption frequency or causality.
  Runtime trace coverage remains unknown. No farming-order change was made.
- Reproducible source failure: low-health away-from-spawn turns call recall and
  return without moving. Damage cancels recall, permitting repeated stationary
  restart attempts while attackers remain in range.
- Add one call to existing bounded navigation toward allied spawn in that branch.
  Requery position after movement. Recall only if still away from spawn; if
  walking reaches spawn, return through official end_turn for healing instead.
  Failed/unavailable movement retains the existing recall fallback. Existing
  active-channel guard precedes movement, so useful recalls remain running.
- GameRules.md 116, 122, 272, 369-375: movement precedes channel start; channels
  block later actions, recall is damage-interruptible, spawn heals at turn end.
  C++ header 3661-3665: recall is a self-only void command; the engine validates
  channel legality. Existing move helper checks allowance, blockers/reachability.
- Same health threshold (35%), no new private/shared state, draft, shopping,
  randomness, combat targeting or fuel settings. Other five source files unchanged.
- Distinct from prior spawn-heal trials: this addresses stationary restarts away
  from spawn. No old spawn-heal guard or other experiment is combined here.

## Validation and uncertainty
- git diff --check PASSED, exit 0. Accepted-relative review shows only the
  low-health recall branch changed; unconditional official yield retained.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact checked source
  0c91f9bf05bff0bfbf70eb1a00633ec2699e650db57a1dcda0316055df93dd26.
  Report: .agent/check-task-1d40090f953b4001923fb46ca3b542b8.json.
  Reference: check:task-1d40090f953b4001923fb46ca3b542b8:0c91f9bf05bff0bfbf70eb1a00633ec2699e650db57a1dcda0316055df93dd26.
  Smoke IDs 99f1f1ee810da8db5abd887ef473791ed186710b86bc1e6f63a6ae2a530b6b67
  and e102548e16d131b44ff832e53a05a56236c47cb570171db089cfc8dfc8e18a99.
  Smoke finals/action logs not inspected; IDs alone establish neither completed
  games nor retreat branch coverage. No strength improvement is claimed.
- READY_FOR_EVAL; source unchanged after check. No publication or evaluation
  invoked by this worker. No compiler/runtime settings changed.
- Remaining risks: moving toward spawn may approach a threat, consume fuel or
  reveal an obstruction; it does not prove safety or monotonically lower actual
  path distance as live occupancy changes. A recall may still be interrupted.
  Reaching spawn by recall can still trigger the accepted early-departure policy.
- Next: supervisor evaluates the exact checked source against accepted source,
  comparing deaths, submitted/collected gems and outcomes. If mortality does not
  improve, obtain bounded runtime interruption/retreat traces before refinement.
