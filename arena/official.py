"""Fail-closed official selection monitor. No guessed platform API or upload call.

Login alone does not verify event policy, quotas or activation effects. Until a
reviewed adapter exists, this module can only nominate; it cannot publish.
"""
import json
import time

from .common import identity


def cadence_status(arena, candidate, now=None):
    """Durable nomination clock, not an upload adapter or a simulated submission."""
    now = time.time() if now is None else now
    policy = arena.config.get('official_schedule', {})
    interval = policy.get('check_interval_seconds', 5 * 3600)
    duplicate_wait = policy.get('unchanged_recheck_seconds', 3 * 3600)
    schedule = arena.db.get('official_schedule', {})
    last_upload = arena.db.get('official_last_upload_at', 0)
    next_check = max(schedule.get('next_check_at', 0), last_upload + interval if last_upload else 0)
    if now < next_check:
        return dict(schedule, next_check_at=next_check, due=False, uploads_performed=0)
    source = candidate.get('source_hash') if candidate else None
    previous = arena.db.get('official_submission:' + source, {}) if source else {}
    duplicate = bool(previous.get('confirmed') is True and previous.get('submission_id'))
    ambiguous = arena.db.get('official_upload_intent', {}).get('state') == 'UNKNOWN'
    action = ('BLOCKED_AMBIGUOUS_CREATION' if ambiguous else 'SKIP_ALREADY_SUBMITTED' if duplicate else
              'NOMINATED_NOT_UPLOADED' if candidate else 'NO_ELIGIBLE_REVISION')
    schedule = {'last_checked_at':now, 'next_check_at':now + (duplicate_wait if duplicate else interval),
                'action':action, 'candidate_source_hash':source,
                'previous_submission_id':previous.get('submission_id') if duplicate else None,
                'check_interval_seconds':interval, 'unchanged_recheck_seconds':duplicate_wait}
    arena.db.put('official_schedule', schedule)
    return dict(schedule, due=True, uploads_performed=0)


def selection_status(arena, now=None):
    now = time.time() if now is None else now
    blockers = []
    readiness = arena.db.get('readiness', {})
    if not readiness.get('competition_parity_verified'):
        blockers.append('competition/readiness review incomplete')
    candidates = []
    excluded = []
    for bot in arena.config['workers']:
        row = arena.db.one("SELECT e.*,r.commit_sha,r.source_hash FROM bots b JOIN evaluations e "
                           "ON e.revision_id=b.accepted_revision JOIN revisions r ON r.id=e.revision_id "
                           "WHERE b.id=? AND e.state='ACCEPTED' AND e.incumbent_id IS NOT NULL "
                           "ORDER BY e.finished DESC LIMIT 1", (bot,))
        if not row:
            excluded.append(f'{bot}: no full-gate accepted improvement')
            continue
        suite, metrics = json.loads(row['suite']), json.loads(row['metrics'])
        opponents = suite.get('opponents', {})
        if (suite.get('coverage') not in ('full-nine-map', 'full-map-pool') or
                suite.get('maps') != arena.freeze_maps() or
                len({o['source_hash'] for o in opponents.values()}) < 3 or
                metrics.get('paired_cases') != len(suite['maps']) * len(opponents) or
                metrics.get('missing') or metrics.get('fault_matches') or metrics.get('unknown_reliability') or
                metrics.get('decision') != 'ACCEPTED' or
                suite.get('infrastructure_commit') != arena.config['infrastructure_commit'] or
                suite.get('engine_lock_hash') != arena.adapter().lock_hash):
            excluded.append(f'{bot}: full-gate evidence incomplete or stale')
            continue
        panel = identity({k: suite[k] for k in ('maps', 'opponents', 'engine_lock_hash')})
        games = metrics['wins'] + metrics['losses']
        candidates.append({'bot': bot, 'commit': row['commit_sha'], 'source_hash': row['source_hash'],
                           'evaluation_id': row['id'], 'panel': panel,
                           'score': metrics['wins'] / games if games else 0})
    if len({c['panel'] for c in candidates}) > 1:
        blockers.append('lane champions need the same frozen comparison panel')
    if not candidates:
        blockers.append('no full-gate eligible improvement')
    leader = None
    if not blockers and candidates:
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
    interval = arena.config.get('official_schedule', {}).get('check_interval_seconds', 5 * 3600)
    if now - arena.db.get('official_last_upload_at', 0) < interval:
        blockers.append('five-hour submission interval')
    # Deliberately impossible to enable via configuration: implement only after interface review.
    blockers.append('official adapter not verified: upload activation effects, event policies, quotas and challenge interface')
    return {'enabled': False, 'candidate': leader, 'stable_seconds': stable,
            'schedule': cadence_status(arena, leader, now),
            'selection_scope':'best among full-gate eligible evaluated lane champions', 'excluded_lanes':excluded,
            'blockers': blockers, 'login_required_every_days': 7,
            'platform_submission_quota': 'unverified', 'max_outstanding_challenges': 1,
            'unknown_remote_creation': 'stop and reconcile; never blindly retry'}
