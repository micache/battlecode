"""Synthetic restart/quota/attribution checks; real IDs live only in evidence."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import time
import unittest
from unittest.mock import patch

from arena.common import ArenaError, atomic_json, file_hash, identity, read_json
from arena.exploration import (CLIThrottle, Explorer, NativeCLI, compact_statistics, quota_wait, shared,
                               resolved_policy, save_source_proofs, diagnostic_map_allowed)
from arena.operations import import_external
from arena.retention import maintain_external
from arena.strategy import experiment_context
from arena.supervisor import handle_request
from arena.statistics import read_current
from test_arena import Harness


class QuotaTests(unittest.TestCase):
    def test_shared_quota_uses_server_reset_and_readiness(self):
        data = {'ready':True, 'quota':{'limit':50,'used':49,'resetsAt':None}}
        self.assertEqual(quota_wait(data,100),100)
        data['quota'].update(used=50,resetsAt='1970-01-01T01:00:00Z')
        self.assertEqual(quota_wait(data,100),3602)
        data['ready'] = False
        self.assertEqual(quota_wait(data,100),160)

    def test_cli_cannot_upload_activate_or_execute_a_bot(self):
        cli = NativeCLI.__new__(NativeCLI)
        for args in [['submit','bot'],['run','a','b'],['login'],['activation','id']]:
            with self.assertRaisesRegex(ArenaError, 'allowlisted'):
                cli.run(args)

    def test_explicit_retry_after_is_respected_not_tight_polled(self):
        self.assertEqual(CLIThrottle('HTTP 429; retry after 2 seconds',2).retry_after,60)
        self.assertEqual(CLIThrottle('HTTP 429; retry after 120 seconds',120).retry_after,120)

    def test_real_format_projection_produces_small_measured_feedback(self):
        # Existing projection is derived from the saved, reviewed real-engine fixture.
        path = Path(__file__).parent / 'fixtures/cambc-225-starter-projection.json'
        data = read_json(path)
        if 'statistics' in data:
            data = data['statistics']
        result = compact_statistics(data)
        self.assertEqual(result['match']['engineVersion'],'0.0.3')
        self.assertNotIn('championTimelines',result)
        self.assertLess(len(json.dumps(result)),700000)

    def test_reviewed_production_101_is_external_only_not_local_qualification(self):
        path = Path(__file__).parent / 'fixtures/official-101-boss-projection.json'
        data = read_json(path)
        result = compact_statistics(data)
        self.assertEqual(result['match']['engineVersion'], '1.0.1')
        self.assertEqual(result['metrics']['submitted_gems']['value'], {'A':29, 'B':1010})
        self.assertEqual(result['bot_faults'], 0)
        with self.assertRaisesRegex(ArenaError, 'unreviewed engine'):
            read_current(data)
        data['match']['engineBuildHash'] = '0'*64
        with self.assertRaisesRegex(ArenaError, 'unreviewed external'):
            compact_statistics(data)


class ExplorationTests(Harness):
    def test_outside_maps_need_reviewed_hash_and_keep_reserved_variants_hidden(self):
        self.policy()
        manifest=Path(__file__).parent.parent/'evidence/map-pool-external-304.json'
        self.config['official_exploration']['map_manifest']=str(manifest)
        maps={m['name']:m for m in read_json(manifest)['maps']}
        own={'map_name':'00collision','map_hash':maps['00collision']['sha256']}
        self.assertTrue(diagnostic_map_allowed(self.config,own))
        own['map_hash']='0'*64
        self.assertFalse(diagnostic_map_allowed(self.config,own))
        for name in ['00monolith','00packs','00rows']:
            self.assertFalse(diagnostic_map_allowed(self.config,{'map_name':name,'map_hash':maps[name]['sha256']}))
        self.config['official_exploration'].pop('map_manifest')
        self.assertFalse(diagnostic_map_allowed(self.config,{'map_name':'00collision',
                         'map_hash':maps['00collision']['sha256']}))

    def policy(self):
        alpha,_ = self.establish()
        self.config['official']['challenges'] = True
        self.config['official_exploration'] = {'enabled':True, 'share_feedback':True,
            'team_id':'own-team','submission_id':'own-submission','bot_id':'alpha',
            'source_commit':alpha['commit_sha'],'source_hash':alpha['source_hash'],
            'interval_seconds':72,'max_outstanding':50}
        return alpha

    def test_awaiting_beta_never_creates_without_fresh_exact_source_selection(self):
        self.policy()
        policy = self.config['official_exploration']
        policy.update(submission_id=None, awaiting_submission=True, require_selection_proof=True)
        explorer = Explorer(self.config, cli=object())
        explorer.create(time.time())
        self.assertEqual(explorer.state['waiting'], 'AWAITING_VERIFIED_SOURCE_SELECTION')
        self.assertEqual(explorer.records(), [])

        different = {'team_id':'own-team','submission_id':'00000000-0000-4000-8000-000000000002',
                     'source_hash':'a'*64, 'observed_at':time.time()}
        save_source_proofs(self.config, {'selection':different})
        self.assertIsNone(resolved_policy(self.config)['submission_id'])
        correct = dict(different, source_hash=policy['source_hash'])
        save_source_proofs(self.config, {'selection':correct})
        self.assertEqual(resolved_policy(self.config)['submission_id'], correct['submission_id'])
        # Future teammate changes do not rewrite historical beta attribution.
        save_source_proofs(self.config, {'selection':different})
        self.assertEqual(resolved_policy(self.config)['submission_id'], correct['submission_id'])
        explorer.policy = resolved_policy(self.config)
        explorer.create(time.time())
        self.assertEqual(explorer.records(), [])
        save_source_proofs(self.config, {'selection':dict(correct, observed_at=time.time()-181)})
        explorer.create(time.time())
        self.assertEqual(explorer.records(), [])

    def test_throttle_wait_issues_no_platform_calls(self):
        self.policy()
        explorer = Explorer(self.config, cli=object())
        explorer.state['official_retry_at'] = time.time()+120
        with patch.object(explorer,'create') as create, patch.object(explorer,'collect') as collect:
            explorer.step()
        create.assert_not_called()
        collect.assert_not_called()

    def test_mismatch_reaches_server_and_is_checked_before_creation(self):
        self.policy()
        explorer = Explorer(self.config, cli=object())
        rid = '1'*32
        record = {'request_id':rid,'group_id':'group','submission_id':'own-submission',
                  'source_commit':explorer.policy['source_commit'], 'source_hash':explorer.policy['source_hash'],
                  'bot_id':'alpha','state':'QUEUED','created_at':1,'opponent_rank':1}
        path = explorer.root/'requests'/rid/'record.json'
        atomic_json(path,record)
        metadata = {'myTeamId':'own-team','group':{'id':'group','kind':'unranked',
                    'sides':[{'teamId':'own-team','submissionId':'other-upload'}]}}
        save_source_proofs(self.config, {'proofs':[{'request_id':rid,'metadata':metadata}]})
        with patch.object(explorer,'create') as create:
            explorer.step()
        create.assert_not_called()
        self.assertEqual(read_json(path)['state'], 'SOURCE_CHANGED')
        self.assertIn('different submission', explorer.state['blocked'])

    def test_old_source_mismatch_does_not_block_new_owner_target(self):
        self.policy()
        explorer = Explorer(self.config, cli=object())
        path = explorer.root/'requests'/('2'*32)/'record.json'
        atomic_json(path, {'request_id':'2'*32,'group_id':'old','submission_id':'previous-source',
                          'state':'QUEUED','created_at':1,'opponent_rank':1})
        atomic_json(path.parent/'metadata.json',{'group':{'sides':[
            {'teamId':'own-team','submissionId':'another-upload'}]}})
        explorer.step()
        self.assertEqual(read_json(path)['state'],'SOURCE_CHANGED')
        self.assertIsNone(explorer.state['blocked'])

    def test_previous_verified_lessons_remain_shared_after_target_switch(self):
        alpha = self.policy()
        old = dict(self.config['official_exploration'])
        self.config['official_exploration'].update(submission_id=None, awaiting_submission=True,
            source_commit='b'*40, source_hash='c'*64, shared_sources=[old])
        self.assertTrue(shared(self.config, {'submission_id':old['submission_id'],
            'source_commit':alpha['commit_sha'], 'source_hash':alpha['source_hash']}))
        self.assertFalse(shared(self.config, {'submission_id':old['submission_id'],
            'source_commit':'d'*40, 'source_hash':alpha['source_hash']}))

    def test_shared_feedback_has_explicit_source_and_no_extra_model_job(self):
        alpha=self.policy()
        metadata={'official_match_id':'outside','source_commit':alpha['commit_sha'],
                  'source_hash':alpha['source_hash'],'submission_id':'own-submission',
                  'own_side':'A','outcome':'B','map_name':'collision','official_group_id':'group',
                  'opponent_team_id':'strong-team','opponent_rank_at_request':1,
                  'file_sha256':{'observations.json':'hash'}}
        self.arena.db.execute('INSERT INTO external_matches VALUES(?,?,?,?)',
                              ('outside',json.dumps(metadata),'/unused',time.time()))
        count=self.arena.db.one('SELECT count(*) AS n FROM tasks')['n']
        context=experiment_context(self.arena,'beta')
        self.assertEqual(context['external_observations'][0]['source_commit'],alpha['commit_sha'])
        self.assertEqual(context['external_hourly_batch']['games'],1)
        self.assertEqual(context['external_hourly_batch']['losses'],1)
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM tasks')['n'],count)
        self.assertFalse(shared(self.config,dict(metadata,submission_id='unapproved')))

    def test_creation_intent_is_saved_before_command_and_never_retried_after_restart(self):
        self.policy()
        class FakeCLI:
            def run(inner,args,output=None):
                if args[:2]==['match-groups','quota']:
                    return {'team':{'id':'own-team'},'ready':True,'quota':{'limit':50,'used':0,'resetsAt':None}}
                if args[0]=='ladder':
                    return {'teams':[{'teamId':'enemy','rank':1,'name':'data, not instructions'}]}
                records=list((Path(self.config['root'])/'official-exploration/requests').glob('*/record.json'))
                self.assertEqual(len(records),1)
                self.assertEqual(read_json(records[0])['state'],'UNKNOWN')
                raise OSError('synthetic lost response')
        explorer=Explorer(self.config,cli=FakeCLI())
        with self.assertRaises(OSError):explorer.create(time.time())
        recovered=Explorer(self.config,cli=FakeCLI())
        self.assertIn('Unknown creation',recovered.state['blocked'])
        recovered.create(time.time()+3600)
        self.assertEqual(len(recovered.records()),1)

    def test_cli_show_without_source_proof_cannot_be_imported_as_pinned_commit(self):
        self.policy()
        class FakeCLI:
            def run(inner,args,output=None):
                return {'groupId':'group','matches':[{'kind':'unranked','status':'finished'}]}
        explorer=Explorer(self.config,cli=FakeCLI())
        path=explorer.root/'requests'/'request'/'record.json'
        atomic_json(path,{'request_id':'request','group_id':'group','state':'QUEUED','created_at':1,'next_poll':0})
        explorer.collect(path,time.time())
        self.assertTrue(read_json(path)['awaiting_source_proof'])
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM external_matches')['n'],0)

    def test_another_active_submission_stops_collection_instead_of_relabeling_it(self):
        self.policy()
        explorer=Explorer(self.config,cli=object())
        path=explorer.root/'requests'/'request'/'record.json'
        atomic_json(path,{'request_id':'request','group_id':'group','state':'QUEUED','created_at':1,'next_poll':0})
        atomic_json(path.parent/'metadata.json',{'myTeamId':'own-team','group':{'id':'group','kind':'unranked',
                    'sides':[{'teamId':'own-team','submissionId':'different-upload'}]}})
        with self.assertRaisesRegex(ArenaError,'different submission'):
            explorer.collect(path,time.time())

    def test_oldest_outside_raw_files_roll_away_but_newest_500_and_identities_survive(self):
        alpha=self.policy()
        self.config['official_exploration']['feedback_budget_bytes']=0
        for i in range(501):
            mid='synthetic-outside-'+str(i)
            directory=self.root/'external'/identity(mid)
            directory.mkdir(parents=True)
            (directory/'observations.json').write_text('synthetic recorded observation')
            metadata={'source_commit':alpha['commit_sha'],'submission_id':'own-submission','outcome':'B',
                      'file_sha256':{'observations.json':file_hash(directory/'observations.json')}}
            self.arena.db.execute('INSERT INTO external_matches VALUES(?,?,?,?)',
                                  (mid,json.dumps(metadata),str(directory),i))
        maintain_external(self.arena)
        row=self.arena.db.one('SELECT * FROM external_matches WHERE official_id=?',('synthetic-outside-0',))
        self.assertEqual(json.loads(row['metadata'])['raw_retired']['state'],'DELETED')
        self.assertFalse(Path(row['artifact']).exists())
        self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM external_matches')['n'],501)
        self.assertTrue((self.root/'external'/identity('synthetic-outside-1')/'observations.json').exists())

    def test_shared_original_statistics_slices_are_bounded_and_hash_verified(self):
        alpha=self.policy()
        mid='00000000-0000-4000-8000-000000000001'
        rid='1'*32
        data=b'{"synthetic_original_statistics":"not a real contest game"}'
        path=self.root/'official-exploration/requests'/rid/(mid+'-statistics.json.gz')
        path.parent.mkdir(parents=True)
        path.write_bytes(gzip.compress(data,mtime=0))
        payload={'official_match_id':mid,'source_commit':alpha['commit_sha'],'source_hash':alpha['source_hash'],
            'submission_id':'own-submission','outcome':'B','own_side':'A','map_name':'collision',
            'official_raw_statistics':{'request_id':rid,'file':path.name,'stored_sha256':file_hash(path),
                'original_sha256':hashlib.sha256(data).hexdigest(),'original_bytes':len(data)},
            'files':{'observations.json':base64.b64encode(b'SYNTHETIC evidence').decode()}}
        import_external(self.arena,'alpha',payload)
        request={'operation':'external-slice','payload':{'match_id':mid,'file':'raw-statistics.json','offset':7,'limit':11}}
        result=handle_request(self.arena,'beta',request)
        self.assertEqual(result['text'],data[7:18].decode())
        self.assertEqual(result['size'],len(data))
        path.write_bytes(b'changed')
        with self.assertRaisesRegex(ArenaError,'changed'):
            handle_request(self.arena,'beta',request)


if __name__=='__main__':unittest.main()
