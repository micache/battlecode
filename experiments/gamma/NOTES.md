# Gamma operational notes

## task-ce3692cbfe1f45ffab7f246b29e02f3b — distributed camp intents

- Exploration, one candidate. Branch bot/gamma; HEAD/input
  81434048685e159a41d861303ace6e27f99c4e71; actual edit commit
  1b34f42a5266051ee50bae4cf74197b99b1115cb, verified source
  3ce565f611a1dbd1c59f89c35c00bdb99cba8343eff243b8370017fbe64b1565.
  Initial source files matched frozen gamma hashes exactly; initial bot.cpp diff
  from HEAD is trusted preparation, not incomplete worker work. Protected champion
  1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains in Git. Latest experiment is
  evaluated, not pending; continuous self-play pending matches are separate.
- Hypothesis: expiring team target intents will reduce duplicate camp trips and
  increase matched mean collected AND submitted gems versus the edit base without
  new bot faults. Falsifier: either mean does not improve or faults appear. Wins
  and the unchanged promotion gate govern selection. Duplication is a SOURCE-
  GROUNDED, UNMEASURED mechanism; finals do not establish wasted travel/capture.
- Bottleneck: farmers use the same independent reward/time score; only a visible
  ally already occupying a CLEARED group reserves it. No coordination of distant
  targets or ongoing clears. Extra allies do not accelerate capture; each also
  needs a banking trip. A soft target penalty lets farmers spread work without
  forbidding cooperative clearing when alternatives cost substantially more.

## Candidate policy and memory contract

- Keep draft Varg/Vendetta/Marcella/Ryth/Tavi, Strength build, combat/reset/shield,
  capture occupancy, farming scores, all-bag banking, recall and healing from base.
- New camp_claims.h protocol v1: byte 0 = 0xD1; bytes 1..6 = one intent per actual
  BODY, ranked by immutable ally handle; byte 7 unused. No hidden ally state read.
  Both Cassi and Issac would get distinct slots. Unsupported >6 bodies or >63
  groups use independent farming; no truncated IDs or buffer overflow.
- Each owner exclusively writes its slot. One byte publishes complete group+clock:
  low six bits = canonical sorted group index+1, zero releases; top two = round
  modulo four. Header initialization is idempotent; unknown versions untouched.
  No rich unit state, observations, positions or draft messages are serialized.
- Every owner turn releases the old intent BEFORE dead/channel/stun/healing/
  banking/retreat branches. Only selected farming/capture republishes. Claims are
  hints, never treated as proof of an ally position or hidden camp state.
- Freshness requires modulo age <=1 AND private time since token change <=1.
  Unchanged abandoned tokens never revive on clock wrap. First observation of an
  old byte can look fresh for at most two observations; skipping a full heartbeat
  cycle may conservatively discard an active claim. Renewed changed tokens revive.
  Writes are single-byte host calls, with no multi-byte torn record to interpret.
- Camp score multiplier = 1 + 1.5 * fresh other claims, then existing 0.85 target
  hysteresis. Reservations are SOFT: help a claimed group when alternatives are
  much worse. Existing visible uncontested capture reservation and occupancy
  preservation take precedence. Static group handles are sorted for common IDs.
- Six observations and one six-byte read starting at offset 1
  per body turn, plus own release/publish. No searches added, normal fuel retained.
  Exact temporal/boundary assertions in the header compile with the real policy.

## Evidence and rejected alternatives

- Latest evaluated source f7d71d2cebfdbfc7b1214a888c1514ae33657003c43d52c3e5e7a17894ff6ac6
  is NOT today's edit base. Evaluation
  870d0ce3e3dee3d0dd40628e35d859427d6d046acaa6b129dfa44e1d881fb1ce:
  overall 45W/27L, INCONCLUSIVE; development 26W/22L, faults zero.
  Matched development delta vs actual edit base -0.0208333 on 24 side-paired cases.
  Previous threat-routing idea did not beat this base; retained in
  archive/task-f10f6850851a4b819ef515def204aab6.md, not reapplied.
- camp-claims-evidence.json saves supplied exact-base self-play finals, all vs
  beta d2d57274232ca7cead5bacf650d6f51fd5b3bc3d, zero faults on both sides:
  Interlock A 3e3cd7fe03e8848a724c5cb3a7478d676e4d7e0a4fb32e38f8a863014e807f3e:
  round 609 loss, 968 collected AND submitted vs 1010, five own deaths.
  Lanes A d36694ea34fad7710a893a7970a447abf89640d425d1b6f833b0628bb4422aaa:
  round 432 loss, 786 collected AND submitted vs 1010, one own death.
  Lanes B 759094967480eed1b72e4d10f0b0d23d2f333c77948c3bd195f5e0652b106962:
  round 447 loss, 948 collected / 912 submitted vs 1008, two own deaths.
  These motivate throughput exploration but do not prove duplicate targeting.
- Contrasting exact-base smoke wins already saved in smoke-evidence.json:
  A 4cae2e4e3ee2e0b28310eecc700849b9deb0164dfb981b15c98aa7b292193be0,
  1006 tribute at round 596; B
  437e20a563cc5112573c2e614895606deb42a3db7a0cb94100002b88ffadc2bf,
  1084 at round 640; both zero faults. Maps/opponent revisions UNKNOWN, so these
  are not controlled development contrasts. Supplied individual development
  examples are losses; aggregate wins are not evidence of their mechanisms.
- Frozen manifest 9d8e11bbbc803745d63e3fd2a46d7301afb4c7f23bdbc57bbd8958386f844aba.
  Alpha 5f73d078 (source ba646c6e...) adds opportunistic 10-gold altar locks and
  privately observed respawn rotation to enemy-first combat and spawn-union farming;
  it has no target intent protocol. Beta d2d57274 (source 7daa9117...) deliberately
  drafts melee farmers, uses Strength+durability, local ally proximity penalty and
  visible collector reservations, but cannot coordinate out-of-vision targets.
  The protocol addresses a shared source limitation without copying their policy.
- Rejected this task: another banking-risk tuning (latest measured regression),
  hard map sectors (could strand farmers behind terrain/cooldowns), hard exclusive
  claims (would prevent useful help), draft overhaul (isolated Varg change was
  inconclusive). Base accepted/rejected history stays in earlier archives.
- Unchanged docs/SDK per trusted handoff; consulted reference, playbooks C/E/F,
  research/organizer limits, shared-memory rules/API and pinned header contracts.
  Engine/SDK 2.1.6; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  No claim of production parity or complete event-policy review.

## Checks and next action

- `python3 experiments/gamma/check_harvest.py`: PASSED, exit 0;
  harvest-source-check.json. Existing visibility/action/capture/draft/geometry
  invariants retained; previous no-memory assertion replaced with confinement to
  the new protocol. Header temporal/boundary static_asserts compiled successfully.
- `bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json`:
  PASSED, exit 0, final source
  490fd85093ab5ce3b22a9f6f86fadffe719d2b03e9d37ea4062b0f28d0654e73.
  Report .agent/check-task-ce3692cbfe1f45ffab7f246b29e02f3b.json;
  check:task-ce3692cbfe1f45ffab7f246b29e02f3b:490fd85093ab5ce3b22a9f6f86fadffe719d2b03e9d37ea4062b0f28d0654e73.
  Exact-source check-report agrees. No source edits after trusted validation.
- camp-claims-smoke.json retains complete paged finals and own stdout:
  A a4d394a3eb2b2dc13cdbc79ec5961ee9ffcf4042fa2e6a85a284a3ed11153fca:
  completed teamA win, 1104 vs 430 tribute, round 718, both sides zero faults.
  B 1cd294c232fa621f34d58f15db2cf3838afde1a5da8b6ed96497862d49d10f76:
  completed teamB win, 1030 vs 176 tribute, round 554, both sides zero faults.
  Both own logs: zero bot-error, suspension and settings-mismatch markers.
  Lowest logged running fuel minima: A 9363, B 11928 before dispatcher yield.
  This is sampled smoke headroom, not a guarantee for every turn/map. Maps and
  opponent revisions UNKNOWN in exports; smoke wins do not measure superiority.
  Finals still report engineVersion 0.0.1; production parity remains unresolved.
- `git diff --check`: PASSED, exit 0.
- Risk: separated farmers lose cooperative clear speed or combat protection;
  stale hints can briefly penalize good camps; low-fuel scanning remains bounded
  but may still bias selection. No comparative gain measured in this invocation.
- Next: supervisor evaluates exact checked candidate vs edit base on matched
  maps/sides/opponents, inspects collected/submitted gems and wins, and applies
  the unchanged champion promotion gate. If unsupported, inspect bounded target
  traces before further coordination or penalty tuning.
