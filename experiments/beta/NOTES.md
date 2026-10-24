# Operational summary

## task-6eb24475a7c44d8ca4c35c078f960c06 — visible-contact survival

Identity: beta, bot/beta; HEAD/input df9fd0288ecd167dd55ca844da034580c58837ab.
Edit base 863825b744eb21ee366370c9b1919ce73210d9d4 / source
c9c933a21b50bd9e01ca1dfdaca7bd290b0259e8cd51bc7c59ad340853232c11.
Protected champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 unchanged.
All seven source files matched trusted edit-start hashes before edits. Prepared
changes relative to HEAD were edit-base restoration, not unfinished work.
Latest candidate already evaluated; no pending beta work. Identity artifact in
this task directory. Earlier notes/negative findings remain in Git and artifacts.

Hypothesis: bounded visible-contact withdrawal will increase matched wins and
mean tribute while reducing deaths over the edit base, without new faults or
fuel suspensions. Nonpositive win/tribute gains, unchanged/increased deaths, or
new reliability failures falsify it. Mechanism is a source-grounded deduction;
final statistics do not prove the cause of losses.

Evidence: latest evaluated df9fd028 / d9bfba26, evaluation 5e88fdea,
234W/166L INCONCLUSIVE; development-base delta +0.0054054, 185 paired cases.
Latest-candidate metrics must not be attributed to the c9c933a2 edit base or new candidate.
- 00ambush/A da7e69cd9b7b4bb66ac938fa1e483fd250de08d648bb4b9961b0d97fdf413610:
  completed round 1721, 500:1020 tribute, 551:1038 collection, 11:4 deaths,
  51 own bag loss, 14344.60 own champion damage taken vs 6143 dealt.
- 00ambush/B 096bd464d8ba0f61db763fea41bd9c0bd3b5baf4644bb5cb11f05ac745c0da52:
  completed round 1831, 621:1009 tribute, 794:1079 collection, 13:7 deaths,
  136 own bag loss, 20448.80 own champion damage taken vs 8552 dealt.
Both zero own faults/suspensions. Opponent revision unknown from summaries.
Contrasting edit-base smoke wins 9484a7a3/A and d4cff166/B completed with zero
own deaths, bag loss, faults and suspensions; useful reliability fixtures, not
proof of strength against the boss. Compact provenance/metrics in evidence.json.

Frozen manifest 090b0bb9, six sources. Inspected shared boss 4feab379 /
ea15ef0f / f4b4f65e draft, builds, support casts, skirmish and shop routines.
It favors Vendetta/Varg/Ryth, uses kit-specific Jungle/Monster builds, local
HP*Strength odds, 30-gem banks and spawn-directed withdrawal. Adapted its local
odds idea with explicit escape-step hazard scoring; retained our own controller.
Frozen source does not establish official-opponent behavior.

Changes from edit base:
- policy.h: contact radius 6, odds threshold 0.9, lethal pressure >=80% current
  health, conservative enemy range+1 reach, lexicographic escape ordering.
- bot.cpp: assess only visible living champions; nearby visible ally support is
  advisory. If losing and threatened, shield and choose a reachable free visible
  local step minimizing projected champion/awake-camp damage, then maximizing
  enemy separation, then reducing geometric spawn distance. No chase/dash/search.
- Escape hazard count capped at 32; 45k entry gate, 30k scan/action reserves,
  at most two move attempts with fresh blocker masks. Low budget/dense hazards
  defend in place. Refresh targets after movement/reveal for legal counterattacks;
  pass walked flag so exclusive spells cannot follow walking.
- Contact response precedes capture/farming/recovery movement; abandoned target
  excluded twelve rounds. Useful channels and spawn turn-end healing preserved.
- contact_test.h: sixteen compile-time cases for no-contact/spawn/favorable odds,
  losing odds/lethal pressure, melee/ranged reach and escape ordering.
- Existing draft, builds, bank thresholds, capture, navigation, recovery and
  intentional end_turn remain. All new state private; no shared-memory writes.

Validation: artifacts in experiments/beta/task-6eb24475a7c44d8ca4c35c078f960c06.
Exact command for all builds:
bot-check --owner-config /var/lib/battlecode-volume/config/beta.json
- Red FAILED/1, check-red.json, source 2a720de5: expected missing policy helpers.
- Intermediate PASSED/0, check-intermediate.json, source a183964a.
- Final PASSED/0, check-final.json, source
  b7375e5eedaab75ad145ae0c958deda1f0f21f7d79bad5a1f00ef9d2d9edd042.
  No source edits afterward; final-source-files.json records per-file hashes.
- Final smoke A a4c655656ee4ea35db143dfbaee3d351f9a4b106349bbd88d034e9dff40f49e2:
  COMPLETED own win round 1072, 1002:6 tribute, one own death, zero bag loss.
- Final smoke B bd06d00e9b14d1c193e4acacae7e390a29679cdbff8e17da485e265da64ae52f:
  COMPLETED own win round 1044, 1002:22 tribute, zero own deaths/bag loss.
Both zero own faults/suspensions. Same 41x41 map hash 6e3c6795, observed seed
17615240315955964814; map name/opponent revision unknown. No seed flag used.
Smoke timings 1072/1044 vs edit-base fixtures 1026/1033 show no speedup, and A
mortality worsened. These limited fixtures do not establish competitive gain.
Sparse first log slices contain no sampled evade stage; they do not measure
all contact decisions or all-turn minimum fuel. Full normalized summaries saved.
- git diff --check PASSED/0. Author self-review in review.md; no agents used.

Rules/SDK unchanged per handoff; header 894229e1 independently verified. Read
compact reference, relevant combat/economy/diagnostic playbooks and SDK/API
contracts; research/organizer ledger preserves policy/production-parity limits.
Rejected this cycle: further terrain ranking (latest inconclusive), kit/build
changes (separate scaling experiment), repeating kill-reset/capture changes.
Prior strict gold restrictions and draft-only changes retain negative findings.

Uncertainty: odds omit hidden enemies, spell readiness, shields and separating
walls; adjacent allies may not help. Ranged reach estimate is conservative.
Local escape can fail in corridors; new reveals may add threats absent from the
advisory snapshot. Retreat can reset captures or delay banks. Broad performance
and the proposed mortality reduction remain unmeasured; no strength claim.
Next: supervisor evaluates exact checked candidate against edit base/protected
champion and frozen opponents under unchanged gates; compare wins, tribute,
deaths, bag loss, collection and reliability, especially boss contact maps.
No commits, pushes, agents, official actions, comparative evaluation or polling.
