# Gamma operational notes

## task-37a2c7761ec24fbc83a0b91519f80cb4 — tribute on arrival

- Identity: bot/gamma; input/HEAD 09b4f9d1c26f8700a8a7c7017e4977e79e013abb.
  Edit start: accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d;
  base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  All six source hashes and accepted Git blobs match the handoff. Initial diff
  is the trusted restore. Accepted source remains in Git and trusted snapshot.
  Latest candidate evaluated; no pending or incomplete source work to recover.
  Previous notes archived by task ID. Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Documentation unchanged; targeted API review only.
- Playbook C: reduce the banking leg's avoidable delay.
- Hypothesis: starting tribute on the turn movement reaches an unlocked altar
  approach removes one idle pre-channel turn per successful approach, increasing
  submitted gems versus accepted source without introducing bot faults.
- Falsifiable policy prediction: only after successful banking movement, refresh
  position and lock observations; if within the SDK tribute range of an unlocked
  altar, start tribute once and return. A failed move, out-of-range arrival or
  locked altar starts no channel. Existing adjacent submission, recall, combat
  priority, ongoing channels and route remain unchanged. No new policy threshold.
  Expected matched development result: higher mean submitted gems and zero new
  faults; equal/lower submitted gems fails to support the objective benefit.
  Wins govern promotion; no tournament result has been measured for this source.
- Source reproducer: accepted banking branch unconditionally returns after
  move_towards_closest(goals), even when the refreshed position is in altar range.
  Tribute ticks at starting turn end, so waiting delays completion by one owner
  turn absent intervening events. GameRules.md 116, 219-231; C++ cambc.h 3690-3694:
  submit_gems is a checked void action, not a boolean or a basic attack.
- Motivation: latest evaluated recall-retry source
  e43461817a5c4c96349f0b79c358e81ab909b7fd26421d3ea194e4b4f662d23c,
  commit 09b4f9d1c26f8700a8a7c7017e4977e79e013abb, differs from edit start.
  Evaluation cee2f9767e9104640561ae0baa81ebce5f8374bf56e86c26005313d6821fe9ac:
  INCONCLUSIVE, provisional-three-map-wiring, 15W/9L, no faults/missing/unknown.
  Collision A loss a503289405677a32258a2a2ae57be0c8ba509c79b4bce5129222eae667159d0e:
  902 collected, 792 submitted, 66 carried, four body deaths, round 1324.
  Collision B loss 472aa71bd07294f66a66c362fcb054fd00efb7d00eb29d0399902786a6a210d9:
  990 collected, 880 submitted, zero carried, 12 body deaths, round 1151.
  Both sides have zero faults. Strategic losses, not engine failures; final
  totals do not attribute delays or prove this mechanism caused either loss.
  Saved bounded supplied metrics and provenance: tribute-arrival-evidence.json.
- Refinement: distinct from prior combat-before-banking reorder and recall work.
  This tests only the gap between arrival and starting tribute on accepted code.
- Source validation: `python3 experiments/gamma/check_tribute_arrival.py`, PASSED,
  exit 0; tribute-arrival-source-check.json. Verifies refreshed position/locks,
  successful-move gating, one submission then return, and all other source tokens
  preserved versus accepted. First test run failed only because its comparison
  retained comment whitespace; fixed checker normalization, with bot unchanged.
  `git diff --check`, PASSED, exit 0. These are source checks, not engine fixtures.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact candidate source
  207a94cfd490b8d4d4d2b2029a01cd4dbcfa485156868465f1eb60e39f96edae.
  Report: .agent/check-task-37a2c7761ec24fbc83a0b91519f80cb4.json;
  reference check:task-37a2c7761ec24fbc83a0b91519f80cb4:207a94cfd490b8d4d4d2b2029a01cd4dbcfa485156868465f1eb60e39f96edae.
  Two smoke match IDs supplied; scores, completed-game status and fuel headroom
  are not supplied. READY_FOR_EVAL means checked candidate, not measured gain.
- Uncertainty: no per-turn tribute trace or fuel telemetry. Earlier commitment
  can expose the channel to a new lock/stun, and earlier bag timing may change
  later captures. No claim of gain or runtime parity. Organizer AGENTS.md absent.
- Next: supervisor evaluates the exact checked source against accepted source on
  frozen development cases. If unsupported, inspect route/lock blockage evidence.

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
