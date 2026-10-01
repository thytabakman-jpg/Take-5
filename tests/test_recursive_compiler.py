import sys
sys.path.insert(0,"runtime")

from recursive_compiler import (
    CompilerNode,
    affected_cone,
    evaluate_global_closure,
    hf2_fixed_point_witness,
    validate_execution_profile,
)


def _trace(material_first=True):
    out=[]
    if material_first:
        out.append({
            "disposition":"REAPPLY_C",
            "delta":{"material_result_delta":True},
        })
    out.append({
        "disposition":"RELATIVE_CLOSE",
        "delta":{"material_result_delta":False},
    })
    return out


def _nodes():
    return (
        CompilerNode(
            "M","manuscript",None,
            gates={"goal":True,"architect":True},
            protected_constraints=("principal_delta_first",),
            delta_ids=("d-root",),
        ),
        CompilerNode(
            "S1","section","M",
            gates={"goal":True,"architect":True},
            protected_constraints=("principal_delta_first",),
            delta_ids=("d-s1",),
        ),
        CompilerNode(
            "P1","paragraph","S1",
            gates={"goal":True,"architect":True,"prose":True},
            protected_constraints=("principal_delta_first",),
            delta_ids=("d-p1",),
        ),
    )


def _base_kwargs():
    nodes=_nodes()
    return dict(
        nodes=nodes,
        edge_receipts={("M","S1"):True,("S1","P1"):True},
        constraint_receipts={
            ("M","principal_delta_first"):True,
            ("S1","principal_delta_first"):True,
            ("P1","principal_delta_first"):True,
        },
        admitted_delta_hashes={"d-root":"a","d-s1":"b","d-p1":"c"},
        realized_delta_hashes={"d-root":"a","d-s1":"b","d-p1":"c"},
        hf2_trace=_trace(),
    )


def test_global_close_requires_every_level_and_clean_hf2_successor_pass():
    out=evaluate_global_closure(**_base_kwargs())
    assert out.status=="GLOBAL_CLOSED"
    assert out.checked_nodes==3
    assert out.checked_edges==2
    assert out.checked_deltas==3


def test_missing_delta_blocks_global_close():
    kw=_base_kwargs()
    kw["realized_delta_hashes"]={"d-root":"a","d-s1":"b"}
    out=evaluate_global_closure(**kw)
    assert out.status=="OPEN"
    assert "DELTA_MISSING:d-p1" in out.reasons


def test_delta_semantic_drift_blocks_global_close():
    kw=_base_kwargs()
    kw["realized_delta_hashes"]={**kw["realized_delta_hashes"],"d-p1":"changed"}
    out=evaluate_global_closure(**kw)
    assert "DELTA_SEMANTIC_DRIFT:d-p1" in out.reasons


def test_constraint_order_failure_blocks_global_close():
    kw=_base_kwargs()
    kw["constraint_receipts"]={**kw["constraint_receipts"],("P1","principal_delta_first"):False}
    out=evaluate_global_closure(**kw)
    assert "PROTECTED_CONSTRAINT_OPEN:P1:principal_delta_first" in out.reasons


def test_local_node_pass_cannot_hide_unreconciled_parent_child_edge():
    kw=_base_kwargs()
    kw["edge_receipts"]={("M","S1"):True,("S1","P1"):False}
    out=evaluate_global_closure(**kw)
    assert "UNRECONCILED_EDGE:S1->P1" in out.reasons


def test_stale_ancestor_blocks_close_after_descendant_mutation():
    nodes=list(_nodes())
    nodes[0]=CompilerNode(
        "M","manuscript",None,
        gates={"goal":True,"architect":True},
        protected_constraints=("principal_delta_first",),
        delta_ids=("d-root",),
        stale=True,
    )
    kw=_base_kwargs()
    kw["nodes"]=tuple(nodes)
    out=evaluate_global_closure(**kw)
    assert "STALE_NODE:M" in out.reasons


def test_affected_cone_invalidates_ancestors_and_descendants():
    assert affected_cone(_nodes(),{"S1"})==frozenset({"M","S1","P1"})


def test_hf2_material_last_pass_cannot_self_certify_fixed_point():
    assert not hf2_fixed_point_witness([
        {"disposition":"RELATIVE_CLOSE","delta":{"material_result_delta":True}}
    ])


def test_hf2_clean_last_pass_is_required_even_after_reentry():
    assert hf2_fixed_point_witness(_trace())


def test_recursive_compiler_requires_full_36_observer_focused_observer_profile():
    validate_execution_profile(
        cell_count=36,
        mode_trace=("OBSERVER","FOCUSED","OBSERVER"),
    )


def test_recursive_compiler_rejects_profile_downgrade():
    import pytest
    with pytest.raises(RuntimeError,match="RECURSIVE_COMPILER_36D_DOWNGRADE"):
        validate_execution_profile(
            cell_count=12,
            mode_trace=("OBSERVER","FOCUSED","OBSERVER"),
        )


def test_recursive_compiler_rejects_missing_observer_return():
    import pytest
    with pytest.raises(RuntimeError,match="RECURSIVE_COMPILER_MODE_SEQUENCE_INVALID"):
        validate_execution_profile(
            cell_count=36,
            mode_trace=("OBSERVER","FOCUSED"),
        )
