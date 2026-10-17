# Current experiment: task-fc527578bbbf42f5be88544f50e93a50

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD b5ff9f073c01c9bb68360ccaf257dc301a65b7af.
- Accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Six entry files match accepted Git contents and supplied file hashes. Unchanged
  docs and SDK hash verified in this task's -identity.json. No bootstrap review.
- Engine/SDK 2.1.6; suite historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest candidate was evaluated INCONCLUSIVE, not pending. Previous notes archived
  as task-3afe79d6edd04c12b15814296878cc69.md. Older interrupted work is already
  preserved and was not applied. Accepted Git snapshot remains outside this edit.

## One hypothesis: playbook C, finish capture before new fights
Prioritizing visible cleared camp groups over live-camp attacks and exploration,
then holding a spawn tile until collection, will increase mean collected gems
versus accepted source on matched development cases. Unchanged or decreased mean
collected gems falsifies this prediction. Compare tribute, deaths and outcomes
for opportunity cost; no improvement is claimed before evaluation.

## Evidence and focused change
- Evaluation b7053d9ac454dc46f479d1e9d96aa3efc6f5d6f3b19b87f264f0f13208d55053:
  source e34275aad6113db66be4569d8a5ad8b07117fb2636116df8522a586ad3223c3e,
  revision a58a804523bcb54ed1d781318143c403be6e9b44d746b817b3d94c745b9f38fb,
  commit equal to input HEAD; this is NOT the restored source edited here.
- Collision B loss 6328f7f536da56a4bdf5d40eb63badb58ec3129c7b60a292312191ea61f68389:
  collected 1056 vs 1144, submitted 814 vs 1012, deaths 39, round 1427.
- Collision B loss d24232c33b8f2e028007d01b2e01cc95d712180d396b9bbbfc91a455c5237763:
  collected 1144 vs 1166, submitted 858 vs 1012, deaths 35, round 1384.
  Both have zero faults on both sides. Supplied complete final-metric summaries
  saved in this task's -evidence.json. Optional final.json slice was truncated;
  no additional conclusions drawn from it. No engine/arena failure identified.
- These aggregates establish objective deficits, not missed capture frequency.
  Runtime traces, abandoned rewards and clear-to-capture delays remain unknown.
- Accepted source attacks any nearby camp before routing, then gives reward sites
  and live/hidden groups equal pathfinding priority. A nearer live camp can defer
  an already-cleared reward, despite clearing alone earning no capture reward.
- One farming selection change: scan each group's static spawns once; read state
  only when a spawn is currently visible; collect reward_available spawn goals.
  Hold if already on such a tile, otherwise try existing legal pathfinder first.
  Empty/unreachable/blocked reward goals fall back to ordinary attacks/navigation.
- No post-move live state is reused for an action; successful reward movement
  returns, failed movement falls back to refreshed vision for camp targeting.
- Respawning groups remain excluded, allowing departure after collection; hidden
  groups remain exploration goals without hidden state reads. No new persistent
  state, parameters or shared-memory layout. Dispatcher still always yields.
- GameRules.md 191-205: uncontested spawn occupancy starts a five-round capture;
  leaving resets it; extra allies do not accelerate it. SDK cambc.h 4300-4374:
  reward_available means all camps defeated; state requires visible spawn.
- Read compact reference, playbook C, relevant handbook and installed SDK sections,
  and RESEARCH.md. Separate organizers' AGENTS.md remains unavailable.

## Validation and uncertainty
- python3 experiments/alpha/check_capture_priority.py PASSED, exit 0; source safety
  and ordering invariants only. Report: this task's -source-check.json.
- git diff --check PASSED, exit 0.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; checked source
  de641864b31c9d6705aed5fdb4f9c7c9e5f1a4c643df09a614ba88324dce0f14.
  Local report: .agent/check-task-fc527578bbbf42f5be88544f50e93a50.json;
  preserved as this task's -bot-check.json. Trusted reference:
  check:task-fc527578bbbf42f5be88544f50e93a50:de641864b31c9d6705aed5fdb4f9c7c9e5f1a4c643df09a614ba88324dce0f14.
- Wrapper smoke IDs 1abe1f3bf1611ddf24ac1769e3b4ec31830736a5dc3140a6d84adaf9414b1970
  and 20890d81be38ca238303069a1efa55b2c4e1c5ba57c6a51cbc2178142c6e8db1.
  Smoke finals not inspected; IDs alone do not establish full-game completion.
- Accepted-relative source diff reviewed: only farming selection changes.
  Outcome READY_FOR_EVAL; no tournament evaluation, publication or submission.
- Risks: several allies may converge on the same reward; contested captures may
  draw champions into danger; holding sacrifices incidental monster damage.
  Fuel headroom and full-game capture benefit are unmeasured. The group scan now
  also runs before stationary attacks, but is not duplicated for fallback routing.
- Next: supervisor evaluates this exact checked source against accepted, comparing
  collected/submitted gems, deaths and outcomes. If income fails to improve,
  inspect clear-to-capture delays and duplicate collectors before further changes.
