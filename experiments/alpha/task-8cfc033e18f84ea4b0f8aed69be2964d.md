# Current experiment: task-8cfc033e18f84ea4b0f8aed69be2964d

## Identity and prior work
- Bot alpha, branch bot/alpha; input HEAD
  e1a911c7fe1e75cab3427f7f729a57ed509054b6 verified.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e;
  base 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  Six accepted file hashes and SDK/header/documentation hashes verified.
  Accepted Git snapshot remains outside this edit transaction.
- Engine/SDK 2.1.6; historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest candidate evaluated INCONCLUSIVE, not pending. Previous NOTES archived
  as task-399d4cbedcc6474aa5171ffffd2c89c4.md. Older paused work is already
  preserved in owned experiments; no recovery patch applied.
- Routine iteration: compact reference, RESEARCH.md, playbook C, action-allowance
  rules and relevant C++ SDK sections consulted. Documentation unchanged.
  Separate organizers' AGENTS.md remains unavailable.

## One hypothesis: playbook C, movement after opportunistic combat
Continuing banking/farming when movement remains after an enemy basic attack
will increase mean submitted gems versus accepted source on matched development
cases. Unchanged or decreased submission falsifies this prediction. Compare
collection, deaths and outcomes to detect movement into danger or missed captures.

## Evidence and focused change
- Evaluation 2ddf5eb167ad9e5150dc0b2dfb2abc4a7442989499a95da7ed3f911f70ac6a69
  evaluated commit e1a911c7fe1e75cab3427f7f729a57ed509054b6, source
  cf24242fd1696728bbe26f1e416932bc815b950ba63e3c801782276de9df0109,
  NOT the accepted edit start. Development 10W/14L, no faults or missing cases.
- Collision A loss 620c7c3ba7b002ef9052785532aaac8a3ff003fccef99e211680430556d28d61:
  1144 collected, 990 submitted, 18 deaths; opponent submitted 1012; round 1341.
- Collision A loss 9677d8ac726f31425d2bf40544f11479eb70be33d45b023197aa7eacf579e89c:
  792 collected, 572 submitted, 22 deaths; opponent submitted 1012; round 1036.
- Both are strategic losses with zero reported faults on either side; no engine
  failure identified. Feedback extracts saved in this task's -evidence.json.
  Partial final-statistics slices corroborate champion totals; no action trace
  establishes how often unused movement caused these losses.
- Source unconditionally returned after an enemy hit, deferring every objective
  action. GameRules.md 117 gives melee separate move/attack allowances, with
  ranged move/attack shared. SDK can_move() queries current champion state.
- Replace that unconditional return with a live can_move check: return if spent,
  otherwise break from enemy scan and continue existing banking/farming logic.
  At most one enemy attack; existing attack helper rechecks attack availability.
  Farming and movement use fresh vision. New kill gems use fresh gem_count().
- No new thresholds, memory, RNG draws, casts or navigation algorithm. This differs
  from prior banking-first experiments: it retains the hit and uses leftover
  movement. Ranged spent-movement early return remains. Any subsequent priority
  draw can shift later priorities, as in existing farming turns.

## Validation and uncertainty
- git diff --check PASSED, exit 0; accepted-relative patch reviewed: bot.cpp only.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact source
  f9b2cc2dc5088ee5110d2b8e6d1ac062b79aa3fef330bf70fd59d85373626706.
  Report: .agent/check-task-8cfc033e18f84ea4b0f8aed69be2964d.json;
  reference check:task-8cfc033e18f84ea4b0f8aed69be2964d:f9b2cc2dc5088ee5110d2b8e6d1ac062b79aa3fef330bf70fd59d85373626706.
  Smoke IDs 27495c84a61f48a2ecad232cf513ad607c88ea5ba508957914a2cf544aefad60
  and b9e199e9a8654e671ca228a276ce6df395f546ce4b742f8958778cb3d3d8b64e.
  Smoke finals not inspected; these IDs alone do not establish full-game completion.
- Outcome READY_FOR_EVAL. No tournament evaluation or strength gain claimed.
- Benefit remains unproven. Melee movement can expose another camp/enemy, and
  changed farming paths can lose captures. Existing low-health recall, spawn
  healing and camp-selection limits remain. Fuel headroom is unmeasured; no
  additional search or diagnostic logging added.
- Next: supervisor evaluates exact checked source against accepted source,
  comparing submitted/collected gems, deaths and outcomes. If submission does not
  improve, obtain bounded movement/attack traces before refining this mechanism.
