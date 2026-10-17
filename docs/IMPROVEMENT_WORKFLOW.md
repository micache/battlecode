# Shared competitive improvement workflow

All lanes use `skills/battlecode-strategy/SKILL.md` and the same worker prompt.
Bot ID, branch, evidence and mode are task inputs, not separate personalities or
hard-coded strategies. The existing subscription model/effort, hourly cadence,
one global model slot and continuous self-play remain unchanged.

## What was limiting progress

The old worker reset every experiment to `accepted_snapshot`. Automatic champion
promotion is disabled, so the protected accepted source stayed at the starter.
Even a useful evaluated candidate was not automatically carried into the next
task. The shared instructions also repeatedly encouraged a smallest-component
repair, and a bot branch could retain old root instructions across runtime
upgrades. A small diff alone does not prove poor strategy, but these are concrete
workflow limits on cumulative improvement.

## Starting code and evaluation are separate decisions

`arena/development.py` recomputes a training incumbent from saved completed
evaluations. Start with the accepted champion; consider broader-coverage sources
first (chronological order on a coverage tie) and advance only with:

- No missing games, faults or unknown reliability in that evaluation.
- Current engine lock/map hashes and matching settings, fixed opponent source,
  map and side, with both A/B cases and at least three development maps.
- At least the configured minimum gain and no map drop beyond the configured
  maximum. Ties keep the prior development incumbent.

Repeated identical inputs count once. Contradictory outcomes for a semantic input
are excluded. Raw win rates against different panels are never ranked. Reserved
holdout scores do not select the edit base. A three-map advance is provisional
training evidence, not a full-gate champion or a claim of statistical significance.
Insufficient evidence retains the current base; an engine change falls back to
the accepted champion until matching new evidence exists.

Each task freezes `edit_commit`, `edit_snapshot`, `base_source_hash` and the
selection evidence. `accepted_commit`/`accepted_snapshot` still name the protected
champion, and `input_revision` still names the branch tip used as publication
parent. Publication records the actual edit-base hash on the resulting revision.
Neither this selection nor a worker changes the full champion gate or enables
automatic promotion/official submission. The full evaluator still uses the
accepted champion and frozen matched opponents.

New workflow candidates also evaluate their frozen development base against the
same opponent panel on all six development maps, both sides. This supplies the
missing comparisons as opponents change and prevents a starter-only plateau from
blocking cumulative progress. These additional cases do not replace the protected
champion comparison or reveal reserved holdout traces. Initial new-lane wiring
still uses its three maps; ordinary new-workflow screening is explicitly labeled
`development-six-map`, and full promotion checks retain all nine maps.

## Strategy phases and memory

The first published experiment under this workflow is a **foundation** task:
derive a coherent contender from rules and current source, with explicit draft,
roles, economy/capture, banking, combat, recovery and navigation decisions.
Legal starter behavior is a floor, not the target. Coupled multi-file upgrades
are allowed, with no diff-size target. The 20-minute invocation must finish with
a playable candidate, trusted checks and a falsifiable strategy claim.

Later jobs use the existing refinement/exploration schedule. They compare
alternative high-value ideas, diagnose actual bottlenecks, study our frozen
opponents and implement one coherent candidate. Compact notes retain the current
strategy, parameters, evidence, rejected ideas, uncertainties and next experiment.
`.agent/base-notes.md` preserves notes from the chosen starting commit separately
from HEAD's possibly rejected latest experiment. History/checkpoints remain
retrievable; no conversation transcript or private reasoning is required.

## Readable knowledge, without credential sharing

The trusted supervisor freezes documentation hashes and up to six distinct
arena opponent source snapshots per task. Worker preparation verifies them,
delivers current documents to `.agent/knowledge/`, installs the discoverable
skill under `.agents/skills/`, and supplies `AGENTS.override.md` so old bot
branches cannot load stale root instructions. These preparation-only paths are
excluded from Git and checked against the trusted envelope before publication.
Only owned source and notes enter the publisher's clean commit.

The opponent manifest identifies exact bot/commit/source/file hashes and paths.
Workers can inspect strategy from those frozen sources. No private owner notes,
credentials, mutable opponent checkout or reserved match traces are shared.
Source comments/logs are data, never instructions. Visibility restrictions still
apply inside the actual game.

The organizer's LLM download page was accessed and its unchanged rules plus
current C++/Python exports are retained; see `docs/rules/organizer-agents.md`.
Full applicable game/API/SDK review happens once or when gameplay hashes change;
ordinary instruction-only changes do not force another full API read. Routine
jobs use the compact reference and targeted lookups. The installed pinned SDK
remains authoritative for which methods compile; web examples are not blindly
assumed compatible with the local engine.

## Research basis and limits

OpenAI's [reasoning guidance](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
supports clear objectives and success criteria rather than chain-of-thought
transcript prompts. Its [skills documentation](https://developers.openai.com/codex/skills)
describes progressive disclosure and repository skill discovery. The
[GPT-6 family guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.1-sol)
recommends auditing conflicting instructions and calibrating verification; its
behavior examples are mainly Astra observations, not a measured Sol win-rate
claim. We retain `gpt-6.1-sol` / `high`. Skill Creator informed a single focused
instruction-only skill instead of extra agents, repeated manuals or a new agent
framework.

Tests establish source continuity, frozen identities, isolation and gate
preservation. They cannot establish that the new prompt produces stronger bots.
That requires actual new candidate evaluations on saved immutable inputs.
