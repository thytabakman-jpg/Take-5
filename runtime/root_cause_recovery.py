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

    # An executable synthetic intervention demonstrates each positive witness.
    # This verifies the RootCause proof gate, not a real-world causal attribution.
    def synthetic_failure(*,root_present:bool,rival_present:bool)->bool:
        return root_present

    with_root=synthetic_failure(root_present=True,rival_present=False)
    without_root=synthetic_failure(root_present=False,rival_present=False)
    with_rival_only=synthetic_failure(root_present=False,rival_present=True)
    with_both=synthetic_failure(root_present=True,rival_present=True)
    fixture_valid=(with_root and with_both and not without_root and not with_rival_only)
    root=RootCandidate(
        "R","ROOT_GENERATOR",frozenset({"A"}),
        evidence=frozenset({"synthetic:failure_with_R","synthetic:no_failure_without_R"})
                 if fixture_valid else frozenset(),
        survives_representation_change=bool(with_root and with_both),
        removal_breaks_recurrence=bool(with_root and not without_root),
        causal_test_evidence=frozenset({"synthetic:removal_stops_failure"})
                            if fixture_valid else frozenset(),
        rival_discrimination_evidence=frozenset({"synthetic:rival_only_no_failure"})
                                     if fixture_valid else frozenset(),
    )
    out=run_root_cause_hf2(
        failure_class={"A"},
        candidates=(root,),
        basis_id="recovery-synthetic-controlled",
    )
    if not fixture_valid or out.status!="RELATIVE_CLOSE" or out.root_candidates!=("R",):
        failures.append("ROOT_CAUSE_RUNTIME_DRIFT")

    # An otherwise identical root with unobserved causal/rival tests must not close.
    unwitnessed=RootCandidate(
        "UNTESTED","ROOT_GENERATOR",frozenset({"A"}),
        evidence=frozenset({"reported_only"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    negative=run_root_cause_hf2(
        failure_class={"A"},candidates=(unwitnessed,),basis_id="recovery-negative",
    )
    if negative.status=="RELATIVE_CLOSE" or negative.root_candidates:
        failures.append("ROOT_CAUSE_UNWITNESSED_PROMOTION")

    return {
        "status":"PASS" if not failures else "FAIL",
        "missing":missing,
        "failures":tuple(failures),
    }

if __name__=="__main__":
    out=validate_root_cause_recovery()
    print(out)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
