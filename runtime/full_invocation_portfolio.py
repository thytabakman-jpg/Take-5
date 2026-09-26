"""Whole-repertoire audit for the canonical full invocation profile.

This audit proves repository routing/execution reachability, not each tool's
domain-semantic correctness. Synthetic adapters witness that every currently
registered identity crosses the same full plan + recurrence path.
"""
from __future__ import annotations

from dataclasses import dataclass

from global_tool_execution import execute_protected_transition
from direct_tool_command_gateway import (
    bind_direct_tool_commands,
    direct_tool_ids,
    execute_direct_tool_commands,
)
from tool_manifest import reconstructs
from tool_run_registry import CONFIGURED_RUNS


REQUIRED_GENERIC_BEHAVIORS=(
    "PROTECTED_TRANSITION_INTEGRITY",
    "CONFIGURED_HF2_RECURRENCE",
    "FULL_CONFIGURED_INVOCATION_PROFILE",
)


@dataclass(frozen=True)
class FullInvocationPortfolioAudit:
    status:str
    checked:int
    failures:tuple[str,...]


def audit_full_invocation_portfolio()->FullInvocationPortfolioAudit:
    failures=[]

    for tool_id,spec in CONFIGURED_RUNS.items():
        expected_engine="SELF" if tool_id=="HF002" else "HF002"

        if not spec.complete():
            failures.append(f"{tool_id}:CONFIGURED_SPEC_INCOMPLETE")
            continue

        if spec.recurrence_engine!=expected_engine:
            failures.append(
                f"{tool_id}:RECURRENCE_ENGINE:{spec.recurrence_engine}"
            )

        if spec.invocation_profile!="FULL_CONFIGURED_HF2_V1":
            failures.append(
                f"{tool_id}:INVOCATION_PROFILE:{spec.invocation_profile}"
            )

        if not reconstructs(
            tool_id,
            tuple(spec.protected_behaviors)+REQUIRED_GENERIC_BEHAVIORS,
        ):
            failures.append(f"{tool_id}:MANIFEST_RECURRENCE_UNRECOVERED")

        try:
            ids=direct_tool_ids(f"run {tool_id}")
            if ids!=(tool_id,):
                failures.append(f"{tool_id}:DIRECT_RESOLUTION:{ids}")
                continue

            bound=bind_direct_tool_commands(f"run {tool_id}")
            if not bound.complete or len(bound.bindings)!=1:
                failures.append(f"{tool_id}:DIRECT_BINDING_INCOMPLETE")
                continue

            plan=bound.bindings[0].plan
            if not plan.complete:
                failures.append(f"{tool_id}:PLAN_INCOMPLETE")
            if len(plan.cells)!=36:
                failures.append(f"{tool_id}:CELL_COUNT:{len(plan.cells)}")
            if len(plan.questions)!=22*36:
                failures.append(
                    f"{tool_id}:QUESTION_COUNT:{len(plan.questions)}"
                )
            if len(plan.cognitive)!=4*36:
                failures.append(
                    f"{tool_id}:COGNITIVE_COUNT:{len(plan.cognitive)}"
                )
            if plan.recurrence_engine!=expected_engine:
                failures.append(
                    f"{tool_id}:PLAN_RECURRENCE:{plan.recurrence_engine}"
                )

            calls=[]
            def adapter(current,current_plan,_tool_id=tool_id):
                calls.append(
                    (
                        current_plan.tool_id,
                        current_plan.recurrence_engine,
                        len(current_plan.cells),
                    )
                )
                return {
                    "status":"EXECUTED",
                    "execution_truth":"IMPLEMENTATION_EXECUTED",
                    "result":{"portfolio_witness":_tool_id},
                    "material_delta":False,
                    "evidence":(
                        f"full-invocation-portfolio:{_tool_id}",
                    ),
                }

            out=execute_direct_tool_commands(
                f"run {tool_id}",
                adapters={tool_id:adapter},
            )
            if out.status!="EXECUTED":
                failures.append(f"{tool_id}:EXECUTION_STATUS:{out.status}")
            if calls!=[(tool_id,expected_engine,36)]:
                failures.append(f"{tool_id}:ADAPTER_CALL:{calls}")

            if not out.executions:
                failures.append(f"{tool_id}:EXECUTION_RECEIPT_MISSING")
            else:
                execution=out.executions[0]
                if execution.recurrence_engine!=expected_engine:
                    failures.append(
                        f"{tool_id}:RECEIPT_RECURRENCE:{execution.recurrence_engine}"
                    )
                expected_status=(
                    "SELF_CLOSE" if tool_id=="HF002" else "RELATIVE_CLOSE"
                )
                if execution.recurrence_status!=expected_status:
                    failures.append(
                        f"{tool_id}:RECURRENCE_STATUS:"
                        f"{execution.recurrence_status}"
                    )

            missing=execute_direct_tool_commands(
                f"run {tool_id}",
                adapters={},
            )
            if missing.status!="OPEN":
                failures.append(
                    f"{tool_id}:MISSING_ADAPTER_NOT_OPEN:{missing.status}"
                )
            if missing.blocker!=f"CONFIGURED_TOOL_ADAPTER_REQUIRED:{tool_id}":
                failures.append(
                    f"{tool_id}:MISSING_ADAPTER_BLOCKER:{missing.blocker}"
                )


            pti=execute_protected_transition(
                spec,
                behavior_id="FULL_CONFIGURED_INVOCATION_PROFILE",
                dispatch_fn=lambda current_plan,_tool_id=tool_id:(
                    {"tool_id":_tool_id},
                    f"portfolio-pti-dispatch:{_tool_id}",
                ),
                execute_fn=lambda value,current_plan,_tool_id=tool_id:(
                    {"tool_id":_tool_id,"executed":True},
                    f"portfolio-pti-execution:{_tool_id}",
                ),
                consume_fn=lambda value,current_plan,_tool_id=tool_id:(
                    {"consumed":value},
                    f"portfolio-pti-consume:{_tool_id}",
                ),
                update_fn=lambda value,current_plan,_tool_id=tool_id:(
                    {"updated":value},
                    f"portfolio-pti-update:{_tool_id}",
                ),
                reentry_fn=lambda value,current_plan,_tool_id=tool_id:(
                    {"reentered":value},
                    f"portfolio-pti-reentry:{_tool_id}",
                ),
                emission_audit_fn=lambda value,current_plan,_tool_id=tool_id:(
                    f"portfolio-pti-emission:{_tool_id}"
                ),
            )
            recurrence_ev=pti.transition_receipt.evidence.get("execution","")
            expected_recurrence=(
                "configured-recurrence:SELF:SELF_CLOSE:rounds=1"
                if tool_id=="HF002"
                else "configured-recurrence:HF002:RELATIVE_CLOSE:rounds=1"
            )
            if expected_recurrence not in recurrence_ev:
                failures.append(
                    f"{tool_id}:PTI_RECURRENCE_EVIDENCE:{recurrence_ev}"
                )

        except Exception as exc:
            failures.append(
                f"{tool_id}:FULL_INVOCATION:{type(exc).__name__}:{exc}"
            )

    return FullInvocationPortfolioAudit(
        "CLOSED_RELATIVE" if not failures else "OPEN",
        len(CONFIGURED_RUNS),
        tuple(failures),
    )


if __name__=="__main__":
    out=audit_full_invocation_portfolio()
    print(out)
    raise SystemExit(0 if out.status=="CLOSED_RELATIVE" else 1)
