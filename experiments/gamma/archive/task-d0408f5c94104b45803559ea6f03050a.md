# Gamma operational notes

## task-d0408f5c94104b45803559ea6f03050a — recover immediate capture entry

- One refinement candidate. Branch bot/gamma, HEAD/input/edit commit
  ecbc8203fd2ef0696ef7784c8b39528bb182ad7b, base source
  ff511c52577a0f42c5e17329423aaa100b0317ddcaf037f8b2ba59b808061671.
  Initial worktree clean, trusted entry verified, six source files at edit base.
  Protected accepted champion: 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d.
- Prior task-9c55d0328faf44f1945faa1770eac277 was PAUSED, never published or
  evaluated. History attributes incomplete check to old evaluation backlog then
  ENOSPC, not bot failure; infrastructure fix c332df20361a5ad40834622baf2e54ce51f43d33.
  Exact-source prior check-report lookup returned unknown check, exit1. Original
  source, notes and supervisor checkpoint remain in that owner attempt. Inspected
  the patch before recovering it unchanged; no pending evaluation to poll.
  Both prior notes retained in archive/task-9c55d0328faf44f1945faa1770eac277.md
  and archive/task-cf1855961cf741329d7612ce37c0e3cb.md.
- Hypothesis: legal same-turn local capture entry after a final monster kill
  increases matched development win rate AND mean submitted gems versus ff511c52,
  without new bot faults. Non-increasing either metric or any new fault rejects
  it. Mechanism is an UNMEASURED rules/source deduction; no causal loss trace.

## Strategy and recovered change

- Keep Varg/Vendetta/Marcella/Ryth/Tavi draft; group value/travel/clear/capture
  scoring; bank every positive bag; hostile-lock attacks; 35% retreat, 98% spawn
  healing, 300-gold safe empty-bag recall. Jungle Strength, Monster Strength,
  one Durability Health, then Power Strength. Ten-gold route locks retained.
- Current base returns after every successful fight, including a final melee
  basic/reset kill with walking remaining. Capture starts only when a spawn is
  occupied at a capture phase; earlier entry can save one round each rotation.
- Track successful casts' movement exclusion in all four existing cast paths.
  Failure does not mark exclusion. After pre-movement farming combat, require
  alive self, remaining movement, no exclusive cast/movement restriction,
  >=30000 fuel, fresh visible reward state, and no ally already collecting.
- Intersect spawns with fresh vision, fresh occupancy and SDK locally reachable
  tiles. One ordinary move attempt, no new global search or second combat.
  Skip when already on the spawn region. False reveals an obstruction and ends
  this optional follow-through. Successful arrival may place an existing lock.
- Log at most three capture entries per private body instance. No shared-memory,
  fuel, draft, navigation, bank, recovery, item or combat-priority policy change.
  Source is identical to prior candidate c44b1194fe72c682d2f70e3f9ed206a518040fe909f18952a83718b03543b4a2.

## Evidence and limits

- Exact-base evaluation 1a898e7cd33630cb6034475a6a8f7beeb234f47dc7186fac6fa80e94110e76f2:
  114W/22L, zero faults, INCONCLUSIVE. Matched development-base delta +0.0892857
  over 56 paired cases is separate from protected champion comparison.
- Ambush A loss 46169b0b3c07969ecdaaf079e30dc16aa4d64b59d28ae87ae0549d0709cbe3ec:
  exact ff511c52, 960 vs1010 tribute, round935, eight deaths, one own suspension.
  Collision A loss 350aedb52aadcef0e0769f398a80fd46aaa1efb8c137de550ed8a34b8a13ee66:
  same source, 246 vs1002 tribute, round570, five deaths, zero suspensions.
  Both zero faults. Opponent revisions unknown in summaries. These finals do
  not prove that capture delay caused either loss. Compact recovered artifacts:
  capture-entry-matches.json, including contrasting exact-base Collision A smoke
  win 41c22e31 (1028 vs66, round716, zero faults/suspensions).
- Current frozen manifest SHA256 22a5e65a680916adbc2a1222a5f3372d2f824fe9bb263cfd618c8ec57d917975;
  verified all six file sets. Beta 7cab9b0f/fd5e2554 uses Varg/Tavi/Ryth, recovery,
  shields/dashes, survival items, route locks and a post-bootstrap gold penalty;
  its farming also returns after combat. Alpha 82a14a04/6e362fd7 uses random
  draft/Power stats, bounded combat, timed respawn rotation and altar preference.
  No macro cloning: capture follow-through remains an independent rules deduction.
- Prior target-aware combat, camp claims, threat-aware banking, protected transit
  and Ryth-for-Marcella draft were not selected into this base. Negative findings
  retained in archives; no repetition bundled into recovery.
- Routine unchanged-doc iteration: consulted BOT_REFERENCE, playbooks B/C/D/F/G,
  RESEARCH/organizer ledger, capture phase/action order, C++ movement/group-state
  export and installed SDK. Header SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264
  verified. Engine2.2.5/lock0cabb3c7; suite published-17-release-225-v1. Organizer
  download hub is not complete policy review; official production parity unknown.
  External observations concern another source/opponents and are not used as tests.

## Checks and next action

- python3 experiments/gamma/check_capture_entry.py: PASSED, exit0, report
  capture-entry-source-check.json. Nine source safety/isolation invariants only,
  not an engine simulation or competitive result. git diff --check PASSED, exit0.
- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json: PASSED,
  exit0, exact candidate c44b1194fe72c682d2f70e3f9ed206a518040fe909f18952a83718b03543b4a2.
  Report .agent/check-task-d0408f5c94104b45803559ea6f03050a.json.
  No source edited after validation launch. Smoke details: capture-entry-smoke.json.
- Both completed Collision smoke games (mapHash ebfcace1, build d7e29ae3) have
  zero faults/suspensions on both sides. A e9c9af0c: 1100 vs110 tribute, round715;
  B 240888b0: 1052 vs328, round865. Opponent revisions unknown in summaries.
  Own logs contain eight/nine successful follow-through markers, no bot errors,
  and sampled minimum fuel 11339/12031. Capped logs demonstrate execution, not
  a controlled one-round timing gain. Smoke wins are validity, not improvement.
- Risks: earlier occupancy can expose a farmer or change contest timing; allies
  outside local vision may also collect. Fuel guard/local-only work bounds cost,
  but smoke must check errors and actual headroom. One saved round may not win.
- Next: supervisor evaluates the checked exact source against ff511c52 on
  matched maps/sides/opponents under unchanged gates; compare
  wins, tribute, deaths, faults and fuel suspensions. Logs should confirm the
  follow-through executes; a controlled trace should verify capture phase timing.
  If no gain, investigate recovery/route exposure before changing combat again.
