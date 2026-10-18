#!/usr/bin/env python3
"""Explicit stopped-service CLI upgrade. Never edits credentials or bot source.

capture/rebaseline run as bc-arena; activate runs as root after ops/upgrade.py.
Saved old matches/evaluations retain their original identities and engine locks.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, lock, read_json, require


ROOT = Path('/srv/battlecode')
RECORD = ROOT / 'acceptance/cambc-225-transition'
STAGE = ROOT / 'toolchains/cambc-225'


def capture():
    from arena.config import load
    from arena.service import Arena
    from arena.development import select_base
    from arena.operations import backup
    require(os.geteuid() == (ROOT / 'state').stat().st_uid, 'run capture as bc-arena')
    require(not RECORD.exists(), 'transition capture exists; preserve and inspect it')
    config = load('/etc/battlecode/arena.json')
    require(config['engine']['version'] == '2.1.6', 'capture the old engine before activation')
    arena = Arena(config)
    require(arena.db.get('paused') and not arena.db.one("SELECT id FROM workers WHERE state='RUNNING'"),
            'pause and finish active coding tasks first')
    bases = {}
    for bot in config['workers']:
        base, selection = select_base(arena, bot)
        latest = arena.db.one('SELECT id,commit_sha,source_hash FROM revisions WHERE bot_id=? '
                              'ORDER BY created DESC LIMIT 1', (bot,))
        bases[bot] = {'base': base, 'selection': selection, 'latest': latest}
    RECORD.mkdir()
    for label, path in [('config', '/etc/battlecode/arena.json'), ('engine', config['engine_lock']),
                        ('parser', config['parser_contract'])]:
        atomic_json(RECORD / (label + '.json'), read_json(path))
    for label in ('starter-check.json', 'diagnostic-review.json'):
        path = ROOT / 'acceptance' / label
        if path.exists():
            atomic_json(RECORD / label, read_json(path))
    record = {'captured': time.time(), 'bases': bases, 'backup': backup(arena),
              'old_engine_lock_hash': arena.adapter().lock_hash}
    atomic_json(RECORD / 'capture.json', record)
    print(json.dumps({'captured': str(RECORD), 'bases': {
        bot: value['base']['commit_sha'] for bot, value in bases.items()}}))


def activate():
    require(os.geteuid() == 0, 'administrator required for configuration activation')
    require((RECORD / 'capture.json').is_file(), 'capture before switching versions')
    old = read_json(RECORD / 'config.json')
    config = read_json('/etc/battlecode/arena.json')
    require(config['engine'] == old['engine'], 'configuration already changed; inspect instead of retrying')
    expected = read_json('/opt/battlecode/evidence/map-pool-225.json')
    maps = STAGE / 'template/maps'
    require({p.stem for p in maps.glob('*.map26a')} == {m['name'] for m in expected['maps']},
            'staged published map pool differs from reviewed manifest')
    require(all(file_hash(maps / (m['name'] + '.map26a')) == m['sha256'] for m in expected['maps']),
            'staged map bytes changed')
    # Public SDK only; worker homes and credential permissions never change.
    for path in (STAGE.parent, STAGE, STAGE / 'template', *(STAGE / 'template').rglob('*')):
        require(not path.is_symlink(), 'unexpected staged SDK symlink')
        path.chmod(path.stat().st_mode | (0o555 if path.is_dir() else 0o444))
    config['engine'] = read_json('/opt/battlecode/config/pilot.json')['engine']
    config['engine_lock'] = str(ROOT / 'locks/engine-225.json')
    config['parser_contract'] = '/etc/battlecode/parser-225.json'
    require(not Path(config['engine_lock']).exists() and not Path(config['parser_contract']).exists(),
            'new-version lock/parser already exists; reconcile interrupted activation')
    config['maps'] = str(maps)
    config['map_manifest'] = '/opt/battlecode/evidence/map-pool-225.json'
    gate = config['evaluation']
    holdouts = gate['holdout_maps']
    require(set(holdouts) <= {m['name'] for m in expected['maps']}, 'reserved map disappeared; review split')
    gate.update(full_evaluation=True, suite_version='published-17-release-225-v1',
                development_maps=[m['name'] for m in expected['maps'] if m['name'] not in holdouts])
    gate.pop('max_promotion_checks_per_day', None)
    # Promotion remains disabled: expanded coverage is not permission to bypass readiness.
    gate['automatic_promotion'] = False
    atomic_json('/etc/battlecode/arena.json', config, 0o644)
    subprocess.run(['python3', '/opt/battlecode/ops/as-arena.py', '/usr/local/bin/arena', 'register-toolchain',
                    '--image-id', (STAGE / 'image-id.txt').read_text().strip(),
                    '--template', str(STAGE / 'template'), '--compiler-record', str(STAGE / 'compiler-record.json')],
                   check=True, stdout=subprocess.DEVNULL)
    atomic_json(RECORD / 'activation.json', {'at': time.time(), 'config': config,
                'engine': read_json(config['engine_lock']), 'services_started': False})
    print(json.dumps({'activated': '2.2.5', 'maps': len(expected['maps']), 'services_started': False}))


def rebaseline():
    from arena.config import load
    from arena.service import Arena
    from arena.operations import ensure_starter_reference
    require(os.geteuid() == (ROOT / 'state').stat().st_uid, 'run rebaseline as bc-arena')
    arena = Arena(load('/etc/battlecode/arena.json'))
    require(arena.config['engine']['version'] == '2.2.5' and arena.db.get('paused'), 'new engine must remain paused')
    require(arena.db.get('starter_verified') and arena.adapter().contract and
            arena.db.get('starter_engine_lock_hash') == arena.adapter().lock_hash,
            'review new starter/parser first; old starter verification cannot carry forward')
    require(not (RECORD / 'rebaseline.json').exists(), 'rebaseline exists; inspect rather than duplicate')
    # Finish obsolete evaluations without reusing their outcomes on the new engine.
    arena.advance_evaluations()
    for row in arena.db.all("SELECT id,spec FROM match_jobs WHERE state='QUEUED'"):
        if json.loads(row['spec'])['engine_lock_hash'] != arena.adapter().lock_hash:
            arena.db.execute("UPDATE match_jobs SET state='CANCELLED' WHERE id=?", (row['id'],))
    arena.db.execute("UPDATE training_rounds SET state='SUPERSEDED' WHERE state='RUNNING'")
    arena.db.put('readiness', {})
    arena.db.put('service_error', None)
    arena.db.put('adapter_paused', False)
    ensure_starter_reference(arena)
    captured = read_json(RECORD / 'capture.json')
    evaluations = {}
    for bot, item in captured['bases'].items():
        base = item['base']
        require(base, 'missing preserved development source')
        arena.db.execute("UPDATE revisions SET state='PENDING' WHERE id=?", (base['id'],))
        evaluations[bot] = arena.start_evaluation(base['id'])
        latest = item['latest']
        if latest and latest['source_hash'] != base['source_hash']:
            arena.db.execute("UPDATE revisions SET state='PENDING' WHERE id=?", (latest['id'],))
        arena.db.execute("UPDATE workers SET state='WAITING_EVALUATION' WHERE id=? AND paused=0", (bot,))
    record = {'at': time.time(), 'engine_lock_hash': arena.adapter().lock_hash,
              'evaluations': evaluations, 'old_results_relabelled': False, 'promotion_enabled': False}
    atomic_json(RECORD / 'rebaseline.json', record)
    arena.export_status()
    print(json.dumps(record))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('capture', 'activate', 'rebaseline'))
    args = parser.parse_args()
    # Read-only lock opens: root must not create arena-owned lock files.
    with (ROOT / 'state/service.lock').open('r') as service, (ROOT / 'model.lock').open('r') as model:
        for handle in (service, model):
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # register-toolchain also needs service.lock; release only our check
        # while no supervisor is running. Its own lock provides exclusion.
        if args.command == 'activate':
            fcntl.flock(service, fcntl.LOCK_UN)
        globals()[args.command]()


if __name__ == '__main__':
    main()
