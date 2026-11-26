"""Runner-independent archive recovery and cross-tool input routing regressions."""
import tempfile
import unittest
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

    def test_corrupt_and_missing_blobs_fail_before_output(self):
        sha=self.blob(b'good'); tree={'a':('100644',sha)}
        (self.blobs/sha).write_bytes(b'bad')
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_BLOB_MISMATCH'):
            self.assemble('bad.zip',tree)
        (self.blobs/sha).unlink()
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_BLOB_REQUIRED'):
            self.assemble('bad.zip',tree)
        self.assertFalse((self.root/'bad.zip').exists())

    def test_wrong_commit_and_cache_overwrite_rejected(self):
        tree={'a':('100644',self.blob(b'good'))}; sha,obj=self.basis(tree)
        with self.assertRaisesRegex(ValueError,'SOURCE_COMMIT_OBJECT_MISMATCH'):
            bootstrap.assemble_verified_archive(self.root/'bad.zip','f'*40,obj,tree,self.blobs,self.manifest,self.companions)
        self.assemble('old.zip',tree)
        with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_OUTPUT_OVERWRITES_CACHE'):
            self.assemble('old.zip',tree,self.root/'old.zip')


if __name__=='__main__':
    unittest.main()
