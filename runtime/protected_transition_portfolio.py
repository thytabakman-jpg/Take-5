"""Portfolio audit for Protected Transition Integrity."""
from __future__ import annotations

from dataclasses import dataclass
from formal_object_registry import canonical_formal_label
from global_tool_execution import build_tool_execution_plan
from tool_manifest import reconstructs
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS


@dataclass(frozen=True)
class PTIPortfolioAudit:
    status:str
    failures:tuple[str,...]
    checked:int


def audit_protected_transition_portfolio()->PTIPortfolioAudit:
    failures=[]
    for tool in MATERIAL_TOOLS:
        spec=CONFIGURED_RUNS[tool]
        if not spec.complete():
            failures.append(f"{tool}:CONFIGURED_RUN_INCOMPLETE")
            continue
        if not reconstructs(tool,tuple(spec.protected_behaviors)+("PROTECTED_TRANSITION_INTEGRITY",)):
            failures.append(f"{tool}:PTI_MANIFEST_MISSING")
        try:
            plan=build_tool_execution_plan(spec)
            if not plan.complete:
                failures.append(f"{tool}:EXECUTION_PLAN_INCOMPLETE")
        except Exception as exc:
            failures.append(f"{tool}:EXECUTION_PLAN:{type(exc).__name__}")
        try:
            if canonical_formal_label(tool)!=tool:
                failures.append(f"{tool}:FORMAL_IDENTITY_DRIFT")
        except Exception:
            failures.append(f"{tool}:FORMAL_IDENTITY_MISSING")
    return PTIPortfolioAudit(
        "PASS" if not failures else "FAIL",
        tuple(failures),
        len(MATERIAL_TOOLS),
    )


if __name__=="__main__":
    out=audit_protected_transition_portfolio()
    print(out)
    raise SystemExit(0 if out.status=="PASS" else 1)
