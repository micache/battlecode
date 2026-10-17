# Current experiment: task-3afe79d6edd04c12b15814296878cc69

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD 4d75e3cd3a979ebc2c3b332fb7fda79c5e5383d3.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Six entry source files match accepted commit and supplied file hashes exactly.
  SDK header and unchanged documentation hashes verified; see -identity.json.
- Engine/SDK 2.1.6; suite historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest evaluation 4fc13eb7140afa033901cdc7265a04ec1886e8821bd2bb330633e72aac0e6e83
  is INCONCLUSIVE, 9W/9L, zero faults, provisional three-map coverage. Its source
  7ca1f1a701c05af2c3c07f5eb05407f470585fd523a6eed91af5314aeac18741,
  revision 9ce920873e6ddf0ae4b087adb9d5f690304da82eee2a1814a085a71e9c5b6318,
  commit equal to input HEAD, is NOT the restored edit source. No pending candidate.
- Previous notes archived as task-1f839e6b5aba43b3a37f9f38acc716b1.md.
  Earlier interrupted patches/notes already preserved; none applied here.
  Accepted Git snapshot remains outside this edit transaction.

## One hypothesis: playbook D, unused direct camp damage
After a basic hit on a surviving visible camp, using one ready direct-damage
spell before any movement will increase mean collected gems versus accepted
source on matched development cases. Unchanged or decreased income falsifies
this prediction. Compare submitted gems, deaths and outcomes for objective cost.

## Evidence and focused change
- Development loss 7fbb0ae492c35f74505540d0e92b49057a20033bd007b0c8e61519a2f17d54d3,
  collision A, evaluated source/revision above: collected 476 vs 1034, submitted
  300 vs 1012, 20 deaths, round 966; both sides have zero faults. Complete
  final.json saved as this task's -collision-final.json.
- Development loss a9898e198139d6a6e1d63a848c461a5ab1f3a8e6a27253f6fae530e57c65b2b3,
  collision B, same source/revision: collected 1114, submitted 924 vs 1012,
  31 deaths, round 1443, zero faults (supplied task feedback).
- These aggregates motivate productive farming; they do not identify spell
  omission as the cause. Clear times and per-turn ability opportunities are unknown.
- Accepted source and evaluated Jungle candidate never cast abilities. Both retain
  Focus purchases. Handbook specifies direct camp damage for Cassi, Prism,
  Stellar, Marcella, Tavi and Ren; this differs from the rejected attack-reset test.
- Added attack_camp_with_damage only to the pre-movement camp attack loop.
  Preserve the existing first basic hit; refresh camp visibility and health after
  it; scan exactly two SDK slots for direct damage, readiness, camp target
  permission and geometric range. Attempt at most one cast, then return.
- Post-movement attacks remain basic-only, ensuring walking-exclusive spells are
  not attempted after routing. The helper is reached only after earlier branches
  return without farming or perform no movement. No new state or tuning parameters.
- Installed cambc.h 3150-3348: is_ready checks cooldown and live can_cast;
  can_target_camps and valid_tiles check distinct conditions; use(camp) returns bool.
  False leaves the completed basic hit as the bounded fallback; main still yields
  after normal return or caught invalid action.
- Read compact reference, playbook D, relevant handbook/API/SDK sections and
  RESEARCH.md. Separate organizers' AGENTS.md remains unavailable.

## Validation and remaining uncertainty
- git diff --check PASSED, exit 0.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; source
  e34275aad6113db66be4569d8a5ad8b07117fb2636116df8522a586ad3223c3e.
  Local report .agent/check-task-3afe79d6edd04c12b15814296878cc69.json
  preserved as this task's -bot-check.json. Trusted reference:
  check:task-3afe79d6edd04c12b15814296878cc69:e34275aad6113db66be4569d8a5ad8b07117fb2636116df8522a586ad3223c3e.
- Wrapper smoke IDs a393c354651260d9a72cceb564856445b58a6182b4ac452abda83f625cd92ebc
  and 6328f7f536da56a4bdf5d40eb63badb58ec3129c7b60a292312191ea61f68389.
  Smoke finals not inspected; these IDs alone do not prove full-game completion.
- Accepted-relative diff reviewed: only the new pre-movement helper and its
  call replace the initial camp attack. bot.h's entry restoration is retained.
- Outcome READY_FOR_EVAL; no tournament evaluation, publication or submission.
- Fuel headroom, actual cast coverage and full-game effect are unmeasured.
- Risks: overkill, using a cooldown before later combat, and earlier camp kills
  changing capture/routing. No improvement is claimed before evaluation.
- Next: supervisor evaluates exact checked source against accepted, comparing
  collected/submitted gems, deaths and outcomes; inspect cast opportunities if
  the income prediction fails.
