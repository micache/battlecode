#!/usr/bin/env python3
"""Stopped setup: preserve the verified team bot as a read-only shared boss."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0,'/opt/battlecode')
from arena.common import atomic_json,lock,read_json,require
from arena.config import load


INSTALL='''import json,sys
from pathlib import Path
sys.path.insert(0,'/opt/battlecode')
from arena.common import atomic_json,lock,read_json,require
from arena.config import load
from arena.service import Arena
from arena.boss import register
config=load('/etc/battlecode/arena.json')
with lock(Path(config['root'])/'state/service.lock'),lock(Path(config['root'])/'model.lock'):
 a=Arena(config)
 require(not a.db.one("SELECT id FROM workers WHERE state='RUNNING'"),'model writer still active')
 result=register(a,read_json(sys.argv[1]))
 atomic_json(Path(config['root'])/'public/team-boss-registration.json',result,420)
 print(json.dumps(result))
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-envelope',required=True,type=Path)
    args=parser.parse_args()
    require(os.geteuid()==0,'administrator required')
    path=Path('/etc/battlecode/arena.json');old=load(path)
    # The child owns the sole SQLite writer and its native credentials remain private.
    result=subprocess.run(['python3','/opt/battlecode/ops/as-arena.py','python3','-c',INSTALL,
                           str(args.source_envelope)],capture_output=True,text=True,check=True)
    boss=json.loads(result.stdout)
    with lock(Path(old['root'])/'state/service.lock'),lock(Path(old['root'])/'model.lock'):
        config=read_json(path);atomic_json(path.with_name('arena.before-boss-'+str(time.time_ns())+'.json'),config,0o600)
        from arena.exploration import resolved_policy
        previous=resolved_policy(config)
        sources=[*previous.get('shared_sources',[])]
        if previous.get('submission_id'):sources.append({k:previous[k] for k in
            ['bot_id','source_commit','source_hash','submission_id']})
        config['boss']=boss
        config['official_exploration']={**config['official_exploration'],
            **{k:boss[k] for k in ['bot_id','source_commit','source_hash','submission_id','package_sha256','team_id']},
            'enabled':True,'owner_authorized':True,'awaiting_submission':False,'require_selection_proof':True,
            'feedback_bot_id':'alpha','shared_sources':sources,'authorization':boss['authorization']}
        config['official']['challenges']=True
        state_path=Path(config['root'])/'official-exploration/state.json'
        state=read_json(state_path);detail=state.get('blocked')
        require(not detail or detail=='Team selected a different submission; review source mapping',
                'different external stop requires review; not cleared by boss selection')
        require(not any(read_json(p)['state']=='UNKNOWN' for p in state_path.parent.glob('requests/*/record.json')),
                'unknown external creation must be reconciled')
        atomic_json(path,config,0o644);load(path)
        owner=state_path.stat();state.update(blocked=None,next_create=time.time()+5,waiting='AWAITING_VERIFIED_SOURCE_SELECTION')
        state['reviewed_source_change']={'at':time.time(),'previous_stop':detail,'new_submission':boss['submission_id']}
        atomic_json(state_path,state,0o600);os.chown(state_path,owner.st_uid,owner.st_gid)
        print(json.dumps({'boss':boss,'services_started':False,'official_uploads_or_activation':False}))


if __name__=='__main__':main()
