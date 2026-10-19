# Gamma operational notes

## task-cf1855961cf741329d7612ce37c0e3cb — opportunistic altar control

- Exploration; one candidate. Branch bot/gamma, HEAD/input
  66c7cc5c5ad6cc9a583ad9a79d0c04514bc6db83. Actual edit commit
  63d05e37a937fa2bfebf3de613af2ee3113b21a8, source
  a4d664c874cc2e1e56e59dfbb08e7904b8652d305cc881b74661b00baf4264ec.
  All six initial source files matched trusted edit hashes and that commit.
  Prepared draft.cpp difference from HEAD is intentional base restoration.
  Latest candidate evaluation completed; no pending candidate blocks this task.
  Protected champion remains 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d.
  Previous notes: archive/task-be62cdde8f4f40b1b40c40728bf66a78.md.
- Hypothesis: opportunistic ten-gold altar locks on existing routes increase
  matched development win rate versus a4d664c8, without new bot faults.
  Non-increasing matched win rate or a new fault falsifies it. Tribute margin,
  enemy delays and item timing explain results; they do not replace wins.
  Mechanism is an UNMEASURED rules/source deduction, not proven by finals.

## Current strategy and change

- Retain Varg/Vendetta/Marcella/Ryth/Tavi draft order and unique fallback roster.
  Group-value/travel/clear/capture scoring, bank any positive bag, hostile-lock
  attacks, 35% retreat, 98% spawn healing and 300-gold empty-bag recall retained.
  Jungle Strength, Monster Strength, one Durability Health, then Power Strength.
- Buy one altar lock before shards whenever SDK can_buy permits, including dead
  shop turns. Cost 10 gold, carry limit one; Tavi cannot buy consumables remotely.
- On active non-stunned turns and after successful ordinary movement, use an
  owned lock on the first visible unlocked altar within Chebyshev distance two.
  No detour or combat pursuit. Never replace a visible lock of either team.
  Skip own recall/tribute/teleport, consumable restrictions and fuel below 18000.
  One use attempt per observation phase, including a False obstruction reveal.
  Placement after movement happens before arrival tribute begins.
- Only bot.cpp differs from actual edit base. No draft/combat/macro-policy bundle,
  no new search, shared memory, logging or fuel settings. Main yield unchanged.
- Reason: existing bank-any-bag travel repeatedly passes altars. Friendly locks
  allow our tribute, cancel opposing tribute and force three enemy basic hits.
  Denial may improve the objective race for ten gold without a travel tax.

## Evidence and retained negative findings

- Evaluation 054b1a16de90845c74e6ef02fa0551d50756cb27d45dd8f2f411f8fba398639f
  tested Ryth draft source c11c50fe59ace9c2050647d63b45032ba2ae34e2aad85c66e3751723e7f7604c,
  not today's restored source. Full result 102W/34L, no faults; matched
  development-base delta -0.0178571 across 56 side pairs. No promotion inferred.
- Collision A loss 20c460d7eef1f20b2d00d3fe8fab32ad7ce14aef34c68f2586ccbc6a0a102832,
  c11c50fe source: 112 vs 1012 tribute, round556, nine deaths, 242 bag loss,
  no faults/suspensions. Opponent revision UNKNOWN in summary. This does not
  establish why deaths occurred, or show that a lock would have saved the game.
- Contrasting Collision A smoke win 294d09269af4ece82722c1fac0dd7d9695d21dc59221f1e70899da1160583e33,
  same c11c50fe source/mapHash ebfcace1: 1078 vs 286, round712. Opponent revision
  UNKNOWN; not a controlled comparison with that loss. Saved ryth-draft-smoke.json.
- Exact-base Lanes B loss 12d552bb0d46f68fdffff706151e6602abc99a039e749826dfe0509f346823b2:
  902 vs 1008 tribute, round519, no faults. Beta d2d57274/e8aa98b8 identity comes
  from prior brief; summary alone lacks revision. Close score supports exploring
  denial value, not a causal lock claim. Saved ryth-draft-summaries.json.
- Current frozen manifest SHA256 079ed02010a32e2d995690fae536fc83cec46c5eb5411e19aea50d6a6b3748e1;
  all six source file sets verified. Alpha 046f1c3a/47ad41aa and beta
  50a0d7d5/675607ad buy locks before items and place along normal routes.
  Import only this independent consumable policy into gamma's frequent bank
  routes; retain gamma composition, route scoring, recovery and build.
  Alpha uses random draft/Power stat and bounded combat; beta uses Varg/Tavi/Ryth
  and reset/AoE farming with survival items, recovery latch and newer dash.
- Target-aware combat, camp claims and threat-aware banking previously regressed.
  Latest Ryth draft also regressed against this edit base. Do not repeat these
  without changed evidence. No shield/dash or Cassi/Issac policy bundled here.
- Detailed decision, falsifier and attribution: altar-control-evidence.json.
  Source isolation and guard review: altar-control-source-review.json.

## Runtime review, checks and next action

- Engine CLI 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d,
  suite published-17-release-225-v1. Routine unchanged-doc iteration, matching
  installed cambc-225 C++ header. Consulted consumable use/count, can_buy and
  placement range contracts plus BOT_REFERENCE, playbooks B/C/E/G and ledger.
  No unrelated Python binding or entire unchanged SDK reread.
- Organizer page is a download hub; additional policy/production parity remains
  uncertified. No SDK, map, opponent, threshold or accepted snapshot changed.
- git diff --check and manual source-isolation audit passed.
- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json: PASSED,
  exit 0, candidate source ff511c52577a0f42c5e17329423aaa100b0317ddcaf037f8b2ba59b808061671.
  Report .agent/check-task-cf1855961cf741329d7612ce37c0e3cb.json; exact-source
  check-report agrees. No bot source edited after validation launch.
- Risk: reserving ten gold may delay an emblem, a lock may protect an unused
  altar, and ranged enemies may clear cheaply. No measured improvement claimed.
- Next: supervisor evaluates checked exact source against a4d664c8 on matched
  maps/sides/opponents; compare wins, tribute margin, deaths, item timing, faults
  and enemy tribute delays where telemetry permits. Apply unchanged gates.
- Smoke summaries saved in altar-control-smoke.json. Both are completed Collision
  games (mapHash ebfcace1), engine build d7e29ae3. Opponent revisions UNKNOWN.
  A 41c22e31989d7f3134bb2f4da0afdcc16f151d72d994fd90a6b1f14dff082ff0:
  1028 vs 66 tribute, round716. B
  61cbb3926bef91c14be2d24b142890fc2e512019855495d858e62cd639e6cb2e:
  1002 vs 198, round826. Both sides have zero faults and fuel suspensions.
  Gamma bought four locks and retained three at final state in each game;
  inventory alone is not a trace of enemy tribute cancellation.
  These are validity checks, not a matched improvement comparison.
