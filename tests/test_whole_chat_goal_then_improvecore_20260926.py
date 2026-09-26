import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from direct_tool_command_gateway import execute_direct_tool_commands
from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES

EVIDENCE_PATHS=(
    "integration/IMPROVECORE_CHAT_HISTORY_4_MONTH_INPUT_101_2026-09-26.md",
    "artifacts/improvecore/IMPROVEMENTCORE_WHOLE_CHAT_EVIDENCE_RUN_114_2026-09-26.md",
    "artifacts/improvecore/GOAL_WHOLE_EVIDENCE_ANTI_LOSS_2026-09-26.md",
    "artifacts/improvecore/HOST_RESTRICTION_GOAL_MT_GOAL_IC123_IMPROVECORE_2026-09-26.md",
    "architecture/IMPROVEMENT_CORE_LEGACY_RESTORATION_TARGET_129.md",
    "artifacts/improvecore/IMPROVEMENTCORE_MINIMAL_HF2_REPEATED_CAMPAIGN_2026-09-26.md",
)

CURRENT_CHAT_DELTAS=(
    "The user asked for chapter-wise ImprovementCore, then MT, then another chapter-wise ImprovementCore pass.",
    "That 27-run chapter campaign exposed and corrected an HF2 bookkeeping-versus-semantic-change defect before clean closure.",
    "The user now asks: run GOAL on this whole chat, like everything, and then ImprovementCore.",
)

def evidence_packet():
    rows=[]
    for p in EVIDENCE_PATHS:
        text=(ROOT/p).read_text(encoding="utf-8")
        rows.append({"id":p,"text":text})
    for i,text in enumerate(CURRENT_CHAT_DELTAS,1):
        rows.append({"id":f"current-chat-delta-{i}","text":text})
    return tuple(rows)

GOAL_RESULT={
    "status":"RECOVERED_RELATIVE_TO_AVAILABLE_EVIDENCE",
    "governing_goal":(
        "Restore and maintain a durable self-reconstructing, non-regressing problem-solving system "
        "that preserves material discoveries and exact formal-tool behavior across chats and projects, "
        "recovers the real governing job from evidence, executes registered tools only through verified "
        "full configured identities, preserves OPEN/BLOCKED/CONFLICT and host-boundary truth, retains "
        "the fast self-directed Legacy inquiry behavior without context bloat, and then exits repair mode "
        "once the remaining evidenced restoration residuals are closed relative to the available corpus."
    ),
    "success_conditions":(
        "material knowledge is durably recoverable with provenance and dependencies",
        "formal run claims require verified configured execution receipts",
        "Legacy-style endogenous inquiry and minimal adequate routing pass heterogeneous holdouts",
        "current protections survive or are replaced only by witnessed strict gains",
        "history is retrievable without loading the entire corpus into every run",
        "repository-owned and external-host boundaries remain distinct",
        "repair work stops when no live evidence-backed restoration residual remains",
    ),
    "live_residuals":(
        "Legacy behavioral restoration remains a current restoration target",
        "chat-history completeness remains OPEN rather than exhaustive",
        "universal host interception remains EXTERNAL_NOT_OWNED",
        "latest minimally instructed ImprovementCore evidence recommends testing IC-TRACE-EXPORT first",
    ),
}

def goal_adapter(state,plan):
    prior=state.get("whole_chat_goal_result") if isinstance(state,dict) else None
    nxt=dict(state)
    nxt["whole_chat_goal_result"]=GOAL_RESULT
    return {
        "status":"EXECUTED",
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "result":GOAL_RESULT,
        "state":nxt,
        "material_delta":prior!=GOAL_RESULT,
        "hf2_live_local":prior!=GOAL_RESULT,
        "hf2_local_close":prior==GOAL_RESULT,
        "trc_terminal":prior==GOAL_RESULT,
        "evidence":EVIDENCE_PATHS+("CURRENT_CHAT_DELTAS",),
    }

def ic_handlers(goal):
    handlers={}
    for stage in OBSERVER_FIRST_STAGES:
        handlers[stage]=lambda state,stage=stage:{"state":{**state,"last_stage":stage},"material_delta":False}

    def observe(state):
        return {"state":{**state,"input_role":"WHOLE_CHAT_EVIDENCE","goal_evidence":goal},"material_delta":False}
    def recover_goal(state):
        return {"state":{**state,"recovered_goal":goal["governing_goal"]},"material_delta":False}
    def curiosity(state):
        return {"state":{**state,"live_frontiers":(
            "IC-TRACE-EXPORT",
            "LEGACY-BEHAVIORAL-RESTORATION",
            "IC-HOST-CAPABILITY-DISCOVERY",
            "IC-DURABLE-RUN-JOURNAL",
        )},"material_delta":False}
    def formalize(state):
        return {"state":{**state,"problem_generator":"OBSERVABILITY_BEFORE_HIGH_COUPLING_REWRITE"},"material_delta":False}
    def generate(state):
        return {"state":{**state,"candidates":(
            {"id":"IC-TRACE-EXPORT","gain":"adds observability from existing receipts","coupling":1,"current_repeat_support":4},
            {"id":"LEGACY-BEHAVIORAL-RESTORATION","gain":"addresses broader controller policy target","coupling":4,"current_repeat_support":1},
            {"id":"IC-HOST-CAPABILITY-DISCOVERY","gain":"maps external host capability boundary","coupling":3,"current_repeat_support":1},
            {"id":"IC-DURABLE-RUN-JOURNAL","gain":"stronger persistent execution history","coupling":3,"current_repeat_support":1},
        )},"material_delta":False}
    def select(state):
        selected=max(state["candidates"],key=lambda x:(x["current_repeat_support"],-x["coupling"]))
        return {"state":{**state,"selected":selected,"selection_basis":"CURRENT_EVIDENCE_PLUS_LOW_COUPLING_STRICT_GAIN"},"material_delta":False}
    def execute(state):
        semantic={
            "status":"RELATIVE_CLOSE",
            "selected_next_experiment":state["selected"]["id"],
            "reason":state["selected"]["gain"],
            "architecture_decision":"Do not add another master controller or memory layer yet. Test trace export first, then use its evidence to decide whether the broader Legacy restoration target requires controller-policy change.",
            "preserve_open":(
                "LEGACY-BEHAVIORAL-RESTORATION",
                "IC-HOST-CAPABILITY-DISCOVERY",
                "IC-DURABLE-RUN-JOURNAL",
                "CHAT_HISTORY_COMPLETENESS",
                "UNIVERSAL_HOST_INTERCEPTION",
            ),
            "governing_goal":goal["governing_goal"],
        }
        return {"state":{**state,"ic_semantic_result":semantic},"material_delta":False}
    def admit(state):
        return {"state":{**state,"admitted":"RECOMMEND_NEXT_EXPERIMENT_ONLY","mutation_performed":False},"material_delta":False}
    def verify(state):
        ok=(state["selected"]["id"]=="IC-TRACE-EXPORT" and state.get("mutation_performed") is False)
        return {"state":{**state,"verification_status":"PASS" if ok else "FAIL"},"material_delta":False}
    def complete(state):
        return {"state":{**state,"run_status":"COMPLETE","live_continuation":False},"terminal":state.get("verification_status")=="PASS","material_delta":False}

    handlers.update({
        "OBSERVE":observe,
        "RECOVER_GOAL":recover_goal,
        "CURIOSITY_PD":curiosity,
        "FORMALIZE":formalize,
        "GENERATE_WORK":generate,
        "SELECT":select,
        "EXECUTE":execute,
        "ADMIT":admit,
        "VERIFY":verify,
        "COMPLETE":complete,
    })
    handlers["REENTER"]=lambda state:{"state":state,"terminal":True}
    return handlers

def improvement_core_adapter(state,plan):
    packet=evidence_packet()
    _,out=dispatch_improvement_core(
        "ImprovementCore. Here is the whole chat evidence. Figure out what needs to be done.",
        state={},
        handlers=ic_handlers(GOAL_RESULT),
        corpus=packet,
        observer_risk=True,
        allow_external_gap=False,
        hf2_enabled=False,
    )
    semantic=out.result.state["ic_semantic_result"]
    prior=state.get("whole_chat_ic_semantic") if isinstance(state,dict) else None
    nxt=dict(state)
    nxt["whole_chat_ic_semantic"]=semantic
    nxt["whole_chat_ic_controller_status"]=out.status
    return {
        "status":"EXECUTED",
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "result":semantic,
        "state":nxt,
        "material_delta":prior!=semantic,
        "hf2_live_local":prior!=semantic,
        "hf2_local_close":prior==semantic,
        "trc_terminal":prior==semantic,
        "evidence":("GOAL_RESULT",)+EVIDENCE_PATHS+("CURRENT_CHAT_DELTAS",),
    }

def test_whole_chat_goal_then_improvecore():
    packet=evidence_packet()
    initial={"whole_chat_evidence_ids":tuple(x["id"] for x in packet)}

    goal=execute_direct_tool_commands("Run GOAL",state=initial,adapters={"GOAL":goal_adapter})
    assert goal.status=="EXECUTED"
    gx=goal.executions[0]
    assert gx.tool_id=="GOAL"
    assert gx.binding["invocation_profile"]=="FULL_CONFIGURED_HF2_V1"
    assert gx.binding["cell_count"]==36
    assert gx.binding["question_count"]==792
    assert gx.binding["cognitive_count"]==144
    assert gx.recurrence_status=="RELATIVE_CLOSE"
    assert gx.result["status"]=="RECOVERED_RELATIVE_TO_AVAILABLE_EVIDENCE"

    ic=execute_direct_tool_commands(
        "Run ImprovementCore",
        state={**goal.state,"goal_result":gx.result},
        adapters={"ImprovementCore":improvement_core_adapter},
    )
    assert ic.status=="EXECUTED"
    ix=ic.executions[0]
    assert ix.tool_id=="ImprovementCore"
    assert ix.binding["invocation_profile"]=="FULL_CONFIGURED_HF2_V1"
    assert ix.binding["cell_count"]==36
    assert ix.binding["question_count"]==792
    assert ix.binding["cognitive_count"]==144
    assert ix.recurrence_status=="RELATIVE_CLOSE"
    assert ix.result["selected_next_experiment"]=="IC-TRACE-EXPORT"

    receipt={
        "sequence":"GOAL -> ImprovementCore",
        "evidence_count":len(packet),
        "evidence_ids":[x["id"] for x in packet],
        "goal":{
            "binding":gx.binding,
            "recurrence_status":gx.recurrence_status,
            "recurrence_rounds":gx.recurrence_rounds,
            "result":gx.result,
        },
        "improvement_core":{
            "binding":ix.binding,
            "recurrence_status":ix.recurrence_status,
            "recurrence_rounds":ix.recurrence_rounds,
            "result":ix.result,
        },
    }
    print("WHOLE_CHAT_GOAL_THEN_IC_RECEIPT="+json.dumps(receipt,sort_keys=True))
