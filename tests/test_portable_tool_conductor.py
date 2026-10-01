from portable_tool_conductor import (
    compile_repertoire,
    compilation_witness,
    portability_closed,
    portability_open_set,
    run_tool_conductor,
)
from tool_run_registry import MATERIAL_TOOLS


def test_every_registered_tool_has_compilation_witness():
    witnesses = compile_repertoire()
    assert tuple(w.tool_id for w in witnesses) == tuple(MATERIAL_TOOLS)
    assert all(w.status for w in witnesses)
    assert all(w.evidence for w in witnesses)


def test_all_atomic_capabilities_have_direct_effective_programs():
    for i in range(1, 50):
        w = compilation_witness(f"C{i:02d}")
        assert w.entrypoint == "capability_runtime.execute_capability"
        assert w.self_contained is True


def test_tool_conductor_self_application_is_nonrecursive_witness():
    w = compilation_witness("ToolConductor")
    assert w.status == "SELF_WITNESS"
    assert w.self_contained is True


def test_learning_callback_dependencies_are_explicit():
    assert compilation_witness("L-BAYES").self_contained is True
    assert compilation_witness("L-RATE-DISTORTION").self_contained is True
    assert compilation_witness("L-D6").required_environment == ("sense", "d4", "ground")
    assert compilation_witness("L-D6").self_contained is False


def test_portability_claim_is_fail_closed():
    open_set = portability_open_set()
    assert open_set
    assert portability_closed() is False


def test_conductor_emits_exactly_one_disposition_per_registered_tool():
    out = run_tool_conductor({})
    assert out["tool_count"] == len(MATERIAL_TOOLS)
    assert tuple(r["tool_id"] for r in out["results"]) == tuple(MATERIAL_TOOLS)
    assert len({r["tool_id"] for r in out["results"]}) == len(MATERIAL_TOOLS)
    assert out["status"] == "OPEN"



def test_every_conductor_factor_exposes_current_full_invocation_plan():
    out=run_tool_conductor({})
    assert out["tool_count"]==len(MATERIAL_TOOLS)
    for row in out["results"]:
        plan=row["configured_plan"]
        assert plan["wrapper_required"] is True
        assert plan["geometry"]=="D36_C"
        assert plan["cell_count"]==36
        assert plan["question_count"]==22*36
        assert plan["cognitive_count"]==4*36
        assert plan["recurrence_required"] is True
        assert plan["recurrence_engine"]==(
            "SELF" if row["tool_id"]=="HF002" else "HF002"
        )
        assert plan["invocation_profile"]=="FULL_CONFIGURED_HF2_V1"


def test_conductor_factor_can_recur_under_hf2_without_duplicate_factor_dispositions():
    calls=[]

    def mt_adapter(packet):
        n=len(calls)+1
        calls.append(n)
        return {
            "status":"EXECUTED",
            "execution_truth":"SEMANTICALLY_APPLIED",
            "result":{"round":n},
            "material_delta":n<2,
            "hf2_live_local":n<2,
        }

    out=run_tool_conductor({},adapters={"MT":mt_adapter})
    mt=[row for row in out["results"] if row["tool_id"]=="MT"]
    assert len(mt)==1
    assert calls==[1,2]
    assert mt[0]["status"]=="EXECUTED"
    assert mt[0]["recurrence"]["engine"]=="HF002"
    assert mt[0]["recurrence"]["status"]=="RELATIVE_CLOSE"
    assert mt[0]["recurrence"]["rounds"]==2
    assert mt[0]["recurrence"]["call_count"]==2
    assert mt[0]["recurrence"]["trace"][-1]["disposition"]=="RELATIVE_CLOSE"
