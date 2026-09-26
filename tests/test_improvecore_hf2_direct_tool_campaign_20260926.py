import sys
sys.path.insert(0,"runtime")

from direct_tool_command_gateway import execute_direct_tool_commands
from entry_contract import MODE_GOAL_DIRECTED
from hf002_recursive_continuation import HF002RecursiveContinuation
from ic028_operator import GOAL_DIRECTED_STAGES
from improvement_core_learning_memory import LearningMemory
from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_regime import run_improvement_core_regime


def _handlers(phase):
    handlers={}

    def passthrough(stage):
        def fn(state):
            return {"state":{**state,"last_stage":stage},"material_delta":False}
        return fn

    for stage in GOAL_DIRECTED_STAGES:
        handlers[stage]=passthrough(stage)

    def recover_goal(state):
        return {
            "state":{
                **state,
                "goal":"Make repository-owned direct formal-tool invocation use the current full configured plan plus actual HF2 recurrence without duplicating PTI.",
            },
            "material_delta":False,
        }

    def formalize(state):
        if phase==0:
            finding="PLAN_FULL_BUT_GENERIC_HF2_ATTACHMENT_MISSING"
        elif phase==1:
            finding="SHARED_HF2_EXECUTION_PRIMITIVE_WORKS_FOR_DIRECT_AND_SELECTED_TOOL_PATHS"
        else:
            finding="RUNTIME_GATE_CLOSED_RELATIVE_IDENTITY_COORDINATE_DEFERRED_TO_THINK_BIG"
        return {
            "state":{**state,"phase_finding":finding},
            "material_delta":False,
        }

    def generate_work(state):
        if phase==0:
            candidates=(
                "DOCUMENT_HF2",
                "DIRECT_ONLY_HF2",
                "BRIDGE_ONLY_HF2",
                "SHARED_CONFIGURED_HF2_EXECUTION_PRIMITIVE",
            )
        elif phase==1:
            candidates=(
                "VERIFY_DIRECT_GATEWAY",
                "VERIFY_SELECTED_TOOL_BRIDGE",
                "CHECK_CONFIGURED_IDENTITY_RECURRENCE_COORDINATE",
            )
        else:
            candidates=("DEFER_IDENTITY_QUESTION_TO_FINAL_THINK_BIG",)
        return {"state":{**state,"candidates":candidates},"material_delta":False}

    def select(state):
        selected=(
            "SHARED_CONFIGURED_HF2_EXECUTION_PRIMITIVE"
            if phase==0
            else "CHECK_CONFIGURED_IDENTITY_RECURRENCE_COORDINATE"
            if phase==1
            else "DEFER_IDENTITY_QUESTION_TO_FINAL_THINK_BIG"
        )
        return {"state":{**state,"selected":selected},"material_delta":False}

    def execute(state):
        evidence={}
        if phase>=1:
            calls=[]
            def adapter(current,plan):
                n=int(current.get("n",0))+1
                calls.append(n)
                return {
                    "status":"EXECUTED",
                    "execution_truth":"IMPLEMENTATION_EXECUTED",
                    "state":{**current,"n":n},
                    "result":{"n":n},
                    "material_delta":True,
                    "hf2_live_local":n<2,
                }
            out=execute_direct_tool_commands(
                "run MT",
                state={"n":0},
                adapters={"MT":adapter},
            )
            evidence={
                "direct_status":out.status,
                "calls":tuple(calls),
                "recurrence_engine":out.executions[0].recurrence_engine,
                "recurrence_status":out.executions[0].recurrence_status,
                "recurrence_rounds":out.executions[0].recurrence_rounds,
            }
        return {
            "state":{
                **state,
                "execution_evidence":evidence,
            },
            "material_delta":phase<2,
            "delta":{
                "execution_truth_strengthened":phase<2,
                "material_relation_delta":phase<2,
            },
        }

    def admit(state):
        if phase==0:
            status="SHARED_GATE_SELECTED"
        elif phase==1:
            status="SHARED_GATE_EXECUTION_VERIFIED"
        else:
            status="RUNTIME_GATE_RELATIVE_CLOSE"
        return {
            "state":{
                **state,
                "stage_status":status,
                "identity_recurrence_coordinate":"OPEN_FOR_FINAL_THINK_BIG",
            },
            "material_delta":phase<2,
            "delta":{
                "execution_truth_strengthened":phase<2,
                "material_relation_delta":phase<2,
            },
        }

    def verify(state):
        if phase==0:
            ok=state.get("selected")=="SHARED_CONFIGURED_HF2_EXECUTION_PRIMITIVE"
        elif phase==1:
            ev=state.get("execution_evidence",{})
            ok=(
                ev.get("direct_status")=="EXECUTED"
                and ev.get("calls")== (1,2)
                and ev.get("recurrence_engine")=="HF002"
                and ev.get("recurrence_status")=="RELATIVE_CLOSE"
                and ev.get("recurrence_rounds")==2
            )
        else:
            ok=state.get("stage_status")=="RUNTIME_GATE_RELATIVE_CLOSE"
        return {
            "state":{**state,"verification":"PASS" if ok else "FAIL"},
            "material_delta":False,
        }

    def complete(state):
        terminal=state.get("verification")=="PASS"
        return {
            "state":{**state,"live_continuation":False},
            "terminal":terminal,
            "material_delta":False,
        }

    handlers.update({
        "RECOVER_GOAL":recover_goal,
        "FORMALIZE":formalize,
        "GENERATE_WORK":generate_work,
        "SELECT":select,
        "EXECUTE":execute,
        "ADMIT":admit,
        "VERIFY":verify,
        "COMPLETE":complete,
    })
    handlers["REENTER"]=lambda state:{"state":state,"terminal":True}
    return handlers


def _run_ic(state,memory):
    phase=int(state.get("hf2_round",0))
    out=run_improvement_core_regime(
        "Improvement Core. Fix direct formal-tool invocation using the IC123 rewrite.",
        target="repository-owned formal-tool invocation path",
        job="select and verify shared full-configured HF2 execution",
        basis="DIRECT_TOOL_HF2_CAMPAIGN_119",
        state=state,
        handlers=_handlers(phase),
        explicit_mode=MODE_GOAL_DIRECTED,
        observer_risk=False,
        learning_memory=LearningMemory(),
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="COMPLETE"
    return {
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "state":dict(out.result.state),
        "phase":phase,
    }


def _admit(raw,state,memory):
    phase=int(raw["phase"])
    nxt=dict(raw["state"])
    nxt["hf2_round"]=phase+1
    material=phase<2
    return nxt,{
        "material_result_delta":material,
        "material_relation_delta":material,
        "route_equivalence":f"DIRECT_TOOL_HF2_IC_PHASE_{phase}",
    }


def test_improvementcore_reapplies_under_hf2_multiple_times_before_relative_close():
    hf2=HF002RecursiveContinuation(
        run_capability=_run_ic,
        admit_normalize=_admit,
        trc_verify=lambda before,after,delta:{"terminal":True},
        hf1_classify=lambda before,after,delta:{"disposition":"STABLE"},
        live_local=lambda state,memory:int(state.get("hf2_round",0))<3,
        local_close=lambda state,memory:(
            int(state.get("hf2_round",0))>=3
            and state.get("stage_status")=="RUNTIME_GATE_RELATIVE_CLOSE"
        ),
        max_rounds=6,
    )

    out=hf2.run({"hf2_round":0},{})
    assert out["status"]=="RELATIVE_CLOSE"
    assert len(out["trace"])==3
    assert [row["disposition"] for row in out["trace"]]==[
        "REAPPLY_C","REAPPLY_C","RELATIVE_CLOSE"
    ]
    final=out["state"]
    assert final["verification"]=="PASS"
    assert final["identity_recurrence_coordinate"]=="OPEN_FOR_FINAL_THINK_BIG"
