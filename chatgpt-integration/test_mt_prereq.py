import hashlib
import unittest
from document_tool_adapters import _configured_mt_prerequisite, digest, bind_adapters
from direct_tool_command_gateway import execute_direct_tool_commands


class MTPrerequisiteTests(unittest.TestCase):
    def test_rejected_mt_payload_cannot_license_goal(self):
        packet={'sources':[]}
        for status in ('BLOCKED','CONFLICT'):
            with self.subTest(status=status):
                def worker(state,plan):
                    return {'status':status,'execution_truth':status,
                            'result':{'status':'CLOSED_RELATIVE','open_objects':(),'rounds':1,'state':{'packet':digest(packet)}},
                            'evidence':['native:mt_semantic_return_gate.run_mt_with_before_return_gate',f'packet:{digest(packet)}']}
                out,receipt=_configured_mt_prerequisite(packet,worker)
                self.assertEqual(out.executions[0].status,status)
                self.assertIsNone(receipt)

    def test_unbound_mt_claim_cannot_license_goal(self):
        packet={'sources':[]}
        def worker(state,plan):
            return {'status':'EXECUTED','execution_truth':'IMPLEMENTATION_EXECUTED',
                    'result':{'status':'CLOSED_RELATIVE','open_objects':(),'rounds':1,'state':{'packet':'stale'}},
                    'evidence':['native:mt_semantic_return_gate.run_mt_with_before_return_gate',f'packet:{digest(packet)}']}
        out,receipt=_configured_mt_prerequisite(packet,worker)
        self.assertIsNone(receipt)

    def test_actual_document_mt_open_remains_admissible(self):
        text='Goal: repair broken links.'
        sha=hashlib.sha1(f'blob {len(text.encode())}\0'.encode()+text.encode()).hexdigest()
        packet={'sources':[{'path':'a.md','sha':sha,'latest_sha':sha,'text':text}],
                'document_observations':{'target':'a.md','observations':[{'id':'g','source':'a.md','quote':text,'interpretation':'Governing goal.'}]},
                'goal_candidates':[{'id':'g','goal':{'X':'a.md','T':'repair broken links','I':'source','Sigma':'links resolve'},
                                    'constraints':[],'evidence':['g'],'grounded':True,'authority_typed':True,'determinate_enough':True,
                                    'authority_basis':'explicit goal','determination_basis':'exact text'}]}
        out=execute_direct_tool_commands(['GOAL'],adapters=bind_adapters(packet))
        e=out.executions[0]
        self.assertEqual(e.result['native']['status'],'CLOSED_RELATIVE')
        self.assertIn('MT_PREFLIGHT:OPEN',e.result['native']['evidence'])
