# Operational summary

## task-22caf7462e2948bb8845e85c3489e69a — unit spells after stationary attacks

Playbook D. Hypothesis: following a stationary basic attack with one ready,
legal direct-damage/CC spell against its surviving target uses otherwise idle
Focus and cooldowns, increasing damage/control without changing target choice.
Falsifiable expectation: a surviving visible target in basic and spell range,
with a matching target mask and ready damage/CC slot, receives one spell after
the basic attack; a lethal basic attack, dead caster, no eligible spell, or an
attack after walking receives no spell. Never cast twice successfully.
Expected strategic benefit is faster camp clearing and better exchanges;
win rate, clearing time and survival effects remain unmeasured.

Identity: beta, bot/beta, input/HEAD a347d811a59adb7c2a3f69bedde352ed7bbf1b2e.
Accepted edit start: commit 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9;
source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
Entry identity, all six accepted source file hashes and Git blobs verified.
Engine/SDK 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Matching C++ header SHA-256 verified:
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
All reviewed documentation hashes unchanged. Only relevant rule/API/SDK sections
consulted this routine task. Separate organizer AGENTS.md remains unavailable.
Accepted Git/supplied snapshot preserves baseline outside the edit transaction.
Initial diff from HEAD removes the prior tribute candidate by trusted restoration,
not by this experiment. Prior notes archived by task ID. No pending evaluation.
Older interrupted work remains preserved in existing recovery files.

Development context: evaluation
719be6f1c93a369eb097b155f54882e8990fe86aeab77b77c852e800a657bab7,
commit a347d811a59adb7c2a3f69bedde352ed7bbf1b2e, source
a080397e5dc62a5007e7ad5398240f1aea5e9f7a6e67b94f3ce62622041ca310,
INCONCLUSIVE, provisional three-map coverage, 10W/14L, 0 faults, 0 missing.
Representative collision B losses:
064016aab5657c363b87cf6f2199eaa4d0d5e3e4872aed52c344da2fada3e069 and
280b86ae5b84fc4b33c05167ee41a2474248e47be9eec28411e99124062e97eb.
Development means: deaths 27.67, kills 6.08, collected gems 774.17, submitted
664.25 over 24 games. These are strategic-loss context, not proof of unused-spell
causation, and do not evaluate the restored accepted source or this candidate.
Source-supported failure: attack_if_in_range always returns after one basic
attack, and no accepted source path casts any ability. Focus shards can be
chosen but spell damage is unused. Earlier reset experiment task-32b6f4ccb8f54f1ead2a0e7c4bdcac48
was INCONCLUSIVE (3W/3L); this tests direct damage/CC, not another reset policy.
No turn-level damage, cooldown or camp-clear telemetry is supplied.

Contracts: GameRules.md:245–266,416; BOT_REFERENCE.md sections 3,5,6;
C++ cambc.h ability::is_ready checks cooldown plus caster can_cast; valid_tiles
checks range only; can_target_camps/enemies supplies the separate category check.
Unit casts use ability.use(target). Both current slots are examined in index
order; only damage/CC kinds qualify. We conservatively skip all spells after
walking, including walk-compatible spells, rather than infer walking from the
remaining allowance (a stationary ranged attack also consumes movement).

Implemented: bot.cpp adds a guarded single-target spell follow-up after the
existing basic attack; only damage/CC kinds qualify, with live readiness,
category and range checks. Refresh survival/visibility after basic damage and
retaliation. The post-movement camp attack explicitly disables spells. Main's
end_turn dispatch, channels, target order, draft, shopping and RNG are unchanged.
Only bot.cpp differs from accepted source (19 insertions, 3 deletions).

`python3 experiments/beta/check_unit_spells.py` exited 0. Report:
experiments/beta/task-22caf7462e2948bb8845e85c3489e69a/unit-spells-invariant.txt.
Checks guarded cast order, target masks/range/readiness, survival/visibility,
single success and movement exclusion; rejects accepted source and nine
mutations. Source invariant only, not a simulation or measured spell trace.
`git diff --check` exited 0.
Trusted command:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, PASSED, for exact candidate source
0c8c6de101ec85fcad250ef308157891de39e173751780d4e7b117285a73e5a1.
Local report: .agent/check-task-22caf7462e2948bb8845e85c3489e69a.json.
Reference: check:task-22caf7462e2948bb8845e85c3489e69a:0c8c6de101ec85fcad250ef308157891de39e173751780d4e7b117285a73e5a1.
Smoke IDs: 77edcd12ee37b66a10e772dacf23a95694af989d131fc24b3a37a40b86cbd9e0,
73172cde42a510b26c762c7249dbc18d6a6a2e7b28ccb49b3a63dec521140494.
Wrapper success alone does not establish completed-game outcomes, tactical
spell traces, measured fuel headroom, or strategic improvement.
Remaining uncertainty: extra actions cost fuel and retaliation can kill casters;
spell use on camps may sacrifice an upcoming defensive stun. Single-target-only
policy leaves AoE, resets, shields, heals, and longer-range attacks untested.
Next: supervisor evaluates this exact candidate against accepted; inspect clear
speed, survival and objective costs before broadening ability use.
