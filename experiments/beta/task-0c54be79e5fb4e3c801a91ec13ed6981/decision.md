# Unspent-cash cap on gold-only farming

Hypothesis: suppressing new zero-gem camp targets at 150 unspent gold, before
shortlisting and regardless of commitment, improves matched wins and submitted
gems versus a4a26c5d / 9f254079. No win gain, lower submissions, or increased
own faults/fuel suspension falsifies it. Mechanism: fewer high-cash, zero-gem
farmers and more gem collection. This candidate's gain is unmeasured.

Identity: task-0c54be79e5fb4e3c801a91ec13ed6981, beta, bot/beta. All six source
files matched feedback.handoff edit_start hashes; clean initial Git status and
HEAD a4a26c5d match trusted input/edit. Prior task-2906ee1a was PUBLISHED and
its candidate evaluated. Accepted champion 0ca5c04e remains in trusted Git and
accepted_snapshot; no recovery required. Engine 2.2.5, unchanged SDK/docs,
lock 0cabb3c7; suite published-17-release-225-v1.

Evidence: f59892af evaluation of this exact base; INCONCLUSIVE overall,
105W/31L, zero own fault matches. Development-only table 87W/25L, 112 distinct
completed cases, matched development gain +0.0625 from the prior edit base.
Do not pool scores from older candidates or count deterministic repeats.
- 33fdddcfbb1f9a83dc5f5d72a0f6dc8de4b6aff17b36e74be43b5e63c9e70b39:
  ambush A, round 1069, lost 836:1008 submitted. Ryth earned 1697 gold and
  Marcella 1260, each zero collected gems, zero spent gold, zero monster damage
  taken. Zero own deaths, faults, fuel suspension and bag loss.
- 61cf5ad8aedbfcfb3ca2c38e5490cd469597bcb642dffab692a6699be9af43f0:
  ambush A, round 799, lost 144:1004 submitted. Varg earned 805 gold and
  Marcella 1085, each zero collected gems and spending. One own death, zero own
  faults/suspension/bag loss; the one match suspension belongs to B.
- 037019ccc58ed90d19b7726e747478961ff70dbf9d534ae89fb236bf157ce6ea:
  rushbait-v2 A versus gamma bd4078cd, round 705, lost 234:1034 submitted;
  this is a different failure, with two own deaths and substantial gem losses.
  Cash eligibility is not expected to solve every loss.
- Contrasting base development success: collision/corners/eight/lanes each 4W/0L
  per side; ambush B 4W/0L. Individual winning IDs unavailable in compact table.
  Protect these cases in evaluation. Opponent revisions of the two ambush games
  are unknown in supplied compact records; do not infer them from draft order.
Saved complete summary.json slices beside this decision. Final statistics do
not prove routes or exact causal turns; the source's gold eligibility and target
commitment support the loop hypothesis. No omniscient state becomes runtime input.

Chosen policy:
- Current cash >=150 excludes zero-gem groups BEFORE the 12-group shortlist.
  Positive-gem and mixed groups retain exactly the existing final score.
- Count cash only. Purchased equipment and lifetime earned gold do not count.
  After shopping below 150, pure gold is eligible again. Startup is preserved.
- Before economic filtering, preserve any cleared reward occupied by self.
  Inspect state only where self stands on that group's original spawn tile.
- A formerly committed gold target has no exemption; otherwise commitment would
  perpetuate the loop. No new path search, shared-memory writes or live queries
  per nonoccupied group. Existing 12 inspections/reserves/movement/yield remain.
- Compile-time policy checks cover 149/150, no cash, large cash, and positive gems.

Why this experiment after previous negatives: earlier +40 penalty at 300 total
capital could still select gold; the strict gem/full-trip scheduler at 150 total
capital changed scoring, tiers, Monolith handling and cooldowns and gained only
+0.008929 with regressions. Healthy shopping and bank detours gained zero. This
candidate tests reversible CASH saturation alone on the newly advanced melee
roster, whose two current-source ambush losses reproduce severe idle-capital
symptoms. It leaves ranking among productive groups intact and permits renewed
gold farming after investment. It does not restore the rejected scheduler or
add healthy shopping trips. Recovery/combat changes are not indicated by the
first death-free loss.

Frozen opponent manifest 44885ad0: inspected gamma ecbc8203/ff511c52,
revision bd4078cd26f091dc34cbaa80a9d40d04d7a2e53cc7ae156430d1ec212e6c6974.
Its Varg/Vendetta/Marcella/Ryth/Tavi draft, melee resets, reward/time farming
with 0.12 gold conversion and 300-gold shopping recall explicitly convert gold
into power. Beta instead recalls at 150 only below 80% health; damage-free gold
farmers do not qualify. Adapt the principle of limiting idle capital by limiting
further pure-gold work; retain beta's farm score, roster and recall policy.
Frozen arena source is not evidence of private official opponents' behavior.

Risks: hard cash cap can deny valuable future investment or send farmers toward
contested/remote gems; existing geometric ranking can pick costly Monoliths;
the first 12 inspected groups can be unavailable or unreachable. Tavi can spend
in the field and may not saturate cash; this does not solve her gold preference.
If no eligible group can be selected, the old no-target fallback yields; it does
not guarantee exploration or vacating a respawn region. Holding a gold capture
is preserved, but no team-wide reservation or rich memory is added. Additional
local group scan and vector filtering have not been measured for fuel headroom.

Rules: compact BOT_REFERENCE, RESEARCH, organizer-agents ledger and Playbooks
B/C/E/F/G; targeted handbook camps/capture/items and C++ group-value/state API;
matching installed 2.2.5 header shows immutable cached gem_value and current-
vision state guard. SDK hash ee131e29, unchanged per trusted handoff. The organizer
Markdown hub is not a certification of all event policies or production parity.

Next: supervisor evaluates exact checked candidate against a4a26c5d/9f254079
on matched maps, both sides and frozen opponents. Prioritize wins/submissions;
inspect reduction in high-cash zero-gem champions, not gold-spending alone.
Protect collision/corners/eight/lanes and ambush B; full champion gate required.

Validation: final bot-check PASSED/0, exact source 6145b56e00470cc005a82f686f655f267b46545967b28fab257fdd7a58de0dc7.
Report .agent/check-task-0c54be79e5fb4e3c801a91ec13ed6981.json copied to
check-report.json. Exact-source check-report PASSED/0. Both own-side smoke
stdout exports exited 0 and are empty (smoke-a.json, smoke-b.json).
git diff --check PASSED/0. No bot source changes after check. Compilation includes
policy static_assert cases; smoke is not comparative evidence, complete-game
certification, actual policy coverage, or measured fuel headroom.
