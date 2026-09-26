"""Executable recovery check for Protected Transition Integrity."""
from pathlib import Path

from protected_transition_integrity import (
    COORDINATES,
    complete_receipt,
    require_protected_transition,
)
from protected_transition_portfolio import audit_protected_transition_portfolio

ROOT=Path(__file__).resolve().parents[1]

REQUIRED=(
    "integration/CURRENT_PROTECTED_TRANSITION_INTEGRITY.md",
    "architecture/PROTECTED_TRANSITION_INTEGRITY_090.md",
    "runtime/protected_transition_integrity.py",
    "runtime/protected_transition_portfolio.py",
    "tests/test_protected_transition_integrity.py",
    "tests/test_protected_transition_portfolio.py",
)

def validate_pti_recovery():
    missing=tuple(p for p in REQUIRED if not (ROOT/p).exists())
    failures=[]
    if missing:
        failures.append("MISSING_PTI_RECOVERY_SURFACES")

    audit=audit_protected_transition_portfolio()
    if audit.status!="PASS":
        failures.extend(audit.failures)

    evidence={x:f"recovery:{x}" for x in COORDINATES}
    try:
        require_protected_transition(
            complete_receipt(
                object_id="PTIRecovery",
                behavior_id="CHAIN",
                evidence=evidence,
            )
        )
    except Exception as exc:
        failures.append("PTI_COMPLETE_CHAIN_FAILED:"+type(exc).__name__)

    return {
        "status":"PASS" if not failures else "FAIL",
        "missing":missing,
        "failures":tuple(failures),
        "checked":audit.checked,
    }

if __name__=="__main__":
    out=validate_pti_recovery()
    print(out)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
