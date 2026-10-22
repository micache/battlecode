"""Boss orchestration fixtures are synthetic, not actual contest scores."""
import base64
import json
from pathlib import Path

from test_arena import Harness
from arena.boss import register,bootstrap,context
from arena.common import ArenaError,atomic_json,identity,read_json
from arena.knowledge import freeze_opponents
from arena.operations import import_external
from arena.protocol import decode_source
from arena.strategy import opponent_panel,experiment_context
from arena.supervisor import handle_request
from arena.training import roster


class BossTests(Harness):
    def install(self):
        self.establish()
        source={'main.cpp':base64.b64encode(b'SYNTHETIC TEAM BOSS').decode()}
        _,digest=decode_source(source)
        sid='00000000-0000-4000-8000-000000000017'
        proof={'team_id':'test-team','source_hash':digest,'package_sha256':'a'*64,
            'active':{'id':sid,'version':17,'language':'cpp','status':'active'},'selected':{'id':sid}}
        self.config['official_exploration']={'team_id':'test-team'}
        envelope={'source':source,'proof':proof}
        boss=register(self.arena,envelope);self.config['boss']=boss
        return boss,envelope

    def test_reference_is_immutable_idempotent_and_never_a_worker(self):
        boss,envelope=self.install()
        self.assertEqual(register(self.arena,envelope)['source_commit'],boss['source_commit'])
        self.assertEqual(register(self.arena,envelope)['revision_id'],boss['revision_id'])
        self.assertFalse(boss['published_to_github'])
        self.assertIsNone(self.arena.db.one("SELECT id FROM workers WHERE id='boss'"))
        self.assertEqual(self.arena.db.one("SELECT state FROM revisions WHERE id=?",(boss['revision_id'],))['state'],'REFERENCE')
        self.assertIn(boss['revision_id'],opponent_panel(self.arena))
        self.assertIn('boss',roster(self.arena))

    def test_frozen_source_is_first_in_every_agents_packet(self):
        boss,_=self.install()
        for bot in self.config['workers']:
            packet=freeze_opponents(self.arena,bot,'task-fixture-'+bot)
            item=read_json(packet['manifest'])['opponents'][0]
            self.assertEqual(item['role'],'shared-boss')
            self.assertEqual(item['source_hash'],boss['source_hash'])

    def test_bootstrap_shares_results_and_development_traces_without_extra_models(self):
        boss,_=self.install()
        count=self.arena.db.one('SELECT count(*) n FROM tasks')['n']
        rid=bootstrap(self.arena)
        data=context(self.arena)
        self.assertEqual({g['bot_id'] for g in data['progress']},set(self.config['workers']))
        self.assertTrue(all(g['wins']==g['losses']==1 for g in data['progress']))
        self.assertEqual(self.arena.db.one('SELECT count(*) n FROM tasks')['n'],count)
        row=self.arena.db.one("SELECT j.* FROM training_cases t JOIN match_jobs j ON j.id=t.job_id "
                              "WHERE t.round_id=? AND t.a_bot='alpha'",(rid,))
        artifacts=Path(row['artifact'])/'artifacts';artifacts.mkdir()
        (artifacts/'summary.json').write_text('SYNTHETIC boss lesson')
        reply=handle_request(self.arena,'beta',{'operation':'slice','payload':{
            'match_id':row['id'],'file':'summary.json'}})
        self.assertIn('boss lesson',reply['text'])
        self.assertEqual(experiment_context(self.arena,'alpha')['shared_boss']['boss']['source_hash'],boss['source_hash'])
        spec=json.loads(row['spec']);spec['map_name']=self.config['evaluation']['holdout_maps'][0]
        self.arena.db.execute('UPDATE match_jobs SET spec=? WHERE id=?',(json.dumps(spec),row['id']))
        with self.assertRaises(ArenaError):
            handle_request(self.arena,'beta',{'operation':'slice','payload':{'match_id':row['id'],'file':'summary.json'}})

    def test_migration_wiring_uses_explicit_preserved_sources_and_three_maps(self):
        self.install()
        selected={b:self.arena.db.one('SELECT accepted_revision FROM bots WHERE id=?',(b,))['accepted_revision']
                  for b in self.config['workers']}
        rid=bootstrap(self.arena,selected,self.config['evaluation']['screen_maps'])
        cases=self.arena.db.all('SELECT * FROM training_cases WHERE round_id=?',(rid,))
        self.assertEqual(len(cases),len(selected)*3*2)
        self.assertEqual({c['map_name'] for c in cases},set(self.config['evaluation']['screen_maps']))
        for c in cases:
            bot=c['a_bot'] if c['a_bot']!='boss' else c['b_bot']
            self.assertEqual(c['a_revision'] if c['a_bot']==bot else c['b_revision'],selected[bot])

    def test_boss_external_import_needs_private_trusted_collector_payload(self):
        boss,_=self.install()
        self.config['official_exploration'].update(enabled=True,share_feedback=True,
            bot_id='boss',feedback_bot_id='alpha',
            **{k:boss[k] for k in ['source_commit','source_hash','submission_id']})
        mid='00000000-0000-4000-8000-000000000018';rid='1'*32
        payload={'official_match_id':mid,'source_bot_id':'boss','source_commit':boss['source_commit'],
            'source_hash':boss['source_hash'],'submission_id':boss['submission_id'],'outcome':'B',
            'official_raw_statistics':{'request_id':rid},'files':{
                'observations.json':base64.b64encode(b'SYNTHETIC outside evidence').decode()}}
        with self.assertRaisesRegex(ArenaError,'trusted boss'):
            import_external(self.arena,'alpha',payload)
        atomic_json(self.root/'official-exploration/requests'/rid/(mid+'-import.json'),payload)
        from arena.exploration import Explorer
        explorer=Explorer(self.config,cli=object())
        self.assertFalse(explorer.import_payload(payload))
        requests=list((self.root/'inbox/alpha').glob('request-*.json'))
        self.assertEqual(len(requests),1)
        self.assertEqual(read_json(requests[0])['payload']['source_bot_id'],'boss')
        self.assertFalse((self.root/'inbox/boss').exists())
        import_external(self.arena,'alpha',payload)
        row=self.arena.db.one('SELECT metadata FROM external_matches WHERE official_id=?',(mid,))
        self.assertEqual(json.loads(row['metadata'])['source_bot_id'],'boss')

    def test_adding_boss_changes_only_future_evaluation_panels(self):
        boss,_=self.install()
        self.config['boss']['enabled']=False
        a=self.commit('alpha','before boss');old=self.arena.start_evaluation(a['id'])
        frozen=self.arena.db.one('SELECT suite FROM evaluations WHERE id=?',(old,))['suite']
        self.config['boss']['enabled']=True
        b=self.commit('beta','after boss');new=self.arena.start_evaluation(b['id'])
        self.assertEqual(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?',(old,))['suite'],frozen)
        suite=json.loads(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?',(new,))['suite'])
        self.assertIn(boss['revision_id'],suite['opponents'])
