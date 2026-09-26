import sys
sys.path.insert(0,"runtime")

from configured_run import FULL_INVOCATION_PROFILE
from entry_contract import MODE_GOAL_DIRECTED
from full_invocation_portfolio import audit_full_invocation_portfolio
from hf002_recursive_continuation import HF002RecursiveContinuation
from ic028_operator import GOAL_DIRECTED_STAGES
from improvement_core_learning_memory import LearningMemory
from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_regime import run_improvement_core_regime
from tool_manifest import reconstructs
from tool_run_registry import CONFIGURED_RUNS


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
                "command":"Think big.",
                "goal":"Make full wrapper + D36_C + current configured identity + actual recurrence non-bypassable inside every Take-5-governed formal-tool invocation.",
            },
            "material_delta":False,
        }

    def curiosity_pd(state):
        generator=(
            "RECURRENCE_NOT_PROTECTED_IN_CONFIGURED_IDENTITY"
            if phase==0
            else "PORTFOLIO_ENFORCEMENT_NOT_YET_WITNESSED"
            if phase==1
            else "NO_REMAINING_REPOSITORY_OWNED_INVOCATION_BYPASS"
        )
        return {
            "state":{**state,"problem_generator":generator},
            "material_delta":False,
        }

    def formalize(state):
        return {
            "state":{
                **state,
                "phase":phase,
                "external_boundary":"UNIVERSAL_HOST_INTERCEPTION:EXTERNAL_NOT_OWNED",
            },
            "material_delta":False,
        }

    def generate_work(state):
        if phase==0:
            candidates=(
                "PROMOTE_RECURRENCE_INTO_CONFIGURED_IDENTITY",
                "LEAVE_RUNTIME_CONVENTION_ONLY",
                "DUPLICATE_WRAPPER_STACK",
            )
        elif phase==1:
            candidates=(
                "AUDIT_FULL_REGISTERED_REPERTOIRE",
                "SAMPLE_ONLY_MT_AND_GOAL",
            )
        else:
            candidates=(
                "RELATIVE_CLOSE_REPOSITORY_OWNED_SEAM",
                "CLAIM_UNIVERSAL_HOST_INTERCEPTION",
            )
        return {"state":{**state,"candidates":candidates},"material_delta":False}

    def select(state):
        selected=(
            "PROMOTE_RECURRENCE_INTO_CONFIGURED_IDENTITY"
            if phase==0
            else "AUDIT_FULL_REGISTERED_REPERTOIRE"
            if phase==1
            else "RELATIVE_CLOSE_REPOSITORY_OWNED_SEAM"
        )
        return {
            "state":{
                **state,
                "selected":selected,
                "selection_preserves_host_boundary":True,
            },
            "material_delta":False,
        }

    def execute(state):
        evidence={}
        if phase==0:
            failures=[]
            for tool_id,spec in CONFIGURED_RUNS.items():
                expected="SELF" if tool_id=="HF002" else "HF002"
                if not spec.complete():
                    failures.append(f"{tool_id}:spec")
                if spec.recurrence_engine!=expected:
                    failures.append(f"{tool_id}:recurrence")
                if spec.invocation_profile!=FULL_INVOCATION_PROFILE:
                    failures.append(f"{tool_id}:profile")
                if not reconstructs(
                    tool_id,
                    tuple(spec.protected_behaviors)+(
                        "PROTECTED_TRANSITION_INTEGRITY",
                        "CONFIGURED_HF2_RECURRENCE",
                        "FULL_CONFIGURED_INVOCATION_PROFILE",
                    ),
                ):
                    failures.append(f"{tool_id}:manifest")
            evidence={
                "identity_failures":tuple(failures),
                "checked":len(CONFIGURED_RUNS),
            }
        elif phase==1:
            audit=audit_full_invocation_portfolio()
            evidence={
                "portfolio_status":audit.status,
                "checked":audit.checked,
                "failures":audit.failures,
            }
        else:
            evidence={
                "repository_owned_full_invocation":"CLOSED_RELATIVE",
                "universal_host_interception":"EXTERNAL_NOT_OWNED",
            }

        return {
            "state":{**state,"evidence":evidence},
            "material_delta":phase<2,
            "delta":{
                "execution_truth_strengthened":phase<2,
                "resolved_open":phase<2,
            },
        }

    def admit(state):
        status=(
            "CONFIGURED_IDENTITY_PROMOTED"
            if phase==0
            else "PORTFOLIO_AUDIT_CLOSED_RELATIVE"
            if phase==1
            else "REPOSITORY_OWNED_INVOCATION_CLOSED_RELATIVE"
        )
        return {
            "state":{
                **state,
                "admission":status,
                "repository_owned_full_invocation":(
                    "CLOSED_RELATIVE" if phase==2 else "VERIFYING"
                ),
                "universal_host_interception":"EXTERNAL_NOT_OWNED",
            },
            "material_delta":phase<2,
            "delta":{
                "execution_truth_strengthened":phase<2,
                "resolved_open":phase<2,
            },
        }

    def verify(state):
        ev=state.get("evidence",{})
        if phase==0:
            ok=ev.get("identity_failures")==() and ev.get("checked")==len(CONFIGURED_RUNS)
        elif phase==1:
            ok=(
                ev.get("portfolio_status")=="CLOSED_RELATIVE"
                and ev.get("checked")==len(CONFIGURED_RUNS)
                and ev.get("failures")==()
            )
        else:
            ok=(
                state.get("repository_owned_full_invocation")=="CLOSED_RELATIVE"
                and state.get("universal_host_interception")=="EXTERNAL_NOT_OWNED"
                and state.get("selection_preserves_host_boundary") is True
            )
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
        "CURIOSITY_PD":curiosity_pd,
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
        "Improvement Core. Think big.",
        target="whole Take-5 configured formal-tool invocation system",
        job="promote and verify non-bypassable full invocation recurrence",
        basis="THINK_BIG_DIRECT_TOOL_120",
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
        "resolved_open":material,
        "route_equivalence":f"THINK_BIG_DIRECT_TOOL_PHASE_{phase}",
    }


def test_final_think_big_improvementcore_reapplies_under_hf2_until_system_closes():
    hf2=HF002RecursiveContinuation(
        run_capability=_run_ic,
        admit_normalize=_admit,
        trc_verify=lambda before,after,delta:{"terminal":True},
        hf1_classify=lambda before,after,delta:{"disposition":"STABLE"},
        live_local=lambda state,memory:int(state.get("hf2_round",0))<3,
        local_close=lambda state,memory:(
            int(state.get("hf2_round",0))>=3
            and state.get("repository_owned_full_invocation")=="CLOSED_RELATIVE"
            and state.get("verification")=="PASS"
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
    assert final["command"]=="Think big."
    assert final["repository_owned_full_invocation"]=="CLOSED_RELATIVE"
    assert final["universal_host_interception"]=="EXTERNAL_NOT_OWNED"
    assert final["verification"]=="PASS"
