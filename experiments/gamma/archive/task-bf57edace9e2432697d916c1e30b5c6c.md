# Gamma operational notes

## task-bf57edace9e2432697d916c1e30b5c6c — protected objective travel

- One refinement candidate. Branch bot/gamma; clean initial worktree; HEAD/input
  and edit commit 63d05e37a937fa2bfebf3de613af2ee3113b21a8, source
  a4d664c874cc2e1e56e59dfbb08e7904b8652d305cc881b74661b00baf4264ec.
  Entry and edit-base file hashes verified. Protected accepted champion remains
  1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d. Prior candidate evaluation is complete;
  pending continuous self-play is separate. Prior notes archived under
  archive/task-ffac8b92c85645ca803df9d1120ffd48.md.
- Hypothesis: walking-compatible shields and progress-only dashes on banking/
  recovery routes will increase matched mean submitted gems and reduce Collision
  champion deaths versus this edit base without new bot faults. Either failed
  directional metric or a new fault falsifies the mechanism. Wins and unchanged
  promotion gates determine selection. This is an UNMEASURED source/rules
  deduction; finals do not identify when/where deaths occurred.
- Source bottleneck: bank() never cast protection or mobility; low-health
  recovery also skipped abilities. This leaves Varg exposed before tribute and
  wastes Vendetta's dash while carrying. Both normally skip farming combat.

## Candidate strategy and bounds

- Preserve Varg/Vendetta/Marcella/Ryth/Tavi draft, Jungle Strength, Monster
  Strength, one Durability Health, then Power Strength. Existing combat,
  camp selection/capture/respawn, retreat threshold 35%, spawn healing 98%,
  empty-bag shop recall 300 gold and hostile-lock attacks are unchanged.
- Bank/recovery movement alone opts into dash. Ready, ground-targeted,
  walking-compatible dash must advance >=2 route steps; range capped at 2.
  Candidates intersect SDK walk-reachable tiles, cast range and free occupancy.
  This intentionally excludes hole shortcuts. Reuse the existing route field;
  no additional global search or different bank destination.
- After dash success OR a hidden-blocker reveal, refresh occupancy before the
  ordinary walk. Preserve success if dash arrived but no walk is needed/possible.
  Re-read movement allowance/restrictions and retain two movement attempts max.
  Ability inspection is two slots; candidate mask at most 25 tiles per slot.
- Shield only when ready, self-targeted, walking-compatible, exposed to a visible
  enemy/camp, and no active shield. Protect before bank travel/tribute and before/
  after recovery travel; refresh threats after travel. Never cancel a channel.
- Planning reserve 30k, action reserve 10k; ordinary walk remains the cheap
  fallback. New action logs capped at three dash and three shield events per
  body per game. No live shared memory, hidden-state reads or fuel overrides.

## Evidence and alternatives

- Evaluation 4c4120d3beed5bee0d15ccebe1c94f04fba58e7c1daa29028921e8cc3d11c95e
  evaluates the exact edit base: 31W/17L, zero faults, 48 completed games.
  Collision 3W/5L; development-base matched delta +0.0833333 across 24 paired
  cases. Protected-champion comparison is separate; result INCONCLUSIVE.
- Collision A loss 5b443161c09ff220d43551bc44b0fcc2b637731e1db0299d8b4cc8f9dbb7cdef:
  922 collected / 886 tribute vs 1032, two deaths, round 798. Varg 400 collected /
  364 submitted; Vendetta 144/144. This close race also needs useful throughput.
- Collision A loss d3e47f475514c3d33d65b8354010a50c6b949315e488caccf8170869d5b3c2ed:
  520 collected / 152 tribute vs 1006, eight deaths, round 505. Varg 224/22 and
  four deaths; Vendetta 144/0 and two deaths. Opponent revision UNKNOWN in the
  final slice; do not infer a per-turn cause or an exact opponent from its draft.
- Contrasting Corners A loss 1a34ac22cfc0efa7805b0eacf5cf2218a68ad3e56485c06c3cbe71da15d01e25
  vs frozen gamma 1b34f42a: 624 collected / 576 tribute vs 1008, eight deaths,
  round 480. Conversion alone is not the whole macro problem.
- Complete paged finals saved in protected-transit-finals.json. Exact-source
  previous smoke wins in durability-build-smoke.json: A 289095505f992a52ae7be0d50d5abeade2d1873cb061474878fca4b7743bb816
  1006 tribute round 608; B 3fc501dfc08f3d73459ced366db89ea85f676dda6bee2016f7739a1737d770f3
  1010 round 628; both zero faults. Maps/opponents UNKNOWN; validity contrasts.
- Frozen manifest 5e259511f78250eadfed0c7c3664be8623bd6eb07b19aafba60c1dc2a299b0ac;
  all file hashes verified. Alpha 6af1685b uses random Power stat/draft,
  enemy-first bounded combat and spawn-union farming. Beta d2d57274 uses
  Varg/Tavi/Ryth, group routing, shield-first exposed combat and recovery latch.
  Beta 9f7ae1c8 adds opportunistic locks to that macro (verified source diff).
  Adapt the protection idea to gamma's carrier path, not beta's whole strategy.
- Prior target-aware combat, camp claims and threat-aware bank routes regressed;
  do not repeat without changed evidence. Keep the measured survival item stage.
- protected-transit-evidence.json records hypothesis, falsifier, frozen-source
  identities, metric summary, risks and rejected alternatives.

## Validation, limits and next action

- Docs unchanged per trusted handoff; consulted compact reference, playbooks
  B/C/D/F/G, research/evidence ledger, movement/dash/shield rules, matching C++
  API sections and installed SDK. SDK hash verified; engine 2.1.6, lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Manual source-isolation audit passed: combat/threat model/defend/shop/farming
  and all five other source files match edit base. git diff --check passed.
- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json:
  PASSED, exit 0; exact source
  85c39989f37666a2b352a143f278998a98770cc7a97b057dbd9daf5f1e4fc42a.
  Report .agent/check-task-bf57edace9e2432697d916c1e30b5c6c.json;
  exact-source check-report agrees. No bot source edits after validation.
- protected-transit-smoke.json saves complete finals and own logs with zero
  padding removed after inspecting all pages. A
  62ed7201f9cb0267c8593e17095daec672d08f6f4e960e52d25df68d7e652349:
  teamA win, 1034 vs 264 tribute, round 675. B
  7aea8bbb2c3439ae907bc36ce4eea5933a1733a6aa8f2033795159f1209c36d6:
  teamB win, 1026 vs 394, round 629. Both games zero faults on both sides.
  Own logs each show three dash and three shield events, zero error/suspension/
  settings-mismatch markers. Sampled running fuel minima A 14263 / B 12865;
  not an all-map guarantee. Map/opponent revisions UNKNOWN; validity only.
- Risks: dash consumes a cast that could later reset combat; shield can be spent
  on a threat that never attacks; conservative paths forgo hole shortcuts.
  Hidden threats and route choices remain uncertain. Finals cannot establish
  transit deaths, improved safety or competitive strength. Production parity
  remains unresolved (saved finals report engineVersion 0.0.1).
- Next: supervisor evaluates exact checked source against this edit base across
  matched maps/sides/opponents; inspect Collision deaths, tribute and wins,
  plus faults and broad regressions. Apply unchanged promotion gates.
