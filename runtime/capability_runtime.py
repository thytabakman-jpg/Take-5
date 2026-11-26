"""Executable dispatch for the complete C01-C49 capability registry."""
from dataclasses import replace
from types import MappingProxyType
from program_registry import ProgramRegistry
from tool_run_registry import CAPABILITY_DEFINITIONS, EXPECTED_C
from a5_programs import (
    run_orient, run_map, run_attack, run_candidate_development, run_structural_improvement, run_improvement_evaluation, run_knowledge_transfer, run_verification
)


_FAMILY_BINDINGS = (
    (run_orient, ("C01", "C02", "C03", "C04", "C05", "C06")),
    (run_map, ("C07", "C08", "C09", "C10", "C11", "C12", "C13", "C49")),
    (run_attack, ("C14", "C15", "C16", "C17", "C18", "C19")),
    (run_candidate_development, ("C20", "C21", "C22", "C23")),
    (run_structural_improvement, ("C24", "C25", "C26", "C27", "C28", "C29", "C30", "C31")),
    (run_improvement_evaluation, ("C32", "C33", "C34", "C35", "C36")),
    (run_knowledge_transfer, ("C37", "C38", "C39", "C40", "C41", "C42", "C43")),
    (run_verification, ("C44", "C45", "C46", "C47", "C48")),
)


def _build_bindings():
    bindings = {}
    for handler, ids in _FAMILY_BINDINGS:
        for pid in ids:
            if pid in bindings:
                raise ValueError(f"Duplicate capability binding: {pid}")
            bindings[pid] = handler
    if set(bindings) != EXPECTED_C or set(CAPABILITY_DEFINITIONS) != EXPECTED_C:
        raise ValueError("Current capability definition/binding coverage mismatch")
    return MappingProxyType(bindings)


CAPABILITY_BINDINGS = _build_bindings()
REGISTRY = ProgramRegistry()
for _spec in CAPABILITY_DEFINITIONS.values():
    REGISTRY.register(replace(_spec, executable=_spec.program_id in CAPABILITY_BINDINGS))


def execute_capability(program_id, payload):
    if not isinstance(program_id, str):
        raise KeyError(program_id)
    return CAPABILITY_BINDINGS[program_id](program_id, payload)
