"""Recovery validator for current ImprovementCore.

This module provides an executable witness that the documented recovery surface
still reconstructs the current user-facing regime and that key currentness
pointers have not drifted.
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

EXPECTED_MERGE="4408dc5918f1593ecdada8cd7905a4c0346867e1"
EXPECTED_VALIDATION_RUN="36220020527"

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
        evidence=manifest.get("evidence",{})
        if evidence.get("merge_commit")!=EXPECTED_MERGE:
            failures.append("RECOVERY_MANIFEST_MERGE_DRIFT")
        if str(evidence.get("validation_run"))!=EXPECTED_VALIDATION_RUN:
            failures.append("RECOVERY_MANIFEST_VALIDATION_DRIFT")

        max_doc=_read("architecture/IMPROVEMENT_CORE_MAXIMIZATION_081.md")
        if "Status: IMPLEMENTED / VALIDATED / MERGED" not in max_doc:
            failures.append("MAXIMIZATION_STATUS_STALE")
        if EXPECTED_MERGE not in max_doc:
            failures.append("MAXIMIZATION_MERGE_WITNESS_MISSING")
        if EXPECTED_VALIDATION_RUN not in max_doc:
            failures.append("MAXIMIZATION_VALIDATION_WITNESS_MISSING")

        handoff=_read("integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md")
        marker="1. `integration/CURRENT_IMPROVEMENT_CORE.md`"
        if marker not in handoff:
            failures.append("HANDOFF_CURRENT_ANCHOR_MISSING")

    return {
        "status":"PASS" if not failures else "FAIL",
        "missing":missing,
        "failures":tuple(failures),
        "controller":resolution.controller,
        "entrypoint":resolution.entrypoint,
    }

if __name__=="__main__":
    result=validate_recovery()
    print(result)
    raise SystemExit(0 if result["status"]=="PASS" else 1)
