#!/usr/bin/env python3
"""Re-review sealed diagnostics without editing their original evidence."""
import collections
import json
from pathlib import Path
import re
import sys
import zipfile

sys.path.insert(0, '/opt/battlecode')
from arena.common import atomic_json, file_hash, read_json
from arena.config import load
from arena.engine import OfficialEngine, normalize_result, verify_artifacts

config = load('/etc/battlecode/arena.json')
root = Path(config['root'])
engine = OfficialEngine(config)
reports = []
for directory in sorted((root / 'acceptance/real-fixtures').iterdir()):
    if not (directory / 'completion.json').is_file():
        continue
    spec = read_json(directory / 'spec.json')
    verify_artifacts(directory, spec['job_id'], 1)
    output = directory / ('artifacts' if spec['fixture'] in ('timeout', 'truncated') else 'run/artifacts')
    markers = {}
    observations = {}
    for replay in output.glob('*.repl26a'):
        with zipfile.ZipFile(replay) as archive:
            for name in ('team-a.stdout', 'team-b.stdout'):
                info = archive.getinfo(name)
                if info.file_size > 8 * 1024**2:
                    raise RuntimeError('diagnostic stdout exceeds review bound')
                text = archive.read(name).replace(bytes([0]), b'').decode(errors='replace')
                markers[name] = dict(collections.Counter(re.findall(r'CHECK (?:PASS|FAIL) [a-z-]+', text)))
                observations[name] = [line[:500] for line in text.splitlines()
                                      if line.startswith(('PROFILE', 'FUEL', 'HIDDEN'))][:100]
    reports.append({'fixture': spec['fixture'], 'match_id': spec['job_id'], 'directory': str(directory),
                    'seal_sha256': file_hash(directory / 'completion.json'),
                    'result': normalize_result(output, engine.contract, engine.lock['engine_sha256']),
                    'markers': markers, 'observations': observations,
                    'scoring_evidence': False})
target = root / 'acceptance/diagnostic-review.json'
atomic_json(target, {'engine_lock_hash': engine.lock_hash, 'diagnostics': reports,
                    'note': 'Absent PASS markers are unverified, not passing. Original sealed reviews remain unchanged.'}, 0o644)
print(json.dumps({'path': str(target), 'sha256': file_hash(target), 'fixtures': len(reports)}))
