#!/usr/bin/env python3
"""Root-only host preparation; never authenticates owners or runs model jobs."""
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def main():
    if os.geteuid() != 0 or not Path('/persist').is_mount():
        raise RuntimeError('root and a mounted persistent volume required')
    # Fresh provider volumes default to root-only; owners need traversal, not listing.
    Path('/persist').chmod(0o711)
    data = Path('/var/lib/battlecode-volume')
    if not data.is_mount():
        raise RuntimeError('run blaxel-volume.py first; POSIX volume must be mounted')
    for target, persisted in (('/etc/battlecode', str(data / 'config')), ('/srv/battlecode', str(data / 'arena'))):
        destination = Path(persisted)
        destination.mkdir(mode=0o755, parents=True, exist_ok=True)
        if target == '/etc/battlecode':
            destination.chmod(0o755)
        link = Path(target)
        link.parent.mkdir(parents=True, exist_ok=True)
        if not link.exists():
            link.symlink_to(destination, target_is_directory=True)
        elif not link.is_symlink() or link.resolve() != destination:
            raise RuntimeError(f'refusing to replace existing {target}')
    # Old image versions may not honor the API-isolation environment flag.
    # Explicitly deny workload UIDs and nested/forwarded traffic to the root API.
    for rule in (['OUTPUT', '-p', 'tcp', '--dport', '8080', '-m', 'owner', '!', '--uid-owner', '0',
                  '-j', 'REJECT', '--reject-with', 'tcp-reset'],
                 ['FORWARD', '-p', 'tcp', '--dport', '8080', '-j', 'REJECT', '--reject-with', 'tcp-reset']):
        check = subprocess.run(['iptables', '-C', *rule], capture_output=True)
        if check.returncode:
            run('iptables', '-I', *rule)
    from provision import provision_users
    provision_users()
    for name in ('bc-arena', 'bc-alpha', 'bc-beta'):
        home = Path(pwd.getpwnam(name).pw_dir)
        target = data / 'homes' / name
        target.parent.mkdir(mode=0o755, exist_ok=True)
        target.parent.chmod(0o755)
        if not target.exists():
            if (home / '.codex').exists() or (home / '.ssh').exists():
                raise RuntimeError('refusing to copy an authenticated home; use a fresh owner identity')
            shutil.copytree(home, target)
            home.rename(home.with_name(home.name + '.initial-home'))
            home.symlink_to(target, target_is_directory=True)
        elif not home.is_symlink() or home.resolve() != target:
            raise RuntimeError('existing persistent home requires explicit recovery, never overwrite')
        user = pwd.getpwnam(name)
        target.chmod(0o700)
        os.chown(target, user.pw_uid, user.pw_gid)
        if target.stat().st_uid != user.pw_uid:
            raise RuntimeError('persistent filesystem does not honor owner IDs')
    root = Path('/sys/fs/cgroup')
    (root / 'cgroup.subtree_control').write_text('+cpu +memory +pids')
    delegated = root / 'battlecode-arena'
    delegated.mkdir(exist_ok=True)
    (delegated / 'cgroup.subtree_control').write_text('+cpu +memory +pids')
    leaf = delegated / 'service'
    leaf.mkdir(exist_ok=True)
    arena = pwd.getpwnam('bc-arena')
    for path in (delegated, delegated / 'cgroup.procs', delegated / 'cgroup.subtree_control',
                 delegated / 'cgroup.threads', leaf, leaf / 'cgroup.procs', leaf / 'cgroup.threads'):
        os.chown(path, arena.pw_uid, arena.pw_gid)
    runtime = Path('/run/battlecode-arena')
    runtime.mkdir(mode=0o700, exist_ok=True)
    os.chown(runtime, arena.pw_uid, arena.pw_gid)
    for filename in ('/etc/subuid', '/etc/subgid'):
        path = Path(filename)
        text = path.read_text() if path.exists() else ''
        if not any(row.startswith('bc-arena:') for row in text.splitlines()):
            for row in text.splitlines():
                _, start, count = row.split(':')
                if int(start) < 265536 and int(start) + int(count) > 200000:
                    raise RuntimeError('subordinate ID range collision')
            with path.open('a') as handle:
                handle.write('bc-arena:200000:65536\n')
    print(json.dumps({'users_created': ['bc-arena', 'bc-alpha', 'bc-beta'],
                      'persistent_homes': True, 'local_api_firewall': 'installed',
                      'delegated_cgroup': str(delegated), 'owner_login': 'manual'}))


if __name__ == '__main__':
    main()
