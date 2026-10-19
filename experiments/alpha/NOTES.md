# Current experiment: task-5da9c09daeab4e33839a785c51b5c1a8

## Identity and status
- Alpha, bot/alpha; HEAD/input/edit commit 046f1c3a41fe746c65c0982d06062623200fa931.
  Base source 07022bad764ef37711c5afeddb10a434a0d5f9c5581e519f8bb575ced706fca2.
  All nine starting files matched trusted edit-start hashes; working tree was clean.
  Protected accepted champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e stays in Git.
- Prior task-758e6444 checkpoint patch is empty, notes are the same as base and
  final result is absent. Those supplied prior paths remain intact; no edits to
  recover. Latest published candidate has evaluated feedback; no pending candidate.
  Continuous self-play pending matches in the brief are separate ongoing coverage.
- Engine/SDK 2.2.5, lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
  suite published-17-release-225-v1. Documentation unchanged since task-59a846e1.
  Consulted compact reference, playbooks B/C/D/F/G, RESEARCH/organizer limits and
  targeted crystal/channel/movement API and matching installed header sections.
  Handbook 1000 tribute / 2000 rounds / absolute B final tiebreak remain applicable.
  Organizer page is a download hub; no new production/policy certification.
- Previous operational notes archived as task-59a846e1bfeb476f999d44d2266677a1-NOTES.md.

## One hypothesis
Using teleport crystals only for quiet, personally visible terrain shortcuts that
save at least channel duration plus three walking turns increases matched
development win rate over this edit base. Unchanged or lower win rate falsifies
this prediction. Earlier arrivals/tribute, collection and paired-win completion
rounds are mechanism diagnostics. This is an unmeasured rules/source deduction,
not a traced explanation of any supplied match loss.

## Evidence and decision
- Evaluation 130f31b3b08bd47cacbc735c483b463c53bee38b57854575fd15200b2e06cf44
  measures this exact edit source: 106W/30L overall, zero faults/missing/unknown;
  development-base matched delta +0.0535714 across 56 side-paired cases. Protected
  champion comparison +0.6470588 is separate; result remains INCONCLUSIVE.
- Ambush A loss d4c63b042b47f5bf760a2097114f5c8d29b303b2097e3294b91a3e7e97ae6424:
  round 882, own collection/tribute 918/846 vs 1326/1014, deaths 1 vs 4, faults 0.
  Ambush B loss 6ef846d2082efb5b6cfaeb8f99b8e909e40f32458463c46a19181909e2a6943c:
  round 966, own collection/tribute 870/750 vs 1200/1020, own deaths 0, faults 0.
  These support a remaining objective throughput deficit despite good survival;
  finals do not establish missed shortcuts, actual travel time or channel safety.
  Exact supplied final metrics saved in this task's decision JSON.
- Contrasting exact-source development map aggregates: elkring, fragment,
  pilgrimage and stampede each 8/8 wins. No per-turn win trace is claimed.
  Continuous self-play source revisions/opponents are separate, not pooled scores.
- Frozen manifest ffc1de857d326e21fab7a984945f035eb57d62799c62e83de25e25b5e4ea2f62:
  verified all files, inspected gamma ecbc8203 (ff511c52...) and beta 50a0d7d5
  (6d66a77f...). Melee farming, passives, capture deference/commitment, lock tools;
  beta has terrain-respecting two-step dashes. Neither inspected route uses crystals.
  Source inspection does not identify any unknown runtime opponent revision.
- Prior fixed draft/stat/items, banking/batching, capture priority/follow-through,
  arrival-aware cooldowns, focus-fire/AoE, economic resupply, travel dashes and
  group-first/ranked routing negative/deferred findings remain. No repeat here.
  Crystal crossings differ from dashes: ignore intervening terrain, and must save
  >=6 walking turns under the default channel instead of merely two route steps.

## Candidate policy
- route_teleport.h owns purchase, pure timing contracts and bounded route selection.
  Buy one ten-gold tp_crystal at spawn/while dead, after lock before base shopping.
- Reuse the existing objective distance field before walking. Keep only personally
  visible, free landings <=3 Chebyshev away that cannot be terrain-walked to within
  three steps. Origin and landing fields must be finite: no stranding in a region
  reachable only with our single crystal. Existing goals and route priorities stay.
- Require ceil(from/base_speed)-ceil(to/base_speed) >= SDK tp_crystal_time + 3.
  SDK duration, not a hard-coded timer, prices the channel. Normal handbook duration
  is three ticks; choose the greatest saving. Open-ground jumps are rejected.
- No visible damaging camp, including sleepers, may reach either endpoint. Visible
  enemy exclusion radius is max(4, basic range)+channel*base_move_speed; four covers
  published spell range. Hidden enemies, dashes, future CC/spells remain uncertainty.
- Entry reserve 45k fuel, scan/action reserve 28k; <=32 camps, <=6 enemies, <=49
  landing tiles; partial scans abort. Native local terrain reach mask plus existing
  route field only. No recursive planning, new shared bytes or enemy cache.
- One use attempt ends navigation even on False/reveal, preventing stale walking
  or postwalk fighting. Existing channel guard and exception-safe end_turn remain.
  Singleton routes retain native move_towards when shortcut planning is unavailable.
- Recovery, camp rotation, draft/stat RNG, combat, banking/locks and four-byte
  shared-round protocol retain the base policy. Buying crystals changes economy.

## Checks and uncertainty
- Nine embedded constexpr contracts cover exact channel+margin boundary, ordinary
  open-ground rejection, speed conversion, SDK duration changes, disconnected
  origin/destination and zero speed. Trusted build compiled these contracts.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0; exact source 0ef30884a3076a9a2750ff5d808e8c8bfa3d2e4851f5706df1b97ef6f1224fd6.
  Report .agent/check-task-5da9c09daeab4e33839a785c51b5c1a8.json, copied into
  experiments/alpha/task-5da9c09daeab4e33839a785c51b5c1a8-bot-check.json.
  Smoke IDs 0c51a0b62e6dcc56ab94c8769772f087a8d8a67a3f90d05b5a614ba1ac6514f5
  and 4a89bd45ef704afe56bbb9d43a9c2c1e03d835cd6a58c6152dbf3fe4b407342f.
  This summary establishes wrapper success; full game completion, shortcut branch
  coverage and normal-turn fuel headroom are not established by that summary.
- git diff --check PASSED, exit 0. Per-file hashes still match the checked source.
  READY_FOR_EVAL; no comparative tournament was invoked.
- Risks: extra ten gold delays shards, targets/occupancy can change during channel,
  dynamic blockers can inflate field savings even with terrain-only landing gate,
  visibility/threat conservatism can leave crystals unused, and normal-turn fuel
  headroom/shortcut branch coverage are not yet measured. No strength claim.
- Supervisor should evaluate the exact checked candidate against edit base and
  protected champion across maps/both sides. If wins do not improve, reject;
  inspect crystal usage, travel/tribute timing and gold opportunity cost before
  relaxing safety/saving gates. No agents, publication, commit/push or official action.
