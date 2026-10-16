"""Provision only the pilot identities; authentication remains an owner action."""
import grp
import json
import os
from pathlib import Path
import pwd
import subprocess


def provision_users():
    if os.geteuid() != 0:
        raise RuntimeError("administrator/root required to provision Linux users")
    path = Path("/etc/battlecode/users.json")
    recorded = json.loads(path.read_text()) if path.exists() else {}
    names = ("bc-arena", "bc-alpha", "bc-beta")
    for name in names:
        try:
            account = pwd.getpwnam(name)
        except KeyError:
            continue
        if (name not in recorded or recorded[name]["uid"] != account.pw_uid or
                recorded[name]["home"] != account.pw_dir or account.pw_uid == 0):
            raise RuntimeError(f"unregistered existing identity {name}; inspect before adopting")
    for name in ("bc-read", "bc-alpha", "bc-beta"):
        try:
            grp.getgrnam(name)
        except KeyError:
            subprocess.run(["groupadd", name], check=True)
    path.parent.mkdir(mode=0o755, exist_ok=True)
    for name in names:
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
                        "bc-alpha,bc-beta" if name == "bc-arena" else "bc-read", name], check=True)
        Path(recorded[name]["home"]).chmod(0o700)
    return {"users": recorded, "owner_authentication": "manual; no credentials copied"}


if __name__ == "__main__":
    print(json.dumps(provision_users(), indent=2))
