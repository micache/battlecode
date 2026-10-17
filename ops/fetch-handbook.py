#!/usr/bin/env python3
"""Download the organizer's LLM exports through its actual browser controls.

Read-only contest operation. Uses the owner's already-approved browser profile;
never extracts cookies/tokens or guesses a private documentation API.
"""
import argparse
import json
from pathlib import Path
import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arena.common import atomic_json, file_hash, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New directory for unmodified downloads')
    args = parser.parse_args()
    require(not args.output.exists(), 'preserve existing downloads; choose a new output directory')
    args.output.mkdir(parents=True, mode=0o700)
    profile = Path.home() / '.local/share/battlecode-contest-browser'
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(profile), headless=True)
        page = context.pages[0] if context.pages else context.new_page()
        response = page.goto('https://2026a.battlecode.co.uk/game/docs/agents',
                             wait_until='networkidle', timeout=45000)
        require(response.status == 200, 'documentation access failed; owner browser login may be needed')
        require(page.get_by_role('button', name='Download GameRules.md', exact=True).count() == 1,
                'organizer export controls unavailable; do not guess endpoints')
        report = {'source': page.url, 'retrieved_at': time.time(), 'files': {},
                  'page_text': page.locator('article').inner_text(),
                  'observation': 'Agents.md page is a language-selectable Markdown export hub, '
                                 'not a separate downloaded agent-instructions file.'}
        for name, language in [('GameRules.md', None), ('BotAPICpp.md', 'cpp'), ('BotAPIPython.md', 'python')]:
            if language:
                page.get_by_role('combobox', name='Bot API language').select_option(language)
            with page.expect_download(timeout=30000) as download:
                page.get_by_role('button', name='Download ' + name, exact=True).click()
            path = args.output / name
            download.value.save_as(path)
            report['files'][name] = {'sha256': file_hash(path), 'bytes': path.stat().st_size,
                                    'suggested_filename': download.value.suggested_filename}
        context.close()
    atomic_json(args.output / 'provenance.json', report, 0o600)
    print(json.dumps({k: v for k, v in report.items() if k != 'page_text'}, indent=2))


if __name__ == '__main__':
    main()
