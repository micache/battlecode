#!/usr/bin/env python3
"""Register one additional owner lane while services are stopped; never log in."""
import argparse
import json
import os
from pathlib import Path
import pwd
import shutil
import sys

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, lock, read_json, require, slug
from provision import provision_users


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bot')
    args = parser.parse_args()
    require(os.geteuid() == 0, 'administrator required; stop services first')
    bot = slug(args.bot)
    require(bot not in ('starter', 'arena', 'read'), 'reserved infrastructure identity')
    require(len(bot) <= 28, 'Linux username length limit')
    path = Path('/etc/battlecode/arena.json')
    config = read_json(path)
    require(bot not in config['workers'], 'lane already exists; preserve its state')
    root = Path(config['root'])
    with lock(root / 'state/service.lock'), lock(root / 'model.lock'):
        provision_users((*config['workers'], bot))
        user, arena = pwd.getpwnam(f'bc-{bot}'), pwd.getpwnam('bc-arena')
        home = Path(user.pw_dir)
        if config.get('deployment', {}).get('mode') == 'blaxel':
            target = Path('/var/lib/battlecode-volume/homes') / user.pw_name
            require(not target.exists() and not (home / '.codex').exists(), 'fresh identity required')
            shutil.copytree(home, target)
            home.rename(home.with_name(home.name + '.initial-home'))
            home.symlink_to(target, target_is_directory=True)
            os.chown(target, user.pw_uid, user.pw_gid)
        home.chmod(0o700)
        runtime = home / '.runtime'
        runtime.mkdir(mode=0o700)
        os.chown(runtime, user.pw_uid, user.pw_gid)
        for name in ('inbox', 'outbox', 'tasks', 'feedback', 'external-inbox'):
            directory = root / name / bot
            directory.mkdir()
            os.chown(directory, arena.pw_uid, user.pw_gid)
            directory.chmod(0o2770 if name in ('inbox', 'external-inbox') else 0o2750)
        config['workers'][bot] = {'linux_user':user.pw_name, 'branch':f'bot/{bot}',
                                 'clone':str(home / 'battlecode'), 'enabled':False, 'owner_confirmed':False}
        binary = '/usr/local/bin/codex'
        owner = {'protocol_version':1, 'bot_id':bot, 'linux_user':user.pw_name, 'branch':f'bot/{bot}',
                 'root':str(root), 'infrastructure':config['infrastructure'], 'read_repository':config['mirror'],
                 'clone':str(home / 'battlecode'), 'attempts':str(home / 'attempts'),
                 'codex_executable':binary, 'codex_sha256':file_hash(binary), 'model':None}
        atomic_json(path.with_name(f'{bot}.json'), owner, 0o644)
        atomic_json(path, config, 0o644)
    print(json.dumps({'registered':bot, 'enabled':False,
        'next':['Publish/ingest its starter with ops/bootstrap-lanes.py as bc-arena.',
                f'Owner: runuser -l bc-{bot} -c "/usr/local/bin/codex login --device-auth"',
                'Attest distinct account ownership, establish baseline, then explicitly resume the lane.']}))


if __name__ == '__main__':
    main()
