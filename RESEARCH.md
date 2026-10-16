# Research record and limits

Initial online research: 15 October 2026 UTC / 16 October 2026 local time. Revised 16 October 2026, Asia/Saigon, after reading both user-supplied exports in full. Distinguish inspected evidence from recommendations in README.md. All supplied gameplay rules/API text was read; this pack does not certify that every event policy or the separate organizers' AGENTS.md was read.

## Access and verification record

| Source or action | Observed result | What it establishes |
|---|---|---|
| User's `/game/docs` URL | HTML application shell retrieved; application asset returned HTTP 403 with a missing signed-key/cookie message | Full protected documentation was not accessible in this session |
| User's unranked chooser URL | Application shell only | No verified challenge controls, API, quotas, or replay permissions |
| Public event page and published landing asset | Retrieved | Autumn 2026 event identity, public FAQ, format and schedule |
| Official distribution metadata | Retrieved successfully | Published CLI 2.1.6 and platform-specific binary hashes |
| Official map-pool metadata | Retrieved successfully | Nine current named maps and their hashes |
| PyPI cambc 2.1.6 Linux wheel | Downloaded and hashed | Wheel matches PyPI checksum; extracted binary matches contest distribution checksum |
| Official CLI help | Executed | Actual build/run/batch/bundle/login/submit interface |
| `cambc init --yes` in a disposable project | SDK and C++ starter generated; toolchain download failed with connection refused | Generated source is inspectable, but initialization/build was not completed |
| Generated SDK and starter | Inspected C++ declarations, Python public API/docs, constants, draft, map/vision APIs, starter control flow and RNG | Concrete bot programming interfaces; not the entire event ruleset |
| Supplied GameRules.md | Read all 792 lines, including every included champion specification | Published gameplay, numeric defaults, tie order, memory and fuel rules as represented by the supplied export |
| Supplied BotAPIPython.md | Read all 6,689 lines | Every signature, description and example in the supplied Python API export; some exporter defects were reconciled with the generated SDK |
| Separate organizers' AGENTS.md | Not supplied or accessed | Our project AGENTS.md is not the organizers' file |
| Game execution | Not run | No measured throughput, completed-match fixture, or verified final-statistics schema yet |
| Official submission/challenge | Not performed | No account or team state changed |

No authenticated browser session, account login, server rental, daemon deployment, repository push, or paid model request was performed for this design.

## Current engine evidence

| Item | Value |
|---|---|
| CLI version | `2.1.6` |
| Wheel | `cambc-2.1.6-py3-none-manylinux_2_28_x86_64.whl` |
| Wheel SHA-256 | `209370d22858e1404ee4c03b64d1b23abf3fc86f4efe78145fc1642b8bc451e0` |
| Extracted Linux x86-64 binary SHA-256 | `e2a641bab3c9ec3b80d595c2956e6dbb115959b039617efb14e554617bf0d08c` |
| Official distribution's Linux x86-64 binary hash | Same as the extracted binary |
| PyPI provenance repository | `cambattlecode/cambc2026a` |
| Provenance commit | `e6c61e1d9f6ec14952ec2052bae2b6e76fd286cb` |
| Generated project SDK version | `2.1.6` |

The provenance repository could not be retrieved publicly. Do not assume the arena can clone it. The distributed CLI is sufficient to bootstrap an official SDK project when its required toolchain downloads are reachable. A PyPI version pin alone is weaker than retaining the package and executable hashes.

The earlier public FAQ names C, C++, Rust and Python and mentions a 20× Python multiplier. The CLI lists cpp, rust, python and ocaml. The newly supplied handbook explicitly gives C++/Rust 100k, OCaml 5× and Python **25×**, resolving our default game-budget guidance in favor of the supplied current handbook. Actual runtime settings and build-service eligibility still need verification. Do not propagate the older 20× figure. Use the C++ starter as a default for a new baseline, or preserve an existing valid team language; do not force a rewrite merely to standardize it.

### Verified CLI features and implications

- `build --output` emits a compiled WASI artifact. Source and compiled identities must both be recorded.
- `run` has `--map`, `--out-dir`, `--rounds`, `--fuel`, `--view`, and `--statistics`. Final statistics require a completed game. A shorter round override may truncate a game; the flag alone does not establish completion. No public seed flag was listed.
- `run-batch` accepts a four-path text manifest and has concurrency and timeout options. It also advertises API-v1 compiled JSONL inputs, whose detailed schema still needs verification.
- `view` accepts `.repl26a` or a match directory. The local arena should preserve replay bundles rather than retaining only stdout.
- `maps pull` refreshes published maps while preserving custom/edited maps. Evaluation still needs an immutable pool snapshot.
- `bundle` packages bot source; `submit` uploads it. The help does not establish activation effects or unranked challenge selection.
- `login` says the platform session lasts seven days. This is separate from coding-provider authentication.

The literal help output is in evidence/cli-help.txt. Undocumented strings found inside a binary are not a supported integration contract; the design therefore does not depend on hidden runner commands or inferred JSON request fields.

### Current map pool

The nine names returned were: collision, corners, elkring, expanse, interlock, lanes, monolith, packs, and rows. Exact IDs and hashes are retained in evidence/map-pool.json. The design uses the observed pool size for evaluation-cost examples, not as a permanent assumption. Pool membership and map bytes can change.

## Game mechanics grounded in the generated SDK

The autumn SDK is a champion-based game. It exposes draft choices, neutral camps, gold/items, carried and submitted gems, altars and altar locks, visibility/wards, abilities, recall/teleport/submission channels, and shared team memory. It does not use the earlier game's harvesters and conveyors.

The SDK obtains game settings from the engine, including winning gems, maximum rounds, rewards, durations and memory capacities. The supplied handbook now establishes the documented target: first to 1,000 tributed gems wins; at 2,000 rounds compare tributed gems, lifetime gold earned, champion kills, then absolute Team B. A complete tie is not a draw. Effective local/production settings are not yet measured; do not conflate documented defaults with executed parity evidence.

There are 11 draft-choice enum entries and 12 physical champion-type entries in the inspected SDK. Cassi and Issac share a draft choice. This is not a license to hard-code a permanent roster; current eligibility and any later unlocks must be checked.

Public API details that affect implementation:

- Draft size and completed picks have official queries. The starter dispatches draft and champion logic separately and yields after each decision.
- Live hidden-unit queries can fail. Visibility, cached observations, and static design information must not be confused.
- Movement/cast helpers distinguish certain newly revealed obstructions from known-invalid actions. An action's geometric mask alone does not prove full legality.
- The API has separate channel states, so returning early while a useful channel continues may be correct.
- Team shared memory is distinct from the draft snapshot. In C++, assigning draft bytes submits them without changing the local startup snapshot; the SDK documents truncation/preservation behavior for writes of different lengths.
- The scheduling-priority setter affects the next round. North is positive y in the inspected vector API.
- Fuel can be queried. The C++ API documents increased budgets for the first draft turn and each champion's first turn; do not judge normal-turn headroom from initialization alone.
- The starter explicitly seeds its PRNG from game positions because WASI randomness is zero in matches. This motivates reproducible policy parameters and avoiding redundant identical trials.

SDK evidence paths after initialization: `sdk/cpp/cambc.h`, `sdk/python/_cambc.pyi`, `sdk/python/cambc/__init__.py`, `constants.py`, `draft.py`, `game_map.py`, `vision.py`, and `bots/starter-cpp/src/`. The full SDK is not duplicated in this design archive; regenerate it through the pinned official tool.

## Supplied handbook/API audit

Unchanged source copies are retained as sources/GameRules.md and sources/BotAPIPython.md. The exports identify event cambc2026a but do not specify an exact engine commit/export timestamp. The version 2.1.6 SDK comparison is therefore independent evidence, not proof that the exports are versioned to that exact binary.

| Export | SHA-256 |
|---|---|
| GameRules.md | `1c7fcf111d95b4734070f8f676cd50a48154feb0673de73a31c79845afa34732` |
| BotAPIPython.md | `3013fde86080e89ebf109357d4b8ca913babcb4592be542d92df0fadd542772f` |

Substantive guidance added after this audit:

- Shared team memory is 8 live bytes, versus 1,024 draft bytes; ally vision is not shared. Cassi/Issac's combined pick produces two bodies, so physical instance count can exceed draft size.
- Owner turn ends decrement timers; zero resolves at the next owner turn start. Captures resolve before champion channels. Tribute duration is based on the starting bag but completion deposits the entire current bag.
- Damage cancels recall but not tribute/teleport. Stay through spawn turn end to heal after recall. Capture needs uncontested occupancy; extra allies do not accelerate it and occupied spawn tiles delay group respawn.
- Fuel exhaustion is suspension/resumption, not automatically a crash. Normal base budgets, language multipliers, first-turn boosts and intentional yielding need distinct measurement from host wall time.
- Ranged movement/basic attacks share allowance, some spells exclude walking, and resets can restore allowances. One successful cast normally spans both slots.
- The export's examples sometimes omit instance receivers; properties are rendered like methods; consumable can_buy count handling requires reading the binding. move_towards needs a free destination, while a distance field yields a direction delta.

BOT_REFERENCE.md includes the complete derived operating guidance and a roster index. Disputed prose remains explicit: the teleport-wall table versus forbidden landings; two descriptions of monster sleep; generic all-camps range versus zero-range resource clusters. No engine fixture has resolved these disagreements. Do not silently treat one sentence as tested behavior.

Neither supplied export is the separate organizers' AGENTS.md. Neither establishes event eligibility, AI-assistance policy, sharing policy, upload constraints or official challenge automation permission. Those remain separate ledger items.

## Subscription findings

OpenAI documents remote device-code login, saved-auth reuse for `codex exec`, and a trusted-private automation path that preserves refreshed account credentials. These support an owner-operated persistent worker. They do not guarantee indefinite authentication or unlimited included usage. API authentication is a different billing path and is excluded here.

Anthropic documents subscription login, `claude setup-token` for script environments, and non-interactive `claude -p`. Current documentation says bare mode omits subscription OAuth credentials. Its credential guidance distinguishes an owner's use of unmodified Claude Code from offering a third-party service that intermediates users' subscription credentials. This design uses the former pattern, with separate owners and no proxy.

Both providers have plan-dependent usage limits. The user did not specify the Codex plan tiers or whether Max is 5x/20x, so a defensible numeric token budget or 24/7 inference guarantee cannot be calculated. Runtime limits/reset times and measured task costs should drive scheduling. Pacing, checkpointing, and waiting are part of the design.

## What remains unverified

The separate organizers' AGENTS.md; event policy on AI assistance and team code sharing; effective production settings and source/build constraints; the few contradictory gameplay passages; match outcome/statistics and replay schemas; actual host throughput; leaderboard contents; unranked automation permission/rate limits; official submission activation effects; exact challenge version pinning; and what opponent replay/log information is available. The documented win/tie sequence and fuel/memory defaults are now known from the supplied export, while runtime parity remains untested.

These unknowns are operationally different. Missing challenge access should not prevent private arena implementation. Missing authoritative execution settings prevents claiming evaluation parity. Missing final-statistics parsing prevents automatic promotion until a real fixture is verified.

## Primary sources

| ID | Source | Use |
|---|---|---|
| S1 | [Event home](https://2026a.battlecode.co.uk/) | Current event identity and public FAQ |
| S2 | [Game documentation](https://2026a.battlecode.co.uk/game/docs) | Website application inaccessible; supplied exports reviewed separately below |
| S3 | [Unranked chooser](https://2026a.battlecode.co.uk/game/matches?challenge=choose) | User-identified external-play entry point; controls unverified |
| S4 | [Official distribution metadata](https://2026a.battlecode.co.uk/api/v1/distribution) | Current executable version and hashes |
| S5 | [Official map pool](https://2026a.battlecode.co.uk/api/v1/maps/pool) | Map IDs and hashes |
| S6 | [cambc 2.1.6](https://pypi.org/project/cambc/2.1.6/) | Official-owner package, platform wheels and provenance |
| S7 | [Codex authentication](https://learn.chatgpt.com/docs/auth) | Remote login |
| S8 | [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) | Scripted invocation, structured output, permissions |
| S9 | [Codex account auth in private CI/CD](https://learn.chatgpt.com/docs/auth/ci-cd-auth) | Refresh persistence and copied-cache concurrency concerns |
| S10 | [Codex pricing and usage](https://learn.chatgpt.com/docs/pricing) | Plan-dependent limits, status, separate API billing |
| S11 | [Claude Code authentication](https://code.claude.com/docs/en/authentication) | Subscription login, token setup, credential precedence |
| S12 | [Claude Code headless mode](https://code.claude.com/docs/en/headless) | `-p`, output and permission handling, bare-mode behavior |
| S13 | [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) | Invocation options |
| S14 | [Claude Code Pro/Max](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan) | Shared subscription limits and billing-path separation |
| S15 | [Claude Code credential-use guidance](https://code.claude.com/docs/en/legal-and-compliance) | Official-client versus intermediated-service distinction |
| S16 | [Claude project instructions](https://code.claude.com/docs/en/memory) | AGENTS.md loading and CLAUDE.md import |
| S17 | [Supplied GameRules.md](sources/GameRules.md) | Complete supplied handbook and champion specifications read |
| S18 | [Supplied BotAPIPython.md](sources/BotAPIPython.md) | Complete supplied Python API export read |
| S19 | [Organizers' agents page](https://2026a.battlecode.co.uk/game/docs/agents) | Explicitly requested source; webpage inaccessible and separate markdown not supplied |

All resource sizing, scheduling cadence, evaluation stages, retention budgets, and promotion thresholds in this pack are proposed engineering choices. They are not organizer rules or measured performance claims. Recheck the live official sources when implementing; this is a dated research snapshot.
