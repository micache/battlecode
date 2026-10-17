#!/usr/bin/env python3
"""Owner-controlled browser for read-only match inspection and UI downloads.

Uses a separate private browser profile, never an owner's existing auth files.
The owner signs in manually when required. It has no submission/challenge code.
JSON commands on stdin: snapshot, goto (same contest origin), click (button/link).
"""
import argparse
import json
from pathlib import Path
import hashlib
import re
import sys
import time
from urllib.parse import urlsplit
import uuid

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--match-id', required=True)
    parser.add_argument('--output', type=Path, default=Path.home() / '.local/share/battlecode-contest-downloads')
    args = parser.parse_args()
    uuid.UUID(args.match_id)
    args.output.mkdir(parents=True, exist_ok=True, mode=0o700)
    profile = Path.home() / '.local/share/battlecode-contest-browser'
    profile.mkdir(parents=True, exist_ok=True, mode=0o700)
    origin = 'https://2026a.battlecode.co.uk'
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from arena.common import atomic_json, file_hash
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(profile), headless=False,
                    accept_downloads=True, viewport={'width':1200, 'height':900})
        page = context.pages[0] if context.pages else context.new_page()

        active_group = {'id':None, 'downloads':0}
        observed = set()

        def download(item):
            target = args.output / (uuid.uuid4().hex + '-download.pending')
            item.save_as(target)
            digest = file_hash(target)
            directory = args.output / 'groups' / (active_group['id'] or 'unattributed')
            directory.mkdir(parents=True, exist_ok=True)
            final = directory / ('bundle-' + digest + '.zip')
            if final.exists():
                if file_hash(final) != digest:
                    raise ValueError('existing download changed')
                target.unlink()
            else:
                target.rename(final)
            atomic_json(directory / 'download.json', {'path':str(final), 'sha256':digest,
                        'bytes':final.stat().st_size, 'group_id':active_group['id'], 'downloaded_at':time.time()}, 0o600)
            active_group['downloads'] += 1
            print(json.dumps({'downloaded':str(final), 'bytes':final.stat().st_size}), flush=True)

        page.on('download', download)
        context.on('page', lambda new: new.on('download', download))

        def redact(value):
            if isinstance(value, dict):
                return {k:redact(v) for k,v in value.items() if not re.search(r'(^|_)(token|secret|authorization|cookie)($|_)', k, re.I)}
            if isinstance(value, list):
                return [redact(v) for v in value]
            if isinstance(value, str) and value.startswith('https://') and '?' in value:
                return value.split('?')[0] + '?[query-redacted]'
            return value

        def response(item):
            parsed = urlsplit(item.url)
            if parsed.netloc != '2026a.battlecode.co.uk' or item.request.method != 'GET':
                return
            if not parsed.path.startswith('/api/') or not re.search(r'/(matches|match-groups|submissions|teams|maps)(/|$)', parsed.path):
                return
            try:
                value = item.json()
            except Exception:
                return
            observed.add(item.url)
            name = hashlib.sha256(item.url.encode()).hexdigest()
            atomic_json(args.output / 'api' / (name + '.json'), {'path':parsed.path, 'status':item.status,
                        'response_redacted':redact(value), 'observed_at':time.time()}, 0o600)

        page.on('response', response)

        def snapshot():
            report = {'url':page.url.split('?')[0], 'title':page.title().split('?')[0] if 'Loading https://' not in page.title() else 'Replay download',
                  'body':page.locator('body').inner_text(),
                  'buttons':page.get_by_role('button').all_text_contents(),
                  'links':page.locator('a').evaluate_all('(items)=>items.map(a=>({text:a.textContent,href:a.getAttribute("href")}))')}
            report = redact(report)
            if page.url.startswith(origin + '/game/'):
                name = hashlib.sha256(page.url.split('?')[0].encode()).hexdigest()
                atomic_json(args.output / 'pages' / (name + '.json'), report, 0o600)
            report['body'] = report['body'][:16000]
            print(json.dumps(report), flush=True)

        def collect(group):
            uuid.UUID(group)
            active_group['id'] = group
            page.goto(origin + '/game/match-groups/' + group, wait_until='domcontentloaded', timeout=45000)
            page.wait_for_timeout(3500)
            body = page.locator('body').inner_text()
            if "Your team" not in body:
                raise ValueError('current-team membership not established; no downloads attempted')
            for label in ('Summary', 'Diagnostics'):
                for button in page.get_by_role('button', name=re.compile('^'+label)).all():
                    button.click()
                    page.wait_for_timeout(300)
            snapshot()
            buttons = page.get_by_role('button', name=re.compile(r'^Download \d+ games?'))
            if not buttons.count():
                print(json.dumps({'group':group, 'download':'unavailable', 'state':'inspect saved page/API metadata'}), flush=True)
                return
            if (args.output / 'groups' / group / 'download.json').exists():
                print(json.dumps({'group':group, 'download':'already preserved'}), flush=True)
                return
            before = active_group['downloads']
            buttons.first.click()
            deadline = time.monotonic() + 120
            while active_group['downloads'] == before and time.monotonic() < deadline:
                page.wait_for_timeout(1000)
            if active_group['downloads'] == before:
                raise ValueError('download not confirmed; inspect browser; no success claimed')

        page.goto(origin + '/game/match-groups/' + args.match_id, wait_until='domcontentloaded', timeout=45000)
        page.wait_for_timeout(5000)
        snapshot()
        for line in sys.stdin:
            try:
                command = json.loads(line)
                if command['operation'] == 'snapshot':
                    page.wait_for_timeout(1000)
                elif command['operation'] == 'goto':
                    url = command['url']
                    if not url.startswith(origin + '/game/'):
                        raise ValueError('only contest game navigation allowed')
                    page.goto(url, wait_until='domcontentloaded', timeout=45000)
                    page.wait_for_timeout(3000)
                elif command['operation'] == 'click':
                    if command['role'] not in ('button', 'link'):
                        raise ValueError('button/link required')
                    locator = page.get_by_role(command['role'], name=command['name'], exact=True)
                    locator.nth(command.get('index', 0)).click(timeout=15000)
                    page.wait_for_timeout(3000)
                elif command['operation'] == 'collect':
                    for group in command['groups']:
                        collect(group)
                    continue
                elif command['operation'] == 'history':
                    page.goto(origin + '/game/matches', wait_until='domcontentloaded', timeout=45000)
                    page.wait_for_timeout(3000)
                    page.get_by_role('button', name='My team', exact=True).click()
                    groups, stable = set(), 0
                    for _ in range(80):
                        previous = len(groups)
                        groups.update(page.locator('a[href^="/game/match-groups/"]').evaluate_all('(es)=>es.map(e=>e.getAttribute("href").split("/").pop())'))
                        stable = stable + 1 if len(groups) == previous else 0
                        if stable >= 4:
                            break
                        page.mouse.wheel(0, 6000)
                        page.wait_for_timeout(1500)
                    atomic_json(args.output / 'history.json', {'groups':sorted(groups), 'observed_at':time.time()}, 0o600)
                    print(json.dumps({'history_group_ids':sorted(groups), 'count':len(groups)}), flush=True)
                    continue
                else:
                    raise ValueError('unsupported operation')
                snapshot()
            except Exception as exc:
                print(json.dumps({'error':str(exc)[:2000]}), flush=True)
        context.close()


if __name__ == '__main__':
    main()
