# Gamma operational notes

## task-ccebe4f09a07468fb85c1ff4ff3feb92 — target-aware combat economy

- One refinement candidate. Branch bot/gamma; HEAD/input
  db8b69148809f2d7872142d5e5bdffdf071f7c32. Actual edit commit
  1b34f42a5266051ee50bae4cf74197b99b1115cb, source
  3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565.
  All six initial source files matched frozen gamma SHA256s. Prepared bot.h/
  bot.cpp changes and deletion of camp_claims.h restore this base; they were not
  incomplete worker edits. Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d
  remains in Git. No evaluation of the latest candidate was pending.
- Hypothesis: refreshing targets after actions and ranking useful reset/direct/
  area damage will increase matched mean collected AND submitted gems versus
  this edit base without new bot faults. Either mean failing to increase or new
  faults falsifies the throughput claim. Wins and the promotion gate govern
  acceptance. This is a SOURCE-GROUNDED, UNMEASURED mechanism, not a replay finding.
- Bottleneck: base fight returns if its original target dies after the basic,
  stranding a potentially usable cast; it also selects any ready reset before
  comparing direct/area damage. Ryth can prefer one extra Strength hit over a
  multi-target Focus spell. Varg aims at lowest HP without valuing splash coverage.
- Chosen policy: group-scoped combat selection and observation refresh. Rejected
  another camp-claim/coordination penalty or banking-risk adjustment because the
  latest experiments regressed against this base. Durability/health investment
  remains a separate experiment; do not conflate its effect with combat selection.

## Policy, bounds and safety

- Retain Varg/Vendetta/Marcella/Ryth/Tavi draft, Jungle+Monster Strength then Power
  Strength build, reachable camp value/time scoring, 0.85 target hysteresis,
  capture occupancy and respawn observations, all-bag banking, recall and healing.
  No shared-memory writes, allied hidden vision, draft changes or fuel overrides.
- Combat considers only the selected physical camp group, or visible defensive
  champions in basic range satisfying the old adjacent/cheap-finish eligibility.
  It does not chase. Low-fuel farming keeps its eight-camp fallback.
- At most four decision steps and twelve candidate inspections per step; stop
  optional combat work below 18k fuel. Visibility precedes live HP/position reads.
  Rebuild observations after each basic/cast; inspect actual can_attack/can_cast,
  restrictions and cooldowns rather than assuming a kill restored allowances.
  Vendetta's cooldown reset is not assumed to grant an extra cast allowance.
- Spend a ready basic first. Compare subsequent reset damage with direct damage
  and area damage summed over observed targets. Cap each contribution at HP;
  finishing bonus = 0.25 * Strength. Estimate basics using Strength plus a single
  Monster passive; ability.damage_amount() supplies engine caster scaling.
- Varg basic scoring sums radius-one splash including the primary exactly once.
  Ground spells aim only at observed target tiles. No exhaustive tile search.
  Scores approximate shield/mitigation effects and omit targets beyond the cap;
  they are estimates, never assertions about hidden state or exact outcomes.
- Preserve Varg's below-75%-HP shield preference against nearby damaging targets;
  do not replace an active shield. Self resets never query a rangeless target mask.
  Reset + refreshed legal basic complete together, even at the loop boundary.
  Exclusive spells are forbidden after walking; no walking after combat, even
  if an ability killed the group's last monster. Dispatcher still always yields.

## Evidence and retained negative findings

- combat-evidence.json saves current source deductions, frozen source identities,
  selected exact-base finals and the current development comparison.
- Latest evaluated camp-claim source 490fd85093ab5ce3b22a9f6f86fadffe719d2b03e9d37ea4062b0f28d0654e73
  at db8b6914 is NOT this edit base or candidate. Evaluation
  3d64e64e7554fd39566226269de41f297d4cbc4ece281f716afa3252f2a56a82:
  20W/28L, zero faults; matched development delta vs edit base -0.1458333,
  24 side-paired cases. Previous threat-routing experiment also failed to improve
  the edit base. Prior notes archived as task-ce3692cbfe1f45ffab7f246b29e02f3b.md.
- That later source lost Collision A ec73ece3885f2c648cddb220e63a06a8bb50fed24d64a4457e588fe94f2761d4:
  188 tribute vs 1002, 12 deaths, round 543; Collision B
  967695d195aa8e4b3e17549bcf5c53934104d303d22d9754bd8eb2882faa99ec:
  400 vs 1028, 10 deaths, round 667. These are strategic losses without faults;
  finals cannot establish the per-turn cause or this candidate's performance.
- Exact-base loss contrasts retained in camp-claims-evidence.json, vs beta
  d2d57274232ca7cead5bacf650d6f51fd5b3bc3d: Interlock A
  3e3cd7fe03e8848a724c5cb3a7478d676e4d7e0a4fb32e38f8a863014e807f3e,
  968 tribute vs 1010 at round 609; Lanes A
  d36694ea34fad7710a893a7970a447abf89640d425d1b6f833b0628bb4422aaa,
  786 vs 1010 at round 432. Contrasting exact-base smoke wins in smoke-evidence.json:
  A 4cae2e4e3ee2e0b28310eecc700849b9deb0164dfb981b15c98aa7b292193be0,
  1006 at round 596; B 437e20a563cc5112573c2e614895606deb42a3db7a0cb94100002b88ffadc2bf,
  1084 at round 640. Their maps/opponent revisions are UNKNOWN, not controlled cases.
- Frozen manifest SHA256 d6be412acd64b3a56d605621ef0d3cea3aa0bb693087c1b59cb6574b85e508bd:
  alpha 5f73d078 ranks useful direct/reset damage, refreshes after casts, and uses
  locks/private respawn observations with enemy-first combat/spawn-union farming.
  Beta d2d57274 drafts melee farmers plus Tavi, buys durability Health after farming
  Strength, ranks AoE/reset damage but retains one target across its initial basic.
  Transfer: bounded spell-value comparison fits gamma's farming composition;
  preserve gamma's objective-first macro and add group-specific refresh/splash aim.
- Unchanged docs/SDK per trusted handoff. Consulted compact reference, playbooks
  C/D/F, relevant handbook abilities/items and installed C++ ability/unit contracts;
  research and organizer evidence limits retained. Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.

## Validation and next action

- `python3 experiments/gamma/check_harvest.py`: PASSED, exit 0;
  harvest-source-check.json. Existing geometry/draft/channel/visibility safeguards
  plus combat bounds/scope/control-flow assertions. These are source invariants,
  not engine simulation. Updated obsolete claim-protocol assertions for this base.
- combat_value.h static_asserts exercise the exact scoring kernel: capped overkill,
  dead/zero-damage targets, Varg middle-target splash without primary duplication,
  multi-target Ryth AoE beating a reset, and high Strength reversing the lone-target
  ordering. Compiled by the trusted wrapper with the real bot.
- `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`:
  PASSED, exit 0, exact final source
  f857236953b7f785b46f7f465b429635fbf07f961a43e1012b280aede2f970d7.
  Report .agent/check-task-ccebe4f09a07468fb85c1ff4ff3feb92.json;
  check:task-ccebe4f09a07468fb85c1ff4ff3feb92:f857236953b7f785b46f7f465b429635fbf07f961a43e1012b280aede2f970d7.
  Exact-source check-report agrees. No bot source edits after this validation.
- combat-smoke.json saves complete paged finals and own stdout. A
  3e3f8d8cb70145c7fbb0617c005cd75860bd724ebd7cc909ddb10734b9a6e8dc:
  completed teamA win, 1020 vs 502 tribute, round 702. B
  c9a180adb81bf271f5c2e8f80a5e534cb398ff9a703beda800c7a62a79b5629e:
  completed teamB win, 1026 vs 242, round 638. Both sides zero faults in both games;
  own logs have zero bot-error/suspension/settings-mismatch markers. Lowest logged
  running fuel minima: A 15847, B 15325 before dispatcher yield; sampled headroom,
  not an all-map guarantee. Maps/opponent revisions UNKNOWN. Smoke validity only,
  no comparative strength claim. Finals still report engineVersion 0.0.1, so
  production parity remains unresolved.
- `git diff --check`: PASSED, exit 0.
- Risks: approximate values can overrate shielded targets, larger groups are capped,
  extra scans cost fuel, and damage-maximizing aims may delay a useful kill.
- Next: supervisor evaluates this exact source against the edit base on matched
  maps/sides/opponents; compare collected/submitted gems, deaths, faults and wins,
  then apply the unchanged champion promotion gate. If unsupported, inspect bounded
  ability-choice/target traces before changing damage weights or the item build.
