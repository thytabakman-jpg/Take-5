"""Executable recovery check for current HF1 mathematics."""
from pathlib import Path
from hf1_episode import classify_delta, select_sufficient_package
from tool_manifest import reconstructs

ROOT=Path(__file__).resolve().parents[1]
REQUIRED=(
    "integration/CURRENT_HF1.md",
    "architecture/HF1_MATHEMATICS_084.md",
    "runtime/hf1_episode.py",
    "tests/test_hf1_episode.py",
)

def validate_hf1_recovery():
    failures=[]
    missing=tuple(p for p in REQUIRED if not (ROOT/p).exists())
    if missing:
        failures.append("MISSING_HF1_RECOVERY_SURFACES")
    if not reconstructs("HF001",("HF001_GOVERNED_EPISODE",)):
        failures.append("HF1_CANONICAL_IDENTITY_INCOMPLETE")
    p=select_sufficient_package(("A","B"),{"X":["A"],"Y":["B"]})
    if set(p)!={"X","Y"}:
        failures.append("HF1_SUFFICIENT_COVER_DRIFT")
    base={"world_state":"w","discovery_state":"d","result_sensitive_state":"r"}
    delta=classify_delta(base,{**base,"world_state":"w2"})
    if not delta.world_changed or delta.discovery_changed or delta.result_sensitive_delta:
        failures.append("HF1_DELTA_SEMANTICS_DRIFT")
    return {"status":"PASS" if not failures else "FAIL","missing":missing,"failures":tuple(failures)}

if __name__=="__main__":
    out=validate_hf1_recovery()
    print(out)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
