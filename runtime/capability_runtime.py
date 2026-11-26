"""Executable dispatch for the complete C01-C49 capability registry."""
from a5_programs import CAPABILITY_BINDINGS


def execute_capability(program_id, payload):
    if not isinstance(program_id, str):
        raise KeyError(program_id)
    return CAPABILITY_BINDINGS[program_id](program_id, payload)
