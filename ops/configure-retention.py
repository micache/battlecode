#!/usr/bin/env python3
"""Enable bounded local history, with services stopped. Never touches credentials."""
import fcntl
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, read_json, require


def main():
    require(os.geteuid()==0, 'administrator required; stop services first')
    handles = []
    for path in ('/srv/battlecode/state/service.lock', '/srv/battlecode/model.lock'):
        handle = open(path, 'a')
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        handles.append(handle)
    config = read_json('/etc/battlecode/arena.json')
    config['limits']['rolling_history'] = True
    config['limits']['archive_completed_projects'] = False
    config['limits']['artifact_budget_bytes'] = 768*1024**2
    atomic_json('/etc/battlecode/arena.json', config, 0o644)
    import pwd
    owner = pwd.getpwnam('bc-arena')
    os.setgroups(os.getgrouplist(owner.pw_name,owner.pw_gid))
    os.setgid(owner.pw_gid)
    os.setuid(owner.pw_uid)
    # Public prepared offload batches are redundant copies; original match
    # worktrees remain untouched until the single-writer retention pass.
    from arena.service import Arena
    arena = Arena(config)
    try:
        pending = arena.db.get('offload_pending')
        if pending:
            import re
            batch = pending['batch_id']
            require(re.fullmatch('[a-f0-9]{64}',batch), 'unexpected pending batch')
            path = Path(pending['archive_path'])
            require(path.parent.resolve()==(arena.root/'public/offload').resolve() and
                    path.name in (batch+'.tar',batch+'.tar.xz') and not path.is_symlink(), 'unsafe pending archive')
            arena.db.put('offload_abandoned:'+batch, dict(pending, reason='owner selected rolling local history'))
            arena.db.put('offload_pending', None)
            path.unlink(missing_ok=True)
        print(json.dumps({'rolling_history':True,'artifact_budget_bytes':config['limits']['artifact_budget_bytes'],
                          'offloading':False,'source_commits_and_compact_results':'retained',
                          'old_routine_raw_history':'permanently pruned oldest first','services_started':False}))
    finally:
        arena.db.connection.close()


if __name__=='__main__':
    main()
