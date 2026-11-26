"""Bounded integration regressions against the authoritative native runtime."""
import hashlib
import unittest

from document_tool_adapters import bind_adapters, fnv
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


if __name__ == '__main__':
    unittest.main()
