# Gamma operational notes

## task-be62cdde8f4f40b1b40c40728bf66a78 — three-pick farming core

- Refinement; branch bot/gamma, input/HEAD 7ed7e6a36e1795158656ed80c06d72b337f2192d.
  Actual edit commit 63d05e37a937fa2bfebf3de613af2ee3113b21a8, source
  a4d664c874cc2e1e56e59dfbb08e7904b8652d305cc881b74661b00baf4264ec.
  All six starting source files matched that commit and the trusted entry.
  Prepared bot.cpp restoration from HEAD is intentional, not interrupted work.
  Protected champion remains 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d.
  Prior candidate evaluation is complete; pending continuous self-play is separate.
  Previous notes preserved in archive/task-bf57edace9e2432697d916c1e30b5c6c.md.
- Hypothesis: replacing Marcella with Ryth on three-pick maps, retaining Varg and
  Vendetta and the complete edit-base gameplay policy, increases matched mean
  submitted gems AND win rate on three-pick cases without new bot faults.
  Either non-increasing metric or a new fault falsifies it. Full-suite wins and
  unchanged promotion gates govern acceptance. UNMEASURED rules/source deduction.

## Policy and reason

- Query SDK team_size. Exactly three picks: Varg / Vendetta / Ryth. Four and
  five picks keep Varg / Vendetta / Marcella / Ryth / Tavi. Full unique fallback
  roster retained; completed draft guard prevents an extra pick.
- Ryth and Marcella both start with 1,200 HP and have the same Health/Strength
  growth. Ryth starts with 50 Strength vs 45 and 100 Focus vs 50, has an area
  damage/stun, and gains Strength from the existing Durability Health investment.
  Existing fight() already handles his ground AoE, reset and walk exclusion.
- Only draft.cpp differs from the edit commit. Combat, camp routing/capture,
  bank-any-bag, hostile lock attacks, 35% retreat, 98% spawn healing, 300-gold
  empty-bag shop recall, and Jungle Strength / Monster Strength / one Durability
  Health / Power Strength remain byte-identical to the edit base.
- No new gameplay searches, observations, memory writes, logging or fuel settings.
  Dispatcher still catches failures and intentionally yields. This is a roster
  experiment, including its resulting spawn/scheduling/route consequences.

## Evidence and negative findings

- Latest evaluation ad86569852d0fa8ad4f95c05762d627ebc9a1f5295b7bf5ef91fd35ae0071554
  evaluates later source 85c39989f37666a2b352a143f278998a98770cc7a97b057dbd9daf5f1e4fc42a,
  not today's base or candidate. 112 development games: 86W/26L, zero faults.
  Matched base a4d664c8: 83W/29L; small +0.0267857 delta, separate from champion.
- Collision A loss 38f16f3c23229d96bf1d0f5526990c0f69696172e36f7ebe6bcec46534624b98,
  later 85c39989 source: 72 vs 1052 submitted at round 596, nine deaths,
  zero faults. Three-pick roster excludes Ryth. Marcella 36 collected / 0 tribute /
  three deaths; Varg 288/72/four and Vendetta 22/0/two. Opponent revision UNKNOWN
  in summary; draft resemblance does not establish alpha identity.
- Ambush A loss 2ac9c4a85653e75e732974e92a83ee05eb15367bcdab91f1267c52dc6614dfe6,
  same later source: 720 vs 1010 tribute, round 816; Ryth 390 tribute / zero deaths,
  Marcella 30 / one. Finals do not establish why; five-pick behavior is retained.
- Exact-base Lanes B loss 12d552bb0d46f68fdffff706151e6602abc99a039e749826dfe0509f346823b2
  vs beta d2d57274, revision e8aa98b8 per brief: 902 vs 1008 tribute at round 519,
  zero faults. Marcella 318 tribute / zero deaths vs Ryth 168 / zero. This is a
  useful counterexample to universal Ryth superiority: retain larger-team order.
- Full paged summaries saved in ryth-draft-summaries.json. Current engine finals
  report official engine 0.0.3 build d7e29ae3. No per-turn cause inferred.
- All six frozen opponent file hashes verified against manifest d4ad3588.
  Alpha 6af1685b uses random draft/Power stat, enemy-first bounded combat and
  spawn-union farming. Alpha 5f73d078 adds nearby lock control. Beta d2d57274 uses
  Varg/Tavi/Ryth opening, group routes, reset/AoE, recovery latch and survival
  items; beta 50a0d7d5 adds dash/locks. Adapt the Ryth small-team idea to gamma's
  melee core; do not clone beta's field-shopper composition or route policy.
- Target-aware combat, camp claims and threat-aware banking previously regressed.
  Do not repeat without changed evidence. Do not bundle the later shields/dash
  experiment into this base. Linked Cassi/Issac needs its own survival policy.
- Decision, falsifier, source isolation, opponent identities and risks saved in
  ryth-draft-evidence.json. No measured improvement claimed.

## Runtime review, validation and next action

- Engine CLI 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d,
  suite published-17-release-225-v1. Changed-document review used current rules,
  C++ API contracts, matching installed header, BOT_REFERENCE, RESEARCH, organizer
  ledger and playbooks A/B/E/G. Header SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264 verified.
  Documented ward::owner is absent from pinned header; unused. Handbook unchanged.
  The organizer page is a download hub; additional policy/production parity is
  not certified by this review. No unrelated Python binding imported.
- Source-isolation audit and git diff --check passed before trusted check.
- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json: PASSED,
  exit 0, source c11c50fe59ace9c2050647d63b45032ba2ae34e2aad85c66e3751723e7f7604c.
  Report .agent/check-task-be62cdde8f4f40b1b40c40728bf66a78.json; exact-source
  check-report agrees. No bot source edits after validation.
- ryth-draft-smoke.json saves complete paged summaries. Both completed Collision
  games match the historical Collision mapHash ebfcace1; opponent revisions
  UNKNOWN in summaries. A 294d09269af4ece82722c1fac0dd7d9695d21dc59221f1e70899da1160583e33:
  1078 vs 286 tribute, round 712. B
  8a73ba1019a4eef0ad82bd7f3323b4c6cc966d703aa604ad0acaf678b4d6902d:
  1006 vs 506, round 888. Both show Varg/Vendetta/Ryth for gamma, zero faults
  and zero fuel suspensions on both sides. Validity evidence, not a controlled
  improvement claim. Official engine build matches the current pinned profile.
- Complete own smoke logs saved in ryth-draft-smoke-logs.json with padding
  removed: zero error/suspension/settings-mismatch markers. Sampled running fuel
  minima A 12693 / B 12909; not an all-map guarantee.
- Final git diff --check passed.
- Risk: loss of Marcella stun immunity may outweigh Ryth's farming/area control;
  current reset-first combat may limit area spell value. Draft changes positions
  and routes too. Historical finals cannot prove the predicted mechanism.
- Next: supervisor evaluates exact checked source against a4d664c8 on matched
  maps/sides/opponents, separating three-pick results from unchanged larger-team
  controls; inspect tribute, collection, deaths, faults and wins. Apply unchanged
  champion gate. If unsupported, inspect small-team route/recovery traces before
  changing combat or importing a second macro policy.
