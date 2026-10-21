"""Continuous low-priority development self-play, separate from promotion.

One frozen round-robin at a time. No model calls, mutable bot checkouts, seed
overrides or synthetic strategy variants. Repeated inputs are recorded honestly.
"""
import itertools
import json
import time

from .common import fresh_id, identity


def roster(arena):
    """Latest reliability-valid evaluated source per enabled lane; not a champion."""
    chosen = {}
    for bot, worker in sorted(arena.config['workers'].items()):
        if not worker['enabled'] or not worker['owner_confirmed']:
            continue
        for row in arena.db.all('SELECT r.id,r.commit_sha,r.source_hash,e.metrics,e.suite FROM evaluations e '
                                'JOIN revisions r ON r.id=e.revision_id WHERE e.bot_id=? '
                                'AND e.finished IS NOT NULL AND e.metrics IS NOT NULL ORDER BY e.created DESC', (bot,)):
            metrics, suite = json.loads(row.pop('metrics')), json.loads(row.pop('suite'))
            if (suite['engine_lock_hash'] != arena.adapter().lock_hash or
                    metrics.get('missing') or metrics.get('fault_matches') or metrics.get('unknown_reliability') or
                    not metrics.get('wins', 0) + metrics.get('losses', 0)):
                continue
            chosen[bot] = dict(row, build=arena.build(row['id']))
            break
    boss=arena.config.get('boss',{})
    if boss.get('enabled'):
        row=arena.db.one('SELECT id,commit_sha,source_hash FROM revisions WHERE id=?',(boss['revision_id'],))
        chosen['boss']=dict(row,build=arena.build(row['id']))
    return chosen


def replenish(arena):
    db = arena.db
    if (not arena.config['limits'].get('continuous_matches', False) or db.get('paused', True) or
            db.get('disk_pressure', False) or db.get('adapter_paused', False) or not db.get('starter_verified', False)):
        return None
    active = db.one("SELECT * FROM training_rounds WHERE state='RUNNING' ORDER BY created LIMIT 1")
    if active:
        spec = json.loads(active['spec'])
        jobs = db.all('SELECT j.id,j.state FROM training_cases t JOIN match_jobs j ON j.id=t.job_id '
                      'WHERE t.round_id=?', (active['id'],))
        changed = (spec['engine_lock_hash'] != arena.adapter().lock_hash or
                   spec['infrastructure_commit'] != arena.config['infrastructure_commit'] or
                   spec.get('boss_revision')!=arena.config.get('boss',{}).get('revision_id'))
        if changed:
            with db.transaction():
                for job in jobs:
                    db.execute("UPDATE match_jobs SET state='CANCELLED' WHERE id=? AND state='QUEUED'", (job['id'],))
                db.execute("UPDATE training_rounds SET state='SUPERSEDED',finished=? WHERE id=?",
                           (time.time(), active['id']))
        elif any(job['state'] in ('QUEUED','RUNNING') for job in jobs):
            return active['id']
        else:
            db.execute('UPDATE training_rounds SET state=?,finished=? WHERE id=?',
                       ('COMPLETED' if all(j['state']=='COMPLETED' for j in jobs) else 'INCONCLUSIVE',
                        time.time(), active['id']))
    # Evaluation/smoke work runs first; prepare another frozen training round
    # only when it has no jobs to serve. The queue stays bounded to one round.
    if db.one("SELECT id FROM match_jobs WHERE state IN ('QUEUED','RUNNING') LIMIT 1"):
        return None
    selected = roster(arena)
    if len(selected) < 2:
        return None
    maps = arena.freeze_maps()
    maps = {name:maps[name] for name in arena.config['evaluation']['development_maps']}
    round_id = fresh_id('training')
    spec = {'protocol_version':1,'engine_lock_hash':arena.adapter().lock_hash,
            'infrastructure_commit':arena.config['infrastructure_commit'], 'maps':maps,
            'roster':selected, 'independent_reruns':False,
            'boss_revision':arena.config.get('boss',{}).get('revision_id'),
            'purpose':'Continuous development self-play, never promotion or official submission evidence.'}
    with db.transaction():
        db.execute("INSERT INTO training_rounds VALUES(?,?,'RUNNING',?,NULL)",
                   (round_id,json.dumps(spec),time.time()))
        for name,map_info in maps.items():
            for a_bot,b_bot in itertools.permutations(selected,2):
                a,b = selected[a_bot],selected[b_bot]
                job_id = arena.queue_match(a['build'],b['build'],map_info,
                                           training_round={'id':round_id,'a_bot':a_bot,'b_bot':b_bot})
                match_spec = json.loads(db.one('SELECT spec FROM match_jobs WHERE id=?',(job_id,))['spec'])
                inputs = {k:v for k,v in match_spec.items()
                          if k not in ('training_round','job_id','map_path') and not k.endswith('snapshot')}
                db.execute('INSERT INTO training_cases VALUES(?,?,?,?,?,?,?,?)',
                           (job_id,round_id,a_bot,b_bot,a['id'],b['id'],name,identity(inputs)))
    return round_id


def status(arena):
    active = arena.db.one("SELECT * FROM training_rounds ORDER BY created DESC LIMIT 1")
    result = {'enabled':arena.config['limits'].get('continuous_matches',False),
              'priority':'below evaluations and smoke checks',
              'maps':f"{len(arena.config['evaluation']['development_maps'])} development maps; both sides",
              'coding_interval_seconds':arena.config['limits'].get('improvement_interval_seconds',3600),
              'model_pauses_do_not_stop_games':True,'independent_reruns':False}
    result['rounds'] = arena.db.all('SELECT state,count(*) AS count FROM training_rounds GROUP BY state')
    if active:
        spec = json.loads(active['spec'])
        result.update(round_id=active['id'],round_state=active['state'],
                      roster={bot:{k:v for k,v in row.items() if k!='build'} for bot,row in spec['roster'].items()},
                      jobs=arena.db.all('SELECT j.state,count(*) AS count FROM training_cases t '
                                        'JOIN match_jobs j ON j.id=t.job_id WHERE t.round_id=? GROUP BY j.state',
                                        (active['id'],)))
    return result


def window(arena, bot, since):
    """Bounded handoff: unique-input outcomes, repeats and readable loss references."""
    rows = arena.db.all('SELECT t.*,j.spec,j.result,j.state,ra.commit_sha AS a_commit,rb.commit_sha AS b_commit '
        'FROM training_cases t JOIN match_jobs j ON j.id=t.job_id '
        'JOIN revisions ra ON ra.id=t.a_revision JOIN revisions rb ON rb.id=t.b_revision '
        'WHERE (t.a_bot=? OR t.b_bot=?) AND (j.created>=? OR EXISTS('
        'SELECT 1 FROM match_attempts a WHERE a.job_id=j.id AND a.finished>=?)) '
        'ORDER BY j.created DESC,j.id DESC LIMIT 2000', (bot,bot,since,since))
    groups, seen = {}, {}
    for row in rows:
        if row['map_name'] not in arena.config['evaluation']['development_maps']:
            continue
        spec = json.loads(row['spec'])
        own = 'a' if row['a_bot']==bot else 'b'
        enemy = 'b' if own=='a' else 'a'
        key = (spec[own+'_source_hash'],spec['engine_lock_hash'])
        group = groups.setdefault(key, {'source_hash':key[0],'commit':row[own+'_commit'],
            'engine_lock_hash':key[1],'completed_matches':0,'unique_input_cells':0,'repeat_matches':0,
            'wins':0,'losses':0,'noncompleted':0,'pending_matches':0,'fault_matches':0,'unknown_reliability':0,
            'repeat_outcome_disagreements':0,'by_map_side':{},'by_opponent':{},'examples':[],'metrics':{}})
        result = json.loads(row['result']) if row['result'] else {}
        if row['state'] in ('QUEUED','RUNNING'):
            group['pending_matches'] += 1
            continue
        if not result.get('completed') or row['state']!='COMPLETED':
            group['noncompleted'] += 1
            continue
        group['completed_matches'] += 1
        group['fault_matches'] += int(bool(result.get('bot_faults')))
        group['unknown_reliability'] += int(result.get('bot_faults') is None)
        observation_key = (row['input_identity'],own)
        if observation_key in seen:
            group['repeat_matches'] += 1
            group['repeat_outcome_disagreements'] += int(seen[observation_key] != result.get('winner'))
            continue
        seen[observation_key] = result.get('winner')
        group['unique_input_cells'] += 1
        won = result.get('winner')==own.upper()
        group['wins' if won else 'losses'] += 1
        cell = group['by_map_side'].setdefault(row['map_name']+'/'+own.upper(),[0,0])
        cell[0 if won else 1] += 1
        opponent = spec[enemy+'_source_hash']
        record = group['by_opponent'].setdefault(opponent,{'commit':row[enemy+'_commit'],'wins':0,'losses':0})
        record['wins' if won else 'losses'] += 1
        if not won and len(group['examples'])<3:
            group['examples'].append({'match_id':row['job_id'],'side':own.upper(),'map':row['map_name'],
                                      'opponent_commit':row[enemy+'_commit']})
        for name,measurement in result.get('metrics',{}).items():
            if measurement.get('available'):
                value = measurement.get('value')
                if isinstance(value,dict):
                    value = value.get(own.upper())
                if isinstance(value,(float,int)) and not isinstance(value,bool):
                    stat = group['metrics'].setdefault(name,{'sum':0,'observations':0})
                    stat['sum'] += value
                    stat['observations'] += 1
    for group in groups.values():
        group['metrics'] = {k:{'mean':v['sum']/v['observations'],'observations':v['observations']}
                            for k,v in group['metrics'].items()}
    return {'source_groups':list(groups.values())[:8],'omitted_source_groups':max(0,len(groups)-8),
            'window_limit_reached':len(rows)==2000,
            'interpretation':'Self-play only; separate from promotion scores. Wins/losses deduplicate identical '
                'inputs within this window; repeat_matches counts additional executions, not independent evidence. '
                'Sources, opponent commits, sides and engine identities remain explicit; no holdout traces. '
                'Fault counts describe the match, not necessarily the owning side. Replays/statistics remain canonical.'}
