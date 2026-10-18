# Gamma operational notes

## task-74db5e961da646ab895aa56505d86528 — recovered capture-aware melee economy

- One foundation candidate (brief also labels experiment mode refinement).
  Branch bot/gamma; HEAD/input 4e34fd3f9bb5df6a3adb41d90d7ba7d45894174b.
  Edit base e9704a214cdc159318c72bf8d0213dd082b8f702, source
  3ddcabd550a7198b7553379a78a11ce62ece141f30dbbb772b36ef8257d2f769.
  All six initial source files matched that Git commit and frozen gamma hashes.
  Initial bot.cpp/draft.cpp diffs are the trusted restore. Protected champion
  1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains preserved in Git.
- History lookup confirmed task-9ae6a622bdd841fbb6bd9e2cf6338e03 was PAUSED,
  unpublished, with no evaluation pending. Trusted infrastructure finding repairs
  its smoke-log access and explicitly requests recovery. Its original source,
  patch and notes remain in the prior own attempt/checkpoint. Prior notes copied
  to archive/task-9ae6a622bdd841fbb6bd9e2cf6338e03.md before recovery; previous
  operational summary retained in archive/task-a1a0fd0bf4a7437389ce07280d8aceee.md.
- Hypothesis: coupling melee reset/splash combat, Strength purchases and
  capture-aware routing will increase matched mean collected AND submitted gems
  versus the edit base without new bot faults. If either mean fails to rise or
  new bot faults appear, this throughput claim is unsupported. Wins govern
  selection/promotion; this is a coherent coupled experiment, not an ablation.
- Playbooks A/C/D/E/F. Source audit: random draft/stat, basic-only combat,
  implicit capture routing and absent spawn-healing wait limit the old loop.
  Recover prior checked source 197bec154516a17926028ab2fa5c9572571ffd7e2ac1f94a66aea43936ddc02f;
  harden action restrictions and forbid post-combat walking even when a spell
  kills the last monster (can_move alone does not encode walk exclusion).

## Policy and deterministic parameters

- Draft Varg, Vendetta, Marcella, Ryth, Tavi; complete nonduplicate fallback
  roster covers all 11 choices and map-dependent 3–5 picks. No memory writes.
- Buy one Jungle Strength emblem, one Monster Strength emblem, then Power
  Strength indefinitely. Query costs/combination sizes and can_buy. Shop on
  spawn, while dead, or in field where Tavi permits it. No duplicate passives.
- Camp selection minimizes (reachable travel + estimated clear + capture)/
  (gems + 0.12 * gold); estimate basic DPS as 1.12 * Strength, retain target
  with 0.85 score multiplier. Unseen HP uses static design as uncertain estimate.
  Avoid living monoliths; permit their cleared rewards. Private camp cache only.
- Preserve capture occupancy through reward collection. Visible uncontested
  allied collectors reserve cleared groups; others rotate. Vacate after capture
  to permit respawn. Respawn observations expire at observed round + timer,
  at least one round; group state requires a currently visible original spawn.
- Attack, then ready self reset and fresh basic; otherwise legal damage/CC/AoE.
  Shield below 75% HP against dangerous nearby targets without replacing a shield.
  Refresh visibility/life/allowances after actions. Never chase enemy champions;
  defend against adjacent enemies or cheap in-range finishes (<=2 * Strength).
- Bank before incidental combat, including arrival; friendly locks allow tribute,
  hostile locks can be hit rather than excluded forever. Retain all-bag banking.
- Preserve channels; retreat before recall below 35% HP. Stay on spawn until
  at least 98% HP. Empty-bag safe recall at 300 gold converts savings to damage.
- Explicit move/attack/cast restrictions, stun guard before channel initiation.
  Free approach/capture goals; hidden bumps allow one refreshed alternative and
  fresh combat scan even if movement failed. No walk after any combat action;
  capture movement after a last-monster kill replans on the next owner turn.
- Native bitboards/fields. Stop optional selection below 30k fuel; movement
  requires 10k, at most two attempts. Cheap fallback checks at most eight camps.
  Dispatcher catches invalid actions and intentionally yields. Bounded logs every
  100 rounds include fuel/minimum; crossed-round decisions log suspension.
  No fuel/settings overrides. No live shared-memory protocol or hidden ally vision.

## Evidence and negative findings

- Current frozen manifest b7c351acc1d721afaf0c7136930d3a8acaaa8096e5077e3bba904044f778855f.
  Alpha 2e82fe18 uses bounded reset/direct/AoE/CC plus shields/heals and opportunistic
  locks; alpha 6af1685b has that combat without locks. Beta 6450f600 follows basic
  with a stationary direct spell. All retain random draft/Power stat, enemy-first
  distractions and spawn-union farming. Starter basic-only; frozen gamma is base.
  See recovery-audit.json for exact commits and strategy/source limits.
  This candidate uses no copied opponent module: deliberate melee economy remains
  distinct; clearing hostile locks avoids a failure against alpha's denial policy.
- Latest evaluation 1f7282e64f880a00581dd984e42729b5ba268e145861600bf4a412be4c99f07d
  evaluates source cf45a24a06fc9892ff1f777432b9dc90913169d58740bebac89385b657718f51,
  NOT edit base or today's candidate: 4W/20L, delta 0, zero faults/missing/unknown,
  INCONCLUSIVE/provisional-three-map-wiring. Varg-only draft did not improve wins.
- Saved prior final exports in harvest-evidence.json: collision B loss
  a9a93bc2feb7861abe6702c38d5eb3de9adb2a37437fefb8dfd6f7b84374d7f0:
  814 collected / 682 tribute vs 1012, 34 deaths, round 1840, both sides zero faults.
  Collision A loss 3ad701df605dac54c68d5b15ab3a75c526a93d444b0b91dc5624762a10096cfd:
  286 collected / 132 tribute vs 1012, 16 deaths, round 789, both zero faults.
  These establish economy losses, not turn-level causes or candidate performance.
- Additional complete old-source corners A loss in corners-loss-final.json:
  3a2714f3befc32cf60018cd36dcb15d4be608d265756cf2a4ffb8df0a5cec945,
  opponent commit 7773859f872f54d846088226ef1cf7b855cbb0a6, round 911:
  1066 collected / 784 tribute vs 1060, 20 deaths, both sides zero faults.
  High collection alone did not win; this reinforces measuring tribute and wins.
  This supplied self-play example is a loss, not a contrasting win. Individual
  older wins were not supplied; aggregate wins do not establish their mechanism.
- Prior isolated direct spell/Jungle/camp-goal experiments remained inconclusive;
  integrated reset/build/route changes need measurement, not additive gain claims.

## Rules/API review and checks

- Changed-document review: full handbook, C++ export signatures/descriptions and
  examples, pinned cambc.h implementation, compact reference, research, organizer
  access ledger and verification ledger; repeated API boilerplate deduplicated
  during review. No unrelated Python re-review. Engine/SDK 2.1.6; suite
  historical-panels-v1; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Hashes: handbook 1c7fcf111d95b4734070f8f676cd50a48154feb0673de73a31c79845afa34732;
  C++ export 084ef94b338bebf088864ba2d7d777714bcd66b6c0c03601e91e1e5153a41a53;
  cambc.h 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d;
  BOT_REFERENCE 5eb0692a69fd6440ba9ce4ede1413c4ed2a6e95720c0ef8b7b90ea4560daf7f2.
- Objective/memory profile checked once at runtime: 1000 tribute, 2000 rounds,
  8 live/1024 draft bytes. Gold tiebreak is lifetime earned; final full tie B wins.
  Web C++ export has camp::is_awake/state absent from pinned header; recovered code
  avoids those methods. Teleport/sleep/range prose disputes remain. Organizer
  Agents page is a download hub, not certification of all event policies.
- `python3 experiments/gamma/check_harvest.py`: PASSED, exit 0;
  harvest-source-check.json. Draft legality, stable geometry and safety control
  invariants only; no engine simulation or strength measurement.
- `git diff --check`: PASSED, exit 0.
- Intermediate recovered-source compilation/smoke PASSED, exit 0, exact source
  197bec154516a17926028ab2fa5c9572571ffd7e2ac1f94a66aea43936ddc02f;
  recovered-intermediate-check.json. This is not final-source validation.
- Final `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`:
  PASSED, exit 0, exact source
  3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565.
  Report .agent/check-task-74db5e961da646ab895aa56505d86528.json;
  reference check:task-74db5e961da646ab895aa56505d86528:3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565.
- Repaired smoke export access worked. Full paged finals and own stdout preserved
  in smoke-evidence.json. A 4cae2e4e3ee2e0b28310eecc700849b9deb0164dfb981b15c98aa7b292193be0:
  completed teamA win, 1006 vs 154 tribute at round 596, both sides zero faults.
  B 437e20a563cc5112573c2e614895606deb42a3db7a0cb94100002b88ffadc2bf:
  completed teamB win, 1084 vs 286 tribute at round 640, both sides zero faults.
  Map and opponent revisions are not exposed by these reports: UNKNOWN.
  Both own logs have zero bot-error/suspension/settings-mismatch markers. Logged
  running minimum fuel is 14,291 on A and 11,783 on B before dispatcher yield;
  this is observed smoke headroom, not a guarantee on other maps or every yield.
  Finals report engineVersion 0.0.1 versus CLI/SDK 2.1.6; parity remains unresolved.
  Smoke wins are validity evidence, not a controlled superiority/promotion result.

## Uncertainty and next action

- Melee can lose on isolated/ranged maps; greedy groups can converge bodies;
  recall safety is conservative and can still fail. Monolith exclusion gives up
  that objective. No measured strategic gain or production parity is claimed.
- Supervisor evaluates the final exact checked source on frozen development
  maps/sides/opponents and applies the full promotion gate. If unsupported,
  inspect capture/routing and fuel logs before further threshold changes.
