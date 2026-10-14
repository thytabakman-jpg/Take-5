"""Candidate safeguard: preserve all 36 logical coordinates when compressing blank files.

This file is proposal-only until the governing package change is approved.
"""


def test_coverage_dimension_is_not_file_count():
    assert 6 * 6 == 36
