"""Synthetic compiler/cache fixtures, not evidence of engine reproducibility."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from arena.common import ArenaError, atomic_json, file_hash, identity, read_json, tree_hash
from arena.engine import OfficialEngine
from test_arena import Harness


class FrozenCacheTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.source=self.root/'snapshot/src';self.source.mkdir(parents=True)
        (self.source/'main.cpp').write_text('SYNTHETIC SOURCE')
        self.engine=OfficialEngine.__new__(OfficialEngine)
        self.engine.config={'root':str(self.root),'infrastructure_commit':'b'*40}
        self.engine.lock_hash='f'*64
        self.old=identity('old-frozen-cache');self.new=identity('new-infrastructure-cache')
        origin=self.root/'builds'/self.new
        (origin/'output').mkdir(parents=True);(origin/'output-b').mkdir()
        (origin/'output/bot.wasm').write_bytes(b'SYNTHETIC WASM')
        (origin/'output-b/bot.wasm').write_bytes(b'SYNTHETIC WASM')
        work=origin/'prepare-new'
        for side in ['side-a','side-b']:
            cache=work/'bots'/side/'.cambc';cache.mkdir(parents=True)
            (cache/'compiler-cache.bin').write_bytes(b'SYNTHETIC compiler log')
        self.rebuilt={'build_id':self.new,'revision_id':'revision','source_hash':tree_hash(self.source),
            'lock_hash':self.engine.lock_hash,'wasm_sha256':file_hash(origin/'output/bot.wasm'),
            'side_b_wasm_sha256':file_hash(origin/'output-b/bot.wasm'),
            'snapshot':str(self.source.parent),'artifact':str(origin/'output/bot.wasm'),
            'cache_project':str(work),'cache_hashes':{side:tree_hash(work/'bots'/side/'.cambc')
                                                   for side in ['side-a','side-b']}}
        atomic_json(origin/'build.json',self.rebuilt)
        self.frozen=dict(self.rebuilt,build_id=self.old,artifact=str(self.root/'builds'/self.old/'output/bot.wasm'),
                         cache_project=str(self.root/'builds'/self.old/'prepare-old'))

    def test_restores_old_identity_only_with_both_original_executable_hashes(self):
        before=json.dumps(self.frozen,sort_keys=True)
        with patch.object(self.engine,'prepare_bot',return_value=self.rebuilt) as build:
            restored=self.engine.restore_frozen(self.frozen)
        build.assert_called_once_with(self.frozen['snapshot'],self.frozen['revision_id'])
        self.assertEqual(restored['build_id'],self.old)
        self.assertEqual(file_hash(self.frozen['artifact']),self.frozen['wasm_sha256'])
        self.assertEqual(json.dumps(self.frozen,sort_keys=True),before)
        self.assertTrue(Path(restored['cache_project']).is_dir())
        journal=read_json(self.root/'build-recoveries'/(self.old+'.json'))
        self.assertEqual(journal['state'],'COMPLETE')
        self.assertEqual(journal['original_record_sha256'],identity(self.frozen))

    def test_different_binary_is_never_published_or_retried_indefinitely(self):
        for key in ['wasm_sha256','side_b_wasm_sha256']:
            with self.subTest(key=key):
                journal=self.root/'build-recoveries'/(self.old+'.json')
                if journal.exists():journal.unlink()
                wrong=dict(self.rebuilt,**{key:'0'*64})
                with patch.object(self.engine,'prepare_bot',return_value=wrong) as build:
                    with self.assertRaisesRegex(ArenaError,'binary differs'):
                        self.engine.restore_frozen(self.frozen)
                    with self.assertRaisesRegex(ArenaError,'recovery failed'):
                        self.engine.restore_frozen(self.frozen)
                self.assertEqual(build.call_count,1)
                self.assertFalse(Path(self.frozen['artifact']).exists())


class SchedulerRecoveryTests(Harness):
    def test_queued_recovery_keeps_job_id_and_does_not_consume_an_attempt(self):
        alpha,_=self.establish()
        build=self.arena.build(alpha['id'])
        job=self.arena.queue_match(build,build,self.arena.freeze_maps()['collision'],repetition='missing-cache')
        Path(build['artifact']).unlink()
        def restore(frozen):
            self.assertEqual(self.arena.db.one('SELECT attempt_count FROM match_jobs WHERE id=?',(job,))['attempt_count'],0)
            Path(frozen['artifact']).write_bytes(b'SYNTHETIC, NOT WASM')
        with patch.object(self.engine,'restore_frozen',side_effect=restore,create=True) as recovery:
            self.arena.run_one_match(job)
        recovery.assert_called_once()
        row=self.arena.db.one('SELECT * FROM match_jobs WHERE id=?',(job,))
        self.assertEqual(row['id'],job)
        self.assertEqual(row['state'],'COMPLETED')
        self.assertEqual(row['attempt_count'],1)

    def test_existing_changed_binary_is_not_silently_replaced(self):
        alpha,_=self.establish();build=self.arena.build(alpha['id'])
        Path(build['artifact']).write_bytes(b'changed')
        with patch.object(self.engine,'restore_frozen',create=True) as recovery:
            with self.assertRaisesRegex(ArenaError,'artifact changed'):
                self.arena.frozen_build(build['build_id'],alpha['id'])
        recovery.assert_not_called()


if __name__=='__main__':unittest.main()
