"""Native Raise-the-Ceiling tool.

RTC is the configured high-level specialization of C48 Raise Ceiling. It returns
strict-gain candidates that preserve the declared protected basis, or a typed
no-gain result.
"""
from __future__ import annotations

from capability_runtime import execute_capability


def raise_the_ceiling(payload):
    return execute_capability("C48", dict(payload))
