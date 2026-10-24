# Final review (author self-review; user prohibits agents)

Compared source against trusted edit commit 863825b7, not HEAD. Only bot.cpp,
policy.h and new contact_test.h change from that edit base. Initial differences
in bot.h and removal of routing_test.h relative to HEAD are prepared edit-base
restoration, not this policy experiment.

- Identity: branch/head/entry and seven source file hashes matched before edits.
  Latest candidate already evaluated INCONCLUSIVE; no pending/recovered work.
- Scope: only beta source and beta experiment artifacts changed. Accepted bot
  remains protected in Git; no publication, agents or evaluation initiated.
- Hidden state: every enemy/ally/camp live query follows visibility. Danger
  snapshots are private observations from this turn, not shared or omniscient.
- Action safety: move destinations are reachable, currently free, visible tiles;
  retry refreshes blocker/visibility masks. Counterattack rebuilds live targets
  after movement/reveal and passes the walked flag for spell exclusivity.
- Channels/healing: existing channel return remains first; spawn healing holds
  before contact response. New policy never cancels a channel.
- Budget: contact scan starts above 45k, camp scan/escape actions retain 30k,
  at most 32 awake hazards, at most two move attempts, normal fuel settings.
  If hazard inspection is deferred or too dense, defend in place; do not resume
  farm movement. Existing main always yields, including caught exceptions.
- Strategy: losing contact precedes capture/farming/recovery movement, resets
  commitment and excludes its camp for twelve rounds. No chase/draft/build/
  banking/shared-memory changes. Counterattack cannot resume farming that turn.
- Compile-time regressions cover contact/no-contact, spawn hold, local odds,
  lethal pressure, melee/ranged envelope and escape lexicographic ordering.
  Trusted red build failed specifically on absent policy functions; final green
  build and two completed games establish legality in that fixture, not odds
  calibration or universal escape safety.

Limitations: HP*Strength ignores spell readiness, shields, hidden enemies and
walls separating allies. One-step ranged reach is deliberately conservative.
New blockers can reveal threats missing from the original advisory snapshot;
movement authorization itself refreshes live blockers and post-move combat
refreshes live targets. Local steps can fail in corridors. Retreat can reset a
capture or delay an urgent bank; no finishing exception is used. Spawn distance
is geometric and only a safety tie breaker. No independent code reviewer.

No remaining known action-contract defect identified in this pass. Competitive
benefit remains unmeasured; matched evaluation, especially boss contact maps,
must resolve retreat cost versus mortality and collection/tribute gains.
