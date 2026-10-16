"""Fail-closed official selection monitor. No guessed platform API or upload call.

Login alone does not verify event policy, quotas or activation effects. Until a
reviewed adapter exists, this module can only nominate; it cannot publish.
"""
import json
import time

from .common import identity


def selection_status(arena, now=None):
    now = time.time() if now is None else now
    blockers = []
    readiness = arena.db.get('readiness', {})
    if not readiness.get('competition_parity_verified'):
        blockers.append('competition/readiness review incomplete')
    candidates = []
    for bot in arena.config['workers']:
        row = arena.db.one("SELECT e.*,r.commit_sha,r.source_hash FROM bots b JOIN evaluations e "
                           "ON e.revision_id=b.accepted_revision JOIN revisions r ON r.id=e.revision_id "
                           "WHERE b.id=? AND e.state='ACCEPTED' AND e.incumbent_id IS NOT NULL "
                           "ORDER BY e.finished DESC LIMIT 1", (bot,))
        if not row:
            blockers.append(f'{bot}: no full-gate accepted improvement')
            continue
        suite, metrics = json.loads(row['suite']), json.loads(row['metrics'])
        opponents = suite.get('opponents', {})
        if (suite.get('coverage') != 'full-nine-map' or len(suite.get('maps', {})) != 9 or
                len({o['source_hash'] for o in opponents.values()}) < 3 or
                metrics.get('paired_cases') != 9 * len(opponents) or
                metrics.get('missing') or metrics.get('fault_matches') or metrics.get('unknown_reliability') or
                metrics.get('decision') != 'ACCEPTED' or
                suite.get('infrastructure_commit') != arena.config['infrastructure_commit'] or
                suite.get('engine_lock_hash') != arena.adapter().lock_hash):
            blockers.append(f'{bot}: full-gate evidence incomplete or stale')
            continue
        panel = identity({k: suite[k] for k in ('maps', 'opponents', 'engine_lock_hash')})
        games = metrics['wins'] + metrics['losses']
        candidates.append({'bot': bot, 'commit': row['commit_sha'], 'source_hash': row['source_hash'],
                           'evaluation_id': row['id'], 'panel': panel,
                           'score': metrics['wins'] / games if games else 0})
    if len({c['panel'] for c in candidates}) > 1:
        blockers.append('lane champions need the same frozen comparison panel')
    leader = None
    if not blockers and len(candidates) == len(arena.config['workers']):
        candidates.sort(key=lambda c: (-c['score'], c['bot']))
        if len(candidates) > 1 and candidates[0]['score'] - candidates[1]['score'] < .05 - 1e-12:
            blockers.append('team lead below five percentage points')
        else:
            leader = candidates[0]
    observation = arena.db.get('official_leader', {})
    key = identity(leader) if leader else None
    if observation.get('identity') != key:
        observation = {'identity': key, 'since': now, 'candidate': leader}
        arena.db.put('official_leader', observation)
    stable = now - observation.get('since', now) if leader else 0
    if leader and stable < 6 * 3600:
        blockers.append('leader must remain unchanged for six hours; elapsed time is not independent game evidence')
    if now - arena.db.get('official_last_upload_at', 0) < 86400:
        blockers.append('24-hour submission cooldown')
    # Deliberately impossible to enable via configuration: implement only after interface review.
    blockers.append('official adapter not verified: upload activation effects, event policies, quotas and challenge interface')
    return {'enabled': False, 'candidate': leader, 'stable_seconds': stable,
            'blockers': blockers, 'login_required_every_days': 7,
            'max_uploads_per_day': 1, 'max_outstanding_challenges': 1,
            'unknown_remote_creation': 'stop and reconcile; never blindly retry'}
