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
