# Operational summary

## task-382a14ecf8cd42cab6e8f6d3b27f92bd — end-to-end gem-return routing

Hypothesis: strict gem-source priority after 150 gold of cash/equipment, with
full collection-to-tribute rate ranking, improves matched wins and submitted
gems. No win gain, lower submissions, or increased deaths/faults/suspension
falsifies it. New candidate performance and mechanism coverage are unmeasured.
Decision, evidence and check artifacts: this task directory. Prior notes archived
through task-b117f31ca086427583ad098da9e76b71.

Identity: beta / bot/beta; input HEAD d42689eb877943df1c4b83c2613650b63249199c;
edit 50a0d7d5ecbd99c70536b4c71c54e404f2daa2b1 / source
6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
All six source files matched trusted edit blobs/per-file hashes before editing.
Prepared bot.cpp changes and absent recovery_policy.h are intentional relative
to HEAD. Prior task PUBLISHED/evaluated; no unpublished work awaits evaluation.
Accepted 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in trusted Git/snapshot.
No agents, commit, publication, official action or comparative evaluation run.

Latest f5b67475 evaluated d42689eb/72275bc2 (recovery), NOT current edit/new code.
Development 83W/29L, zero own faults; +0.0267857 vs edit on 56 side pairs.
Mean deaths 2.241071, bag loss 42.767857. Ambush only 1W/3L per side.
- Ambush A cfdfa2b70be19323169334e189a0fb3deee26ccf971bad95ea35ed16e16bc4bd:
  round 1069; 538:1008 submitted; no own deaths/bag loss/faults/suspension.
  Ryth earned 1504 and Marcella 1260 gold; each collected/submitted zero gems.
- Ambush B 405a38f861c545db74ea87e304c062371b46952b400b195866b3224b1d3cc719:
  round 1091; 696:1034 submitted; no own deaths/faults/suspension.
  Varg earned 1575 gold but collected zero gems; own team earned 6420.
- Opponent revisions unknown in summaries; no identity inferred from draft.
  Gold-loop mechanism is source-supported inference, not a turn trace.
- Contrasting latest aggregate wins: collision/corners/eight/swirl 4W/0L per
  side, individual win IDs unknown. Protect these in evaluation.
- ce3253a0 summary retained but exact source/side assignment unknown; not used
  as an attributed candidate win. Official alpha observations are uncontrolled
  older/different-source evidence and were not used as beta scores.

Frozen manifest f94b3422: inspected gamma ecbc8203/ff511c52 draft, economy,
banking and route code; alpha 82a14a04/6e362fd7 relevant combat/bank sections;
beta 7cab9b0f/fd5e2554 prior penalty. Gamma uses melee-first, reachable reward/time
routes, 0.12 gold valuation, no live Monoliths and each-bag banking. Adapt rate
normalization/safety, retain beta shortlist, add bank-leg cost and strict tier.
Arena sources do not establish private official opponents' behavior.

Current strategy: Varg/Tavi/Ryth/Vendetta/Marcella; Jungle Strength, Monster
Strength, Durability Health then Power Strength. Independent captures, each-bag
banking, full spawn healing, locks and guarded route dashes. Original edit-base
45% recovery remains. No live team-memory protocol.
New objective routing:
- Endowment = cash plus purchase cost of all four equipment lines, not lifetime
  earned gold. Tavi's spent field gold counts. Bootstrap boundary 150.
- Gem tier outranks gold-only tier in shortlist and final choice after bootstrap;
  gold stays fallback. Current target cannot cross tiers. Original final scoring
  remains before bootstrap; committed group is refreshed first within its tier.
- Full-trip cost: outbound geometry + HP/(Strength*1.12) + six capture phases
  + bank geometry + ceil(gems/10), divided by gems; commitment multiplier 0.85.
  Gold fallback divisor gold*0.12. Immutable yields/nearest altar geometry cached.
- Preserve occupied cleared capture before selection, including gold-only groups.
  Cache visible respawn deadlines; filter deadlines/retries before shortlist.
  Vacate captured regions on no-target turns. Max 12 group inspections, existing
  45k scan/18k planning reserves and native movement fallback retained.
- New rate omits retaliation: exclude whole live Monolith groups in objective
  mode, retaining visible cleared rewards. Bootstrap policy remains unchanged.
- objective_policy.h compiled fixtures test boundary, tiers, travel/clear/bank
  cost sensitivity, live/cleared Monolith eligibility and commitment discount.
Only bot.cpp, bot.h and new objective_policy.h differ from trusted edit source.

Risks: geometry underestimates terrain/hidden danger; clearing estimate omits
spells, incoming damage, healing, locks and contention. Strict gems can reduce
investment or concentrate allies. Boundaries/clear multiplier unmeasured.
Fuel headroom and action coverage unknown; shortlist can miss good groups.
No strategic gain claimed. Existing banking/channel/visibility limitations persist.
Negative findings retained: previous +40 gold penalty after 300 capital +0.044643
with regressions; full scheduler +0.041667 with interlock regression; cooldown
ablation +0.008929; combat rewrite -0.041667; healthy shopping/bank detours zero
gain; isolated draft/items/shield/harvest ideas have no established additive gain.

Engine 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
suite published-17-release-225-v1. Docs unchanged per handoff. Consulted compact
BOT_REFERENCE, RESEARCH, organizer record, Playbooks B/C/F/G, relevant C++ field
API and installed SDK group-state/cooldown/reward contracts. SDK SHA256
ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
Organizer hub does not certify all policies or production parity; absent ward::owner unused.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0 final source 4ba62e96fe958a8c342a85175e579584e5601238a398ae0a37a815627060c6a9.
Local report .agent/check-task-382a14ecf8cd42cab6e8f6d3b27f92bd.json;
exact-source check-report PASSED/0 saved in task directory. Earlier a4b84b4d
also passed but superseded; check-superseded.json retained. No source edits
following final check. Final smoke IDs 9dc0d4881b140a95cf7ad8fe05bd5582ab8de2a119fa220b2cd007b5440c1bf2
and f53bf709d352b3802b8f27ef684858a4e0d112186e0a601c405a9a666379ca12;
own stdout empty, export exit 0 (smoke-a/b.json). These are smoke checks, not
claims of completed competitive games or measured zero fuel suspension.
`git diff --check` PASSED/0, report diff-check.txt.

Next: supervisor evaluates exact checked source vs 50a0d7d5/6d66a77f across
matched maps, both sides and frozen opponents. Prioritize wins/submitted gems;
inspect previously zero-gem/high-gold farmers, deaths/bag loss/faults/suspension.
Protect existing wins; full champion promotion gate remains mandatory.
If this fails, inspect actual ambush gold routes and banking stalls before
another economy threshold change.
