# Gamma operational notes

## task-9ae6a622bdd841fbb6bd9e2cf6338e03 — capture-aware melee economy

- One foundation candidate, using Playbooks C/D/E/F. Edit base is development
  e9704a214cdc159318c72bf8d0213dd082b8f702, source
  3ddcabd550a7198b7553379a78a11ce62ece141f30dbbb772b36ef8257d2f769.
  HEAD/input is 4e34fd3f9bb5df6a3adb41d90d7ba7d45894174b, branch bot/gamma.
  All six starting files match entry/handoff and frozen gamma manifest hashes.
  Initial dirty bot.cpp/draft.cpp are the trusted restore, not unfinished work.
  Latest published candidate has completed evaluation; no candidate awaits it.
  Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains in Git.
- Hypothesis: a melee farming loop coupling reset/splash combat, strength growth,
  explicit capture occupancy and reward-per-travel/clear selection will collect
  and tribute more gems than this edit base, without more bot faults.
- Falsifier: matched development mean collected AND submitted gems must rise;
  otherwise the throughput claim is unsupported. Actual wins govern selection.
  This integrated foundation design is not an ablation or a measured improvement.
- Source audit: random draft, random single-stat Power build, basic-only combat,
  no explicit group ownership/targeting and no spawn healing wait bottleneck the
  old harvest loop. All carried gems are already banked; keep that discipline.
- Chosen coupled policy:
  * Draft Varg, Vendetta, Marcella, Ryth, Tavi in that order, skipping duplicates;
    fallback order covers all 11 released picks. 3–5 picks remain deliberate.
    Varg splash plus melee move/attack/reset is the core; Tavi scales in field.
  * Buy five Jungle Strength shards, then five Monster Strength shards, then
    Power Strength indefinitely. Query combination sizes and costs. Shop while
    dead or where can_buy allows; no duplicated family passives.
  * Private static camp cache; choose cost/value using reachable approach distance,
    visible remaining HP (otherwise static design estimate), capture duration,
    gold weight 0.12 and 1.12 basic-DPS estimate. Retain current target with 0.85
    score multiplier. Exclude living monoliths; allow already-cleared rewards.
  * Stay on cleared spawn tiles through collection. Visible uncontested allied
    collectors reserve that reward; other bodies rotate. Vacate collected regions.
    No shared-memory protocol; only each body's own visible ally occupancy is used.
  * Basic attack, then ready self reset and fresh basic attack. Otherwise use a
    legal direct/ground damage or CC spell; walking excludes incompatible spells.
    Varg shield below 75% HP against a nearby dangerous target, without replacing
    active shields. Re-read life, visibility and allowance after attacks/casts.
  * Bank before incidental fighting, including on arrival. Friendly locks permit
    tribute; hostile locks can be hit rather than causing permanent exclusion.
    Defend against adjacent enemies/cheap in-range finishes; never chase them.
  * Preserve channels; retreat before recall below 35% HP. Wait on spawn below
    98% HP. Empty-bag safe recall at 300 gold converts earnings into Strength.
- Navigation: only free approach/capture goals seed fields. Unseen spawn tiles
  are exploration destinations, not presumed live camps. Do not target visibly
  empty members of an alive group. Failed hidden bumps trigger one fresh path
  attempt and a fresh combat scan even when no movement occurred.
- Visibility/memory: group.state only when a spawn is visible (self occupancy
  suffices). Respawn observations expire at observed round + timer; zero timer
  gets one-round expiry. No hidden health/position reads or allied shared vision.
  No draft/live memory writes. Private camp records do not consume team bytes.
- Fuel: native bitboards/fields; stop optional selection below 30k fuel; movement
  requires 10k, retries at most twice; cheap in-range fallback checks at most eight
  camps. Dispatcher still catches invalid actions and intentionally yields.
  Bounded logs every 100 rounds report fuel/minimum, and round changes diagnose
  suspension. No fuel/settings overrides. Effective headroom remains to be read.

## Evidence and prior negative findings

- Frozen manifest SHA 82f9bdf3ca4449bff5684dd2c8f43150961ecfd6d7f94cbdf3e0e681e1670dda:
  alpha 0c91f9bf... basic-only/retreat; beta 0c8c6de1... adds direct spell after
  stationary attack; starter 9e804e3e... basic-only/stationary recall; frozen gamma
  is our edit base. All use random nonduplicate draft, random Power stat, nearest
  spawn unions and bank any bag. Inspection establishes code policy, not outcomes.
- Latest evaluation 1f7282e64f880a00581dd984e42729b5ba268e145861600bf4a412be4c99f07d
  evaluates cf45a24a06fc9892ff1f777432b9dc90913169d58740bebac89385b657718f51,
  commit HEAD above, NOT edit base or today's candidate: 4W/20L, delta 0,
  zero faults/missing/unknown reliability, INCONCLUSIVE/provisional coverage.
- Saved full final exports in harvest-evidence.json, byte lengths reconstructed:
  collision B a9a93bc2feb7861abe6702c38d5eb3de9adb2a37437fefb8dfd6f7b84374d7f0:
  814 collected, 682 tribute vs 1012, 34 deaths, round 1840, zero faults both sides.
  collision A 3ad701df605dac54c68d5b15ab3a75c526a93d444b0b91dc5624762a10096cfd:
  286 collected, 132 tribute vs 1012, 16 deaths, round 789, zero faults both sides.
  These establish old-candidate economy losses, not particular turn sequences.
  Finals report engineVersion 0.0.1 versus trusted CLI/SDK 2.1.6: parity unresolved.
- Varg-only draft had no matched win gain; do not repeat it as a standalone claim.
  Earlier direct-spell and Jungle-only experiments had +1/6 and +1/8 provisional
  deltas, but were INCONCLUSIVE. Filtered camp-goals alone had delta 0. New rationale
  is melee/reset/build/routing coupling, not an assertion that isolated gains add.
  Base retreat source was selected for development, not champion promotion.
- Previous operational notes retained in archive/task-a1a0fd0bf4a7437389ce07280d8aceee.md.

## Rules/API review and validation

- Changed-document review: complete handbook; C++ export declarations/descriptions
  and pinned SDK implementation; compact reference, research, organizer access and
  verification ledger. C++ export is 084ef94b...; GameRules 1c7fcf11...; installed
  cambc.h is 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
  No unrelated Python export re-review. Handbook objective: 1000 tribute; at 2000
  rounds tribute, lifetime gold, kills, then B. Main checks SDK objective/memory
  profile once. Capture/channel ticks, ranged allowances and visibility respected.
- Organizer agents page is a download hub, not an additional policy. Eligibility,
  official automation and production parity remain unverified. Teleport/sleep/
  camp-range wording disputes remain; this candidate does not rely on them.
- Initial trusted build FAILED, exit 1, source 11cfeea37918bdc6aaea7be4f311e88899af81ac0b7acc744e58f12f12b080dd:
  current web export advertises camp::is_awake(), absent from pinned cambc.h.
  Replaced it with conservative visible living camp threat bounds. Failure report
  preserved at harvest-build-failure.json. No SDK/infrastructure changes.
- Intermediate trusted build/smoke PASSED, exit 0, source db1cb70107dcc529db9661cfef2f356cbdb0d1b66109f52d73ed753f48c4d64b;
  harvest-intermediate-check.json. Subsequent hidden-bump refresh and diagnostics
  require final exact-source check below; do not treat this as final validation.
- `python3 experiments/gamma/check_harvest.py`: PASSED, exit 0;
  harvest-source-check.json. Source safety invariants and finite geometry/draft
  checks only; no SDK runtime behavior or strength inferred.
- `git diff --check`: PASSED, exit 0.
- Final trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact source
  197bec154516a17926028ab2fa5c9572571ffd7e2ac1f94a66aea43936ddc02f.
  Report .agent/check-task-9ae6a622bdd841fbb6bd9e2cf6338e03.json;
  check:task-9ae6a622bdd841fbb6bd9e2cf6338e03:197bec154516a17926028ab2fa5c9572571ffd7e2ac1f94a66aea43936ddc02f.
  Smoke IDs 15228ea17c4b294bf3c47db055c6974a61e89ae7e88acc9cb522ea366145e619
  and 0fc4f4841f03443d4d742b70faedf860146a6d5ebd5fd1dfe945283614218226.
- Optional smoke log exports were DENIED (exit 1) by arena-client:
  `slice --match-id 15228ea17c4b294bf3c47db055c6974a61e89ae7e88acc9cb522ea366145e619 --file bot-a.stdout.log`
  and `slice --match-id 0fc4f4841f03443d4d742b70faedf860146a6d5ebd5fd1dfe945283614218226 --file bot-b.stdout.log`,
  both with `--config /var/lib/battlecode-volume/config/gamma.json`.
  Exact response: only this lane's development evidence may be exported.
  Stopped those reads without retrying or seeking private artifacts. Completion,
  scores and fuel headroom remain unknown. Candidate is fully checked, but result
  is BLOCKED under the instruction to stop on a permission denial; preserve it
  for supervisor review. No additional source changes after the final check.
- Risks: composition may be weaker on isolated/ranged maps; greedy value scoring
  can converge bodies or neglect contested territory; safety thresholds may still
  recall too late; monolith exclusion gives up that objective. No per-turn loss
  trace proves the hypothesis. Tournament evaluation and fuel telemetry decide.
- Next: supervisor reviews the evidence-export denial and retained checked patch;
  if accepted for evaluation, compares it with the edit base across
  frozen development maps, sides and opponents, then applies full promotion gate.
  If unsupported, examine capture/routing and fuel logs before another threshold.
