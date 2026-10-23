"""Progress, not just process liveness. No model or network calls."""
import time


def progress(status, db, limits, now=None):
    now=time.time() if now is None else now
    queued=sum(r['count'] for r in status['matches'] if r['state']=='QUEUED')
    last=db.one('SELECT max(finished) AS finished FROM match_attempts')['finished']
    age=max(0,now-last) if last is not None else None
    threshold=max(1800,2*(limits.get('match_timeout_seconds',300)+limits.get('build_timeout_seconds',300)))
    if status['paused']:state,reason='PAUSED','operator pause'
    elif status['adapter_paused']:state,reason='ADAPTER_BLOCKED',status['adapter_paused']
    elif status['service_error']:state,reason='ERROR',status['service_error']
    elif status['disk']['free']<limits['minimum_free_bytes']:
        state,reason='STORAGE_BLOCKED','physical free-space safety floor'
    elif not limits.get('rolling_history',False) and status['disk']['artifact_bytes']>=limits['artifact_budget_bytes']:
        state,reason='STORAGE_BLOCKED','non-rolling artifact cap'
    elif queued and (age is None or age>threshold):
        state,reason='STALLED','queued games without completed-match progress'
    else:state,reason=('WORKING',None) if queued else ('IDLE',None)
    return {'state':state,'reason':reason,'queued_games':queued,'last_match_finished_at':last,
            'seconds_since_match':age,'stall_threshold_seconds':threshold,
            'history_target_exceeded':status['disk']['artifact_bytes']>=limits['artifact_budget_bytes']}
