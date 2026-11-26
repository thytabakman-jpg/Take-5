"""Runner-independent archive recovery and cross-tool input routing regressions."""
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from document_tool_adapters import bind_adapters, builtin_adapters, digest, fnv
from direct_tool_command_gateway import execute_direct_tool_commands
import runtime_bootstrap as bootstrap


class ScopedRoutingTests(unittest.TestCase):
    def packet(self):
        body='Goal: repair links.'
        sha=bootstrap.git_blob_sha(body.encode())
        raw='A x\nB x\nC x'
        return {'command':['GOAL','ASSERT','MultiObject','PDAudit'],
                'sources':[{'path':'a.md','sha':sha,'latest_sha':sha,'text':body,'refetched_text':body}],
                'tool_inputs':{
                    'GOAL':{'document_observations':{'target':'a.md','observations':[
                        {'id':'g','source':'a.md','quote':body,'interpretation':'Explicit goal.'}]},
                        'goal_candidates':[{'id':'g','goal':{'X':'a.md','T':'repair links','I':'navigation','Sigma':'links resolve'},
                        'constraints':['preserve content'],'evidence':['g'],'grounded':True,'authority_typed':True,'determinate_enough':True,
                        'authority_basis':'Explicit goal','determination_basis':'Explicit operation'}]},
                    'ASSERT':{'assert_quotes':{'claims':[{'id':'g','source':'a.md','quote':body}]}},
                    'MultiObject':{'matrix':{'axes':['tag'],'raw':raw,'transfer_fnv':fnv(raw)}},
                    'PDAudit':{'pd_frame':{'cases':[{'id':'a','result':False,'coordinates':{'x':0}},
                        {'id':'b','result':True,'coordinates':{'x':1}}], 'representations':{'x':['x']}}}}}

    def adapters(self, packet):
        return {**builtin_adapters(packet,'outer-packet'),**bind_adapters(packet)}

    def test_incompatible_families_independently_execute(self):
        packet=self.packet()
        adapters=self.adapters(packet)
        for tool in packet['command']:
            with self.subTest(tool=tool):
                result=adapters[tool]({},None)
                self.assertEqual(result['adapter_provenance']['native_invocation'],'RETURNED')
                self.assertEqual(result['adapter_provenance']['effective_input_sha256'],
                                 digest({'sources':packet['sources'],**packet['tool_inputs'][tool]}))
                self.assertEqual(execute_direct_tool_commands([tool],adapters=adapters).status,'EXECUTED')

    def test_genuine_ambiguity_and_shared_source_override_still_block(self):
        packet=self.packet()
        packet['tool_inputs']['GOAL']['matrix']=packet['tool_inputs']['MultiObject']['matrix']
        packet['tool_inputs']['ASSERT']['sources']=[]
        adapters=self.adapters(packet)
        for tool in ('GOAL','ASSERT'):
            self.assertEqual(adapters[tool]({},None)['adapter_provenance']['native_invocation'],'NOT_INVOKED')
            self.assertEqual(adapters[tool]({},None)['status'],'BLOCKED')
        self.assertEqual(adapters['MultiObject']({},None)['status'],'EXECUTED')

    def test_missing_route_does_not_suppress_other_tools(self):
        packet=self.packet()
        del packet['tool_inputs']['GOAL']
        adapters=self.adapters(packet)
        self.assertEqual(adapters['GOAL']({},None)['status'],'OPEN')
        self.assertEqual(adapters['ASSERT']({},None)['status'],'EXECUTED')


class ReadinessDiagnosticTests(unittest.TestCase):
    def test_provider_admission_and_unknown_execution_remain_distinct(self):
        from execute_tool_packet import _readiness_diagnostic
        for disposition in ('MISSING_ADAPTER','MISSING_OVERRIDE','INCOMPATIBLE_BINDING','PROVIDER_INITIALIZATION_FAILED'):
            with self.subTest(disposition=disposition):
                row={'status':'OPEN','adapter_disposition':disposition,'blocker':'missing'}
                out=_readiness_diagnostic(row)
                self.assertEqual(out['stage'],'PROVIDER_ADMISSION')
                self.assertEqual(out['configured_disposition'],'OPEN')
                self.assertEqual(out['batch_blocker'],'missing')
        self.assertEqual(_readiness_diagnostic({'adapter_disposition':'MISSING_ADAPTER'})['reported_native_invocation'],'NOT_INVOKED')
        self.assertEqual(_readiness_diagnostic({'adapter_disposition':'EXECUTION_ERROR','status':'BLOCKED'})['stage'],'UNRESOLVED_EXECUTION_STAGE')

    def test_packet_receipt_distinguishes_input_open_from_native_open(self):
        from execute_tool_packet import _execute_independent_tools, _packet_receipt
        sha='a'*40
        packet={'command':['MultiObject','CurrentnessAudit','PD'],
                'sources':[{'path':'a.md','sha':sha}]}
        adapters=bind_adapters(packet)
        manifest={'blobs':{'document_tool_adapters.py':sha}}
        ids=packet['command']
        raw=_execute_independent_tools(packet,ids,adapters,set(),None,set(),{},None,'packet',manifest,execute_direct_tool_commands)
        receipt=_packet_receipt(sha,sha,manifest,'packet',ids,None,set(),{},raw)
        rows={row['tool_id']:row for row in receipt['results']}
        for tool in ids:
            self.assertEqual(rows[tool]['status'],'OPEN')
        missing=rows['PD']['readiness_diagnostic']
        self.assertEqual(missing['stage'],'PROVIDER_ADMISSION')
        self.assertEqual(missing['reported_native_invocation'],'NOT_INVOKED')
        missing_input=rows['MultiObject']['readiness_diagnostic']
        self.assertEqual(missing_input['stage'],'INPUT_ADMISSION')
        self.assertEqual(missing_input['adapter_blocker'],'DOCUMENT_INPUT_REQUIRED:matrix')
        returned=rows['CurrentnessAudit']['readiness_diagnostic']
        self.assertEqual(returned['stage'],'NATIVE_RETURNED')
        self.assertEqual(returned['reported_native_invocation'],'RETURNED')
        self.assertEqual(returned['configured_disposition'],'OPEN')
        self.assertEqual(returned['reported_semantic_coverage'],'BOUNDED_NOT_CERTIFIED')
        self.assertTrue(all('readiness_diagnostic' not in row for row in raw))


class ArchitecturePathTests(unittest.TestCase):
    def test_declared_paths_are_distinct_from_execution_and_semantic_evidence(self):
        sha='a'*40
        packet={'command':['Architecture'],'sources':[{'path':'a.md','sha':sha}],
                'architecture_graph':{'expected_units':['a','b','c','d'],'dependency_path_roots':['a','c'],
                    'units':[{'id':uid,'source':'a.md','sha':sha,'role':'fixture','locator':uid,
                              'internal_dependencies':deps,'execution_dependencies':exe}
                             for uid,deps,exe in [('a',['b'],['b']),('b',['c'],[]),
                                                  ('c',[],[]),('d',[],[])]]}}
        result=execute_direct_tool_commands(['Architecture'],adapters=bind_adapters(packet))
        self.assertEqual(result.status,'OPEN')
        native=result.executions[0].result['result']
        interaction=native['InteractionState']
        self.assertEqual(interaction['declared_dependency_paths']['a']['c'],['a','b','c'])
        self.assertNotIn('c',interaction['declared_execution_paths']['a'])
        self.assertEqual(interaction['potential_transitive_consumers']['c'],['a','b'])
        self.assertEqual(native['SuccessorFrontier'],[])
        self.assertTrue(native['OpenConflictBlocked'])


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.companions=self.root/'companions'; self.companions.mkdir()
        self.blobs=self.root/'blobs'; self.blobs.mkdir()
        for name in bootstrap.INTEGRATION_FILES:
            (self.companions/name).write_text(name)
        self.manifest={'commit':'b'*40,'blobs':{n:bootstrap.git_blob_sha((self.companions/n).read_bytes())
                                               for n in bootstrap.INTEGRATION_FILES}}

    def basis(self, tree):
        obj=('tree '+bootstrap.git_tree_sha(tree)+'\n\nfixture\n').encode()
        return bootstrap.git_object_sha('commit',obj),obj

    def blob(self, data):
        sha=bootstrap.git_blob_sha(data)
        (self.blobs/sha).write_bytes(data)
        return sha

    def assemble(self, name, tree, cache=None):
        sha,obj=self.basis(tree)
        return bootstrap.assemble_verified_archive(self.root/name,sha,obj,tree,self.blobs,
                                                   self.manifest,self.companions,cache)

    def test_receipt_path_protects_inputs_and_verified_directories(self):
        archive=self.root/'archive.zip'
        archive.write_bytes(b'original')
        manifest=self.root/'manifest.json'
        manifest.write_bytes(b'identity')
        alias=self.root/'alias'
        alias.symlink_to(archive)
        hard=self.root/'hardlink'
        hard.hardlink_to(archive)
        runtime=self.root/'runtime'
        inputs=(archive, manifest, None)
        protected=((runtime, 'RECEIPT_INSIDE_VERIFIED_RUNTIME'),
                   (self.blobs, 'RECEIPT_INSIDE_BLOB_STORE'))
        cases=((archive, 'RECEIPT_OVERWRITES_VERIFIED_INPUT'),
               (manifest, 'RECEIPT_OVERWRITES_VERIFIED_INPUT'),
               (alias, 'RECEIPT_OVERWRITES_VERIFIED_INPUT'),
               (hard, 'RECEIPT_HARDLINK_NOT_ALLOWED'),
               (runtime/'receipt.json', 'RECEIPT_INSIDE_VERIFIED_RUNTIME'),
               (self.blobs/'receipt.json', 'RECEIPT_INSIDE_BLOB_STORE'))
        for path, reason in cases:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, reason):
                bootstrap.validate_receipt_path(path, inputs=inputs,
                                                protected_directories=protected)
        bootstrap.validate_receipt_path(self.root/'safe.json', inputs=inputs,
                                        protected_directories=protected)
        self.assertEqual(archive.read_bytes(), b'original')
        self.assertEqual(manifest.read_bytes(), b'identity')

    def test_bootstrap_rejects_receipt_overwriting_input_before_failure_write(self):
        manifest=self.root/'bad-manifest.json'
        manifest.write_bytes(b'not json')
        with patch('sys.argv', ['runtime_bootstrap.py', str(self.root/'archive.zip'),
                  '--expected-commit', 'a'*40, '--integration-manifest', str(manifest),
                  '--receipt', str(manifest)]):
            self.assertEqual(bootstrap.main(), 1)
        self.assertEqual(manifest.read_bytes(), b'not json')

    def test_packet_rejects_receipt_hardlink_before_failure_write(self):
        import execute_tool_packet
        packet=self.root/'packet.json'
        packet.write_bytes(b'original packet')
        receipt=self.root/'receipt.json'
        receipt.hardlink_to(packet)
        with patch('sys.argv', ['execute_tool_packet.py',
                  '--runtime', str(self.root/'runtime'), '--expected-commit', 'a'*40,
                  '--bootstrap-receipt', str(self.root/'absent-bootstrap.json'),
                  '--integration-manifest', str(self.root/'manifest.json'),
                  '--packet', str(packet), '--receipt', str(receipt)]):
            self.assertEqual(execute_tool_packet.main(), 1)
        self.assertEqual(packet.read_bytes(), b'original packet')

    def test_cache_and_new_blob_are_verified_then_installed(self):
        old=self.blob(b'old'); new=self.blob(b'new')
        tree={'a':('100644',old)}
        self.assemble('old.zip',tree)
        (self.blobs/old).unlink()
        tree['b']=('100755',new)
        result=self.assemble('current.zip',tree,self.root/'old.zip')
        self.assertEqual((result['reused_cache_blobs'],result['fetched_blobs']),(1,1))
        sha,_=self.basis(tree)
        root,receipt=bootstrap.install(self.root/'current.zip',self.root/'install',sha,self.manifest)
        self.assertEqual((root/'b').read_bytes(),b'new')
        self.assertEqual(receipt['verified_files'],2)

    def test_cache_reuses_renamed_and_duplicate_content_by_blob_identity(self):
        old=self.blob(b'old'); other=self.blob(b'other')
        self.assemble('old.zip',{'old/path':('100644',old),'unrelated':('100644',other)})
        (self.blobs/old).unlink()
        tree={'new/path':('100755',old),'duplicate':('100644',old)}
        cache=self.root/'old.zip'
        self.assertEqual(bootstrap.cached_source_blobs(cache,tree),{old:b'old'})
        result=self.assemble('current.zip',tree,cache)
        self.assertEqual((result['reused_cache_blobs'],result['fetched_blobs']),(2,0))
        self.assertEqual(result['unique_cached_blob_count'],1)
        self.assertEqual(result['unique_required_blob_count'],0)
        sha,_=self.basis(tree)
        root,receipt=bootstrap.install(self.root/'current.zip',self.root/'install',sha,self.manifest)
        self.assertEqual((root/'new/path').read_bytes(),b'old')
        self.assertEqual((root/'duplicate').read_bytes(),b'old')
        self.assertEqual(receipt['verified_files'],2)

    def test_cache_name_does_not_authorize_changed_content(self):
        old=self.blob(b'old'); new=self.blob(b'new')
        self.assemble('old.zip',{'same':('100644',old)})
        (self.blobs/new).unlink()
        tree={'same':('100644',new)}
        self.assertEqual(bootstrap.cached_source_blobs(self.root/'old.zip',tree),{})
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_BLOB_REQUIRED'):
            self.assemble('current.zip',tree,self.root/'old.zip')
        self.assertFalse((self.root/'current.zip').exists())

    def test_corrupt_and_missing_blobs_fail_before_output(self):
        sha=self.blob(b'good'); tree={'a':('100644',sha)}
        (self.blobs/sha).write_bytes(b'bad')
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_BLOB_MISMATCH'):
            self.assemble('bad.zip',tree)
        (self.blobs/sha).unlink()
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_BLOB_REQUIRED'):
            self.assemble('bad.zip',tree)
        self.assertFalse((self.root/'bad.zip').exists())

    def test_smoke_basis_reuse_preserves_test_and_environment_requirements(self):
        receipt={"test_files":["tests/"+name for name in bootstrap.TESTS],
                 "returncode":0,"registry_returncode":0,
                 "registry":{"routing_audit":{"status":"CLOSED_RELATIVE"}},
                 **bootstrap.observed_test_environment()}
        bootstrap.verify_smoke_basis(receipt)
        cases=[
            ({"returncode":False},"BOOTSTRAP_SMOKE_NOT_PASSED"),
            ({"registry_returncode":1},"BOOTSTRAP_SMOKE_NOT_PASSED"),
            ({"test_files":[]},"BOOTSTRAP_TEST_INVENTORY_CHANGED"),
            ({"registry":{"routing_audit":{"status":"OPEN"}}},"BOOTSTRAP_ROUTING_AUDIT_NOT_CLOSED"),
            ({"python":"different"},"BOOTSTRAP_TEST_ENVIRONMENT_CHANGED"),
            ({"dependency_versions":{}},"BOOTSTRAP_TEST_ENVIRONMENT_CHANGED"),
        ]
        for changes,reason in cases:
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError,reason):
                bootstrap.verify_smoke_basis({**receipt,**changes})

    def test_dispatch_rejects_stale_but_verified_commit(self):
        tree={'a':('100644',self.blob(b'good'))}
        sha,_=self.basis(tree)
        self.assemble('current.zip',tree)
        root,receipt=bootstrap.install(self.root/'current.zip',self.root/'install',sha,self.manifest)
        receipt.update(status="BOOTSTRAP_VERIFIED",runtime_path=str(root),
                       smoke={"test_files":["tests/"+name for name in bootstrap.TESTS],
                              "returncode":0,"registry_returncode":0,
                              "registry":{"routing_audit":{"status":"CLOSED_RELATIVE"}},
                              **bootstrap.observed_test_environment()})
        # Only the companion-directory location is substituted for the fixture.
        with patch.object(bootstrap,"__file__",str(self.companions/"runtime_bootstrap.py")):
            self.assertEqual(bootstrap.verify_bootstrap_receipt(root,receipt,self.manifest,
                                 expected_commit=sha),(sha,receipt["source_tree"]))
            with self.assertRaisesRegex(ValueError,"BOOTSTRAP_SOURCE_COMMIT_NOT_CURRENT"):
                bootstrap.verify_bootstrap_receipt(root,receipt,self.manifest,expected_commit="f"*40)

    def test_wrong_commit_and_cache_overwrite_rejected(self):
        tree={'a':('100644',self.blob(b'good'))}; sha,obj=self.basis(tree)
        with self.assertRaisesRegex(ValueError,'SOURCE_COMMIT_OBJECT_MISMATCH'):
            bootstrap.assemble_verified_archive(self.root/'bad.zip','f'*40,obj,tree,self.blobs,self.manifest,self.companions)
        self.assemble('old.zip',tree)
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_OUTPUT_OVERWRITES_CACHE'):
            self.assemble('old.zip',tree,self.root/'old.zip')


class CandidateProviderTests(unittest.TestCase):
    def setUp(self):
        self.sha='a'*40
        self.base={'sources':[{'path':'a.md','sha':self.sha}]}
        self.ev=[{'source_path':'a.md','source_sha':self.sha,'locator':'L1','basis':'fixture observation'}]

    def call(self, tool, key, spec, **extra):
        return bind_adapters({**self.base,key:spec,**extra})[tool]({},None)

    def test_discriminator_retains_unknown_and_closes_unique_evidenced_match(self):
        spec={'inventory_evidence':self.ev,'predicate':'matches the declared criterion',
              'candidates':[{'id':'a','decision':'MATCH','evidence':self.ev},
                            {'id':'b','decision':'UNKNOWN','evidence':self.ev}]}
        out=self.call('Discriminator','candidate_evidence',spec)
        self.assertEqual(out['status'],'OPEN')
        self.assertEqual(out['result']['unknown_candidates'],('b',))
        self.assertEqual(out['adapter_provenance']['native_invocation'],'RETURNED')
        spec['candidates'][1]['decision']='NO_MATCH'
        self.assertEqual(self.call('Discriminator','candidate_evidence',spec)['status'],'EXECUTED')
        self.assertEqual(self.call('Discriminator','candidate_evidence',spec,threshold={})['status'],'BLOCKED')

    def test_reconciler_preserves_type_sensitive_conflict_and_unknown(self):
        spec={'inventory_evidence':self.ev,'claims':[{'id':'a','key':'x','value':True,'evidence':self.ev},
                         {'id':'b','key':'x','value':1,'evidence':self.ev}]}
        out=self.call('Reconciler','reconcile_claims',spec)
        self.assertEqual(out['status'],'OPEN')
        self.assertEqual(out['result']['conflicts'],('x',))
        spec['claims'][1]['value']=None
        self.assertEqual(self.call('Reconciler','reconcile_claims',spec)['result']['open_coordinates'],('x',))
        spec['claims'][1]['value']=True
        self.assertEqual(self.call('Reconciler','reconcile_claims',spec)['status'],'EXECUTED')

    def test_rootcause_returns_native_open_and_rejects_unsupported_positive_flag(self):
        spec={'inventory_evidence':self.ev,'basis_id':'fixture','failure_class':['a','b'],
              'candidates':[{'id':'one','level':'LOCAL_MECHANISM','explains':['a'],
                             'evidence':self.ev,'unresolved':['cause not tested']}]}
        packet={**self.base,'root_cause':spec}
        out=self.call('RootCause','root_cause',spec)
        self.assertEqual(out['status'],'OPEN')
        self.assertEqual(out['adapter_provenance']['native_invocation'],'RETURNED')
        self.assertEqual(execute_direct_tool_commands(['RootCause'],adapters=bind_adapters(packet)).status,'OPEN')
        spec['candidates'][0]['removal_breaks_recurrence']=True
        out=self.call('RootCause','root_cause',spec)
        self.assertEqual(out['status'],'OPEN')
        self.assertEqual(out['adapter_provenance']['native_invocation'],'NOT_INVOKED')


if __name__=='__main__':
    unittest.main()
