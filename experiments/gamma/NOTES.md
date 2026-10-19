# Gamma operational notes

## task-ff42f1f4a5724e2a898c2cea340c1a75 — delivery-aware farm value

- Refinement; one candidate. Branch bot/gamma, HEAD/input
  48b51e3390b618f392cbec1842361bb910c207d3. Actual edit commit
  ecbc8203fd2ef0696ef7784c8b39528bb182ad7b, source
  ff511c52577a0f42c5e17329423aaa100b0317ddcaf037f8b2ba59b808061671.
  Initial six source files matched the edit commit and trusted file hashes.
  Prepared bot.cpp/bot.h restoration and farm_plan.h deletion were intentional,
  not unfinished work. Latest evaluated candidate is complete; nothing pending.
  Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains outside
  this transaction. Prior notes archived under task-2ecb2c23987f429987e000036c718854.
- Hypothesis: including camp-to-altar walking and tribute duration in farm
  selection increases matched development win rate AND mean submitted gems,
  without new bot faults. Non-positive win change, non-increasing mean tribute,
  or any new fault falsifies it. Unchanged arena gates govern selection.
- Bottleneck is a SOURCE deduction: every positive bag immediately banks, yet
  existing group value/time scoring stops at capture. Finals do not establish
  that missing delivery cost caused the observed losses.

## Policy and implementation

- Keep Varg/Vendetta/Marcella/Ryth/Tavi draft; Jungle Strength, Monster Strength,
  one Durability Health, then Power Strength; all-bag banking, 35% retreat,
  98% spawn healing, safe 300-gold recall, route locks and existing combat.
- Once per body's farm initialization, compute a native distance field rooted
  at terrain-free altar approach tiles. Terrain excludes walls, holes, altars
  and enemy spawn. Cache minimum distance over each group's spawn mask.
  Ignore future units/camps/locks explicitly: this is a static estimate, not a
  claim about hidden or future live state. No new per-turn field/search.
- Add ceil(cached delivery steps / base move speed) and SDK-configured tribute
  duration to the existing ingress/clear/capture cost. Estimate the channel from
  full static group gems; shared reward can make this conservative. Retain
  gems + 0.12*gold value and 0.85 target commitment multiplier.
- Gold-only groups incur no delivery/channel cost. Positive-gem groups without
  a static walking path to any altar approach are excluded.
- Live route reachability, visible-state checks, capture occupancy, respawn
  observations, ally collector avoidance, fallback, channel guards and yield
  are retained. No shared-memory changes or fuel overrides. Existing 30k plan,
  10k action fuel guards remain. Changes versus edit base: bot.cpp, bot.h,
  new farm_value.h. The unselected bounded shortlist/capture-entry changes
  are not bundled.
- Actual score helper has compile-time regressions: equal-reward ranking
  reversal under different delivery distances, rich distant reward still
  winning, gold-only exemption, rounded walking time and zero-speed guard.

## Evidence and limits

- Latest evaluation a80b2ab17e6feb44f9081e88aaf3beac9c96e21f7d0e1dd03c6f673bd59b76e2
  evaluated 48b51e33 / 72b489b0, NOT the restored edit base or this candidate.
  106W/30L overall, no faults; supplied matched development delta vs ff511c52
  +0.00892857 across 56 side pairs. No promotion inferred.
- That source's Ambush A loss 972d1330652b465c1e49dd645cc65a95b196f995cf4a42112af46cfd61df821c:
  round1069, 900 collected / 794 submitted vs1008, one death. Ambush B loss
  0b93f219ae848f2f059e07c6cf17fc3d8f811d32a10c9c6dc4b4ee9b1be725e7:
  round1091, 688 collected / 582 submitted vs1034, two deaths. Both completed,
  zero faults/suspensions/PvP damage. Low throughput motivates economy work;
  it does not prove travel duration or identify individual stalled turns.
  Opponent alpha6af1685b/87b9be45 from trusted feedback mapping. Complete
  summaries: ambush-a-loss-summary.json and ambush-loss-summary.json.
- Contrasting same-source Collision smoke wins b3aa8806 (A,1064 vs66) and
  bdd68fd8 (B,1066 vs198), bounded-farming-smoke.json. Different map/opponent
  is not a controlled contrast. Opponent revisions unknown in these summaries.
- Frozen manifest 83314e70bb54166827c7c20206f7e086db33bc0095567d179d3d7a2a8dcafa8b:
  verified all six file sets. Inspected alpha6af1685b's random Power stats/draft,
  bounded damage/reset combat, union-of-spawns farming and all-bag banking;
  beta7cab9b0f/fd5e2554's Varg/Tavi/Ryth, shield/dash/recovery, 12-group
  shortlist/economy penalty; alpha82a14a04's timestamped return-at-arrival
  respawn policy. No opponent private worker state accessed. Delivery scoring
  is an independent refinement fitting gamma's existing banking discipline.
- Prior target-aware combat, camp claims, threat banking, protected transit and
  Ryth swaps were not selected. Avoid repetition without changed evidence.
  Respawn-aware staging and bank batching remain separate future experiments.
- Routine unchanged-doc iteration: compact reference, playbooks B/C/F/G,
  RESEARCH/organizer ledger, C++ field/static reward and tribute contracts,
  matching installed header inspected. SDK SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
  Engine2.2.5, lock0cabb3c7, suite published-17-release-225-v1. Organizer hub
  is not complete policy review; production parity is not newly certified.

## Checks, risks and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json: PASSED,
  exit0, source 846588e44611949d792d1181a38d6ce557b233cd93442f44831431bf9c3da154.
  Report .agent/check-task-ff42f1f4a5724e2a898c2cea340c1a75.json. Actual helper
  assertions compiled in the trusted build. No source edited after check launch.
- Both Collision smokes completed, engine0.0.3/buildd7e29ae3, zero faults and
  suspensions on BOTH sides. A 8c933552: round663,1010 vs44; B 3b923d62:
  round573,1008 vs44. Opponent revisions unknown; smoke validates execution,
  not matched strategic superiority. Full summaries: delivery-value-smoke.json.
- git diff --check: PASSED, exit0. Manual source-isolation/visibility audit
  passed; final file hashes and decision saved in delivery-value-evidence.json.
- Risks: static minimum distance underestimates dynamic obstructions/large-group
  collector position; full group channel cost overpenalizes split rewards;
  altar-near competition/gold-only bias may slow collection. Initialization adds
  one field; smoke headroom does not guarantee every map/turn is suspension-free.
- Next: supervisor evaluates exact checked source vs ff511c52 on matched maps,
  sides and opponents under unchanged gates. Compare wins and tribute first,
  then collection, delivery travel, target distribution and suspensions. If
  unsupported, inspect selected-group delivery estimates before changing weights
  or bundling a new banking/rotation policy.
