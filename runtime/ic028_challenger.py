"""IC-028 protected-behavior challenger gate for Jane/Take-5 closure.

This does not restore IC-028 authority. It prevents silent loss of its protected obligations.
"""
from dataclasses import dataclass

IC028_PROTECTED=(
"return_admission",
"execution_graph",
"owner_closure",
"orphan_ghost_consistency",
"persistence_recovery_idempotency",
"completion_certificate",
"work_obligation_quotient",
"package_policy_realizability",
"typed_retry_effects",
)

@dataclass(frozen=True)
class ParityDisposition:
    obligation:str
    status:str
    evidence:tuple=()

TERMINAL={"PRESERVED","SUBSUMED","NOT_APPLICABLE","OPEN"}

def parity_complete(dispositions):
    by={d.obligation:d for d in dispositions}
    return all(k in by and by[k].status in TERMINAL for k in IC028_PROTECTED)

def missing_obligations(dispositions):
    by={d.obligation:d for d in dispositions}
    return tuple(k for k in IC028_PROTECTED if k not in by or by[k].status not in TERMINAL)
