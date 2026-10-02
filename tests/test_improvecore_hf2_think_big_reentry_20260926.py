import sys
sys.path.insert(0,"runtime")

from entry_contract import MODE_GOAL_DIRECTED
from full_invocation_portfolio import audit_full_invocation_portfolio
from global_tool_execution import execute_protected_transition
from hf002_recursive_continuation import HF002RecursiveContinuation
from ic028_operator import GOAL_DIRECTED_STAGES
from improvement_core_learning_memory import LearningMemory
from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_regime import CURRENT_REGIME, run_improvement_core_regime
from portable_tool_conductor import run_tool_conductor
from tool_run_registry import CONFIGURED_RUNS


def probes():
    pti_calls=[]
    def exec_root(value,plan):
        n=int(value.get("round",0))+1
        pti_calls.append(n)
        return (
            {"root":n},
            f"pti:{n}",
            {
                "next_payload":{"round":n},
                "material_delta":n<2,
                "hf2_live_local":n<2,
            },
        )
    pti=execute_protected_transition(
        CONFIGURED_RUNS["RootCause"],
        behavior_id="ROOT_CAUSE_ROOTNESS_SELECTOR",
        dispatch_fn=lambda plan:({"round":0},"dispatch"),
        execute_fn=exec_root,
        consume_fn=lambda value,plan:(value,"consume"),
        update_fn=lambda value,plan:(value,"update"),
        reentry_fn=lambda value,plan:(value,"reentry"),
        emission_audit_fn=lambda value,plan:"emit",
    )

    conductor_calls=[]
    def mt_adapter(packet):
        n=len(conductor_calls)+1
        conductor_calls.append(n)
        return {
            "status":"EXECUTED",
            "execution_truth":"SEMANTICALLY_APPLIED",
            "result":{"round":n},
            "material_delta":n<2,
            "hf2_live_local":n<2,
        }
    tc=run_tool_conductor({},adapters={"MT":mt_adapter})
    mt=next(row for row in tc["results"] if row["tool_id"]=="MT")
    return {
        "pti_calls":tuple(pti_calls),
        "pti_execution":pti.transition_receipt.evidence["execution"],
        "tc_calls":tuple(conductor_calls),
        "tc_recurrence":mt["recurrence"],
    }


def handlers(phase):
    out={}
    for stage in GOAL_DIRECTED_STAGES:
        out[stage]=lambda state,_stage=stage:{
            "state":{**state,"last_stage":_stage},
            "material_delta":False,
        }

    def recover(state):
        return {
            "state":{
                **state,
                "command":"Think big.",
                "goal":"Close remaining repository-owned full-invocation bypasses.",
            },
            "material_delta":False,
        }

    def execute(state):
        if phase==0:
            evidence=probes()
        elif phase==1:
            audit=audit_full_invocation_portfolio()
            evidence={
                "status":audit.status,
                "checked":audit.checked,
                "failures":audit.failures,
            }
        else:
            evidence={"closed":"CLOSED_RELATIVE"}
        return {
            "state":{**state,"evidence":evidence},
            "material_delta":phase<2,
            "delta":{"execution_truth_strengthened":phase<2},
        }

    def admit(state):
        return {
            "state":{
                **state,
                "repository_owned_full_invocation":(
                    "CLOSED_RELATIVE" if phase==2 else "VERIFYING"
                ),
                "universal_host_interception":"EXTERNAL_NOT_OWNED",
            },
            "material_delta":phase<2,
            "delta":{"resolved_open":phase<2},
        }

    def verify(state):
        ev=state["evidence"]
        if phase==0:
            ok=(
                ev["pti_calls"]==(1,2)
                and "configured-recurrence:HF002:RELATIVE_CLOSE:rounds=2"
                    in ev["pti_execution"]
                and ev["tc_calls"]==(1,2)
                and ev["tc_recurrence"]["engine"]=="HF002"
                and ev["tc_recurrence"]["status"]=="RELATIVE_CLOSE"
                and ev["tc_recurrence"]["rounds"]==2
            )
        elif phase==1:
            ok=(
                ev["status"]=="CLOSED_RELATIVE"
                and ev["checked"]==len(CONFIGURED_RUNS)
                and ev["failures"]==()
            )
        else:
            ok=(
                state["repository_owned_full_invocation"]=="CLOSED_RELATIVE"
                and state["universal_host_interception"]=="EXTERNAL_NOT_OWNED"
            )
        return {
            "state":{**state,"verification":"PASS" if ok else "FAIL"},
            "material_delta":False,
        }

    out.update({
        "RECOVER_GOAL":recover,
        "EXECUTE":execute,
        "ADMIT":admit,
        "VERIFY":verify,
        "COMPLETE":lambda state:{
            "state":{**state,"live_continuation":False},
            "terminal":state.get("verification")=="PASS",
            "material_delta":False,
        },
        "REENTER":lambda state:{"state":state,"terminal":True},
    })
    return out


def run_ic(state,memory):
    phase=int(state.get("round",0))
    result=run_improvement_core_regime(
        "Improvement Core. Think big.",
        target="post-merge full invocation system",
        job="recheck repository-owned execution bypasses",
        basis="THINK_BIG_REENTRY_122",
        state=state,
        handlers=handlers(phase),
        explicit_mode=MODE_GOAL_DIRECTED,
        observer_risk=False,
        learning_memory=LearningMemory(),
        knowledge_ledger=KnowledgeLedger(),
    )
    assert result.status=="COMPLETE"
    return {
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "state":dict(result.result.state),
        "phase":phase,
    }


def normalize(raw,state,memory):
    phase=int(raw["phase"])
    nxt=dict(raw["state"])
    nxt["round"]=phase+1
    material=phase<2
    return nxt,{
        "material_result_delta":material,
        "route_equivalence":f"THINK_BIG_REENTRY_{phase}",
    }


def test_post_merge_think_big_reentry_closes_remaining_bypasses():
    assert CURRENT_REGIME.version=="091"
    assert CURRENT_REGIME.default_local_recurrence=="HF002"

    hf2=HF002RecursiveContinuation(
        run_capability=run_ic,
        admit_normalize=normalize,
        trc_verify=lambda before,after,delta:{"terminal":True},
        hf1_classify=lambda before,after,delta:{"disposition":"STABLE"},
        live_local=lambda state,memory:int(state.get("round",0))<3,
        local_close=lambda state,memory:(
            int(state.get("round",0))>=3
            and state.get("repository_owned_full_invocation")=="CLOSED_RELATIVE"
            and state.get("verification")=="PASS"
        ),
        max_rounds=6,
    )
    result=hf2.run({"round":0},{})
    assert result["status"]=="RELATIVE_CLOSE"
    assert [row["disposition"] for row in result["trace"]]==[
        "REAPPLY_C","REAPPLY_C","RELATIVE_CLOSE"
    ]
    final=result["state"]
    assert final["command"]=="Think big."
    assert final["repository_owned_full_invocation"]=="CLOSED_RELATIVE"
    assert final["universal_host_interception"]=="EXTERNAL_NOT_OWNED"
    assert final["verification"]=="PASS"
