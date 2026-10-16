# Current experiment: task-1b0e5c1c51ef41f4a84bb0ef951cff7f

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD 4b6483b0e91df11262fb6d8b42ab2667778e1571.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK CLI 2.1.6; suite historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- HEAD and branch match envelope. Entry source matched accepted_snapshot/src
  exactly (diff -r exit 0); worker.py make_attempt restores accepted source.
- Preserved entry tracked delta in this task's -entry.patch. Prior NOTES archived
  as task-60546c3a86fa400bb632346db8815d8c.md before editing.
- Latest candidate 24f016d952f46c984bfb2eeff620bbfb78aa5a47a6b72d7893acbf616baeb79f
  completed evaluation INCONCLUSIVE; no pending candidate identified.

## One hypothesis: playbook D, unused attack resets while farming
After a successful basic hit on a surviving camp, cast one ready attack reset and
attempt one further legal basic attack. This should reduce camp clearing time and
increase collected gems relative to accepted source on paired development cases.
Falsifier: mean collected gems does not exceed accepted; also compare submitted
gems and outcomes to detect failure to convert any extra clearing into wins.
Source invariant: no reset without a successful first hit and visible living camp;
at most one cast and one extra attack per farming invocation. Recheck attack
allowance, visibility, health and range after casting. No reset on enemy attacks.

## Evidence and change
- Supplied evaluation e525c2d2f15f5b4d23774ef05a6f1d02f4c1a921e98c20ec650995eb28799f1b:
  candidate four wins/two losses, zero reported bot faults, three provisional maps.
  Candidate revision a1ebb71a3144494723f622be61da10ca05f071b5be0af966c9ae14144b12bcec,
  input commit above; opponent source equals base. This is not our new candidate.
- Corners B, 60f5b94e1c1c0035738a5bf80fe4ba22bec7b8e0e0c267b9b4b09c1f27b34a82:
  submitted 658 vs 1020, collected 838, deaths 17; terminal teamA, round 648.
  Ryth dealt 10335 camp damage, took 1300; Marcella dealt 7740, took 2280.
- Elkring A, e75cb9a38791770ab6434d597066d0f4cfbec4232911e35f500d2855be3e3109:
  submitted 792 vs 1026, collected 918, deaths 45; terminal teamB, round 1115.
  Ryth dealt 17817 camp damage, took 10160; Marcella dealt 22605, took 9130;
  Willow dealt 11786, took 8060. All three have attack resets in handbook/SDK.
- Complete final.json slices retrieved through arena-client only, saved as this
  task's -60f5b94e1c1c-final.json and -e75cb9a38791-final.json; feedback also saved.
  These are offline diagnostics, never runtime inputs. Final exporter labels
  engineVersion 0.0.1; do not equate that field with envelope CLI/SDK 2.1.6.
- Bounded Elkring A stdout slice showed shared-round logs, no action trace;
  actual missed reset counts, clearing times and causality remain unknown.
- Accepted source has no casts and returns immediately after a single camp hit.
  Added attack_camp_with_reset in bot.cpp at both pre/post-movement camp sites.
  Scans the SDK's two ability slots, accepts only a ready attack-reset kind,
  uses its untargeted cast, then the existing fresh attack legality helper.
- All source other than bot.cpp equals accepted snapshot. Entry bot.h restoration
  relative to HEAD is preserved. No item, draft, banking, recall or routing changes.
- GameRules.md 116 and published reset kits describe restored attack allowance.
  Matching C++ cambc.h ability.is_attack_reset/is_ready/use and ability_slots
  reviewed: is_ready includes live can_cast and cooldown. No cast range query
  is made on a range-less reset; second hit refreshes target observations.
- Export hashes match RESEARCH.md; compact reference/relevant rules and SDK read.
  Separate organizers' AGENTS.md remains unavailable.

## Validation and uncertainty
- python3 experiments/alpha/check_camp_reset.py PASSED, exit 0; report:
  experiments/alpha/task-1b0e5c1c51ef41f4a84bb0ef951cff7f-source-check.json.
  Checks exact delta from accepted, first-hit/survivor/readiness guards, bounded
  cast, both farming sites, fresh follow-up legality and retained official yield.
  These are source checks, not runtime or fuel measurements.
- git diff --check PASSED, exit 0 before trusted check.
- Trusted command: bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  FAILED, exit 1, BUILD_FAILED; no smoke matches ran. Checked source hash:
  67e149ef76461fc02aca4bbc6df04ee2234f19f6ea9176dcf47086c7d38ca0f5.
- Local report: .agent/check-task-1b0e5c1c51ef41f4a84bb0ef951cff7f.json;
  preserved under experiments/alpha with this task's -bot-check.json suffix.
- Trusted report reference (not opened directly):
  /srv/battlecode/checks/task-1b0e5c1c51ef41f4a84bb0ef951cff7f/67e149ef76461fc02aca4bbc6df04ee2234f19f6ea9176dcf47086c7d38ca0f5/report.json.
- Wrapper pointed to build diagnostics:
  /srv/battlecode/builds/7962c625cf4dab1209a1648154cfb23748788c0121e53901eb6465b002e989e1/output.
  file/rg access returned Permission denied. Stopped without permission changes,
  toolchain searches or another check. Compiler cause UNKNOWN; cannot distinguish
  bot compilation fault from build infrastructure failure with available output.
- Outcome BLOCKED. Preserve this source patch; it is not valid for evaluation.
  Supervisor must provide compiler diagnostics through an authorized worker-facing
  channel. No further experiment or source repair attempted after the denial.
- Risks: reset cooldown is spent on farming rather than later combat; changes to
  clearing timing can worsen captures/routes. No chaining onto another monster if
  first hit kills; no post-walk reset when ranged basic attack allowance is absent.
- No improvement claim. Capture timing, fuel headroom and exact reset use remain
  unknown until trustworthy runtime evidence. After diagnostics, repair and pass
  trusted checks before requesting evaluation. Next idea only after evaluation:
  inspect capture completion if extra camp damage fails to yield more gems.
