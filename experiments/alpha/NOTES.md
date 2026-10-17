# Current experiment: task-399d4cbedcc6474aa5171ffffd2c89c4

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD
  675d49a0f4079094c7a86d3f79225569397593fe.
- Edit start accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e;
  base 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry/task identities, six accepted source file hashes, unchanged documentation
  and installed C++ header verified. Accepted Git snapshot remains outside edit.
- Engine/SDK 2.1.6; historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest candidate evaluated INCONCLUSIVE, not awaiting evaluation. Prior NOTES
  archived as task-2609ebf30ef34c9eb5ec2dfb854822a1.md. Older paused work already
  preserved in owned experiments; no recovery patch applied.
- Read compact reference, RESEARCH.md, playbook C and relevant rules/SDK sections.
  Separate organizers' AGENTS.md remains unavailable.

## One hypothesis: playbook C, item stats for basic attacks
Buying Power Strength shards for every champion instead of choosing Strength,
Focus or Health randomly will increase mean collected gems versus accepted
source on matched development cases. Unchanged or decreased collection falsifies
this prediction. Compare submitted gems, deaths and outcomes for opportunity cost.

## Evidence and focused change
- Evaluation 5faab96829c42119766ea23e8fd958c2a4fa5aee2798bfb1107b3f7d127f4466:
  candidate commit 675d49a0f4079094c7a86d3f79225569397593fe; source
  4db7aeeb7fca7b20464d7f97c4d79cd29d68cbcaad8080ea5030192fa29fb322.
  It evaluated the banking candidate, NOT the accepted edit start.
- Collision A loss ef124be0bb1282899e821ba1a091bb7199d5a44976eed9f341fb129d417cf079:
  814 collected, 660 submitted, 20 deaths, round 1264, zero faults both sides.
  Marcella bought 28 Health shards; Prism 18 Health shards. Their respective
  collected gems were 220 and 88, versus Strength Ryth's 506. Cross-champion
  differences do not establish purchase causality.
- Collision B loss ea1324626b4ee8793661f8c7f748f1351fd39a97fb4439074ceb50ed53343e09:
  814 collected, 660 submitted, 39 deaths, round 1352, zero faults both sides.
  Issac bought 36 Focus shards and Tavi 32; neither casts in this policy.
  Cassi bought 13 Health shards. These are strategic losses, with no identified
  engine failure or bot fault. Exact clearing/recall traces remain unknown.
- Saved paginated final-statistics extracts in this task's -evidence.json.
  SDK item indices 6/7 = Power Strength, 8/9 = Focus, 10/11 = Health.
- Accepted source randomly selects among those three stats and has no spell
  casts. GameRules.md 245-251: basic attacks use Strength; 282-303: shard growth,
  30 gold cost and Power emblem's six-stat-shard value. Focus has no basic scaling;
  Health offers survival and Ryth passive value, which this experiment trades away.
- buy_items now selects Power Strength directly, retaining affordable count and
  can_buy checks. Replace unused random build state with one initialization flag
  to retain one-time draft logging. Drop unused array include. Draft and action
  policy remain unchanged relative to accepted. No new thresholds or shared state.
- Removing the initial build RNG draw also shifts the later scheduling-priority
  RNG stream; priorities remain deterministic and use the existing policy.

## Validation and uncertainty
- git diff --check PASSED, exit 0; accepted-relative patch reviewed.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0, exact checked source
  cf24242fd1696728bbe26f1e416932bc815b950ba63e3c801782276de9df0109.
  Report: .agent/check-task-399d4cbedcc6474aa5171ffffd2c89c4.json;
  preserved as this task's -bot-check.json. Trusted reference:
  check:task-399d4cbedcc6474aa5171ffffd2c89c4:cf24242fd1696728bbe26f1e416932bc815b950ba63e3c801782276de9df0109.
- Smoke IDs 620c7c3ba7b002ef9052785532aaac8a3ff003fccef99e211680430556d28d61
  and da0342c52fc289ea4e45be06aa4a6de5faa55009d11df0a3ed16dce524bfc3cd.
  Smoke finals not inspected; IDs alone do not prove completed full games.
- Outcome READY_FOR_EVAL; no tournament evaluation or benefit claimed.
- Full-game clearing time, fuel headroom and causal attribution are unknown.
  Reduced Health may increase deaths and interrupt capture; Ryth loses passive
  scaling from Health, and Ren loses Focus-based retaliation growth. Existing
  recall recovery, unused abilities and camp
  targeting remain limitations. Faster clears can still fail to become captures.
- Next: supervisor evaluates exact checked source against accepted source,
  comparing mean collected/submitted gems, deaths and outcomes. If collection
  fails to improve, inspect clear-to-capture delays before another policy change.
