# Operational summary

## task-a84a38285fa94c9e9fd86b5a7d421ae8 — shield before exposed attacks

Playbook D. Hypothesis: casting a ready self-shield immediately before a legal
basic attack on a positive-Strength target whose attack range includes us will
absorb incoming damage, reducing recovery interruptions/deaths and improving
gem throughput. Falsifiable invariant: only an already legal attack can trigger
one successful self-shield cast; non-damaging or out-of-range threats cannot;
shield kind, self-target permission and live readiness are required. Basic
attack allowance is checked again after casting. No shield on travel alone.

Identity: beta; bot/beta; HEAD/input 07b24e4a90a72a8ec6f77ae3cf8093a687daf068.
Accepted edit start 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9, source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source files matched accepted Git blobs at entry. Initial bot.cpp diff
against HEAD is trusted restoration. Accepted Git preserves the baseline.
Prior task PUBLISHED and evaluated; no candidate awaits evaluation. Old recovery
artifacts preserved; prior summary archived through task-41dc854784904d468837b2cde087ddc6.
Engine/SDK 2.1.6; lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Handoff says documentation unchanged. Read compact
reference, RESEARCH.md, Playbooks C/D/F and relevant installed C++ contracts.
Separate organizer AGENTS.md remains absent.

Evidence: evaluation c2f8a2918dad0f78da1cdf1b14acaf9837fd12d694a5786a9d62846f941c7e26
REJECTED/full-nine-map, 14W/58L, matched delta 0, zero reported bot faults,
missing results or unknown reliability. Candidate commit
07b24e4a90a72a8ec6f77ae3cf8093a687daf068, source
fc461f9ba86b39b60ee220037052685a761354cf0fc4eb9926c41e01deebeb93.
Development collision losses: 965700180b56d908ebe1dce2ad1feae1875c35ab11389282fc5af1ab2f2f026a
(side B), 90817aa2654ee7e28441514ba5e838244f5a77319bd85ec66e0969b1e4e7d22e
(side A). Development means: 20.52 deaths, 731.04 collected, 631.63 submitted.
These evaluate weak-camp targeting, NOT restored accepted source. No fault is
evidenced; losses/deaths motivate survivability work without proving causation.
Accepted source never casts any shield. Earlier reset and damage/CC experiments
explicitly excluded shield abilities; this is a distinct defensive policy.

Contracts: GameRules.md:762–792 makes Varg's self-shield walk compatible,
2.5*Focus for five turns, cooldown eight owner ticks. C++ unit::strength and
attack_tiles require visibility; existing attack legality guards precede them.
ability::is_ready checks cooldown and caster can_cast; can_target_self checks
target permission; use() is the no-target cast. Attack mask is geometry, not a
prediction that the target will attack us. Scan is bounded by two ability slots.

Change: attack_if_in_range adds nine lines before the existing basic attack.
Only targets already passing live visibility, health, range and attack-allowance
checks can trigger a shield. Require positive target Strength and its attack
mask to include our tile; scan at most two slots for a ready self-shield, stop
on successful cast, then refresh basic attack allowance. Varg's shield is walk
compatible, so the same helper is used before and after movement. No draft,
shopping, routing, priority, channels, shared-memory or dispatch/yield change
relative to accepted source.

Checks: `python3 experiments/beta/check_defensive_shield.py` PASSED, exit 0.
Report: experiments/beta/task-a84a38285fa94c9e9fd86b5a7d421ae8/defensive-shield-invariant.txt.
Verifies guard/action order, single-success cast and exact accepted-source scope;
rejects baseline and eight unsafe mutations. Initial source-scope assertion
failed because the harness retained an inserted blank line; corrected the
harness boundary and reran successfully without changing bot source.
`git diff --check` PASSED, exit 0.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0. Exact checked source:
bc3f6f13bce3869b6ceb0360eb77cf9789cdfc66dcb05ed978aef306b229a910.
Report: .agent/check-task-a84a38285fa94c9e9fd86b5a7d421ae8.json.
Reference: check:task-a84a38285fa94c9e9fd86b5a7d421ae8:bc3f6f13bce3869b6ceb0360eb77cf9789cdfc66dcb05ed978aef306b229a910.
Smoke IDs: 89eb4c60e968a4d4629f28e0f85fa004373fb225e53390f1a085b59c6f9e7561,
eec2f650cdda93c83d40994ccd012e1f4067b4690eca97290a46c0e073dd9702.
Trusted compilation/smoke passed; local summary does not establish completed
game outcomes, shield activation/absorption, Varg presence or fuel headroom.
Uncertainty: draft may omit Varg; range/Strength do not prove incoming damage
(camps may sleep or attack another champion). Shield may be spent before a
lethal hit or before a more valuable fight. No survival, fuel or strength claim.
Next: supervisor evaluates the exact checked candidate against accepted source;
compare deaths, collected/submitted gems and recovery frequency if available.
