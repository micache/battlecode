# Gamma operational notes

## task-d0c7e96901174e80a58874326056fe19 — retreat from observed attack range

- Identity: bot/gamma; HEAD/input 2aa847284d093b82e68f565e8b74e21e62acdf04.
  Edit start: accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d;
  base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  All six initial source files match accepted Git blobs and trusted file hashes.
  Initial diff was the trusted restore. Accepted source remains in Git and the
  trusted external snapshot. Latest candidate evaluated; no pending source work.
  Prior notes archived by task ID. Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Documentation/header hashes unchanged and verified.
- Playbook C: recall/recovery cost in the farming/banking route.
- Hypothesis: taking one spawnward step before low-health recall only when a
  visible living enemy or camp has us in basic-attack range should avoid repeated
  damage cancellations while retaining stationary recalls outside observed attack
  ranges, reducing deaths and increasing submitted gems versus accepted source.
- Falsifiable prediction: at the unchanged 35% recall threshold away from spawn,
  inspect only visible living units' current attack masks. With no mask covering
  our position, recall without moving. Otherwise attempt one spawnward move,
  refresh position, and recall unless already on spawn. Failed/unavailable moves
  still fall through to recall. Ongoing channels are preserved by the existing
  early guard. No history flags, thresholds or shared-memory changes.
  Matched development deaths must decrease and submitted gems increase to support
  the proposed benefit; wins still govern promotion. No strategic result yet.
- Mechanism: accepted source restarts recall at the same position even within a
  monster's attack range. Damage interrupts recall (GameRules.md 270-274, 369-375).
  Matching C++ cambc.h 2938-2956: attack_tiles is a Chebyshev range mask, not attack
  availability; hidden live state can throw. Explicit is_visible precedes health
  and attack_tiles. This is a source/rules scenario, not a traced loss event.
- Development context: evaluation
  5b361c70c13d014c511552bcf8594544be08fb30cdb4464480a80904fda0966a,
  INCONCLUSIVE / provisional-three-map-wiring, 8W/16L, no faults/missing/unknown.
  Evaluated tribute-arrival source
  207a94cfd490b8d4d4d2b2029a01cd4dbcfa485156868465f1eb60e39f96edae
  at input commit differs from this edit start. Collision B loss
  08eb5c59e2352aca13ea6346a8d6f569133cc392233b65a5c79b54f49adea5ff:
  35 deaths, 902 collected, 660 submitted vs 1012, round 1311, zero faults.
  Collision A loss
  36a0c409f9ec24ed89adec379ddb944a48a57ad4eaf51809497dd52e82406853:
  19 deaths, 484 collected, 352 submitted vs 1012, round 880, zero faults.
  These are strategic losses; totals do not attribute deaths or recall failures.
  Saved bounded feedback/provenance: recall-threat-evidence.json.
- Refinement rationale: unconditional retreat source 3ddcabd5... scored 20W/4L,
  delta 0.5416666667 (evaluation 3f4ce1ba...); retry-only source e4346181...
  scored 15W/9L, delta 0.4166666667 (evaluation cee2f976...). Both INCONCLUSIVE
  with provisional coverage. This tests current geometric exposure rather than
  unconditionally moving or waiting for an inferred first interruption. It is a
  new gate, not a repeat of either policy. Different revisions are not pooled.
- Change limited to low-health recovery branch in bot.cpp. Current visibility
  gates all new live queries; loops stop at the first observed range overlap.
  Existing movement helper supplies legal steps and refreshes position afterward.
- Verification: identity/documentation/patch-scope checks PASSED, exit 0;
  recall-threat-source-check.json. Only the recovery branch differs from accepted;
  other five source files unchanged. No simulated engine fixture was run.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact candidate source
  f89c3f951116f0908f9170c310996bde0e8077ce892748efc11d8cc1ed12400c.
  Report: .agent/check-task-d0c7e96901174e80a58874326056fe19.json;
  reference check:task-d0c7e96901174e80a58874326056fe19:f89c3f951116f0908f9170c310996bde0e8077ce892748efc11d8cc1ed12400c.
  Two smoke match IDs supplied; scores, completed-game status and fuel headroom
  are not supplied. `git diff --check` PASSED, exit 0. READY_FOR_EVAL means a
  checked candidate, not a measured gain.
- Uncertainty: range overlap does not prove a camp is awake or an enemy will
  attack. Spells, hidden enemies and future movement are not predicted. A step
  may retain exposure or approach another threat; safe channels may still be
  interrupted. Additional queries cost fuel; headroom is unknown. Existing spawn
  healing omission persists. Separate organizer AGENTS.md remains unavailable.
- Next: supervisor evaluates the exact checked candidate against accepted source
  on frozen development cases. If unsupported, obtain bounded recall/threat traces
  before another recovery-policy refinement.

## Bootstrap documentation review (2026-10-17)

Read the complete supplied GameRules.md, BotAPIPython.md, BOT_REFERENCE.md and
matching installed C++ cambc.h/imports.h; also RESEARCH.md and playbooks A/C.
Supplied documentation and header hashes match the trusted handoff:

| Source | SHA-256 |
| --- | --- |
| GameRules.md | `1c7fcf111d95b4734070f8f676cd50a48154feb0673de73a31c79845afa34732` |
| BotAPIPython.md | `3013fde86080e89ebf109357d4b8ca913babcb4592be542d92df0fadd542772f` |
| BOT_REFERENCE.md | `7d483da98c0360a9c9b186f46f9aa4408539c7c4be96682791f30b9d65c3829f` |
| C++ cambc.h (2.1.6) | `90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d` |

Reviewed profile: 1,000 tributed gems wins; at 2,000 rounds use tribute, lifetime
earned gold, champion kills, then B. SDK settings are engine-loaded, not evidence
that every executed suite uses handbook defaults. Draft has 3–5 picks; Cassi/Issac
have two bodies. Live memory is 8 team bytes; draft memory 1,024. Visibility gates
live state. Captures require uncontested occupancy; channels resolve at owner
turn start after their zero timer. Damage interrupts recall, not tribute/teleport.
Normal C++ fuel is 100k; exhaustion suspends execution. No fuel override added.
The separate organizers' AGENTS.md remains unavailable. Export example defects,
teleport-wall, monster-sleep and generic camp-range wording remain unresolved as
documented in BOT_REFERENCE.md; this experiment does not depend on those disputes.
