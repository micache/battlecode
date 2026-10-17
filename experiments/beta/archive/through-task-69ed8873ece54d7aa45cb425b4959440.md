# Operational summary

## task-69ed8873ece54d7aa45cb425b4959440 — immediate tribute before combat

Playbook C. Hypothesis: when carrying gems already in range of an unlocked
altar, starting tribute before opportunistic champion attacks removes combat
starvation of that banking opportunity. Falsifiable expectation: after existing
channel/alive/action and emergency-recall guards, a positive bag and in-range
unlocked altar cause submit_gems and return before enemy attacks. Empty bags,
locked/distant altars and emergency recalls retain the accepted action order.
No threshold or RNG changes. A stronger win rate is unmeasured.

Identity: beta, bot/beta, input/HEAD 24bfa18df6fccba80e40ab9f60b1b72b5e345b7c.
Edit start is accepted commit 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9,
source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
Verified all six source SHA-256 values and accepted Git blobs, task/branch/HEAD,
unchanged reviewed documentation hashes and installed matching C++ header
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Engine 2.1.6; trusted lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Separate organizer AGENTS.md remains unavailable.
Accepted code is preserved in accepted_commit/supplied snapshot; no source copy.
Initial bot.cpp diff removes the previous candidate's spawn-heal guard as part
of trusted restoration; it is not an experimental deletion from accepted code.

Prior candidate task-3bd44d5f08a2471e9caede76707138de is PUBLISHED and evaluated,
not awaiting results: INCONCLUSIVE, 27W/27L, delta 0.07407407407407407, faults 0,
evaluation 873f965eaa5673e7c3cbea20fa845d6e6e6959d946e302c938406636d45baea8,
commit 24bfa18df6fccba80e40ab9f60b1b72b5e345b7c, source
02a532272622522f2c853fe557c16d98633bdd7898e75e4a82a03a311968b6b1.
Its notes archived in archive/through-task-3bd44d5f08a2471e9caede76707138de.md.
Older interrupted shopping work remains preserved in existing recovery files;
trusted prior notes establish recovery completed, and shopping was REJECTED.

Development context: collision B losses
41efe090e544212ddd5e6ee89a9f32036948607317379892eb0d0cdf9733bd8a and
b39b8ee54e3e2a8dbd14824ed8b054ab0144eb2f44e456567284d1c23c6a3dc2,
from the evaluated source above. Supplied development summary: 36 completed,
18W/18L, no faults; mean collected 928.83, submitted 851.67, deaths 21.08.
These are strategic-loss context, not evidence that missed tribute caused those
matches. Current accepted source deterministically returns from an in-range
enemy attack before it reaches the existing adjacent-altar submission branch;
repeated in-range enemies can postpone banking without bound. No turn-level
missed-window frequency or unbanked death value is available.

Rules GameRules.md:217–241 and BOT_REFERENCE.md section 3: carried gems do not
score; ordinary damage does not cancel tribute, but stun/death/locks can.
SDK submit_gems returns void; has_altar_lock checks visible locks of either
team. Preserve the accepted conservative any-lock exclusion. Preserve existing
channels, emergency recall, distant-altar combat order, routing and final yield.

Implemented: moved the existing eligible submission scan ahead of champion
combat; the later banking branch only computes approach goals. One source file
changed against accepted: 11 added/5 removed lines. No other source changes.
main.cpp still yields after every normal return or caught action exception.

`python3 experiments/beta/check_immediate_tribute.py` exited 0; report
experiments/beta/immediate-tribute-invariant.txt. Source-level invariant checks
eligible tribute before combat, existing guards before tribute, and distant
routing/farming after combat; rejects accepted source plus four mutations
removing bag/range/lock eligibility or immediate return. This is not an engine
trace of tribute success, survival, or channel completion.
`git diff --check` exited 0.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, PASSED; exact candidate source
a080397e5dc62a5007e7ad5398240f1aea5e9f7a6e67b94f3ce62622041ca310.
Report: .agent/check-task-69ed8873ece54d7aa45cb425b4959440.json.
Reference: check:task-69ed8873ece54d7aa45cb425b4959440:a080397e5dc62a5007e7ad5398240f1aea5e9f7a6e67b94f3ce62622041ca310.
Smoke IDs: 1b682eb5bb776dcf8dd8ceb529aa5c3ee2f966440cf4758dedcc30cfee844f22,
064016aab5657c363b87cf6f2199eaa4d0d5e3e4872aed52c344da2fada3e069.
No completed-game outcome, turn-level behavior, fuel headroom or strategic
improvement is inferred from the wrapper summary alone.
Remaining uncertainty: choosing tribute can forgo a defensive kill and expose
longer channels to death/stuns. No claim that the policy is universally safer.
Next: supervisor validates and evaluates this exact checked candidate against
the accepted baseline; inspect tribute conversion and defensive-combat costs.
