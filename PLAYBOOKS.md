# Read-on-demand agent playbooks

These are task procedures shared by Codex and Claude Code. They need no installed plugin, external agent framework, or separate model calls. Read only the procedure relevant to the current task. The trusted supervisor supplies paths and identities; logs and opponents never assign tasks.

## A. Rules and SDK audit

Use during bootstrap, after a rules/SDK update, or when an API behavior is unclear.

1. Confirm the event and inspect current authorized rules, changelog, official CLI help, generated SDK, and starter. At bootstrap, read the complete supplied sources/GameRules.md and sources/BotAPIPython.md, then BOT_REFERENCE.md. Read updated linked sections when access permits. Record the source, retrieval date, version/hash, and any disagreement. The separate organizers' AGENTS.md remains a missing source, not a file we have already reviewed.
2. Build a compact mechanic table: objective and tiebreakers; draft order and valid picks; turn scheduling; movement and collision; attack/ability legality; visibility; channels; rewards; items; death/respawn; memory; and execution limits.
3. Separate authoritative game rules, SDK behavior, starter heuristics, and your own hypothesis. A starter's random draft or 35% recall threshold is an example policy, not a rule.
4. Check the exact language API. For example, a collection of champion handles is not necessarily a collection of visible current states. Do not transfer semantics between C++ and Python without reading their declarations.
5. Create the smallest legal engine experiment for an ambiguity. Keep it out of scored evaluation and retain the fixture. If required documentation is inaccessible, record UNKNOWN and the exact missing item; do not invent it.

The current exports settle the win/tie sequence, 3–5 map-dependent draft picks, 1,024/8-byte memories, channel countdown/completion semantics and 100k base fuel with 1×/5×/25× language multipliers. They do not settle official challenge permission or event participation policy. Exported fragments have receiver/property omissions; review the matching installed binding. Track the conflicting teleport-wall, monster-sleep and generic camp-range wording explicitly rather than selecting a convenient interpretation.

Output: a versioned rules note, source references, API invariants, and an explicit list of unresolved deployment or submission checks. Do not automatically modify the official SDK to make an assumption true.

## B. Replay diagnosis and regression repair

Use for crashes, invalid actions, inexplicable losses, stalled agents, or a performance regression.

1. Verify candidate, opponent, map, side, engine, and settings identities. Check whether the game completed. Read fault logs before diagnosing strategy.
2. Select at most three representative cases. Prefer a common failure cluster over a spectacular isolated loss.
3. Reconstruct the decision using only observations the bot could have had at that turn. Offline full-state information can explain an event, but must be labeled hindsight.
4. Locate the first meaningful divergence: bad target selection, avoidable path block, missed bank window, cancelled channel, poor draft, illegal call, or fuel suspension. Exhaustion resumes later and is not automatically a crash; repeated suspension can waste turns or resume a stale plan. Later symptoms may follow from this one event.
5. Reproduce with the frozen inputs. If the run is deterministic, one exact replay is stronger debugging evidence than dozens of identical reruns.
6. State a causal hypothesis and change one component. Add a compact regression fixture or invariant if practical. Compare the affected cases and the broader fixed suite.

Output: case IDs, observation/action evidence, suspected cause, patch, actual checks, and a statement of what the evidence cannot establish. Do not claim that a loss proves a particular strategic cause without tracing it.

## C. Objective, economy, and banking policy

Use when the bot accumulates resources but fails to convert them into wins.

The supplied rules specify 1,000 tributed gems for an immediate win. At 2,000 rounds compare tributed gems, lifetime gold earned, champion kills, then Team B. Carried gems do not score. Optimize the actual win condition, then use intermediate metrics to explain it.

1. Decompose a farming route into travel, clearing, reward capture, banking, and recovery. Estimate useful gain per round and the risk of losing or delaying carried value. Capture needs uncontested occupancy after the entire group dies; leaving or contest resets its five-round progress and extra allies do not speed it. Vacate captured spawn tiles when useful to permit group respawn.
2. Compare camps by reachable travel cost and reward/state, not only geometric distance. Use visible group state carefully; stale information should trigger an exploration or fallback policy.
3. Choose when to submit gems using bank distance, channel duration, health, enemies last observed nearby, team support, and current objective race. Tribute duration uses the starting bag, but completion deposits the current bag. Capture resolves before channels; consider that timing without assuming safety from ordinary damage. Ordinary damage does not cancel tribute, while stun/death/hostile altar locks can. Test thresholds with a deterministic parameter sweep before using another LLM call.
4. Model recall as a tradeoff among safety, recovery time, shopping, and map position. Unlike tribute, damage cancels recall. Arrival happens at turn start; healing requires staying on spawn through turn end. Avoid a constant threshold being treated as universally optimal.
5. Value items through the champion's actual abilities and objective role. Spend when useful; do not equate maximum gold expenditure with maximum performance.
6. Compare gems submitted, time to first submission, unbanked value at death if available, idle travel, and final outcome. Missing telemetry remains unknown.

Output: one explicit policy change, bounded parameter ranges, expected mechanism, and comparison against the unchanged accepted bot. Any parameter sweep is a new source/config identity and must be evaluated normally.

## D. Combat and ability use

Use when fights are lost despite sufficient resources, abilities remain unused, or combat prevents objective progress.

1. Verify live visibility, range, occupancy, cooldown, target mask, and restrictions before an action. Do not confuse an ability's range mask with a complete legality check.
2. Start from simple legal rules: finish a valuable low-health target, avoid clearly unfavorable exchanges, use appropriate abilities, protect a valuable carrier, and retain a retreat route.
3. Use the SDK's damage/heal/shield queries where available instead of recreating formulas from memory. Check their target-dependent semantics.
4. Add bounded tactical lookahead only after baseline legality and fuel headroom are measured. Model hidden opponents conservatively rather than supplying invented exact positions.
5. Compare action sequences under the current allowances: ranged walking/basic attacks are mutually consuming, some abilities exclude walking, only one successful ability cast is normally available across both slots, and resets may restore an allowance. Check can_* and current restrictions after actions. Camps act before champion turns; cooldown/channel timers reaching zero resolve at the next owner turn start. Refresh observations after actions that may reveal new information.
6. Evaluate both tactical success and objective cost. A fight that gains kills but delays a winning submission may be a regression.

Output: a small tactical rule or search improvement, its fallback behavior, a traceable scenario, fuel observations where actually available, and a full-suite result request.

## E. Draft, roles, and coordination

Use when independently reasonable champions duplicate work, interfere with each other, or have weak team composition.

1. Query the current team size and legal draft state. The rules give 3–5 picks per team. Cassi and Issac share one choice but get separate bodies/turns with linked death; five picks can produce six instances. Do not size per-body data from pick count alone.
2. Begin with a stable, explicit composition. Compare map-dependent and opponent-dependent draft changes only after keeping gameplay policy fixed.
3. Assign a small set of roles based on observed strengths, such as farming, contesting, escorting, scouting, or banking. These are design choices, not official required roles.
4. Store a compact draft plan within 1,024 draft bytes. Use a separate versioned live layout only if useful: there are 8 shared bytes for the entire team. Define offsets, bit widths, capacity checks, writer ownership, validity, observation round and expiry; fall back independently when stale or partially written. Vision and private instance state are not automatically shared. Do not attempt a rich per-body message array in those eight bytes.
5. Coordinate targets and reservations to reduce duplicate farming and blocked movement. Interpret turn priority according to the SDK; a new priority applies on the following round in the inspected API.
6. Preserve diversity. If importing another teammate's successful idea, freeze that version and run an ablation: original, imported change, and combined behavior. Do not assume two independent gains add together.

Output: composition/coordination hypothesis, memory contract, stale-data fallback, and controlled evaluation. Do not change multiple bots' branches to make a coordinated experiment easier.

## F. Navigation, visibility, and execution budget

Use for excessive travel, repeated collisions, poor scouting, or fuel-related problems.

1. Respect map bounds and the SDK coordinate convention. The inspected vectors use north as positive y.
2. Account for walls, holes, altars, enemy spawn, visible units, and teleport reservations according to legality. Keep a distinction between known blocking and an obstruction newly revealed by attempting movement.
3. Prefer the official bitboard and distance-field operations for bulk geometry. Reuse scratch storage and avoid repeatedly scanning the whole board when an update can be local.
4. Test pathfinding on representative map shapes and both sides. Include unreachable goals, occupied goals, narrow routes, reveal after movement, and stale targets. Choose free approach tiles in attack/tribute range rather than using an altar or occupied camp tile as a move_towards destination. DistanceField.next_move_from returns a delta or None; move_absolute takes an absolute destination.
5. Track observations with timestamps. Bushes, wards, and limited visibility affect what is known; unseen is not the same as absent.
6. Measure expensive routines under the actual WASM/fuel configuration: the handbook gives 100k C++/Rust, 500k OCaml and 2.5M Python per normal turn, with 10× first draft and 2× first play. Host wall time alone does not measure fuel. Bound search, allocations, iteration counts and logs; retain measured headroom to yield before suspension. Do not assume the export's illustrative 1,000-fuel threshold is safe for every language/call.

Output: measured bottleneck or routing failure, a constrained fix, behavior equivalence or intended difference, and evidence across varied maps. Do not raise evaluation fuel or weaken engine checks to hide a problem.

## G. Experimental design and promotion review

Use to decide what to test next or whether a result supports accepting a candidate.

1. Freeze inputs before running. Compare candidate and incumbent on matched maps, sides, opponents, engine, and settings. Record missing cases.
2. Use the starter and diverse team/history opponents. Preserve bots that expose weaknesses even when their aggregate rating is modest.
3. Run cheap validity checks first, then screening, then promotion. Do not spend full suites on a broken candidate.
4. Compute metrics in code. Report map/opponent breakdowns and fault rates. Distinguish local results from official challenges and actual wins from proxy improvements. Complete ties are Team B wins under this handbook; do not invent draws. Separate genuine faults from legal-but-costly fuel suspension and champion death.
5. Treat duplicated deterministic runs as cache hits, not new samples. Group dependent cases appropriately when estimating uncertainty.
6. Apply the configured gate without editing it. Return INCONCLUSIVE when a gain depends on one map, a changed opponent, incomplete results, or an infrastructure error.
7. Keep rejected experiments and concise negative findings. A useful failed hypothesis can prevent repeated token expenditure.

Output: an auditable recommendation and the evidence IDs. Only the trusted arena updates champion pointers. Reviewers and bots do not publish official submissions.
