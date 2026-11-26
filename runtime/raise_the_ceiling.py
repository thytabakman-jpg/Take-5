"""Native Raise-the-Ceiling tool.

RTC is the configured high-level specialization of C48 Raise Ceiling. It returns
candidates with explicit gain and preservation evidence, a typed no-gain
result, or an unresolved disposition. Acceptance may retain unresolved
candidates; supplied flags do not prove protected-set coverage.
"""
from __future__ import annotations

from capability_runtime import execute_capability


def raise_the_ceiling(payload):
    return execute_capability("C48", dict(payload))
