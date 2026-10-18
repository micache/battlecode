#!/usr/bin/env python3
"""Stopped-service recovery for the own-smoke evidence authorization bug.

Run as bc-arena. Validate access before resuming each explicitly named lane.
Keep the historical BLOCKED result, source, notes and checkpoint unchanged;
the next bounded worker task reviews its preserved work, never blindly pushes it.
This is not an auth/quota/permission bypass or a general auto-resume policy.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import lock, require
from arena.config import load
from arena.service import Arena
from arena.supervisor import handle_request


def resolve(arena, bot):
    require(bot in arena.config['workers'], 'unregistered bot')
    worker = arena.db.one('SELECT * FROM workers WHERE id=?', (bot,))
    task = arena.db.one('SELECT * FROM tasks WHERE id=? AND bot_id=?', (worker['task_id'], bot))
    require(task, 'no preserved task')
    receipt_key = 'smoke-access-recovery:' + task['id']
    receipt = arena.db.get(receipt_key)
    if receipt:
        return dict(receipt, already_resolved=True)
    require(arena.db.get('paused', False), 'pause scheduling first')
    require(worker['state']=='PAUSED' and not worker['paused'] and worker['lease_owner']=='server' and
            task['state']=='PAUSED' and task['published_commit'] is None, 'not a stopped server-owned attempt')
    result = json.loads(task['result'])
    reason = result.get('blocked_reason', '')
    require(result['outcome']=='BLOCKED' and reason==worker['detail'] and
            ('smoke-log export was denied' in reason or 'smoke-log exports were denied' in reason),
            'not the known smoke evidence-access blocker; review independently')
    report = arena.db.one("SELECT value FROM meta WHERE key LIKE ? "
                          "ORDER BY json_extract(value,'$.finished') DESC LIMIT 1", (f"check:{task['id']}:%",))
    require(report, 'no preserved check')
    check = json.loads(report['value'])
    require(check['state']=='PASSED' and len(check['matches'])==2, 'no passed both-side check')
    probes = []
    for job in check['matches']:
        for filename in ('final.json', 'bot-a.stdout.log', 'bot-b.stdout.log'):
            response = handle_request(arena, bot, {'operation':'slice',
                'payload':{'match_id':job, 'file':filename, 'limit':128}})
            probes.append({'match_id':job, 'file':filename, 'size':response['size']})
    summary = ('Own smoke-log access is repaired and verified. The prior checked candidate was not published. '
               'Inspect the prior task source/notes/checkpoint under your own attempts_root, recover useful work, '
               'and run bot-check for the current task before returning READY_FOR_EVAL.')
    with arena.db.transaction():
        handle_request(arena, bot, {'operation':'resume'})
        arena.db.execute('UPDATE workers SET detail=NULL WHERE id=?', (bot,))
        receipt = {'bot':bot, 'task_id':task['id'], 'at':time.time(), 'probes':probes,
                   'infrastructure_commit':arena.config['infrastructure_commit'],
                   'source_hash':check['source_hash'], 'original_result_and_checkpoint':'unchanged',
                   'summary':summary}
        arena.db.put('task_infrastructure:' + task['id'], {'summary':summary, 'recovery':receipt_key})
        arena.db.put(receipt_key, receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bot', action='append', required=True)
    args = parser.parse_args()
    require(os.geteuid()!=0, 'run as the arena user, never write SQLite as root')
    config = load('/etc/battlecode/arena.json')
    with lock(Path(config['root'])/'state/service.lock', blocking=False), \
            lock(Path(config['root'])/'model.lock', blocking=False):
        arena = Arena(config)
        try:
            for bot in args.bot:
                print(json.dumps(resolve(arena, bot)), flush=True)
            arena.export_status()
        finally:
            arena.db.connection.close()


if __name__=='__main__':
    main()
