"""Rolling raw history, crash recovery and preservation invariants; fake games."""
import json
from pathlib import Path
from unittest.mock import patch

from test_arena import Harness
from arena.common import ArenaError, atomic_json, read_json, identity, file_hash
from arena.statistics import saved_bytes
from arena.supervisor import handle_request
from arena.engine import seal_artifacts, verify_artifacts
from arena.retention import compact_project, finish_compaction, maintain, protected_jobs, retire, prune_build_cache, size


class RetentionTests(Harness):
    def test_large_active_suite_cannot_pin_all_raw_history_forever(self):
        self.establish()
        candidate=self.commit('alpha','large current suite')
        eid=self.arena.start_evaluation(candidate['id'])
        build=self.arena.build(candidate['id']);m=self.arena.freeze_maps()['collision']
        jobs=[]
        for n in range(125):
            jid=self.arena.queue_match(build,build,m,training_round={'id':'retention-'+str(n)})
            self.arena.run_one_match(jid);jobs.append(jid)
            self.arena.db.execute('INSERT INTO evaluation_cases VALUES(?,?,?,?,?,?,?)',
                (eid,jid,'A','candidate','collision','frozen-opponent-'+str(n),'screen'))
        before={r['id']:r['result'] for r in self.arena.db.all('SELECT id,result FROM match_jobs')}
        self.config['limits'].update(rolling_history=True,minimum_free_bytes=0,
                                     artifact_budget_bytes=int(size(self.root/'matches')*.8))
        report=maintain(self.arena)
        self.assertTrue(set(report['retired_matches']) & set(jobs))
        self.assertEqual(before,{r['id']:r['result'] for r in self.arena.db.all('SELECT id,result FROM match_jobs')})
        self.assertEqual(self.arena.db.one('SELECT state FROM evaluations WHERE id=?',(eid,))['state'],'EVALUATING')
        self.assertTrue(all(c['result']['completed'] for c in self.arena.evaluation_cases(eid) if c['job_id'] in jobs))
        from arena.evaluate import summarize
        metrics=summarize(self.arena.evaluation_cases(eid),self.config['evaluation'],[],False)
        self.assertTrue(all(f['raw_available'] for f in metrics['representative_failures']))

    def test_rolling_target_is_not_a_scheduler_interlock(self):
        self.establish()
        build=self.arena.build(self.arena.db.get('starter_revision'))
        jid=self.arena.queue_match(build,build,self.arena.freeze_maps()['collision'],repetition='rolling-target')
        self.config['limits'].update(rolling_history=True,artifact_budget_bytes=1,minimum_free_bytes=0)
        self.arena.db.put('paused',False)
        with patch('arena.service.poll'),patch('arena.supervisor.dispatch_tasks'):
            self.arena.step()
        self.assertFalse(self.arena.db.get('disk_pressure'))
        self.assertEqual(self.arena.db.one('SELECT state FROM match_jobs WHERE id=?',(jid,))['state'],'COMPLETED')

    def test_progress_health_detects_stall_despite_fresh_heartbeat_and_respects_real_floor(self):
        from arena.health import progress
        self.establish()
        status=self.arena.status();status.update(paused=False,matches=[{'state':'QUEUED','count':1}])
        last=self.arena.db.one('SELECT max(finished) AS finished FROM match_attempts')['finished']
        status['heartbeat']=last+2000
        self.assertEqual(progress(status,self.arena.db,self.config['limits'],last+2000)['state'],'STALLED')
        status['disk']['free']=0
        self.assertEqual(progress(status,self.arena.db,self.config['limits'],last+2000)['state'],'STORAGE_BLOCKED')
        status['paused']=True
        self.assertEqual(progress(status,self.arena.db,self.config['limits'],last+2000)['state'],'PAUSED')

    def test_build_lru_pins_future_stage_development_base(self):
        import os
        self.establish()
        candidate=self.commit('alpha','future-stage candidate')
        eid=self.arena.start_evaluation(candidate['id'])
        root=self.root/'builds';root.mkdir(exist_ok=True)
        frozen=identity({'future-development-base':True})
        directory=root/frozen;directory.mkdir()
        atomic_json(directory/'build.json',{'build_id':frozen})
        os.utime(directory/'build.json',(1,1))
        suite=json.loads(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?',(eid,))['suite'])
        suite['development_build']=frozen
        self.arena.db.execute('UPDATE evaluations SET suite=? WHERE id=?',(json.dumps(suite),eid))
        for n in range(13):
            bid=identity({'newer-cache':n});p=root/bid;p.mkdir()
            atomic_json(p/'build.json',{'build_id':bid});os.utime(p/'build.json',(100+n,100+n))
        removed,_=prune_build_cache(self.arena)
        self.assertNotIn(frozen,removed)
        self.assertTrue((directory/'build.json').exists())

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

    def test_large_statistics_are_lossless_and_slices_remain_transparent(self):
        import gzip
        job, old = self.project_job()
        data = json.dumps({'timeline':['large retained official data'] * 12000}).encode()
        (old/'artifacts/final.json').write_bytes(data)
        seal_artifacts(old,job['id'],job['attempt_count'],json.loads(job['result']))
        compact_project(self.arena,job)
        current = self.arena.db.one('SELECT * FROM match_jobs WHERE id=?',(job['id'],))
        path = Path(current['artifact'])/'artifacts/final.json'
        self.assertFalse(path.exists())
        self.assertEqual(saved_bytes(path),data)
        self.assertEqual(gzip.decompress(Path(str(path)+'.gz').read_bytes()),data)
        self.assertEqual(verify_artifacts(current['artifact'],job['id'],job['attempt_count']),json.loads(job['result']))
        sliced = handle_request(self.arena,'alpha',{'operation':'slice','payload':{
            'match_id':job['id'],'file':'final.json','offset':75,'limit':130}})
        self.assertEqual(sliced['text'],data[75:205].decode())
        self.assertEqual(sliced['size'],len(data))
        proof = read_json(Path(current['artifact'])/'history-prune.json')
        proof['compressed_statistics']['uncompressed_sha256'] = 'f'*64
        atomic_json(Path(current['artifact'])/'history-prune.json', proof)
        with self.assertRaisesRegex(ArenaError,'statistics bytes changed'):
            saved_bytes(path)

    def test_parser_fixture_remains_at_its_exact_uncompressed_path(self):
        job, old = self.project_job()
        path=old/'artifacts/final.json';path.write_bytes(b'x'*200000)
        seal_artifacts(old,job['id'],job['attempt_count'],json.loads(job['result']))
        atomic_json(self.path/'parser.json',{'fixture_path':str(path)})
        self.config['parser_contract']=str(self.path/'parser.json')
        compact_project(self.arena,job)
        self.assertEqual(len(path.read_bytes()),200000)
        self.assertFalse(Path(str(path)+'.gz').exists())

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
