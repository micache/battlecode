"""Synthetic continuous-match orchestration; no real engines or model calls."""
import json
from pathlib import Path
from unittest.mock import patch

from test_arena import Harness
from arena.common import ArenaError
from arena.memory import training_window
from arena.service import Arena
from arena.supervisor import handle_request
from arena.training import replenish, status, window


class ContinuousTrainingTests(Harness):
    def enable(self):
        self.establish()
        self.config['limits']['continuous_matches'] = True
        self.config['evaluation']['max_promotion_checks_per_day'] = 0
        for worker in self.config['workers'].values():
            worker.update(enabled=True,owner_confirmed=True)
        self.arena.db.put('paused',False)

    def drain(self, round_id):
        for job in self.arena.db.all('SELECT job_id FROM training_cases WHERE round_id=?',(round_id,)):
            self.assertTrue(self.arena.run_one_match(job['job_id']))

    def test_idle_game_queue_replenishes_without_a_model_call_or_promotion(self):
        self.enable()
        before = self.arena.db.one('SELECT count(*) AS n FROM evaluations')['n']
        first = replenish(self.arena)
        jobs = self.arena.db.all('SELECT * FROM training_cases WHERE round_id=?',(first,))
        self.assertEqual(len(jobs),12)  # Two lanes x both sides x six development maps.
        self.assertEqual({j['map_name'] for j in jobs},set(self.config['evaluation']['development_maps']))
        self.assertEqual({(j['a_bot'],j['b_bot']) for j in jobs},{('alpha','beta'),('beta','alpha')})
        self.assertEqual(replenish(self.arena),first)
        self.drain(first)
        second = replenish(self.arena)
        self.assertNotEqual(first,second)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM tasks')['n'],0)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM evaluations')['n'],before)
        self.assertEqual(self.arena.db.one("SELECT state FROM training_rounds WHERE id=?",(first,))['state'],'COMPLETED')

    def test_sources_are_frozen_and_evaluation_jobs_take_priority(self):
        self.enable()
        rid = replenish(self.arena)
        before = self.arena.db.one('SELECT spec FROM training_rounds WHERE id=?',(rid,))['spec']
        candidate = self.commit('alpha','new immutable candidate')
        eid = self.arena.start_evaluation(candidate['id'])
        self.assertTrue(self.arena.run_one_match())
        self.assertNotIn('training_round',self.engine.calls[-1])
        self.assertEqual(self.arena.db.one('SELECT spec FROM training_rounds WHERE id=?',(rid,))['spec'],before)
        self.assertEqual(replenish(self.arena),rid)
        self.assertTrue(self.arena.db.one('SELECT id FROM evaluations WHERE id=?',(eid,)))

    def test_restart_keeps_one_round_and_no_duplicate_jobs(self):
        self.enable()
        rid = replenish(self.arena)
        self.arena.run_one_match()
        self.arena.db.connection.close()
        self.arena = Arena(self.config,self.engine)
        self.arena.recover()
        self.assertEqual(replenish(self.arena),rid)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM training_cases')['n'],12)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM training_rounds')['n'],1)

    def test_disabling_continuous_play_parks_queued_training_and_can_resume(self):
        self.enable()
        rid = replenish(self.arena)
        self.config['limits']['continuous_matches'] = False
        self.assertFalse(self.arena.run_one_match())
        self.assertIsNone(replenish(self.arena))
        self.config['limits']['continuous_matches'] = True
        self.assertEqual(replenish(self.arena),rid)
        self.assertTrue(self.arena.run_one_match())

    def test_global_pause_adapter_pause_disk_pressure_and_bootstrap_are_respected(self):
        self.enable()
        for flag,value in [('paused',True),('adapter_paused',True),('disk_pressure',True),('starter_verified',False)]:
            original = self.arena.db.get(flag)
            self.arena.db.put(flag,value)
            self.assertIsNone(replenish(self.arena))
            self.arena.db.put(flag,original)
        self.assertFalse(self.arena.db.one('SELECT * FROM training_rounds'))
        # Coding-account waits are deliberately independent of compiled bot play.
        self.arena.db.execute("UPDATE workers SET state='QUOTA_WAIT',paused=1")
        self.assertIsNotNone(replenish(self.arena))

    def test_round_publication_is_atomic_and_infrastructure_change_supersedes_queue(self):
        self.enable()
        original = self.arena.queue_match
        count = 0
        def interrupted(*args,**kwargs):
            nonlocal count
            count += 1
            if count == 2:
                raise ArenaError('synthetic publication interruption')
            return original(*args,**kwargs)
        with patch.object(self.arena,'queue_match',side_effect=interrupted):
            with self.assertRaises(ArenaError):
                replenish(self.arena)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM training_rounds')['n'],0)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM training_cases')['n'],0)
        rid = replenish(self.arena)
        self.assertIsNotNone(rid)
        self.config['infrastructure_commit'] = '9'*40
        self.assertNotEqual(replenish(self.arena),rid)
        self.assertEqual(self.arena.db.one('SELECT state FROM training_rounds WHERE id=?',(rid,))['state'],'SUPERSEDED')

    def test_repeats_are_not_independent_and_feedback_remains_lane_scoped(self):
        self.enable()
        first = replenish(self.arena)
        self.drain(first)
        second = replenish(self.arena)
        self.drain(second)
        report = window(self.arena,'alpha',0)
        self.assertEqual(len(report['source_groups']),1)
        group = report['source_groups'][0]
        self.assertEqual(group['completed_matches'],24)
        self.assertEqual(group['unique_input_cells'],12)
        self.assertEqual(group['repeat_matches'],12)
        self.assertEqual((group['wins'],group['losses']),(6,6))
        self.assertEqual(training_window(self.arena,'alpha')['continuous_self_play'],report)
        job = self.arena.db.one('SELECT j.* FROM training_cases t JOIN match_jobs j ON j.id=t.job_id')
        artifacts = Path(job['artifact'])/'artifacts'
        artifacts.mkdir()
        (artifacts/'final.json').write_text('{"synthetic":"diagnostic"}')
        response = handle_request(self.arena,'alpha',{'operation':'slice','payload':{
            'match_id':job['id'],'file':'final.json'}})
        self.assertIn('diagnostic',response['text'])
        self.assertEqual(window(self.arena,'unrelated',0)['source_groups'],[])
        with self.assertRaises(ArenaError):
            handle_request(self.arena,'unrelated',{'operation':'slice','payload':{
                'match_id':job['id'],'file':'final.json'}})
        self.assertTrue(status(self.arena)['enabled'])
