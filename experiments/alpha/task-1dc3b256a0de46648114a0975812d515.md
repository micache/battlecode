# Current experiment: task-1dc3b256a0de46648114a0975812d515

## Identity and recovery
- Bot alpha; branch bot/alpha; input HEAD 4b6483b0e91df11262fb6d8b42ab2667778e1571.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Entry branch/HEAD and all six accepted file hashes match the trusted handoff.
  Owned source is intentionally restored to accepted, not HEAD. Preserved entry
  diff and accepted files under this task's -entry.patch / -accepted-* names.
- Latest published candidate 24f016d952f46c984bfb2eeff620bbfb78aa5a47a6b72d7893acbf616baeb79f
  completed evaluation INCONCLUSIVE; no candidate awaiting evaluation identified.
- Read/preserved exact notes, result and checkpoint patch for prior blocked task
  task-1b0e5c1c51ef41f4a84bb0ef951cff7f and interrupted task
  task-d64d418366c1460d8577433cfbaf6b8d (its final result is absent).
  Copies use -recovered-* names; entry NOTES archived by its experiment ID.
- Recover only the most recent camp-reset experiment. The interrupted spawn-heal
  experiment remains archived, without combining behaviors.

## One hypothesis: playbook D, unused camp attack resets
After a basic hit on a surviving visible camp, using at most one ready attack
reset and one further legal basic attack will improve clearing and increase mean
collected gems against accepted source on paired development cases. Falsifier:
mean collected gems does not increase. Compare submitted gems and outcomes too.
Invariant: require the successful first hit, a visible living survivor and cast
readiness; recheck attack availability, visibility, health and range after casting.
No reset on champion attacks and no chaining to another camp after a kill.

## Evidence and implementation
- Evaluation e525c2d2f15f5b4d23774ef05a6f1d02f4c1a921e98c20ec650995eb28799f1b
  evaluated source 24f016d952f46c984bfb2eeff620bbfb78aa5a47a6b72d7893acbf616baeb79f,
  revision a1ebb71a3144494723f622be61da10ca05f071b5be0af966c9ae14144b12bcec,
  commit equal to input HEAD, against opponent source equal to base. It reported
  four wins/two losses, zero faults, provisional-three-map-wiring coverage.
- Corners B: 60f5b94e1c1c0035738a5bf80fe4ba22bec7b8e0e0c267b9b4b09c1f27b34a82,
  terminal teamA round 648; submitted 658 vs 1020. Ryth/Marcella camp damage
  10335/7740 and damage taken 1300/2280, respectively.
- Elkring A: e75cb9a38791770ab6434d597066d0f4cfbec4232911e35f500d2855be3e3109,
  terminal teamB round 1115; submitted 792 vs 1026. Ryth/Marcella/Willow camp
  damage 17817/22605/11786, damage taken 10160/9130/8060.
- Complete final.json obtained in bounded arena-client slices and saved as this
  task's -corners-final.json / -elkring-final.json. Both report zero bot faults.
  These hindsight statistics are never runtime inputs. Their engineVersion 0.0.1
  field is distinct from the trusted envelope's CLI/SDK version 2.1.6.
- Accepted source never casts and returns after one camp hit. Statistics motivate
  testing clear speed but do not establish missed-reset counts or causal losses.
- New recovery rationale: prior source 67e149ef76461fc02aca4bbc6df04ee2234f19f6ea9176dcf47086c7d38ca0f5
  failed BUILD_FAILED before smoke; historical diagnostics were unavailable.
  Installed cambc.h declares ability_slots private (3368) and exposes public
  abilities() (3602). Prior patch incorrectly accessed the private member.
  This is a source-proven compilation defect; historical compiler text is unknown.
- Recover the same bounded helper at both camp attack sites, replacing private
  member access with abilities(). Keep all other accepted source byte-identical.
  No item, draft, routing, banking, recall, memory or fuel-limit changes.
- SDK is_ready() checks cooldown and current can_cast; reset use() is untargeted.
  GameRules.md 116 and published kits specify restored basic attack allowance.
- Handoff flagged documentation changed/unrecorded: read both complete exports,
  BOT_REFERENCE.md and installed C++ cambc.h; hashes match handoff. Consulted
  playbook D and RESEARCH.md evidence limits. SDK header SHA-256
  90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
  Separate organizers' AGENTS.md remains unavailable and unreviewed.

## Validation and uncertainty
- python3 experiments/alpha/check_camp_reset.py PASSED, exit 0; saved report
  task-1dc3b256a0de46648114a0975812d515-source-check.json. Checks first hit,
  visible survivor/readiness, public accessor, bounded reset, fresh second-hit
  legality, both farming sites, exact accepted-source delta and retained yield.
  These are source invariants, not runtime/fuel measurements.
- git diff --check PASSED, exit 0.
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0. Exact checked source:
  3b7a9a65316fc22332da1e1b23910b91e6edea765ddd570beb2a60e4d8882377.
- Local report: .agent/check-task-1dc3b256a0de46648114a0975812d515.json;
  also preserved as this task's -bot-check.json. Trusted reference:
  check:task-1dc3b256a0de46648114a0975812d515:3b7a9a65316fc22332da1e1b23910b91e6edea765ddd570beb2a60e4d8882377.
- Wrapper smoke IDs bf0d8b0295c2129f6923add8a7205565729560815da9c69fceab8267ad42247d
  and 4c97b1033ca6b7cce13f049226547614b21b1832430c8269502228ea97f1e8ca.
  Finals not inspected; IDs alone do not prove full-game completion or gains.
- Saved this task's -identity.json records accepted-source, SDK and doc hashes.
- Existing entry bot.h restoration and Focus item are differences from HEAD;
  the only behavioral delta from accepted is camp-reset use.
- No improvement claim. Runtime reset use, fuel headroom and clear times are
  unknown. Spending resets on camps can weaken later combat or alter routes.
  Capture timing may dominate whether more damage yields more collected gems.
- Outcome READY_FOR_EVAL. Supervisor evaluates this exact checked source
  against accepted. Next idea only after evaluation: inspect capture completion
  if extra camp damage fails to improve collection. No publication performed.
