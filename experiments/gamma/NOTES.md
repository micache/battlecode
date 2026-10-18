# Gamma operational notes

## task-ffac8b92c85645ca803df9d1120ffd48 — bounded survival investment

- One refinement candidate. Branch bot/gamma; HEAD/input eef19f04b32f7a09a3730ecf8464d0bf63a14e0a.
  Actual edit commit 1b34f42a5266051ee50bae4cf74197b99b1115cb, source
  3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565.
  All six initial files matched frozen gamma SHA256s. Prepared bot.cpp change
  and combat_value.h deletion restore this base, not incomplete worker edits.
  Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains in Git.
  Latest published candidate has completed evaluation; no pending candidate
  evaluation blocks this task. Pending self-play games are separate.
- Hypothesis: one Durability Health emblem after the farming core will reduce
  matched mean champion deaths AND increase matched mean submitted gems versus
  this edit base without new bot faults. Either failed directional metric or a
  new fault rejects the mechanism. Wins and unchanged gates decide selection.
  This is an UNMEASURED source/rules deduction, not an inferred replay event.
- Change: Jungle Strength, Monster Strength, exactly one Durability Health,
  then unlimited Power Strength. Stage budgets use current cost/combine_count;
  partial purchases and can_buy retained. Actual completion is refreshed after
  purchase. No other executable change relative to the edit base.
- The new stage spends at most 150 gold at default costs. Varg gains 500 HP and
  10% incoming mitigation instead of six Power Strength growths. Ryth also gains
  5 Strength from bonus Health. Spawn Health purchases heal the gained HP;
  Tavi field purchases do not. Duplicate family passives are not purchased.

## Existing strategy and bounds

- Draft Varg/Vendetta/Marcella/Ryth/Tavi with legal complete fallback roster.
  Melee reset/splash combat, low-health Varg shield preference, objective-first
  banking, hostile lock attacks, channels, recall and spawn-healing preserved.
- Reachable camp value/time scoring, 0.85 target hysteresis, capture occupancy,
  private respawn observations, ally collector avoidance, vacate after rewards.
  No living monolith farming. Free approach tiles, two movement attempts maximum.
- Retreat below 35% HP, wait on spawn until 98%; safe empty-bag shop recall at
  300 gold. Defend only adjacent threats or cheap finishes; no champion chasing.
- Visibility before live reads; refreshed observations after actions. No shared
  memory writes or allied hidden vision. No fuel overrides or extra searches.
  Optional planning stops below 30k fuel; action reserve 10k; fallback eight camps.
  No post-combat walking; dispatcher catches invalid actions and always yields.

## Evidence and retained negative findings

- durability-build-evidence.json saves feedback, exact-base contrasts, source
  identities, audited opponent policies and the decision/falsifier.
- Latest evaluation 804ae9d1b55c15c904978519941ac03229d6781dfc224b27ba9fff79067c037d
  evaluates f857236953b7f785b46f7f465b429635fbf07f961a43e1012b280aede2f970d7
  at eef19f04, NOT today's edit base or candidate: 25W/23L, zero faults;
  matched development delta vs edit base -0.0416667 over 24 side-paired cases.
  Target-aware combat did not improve this base. Earlier camp claims and
  threat-aware banking also regressed. Prior notes preserved in
  archive/task-ccebe4f09a07468fb85c1ff4ff3feb92.md.
- That later source lost Collision A
  8de1fe376614bd1e234627c66ca8ff2101cbaf19e1a5b427ea0e9aefa79fde8f:
  900 collected / 720 tribute vs 1010, six deaths, round 761; Collision B
  80b937e62772954c0abb021bfc5acc390edcbc1424af2526c38f6a8c2528dd13:
  576 collected / 504 tribute vs 1024, eight deaths, round 835. Both zero faults.
  Finals establish strategic losses, not per-turn causes or candidate behavior.
- Exact-base loss vs beta d2d57274232ca7cead5bacf650d6f51fd5b3bc3d:
  Interlock A 3e3cd7fe03e8848a724c5cb3a7478d676e4d7e0a4fb32e38f8a863014e807f3e,
  968 vs 1010 tribute, five deaths, round 609. Lanes A
  d36694ea34fad7710a893a7970a447abf89640d425d1b6f833b0628bb4422aaa,
  786 vs 1010 tribute, one death, round 432: low death count can still lose races.
- Exact-base smoke wins: A 4cae2e4e3ee2e0b28310eecc700849b9deb0164dfb981b15c98aa7b292193be0,
  1006 tribute round 596; B 437e20a563cc5112573c2e614895606deb42a3db7a0cb94100002b88ffadc2bf,
  1084 round 640. Map/opponent revisions UNKNOWN; validity contrasts only.
- Frozen manifest SHA256 a57dcb89eb62db715074041b7dbff23ee624d33001a3211e55d5a75f701d655f.
  Beta d2d57274 uses this survival item stage, Varg/Tavi/Ryth opening, group
  routes, recovery latch and AoE/reset combat. Transfer the bounded item idea
  into gamma's established macro without assuming other beta systems add gains.
  Alpha 5f73d078 uses random Power stat/draft, enemy-first bounded combat,
  opportunistic locks and spawn-union farming. All current alpha/beta source
  file hashes verified. Arena policies do not predict official opponents.
- Unchanged docs per trusted handoff. Consulted compact reference, playbooks C/G,
  relevant item/champion rules, C++ shop API and matching installed SDK, research
  and organizer evidence ledger. Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  Production parity and unrelated organizer policy remain unresolved.

## Validation, risks and next action

- python3 experiments/gamma/check_durability_build.py: PASSED, exit 0;
  durability-build-source-check.json. Checks stage order, one emblem, budget,
  permission, actual completion, Strength scaling and unchanged other policy.
  These are source invariants, not engine simulation or measured item purchases.
- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json:
  PASSED, exit 0, exact source
  a4d664c874cc2e1e56e59dfbb08e7904b8652d305cc881b74661b00baf4264ec.
  Report .agent/check-task-ffac8b92c85645ca803df9d1120ffd48.json;
  check:task-ffac8b92c85645ca803df9d1120ffd48:a4d664c874cc2e1e56e59dfbb08e7904b8652d305cc881b74661b00baf4264ec.
  Exact-source check-report agrees. No bot source edits after validation.
- durability-build-smoke.json saves complete paged finals and own bounded logs.
  A 289095505f992a52ae7be0d50d5abeade2d1873cb061474878fca4b7743bb816:
  completed teamA win, 1006 vs 198 tribute, round 608. B
  3fc501dfc08f3d73459ced366db89ea85f676dda6bee2016f7739a1737d770f3:
  completed teamB win, 1010 vs 330 tribute, round 628. Both sides zero faults
  in both games; own logs zero error/suspension/settings-mismatch markers.
  Logged running fuel minima A 14291 / B 11783 before dispatcher yield; sampled
  headroom, not an all-map guarantee. Maps/opponent revisions UNKNOWN. Smoke
  validity only; no comparative improvement claim. Finals report engineVersion
  0.0.1 despite pinned CLI/SDK 2.1.6, so production parity remains unresolved.
- git diff --check: PASSED, exit 0 after final metadata edits.
- Risks: slower clears may outweigh survival on low-contact maps; Tavi field
  Health increases max HP without healing and may trigger earlier retreat.
  Death reductions alone cannot establish a win gain.
- Next: supervisor compares exact checked candidate against edit base across
  matched maps/sides/opponents: deaths, tribute/collection, faults and wins.
  Apply unchanged promotion gate. If unsupported, inspect recovery/capture
  traces before changing item order or increasing the survival investment.
