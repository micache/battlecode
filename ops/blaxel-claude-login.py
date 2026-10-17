#!/usr/bin/env python3
"""Private terminal bridge to native Claude subscription login. Never paste codes in chat."""
import argparse
import getpass
import json
import re
import time
import uuid

from blaxel import APIError, Client, CREDENTIALS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bot', default='gamma', nargs='?')
    parser.add_argument('--process', help='attach to an already started owner login')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,28}', args.bot):
        parser.error('invalid bot identity')
    credentials = json.loads(CREDENTIALS.read_text())
    client = Client(credentials['key'], credentials['workspace'])
    endpoint = client.endpoint()
    name = args.process or f'{args.bot}-login-{uuid.uuid4().hex[:12]}'
    if not re.fullmatch(r'[a-z0-9-]+', name):
        parser.error('invalid process identity')
    expected = f"runuser -l bc-{args.bot} -c 'USE_BUILTIN_RIPGREP=0 DISABLE_AUTOUPDATER=1 /usr/local/bin/claude auth login --claudeai'"
    attached = bool(args.process)
    if not attached:
        try:
            existing = client.request('GET', f'/process/{args.bot}-owner-login', base=endpoint)
        except APIError as exc:
            if exc.code != 404:
                raise
        else:
            if existing.get('command') == expected and existing.get('status') == 'running' and existing.get('stdin'):
                name, attached = f'{args.bot}-owner-login', True
    if not attached:
        client.request('POST', '/process', {'name':name, 'command':expected,
                       'stdin':True, 'keepAlive':True, 'waitForCompletion':False, 'timeout':1800}, base=endpoint)
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        status = client.request('GET', f'/process/{name}', base=endpoint)
        if status.get('command') != expected or not status.get('stdin'):
            raise SystemExit('not the expected native subscription-login process; no code sent')
        if status.get('status') != 'running':
            raise SystemExit('login process stopped; run this helper again without --process for a fresh login')
        urls = re.findall(r'https://claude\.com/[^\s]+', status.get('stdout', ''))
        if urls:
            break
        time.sleep(1)
    else:
        raise SystemExit('no authorization URL; inspect process without reading credential files')
    print('Open this native Claude subscription authorization URL in your browser:\n' + urls[-1])
    print('Choose your subscription account; do not enable Console or extra paid usage.')
    code = getpass.getpass('Paste the one-time authorization code HERE (hidden, never in chat): ').strip()
    if not code or len(code) > 4096 or any(ch in code for ch in '\r\n'):
        raise SystemExit('invalid authorization code')
    try:
        client.request('POST', f'/process/{name}/stdin', (code + '\n').encode(), base=endpoint)
    except APIError as exc:
        raise SystemExit(f'Code delivery returned HTTP {exc.code}; do not retry automatically; inspect native login status') from None
    del code
    for _ in range(60):
        status = client.request('GET', f'/process/{name}', base=endpoint)
        if status.get('status') != 'running':
            print('Native login finished; exit code:', status.get('exitCode'))
            print('Tell the arena operator "gamma login done". Do not send codes or tokens.')
            return
        time.sleep(1)
    print('Login still pending. Tell the arena operator; no credentials were copied or printed.')


if __name__ == '__main__':
    main()
