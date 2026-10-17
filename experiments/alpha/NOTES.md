# Current experiment: task-1f839e6b5aba43b3a37f9f38acc716b1

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD 5765d16e1d7381f1bba26a05d5cbb3245510f65b.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry six source files matched accepted commit; branch, HEAD, SDK header and
  unchanged documentation hashes verified. See this task's -identity.json.
- Engine/SDK 2.1.6; historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest spawn-heal evaluation 06a2777c9a47592be795d4c2a5affda07b5ae83a4aaf67740d688c686b18693d
  completed INCONCLUSIVE, 27W/27L, zero faults; no pending candidate.
  It evaluates source 4b1ee918038011be24888b3b8e918831c1451e45a07ba9e518647afa93f3e21b,
  commit equal to input HEAD, revision
  f5e83ea90c77f6a30568cc8e0ebfa538d71784154478bb53cdab299817443f0b.
  This is not the restored edit source. Entry diff removing healing is intentional.
- Prior NOTES archived as task-b8b7c1c541fe484ab309e4dbec9b507b.md. Earlier
  interrupted work already has recovered patches/notes; none applied here.
  Accepted Git snapshot remains outside the edit transaction.

## One hypothesis: playbook C, camp damage and item economy
Buying exactly one Jungle emblem in the existing chosen stat, then resuming
Power shards, will reduce mean champion deaths against accepted source on matched
development cases. Unchanged or increased deaths falsifies this prediction.
Compare collected/submitted gems and outcomes to check that survival is useful.

## Evidence and focused change
- Development loss cbe9b19617e2c482cf9303d97fb976860f65ebce56fa467243479be0da88e293,
  collision B: 36 deaths, 858 submitted vs 1012, round 1438, zero faults.
  Candidate took 19,990 camp damage vs 8,952.5 champion damage.
- Development loss 37471a6676b0a12cdacdd4154427d1bdcee67f86b32b38b6172a3903fcada888,
  collision B: 31 deaths, 528 submitted vs 1034, round 1158, zero faults.
  Candidate took 17,491.25 camp damage vs 6,480 champion damage.
  Both belong to the evaluated source/revision above. Saved complete final.json
  slices as this task's -collision-final.json and -collision2-final.json.
  Aggregate damage motivates camp mitigation; damage attribution at death and
  post-purchase timing are unknown, so these totals do not prove causality.
- GameRules.md 280-324: five matching shards combine; Jungle reduces camp damage
  30%; duplicate family passives do not stack; Power gives six shards of stats.
- Added a bounded purchase prefix: use current inventory and SDK item metadata
  to buy no more Jungle shards than required for the first emblem. Partial
  purchases persist in inventory. After completion, refresh gold and use the
  original Power purchase. Both paths retain can_buy checks; zero purchases return.
- Existing three-way stat choice and RNG draws are preserved. No routing, draft,
  attack, recall, memory, channel or turn-yield change relative to accepted source.
  Previous Focus-to-Strength experiment is distinct; no stat substitution here.
- Consulted playbook C, compact reference, relevant item/API/installed C++ SDK
  sections and RESEARCH.md. Separate organizers' AGENTS.md still unavailable.

## Validation and remaining uncertainty
- python3 experiments/alpha/check_jungle_purchase.py PASSED, exit 0; saved
  task-1f839e6b5aba43b3a37f9f38acc716b1-source-check.json. Checks purchase cap,
  emblem gate, stat order, refreshed Power budget and unchanged other behavior.
  These are source invariants, not runtime or measured fuel evidence.
- git diff --check PASSED, exit 0.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; checked source
  7ca1f1a701c05af2c3c07f5eb05407f470585fd523a6eed91af5314aeac18741.
  Local report: .agent/check-task-1f839e6b5aba43b3a37f9f38acc716b1.json;
  preserved as this task's -bot-check.json. Trusted reference:
  check:task-1f839e6b5aba43b3a37f9f38acc716b1:7ca1f1a701c05af2c3c07f5eb05407f470585fd523a6eed91af5314aeac18741.
- Wrapper smoke IDs 30f62c9b024633ea8e5266d8e19c717a1a5da93de9bdf33869a5f1e3c59b11d1
  and 6d58b0e105af2c8ac7c039215a222c2613826020c7210297bd295d0b43db5eff.
  Smoke finals not inspected; IDs do not establish full-game completion or gains.
- Outcome READY_FOR_EVAL; no tournament evaluation, publication or submission.
- Risk: first emblem loses one shard of stats versus Power. Camp mitigation
  activates only after spending 150 gold and does not reduce champion damage;
  linked-body deaths, interrupted recall and leaving spawn injured remain.
  Fuel headroom and actual purchase-branch coverage are unknown.
- Next: supervisor evaluates exact checked source against accepted, comparing
  deaths, submitted gems and outcomes. If survival does not improve, inspect
  post-emblem deaths and camp choice before another change.
