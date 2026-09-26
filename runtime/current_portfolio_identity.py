"""Current-basis portfolio identity audit.

This is deliberately distinct from open-world historical completeness.

For every configured tool in the current Take-5 repertoire, current identity is
closed relative to the declared basis when:
- ConfiguredRunSpec is complete;
- its canonical manifest is complete;
- every currently declared protected behavior is reconstructible;
- Protected Transition Integrity is reconstructible;
- and the global execution plan is complete.

A future recovered historical witness can reopen the affected tool identity
without invalidating the fact that the prior basis was explicitly closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from global_tool_execution import build_tool_execution_plan
from tool_manifest import manifest_for,reconstructs
from tool_run_registry import CONFIGURED_RUNS

@dataclass(frozen=True)
class CurrentToolIdentityAudit:
    status:str
    checked:int
    failures:tuple[str,...]

def audit_current_portfolio_identity()->CurrentToolIdentityAudit:
    failures=[]
    for tool_id,spec in CONFIGURED_RUNS.items():
        if not spec.complete():
            failures.append(f"{tool_id}:CONFIGURED_SPEC_INCOMPLETE")
            continue
        manifest=manifest_for(tool_id)
        if not manifest.complete():
            failures.append(f"{tool_id}:MANIFEST_INCOMPLETE")
            continue
        required=tuple(spec.protected_behaviors)+("PROTECTED_TRANSITION_INTEGRITY",)
        if not reconstructs(tool_id,required):
            failures.append(f"{tool_id}:PROTECTED_BEHAVIOR_UNRECOVERED")
        try:
            plan=build_tool_execution_plan(spec)
            if not plan.complete:
                failures.append(f"{tool_id}:EXECUTION_PLAN_INCOMPLETE")
        except Exception as exc:
            failures.append(f"{tool_id}:EXECUTION_PLAN:{type(exc).__name__}")
    return CurrentToolIdentityAudit(
        "CLOSED_RELATIVE" if not failures else "OPEN",
        len(CONFIGURED_RUNS),
        tuple(failures),
    )
