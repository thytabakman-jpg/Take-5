"""Recovery validator for current ImprovementCore.

Currentness is versioned against the live regime rather than frozen to one merge
hash. Historical merge/validation receipts remain provenance, while behavioral
identity is checked against the executable regime surface.
"""
from __future__ import annotations

import json
from pathlib import Path

from improvement_core_dispatch import resolve_improvement_core_invocation
from improvement_core_regime import CURRENT_REGIME

ROOT=Path(__file__).resolve().parents[1]

REQUIRED_FILES=(
    "integration/CURRENT_IMPROVEMENT_CORE.md",
    "architecture/IMPROVEMENT_CORE_RECOVERY_MANIFEST_082.json",
    "architecture/IMPROVEMENT_CORE_ACTIVATION_083.md",
    "architecture/IMPROVEMENT_CORE_MATHEMATICS_086.md",
    "architecture/IMPROVEMENT_CORE_MATH_CORPUS_INTEGRATION_090.md",
    "runtime/improvement_core_math.py",
    "runtime/improvement_core_math_spine.py",
    "tests/test_improvement_core_math_086.py",
    "runtime/improvement_core_dispatch.py",
    "runtime/improvement_core_regime.py",
    "runtime/improvement_core_manager.py",
    "runtime/ic028_operator.py",
    "runtime/improvement_core_recursive_manager.py",
    "runtime/improvement_core_learning_memory.py",
    "architecture/IMPROVEMENT_CORE_MAXIMIZATION_081.md",
    "architecture/CROSS_REPOSITORY_IMPROVEMENTCORE_LINEAGE_CHOICE_080.md",
    "research/IMPROVEMENT_CORE_USAGE_AUDIT_078_2026-09-26.md",
    "integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md",
)

def _read(rel:str)->str:
    return (ROOT/rel).read_text(encoding="utf-8")

def validate_recovery()->dict:
    missing=tuple(p for p in REQUIRED_FILES if not (ROOT/p).exists())
    failures=[]
    resolution=resolve_improvement_core_invocation("ImproveCore, recover current state")

    if missing:
        failures.append("MISSING_RECOVERY_SURFACES")
    if resolution.controller!="IC-028":
        failures.append("CONTROLLER_IDENTITY_DRIFT")
    if not resolution.entrypoint.endswith("run_improvement_core_regime"):
        failures.append("DISPATCH_REGIME_DRIFT")
    if CURRENT_REGIME.controller!="IC-028":
        failures.append("REGIME_CONTROLLER_DRIFT")
    if "improvement_core_manager" not in CURRENT_REGIME.stage_manager:
        failures.append("STAGE_MANAGER_MISSING")
    if "recursive_manager" not in CURRENT_REGIME.recursive_manager:
        failures.append("RECURSIVE_MANAGER_MISSING")
    if "learning_memory" not in CURRENT_REGIME.learning_memory:
        failures.append("LEARNING_MEMORY_MISSING")

    if not missing:
        manifest=json.loads(_read("architecture/IMPROVEMENT_CORE_RECOVERY_MANIFEST_082.json"))
        if manifest.get("status")!="CURRENT":
            failures.append("RECOVERY_MANIFEST_NOT_CURRENT")
        if manifest.get("controller")!="IC-028":
            failures.append("RECOVERY_MANIFEST_CONTROLLER_DRIFT")
        if manifest.get("invocation",{}).get("entrypoint")!="runtime.improvement_core_regime.run_improvement_core_regime":
            failures.append("RECOVERY_MANIFEST_ENTRYPOINT_DRIFT")
        if str(manifest.get("regime_version"))!=str(CURRENT_REGIME.version):
            failures.append("RECOVERY_MANIFEST_REGIME_VERSION_DRIFT")

        math_state=manifest.get("math",{})
        if math_state.get("current_surface")!="architecture/IMPROVEMENT_CORE_MATHEMATICS_086.md":
            failures.append("IMPROVEMENT_CORE_MATH_SURFACE_DRIFT")
        if math_state.get("preferred_controller")!="C_PLUS_JK":
            failures.append("IMPROVEMENT_CORE_MATH_IDENTITY_DRIFT")
        if math_state.get("runtime")!="runtime/improvement_core_math.py":
            failures.append("IMPROVEMENT_CORE_MATH_RUNTIME_DRIFT")

        regime=manifest.get("regime",{})
        if regime.get("recursive_activation")!="LIVE_CONTINUATION":
            failures.append("RECURSIVE_ACTIVATION_CONTRACT_MISSING")
        if regime.get("learning_activation")!="RECURSIVE_ROUTE_GATE_AND_STAGE_LEARNING_EVENTS":
            failures.append("LEARNING_ACTIVATION_CONTRACT_MISSING")

        max_doc=_read("architecture/IMPROVEMENT_CORE_MAXIMIZATION_081.md")
        if "Status: IMPLEMENTED / VALIDATED / MERGED" not in max_doc:
            failures.append("MAXIMIZATION_STATUS_STALE")

        anchor=_read("integration/CURRENT_IMPROVEMENT_CORE.md")
        if "Current regime version:\n- 084" not in anchor:
            failures.append("RECOVERY_ANCHOR_REGIME_VERSION_DRIFT")

        handoff=_read("integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md")
        if "1. `integration/CURRENT_IMPROVEMENT_CORE.md`" not in handoff:
            failures.append("HANDOFF_CURRENT_ANCHOR_MISSING")

    return {
        "status":"PASS" if not failures else "FAIL",
        "missing":missing,
        "failures":tuple(failures),
        "controller":resolution.controller,
        "entrypoint":resolution.entrypoint,
        "regime_version":CURRENT_REGIME.version,
    }

if __name__=="__main__":
    result=validate_recovery()
    print(result)
    raise SystemExit(0 if result["status"]=="PASS" else 1)
