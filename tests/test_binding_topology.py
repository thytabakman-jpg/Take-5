from binding_topology import NodeKind,EdgeKind,BindingEdge,BindingTopology,primitive_coordinate_admissible

def test_static_tool_on_item_differs_from_feedback_coupled_binding():
    static=BindingTopology((
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.READS),
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.WRITES),
        BindingEdge(NodeKind.ITEM,NodeKind.RESULT,EdgeKind.UPDATES),
    ))
    coupled=BindingTopology((
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.READS),
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.WRITES),
        BindingEdge(NodeKind.ITEM,NodeKind.RESULT,EdgeKind.UPDATES),
        BindingEdge(NodeKind.RESULT,NodeKind.STATE,EdgeKind.UPDATES),
        BindingEdge(NodeKind.STATE,NodeKind.VIEW,EdgeKind.UPDATES),
        BindingEdge(NodeKind.VIEW,NodeKind.CANDIDATE_UNIVERSE,EdgeKind.UPDATES),
        BindingEdge(NodeKind.CANDIDATE_UNIVERSE,NodeKind.HOST,EdgeKind.CONSTRAINS),
        BindingEdge(NodeKind.HOST,NodeKind.TOOL,EdgeKind.SELECTS),
    ))
    assert static.differs_from(coupled)
    assert not static.item_can_change_future_selection()
    assert coupled.item_can_change_future_selection()

def test_delegation_is_representable_without_calling_it_a_new_axis():
    delegated=BindingTopology((
        BindingEdge(NodeKind.HOST,NodeKind.TOOL,EdgeKind.DELEGATES),
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.READS),
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.WRITES),
    ))
    assert delegated.has_edge(NodeKind.HOST,NodeKind.TOOL,EdgeKind.DELEGATES)

def test_primitive_admission_requires_nonreconstructibility():
    assert not primitive_coordinate_admissible(
        distinct_role=True,
        result_sensitive=True,
        consumer_effect=True,
        nonreconstructible=False,
    )
    assert primitive_coordinate_admissible(
        distinct_role=True,
        result_sensitive=True,
        consumer_effect=True,
        nonreconstructible=True,
    )

def test_equal_edge_count_does_not_make_topologies_equivalent():
    a=BindingTopology((
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.READS),
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.WRITES),
    ))
    b=BindingTopology((
        BindingEdge(NodeKind.HOST,NodeKind.TOOL,EdgeKind.DELEGATES),
        BindingEdge(NodeKind.TOOL,NodeKind.ITEM,EdgeKind.READS),
    ))
    assert len(a.edges)==len(b.edges)
    assert a.differs_from(b)
