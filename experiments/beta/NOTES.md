# Operational summary

## task-4acc026b087b4a278e69d874a032cb52 — bounded local harvest circuits

Hypothesis: healthy carriers can improve submitted-gem throughput and wins by
collecting a short, fully observed, non-damaging nearby group before returning to
an altar. This is an unmeasured source/rules deduction. Falsifier: matched wins
or bag conversion regress, deaths/stranded gems increase, or fuel suspension
increases. Decision, evidence identities and alternatives: this task's decision.md.

Identity verified on entry: beta, bot/beta, HEAD/input/edit
 d2d57274232ca7cead5bacf650d6f51fd5b3bc3d; edit source
7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
Clean entry working tree; trusted entry verifies accepted/edit snapshots.
Protected accepted champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 stays in Git.
Prior recovered contender has completed evaluation; no unpublished pending
candidate was found. Self-play pending games concern the already evaluated edit
source and were neither polled nor treated as a pending candidate experiment.

Baseline evidence: evaluation 8874fe2cae89ba66b875b2082e00e01e0257b80aaf09fa757c1c5f24f9cd0178,
INCONCLUSIVE full-nine-map report; development-only window 43W/5L, zero faults,
48 completed games of d2d57274/source 7daa9117. Lanes aggregate A/B 4W/0L each
contrasts collision A/B 3W/1L each. Collision losses
35a896c482526b964ff9dfbfa6d79461021f3494e7fb9d1106bf6311acc0a975 (beta A)
and 5f8eb6f279d9e66464f9c21f475bcede83dbbc40e6282fd8534579c5a3cc1595 (beta B)
versus alpha 6af1685b/source 87b9be45 had 13 and 9 beta deaths respectively.
Self-play corners loss
1ec0801d0d9c8709490ea3a3afe88f4add3494c28266ff9bdcb1681364cabd72,
beta B vs alpha 0b61a3d4/source 7a14708a, ended round 444 with no B champion
deaths in the final slices. No per-turn travel/capture attribution is available.
Broader self-play window: 12W/12L unique cells; repeated games not independent.
Older external official observations have different own revisions/unknown
opponents and do not provide controlled evidence for today's policy.

Frozen manifest 345bc0171ed5d4cb6d7d3c4b7ed1f44565f7a2aeb1570ee83fbebe4d25bea74c
inspected: gamma 1b34f42a/3ce565f6 ranks value/time, remembers observed respawns,
uses melee farmers and banks each bag. Alpha 6af1685b/87b9be45 uses random
roster/builds, nearest-camp unions, enemy-first combat, and banks each bag.
The new circuit policy differs from both; no private notes/state were accessed.

Current strategy retains the recovered contender's roster Varg/Tavi/Ryth/
Vendetta/Marcella; Jungle Strength, Monster Strength, Durability Health then
Power Strength; active kits; bounded group ranking; explicit capture; full
spawn recovery. Prior baseline notes and detailed audit remain in
 task-bc8c3246ad3449e39155d369ae07c9e0/decision.md and its Git revision.

Changes this invocation:
- Small healthy bags can top up only at positive-gem, fully observed groups
  with no living damaging camps, within radius 6 and estimated extra detour 6.
- Travel + health/Strength clearing estimate + capture + one turn must fit the
  remaining 24-round circuit budget. Hidden state never counts as safe/empty.
- Force banking at >=96 gems, <75% health, enemy within 8, immediate camp
  exposure, sufficient winning bag, or 34-round endgame reserve. Return stays
  committed until empty/death; an unproductive circuit immediately returns.
- Preserve a safe ongoing capture before incidental adjacent banking; threat
  and deadline gates override this hold, preventing contested capture stalls.
- Keep channel/recovery precedence, native free-goal navigation, scan reserves,
  bounded retries, final yield, and no live shared-memory writes. Reserve fuel
  before an additional bank path after a failed circuit route.
- circuit_policy.h contains pure policy plus thirteen compile-time regression
  cases: normal opportunity, unknown/damaging state, zero value, radius/detour/
  deadline limits, health/threat, large/winning bags, and endgame banking.

Engine 2.1.6 / lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation/SDK unchanged from recorded full audit.
Consulted current BOT_REFERENCE, RESEARCH, organizer record, Playbooks B/C/F,
relevant handbook channel/capture text and installed C++ settings/objective API.
Header SHA256 remains pinned by brief as 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Organizer page is a download hub; production parity remains unknown.

Checks actually run:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; final source
7a4e377b08086313f1a977afbf99e27c450f80d4a98215cb965f6973c9d21191.
Report .agent/check-task-4acc026b087b4a278e69d874a032cb52.json;
check:task-4acc026b087b4a278e69d874a032cb52:7a4e377b08086313f1a977afbf99e27c450f80d4a98215cb965f6973c9d21191.
Thirteen constexpr policy regressions compiled. Smoke IDs
f8f912f59a7645c6c3e66763a0ca66f8a619525f8dda72c74c0f537269429d31 and
ead4c04c797a28f432397f695e555da58e3b564d90efb45588a7654240556c1a.
Exact-source check-report confirmed PASSED, exit 0. Both approved own-side
stdout exports exited 0; details saved in this task's smoke-a.json/smoke-b.json.
An earlier preliminary check passed be51f8c3 before review found that capture
holding could bypass the deadline/threat gate. Moved forced-bank evaluation
before capture holding, then reran trusted checks for the final hash above.
`git diff --check` PASSED, exit 0. No source edits after final trusted check.
Smoke validity and compile-time bounds do not establish strategy improvement,
actual fuel headroom, complete tournament outcomes or official parity.

Risks: unseen enemies, geometric estimates across walls, larger/longer exposed
channels, missed opportunities outside the bounded scan, interrupted captures,
and additional planning fuel. No measured gain claimed. Earlier weak-camp-only,
shield-only and isolated draft/item experiments did not establish additive gains;
retain their negative findings. Broad risky batching and wholesale gamma routing
were rejected for this experiment.

Next: supervisor compares this exact checked source with d2d57274 on matched
maps, both sides and frozen opponents. Inspect wins, submitted/collected gems,
round, deaths, final bags and available suspension telemetry, especially corners
throughput and collision safety. Full champion gate remains separate.
