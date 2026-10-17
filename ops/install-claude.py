#!/usr/bin/env python3
"""Install one reviewed native Claude binary globally; no login or API billing."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

BASE = 'https://downloads.claude.ai/claude-code-releases'


def main():
    if os.geteuid() != 0:
        raise SystemExit('administrator required; stop services first')
    target = Path('/usr/local/bin/claude')
    if target.exists():
        raise SystemExit('Claude already installed; preserve and review its version before upgrading')
    subprocess.run(['apk', 'add', '--no-cache', 'bash', 'curl', 'libgcc', 'libstdc++', 'ripgrep',
                    'bubblewrap', 'socat'], check=True)
    version = urllib.request.urlopen(BASE + '/latest', timeout=30).read(100).decode().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise SystemExit('invalid official release version')
    manifest = json.load(urllib.request.urlopen(f'{BASE}/{version}/manifest.json', timeout=30))
    platform = 'linux-x64-musl'
    checksum = manifest['platforms'][platform]['checksum']
    if not re.fullmatch(r'[0-9a-f]{64}', checksum):
        raise SystemExit('missing official checksum')
    temporary = target.with_suffix('.pending')
    digest = hashlib.sha256()
    with urllib.request.urlopen(f'{BASE}/{version}/{platform}/claude', timeout=90) as response, temporary.open('xb') as out:
        while block := response.read(1024 * 1024):
            out.write(block)
            digest.update(block)
        out.flush()
        os.fsync(out.fileno())
    if digest.hexdigest() != checksum:
        raise SystemExit('checksum mismatch; pending download retained, not installed')
    temporary.chmod(0o755)
    temporary.rename(target)
    subprocess.run([str(target), '--version'], check=True, env={**os.environ, 'USE_BUILTIN_RIPGREP':'0',
                                                             'DISABLE_AUTOUPDATER':'1'})
    print(json.dumps({'version':version, 'platform':platform, 'sha256':checksum,
                      'installed':str(target), 'authenticated':False}))


if __name__ == '__main__':
    main()
