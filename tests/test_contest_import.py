"""Synthetic source-binding/side-attribution fixtures, not real-game evidence."""
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from arena.common import ArenaError, atomic_json, file_hash, identity

spec = importlib.util.spec_from_file_location('contest_import', Path(__file__).resolve().parents[1]/'ops/import-contest-evidence.py')
operator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator)


class ContestImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root/'submissions').mkdir()
        with zipfile.ZipFile(self.root/'submissions/upload.zip','w') as source:
            source.writestr('src/bot.cpp',b'synthetic source')
        self.manifest = {'commit':'a'*40,'source_hash':identity({'bot.cpp':hashlib.sha256(b'synthetic source').hexdigest()}),
                         'package_sha256':file_hash(self.root/'submissions/upload.zip')}
        atomic_json(self.root/'history-complete.json',{'team_id':'own','observed_at':123})
        group = self.root/'groups/group'
        group.mkdir(parents=True)
        inner = io.BytesIO()
        with zipfile.ZipFile(inner,'w') as archive:
            archive.writestr('replay.repl26a',b'opaque fixture')
            archive.writestr('team-b.stdout',b'\x00draft: hello world\n\x01shared round: 1\n')
        with zipfile.ZipFile(group/'bundle.zip','w') as archive:
            archive.writestr('01-game.zip',inner.getvalue())
        atomic_json(group/'download.json',{'path':str(group/'bundle.zip'),'sha256':file_hash(group/'bundle.zip')})
        atomic_json(group/'metadata.json',{'myTeamId':'own','group':{'id':'group','status':'finished',
            'winnerTeamId':'other','sides':[{'teamId':'own','submissionId':'upload'}]},'matches':[
                {'id':'game','position':1,'status':'finished','rounds':2000,'map':'lanes','mapId':'map',
                 'patchId':'official-patch','sides':[
                     {'side':'a','teamId':'other','score':0,'result':'win','draft':['1'],'version':None},
                     {'side':'b','teamId':'own','score':0,'result':'loss','draft':['2'],'version':3}]}]})

    def test_exact_zip_source_and_absolute_side_are_preserved_even_when_gems_tie(self):
        payloads, report = operator.prepare(self.root,self.manifest,'upload')
        self.assertEqual(report['counts']['losses'],1)
        payload = payloads[0]
        self.assertEqual((payload['own_side'],payload['outcome']),('B','A'))
        self.assertIsNone(payload['opponent_version'])
        evidence = json.loads(base64.b64decode(payload['files']['observations.json']))
        self.assertEqual(evidence['source_hash'],self.manifest['source_hash'])
        self.assertEqual(evidence['stdout']['known_message_count'],2)
        self.assertIsNone(evidence['official_summary'])
        self.assertNotIn('final.json',payload['files'])

    def test_wrong_uploaded_zip_or_source_hash_is_rejected(self):
        for field in ('package_sha256','source_hash'):
            with self.assertRaises(ArenaError):
                operator.prepare(self.root,dict(self.manifest,**{field:'0'*64}),'upload')

    def test_modified_original_game_bundle_is_rejected(self):
        with (self.root/'groups/group/bundle.zip').open('ab') as stream:
            stream.write(b'modified')
        with self.assertRaisesRegex(ArenaError,'checksum changed'):
            operator.prepare(self.root,self.manifest,'upload')
