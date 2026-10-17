"""Choose a cumulative training base without promoting a competition champion.

Compare only complete both-side DEVELOPMENT cases with identical semantic
inputs. Changing panels, repeated games and holdouts cannot inflate the score.
The choice is recomputable from the immutable ledger and frozen in each task.
"""
import collections
import json

from .common import identity


POLICY = 'matched-development-v1'


def select_base(arena, bot):
    db = arena.db
    lane = db.one('SELECT * FROM bots WHERE id=?', (bot,))
    accepted = db.one('SELECT * FROM revisions WHERE id=?', (lane['accepted_revision'],))
    if not accepted:
        return None, {'policy': POLICY, 'reason': 'no validated baseline'}
    maps = arena.freeze_maps()
    scores, revisions, evidence = {}, {accepted['source_hash']: accepted}, {}
    rows = db.all('SELECT * FROM evaluations WHERE bot_id=? AND finished IS NOT NULL '
                  'AND metrics IS NOT NULL ORDER BY created,id', (bot,))
    for row in rows:
        metrics, suite = json.loads(row['metrics']), json.loads(row['suite'])
        if (suite['engine_lock_hash'] != arena.adapter().lock_hash or
                metrics.get('missing') or metrics.get('fault_matches') or metrics.get('unknown_reliability') or
                not metrics.get('wins', 0) + metrics.get('losses', 0)):
            continue
        for role, rid in [('candidate', row['revision_id']), ('incumbent', row['incumbent_id']),
                          ('development-base', suite.get('development_incumbent_id'))]:
            if not rid:
                continue
            revision = db.one('SELECT * FROM revisions WHERE id=?', (rid,))
            source = revision['source_hash']
            revisions.setdefault(source, revision)
            cells = scores.setdefault(source, {})
            for case in db.all('SELECT c.*,j.spec,j.result,j.state AS job_state FROM evaluation_cases c JOIN match_jobs j '
                               'ON j.id=c.job_id WHERE c.evaluation_id=? AND c.role=?', (row['id'], role)):
                name = case['map_name']
                if name not in arena.config['evaluation']['development_maps']:
                    continue
                result = json.loads(case['result']) if case['result'] else {}
                spec = json.loads(case['spec'])
                side = case['candidate_side']
                own, other = ('a', 'b') if side == 'A' else ('b', 'a')
                if (case['job_state'] != 'COMPLETED' or not result.get('completed') or result.get('state') != 'COMPLETED' or
                        result.get('bot_faults') != 0 or spec[f'{own}_source_hash'] != source or
                        spec['engine_lock_hash'] != arena.adapter().lock_hash or
                        spec['settings_hash'] != identity(arena.adapter().lock.get('effective_profile')) or
                        spec['map_hash'] != maps[name]['hash'] or spec.get('round_override') is not None or
                        spec.get('fuel_override') is not None or spec.get('seed') is not None):
                    continue
                key = (name, spec['map_hash'], spec[f'{other}_source_hash'],
                       spec['engine_lock_hash'], spec['settings_hash'], side)
                value = int(result['winner'] == side)
                # Contradictory repeated deterministic inputs are unusable, not extra votes.
                if key in cells and cells[key] != value:
                    cells[key] = None
                else:
                    cells.setdefault(key, value)
                evidence[(source, key)] = {'evaluation_id': row['id'], 'match_id': case['job_id']}
    current, changes = accepted['source_hash'], []
    # Broad coverage first avoids an early starter-only win saturating the
    # comparison forever while better-evaluated contenders are available.
    # Coverage is only an ordering preference; advancement still requires
    # a positive matched-input comparison, never a raw cross-panel win rate.
    for source in sorted(scores, key=lambda s: -sum(v is not None for v in scores[s].values())):
        if source == current:
            continue
        common = set(scores[source]) & set(scores.get(current, {}))
        pairs = collections.defaultdict(dict)
        for key in sorted(common):
            if scores[source][key] is not None and scores[current][key] is not None:
                pairs[key[:-1]][key[-1]] = (scores[source][key], scores[current][key], key)
        pairs = {key: value for key, value in pairs.items() if set(value) == {'A', 'B'}}
        if len({key[0] for key in pairs}) < 3:
            continue
        by_map = collections.defaultdict(list)
        for key, values in pairs.items():
            by_map[key[0]].append(sum(a - b for a, b, _ in values.values()) / 2)
        delta = sum(sum(a - b for a, b, _ in v.values()) / 2 for v in pairs.values()) / len(pairs)
        gate = arena.config['evaluation']
        if (delta + 1e-12 < gate['minimum_gain'] or
                any(sum(v) / len(v) < -gate['maximum_map_drop'] - 1e-12 for v in by_map.values())):
            continue
        changes.append({'from_source': current, 'to_source': source, 'matched_delta': delta,
                        'maps': len(by_map), 'opponent_sources': len({k[2] for k in pairs}),
                        'side_pairs': len(pairs), 'evidence': [evidence[(source, x[2])]
                                                            for v in pairs.values() for x in v.values()]})
        current = source
    selected = revisions[current]
    return selected, {'policy': POLICY, 'revision_id': selected['id'], 'commit': selected['commit_sha'],
                      'source_hash': current, 'accepted_champion_revision': accepted['id'],
                      'decision_digest': identity(changes), 'advances': changes,
                      'meaning': 'Training edit base only, NOT champion promotion or official readiness. '
                                 'Broader coverage considered first; same-input development comparisons, >=3 maps, '
                                 'both sides, configured gain/drop limits. '
                                 'Holdouts never select this base; ties/regressions keep the prior base.'}
