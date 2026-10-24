# Gamma operational notes

## task-e523e59b36b9442d9c09d5225bf2167d — risk-aware camp selection

- Refinement; one candidate. Branch bot/gamma, HEAD/input 63719c284a8377f42684ee01096d43c6fe822e94.
  Actual edit commit ecbc8203fd2ef0696ef7784c8b39528bb182ad7b, source
  ff511c52577a0f42c5e17329423aaa100b0317ddcaf037f8b2ba59b808061671.
  All six source files matched trusted edit hashes. Prepared bot.cpp/bot.h
  restoration and farm_value.h deletion are intentional, not interrupted work.
  Latest candidate has completed evaluation; no own candidate is pending.
  Protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains outside this transaction.
- Hypothesis: risk-aware camp selection with recovery when no feasible target
  remains increases matched development win rate AND mean submitted gems,
  without new own faults. Non-positive win change, non-increasing mean tribute,
  or a new own fault falsifies it. Supervisor applies unchanged arena gates.
- Prior delivery-aware scoring regressed versus this base: latest evaluation
  38b179a2b60a8001d87b4cae0623b89da45db45a64c8de9eb4e51d009cb5cc05,
  candidate63719c28/source846588e4, 87W/49L overall, zero faults; matched
  development delta -0.1339285714 across56 side pairs. Not today's edit base.
  Previous notes archived under task-ff42f1f4a5724e2a898c2cea340c1a75.

## Policy and code

- Keep Varg/Vendetta/Marcella/Ryth/Tavi draft, Jungle Strength, Monster Strength,
  one Durability Health then Power Strength, all-bag banking, route locks,
  300-gold safe recall, 98% spawn healing, existing combat and fuel fallback.
- farm_risk.h estimates damage =0.60*remainingHP*summedStrength/(1.12*selfStrength),
  with 0.70 Jungle and0.90 Durability multipliers only for completed emblems.
  These are policy estimates, not SDK predictions. No shield, spell burst,
  tanking ally or unseen helper credit. The 0.60 exposure model is adapted
  from the frozen boss; gamma retains its own scoring, build and draft.
- Normal target selection rejects predicted clears crossing currentHP minus
  35%maxHP. Committed targets receive no exemption; partially cleared targets
  use fresh visible HP. Unknown members use static design HP/Strength only.
  Completed rewards and harmless clusters bypass the risk rejection.
- If no feasible target remains and wounded, move toward spawn and recall only
  when the refreshed position is unthreatened and action allowances remain.
  This avoids idling forever above the ordinary retreat threshold. Existing
  capture-occupancy return, channels, low-fuel eight-camp fallback and yield stay.
- Only bot.cpp and new farm_risk.h differ from the edit base. No shared-memory
  change, new search, copied SDK, fuel overrides or opponent edits.
- Actual helper has eight compile-time regressions: wolf feasible, early elk
  rejected, geared elk feasible, wounded wolf rejected, harmless/reward exempt,
  mitigation monotonicity and zero-strength guard.

## Evidence and uncertainty

- Frozen manifest5b3413cd81492d5ed792cc24c1deb813e82d3855993b0f2d29c5976f23424d5d:
  all six file sets hash-verified. Boss192daa8e/d10ae8b4 uses Vendetta/Varg/Ryth,
  claim coordination, risk-budgeted clears, support shields, favorable PvP,
  30-gem/near-altar banking and150-gold shopping. Inspected relevant full source.
  Other packet sources: alpha82a14a04/046f1c3a random draft/Power build,
  timestamped rotation (latter adds exposure-aware recovery); beta7cab9b0f and
  a4a26c5d melee/reset farming and defensive builds, former gold-only penalty;
  starter89976632 random draft/Power build. No private opponent state accessed.
- Exact-base boss Collision losses: sideA85bee70b, round670,282 vs1032 tribute,
  eight deaths,21617 camp damage taken vs6492; sideB639ac1ff, round719,
  298 vs1132 tribute,11 deaths,19772 camp damage taken vs6884. Both completed,
  zero faults/suspensions; own sourceff511c52 vs bossd10ae8b4 per trusted brief.
  Saved full compact summaries boss-safety-85bee70b.json and639ac1ff.json.
- Same-base contrasting Collision A smoke41c22e31,1028 vs66 tribute, completed,
  no faults/suspensions (altar-control-smoke.json). Opponent revision unknown;
  different opponent makes this a validity contrast, not a controlled comparison.
- Latest-source Collision A loss377bccb4 (boss-safety-377bccb4.json) had41 deaths,
  1818 bag loss and36 vs278 tribute by round2000; most death pressure is PvP.
  Source846588e4, not edit base. This policy does not claim to solve ranged camping.
- Boss finals motivate survival work but do not prove dangerous pull choices.
  Main risks: full-group model can overexclude sequential/splash clears; no ally
  credit can prevent useful cooperation; unseen design estimates can overstate
  remaining HP. Conservative resets/shields and spell bursts are underestimated.
  Extra Strength reads add fuel cost; original low-fuel fallback bypasses risk
  estimates. Narrow-map all-dangerous openings may have no feasible target.
- Routine unchanged-doc iteration: BOT_REFERENCE, playbooksB/C/D/F/G, RESEARCH,
  organizer ledger, relevant rules and installed C++ camp/design/item contracts.
  SDKee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264;
  CLI2.2.5/lock0cabb3c7/suitepublished-17-release-225-v1. Organizer download hub
  is not complete policy review; production parity is not newly certified.

## Validation and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, checked source1d8ee4138be0bceae136f15ab642f9daf6788729b197b254f3e38c260e1d7b68.
  Report .agent/check-task-e523e59b36b9442d9c09d5225bf2167d.json. Eight actual
  helper assertions compiled. Per-file hashes unchanged after check launch.
- Collision smokes25228946 (A,round540,1010 vs0) and242a34de (B,round557,
  1002 vs22) completed with zero faults/suspensions on BOTH sides. Engine0.0.3,
  buildd7e29ae3; opponent revisions unknown. Execution evidence, not matched
  superiority. Full summaries camp-safety-smoke.json.
- git diff --check PASSED exit0. Candidate decision, hashes and check result:
  camp-safety-evidence.json. No source changes after trusted check.
- Next: supervisor evaluates checked source against ff511c52 and protected
  champion on matched maps, sides and frozen opponents. Compare wins/tribute
  first, then early camp choices, deaths, recovery time and suspensions. If
  overexclusion dominates, inspect live cooperative clear opportunities before
  adding a helper credit or changing the exposure coefficient.
