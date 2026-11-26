"""Bounded integration regressions against the authoritative native runtime."""
import hashlib
import unittest

from document_tool_adapters import bind_adapters, fnv
from execute_tool_packet import builtin_adapters
from direct_tool_command_gateway import execute_direct_tool_commands


class DocumentAdapterTests(unittest.TestCase):
    def setUp(self):
        self.sha = 'a' * 40
        self.source = {'path': 'example.md', 'sha': self.sha, 'latest_sha': self.sha}

    def invoke(self, tool, packet):
        # Exercise the actual provider and native implementation, not a stub.
        return bind_adapters(packet)[tool]({}, None)

    def currentness(self, source):
        return self.invoke('CurrentnessAudit', {'sources': [source]})

    def matrix_packet(self, *, inquiries=(), pair_count=1):
        raw = 'A x'
        proof = 'Two thresholds separated by probes 0 and 1.'
        return {'sources': [self.source], 'expected_ids': ['A'],
                'matrix': {'axes': ['tag'], 'raw': raw, 'transfer_fnv': fnv(raw)},
                'threshold': {'values': [0, 1], 'lower': 0, 'upper': 1,
                              'declared_pair_count': pair_count, 'proof': proof,
                              'proof_fnv': fnv(proof)},
                'open_coordinates': list(inquiries)}

    def test_unchanged_source_is_current(self):
        out = self.currentness(self.source)
        self.assertEqual(out['status'], 'EXECUTED')
        self.assertTrue(out['result']['complete'])
        self.assertEqual(out['result']['receipts'][0]['status'], 'CURRENT')
        self.assertEqual(out['adapter_provenance']['native_invocation'], 'RETURNED')

    def test_changed_source_stays_open(self):
        out = self.currentness({**self.source, 'latest_sha': 'b' * 40})
        self.assertEqual(out['status'], 'OPEN')
        self.assertEqual(out['result']['receipts'][0]['action'], 'RECONCILE_GENERATION_DELTA')
        self.assertFalse(out['result']['complete'])

    def test_missing_latest_source_stays_open(self):
        for latest in (None, ''):
            with self.subTest(latest=latest):
                out = self.currentness({**self.source, 'latest_sha': latest})
                self.assertEqual(out['status'], 'OPEN')
                self.assertFalse(out['result']['complete'])

    def test_invalid_source_identity_blocks_before_native_invocation(self):
        out = self.currentness({**self.source, 'latest_sha': 'not-a-sha'})
        self.assertEqual(out['status'], 'BLOCKED')
        self.assertEqual(out['adapter_provenance']['native_invocation'], 'NOT_INVOKED')

    def test_matrix_assertion_with_open_inquiry_does_not_close(self):
        out = self.invoke('ASSERT', self.matrix_packet(inquiries=['unresolved evidence']))
        self.assertEqual(out['status'], 'OPEN')
        self.assertEqual(out['result']['status'], 'OPEN')
        self.assertEqual(out['result']['state']['inquiries'], ('unresolved evidence',))
        self.assertTrue(all(v == 'TRUE' for v in out['result']['state']['world']['claim_test_status'].values()))

    def test_matrix_assertion_with_resolved_claims_closes(self):
        out = self.invoke('ASSERT', self.matrix_packet())
        self.assertEqual(out['status'], 'EXECUTED')
        self.assertEqual(out['result']['status'], 'CLOSED')
        self.assertEqual(out['adapter_provenance']['semantic_coverage'], 'BOUNDED_NOT_CERTIFIED')

    def test_false_matrix_assertion_does_not_close(self):
        out = self.invoke('ASSERT', self.matrix_packet(pair_count=2))
        self.assertEqual(out['status'], 'OPEN')
        self.assertIn('FALSE', out['result']['state']['world']['claim_test_status'].values())

    def test_quote_assertion_preserves_missing_refetch(self):
        text = 'A verified quotation.'
        raw = text.encode()
        sha = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
        packet = {'sources': [{'path': 'example.md', 'sha': sha, 'text': text}],
                  'assert_quotes': {'claims': [{'id': 'q', 'source': 'example.md', 'quote': text}]}}
        out = self.invoke('ASSERT', packet)
        self.assertEqual(out['status'], 'OPEN')
        self.assertEqual(out['result']['state']['inquiries'], ('q',))

    def test_missing_assertion_input_does_not_disable_currentness(self):
        packet = {'sources': [self.source]}
        out = self.invoke('ASSERT', packet)
        self.assertEqual(out['status'], 'OPEN')
        self.assertEqual(out['adapter_provenance']['native_invocation'], 'NOT_INVOKED')
        self.assertEqual(self.currentness(self.source)['status'], 'EXECUTED')

    def test_configured_gateway_preserves_unresolved_assertion(self):
        packet = self.matrix_packet(inquiries=['unresolved evidence'])
        out = execute_direct_tool_commands(['ASSERT'], adapters=bind_adapters(packet))
        self.assertEqual(out.status, 'OPEN')
        self.assertEqual(out.executions[0].recurrence_status, 'OPEN')

    def test_configured_gateway_closes_unchanged_currentness(self):
        out = execute_direct_tool_commands(['CurrentnessAudit'], adapters=bind_adapters({'sources': [self.source]}))
        self.assertEqual(out.status, 'EXECUTED')
        self.assertEqual(out.executions[0].recurrence_status, 'RELATIVE_CLOSE')


class BuiltinAdapterTests(unittest.TestCase):
    def setUp(self):
        self.packet = {'pd_frame': {'cases': [
            {'id': 'a', 'result': False, 'coordinates': {'x': 0, 'y': 0}},
            {'id': 'b', 'result': False, 'coordinates': {'x': 0, 'y': 1}},
            {'id': 'c', 'result': True, 'coordinates': {'x': 1, 'y': 0}},
            {'id': 'd', 'result': True, 'coordinates': {'x': 1, 'y': 1}},
        ], 'representations': {'xy': ['x', 'y']}},
            'prose': {'text': 'The example contains a claim.',
                      'contract': {'contract_id': 'example', 'constraints': ['AFFIRMATIVE_FIRST']}}}
        self.digest = 'fixture-packet-digest'

    def adapters(self, packet=None):
        return builtin_adapters(self.packet if packet is None else packet, self.digest)

    def test_builtin_and_explicit_bindings_remain_distinct(self):
        self.assertEqual(set(self.adapters()), {'PD', 'PDAudit', 'Prose'})
        self.assertFalse(set(self.adapters()) & set(bind_adapters({})))

    def test_pd_preserves_native_result_and_bounded_provenance(self):
        out = self.adapters()['PD']({}, None)
        self.assertEqual(out['status'], 'RELATIVE_CLOSE')
        self.assertEqual(out['result']['result']['minimal_sensitive'], {'xy': ((0,),)})
        self.assertEqual(out['execution_truth'], 'IMPLEMENTATION_EXECUTED')
        self.assertEqual(out['adapter_provenance']['semantic_coverage'], 'BOUNDED_NOT_CERTIFIED')
        self.assertIn('native:pd.run_pd', out['evidence'])
        self.assertIn('packet-sha256:' + self.digest, out['evidence'])

    def test_pdaudit_preserves_audit_controls(self):
        out = self.adapters()['PDAudit']({}, None)
        result = out['result']['result']
        self.assertEqual(out['status'], 'RELATIVE_CLOSE')
        self.assertEqual(result['minimal_sensitive'], {'xy': ((0,),)})
        self.assertEqual(result['kappa_A'], {'case_count': 4})
        self.assertEqual(result['kappa_Lambda'], {'representation_names': ['xy']})
        self.assertEqual(out['adapter_provenance']['native_invocation'], 'RETURNED')
        self.assertIn('native:pd_audit.run_pd_audit', out['evidence'])

    def test_missing_builtin_inputs_preserve_open_without_invocation(self):
        for tool, blocker in [('PD', 'PD_FRAME_REQUIRED'), ('PDAudit', 'PD_FRAME_REQUIRED'),
                              ('Prose', 'PROSE_TEXT_AND_CONTRACT_REQUIRED')]:
            with self.subTest(tool=tool):
                out = self.adapters({})[tool]({}, None)
                self.assertEqual(out['status'], 'OPEN')
                self.assertEqual(out['blocker'], blocker)
                self.assertEqual(out['adapter_provenance']['native_invocation'], 'NOT_INVOKED')

    def test_invalid_pd_frame_does_not_prevent_independent_prose_binding(self):
        packet = {**self.packet, 'pd_frame': {'cases': [self.packet['pd_frame']['cases'][0]] * 2,
                                              'representations': {'xy': ['x', 'y']}}}
        adapters = self.adapters(packet)
        for tool in ('PD', 'PDAudit'):
            with self.subTest(tool=tool), self.assertRaisesRegex(ValueError, 'DUPLICATE_PD_CASE_ID'):
                adapters[tool]({}, None)
        self.assertEqual(adapters['Prose']({}, None)['adapter_provenance']['native_invocation'], 'RETURNED')

    def test_prose_cannot_certify_host_supplied_semantic_pass_labels(self):
        packet = {**self.packet, 'prose': {**self.packet['prose'], 'evidence': {
            'semantic_preservation': 'PASS', 'earned_claim_strength': 'PASS',
            'no_unsupported_inflation': 'PASS', 'evidence': ['unverified host label']}}}
        out = self.adapters(packet)['Prose']({}, None)
        self.assertEqual(out['status'], 'OPEN')
        self.assertEqual(out['result']['status'], 'OPEN')
        self.assertIn('SEMANTIC_PRESERVATION_RECEIPT_REQUIRED', out['result']['residuals'])
        self.assertEqual(out['adapter_provenance']['native_invocation'], 'RETURNED')

    def test_prose_retains_native_constraint_violation(self):
        packet = {**self.packet, 'prose': {**self.packet['prose'], 'text': 'It is not merely a detail.'}}
        out = self.adapters(packet)['Prose']({}, None)
        self.assertEqual(out['status'], 'OPEN')
        self.assertEqual(out['result']['status'], 'REPAIR_REQUIRED')
        self.assertTrue(any(v['code'] == 'NOT_MERELY' for v in out['result']['violations']))

    def test_builtin_gateway_preserves_native_closure_and_open(self):
        for tool, expected, recurrence in [('PD', 'EXECUTED', 'RELATIVE_CLOSE'),
                                           ('PDAudit', 'EXECUTED', 'RELATIVE_CLOSE'),
                                           ('Prose', 'OPEN', 'OPEN')]:
            with self.subTest(tool=tool):
                out = execute_direct_tool_commands([tool], adapters=self.adapters())
                self.assertEqual(out.status, expected)
                self.assertEqual(out.executions[0].recurrence_status, recurrence)


if __name__ == '__main__':
    unittest.main()
