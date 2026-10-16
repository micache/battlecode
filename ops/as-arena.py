#!/usr/bin/env python3
"""Root operator helper: enter the delegated cgroup, then drop to bc-arena."""
import os
from pathlib import Path
import pwd
import sys

if os.geteuid() != 0 or len(sys.argv) < 2:
    raise SystemExit('administrator and command required')
user = pwd.getpwnam('bc-arena')
Path('/sys/fs/cgroup/battlecode-arena/service/cgroup.procs').write_text(str(os.getpid()))
os.setgroups(os.getgrouplist(user.pw_name, user.pw_gid))
os.setgid(user.pw_gid)
os.setuid(user.pw_uid)
os.environ.clear()
os.environ.update(HOME=user.pw_dir, USER=user.pw_name, LOGNAME=user.pw_name, LANG='C.UTF-8',
                  PATH='/usr/local/bin:/usr/bin:/bin', XDG_RUNTIME_DIR='/run/battlecode-arena')
os.chdir('/opt/battlecode')
os.execvp(sys.argv[1], sys.argv[1:])
