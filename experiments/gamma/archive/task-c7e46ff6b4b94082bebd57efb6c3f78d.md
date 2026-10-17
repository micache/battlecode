# Gamma operational notes

## task-c7e46ff6b4b94082bebd57efb6c3f78d — retreat after interrupted recall

- Identity: bot/gamma; input/HEAD e9704a214cdc159318c72bf8d0213dd082b8f702;
  accepted commit 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d, base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  All six edit-start files match handoff hashes and accepted Git blobs. Initial
  diff is the trusted restore, not unfinished work. Accepted source is preserved
  in Git and the trusted snapshot. Latest candidate has completed evaluation;
  older PAUSED infrastructure task had no source changes. No pending candidate.
  Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
  suite historical-panels-v1. Documentation unchanged; relevant bindings reviewed.
- Playbook C: recovery cost in the farming/banking route.
- Hypothesis: retaining stationary first recalls but stepping spawnward on retries
  after interruption should escape repeated damage-cancel loops while preserving
  the initial safe-recall route, reducing deaths and increasing submitted gems
  versus accepted source on matched development cases.
- Falsifiable policy prediction: first low-health recall in an episode attempts
  no move. After a successful initiation, an actionable low-health turn with no
  running channel and away from spawn attempts at most one spawnward move before
  restarting recall. Re-read position after moving; reaching spawn skips recall.
  A failed move still permits recall. Channels leave the flag alone. Death,
  arrival or recovery to at least the existing 35% threshold clears the flag.
  If matched deaths do not decrease and submitted gems do not increase versus
  accepted source, the expected benefit is unsupported; wins govern promotion.
- Source mechanism: accepted code unconditionally restarts recall without moving
  on every actionable low-health turn. Damage/stun cancels recall, so this loop
  can recur at one position. This is reproducible from source/rules, not a traced
  event in the supplied losses. GameRules.md 270-274, 369-375; matching C++ header
  3447-3448 and 3661-3665: active-channel query and checked, void recall method.
- Prior evidence: evaluation
  3f4ce1baf874f5d4285cbcc6a02256573ddacc61dbe6fc0231ca6af4fca131f2,
  INCONCLUSIVE / provisional-three-map-wiring, 20W/4L, matched delta 0.5416666667,
  zero faults/missing/unknown reliability. Evaluated unconditional-retreat source
  3ddcabd550a7198b7553379a78a11ce62ece141f30dbbb772b36ef8257d2f769,
  commit e9704a214cdc159318c72bf8d0213dd082b8f702, differs from edit-start/current.
  Collision A loss 3ec136b6335cdeb14cc350c052a00f22f22fcdcdb8137a63220b83a339e5e6b1:
  11 deaths, 858 vs 1012 submitted, round 1206, zero faults.
  Elkring A loss c3fc95ae46b74b7f6c4ed2f1817b27cdf990e8bb0d24c97b76a97799c4bbb087:
  12 deaths, 774 vs 1008 submitted, round 934, zero faults.
  These are strategic losses; they do not show interruption frequency or prove
  retreat caused the outcomes. Bounded provenance: recall-retry-evidence.json.
- Refinement rationale: prior movement-on-every-initiation was promising overall
  but safe first recalls can lose position unnecessarily. This experiment uses
  observed channel history to gate retreat. It does not repeat that exact policy
  or combine the independent spawn-healing experiment. No combat/draft/threshold/
  farming/build changes. One private bool per body; no shared-memory expansion.
- Source validation: `python3 experiments/gamma/check_recall_retry.py`, PASSED,
  exit 0; recall-retry-source-check.json. Verifies first/retry gating, reset
  lifetime, fresh position, fallback recall, preserved channels/yield, and only
  intended recovery edits versus accepted source. Source invariant only.
  `git diff --check`, PASSED, exit 0.
- Trusted check: `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`,
  PASSED, exit 0. Exact candidate source
  e43461817a5c4c96349f0b79c358e81ab909b7fd26421d3ea194e4b4f662d23c.
  Report: .agent/check-task-c7e46ff6b4b94082bebd57efb6c3f78d.json;
  reference check:task-c7e46ff6b4b94082bebd57efb6c3f78d:e43461817a5c4c96349f0b79c358e81ab909b7fd26421d3ea194e4b4f662d23c.
  Wrapper supplied two smoke match IDs; scores, completed-game status and fuel
  headroom are not supplied by this report. READY_FOR_EVAL, no measured gain.
- Uncertainty: delaying retreat until the first interruption may lose a turn;
  moving may approach another threat or fail to escape. Lack of current channel
  away from spawn is only an interruption inference, not damage attribution.
  Earlier beneficial outcomes may depend on unconditional first movement. Existing
  start-on-spawn healing omission is unchanged. Fuel headroom and strategic gain
  remain unknown. Organizer AGENTS.md remains absent; no runtime parity claim.
- Next: supervisor evaluates the exact checked candidate against accepted source
  on frozen development cases; compare the prior unconditional-retreat results
  descriptively without pooling different revisions/opponents as repeated trials.

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
