import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from direct_tool_command_gateway import bind_direct_tool_commands,execute_direct_tool_commands
from mt_semantic_return_gate import run_mt_with_before_return_gate
from portable_tool_conductor import compilation_witness
from tool_reality_audit import audit_tool_reality

INPUT=ROOT/"artifacts"/"mt"/"MT_WHOLE_CONVERSATION_INPUT_002_2026-09-27.json"

def packet():
    return json.loads(INPUT.read_text(encoding="utf-8"))

def findings(p):
    reality=audit_tool_reality()
    return [
        {"id":"F1","name":"DIRECT_TOOL_DOWNGRADE","disposition":"CLOSED_RELATIVE",
         "claim":"Registered direct-tool invocation is fail-closed onto the full configured wrapper/profile rather than silently degrading to a bare run."},
        {"id":"F2","name":"D36_AND_Q22_CURRENTNESS","disposition":"CLOSED_RELATIVE",
         "claim":"D36_C axes and Q01-Q22 semantics are recovered on the current basis; global minimality/completeness remains outside the claim."},
        {"id":"F3","name":"IMPROVEMENTCORE_HF2_COMPOSITION","disposition":"CLOSED_RELATIVE",
         "claim":"The current user-facing ImprovementCore path separates one-pass regime, local HF2, and parent-return recurrence, closing the earlier nested-HF2 ambiguity."},
        {"id":"F4","name":"SPECIFICATION_AUTHORITY_EFFECT_ORDER","disposition":"CLOSED_RELATIVE",
         "claim":"Current repository-governed paths separate recovery from transformation, authoritative formal emission, and callback effect licensing."},
        {"id":"F5","name":"STRONG_TOOL_REALITY","disposition":reality.status,
         "claim":"Configured identity and native executable realization remain distinct; strong whole-portfolio tool reality closes only when both are closed.",
         "configured_identity_status":reality.configured_identity_status,
         "explicit_manifest_status":reality.explicit_manifest_status,
         "native_execution_status":reality.native_execution_status,
         "native_unrecovered":reality.native_unrecovered,
         "environment_bound":reality.environment_bound},
        {"id":"F6","name":"PERSISTENCE_SCOPE","disposition":"PARTIAL",
         "claim":"Repository artifacts and durable governed knowledge capture materially reduce regression, but they do not equal capture of every raw chat utterance or inaccessible historical source."},
        {"id":"F7","name":"RAW_CHAT_COMPLETENESS","disposition":"OPEN",
         "claim":"This run cannot certify every raw message in the whole conversation because the active context contains summarized/skipped regions."},
        {"id":"F8","name":"HOST_INTERCEPTION","disposition":"EXTERNAL_NOT_OWNED",
         "claim":"Repository fail-closed routing does not force unrelated future ChatGPT hosts to enter Take-5."},
        {"id":"F9","name":"EXECUTION_TRUTH","disposition":"DISTINCTION_RECOVERED",
         "claim":"Semantic application, artifact creation, configured binding, native execution, persistence, and verified parent closure are distinct claim levels."},
    ]

def adapter(initial,plan):
    p=initial["chat_evidence"]
    def run_mt(state):
        result={
            "target":p["target"],
            "findings":findings(p),
            "black_boxes":tuple(p["black_boxes"]),
            "quotient":(
                "configured identity != native semantic realization",
                "artifact persistence != raw-complete conversation capture",
                "repository closure != universal host enforcement",
                "recovery legality != transformation authority != formal-emission authority",
                "semantic application != native configured execution",
                "basis-relative Q01-Q22 closure != global inquiry completeness",
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
            {"object_id":r.object_id,"tool_id":r.tool_id,"status":r.status,"material":r.material}
            for r in gated.semantic_receipts
        ],
        "rounds":gated.rounds,
    }
    return {
        "status":"OPEN" if gated.status=="OPEN" else "EXECUTED",
        "execution_truth":"SEMANTICALLY_APPLIED",
        "result":result,
        "state":{**initial,"mt_whole_conversation_result":result},
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

def test_mt_whole_conversation_uses_current_full_configured_path_and_preserves_open_black_boxes():
    p=packet()
    binding=bind_direct_tool_commands("Run MT on this whole conversation.",state={"chat_evidence":p})
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
    assert plan.recurrence_engine=="HF002"
    assert plan.invocation_profile=="FULL_CONFIGURED_HF2_V1"

    out=execute_direct_tool_commands(
        "Run MT on this whole conversation.",
        state={"chat_evidence":p},
        adapters={"MT":adapter},
    )
    assert out.status=="OPEN"
    execution=out.executions[0]
    assert execution.tool_id=="MT"
    assert execution.recurrence_engine=="HF002"
    assert execution.recurrence_status=="OPEN"
    assert execution.binding["cell_count"]==36
    assert execution.binding["question_count"]==792
    assert execution.binding["cognitive_count"]==144
    result=execution.result
    assert result["semantic_gate_status"]=="OPEN"
    assert set(result["open_objects"])==set(p["black_boxes"])
    fs={x["id"]:x for x in result["mt_result"]["findings"]}
    assert fs["F1"]["disposition"]=="CLOSED_RELATIVE"
    assert fs["F3"]["disposition"]=="CLOSED_RELATIVE"
    assert fs["F4"]["disposition"]=="CLOSED_RELATIVE"
    assert fs["F5"]["disposition"]=="CLOSED_RELATIVE"
    assert fs["F7"]["disposition"]=="OPEN"
    assert fs["F8"]["disposition"]=="EXTERNAL_NOT_OWNED"
    print("MT_WHOLE_CONVERSATION_RECEIPT="+json.dumps({
        "gateway_status":out.status,
        "blocker":out.blocker,
        "binding":execution.binding,
        "recurrence":{"engine":execution.recurrence_engine,"status":execution.recurrence_status,"rounds":execution.recurrence_rounds},
        "result":result,
    },sort_keys=True,default=str))
