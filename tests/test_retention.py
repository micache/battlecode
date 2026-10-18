"""Rolling raw history, crash recovery and preservation invariants; fake games."""
import json
from pathlib import Path
from unittest.mock import patch

from test_arena import Harness
from arena.common import ArenaError, atomic_json, read_json, identity
from arena.engine import seal_artifacts, verify_artifacts
from arena.retention import compact_project, finish_compaction, maintain, protected_jobs, retire, prune_build_cache


class RetentionTests(Harness):
    def test_build_lru_keeps_newest_twelve_and_queued_immutable_inputs(self):
        import os
        root=self.root/'builds';root.mkdir()
        ids=[]
        for n in range(14):
            bid=identity({'build':n});ids.append(bid)
            directory=root/bid;directory.mkdir()
            atomic_json(directory/'build.json',{'build_id':bid})
            (directory/'cache.bin').write_bytes(b'x'*4096)
            os.utime(directory/'build.json',(100+n,100+n))
        self.arena.db.execute("INSERT INTO match_jobs(id,spec,state,created) VALUES(?,?,'QUEUED',0)",
            ('f'*64,json.dumps({'a_build':ids[0],'b_build':ids[-1]})))
        removed,reclaimed=prune_build_cache(self.arena)
        self.assertEqual(removed,[ids[1]])
        self.assertGreater(reclaimed,4096)
        self.assertTrue((root/ids[0]).exists())
        self.assertTrue(all((root/bid).exists() for bid in ids[-12:]))
        self.assertFalse((root/ids[1]).exists())

    def project_job(self):
        self.establish()
        job = self.arena.db.one("SELECT * FROM match_jobs WHERE state='COMPLETED' LIMIT 1")
        old = Path(job['artifact'])
        (old/'project').mkdir()
        (old/'project/source.cpp').write_bytes(b'original bot source')
        (old/'artifacts').mkdir()
        (old/'artifacts/replay.repl26a').write_bytes(b'original replay')
        (old/'artifacts/final.json').write_bytes(b'original statistics')
        seal_artifacts(old,job['id'],job['attempt_count'],json.loads(job['result']))
        return job,old

    def test_project_compaction_preserves_replay_statistics_and_original_seal(self):
        job,old=self.project_job()
        removed=compact_project(self.arena,job)
        new=Path(self.arena.db.one('SELECT artifact FROM match_jobs WHERE id=?',(job['id'],))['artifact'])
        self.assertGreater(removed,0)
        self.assertTrue(old.is_symlink())
        self.assertFalse((new/'project').exists())
        self.assertEqual((old/'artifacts/replay.repl26a').read_bytes(),b'original replay')
        self.assertEqual((old/'artifacts/final.json').read_bytes(),b'original statistics')
        self.assertIn('project/source.cpp',read_json(new/'history-prune.json')['previous_completion']['files'])
        self.assertEqual(verify_artifacts(new,job['id'],job['attempt_count']),json.loads(job['result']))

    def test_compaction_recovers_pointer_commit_without_losing_old_evidence(self):
        job,old=self.project_job()
        with patch('arena.retention.remove_redundant',side_effect=OSError('synthetic interruption')):
            with self.assertRaises(OSError): compact_project(self.arena,job)
        self.assertTrue((old/'project/source.cpp').exists())
        job=self.arena.db.one('SELECT * FROM match_jobs WHERE id=?',(job['id'],))
        finish_compaction(self.arena,job)
        self.assertTrue(old.is_symlink())
        self.assertEqual((old/'artifacts/final.json').read_bytes(),b'original statistics')

    def test_raw_retirement_keeps_result_cases_and_journals_intent_before_delete(self):
        job,old=self.project_job()
        with patch('arena.retention.remove_redundant',side_effect=OSError('synthetic interruption')):
            with self.assertRaises(OSError): retire(self.arena,job)
        row=self.arena.db.one('SELECT * FROM match_jobs WHERE id=?',(job['id'],))
        self.assertIsNone(row['artifact'])
        self.assertEqual(row['result'],job['result'])
        self.assertTrue(old.exists())
        self.config['limits']['rolling_history']=True
        maintain(self.arena)
        self.assertFalse(old.parent.exists())
        self.assertEqual(self.arena.db.one('SELECT state FROM artifact_retirements WHERE job_id=?',(job['id'],))['state'],'DELETED')
        self.assertIsNotNone(self.arena.db.one('SELECT job_id FROM evaluation_cases WHERE job_id=?',(job['id'],)))

    def test_pins_include_active_evaluations_and_parser_bootstrap_evidence(self):
        alpha,_=self.establish()
        row=self.commit('alpha','candidate pending comparison')
        eid=self.arena.start_evaluation(row['id'])
        jobs={r['job_id'] for r in self.arena.evaluation_cases(eid)}
        fixture=self.arena.db.one("SELECT id,artifact FROM match_jobs WHERE state='COMPLETED' LIMIT 1")
        atomic_json(self.path/'parser.json',{'fixture_path':str(Path(fixture['artifact'])/'artifacts/final.json')})
        self.config['parser_contract']=str(self.path/'parser.json')
        pins=protected_jobs(self.arena)
        self.assertTrue(jobs<=pins)
        self.assertIn(fixture['id'],pins)

    def test_fifo_retirement_under_pressure_keeps_recent_and_evaluation_files(self):
        alpha,_=self.establish()
        build=self.arena.build(alpha['id']);m=self.arena.freeze_maps()['collision']
        ids=[]
        for n in range(125):
            jid=self.arena.queue_match(build,build,m,training_round={'id':str(n)})
            self.arena.run_one_match(jid);ids.append(jid)
        self.config['limits'].update(rolling_history=True,artifact_budget_bytes=1)
        result=maintain(self.arena,deletion_limit=2)
        self.assertEqual(result['retired_matches'],ids[:2])
        self.assertTrue(all(self.arena.db.one('SELECT artifact FROM match_jobs WHERE id=?',(j,))['artifact'] for j in ids[-120:]))
        self.assertTrue(all(self.arena.db.one('SELECT artifact FROM match_jobs WHERE id=?',(j,))['artifact'] for j in protected_jobs(self.arena)))

    def test_unsafe_artifact_target_is_rejected_without_deletion(self):
        job,old=self.project_job()
        with self.assertRaises(ArenaError): retire(self.arena,dict(job,artifact=str(self.root)))
        self.assertTrue(old.exists())
