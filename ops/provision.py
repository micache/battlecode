"""Provision only the pilot identities; authentication remains an owner action."""
import grp
import json
import os
from pathlib import Path
import pwd
import re
import subprocess


def provision_users(bots=("alpha", "beta")):
    if os.geteuid() != 0:
        raise RuntimeError("administrator/root required to provision Linux users")
    path = Path("/etc/battlecode/users.json")
    recorded = json.loads(path.read_text()) if path.exists() else {}
    if not bots or any(not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,31}', bot) for bot in bots):
        raise RuntimeError("invalid bot registration")
    names = ("bc-arena", *(f"bc-{bot}" for bot in bots))
    for name in names:
        try:
            account = pwd.getpwnam(name)
        except KeyError:
            continue
        if (name not in recorded or recorded[name]["uid"] != account.pw_uid or
                recorded[name]["home"] != account.pw_dir or account.pw_uid == 0):
            raise RuntimeError(f"unregistered existing identity {name}; inspect before adopting")
    for name in ("bc-read", *(f"bc-{bot}" for bot in bots)):
        expected_gid = recorded.get('bc-arena' if name == 'bc-read' else name, {}).get('gid')
        try:
            group = grp.getgrnam(name)
            if expected_gid is not None and group.gr_gid != expected_gid:
                raise RuntimeError(f'registered group ID changed: {name}')
        except KeyError:
            subprocess.run(["groupadd", *(['--gid', str(expected_gid)] if expected_gid is not None else []), name], check=True)
    path.parent.mkdir(mode=0o755, exist_ok=True)
    for name in names:
        if name in recorded:
            try:
                pwd.getpwnam(name)
            except KeyError:
                info = recorded[name]
                subprocess.run(['useradd', '--no-create-home', '--shell', '/bin/bash', '--uid', str(info['uid']),
                                '--gid', str(info['gid']), '--home-dir', info['home'], name], check=True)
        if name not in recorded:
            subprocess.run(["useradd", "--create-home", "--shell", "/bin/bash", "--gid",
                            "bc-read" if name == "bc-arena" else name, name], check=True)
            account = pwd.getpwnam(name)
            recorded[name] = {"uid": account.pw_uid, "gid": account.pw_gid, "home": account.pw_dir}
            pending = path.with_suffix(".pending")
            pending.write_text(json.dumps(recorded, indent=2) + "\n")
            pending.chmod(0o644)
            os.replace(pending, path)
        subprocess.run(["usermod", "--append", "--groups",
                        ",".join(f"bc-{bot}" for bot in bots) if name == "bc-arena" else "bc-read", name], check=True)
        Path(recorded[name]["home"]).chmod(0o700)
    return {"users": recorded, "owner_authentication": "manual; no credentials copied"}


if __name__ == "__main__":
    print(json.dumps(provision_users(), indent=2))
