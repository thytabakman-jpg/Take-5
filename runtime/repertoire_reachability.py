"""Finite current-repertoire reachability evidence.

Reachability here means controller-visible configured execution reachability,
not universal direct natural-language aliases and not native semantic-runtime
completeness for every historical tool.

Every current configured tool must have a complete execution plan across the
declared global observer/D36_C shell and a reconstructible current identity.
"""
from dataclasses import dataclass
from current_portfolio_identity import audit_current_portfolio_identity
from protected_transition_portfolio import audit_protected_transition_portfolio

@dataclass(frozen=True)
class RepertoireReachability:
    status:str
    identity_checked:int
    transition_checked:int
    failures:tuple[str,...]

def audit_current_repertoire_reachability()->RepertoireReachability:
    identity=audit_current_portfolio_identity()
    transition=audit_protected_transition_portfolio()
    failures=tuple(identity.failures)+tuple(transition.failures)
    return RepertoireReachability(
        "CLOSED_RELATIVE" if not failures else "OPEN",
        identity.checked,
        transition.checked,
        failures,
    )
