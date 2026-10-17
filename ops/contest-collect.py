#!/usr/bin/env python3
"""Read-only collector using the owner's separately approved browser session.

Routes and the 202 download-job protocol were observed in the current official
UI. No raw credentials, headers, uploads, activation or challenges are used.
Original game bundles stay local; only mapped compact evidence is later imported.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import parse_qsl, urlencode, urlsplit

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import atomic_bytes, atomic_json, file_hash, identity, read_json, require

ORIGIN = 'https://2026a.battlecode.co.uk'


def redact(value):
    if isinstance(value, dict):
        return {k:redact(v) for k,v in value.items() if not re.search(r'(^|_)(token|secret|authorization|cookie)($|_)', k, re.I)}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str) and value.startswith('https://') and '?' in value:
        return value.split('?')[0] + '?[query-redacted]'
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path.home() / '.local/share/battlecode-contest-downloads')
    parser.add_argument('--max-groups', type=int, default=1000)
    parser.add_argument('--max-new-bundles', type=int, default=10)
    parser.add_argument('--resume-after-review', action='store_true', help='Explicitly acknowledge the saved access/rate stop')
    parser.add_argument('--headless', action='store_true', help='Default is the ordinary visible owner browser')
    args = parser.parse_args()
    root = args.output
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    require(not (root/'collection-stop.json').exists() or args.resume_after_review,
            'previous access/rate stop saved; inspect it before --resume-after-review')
    require(args.max_new_bundles > 0, 'positive bounded download count required')
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(Path.home() / '.local/share/battlecode-contest-browser'),
                                                               headless=args.headless, accept_downloads=True)
        page = context.pages[0] if context.pages else context.new_page()

        def get(path):
            parsed = urlsplit(path)
            require(not parsed.netloc or parsed.netloc == '2026a.battlecode.co.uk', 'only same-origin metadata reads')
            require(parsed.path.startswith('/api/v1/'), 'unexpected metadata route')
            response = context.request.get(ORIGIN + path if path.startswith('/') else path, timeout=60000)
            if response.status in (401,403,429):
                atomic_json(root/'collection-stop.json', {'path':parsed.path,'status':response.status,
                            'retry_after':response.headers.get('retry-after'), 'stopped_at':time.time(),
                            'action':'Stop requests; preserve downloads. Owner/operator must review before resume.'}, 0o600)
            require(response.status not in (401,403,429), f'platform access/rate stop: HTTP {response.status}')
            if 'json' not in response.headers.get('content-type', ''):
                require(response.ok, f'platform read failed: HTTP {response.status}')
                blob = response.body()
                require(blob.startswith(b'PK'), 'unexpected non-JSON platform response')
                return blob, response.status
            data = response.json()
            atomic_json(root / 'api' / (hashlib.sha256(path.encode()).hexdigest()+'.json'),
                        {'path':parsed.path, 'query':parsed.query, 'status':response.status,
                         'response_redacted':redact(data), 'observed_at':time.time()}, 0o600)
            require(response.ok or (response.status == 409 and
                    data == {'error':'All requested matches must be finished'}),
                    f'platform read failed: HTTP {response.status}')
            return data, response.status

        submissions, _ = get('/api/v1/submissions')
        team = submissions['team']['id']
        for submission in submissions['submissions']:
            target = root / 'submissions' / (submission['id'] + '.zip')
            if not target.exists():
                response = context.request.get(ORIGIN+'/api/v1/submissions/'+submission['id']+'/archive', timeout=60000)
                require(response.ok, f'own source download failed: HTTP {response.status}')
                atomic_bytes(target, response.body(), 0o600)
            atomic_json(target.with_suffix('.json'), {'submission':submission, 'zip_sha256':file_hash(target),
                        'local_path':str(target)}, 0o600)
        print(json.dumps({'own_team':team, 'source_versions_preserved':len(submissions['submissions'])}), flush=True)

        history_responses = []

        def history_response(response):
            parsed = urlsplit(response.url)
            if parsed.netloc == '2026a.battlecode.co.uk' and parsed.path == '/api/v1/match-groups' and response.request.method=='GET':
                if response.status in (401,403,429):
                    raise RuntimeError('history access/rate stop')
                if response.ok:
                    history_responses.append((parsed.path+'?'+parsed.query, response.json()))

        page.on('response', history_response)
        page.goto(ORIGIN+'/game/matches', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_timeout(4000)
        page.get_by_role('button', name='My team', exact=True).click()
        for _ in range(20):
            if len(history_responses)>1 and any('cursor' in url or 'before' in url for url,data in history_responses):
                break
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)
        require(history_responses, 'no supported current-team history response observed')
        groups = {}
        cursor_key, base_query, base_path = None, None, None
        for url, data in history_responses:
            require(data['myTeamId']==team, 'history team mismatch')
            groups.update({g['id']:g for g in data['groups']})
            parts = urlsplit(url)
            query = dict(parse_qsl(parts.query))
            for key,value in query.items():
                if any(value==old.get('next') for _,old in history_responses if old.get('next')):
                    cursor_key, base_query, base_path = key,query,parts.path
        latest = history_responses[-1][1]
        require(not latest.get('more') or cursor_key, 'pagination parameter not observed; do not guess it')
        seen = set()
        while latest.get('more'):
            cursor = latest['next']
            require(cursor not in seen and len(groups)<args.max_groups, 'history paging bound/repeated cursor')
            seen.add(cursor)
            base_query[cursor_key] = cursor
            latest, _ = get(base_path+'?'+urlencode(base_query))
            require(latest['myTeamId']==team, 'history team mismatch')
            groups.update({g['id']:g for g in latest['groups']})
            time.sleep(.3)
        atomic_json(root / 'history-complete.json', {'team_id':team, 'groups':list(groups.values()),
                    'more':False, 'observed_at':time.time()}, 0o600)
        print(json.dumps({'history_groups':len(groups), 'pagination_complete':True}), flush=True)

        page.remove_listener('response', history_response)
        # No final-statistics endpoint was established. Do not invent one or
        # infer fuel/behavioral statistics from the opaque replay formats.

        active_id = (submissions.get('active') or {}).get('id')
        def ordering(group):
            own = next(s for s in group['sides'] if s['teamId']==team)
            return (own.get('submissionId') != active_id, group['createdAt'])
        new_bundles, complete = 0, True
        for group in sorted(groups.values(), key=ordering):
            own = next((s for s in group.get('sides',[]) if s['teamId']==team), None)
            require(own is not None, 'refusing another team history group')
            if group['status'] not in ('finished','error'):
                continue
            directory = root / 'groups' / group['id']
            if group['status'] == 'finished' and (directory/'download.json').exists():
                # Finalized metadata and its original ZIP are immutable local evidence.
                continue
            if new_bundles >= args.max_new_bundles:
                complete = False
                break
            time.sleep(1)
            details, _ = get('/api/v1/match-groups/'+group['id'])
            atomic_json(directory / 'metadata.json', redact(details), 0o600)
            if not any(m.get('replayUrl') for m in details['matches']):
                continue
            if (directory/'download.json').exists():
                continue
            data, status = get('/api/v1/match-groups/'+group['id']+'/bundle')
            if status == 409:
                # Observed official response for error groups with unfinished games.
                require(group['status'] == 'error', 'unexpected unfinished finished group')
                atomic_json(directory/'unavailable.json', {'status':status, 'response':data}, 0o600)
                continue
            deadline = time.monotonic()+180
            while status == 202:
                atomic_json(directory/'pending-download.json', redact(data), 0o600)
                require(time.monotonic()<deadline, 'bundle still preparing; pending job retained')
                time.sleep(max(1, float(data.get('retryAfter', 2))))
                data, status = get(data['pollUrl'])
            if isinstance(data, bytes):
                blob = data  # Ready poll URL redirects directly to the requested ZIP.
            else:
                url = data['url']
                parsed = urlsplit(url)
                require(parsed.scheme=='https' and parsed.netloc.endswith('.amazonaws.com') and
                        '/match-groups/'+group['id']+'/' in parsed.path and '/teams/'+team+'/' in parsed.path,
                        'unexpected signed download destination')
                response = context.request.get(url, timeout=60000)
                require(response.ok, f'bundle download failed: HTTP {response.status}')
                blob = response.body()
            digest = hashlib.sha256(blob).hexdigest()
            target = directory / ('bundle-'+digest+'.zip')
            if not target.exists():
                atomic_bytes(target, blob, 0o600)
            atomic_json(directory/'download.json', {'path':str(target), 'sha256':digest, 'bytes':len(blob),
                        'group_id':group['id'], 'downloaded_at':time.time()}, 0o600)
            new_bundles += 1
            print(json.dumps({'downloaded_group':group['id'], 'bytes':len(blob), 'submission':own.get('submissionId')}), flush=True)
        atomic_json(root/'collection-status.json', {'complete':complete, 'group_count':len(groups),
                    'new_bundles':new_bundles, 'finished_at':time.time(), 'summary_route_observed':False}, 0o600)
        context.close()


if __name__ == '__main__':
    main()
