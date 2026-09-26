"""Recovery validator for current ImprovementCore.

This module provides a small executable witness that the documented recovery
surface still reconstructs the current user-facing regime.
"""
from __future__ import annotations

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
)

def validate_recovery()->dict:
    missing=tuple(p for p in REQUIRED_FILES if not (ROOT/p).exists())
    resolution=resolve_improvement_core_invocation("ImproveCore, recover current state")
    failures=[]
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
