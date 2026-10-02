"""Repository-native protected execution receipt for the Kernel 053 ICC128 candidate.

This fixture executes the current ICC128 controller through Take-5's registered
D36_C configured plan, HF002 recurrence, and Protected Transition Integrity gate.
It is intentionally deterministic and evidence-only.  It proves repository
execution reachability; it does not claim external ChatGPT-host interception.
"""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from global_tool_execution import build_tool_execution_plan, execute_protected_transition
from icc128_episode_adapter import ICC128EpisodeAdapter
from tool_run_registry import CONFIGURED_RUNS


BEHAVIOR_ID="ICC128_ENDOGENOUS_CONTROLLER_LOOP"


def _episode_adapter():
    def gq(z,m):
        return [{"id":"q-receipt","question":"prove repository execution"}]

    def gw(q,z,m):
        return [{
            "id":"w-receipt",
            "jobs":(),
            "operation_class":"OBSERVE",
            "effect_class":"EVIDENCE_ONLY",
            "burden":1,
            "info_gain":1,
        }]

    def generic_execute(item,z,m):
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"repository_execution":"observed"},
            "material_delta":False,
            "evidence":("kernel053:repository-fixture:executed",),
        }

    def admit(results,z,m):
        return {
            "results":tuple(results),
            "execution_truth_strengthened":True,
        }

    def update(z,m,delta):
        z=dict(z); m=dict(m)
        z["terminal"]="COMPLETE"
        z["admitted_continuation"]=False
        m["repository_receipt_delta"]=delta
        return z,m

    return ICC128EpisodeAdapter(
        generate_questions=gq,
        generate_work=gw,
        admit_results=admit,
        update_state=update,
        generic_execute=generic_execute,
    )


def build_kernel053_repository_receipt():
    spec=CONFIGURED_RUNS["ICC128"]
    plan=build_tool_execution_plan(spec)
    adapter=_episode_adapter()

    packet={
        "job":"kernel053-repository-receipt",
        "identity":"KERNEL_MATH_CONTRACT_053",
        "authority":(),
        "local_authority":(),
        "external_job":"kernel053-repository-receipt",
        "frozen_target":"KERNEL_MATH_CONTRACT_053",
        "operational_goal":"prove configured ICC128 repository execution",
        "frozen_math":{
            "controller":"ICC128",
            "effect":"EVIDENCE_ONLY",
        },
        "frozen_math_fingerprint":"kernel053-repository-receipt-v1",
        "obligations":(),
    }

    def dispatch_fn(current_plan):
        assert current_plan.complete
        return packet,(
            f"dispatch:{current_plan.tool_id}:{current_plan.invocation_profile}:"
            f"{current_plan.geometry}:cells={len(current_plan.cells)}"
        )

    def execute_fn(payload,current_plan):
        result=adapter(payload)
        value={
            "status":result.status,
            "trace_count":len(result.traces),
            "selection_trace_count":len(result.selection_traces),
            "durable_receipt_count":len(result.durable_receipts),
            "controller":"ICC128",
        }
        evidence=(
            f"icc128:candidate:status={result.status}:"
            f"traces={len(result.traces)}:"
            f"selection={len(result.selection_traces)}"
        )
        hints={
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
        }
        return value,evidence,hints

    def consume_fn(executed,current_plan):
        assert executed["controller"]=="ICC128"
        assert executed["status"]=="COMPLETE"
        assert executed["trace_count"]==1
        return {
            "consumed":True,
            "controller":"ICC128",
            "execution":dict(executed),
        },"consume:icc128:candidate-result"

    def update_fn(consumed,current_plan):
        return {
            **consumed,
            "repository_state_updated":True,
            "configured_profile":current_plan.invocation_profile,
        },"state-update:kernel053:receipt-fixture"

    def reentry_fn(updated,current_plan):
        return {
            **updated,
            "reentry_checked":True,
            "reentry_disposition":"CLOSED_RELATIVE",
        },"reentry:icc128:closed-relative"

    def emission_audit_fn(reentered,current_plan):
        assert reentered["controller"]=="ICC128"
        assert reentered["reentry_checked"]
        return "emission:kernel053:repository-fixture:audit"

    protected=execute_protected_transition(
        spec,
        behavior_id=BEHAVIOR_ID,
        dispatch_fn=dispatch_fn,
        execute_fn=execute_fn,
        consume_fn=consume_fn,
        update_fn=update_fn,
        reentry_fn=reentry_fn,
        emission_audit_fn=emission_audit_fn,
    )

    receipt=protected.transition_receipt
    return {
        "status":"VERIFIED",
        "tool_id":"ICC128",
        "behavior_id":BEHAVIOR_ID,
        "invocation_profile":plan.invocation_profile,
        "mode":plan.mode,
        "geometry":plan.geometry,
        "cell_count":len(plan.cells),
        "native_count":len(plan.native),
        "question_count":len(plan.questions),
        "cognitive_count":len(plan.cognitive),
        "recurrence_engine":plan.recurrence_engine,
        "protected_transition":{
            "object_id":receipt.object_id,
            "behavior_id":receipt.behavior_id,
            "coordinates":{
                key:(value.value if hasattr(value,"value") else str(value))
                for key,value in receipt.coordinates.items()
            },
            "evidence":dict(receipt.evidence),
        },
        "external_host_interception":"EXTERNAL_NOT_OWNED",
    }


def write_kernel053_repository_receipt(path):
    receipt=build_kernel053_repository_receipt()
    target=Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(
        json.dumps(receipt,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    return receipt


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument(
        "--json-out",
        default="runtime/state/kernel053-repository-execution-receipt.json",
    )
    args=parser.parse_args()
    out=write_kernel053_repository_receipt(args.json_out)
    print(json.dumps(out,sort_keys=True))
