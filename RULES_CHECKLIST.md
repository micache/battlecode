# Required rules and platform verification

Updated 16 October 2026, Asia/Saigon. The complete supplied sources/GameRules.md and sources/BotAPIPython.md have now been read, including all included champion specifications and API examples. This ledger distinguishes a documented rule from an executed engine check. It is not a replacement ruleset. Record source/hash, version/date, and conclusion for each item in `docs/rules/verified.md`.

| Item | Current status | Required resolution |
|---|---|---|
| Event identity | Verified public site and CLI | Keep Autumn 2026 pinned |
| Official local runner | Verified CLI 2.1.6 interface | Finish toolchain installation and real-engine smoke games |
| Published maps | Metadata verified, nine maps | Download and hash immutable map bytes |
| Objective | Supplied handbook read: 1,000 tributed gems; 2,000 rounds; gems → lifetime earned gold → kills → Team B | Verify effective settings, parser mapping and complete-tie side attribution with a fixture |
| Draft | Supplied handbook/API read: 3–5 simultaneous unique team picks; Cassi/Issac one pick/two bodies | Verify map team size and deliberate picks in the first playable baseline |
| Turn scheduling | Full supplied phase/timer/priority descriptions read | Fixture for turn-end decrement, next-turn-start completion, next-round priority and captures before channels |
| Visibility and observations | Supplied vision/bush/ward rules and API read; no automatic allied vision | Verify runtime defaults and keep masks separate from full legality |
| Camps and rewards | Capture/split/respawn rules and camp values read | Test capture occupancy and reset; resolve conflicting sleep/range prose if behavior depends on it |
| Combat and champion abilities | Every included champion specification read; roster indexed in BOT_REFERENCE.md | Use current design data and test actions/allowances; do not assume exported fragments run verbatim |
| Items, consumables and shopping | Full supplied rules/API read, including stacking, Tavi and gold refunds | Verify can_buy invocation and actual shopping behavior in baseline |
| Death, recall and teleport | Full supplied channel/loss/recovery rules read | Fixture for damage interruption and spawn healing; resolve contradictory teleport-wall wording |
| Fuel and memory | Handbook: 100k base C++/Rust, 5× OCaml, 25× Python; 10× first draft, 2× first play; 1,024/8 bytes | Read back actual settings; classify fuel suspension separately from crash/forfeit |
| Sandbox/source constraints | Runner packaging interface inspected; full event source/runtime restrictions not supplied | Verify WASM memory, dependencies, file limits and production execution configuration |
| Organizers' AGENTS.md | Separate file not supplied; webpage inaccessible | Obtain through the normal site/export, hash and reconcile it; our AGENTS.md is an original project file |
| Packaging and dependencies | Bundle/build/submit interface verified | Verify source/file-size/dependency/language restrictions and build service behavior |
| AI-assisted development | Not verified | Read current event policy; seek clarification if it is silent or ambiguous |
| Team participation and sharing | Public team format only | Verify full eligibility, account/team and code-sharing restrictions |
| Match logs and data use | Local replay interface verified | Verify official replay access, private logs, visibility and reuse restrictions |
| Unranked challenges | User-reported UI entry point only | Confirm supported flow, scheduling rules and quotas |
| Automated official challenges | Not verified | Establish permitted supported integration before enabling |
| Official submission selection | Not verified | Confirm whether challenge selects an immutable submission or current active bot |
| Upload/activation effects | Not verified | Establish whether uploads alter ranked/tournament bot state |
| Opponent version identification | Not verified | Record exposed version or explicitly mark unknown |
| Platform authentication | CLI help says seven-day session | Verify renewal and supported automation credentials |
| Deadline/freeze semantics | Public schedule observed | Verify exact timestamp/timezone and submission freeze behavior for each event |

The docs application could not be loaded in this session, but the user supplied the two reviewed exports. Those resolve the gameplay/API reading gap; they do not resolve the remaining event-policy or platform-integration checks. An owner can provide the separate organizers' AGENTS.md and relevant current policy/platform exports through the normal site. Do not attempt to bypass access controls.

Use three readiness flags rather than one ambiguous “ready” flag:

- `private_arena_ready`: local runner, packaging, parser, attribution, and recovery validated.
- `competition_parity_verified`: current rules and production settings reviewed; local settings matched.
- `official_automation_verified`: official workflow, permission, authentication, quotas, and submission effects reviewed.

Private arena implementation may continue while external checks are pending. Official upload/challenge automation requires the latter two flags. A local win is not evidence that these checks passed.
