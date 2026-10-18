# Operational summary

## task-bc8c3246ad3449e39155d369ae07c9e0 — recover integrated farming contender

Hypothesis: a deliberate farming roster with active combat kits, useful item
passives, explicit group capture and complete recovery will increase collected
and submitted gems while reducing deaths against development base 6450f600.
Falsifier: no objective/win gain in matched development games, or losses from
recovery cost, routing collisions or fuel suspension. This is an unmeasured
rules/source deduction. Decision/audit: this task's decision.md.

Identity: beta; bot/beta; task as above. HEAD/input
7773859f872f54d846088226ef1cf7b855cbb0a6; edit commit
6450f60028bac2047cddd8cb8be0710823d583d3; base hash
0c8c6de101ec85fcad250ef308157891de39e173751780d4e7b117285a73e5a1.
Entry verifies edit and accepted source; all six owned files matched edit Git
blobs on entry. Initial bot.cpp difference from HEAD was trusted preparation.
Accepted champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains protected
in Git/snapshot. No commit, branch change, publication or evaluation invoked.

Recovery: prior task-8fbe93005e2745df8b10d8b9da49fea8 was PAUSED, unpublished,
after optional smoke stdout export denial; not awaiting evaluation. Its exact
own source, notes, final result and checkpoint patch were inspected. Trusted
history says the access gate is repaired. Restored its reviewed bot.cpp, bot.h
and draft.cpp, with unchanged main dispatch/catch/yield. All six source files
now byte-match that candidate; fresh check below confirms the same source hash.
Old attempt, patch and notes remain untouched. Prior HEAD operational notes,
including negative findings, are archived in this task's prior-notes.md.

Evidence context: evaluation 7f75f3277bf710ea352706ce5476e1d1fc7523dc6ae95894f656b8fb3475e921
was INCONCLUSIVE, 6W/18L, zero reported faults, for shield commit 7773859f /
source bc3f6f13, not today's edit base or recovered candidate. Its collision
losses eec2f650cdda93c83d40994ccd012e1f4067b4690eca97290a46c0e073dd9702
(side B) and fdedefd480b828e41cf97462ac1c8f3ef1a7253dcda78e7f0430eafea47b0848
(side A) motivate throughput/survival investigation, not a causal claim.
Self-play 16W/68L likewise evaluates bc3f6f13; repeated executions are not
independent evidence. External older unknown-opponent results are uncontrolled.

Current frozen manifest fa8fcec025d810dc27b754a72cb02ae5af01b08e29d3a53ac7c217ca70fa25d2
was inspected. Gamma e9704a21 / 3ddcabd5 walks before recall; alpha 6af1685b /
87b9be45 uses separate basic and combat spell allowances; alpha 2e82fe18 /
eee9346f adds opportunistic altar locks. They retain random draft/build and
nearest-camp routes. Candidate keeps retreat progress and legal lock clearing,
while composing its own farming, capture and recovery policy. No private state
or official opponent code was read. Full source findings are in decision.md.

Engine 2.1.6, lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Bootstrap/changed-doc audit used current knowledge
GameRules, C++ export, BOT_REFERENCE, RESEARCH, organizer record, ledger and
Playbooks A/C/D/E/F. Matching installed cambc.h SHA256 verified:
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Newer exported camp wake/state, positions_into and debug_block APIs are absent
from the pinned header and unused. Objective is 1,000 tributed gems; 2,000-round
ties compare tributed gems, lifetime gold, kills, then Team B. Organizer page is
a download hub, not a separate policy review. Production parity remains unknown.

Recovered policy:
- Roster Varg, Tavi, Ryth, Vendetta, Marcella, with legal fallbacks. Team-size
  query and own-pick exclusion support map-dependent draft. No draft data needed.
- Complete Jungle Strength, Monster Strength, Durability Health once each, then
  Power Strength. can_buy supports dead shopping and Tavi's field exception.
- Basics plus shield/reset/unit damage/CC/ground AoE; refresh live target state,
  attack allowance and caster survival after actions. Skip exclusive spells
  after movement; one successful cast, legal follow-up reset attack.
- Cache static groups; rank travel, workload and gems with soft visible allied
  congestion. Commitment bonus 12; inspect at most 12 groups, stop scans at 45k
  fuel, reserve 18k before moving, retry failed routes after 12 rounds. Native
  free-root fields and at most two movement attempts; refresh vision after move.
- Hold own cleared camp occupancy through capture; skip rewards with another
  visible collector and visibly respawning groups. No hidden live state queries.
- Bank every bag before unrelated fights; friendly locks permit submission,
  hostile locks use the SDK's tribute-to-lock-attack fallback. Preserve channels.
- Retreat at 45% health, walk before safe recall, continue recovery to full on
  spawn. Safe empty-bag shopping recall at >=150 gold and <80% health.
- No live shared-memory writes, shared-round spam or random priority changes.

Checks actually run:
`python3 experiments/beta/task-bc8c3246ad3449e39155d369ae07c9e0/check_invariants.py`
PASSED, exit 0; report this task's invariants.txt. Covers channel/spawn/capture
preservation, dead shopping, visibility, free roots, bounded retries, movement
exclusions and reset guards; rejects seven unsafe source mutations. Not a game
simulation or measurement of actual fuel use.
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0, source
7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
Report .agent/check-task-bc8c3246ad3449e39155d369ae07c9e0.json;
reference check:task-bc8c3246ad3449e39155d369ae07c9e0:7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
Smoke IDs a7c4d563cf8f1b61e6122fe1d8364e08dba66b8df6cb8849b9857d1ee264c197
and c9741b96598e19d0ffa225d9023bbe080b717278134189f7180b6c8b659b47d4.
check-report confirmed the exact-source PASSED record. Approved stdout exports
now exit 0: first smoke A log and second smoke B log are empty (reported size 0);
first smoke B export is an 8,192-character bounded slice of a 56,138-byte log.
No bot-error marker appears in those exports. Files are saved in this task's
directory. This resolves the historical access blocker; empty logs do not prove
completion, strategic success or absence of fuel suspensions. No score inferred.
`git diff --check` PASSED, exit 0. No source changes after trusted compilation.

Risks: limited geometric ranking can miss further available/cleared groups;
hidden allies are uncoordinated. Recovery overhead, conservative sleeping-camp
threat estimates, shield/reset competition, initialization and path fuel remain
unmeasured. Earlier Varg-first, weak-camp-only, Jungle-only and shield-only
experiments did not establish additive gains; retain these negative findings.
Next: supervisor evaluates exact checked source on matched maps, both sides and
frozen opponents, comparing wins, submitted/collected gems, deaths and any idle
or suspension telemetry. If routing stalls, inspect timestamped respawn-aware
ranking. Promotion still requires the full accepted-champion gate.
