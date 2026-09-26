import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from direct_tool_command_gateway import bind_direct_tool_commands, execute_direct_tool_commands
from mt_semantic_return_gate import run_mt_with_before_return_gate
from portable_tool_conductor import compilation_witness


PACKET={
    "target":"current tool-restriction problem after ImprovementCore rerun 123",
    "facts":[
        "CURRENT_REGISTERED_REPERTOIRE_FULL_INVOCATION is CLOSED_RELATIVE in Take-5.",
        "ImprovementCore rerun 123 completed successfully under IC-028 regime 091.",
        "The same commit passed Take-5 Validation.",
        "ImprovementCore selected IC-HOST-CAPABILITY-DISCOVERY as the strongest current strict-gain candidate.",
        "IC-HOST-CAPABILITY-DISCOVERY is ABSENT_IN_CORE_RUNTIME and classified OPEN_HOST_BOUNDARY.",
        "Universal ChatGPT host interception remains EXTERNAL_NOT_OWNED.",
        "IC-TRACE-EXPORT is admission-ready but does not solve host interception.",
        "Mandatory external host/platform restrictions remain outside Take-5 authority."
    ],
    "black_boxes":["HOST_CAPABILITY_DISCOVERY_BINDING"]
}


def _mt_adapter(initial,plan):
    packet=initial["evidence"]

    def run_mt(state):
        result={
            "target":packet["target"],
            "quotient":[
                "repository-owned invocation integrity != external host interception",
                "host capability discovery != host authority",
                "adapter discovery != removal of mandatory platform constraints",
                "successful ImprovementCore execution != universal future-host guarantee",
                "trace/export observability != host binding"
            ],
            "findings":[
                {
                    "id":"F1",
                    "name":"TAKE5_OWNED_TOOL_DOWNGRADE",
                    "disposition":"CLOSED_RELATIVE",
                    "claim":"Known Take-5-owned registered formal-tool routes preserve FULL_CONFIGURED_HF2_V1 and fail closed rather than silently weakening."
                },
                {
                    "id":"F2",
                    "name":"LATEST_IMPROVEMENTCORE_RUN",
                    "disposition":"EXECUTED_VERIFIED",
                    "claim":"ImprovementCore rerun 123 completed on regime 091 and the same commit passed Take-5 Validation."
                },
                {
                    "id":"F3",
                    "name":"PRIMARY_LIVE_RESIDUAL",
                    "disposition":"OPEN_HOST_BOUNDARY",
                    "claim":"The strongest current residual is typed host capability/adapter discovery, not another internal wrapper or HF2 repair."
                },
                {
                    "id":"F4",
                    "name":"HOST_DISCOVERY_SCOPE",
                    "disposition":"PARTIAL_TARGET",
                    "claim":"A typed host adapter registry/discovery contract can reduce silent host-tool binding failures but cannot compel an unrelated host to enter Take-5."
                },
                {
                    "id":"F5",
                    "name":"PLATFORM_AUTHORITY",
                    "disposition":"EXTERNAL_AUTHORITY_CONSTRAINT",
                    "claim":"Mandatory platform/system restrictions are not removable by Take-5, ImprovementCore, MT, or another repository wrapper."
                },
                {
                    "id":"F6",
                    "name":"SYSTEM_WIDE_END_STATE",
                    "disposition":"OPEN",
                    "claim":"The universal target requires a host-side integration contract that binds formal-tool requests to Take-5 and returns a verifiable execution receipt or explicit blocker."
                },
                {
                    "id":"F7",
                    "name":"TRACE_EXPORT",
                    "disposition":"ADMISSION_READY_SECONDARY",
                    "claim":"Trace export is a useful strict-gain candidate for observability, but it is secondary to host capability discovery for the present problem."
                }
            ],
            "black_boxes":packet["black_boxes"]
        }
        return state,result

    def detect_black_boxes(state,result):
        return tuple(result["black_boxes"])

    def execute_stage(tool_id,object_id,state):
        witness=compilation_witness(tool_id)
        if witness.entrypoint is None:
            return state,"OPEN",False
        return state,"CLOSED_RELATIVE",False

    gated=run_mt_with_before_return_gate(
        initial,
        run_mt=run_mt,
        detect_black_boxes=detect_black_boxes,
        execute_stage=execute_stage,
        max_rounds=4,
    )
    result={
        "semantic_gate_status":gated.status,
        "mt_result":gated.mt_result,
        "open_objects":gated.open_objects,
        "semantic_receipts":[
            {
                "object_id":r.object_id,
                "tool_id":r.tool_id,
                "status":r.status,
                "material":r.material,
            }
            for r in gated.semantic_receipts
        ],
        "rounds":gated.rounds,
    }
    return {
        "status":"OPEN" if gated.status=="OPEN" else "EXECUTED",
        "execution_truth":"SEMANTICALLY_APPLIED",
        "result":result,
        "state":{**initial,"mt_live_result":result},
        "material_delta":False,
        "hf2_live_local":False,
        "hf2_local_close":gated.status!="OPEN",
        "trc_terminal":True,
        "evidence":(
            "direct_tool_command_gateway",
            "FULL_CONFIGURED_HF2_V1",
            "mt_semantic_return_gate",
            "ImprovementCore workflow 36272657431",
            "Take-5 Validation 36272657416",
        ),
    }


def test_mt_live_after_improvecore_123():
    binding=bind_direct_tool_commands("Run MT",state={"evidence":PACKET})
    assert binding.tool_ids==("MT",)
    assert binding.complete
    plan=binding.bindings[0].plan
    assert plan.complete
    assert plan.wrapper_required is True
    assert plan.mode=="OBSERVER"
    assert plan.geometry=="D36_C"
    assert len(plan.cells)==36
    assert len(plan.questions)==792
    assert len(plan.cognitive)==144
    assert plan.recurrence_engine=="HF002"
    assert plan.invocation_profile=="FULL_CONFIGURED_HF2_V1"

    out=execute_direct_tool_commands(
        "Run MT",
        state={"evidence":PACKET},
        adapters={"MT":_mt_adapter},
    )
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_HF2_OPEN:MT"
    execution=out.executions[0]
    assert execution.tool_id=="MT"
    assert execution.recurrence_engine=="HF002"
    assert execution.binding["cell_count"]==36
    assert execution.binding["question_count"]==792
    assert execution.binding["cognitive_count"]==144
    result=execution.result
    assert result["semantic_gate_status"]=="OPEN"
    assert result["open_objects"]==("HOST_CAPABILITY_DISCOVERY_BINDING",)
    assert result["semantic_receipts"]==[
        {
            "object_id":"HOST_CAPABILITY_DISCOVERY_BINDING",
            "tool_id":"PD",
            "status":"OPEN",
            "material":False,
        }
    ]
    findings={x["id"]:x for x in result["mt_result"]["findings"]}
    assert findings["F1"]["disposition"]=="CLOSED_RELATIVE"
    assert findings["F3"]["disposition"]=="OPEN_HOST_BOUNDARY"
    assert findings["F5"]["disposition"]=="EXTERNAL_AUTHORITY_CONSTRAINT"
    assert findings["F6"]["disposition"]=="OPEN"
    print("MT_LIVE_RECEIPT="+json.dumps({
        "gateway_status":out.status,
        "blocker":out.blocker,
        "binding":execution.binding,
        "recurrence":{
            "engine":execution.recurrence_engine,
            "status":execution.recurrence_status,
            "rounds":execution.recurrence_rounds,
        },
        "result":result,
    },sort_keys=True,default=str))
