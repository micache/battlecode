# Current experiment: task-cf106a770c3345388063fa3eee68243f

## Identity and status
- Bot alpha; branch bot/alpha; input HEAD 890937102cebe2aa3035945edbdb14966078eb56.
- Edit commit 2e82fe1839be5b90390f1c625c0f1f2ec8df7cb5; edit source
  eee9346f25577fc3fee419a27bfe416ba0d3b21f9405cca9ac02b24401873133.
  All seven starting source files matched edit_commit byte-for-byte. Initial
  HEAD differences were trusted preparation. No unfinished work recovered.
- Latest candidate completed INCONCLUSIVE evaluation; pending self-play is separate.
  Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
  Previous NOTES archived as task-a0e8129eb70343e8a3e378cc10c964be.md.
- Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Installed C++ header SHA256 verified:
  90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
- Routine unchanged-document iteration: compact reference, playbooks B/C/E/F,
  research and organizer ledger, capture/respawn rules and relevant C++ API/SDK
  state and static-layout contracts consulted. Organizer page is a download hub;
  production parity and additional event policies remain uncertified.

## One hypothesis
Remembering personally observed camp respawn deadlines will increase matched
development win rate over the edit base. Unchanged or lower win rate falsifies
this prediction. Premature return trips, collection/tribute and paired-win rounds
are mechanism diagnostics. This is an unmeasured rules/source deduction; no
provided action trace establishes cooldown amnesia as a cause of any named loss.

## Evidence and decision
- Evaluation 62a7161e6f4f902a5a01be58391af6ce94c310fa362e5b2d1f0b14f630d4322f
  measures 89093710 / source 9943e525d46b664dc01dffaacf5ee853c77127c062dfefccd57458cea0e36580,
  NOT this edit source. 31W/17L, zero faults/missing/unknown reliability;
  matched edit-base delta -0.145833 across 24 side-paired cases.
  Local capture/deference regressed; do not reapply it.
- Latest-source lanes A loss 1085c0315a5b116e88f2592ec88d7ff9bca7f3667a901d3c453f2b0e47a8d99a
  vs beta d2d57274 / source 7daa9117: round 411, tribute/collection 612 vs 1006,
  candidate zero deaths, one kill; faults [0,0]. Complete final saved as this
  task's -lanes-final.json. This is throughput loss, not evidence of lost bags.
- Latest-source expanse B loss 063c811e8af66812d8d253869ec902dbcf863b574e2557546418919996f00a2c
  vs the same beta: round 521, tribute/collection 714 vs 1010, no deaths or
  champion combat; faults [0,0]. Complete final saved as -expanse-final.json.
- Exact-base expanse A loss d31442e3ba9ab8a798d54fa0191c157ebfc43386d4292e2c85a81e8db475b20c
  vs alpha 6af1685b / source 87b9be45: round 762, tribute 920 vs 1042, no deaths
  or combat. Prior task-ce64...-d31442e3-final.json remains canonical.
  Contrasting same-input base aggregate: collision 8/8 wins and lanes 5/8,
  versus latest experiment 7/8 and 1/8 respectively. Preserve successful combat.
- Frozen manifest SHA256 4070fb0970622da9f1e78902b8ad4d88e4539c9115e403bc2f6faeeca2e26a33;
  all four source sets hash-verified. Beta d2d57274 focuses groups with a melee
  farming draft; gamma 1b34f42a uses value/cost routing, collector deference,
  farming passives and expiring observed respawn deadlines. Starter and historical
  alpha retain nearest-group routing. These are source observations, not causality.
- Base queries current cooldown only when farming; hidden groups become route
  goals even if previously seen cooling down. Captures resolve before champion
  turns, after which carrying gems bypasses farming, so observations must also
  be taken before departing with a bag. Positive cooldowns cannot respawn early;
  zero means currently occupancy-blocked, not an additional fixed cooldown.
- Transfer only gamma's timestamped-cooldown idea. Fixed composition/Strength,
  shard-family changes, economic recall/field/death shopping, global/local reward
  priority, batching, broad AoE scoring, travel dashes and focus fire remain
  negative/deferred. No other old experiment was reapplied.

## Candidate policy
- Added camp_rotation.h and changed bot.cpp farming goals/banking observation.
  Per-instance cache owns immutable group identities/spawn masks and expiring
  respawn observations. No new shared bytes, inferred ally vision or enemy cache.
- Only read live group.state() after a spawn intersects current personal vision.
  Remember observation round and earliest eligible round = now + remaining timer.
  Suppress that group's route goals until expiry; expiry makes it unknown/eligible,
  never asserts a hidden respawn. Fresh alive/reward clears the old observation.
- A visible zero/negative countdown excludes only the observation round; next
  round may explore again. Spawn occupancy can delay respawn beyond our deadline.
- Observe before banking leaves a captured camp, and before farm routing. Preserve
  channel returns, retreat and enemy combat priority. Static layouts are cached
  once rather than reconstructed every farming turn. Nearest-goal pathfinding,
  camp attacks/casts, captures, draft/stat RNG, items, locks and yield remain base.
- At most 16 live state queries per pass, rotating scan start; stop observations
  below 45,000 fuel. Existing 18,000 combat reserve remains. Unobserved groups
  remain eligible. A first low-fuel initialization can yield without navigation.
  Cached geometry/goals still scale with static map group count, as in base.
  No measured headroom or changed fuel settings.

## Checks, risks and next step
- python3 experiments/alpha/check_respawn_memory.py PASSED, exit 0; report
  task-cf106a770c3345388063fa3eee68243f-source-check.json. Source invariants verify
  observation visibility, invalidation, channel/yield preservation and unchanged
  executable policy outside the farming goal replacement/banking observer.
- Temporal C++ static_assert compiled in trusted build: unknown eligibility,
  exact positive expiry, zero-timer one-round exclusion, live-state override and
  replacing an older deadline. These are pure policy checks, not engine fixtures.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0. Exact checked source:
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  Actual report inspected: .agent/check-task-cf106a770c3345388063fa3eee68243f.json;
  check:task-cf106a770c3345388063fa3eee68243f:ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  Smoke IDs b5fd719005277c3d996c4f6565c6bab15688a0a09cd02a333eae3c5e370e2cb5
  and 490e5fd1c01513d85352f4dc885f077c23234397d4e4161edb9b5a864f5daa38.
  Summary exposes no detailed runtime/fuel diagnostics; IDs alone do not establish
  full-game completion, observation-branch coverage or competitive improvement.
- Source file hashes reverified unchanged after trusted check; git diff --check
  PASSED. EngineVersion 0.0.1 in historical finals is distinct from CLI 2.1.6;
  relationship remains unknown. Deterministic reruns are not independent evidence.
- Risks: suppressing a nearly ready camp can miss useful early arrival; limited
  visibility/scan budget misses cooldowns; occupied spawn delays can outlast expiry;
  added banking scans may reduce action fuel. Capture duplication remains unsolved.
- READY_FOR_EVAL. Supervisor evaluates exact checked source against edit base and
  protected champion across maps/both sides, comparing matched wins, collection,
  tribute and paired-win rounds. If unchanged/weaker, inspect premature returns
  and missed soon-ready opportunities before adding predictive arrival timing.
  No tournament run, commit, publication, official submission or strength claim.
