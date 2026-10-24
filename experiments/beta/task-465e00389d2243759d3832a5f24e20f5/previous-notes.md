# Operational summary

## task-0c54be79e5fb4e3c801a91ec13ed6981 — cap idle-cash gold farming

Hypothesis: excluding new zero-gem camp targets at 150 unspent gold before the
12-group shortlist improves matched wins and submitted gems versus a4a26c5d /
9f254079. No win gain, lower submissions, or increased own faults/fuel suspension
falsifies it. Expected mechanism: fewer high-cash zero-gem farmers. Unmeasured.
Decision, evidence, complete match summaries and check artifacts are in
experiments/beta/task-0c54be79e5fb4e3c801a91ec13ed6981/.
Previous summary archived through task-2906ee1a; retain its negative findings.

Identity: beta / bot/beta, HEAD/input/edit a4a26c5d8d364055f1b2e36f2bf72885c4e3da54;
base source 9f2540790f9f048d6f404bb0f20a1e9e03180191c9c043c5322171f838253360.
Initial Git clean; all six source files matched trusted per-file hashes.
Prior task PUBLISHED/evaluated, no unfinished candidate. Accepted champion
0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in trusted Git/snapshot.

Base evidence: f59892af evaluation, INCONCLUSIVE/full-map-pool 105W/31L;
development-only 87W/25L in 112 completed distinct cases, zero own fault matches.
Matched development delta +0.0625 versus 50a0d7d5/6d66a77f. These evaluate base,
not today's candidate. Complete summary slices are retained for:
- Ambush A 33fdddcfbb1f9a83dc5f5d72a0f6dc8de4b6aff17b36e74be43b5e63c9e70b39:
  round 1069, 836:1008 submitted. Ryth 1697 and Marcella 1260 earned gold;
  each zero collected gems, spending and monster damage taken. Zero own deaths,
  faults, suspensions and bag loss.
- Ambush A 61cf5ad8aedbfcfb3ca2c38e5490cd469597bcb642dffab692a6699be9af43f0:
  round 799, 144:1004 submitted. Varg 805 and Marcella 1085 earned gold;
  each zero gems/spending. One own death, zero own faults/suspension/bag loss.
  The match's one suspension belongs to B. Ambush opponent revisions unknown.
- Rushbait-v2 A 037019ccc58ed90d19b7726e747478961ff70dbf9d534ae89fb236bf157ce6ea
  vs gamma bd4078cd: round 705, 234:1034, two own deaths, 72 lost gems, zero
  own faults/suspensions. Different failure; cash cap need not solve it.
Contrasting aggregate base wins: collision/corners/eight/lanes 4W/0L each side,
ambush B 4W/0L. Individual winning IDs unavailable in compact table.
Final statistics suggest the gold loop; they do not prove exact routing turns.
External older official observations were not used as controlled results.

Change: economy_policy.h admits any positive-gem group, and zero-gem groups
only below 150 CURRENT cash. Filter before shortlisting; commitment cannot
retain an excluded gold target. Equipment/lifetime gold do not count, so shopping
reenables gold work. Current occupied cleared rewards are held before filtering,
using live state only on self's visible spawn tile. Existing final camp score,
12 inspections, movement/dash, roster, banking, recovery and item build remain.
Compile-time cases cover zero cash, 149/150 boundary, high cash and mixed/gem
rewards. No team memory protocol, extra path search or runtime logging.

Frozen manifest 44885ad0 inspected gamma ecbc8203/ff511c52, revision bd4078cd:
Varg/Vendetta/Marcella/Ryth/Tavi, melee resets, reachable value/time camps,
0.12 gold conversion, 300-gold shopping recall. Beta's safe recall instead needs
150 gold AND <80% health, so damage-free gold farmers hoard it. Adapt idle-capital
constraint through target eligibility, preserving beta's routing/recall strategy.
Shared arena source does not establish private official-opponent behavior.

Why not prior experiments: +40 penalty at 300 total capital still permits gold;
strict gem/full-trip routing at 150 total capital changed multiple policies and
had only +0.008929 development gain with regressions. Here cash-only eligibility
is reversible after spending and score ordering is unchanged on the newly
advanced melee roster. Current-source ambush losses supply fresh evidence.
Healthy shopping and bank detours had zero gain; recovery +0.026786, full
scheduler +0.041667 and gold penalty +0.044643 all had regressions; combat rewrite
-0.041667. Isolated items/shield gains remain unestablished.

Risks: remote/contested gems, reduced investment, existing live-Monolith/ranking
weaknesses and unavailable first-12 targets. Tavi spends in the field and may
continue preferring gold. Empty eligible search retains existing yield fallback;
no guaranteed exploration/respawn-vacating. Additional local scan/filter fuel
headroom is unmeasured. Compile/smoke success does not establish strategic gain.

Engine 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
suite published-17-release-225-v1. Handoff says SDK/docs unchanged. Consulted
compact reference, RESEARCH, organizer ledger, Playbooks B/C/E/F/G, relevant
handbook capture/items, C++ group-value/state API and matching installed SDK.
SDK SHA256 ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
Organizer hub does not certify all event policies or production parity.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0 for candidate source
6145b56e00470cc005a82f686f655f267b46545967b28fab257fdd7a58de0dc7.
Report .agent/check-task-0c54be79e5fb4e3c801a91ec13ed6981.json, copied as
check-report.json. Exact-source arena-client check-report also PASSED/0.
`git diff --check` PASSED/0 (diff-check.txt). Smoke IDs:
899a37562334be85ee1f26d33ae269b0602f9ab213dbddd36d2ec67a1cde16a3 (own A),
9f5299b7712f8ac95c6bbc3624803a5074d69ffee07cc24c721b21455b40b5b7 (own B).
No source edits after check. Both own-side stdout exports exited 0 and are empty
(smoke-a.json/smoke-b.json). Smoke success is not proof of completed competitive
games, policy coverage, zero suspensions or measured fuel headroom.

Next: supervisor evaluates exact checked source vs a4a26c5d/9f254079 on matched
maps/sides/frozen opponents. Wins and submissions primary; inspect high-cash
zero-gem farmers, protect existing collision/corners/eight/lanes and ambush B.
Full champion promotion gate mandatory. No agents, commit, push, official action,
comparative tournament, or waiting for evaluation performed in this invocation.
