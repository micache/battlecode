# Gamma operational notes

## task-f10f6850851a4b819ef515def204aab6 — threat-aware banking

- Refinement; branch bot/gamma; HEAD/input/edit commit
  1b34f42a5266051ee50bae4cf74197b99b1115cb; verified edit source
  3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565.
  Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d stays in Git.
  Clean initial worktree; prior task PUBLISHED and evaluated, no candidate awaiting
  evaluation. Seven pending continuous self-play matches are not a pending candidate.
- Hypothesis: choosing banking approaches and routes using observed threats,
  reachable distance and bag-dependent channel exposure will increase matched
  mean submitted gems and reduce Collision deaths versus the edit base, without
  new faults. Falsified if either predicted metric fails to improve or faults
  appear. Wins and the full promotion gate remain decisive; no gain yet measured.
- Bottleneck evidence: current-source development losses show major gem-conversion
  failure despite collection and no faults. This suggests carrier survival as a
  useful target; final statistics do NOT establish where/when bags were lost.
- Chosen policy: rank free reachable altar approach tiles by distance, three turns
  for a hostile lock, plus projected health loss during tribute/lock clearing.
  Risk cost 12 travel rounds per health bar; add 25 rounds above 70% projected loss.
  Use SDK channel settings; starting bag sets duration, not a hardcoded threshold.
  Enemy radius = observed attack range + one step; pressure = Strength + .25 Focus
  (heuristic, not exact spell damage/cooldown). Visible damaging camps use current
  range/Strength, conservatively active because pinned header lacks wake state.
- First try a path outside observed danger; if disconnected, retry ordinary legal
  terrain. Two attempts maximum, normal fuel guards, 128 approach candidates and
  32 pressure records. No persistent enemy cache or shared-memory protocol.
  Unlocked adjacent altars precede hostile locks. Safe adjacent tribute retains
  priority; exposed carriers pass through the existing low-health recovery check.
  Shield an exposed channel when legal without replacing an active shield.
  Refresh locks/position/visibility after movement; start tribute at the selected
  approach. Preserve useful channels and a cheap adjacent submission fallback.
- Preserve melee farmer draft Varg/Vendetta/Marcella/Ryth/Tavi, Jungle+Monster
  Strength then Power Strength, capture occupancy, respawn vacating, 35% recovery,
  98% spawn healing, and 300-gold empty-bag shopping recall.

## Matched evidence and opponents

- Evaluation 3318aa749628b04a8e7d6b09d2c6a4ffbd2d8242b093832aaf420ae31c618d89
  applies to edit source above: overall 60W/12L, INCONCLUSIVE; development 39W/9L
  on 48 distinct cells, faults 0. Self-play separately 9W/15L on 24 distinct cells;
  repeated executions not independent. No holdout traces used.
- bank-route-evidence.json contains complete paged finals for supplied development
  examples, same own source and alpha 6af1685b849ad23ee9eaadb1a8de18742318d87b:
  Collision A 5fc18347ab2888b5ef80a2d503d531268fc701493973ea48b7b93e59b272826d:
  round 491 loss, 614 collected / 44 submitted vs 1012, 8 own deaths, faults 0/0.
  Collision B bcb9257d90cc7c5da9827de8231b6309f527f467408c7ae7e7bd2a4cf706a7a7:
  round 639 loss, 606 collected / 318 submitted vs 1028, 8 own deaths, faults 0/0.
  Corners A 39c976f384350091e548b0173d473c80340bafe4c9d007a8b307c718ff3045c3:
  round 459 loss, 624 collected / 528 submitted vs 1018, 10 own deaths, faults 0/0.
  Elkring B 316d4ad70f40c542f79b7baa8a275708ce76cd1e86e336fa6d75fe30df1ea78b:
  round 542 loss, 792 collected / 612 submitted vs 1008, 14 own deaths, faults 0/0.
- Contrasting prior exact-base smoke wins are in smoke-evidence.json and archived
  prior notes: A 4cae2e4e3ee2e0b28310eecc700849b9deb0164dfb981b15c98aa7b292193be0,
  B 437e20a563cc5112573c2e614895606deb42a3db7a0cb94100002b88ffadc2bf.
  Both completed, 0/0 faults; maps/opponent revisions unknown. Not controlled
  development contrasts; no individual current development win ID was supplied.
- Frozen manifest e290bdbd287c9cc6b0e328e297d0a9b42b360b43f374fcb9cc4a458be6071104.
  Inspected alpha 6af1685b source: random draft/stat, enemy-first combat with
  reset/direct/AoE/CC and shields/heals, nearest unlocked altar union, camp union.
  It can attack carriers while ours previously ignored fights whenever banking.
  Inspected beta d2d57274232ca7cead5bacf650d6f51fd5b3bc3d: deliberate Varg/Tavi/Ryth
  draft, Strength+durability build, 45% recovery, shield-if-exposed, unlocked-first
  banking, group capture/reservation and bounded geometry-ranked routing.
  Adaptation is risk-aware carrier routing, not copied opponent code or draft.
- Rejected for this candidate: broader draft/build rewrite (working integrated
  base already improved development); blanket combat-before-banking (would lose
  useful score windows); permanent danger exclusion (can deadlock carriers).
  Prior isolated Varg-only and other economy trials remain inconclusive; details
  preserved in archive/task-74db5e961da646ab895aa56505d86528.md and earlier archives.

## Checks, uncertainty and continuation

- Rules/SDK unchanged per trusted handoff; consulted BOT_REFERENCE, playbooks B/C/F,
  research and organizer ledger, relevant tribute/lock rules and pinned header
  channel/visibility/ability contracts. Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  Organizer download hub does not establish every event policy or production parity.
- Existing harvest source/geometry regression: PASSED, exit 0;
  harvest-source-check.json. Source invariants only, not runtime simulation.
- `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`:
  PASSED, exit 0; exact candidate source
  f7d71d2cebfdbfc7b1214a888c1514ae33657003c43d52c3e5e7a17894ff6ac6.
  Report .agent/check-task-f10f6850851a4b819ef515def204aab6.json;
  check:task-f10f6850851a4b819ef515def204aab6:f7d71d2cebfdbfc7b1214a888c1514ae33657003c43d52c3e5e7a17894ff6ac6.
  Exact-source check-report agrees. Complete smoke finals and own paged logs saved
  in bank-route-smoke.json. A 564439933d2c1c8ecc407eab3a5efa6a72e0bde69456b05150bb62d368e7d9b4:
  completed teamA win, 1046 vs 396 tribute at round 967, both sides zero faults.
  B 6ef0c1ddd390b20bf2d3cfa4df15688cdc7ffb03dcc8bf3d8b2e37249509c168:
  completed teamB win, 1004 vs 374 tribute at round 612, both sides zero faults.
  Maps/opponent revisions unknown in these exports; not controlled gain evidence.
  Both logs have zero bot-error, suspension and settings-mismatch markers.
  Logged running minimum fuel: A 11497, B 13330 before dispatcher yield, not a
  guarantee for every turn/map. Finals still report engineVersion 0.0.1 versus
  CLI/SDK 2.1.6; production parity unresolved as in prior notes.
- `git diff --check`: PASSED, exit 0.
- Main regression risks: conservative camp ranges and enemy-step estimates can
  lengthen trips; distant safe altars may become unsafe out of vision; local
  pressure is not a full combat forecast. Fallback can still cross danger. No
  turn-level evidence proves the selected mechanism explains all supplied losses.
- Next: supervisor evaluates final checked source against edit base on matched
  development maps/sides/opponents, inspects Collision conversion/deaths and broad
  wins, then applies the unchanged champion promotion gate.
