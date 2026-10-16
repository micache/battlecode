# Bot reference grounded in the supplied handbook

Reviewed 16 October 2026, Asia/Saigon. Read the complete [GameRules.md](sources/GameRules.md) and [BotAPIPython.md](sources/BotAPIPython.md) at bootstrap, then consult this reference and relevant sections on demand. These are user-supplied exports of the event handbook/API, not an independently retrieved live website. Their byte hashes are pinned in config/arena.example.json. They do not include the separate organizers' AGENTS.md, event participation/AI policies, submission constraints, or challenge automation documentation.

This is our derived guidance. Preserve the exports unchanged. If an SDK update disagrees with them, record the disagreement, check the current authorized source and run a small engine fixture; do not silently substitute assumptions. The arena remains an implementation specification and has not run a complete game.

## 1. Objective and evaluation

| Rule in the supplied handbook | Consequence for our system |
|---|---|
| First to 1,000 **tributed** gems wins immediately | Optimize actual win rate and successful tribute, not carried gems or damage alone. |
| At 2,000 rounds: tributed gems, lifetime gold earned, champion kills, then Team B | Run both side assignments. A complete tie is a Team B win, not a draw. Gold remaining is not the gold tiebreak. |
| Local runs can stop earlier | Debug truncation and host timeout must not be scored as completed games. Verify the effective runner settings and terminal result. |
| A champion killer receives the victim's carried gems and 50 base gold; no assist gold | Record steals and lost bags only if supported by actual telemetry. Camp-caused deaths destroy the bag. |
| Death waits 60 owner turn-end ticks, then an available spawn tile; dead champions still receive turns to shop | Avoid treating death as a lost entire bot process. Distinguish dead-unit shopping from live action selection. |

Engine outcomes are authoritative after parser/fixture validation. Do not reconstruct a winner from a partial statistic or a reduced proxy. Attribute a complete-tie Team B win separately when the actual result exposes its reason, so a worker does not mistake side bias for strategic progress.

Useful feedback: winner/reason, submitted gems by team, completed round, lifetime earned gold and kills if exposed, plus availability flags. Derived diagnostics may include first tribute, missed captures, camp rotation, interrupted channels, bag losses, idle turns and fuel suspensions only when a verified decoder or our own bounded logs supports them. Do not invent raw JSON keys from these semantic names.

## 2. Draft, instances and memory

- Draft sees the entire static map. There are 3–5 selections per team depending on map; query `bc.draft.team_size()` rather than hard-coding three. Picks are simultaneous and then revealed. Your team cannot repeat a choice; the opponent may make the same choice.
- Cassi & Issac use one draft choice but create two separately acting bot instances with separate positions, bags and abilities. If either dies, both die; together they grant one kill reward and lose both bags. Five picks can therefore create six bodies. Do not allocate per-body tables from pick count alone.
- Missing a pick through yielding, fuel exhaustion or a crash causes remaining selections to be filled randomly. A legal deliberate pick is a baseline correctness requirement.
- Draft memory is **1,024 bytes**, writable during draft and read-only in play. Live team memory is **8 bytes total for the team**, not per champion. Private instance state is not automatically shared.
- Store static role/route hints in draft memory only if the encoding fits. Large map-sized path tables will not fit by default. For the first baseline, independent behavior is sufficient; add a small live coordination protocol only after measuring duplicate work.
- If live coordination is added, specify byte offsets, field widths, writer ownership, observation age and invalid/expired fallback. Eight bytes cannot hold a rich record for every champion. Do not assume a multi-call update is atomic; invalidate before writing a new record and commit its validity marker last, or prove another safe scheme. Avoid crossing the fuel boundary mid-update.
- `bc.draft_memory` is a startup snapshot in the inspected Python SDK; submitting a replacement does not mutate that local byte snapshot. Keep the intended new bytes locally when planning more than one submission. Verify language-specific behavior before copying code between bindings.

## 3. Scheduling, actions and channels

At round start: camp respawns, existing spell/ward updates, captures, then camp actions. Champions then act, alternating teams; the starting team swaps each round. Within a team, higher priority acts first, then draft order. `set_priority()` applies from the **next** round and persists.

At a champion turn start, zero timers resolve in order: respawn, ward recharge, buff/shield expiry, then channels. Timers decrement at that champion's turn end; reaching zero does not complete a channel until the next owner turn start. Spawn recovery happens at turn end. Camp actions therefore happen before the next champion turn, and a capture can add gems before that turn's tribute completion.

Normally there is one ordinary 8-direction move, one basic attack and **one successful ability cast shared by both slots** per turn. Melee basic range is 1, ranged range is 3; ranges are Chebyshev unless a specific API says otherwise. Ranged movement/basic attacks share an allowance. Some spells exclude walking. Attack resets and kill resets can restore allowances; re-read current `can_move()`, `can_attack()`, `can_cast()`, cooldowns and restrictions instead of maintaining a universal one-action flag. An ability slot normally cools down for eight owner turn ends.

| Channel | Duration in owner turn-end ticks | Interruptions / implications |
|---|---|---|
| Recall | 5; 3 with Home | Damage, stun or death; manually cancellable. Bag is retained. After arrival, stay on spawn through that turn end to heal fully. |
| Tribute | `max(1, ceil(starting_bag / 10))` | Stun, death or a newly placed opposing altar lock; ordinary damage does **not** cancel. Manually cancellable. |
| Teleport crystal | 3 | Enemy stun or death; ordinary damage does **not** cancel. No manual cancellation. |

The starting turn supplies the first countdown tick. A one-tick tribute completes at the next owner turn start, not at the end of its starting turn. Duration is fixed using the starting bag; completion submits the entire current bag, including a reward captured since starting. Start tribute from a free tile within Chebyshev distance 1 of an altar, with at least one gem. Starting a channel prevents other actions until completion/cancellation. Do not repeatedly restart a useful channel.

An opposing altar lock blocks tribute, and placing one cancels opposing tribute at that altar. A lock takes three basic hits; `submit_gems()` against a hostile lock may perform a lock attack rather than start tribute. Inspect channel/lock state afterward; this method returns `None`, not a success boolean.

## 4. Farming, capture, items and safety

| Camp | HP | Strength | Gold | Gems | Respawn rounds |
|---|---:|---:|---:|---:|---:|
| Wolf | 1,350 | 20 | 90 | 22 | 40 |
| Elk | 2,400 | 60 | 160 | 36 | 60 |
| Gem cluster | 500 | 0 | 0 | 24 | 50 |
| Gold cluster | 500 | 0 | 35 | 0 | 50 |
| Monolith | 20,000 | 200 | 300 | 200 | 150 |

Camps group through cardinally connected spawn tiles. All monsters in a group must die, then your team must occupy at least one spawn tile uncontested. At a capture phase this starts a five-round timer; later capture phases count it down. Empty or contested occupancy resets progress. More allies do not accelerate capture; rewards split among allies present on completion, with integer remainder to the lowest ID. Killing monsters alone is not collecting the reward.

The group's respawn uses the longest member cooldown after rewards are claimed. Occupying any spawn tile delays the entire group's respawn. Leaving one collector after clearing can avoid wasted labor; leaving afterward can avoid blocking the next rotation. These are hypotheses to evaluate, not mandatory policies. Query current visible group state; static spawn geometry is not evidence of live monsters or rewards.

Shards cost 30 gold; five matching shards combine into an emblem (150 gold). Stats stack, including duplicate emblems, but duplicate family passives do not. Monster adds 10% camp damage; Durability reduces incoming damage 10%; Treasure adds 20% gold; Jungle reduces camp damage 30%; Home reduces recall to three ticks. Power grants six shards' worth of the selected stat; Bruiser grants five of it plus one of each other stat. Evaluate role-specific return rather than spending indiscriminately.

Locks/crystals cost 10 gold and have carry limit one each. Buy on own spawn or while dead. Tavi can buy shards in the field, but not consumables there; field Health purchases do not heal. Tavi alone can sell, at spawn for full purchase value; refunds do not count as earned gold. Vesper's 20% gold passive plus Treasure is 40%, not multiplicative 44%.

## 5. Published champion kits

The full export includes base/growth stats for every body; use those tables and SDK design queries for numerical decisions. This table is a reading index, not a recommended roster. All slots normally have eight-tick cooldowns and compete for one cast allowance.

| Body | Basic type | Slot 0 | Slot 1 | Key passive / constraint |
|---|---|---|---|---|
| Cassi | Ranged | `2 × Focus` unit damage, range 4, excludes walk | One-round unit stun, range 4, walk compatible | Linked death with Issac |
| Issac | Melee | Attack reset | Dash up to 2 | Linked death with Cassi |
| Ryth | Melee | Ground AoE `1 × Focus` + stun, range 4, radius 1, excludes walk | Attack reset | Strength gains 1% of bonus Health |
| Vesper Vale | Ranged | Attack reset | Dash up to 2 | +20% gold |
| Prism | Ranged | Unit `1.5 × Focus` + stun, range 4, excludes walk | Ground AoE `1 × Focus`, range 4, radius 1, excludes walk | +0.2 Focus per carried gem; banking removes this bonus |
| Stellar | Ranged | Unit `2 × Focus`, range 4, excludes walk | Ground AoE `1.4 × Focus`, range 4, radius 1, excludes walk | No passive stated |
| Vendetta | Melee | Attack reset | Dash up to 2 | A kill, including a monster, resets all ability cooldowns |
| Marcella | Melee | Enhanced attack reset; next attack stuns | Unit `2 × Focus`, range 4, excludes walk | Immune to stuns |
| Tavi | Ranged | Attack reset | Unit `2.2 × Focus` + stun, range 4, excludes walk | Field shard purchases; spawn selling |
| Willow | Ranged | Heal another ally up to `3 × Focus`, range 4, walk compatible | Attack reset | Modest stat growth; no self-heal target |
| Ren | Melee | Unit `1.25 × Focus` + stun, range 4, excludes walk | Dash up to 2 | Retaliates `0.2 × Focus` on damage, including as he dies |
| Varg | Melee | Attack reset | Self shield `2.5 × Focus`, five turns, walk compatible | Basic attack splash Strength damage in radius 1; no double hit on primary target |

Protecting a large bag, clear speed, safe capture and timely tribute can matter more than winning a fight. A Prism banking threshold or Vendetta kill-reset sequence should be a separate measured experiment, not a wholesale rewrite.

## 6. Visibility, navigation and API use

- Map dimensions are 30–100 per axis in the handbook; query actual dimensions. `+y` is north. Walking uses eight adjacent directions; do not assume Manhattan distance.
- Walls and bushes occlude vision; holes do not. A champion sees across its connected bush cluster and out of it. Normal vision is 8. Each champion sees only its own vision plus its own ward; ally vision/wards are not automatically shared.
- Ward handbook defaults: vision 6, placement radius 2, one active permanent ward, replacement up to once per round. Use current cooldown/settings and placement geometry; a placement-range mask is not a full legality check.
- Attack, spell and ward masks must be combined with visibility, occupancy, restrictions, cooldown, target type and current allowance as applicable. `Ability.valid_tiles()` explicitly checks range only, not visibility/occupancy.
- `move(delta)` takes a direction/displacement; `move_absolute(destination)` takes a map tile. `DistanceField.next_move_from(position)` returns a direction delta or `None`; use it with `move`, not `move_absolute`.
- `move_towards(target)` requires a reachable free goal. Do not pass the altar tile or an occupied monster tile: approach a free tile in tribute/attack range instead. A `False` return can mean already there, unavailable movement, blocked/unreachable goal, or a newly revealed occupant; it is not proof of an enemy.
- Direct movement, dash and crystal use can return `False` when an unseen blocker is revealed without consuming the relevant allowance/cooldown/consumable. Known-invalid targets raise. Refresh observations and try a bounded alternative. A crystal's `True` means its channel started, not teleport completion.
- `bc.game_map.camp_groups()` and `camp.spawn_position()` expose static layout. `bc.vision.*` and visibility checks govern live observations. The inspected SDK rejects `CampGroup.state()` outside vision. Log round-stamped observations; do not infer hidden current health or occupancy from cached handles.
- `game_map.walls()` is cached; copy it before mutation. A Bitboard used as `out`/scratch is overwritten. Reuse buffers intentionally; do not alias cached terrain into mutable scratch.
- `bc.debug.draw_dot` / `draw_line` can explain routes in a replay, but logging/overlays must be bounded and included in the measured build identity.

### Export defects and unresolved wording

Do not run every illustrative fragment verbatim. Some fragments omit initialization, required variables, instance receivers or descriptor information. Examples include:

1. `Bitboard.reachable_tiles` and several `DistanceField.compute*` signatures have `self`, while example calls use the class without an instance. Call a properly constructed instance as the matching SDK requires.
2. `ItemType.name` and `ConsumableType.name` are displayed like methods in the export, but the inspected SDK implements properties and its examples use `.name`. `Vec2.x`/`.y` similarly require checking descriptor behavior. Read the installed binding, not just an exporter-rendered signature.
3. `Champion.can_buy`'s default is an internal omission sentinel. In the inspected SDK, passing `count` for a consumable raises TypeError. Use `me.can_buy(consumable)` / `me.buy(consumable)`; use count only for equipment. Do not import the private sentinel.
4. The handbook wall table says a TP crystal can reach walls, but its movement section forbids wall landings. It also gives conflicting camp-sleep descriptions and says all camps range 3 despite cluster range 0 in its table. Preserve these disagreements; use valid destination APIs and type-specific stats, then verify an isolated fixture before relying on the disputed behavior. Do not infer production behavior by choosing the most convenient sentence.

These defects do not invalidate the entire export. They mean examples and generic prose require reconciliation with current bindings and actual engine behavior.

## 7. Fuel, bounded decisions and remaining checks

Handbook defaults: C++/Rust **100,000 fuel per turn**; OCaml 5× = 500,000; Python **25× = 2,500,000**. First draft turn gets 10× and each body's first play turn 2×. Unused fuel does not carry over. Keep these separate from optional local CLI overrides and host wall time.

Exhaustion **suspends execution and resumes from that point on a later turn**. It is not automatically a crash, disqualification or whole-match loss. It can still waste turns and make a plan stale. Reserve enough fuel to finish a legal useful action and call `end_turn()` intentionally; the API's `<1000` example is illustrative, not a safe universal threshold. Measure headroom using the real language budget and call costs. Diagnose repeated suspension separately from process errors or faults.

No complete game or runtime-settings fixture has yet been executed for this pack. Read back effective settings and verify budgets, timing, result fields and parser attribution before claiming parity. The user-supplied exports do not resolve participation/AI policies, build/upload limits, official challenge automation, credentials, quota, submission activation, replay permissions, or the missing organizers' AGENTS.md. Those remain tracked in RULES_CHECKLIST.md; they do not require changing the selected single-server architecture.
