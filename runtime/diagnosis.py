"""Native Diagnosis tool.

The recovered current Diagnosis job is failure-mechanism disposition before
repair. It is the named configured specialization of C17 Failure Diagnosis.
"""
from __future__ import annotations

from capability_runtime import execute_capability


def diagnose(payload):
    return execute_capability("C17", dict(payload))
