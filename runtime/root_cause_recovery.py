"""Executable recovery check for RootCause/HF002."""
from pathlib import Path
from tool_manifest import reconstructs
from formal_object_registry import canonical_formal_label
from root_cause import RootCandidate,run_root_cause_hf2

ROOT=Path(__file__).resolve().parents[1]

REQUIRED=(
    "integration/CURRENT_ROOT_CAUSE.md",
    "integration/CURRENT_HF2.md",
    "architecture/ROOT_CAUSE_MATHEMATICS_087.md",
    "research/MT_ROOT_CAUSE_WHOLE_CHAT_088_2026-09-26.md",
    "runtime/root_cause.py",
    "runtime/root_cause_managed.py",
    "runtime/hf002_recursive_continuation.py",
    "tests/test_root_cause_hf2.py",
)

def validate_root_cause_recovery():
    failures=[]
    missing=tuple(p for p in REQUIRED if not (ROOT/p).exists())
    if missing:
        failures.append("MISSING_ROOT_CAUSE_RECOVERY_SURFACES")
    if canonical_formal_label("Root Cause")!="RootCause":
        failures.append("ROOT_CAUSE_ALIAS_DRIFT")
    if canonical_formal_label("HF2")!="HF002":
        failures.append("HF2_ALIAS_DRIFT")
    if not reconstructs("HF002",("HF002_LOCAL_RECURSIVE_CONTINUATION",)):
        failures.append("HF2_MANIFEST_DRIFT")
    if not reconstructs("RootCause",(
        "ROOT_CAUSE_ROOTNESS_SELECTOR",
        "ROOT_CAUSE_HF002_LOCAL_RECURRENCE",
        "ROOT_CAUSE_IMPROVEMENTCORE_PARENT_HANDOFF",
    )):
        failures.append("ROOT_CAUSE_MANIFEST_DRIFT")

    root=RootCandidate(
        "R","ROOT_GENERATOR",frozenset({"A"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    out=run_root_cause_hf2(
        failure_class={"A"},
        candidates=(root,),
        basis_id="recovery",
    )
    if out.status!="RELATIVE_CLOSE" or out.root_candidates!=("R",):
        failures.append("ROOT_CAUSE_RUNTIME_DRIFT")

    return {
        "status":"PASS" if not failures else "FAIL",
        "missing":missing,
        "failures":tuple(failures),
    }

if __name__=="__main__":
    out=validate_root_cause_recovery()
    print(out)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
