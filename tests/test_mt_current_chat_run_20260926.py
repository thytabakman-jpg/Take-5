import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from configured_function_ir import encode
from direct_tool_command_gateway import (
    bind_direct_tool_commands,
    execute_direct_tool_commands,
)
from mt_semantic_return_gate import run_mt_with_before_return_gate
from portable_tool_conductor import compilation_witness
from tool_reality_audit import audit_tool_reality

INPUT=ROOT/"artifacts"/"mt"/"MT_CURRENT_CHAT_INPUT_001_2026-09-26.json"


def _packet():
    return json.loads(INPUT.read_text(encoding="utf-8"))


def _semantic_findings(packet):
    facts={row["id"]:row for row in packet["facts"]}
    pd=encode("PD")
    reality=audit_tool_reality()

    findings=[
        {
            "id":"F1",
            "name":"REPOSITORY_FULL_TOOL_INVOCATION_REPAIR",
            "disposition":"CLOSED_RELATIVE",
            "claim":(
                "The repository-owned configured invocation path now binds ordinary registered "
                "tools to the full wrapper, D36_C, FULL_CONFIGURED_HF2_V1, and HF002 recurrence."
            ),
            "basis":("C3","C4","C5"),
        },
        {
            "id":"F2",
            "name":"FUNCTION_SURFACE_NOT_NATIVE_REALIZATION",
            "disposition":"OPEN",
            "claim":(
                "PD now has recovered configured identity and a native runtime, but this "
                "black-box episode still cannot execute PD without its required environment bindings."
            ),
            "basis":("C2","C7"),
            "pd_configured_identity":pd.configured_identity_status,
            "pd_realization":pd.realization_status,
            "pd_residuals":pd.residuals,
        },
        {
            "id":"F3",
            "name":"GOVERNED_KNOWLEDGE_CAPTURE_NOT_RECORD_EVERYTHING",
            "disposition":"PARTIAL",
            "claim":(
                "Durable material-knowledge capture solves governed-path persistence, but it is "
                "not equivalent to recording every raw conversation event or every external source."
            ),
            "basis":("C1","C8","C9","C10"),
        },
        {
            "id":"F4",
            "name":"RAW_CHAT_COMPLETENESS",
            "disposition":"OPEN",
            "claim":(
                "This MT run cannot certify exhaustive whole-chat conclusions because the active "
                "context contains summarized/skipped regions rather than a raw-complete transcript."
            ),
            "basis":("C10",),
        },
        {
            "id":"F5",
            "name":"STRONG_TOOL_REALITY",
            "disposition":reality.status,
            "claim":(
                "Configured identity and current finite-repertoire strong tool reality can both "
                "close relative while environment-bound execution remains a separate coordinate."
            ),
            "configured_identity_status":reality.configured_identity_status,
            "explicit_manifest_status":reality.explicit_manifest_status,
            "native_execution_status":reality.native_execution_status,
            "native_unrecovered":reality.native_unrecovered,
        },
        {
            "id":"F6",
            "name":"IMPROVEMENTCORE_HF2_COMPOSITION",
            "disposition":"OPEN",
            "claim":(
                "Portfolio-wide configured HF2 and ImprovementCore's regime-091 internal HF2 are "
                "both current. The adapter boundary must determine whether direct configured "
                "ImprovementCore invokes the one-pass surface or an already-HF2-wrapped surface; "
                "otherwise nested recurrence remains possible."
            ),
            "basis":("C3","C4","C5"),
        },
        {
            "id":"F7",
            "name":"HOST_INTERCEPTION_BOUNDARY",
            "disposition":"EXTERNAL_NOT_OWNED",
            "claim":(
                "Take-5 can make its own direct-tool path fail closed, but cannot force an unrelated "
                "host that never enters the repository gateway to use that path."
            ),
            "basis":("C8",),
        },
    ]
    return findings


def _mt_adapter(initial,plan):
    packet=initial["chat_evidence"]

    def run_mt(state):
        result={
            "target":packet["target"],
            "findings":_semantic_findings(packet),
            "black_boxes":tuple(packet["black_boxes"]),
            "quotient":(
                "configured invocation != native semantic realization",
                "function-shaped representation != recovered tool semantics",
                "governed knowledge capture != universal record-everything",
                "repository gateway != universal host interception",
                "portfolio HF2 != proof of safe ImprovementCore recurrence composition",
                "available chat context != raw-complete transcript",
            ),
        }
        return state,result

    def detect_black_boxes(state,result):
        return tuple(result["black_boxes"])

    def execute_stage(tool_id,object_id,state):
        witness=compilation_witness(tool_id)
        if witness.entrypoint is None or witness.required_environment:
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
        "state":{**initial,"mt_current_chat_result":result},
        "material_delta":False,
        "hf2_live_local":False,
        "hf2_local_close":gated.status!="OPEN",
        "trc_terminal":True,
        "evidence":(
            "direct_tool_command_gateway",
            "FULL_CONFIGURED_HF2_V1",
            "mt_semantic_return_gate",
            str(INPUT.relative_to(ROOT)),
        ),
    }


def test_current_chat_mt_runs_through_full_configured_gateway_and_fails_closed_on_live_black_boxes():
    packet=_packet()
    binding=bind_direct_tool_commands(
        "Run MT on this chat.",
        state={"chat_evidence":packet},
    )
    assert binding.tool_ids==("MT",)
    assert binding.complete

    plan=binding.bindings[0].plan
    assert plan.complete
    assert plan.wrapper_required is True
    assert plan.mode=="OBSERVER"
    assert plan.geometry=="D36_C"
    assert len(plan.cells)==36
    assert len(plan.questions)==22*36
    assert len(plan.cognitive)==4*36
    assert plan.recurrence_required is True
    assert plan.recurrence_engine=="HF002"
    assert plan.invocation_profile=="FULL_CONFIGURED_HF2_V1"

    out=execute_direct_tool_commands(
        "Run MT on this chat.",
        state={"chat_evidence":packet},
        adapters={"MT":_mt_adapter},
    )

    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_HF2_OPEN:MT"
    assert len(out.executions)==1

    execution=out.executions[0]
    assert execution.tool_id=="MT"
    assert execution.recurrence_engine=="HF002"
    assert execution.recurrence_status=="OPEN"
    assert execution.binding["cell_count"]==36
    assert execution.binding["question_count"]==792
    assert execution.binding["cognitive_count"]==144
    assert execution.binding["invocation_profile"]=="FULL_CONFIGURED_HF2_V1"

    result=execution.result
    assert result["semantic_gate_status"]=="OPEN"
    assert set(result["open_objects"])=={
        "CHAT_CORPUS_COMPLETENESS",
        "IMPROVEMENTCORE_HF2_COMPOSITION_BOUNDARY",
    }

    receipts=result["semantic_receipts"]
    assert receipts==[
        {
            "object_id":"CHAT_CORPUS_COMPLETENESS",
            "tool_id":"PD",
            "status":"OPEN",
            "material":False,
        },
        {
            "object_id":"IMPROVEMENTCORE_HF2_COMPOSITION_BOUNDARY",
            "tool_id":"PD",
            "status":"OPEN",
            "material":False,
        },
    ]

    findings={x["id"]:x for x in result["mt_result"]["findings"]}
    assert findings["F1"]["disposition"]=="CLOSED_RELATIVE"
    assert findings["F2"]["pd_realization"]=="ENVIRONMENT_BOUND"
    assert findings["F4"]["disposition"]=="OPEN"
    assert findings["F5"]["disposition"]=="CLOSED_RELATIVE"
    assert findings["F6"]["disposition"]=="OPEN"
    assert findings["F7"]["disposition"]=="EXTERNAL_NOT_OWNED"

    print(
        "MT_CURRENT_CHAT_RECEIPT="
        +json.dumps(
            {
                "gateway_status":out.status,
                "blocker":out.blocker,
                "binding":execution.binding,
                "recurrence":{
                    "engine":execution.recurrence_engine,
                    "status":execution.recurrence_status,
                    "rounds":execution.recurrence_rounds,
                },
                "result":result,
            },
            sort_keys=True,
            default=str,
        )
    )
