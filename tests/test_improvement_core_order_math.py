from runtime.improvement_core_order_math import (
    ClosureState,
    ComparisonFrame,
    ExecutionLevel,
    NoGainRecord,
    StepReceipt,
    SystemState,
    TransportCertificate,
    classify_step,
    closure_disposition,
    cycle_no_gain,
    equivalent_state,
    finite_fixed_basis_execution_bound,
    frame_chain_strict,
    strict_improvement_in_frame,
    retry_licensed,
    strict_improvement,
    weak_improvement,
)


def s(
    sid,
    *,
    basis="b0",
    caps=(),
    models=("m1","m2","m3"),
    goals=(),
    contrib=(),
    execution=ExecutionLevel.NOT_EXECUTED,
    burden=1.0,
):
    return SystemState(
        sid,
        basis,
        frozenset(caps),
        frozenset(models),
        frozenset(goals),
        frozenset(contrib),
        execution,
        burden,
    )


def test_semantic_gain_is_not_vetoed_by_higher_burden():
    a=s("a",models=("m1","m2","m3"),burden=1.0)
    b=s("b",models=("m1","m2"),burden=9.0)
    assert weak_improvement(a,b)
    assert strict_improvement(a,b)


def test_lower_burden_is_gain_only_inside_semantic_equivalence():
    a=s("a",burden=5.0)
    b=s("b",burden=2.0)
    assert strict_improvement(a,b)
    assert not equivalent_state(a,b)


def test_equal_semantics_and_equal_burden_is_no_gain():
    a=s("a",burden=2.0)
    b=s("b",burden=2.0)
    assert equivalent_state(a,b)
    assert not strict_improvement(a,b)


def test_strict_improvement_is_transitive_on_same_basis():
    a=s("a",models=("m1","m2","m3"),execution=ExecutionLevel.SELECTED)
    b=s("b",models=("m1","m2"),execution=ExecutionLevel.EXECUTED)
    c=s("c",models=("m1",),execution=ExecutionLevel.VERIFIED,goals=("g1",))
    assert strict_improvement(a,b)
    assert strict_improvement(b,c)
    assert strict_improvement(a,c)


def test_protected_capability_loss_is_regression():
    a=s("a",caps=("full-wrapper","observer"))
    b=s("b",caps=("observer",),models=("m1",))
    assert not weak_improvement(a,b)


def test_cross_basis_comparison_fails_closed_without_transport():
    a=s("a",basis="old")
    b=s("b",basis="new")
    assert not weak_improvement(a,b)


def test_cross_basis_transport_enables_comparison():
    a=s("a",basis="old",models=("old:m1","old:m2"))
    b=s("b",basis="new",models=("new:m1",))
    cert=TransportCertificate(
        "old","new","common",
        {"old:m1":"m1","old:m2":"m2"},
        {"new:m1":"m1"},
        evidence=("mapping-audit",),
    )
    assert strict_improvement(a,b,certificate=cert)


def test_cross_basis_transport_requires_path_coherence():
    a=s("a",basis="old")
    b=s("b",basis="new")
    cert=TransportCertificate(
        "old","new","common",{}, {},
        path_coherent=False,
        evidence=("mapping-audit",),
    )
    assert not weak_improvement(a,b,certificate=cert)


def test_selected_is_not_executed_or_consumed():
    a=s("a",execution=ExecutionLevel.SELECTED)
    b=s("b",execution=ExecutionLevel.SELECTED)
    receipt=StepReceipt(
        "route",
        ExecutionLevel.SELECTED,
        boundary_verified=False,
        obligations_terminal=False,
        evidence=("selection-only",),
    )
    assert classify_step(a,b,receipt).status=="OPEN_EXECUTION"


def test_repository_change_without_boundary_verification_stays_open():
    a=s("a")
    b=s("b",models=("m1","m2"))
    receipt=StepReceipt(
        "repo-fix",
        ExecutionLevel.CONSUMED,
        boundary_verified=False,
        obligations_terminal=True,
        evidence=("repo-test",),
    )
    assert classify_step(a,b,receipt).status=="OPEN_BOUNDARY"


def test_strict_step_requires_execution_boundary_obligations_and_evidence():
    a=s("a",models=("m1","m2","m3"))
    b=s("b",models=("m1","m2"))
    receipt=StepReceipt(
        "r",
        ExecutionLevel.CONSUMED,
        boundary_verified=True,
        obligations_terminal=True,
        evidence=("holdout",),
    )
    assert classify_step(a,b,receipt).status=="STRICT_GAIN"


def test_equivalent_consumed_step_is_no_gain():
    a=s("a")
    b=s("b")
    receipt=StepReceipt(
        "r",
        ExecutionLevel.CONSUMED,
        boundary_verified=True,
        obligations_terminal=True,
        evidence=("real-run",),
    )
    assert classify_step(a,b,receipt).status=="NO_GAIN"


def test_no_gain_retry_is_dependency_sensitive():
    rec=NoGainRecord("r","b0","q1",frozenset({"evidence"}),("run",))
    assert not retry_licensed(rec,current_basis_id="b0",current_semantic_class="q1")
    assert retry_licensed(
        rec,
        current_basis_id="b0",
        current_semantic_class="q1",
        changed_coordinates=frozenset({"evidence"}),
    )


def test_semantic_cycle_without_gain_is_blocked():
    assert cycle_no_gain(("A","B","A"),(False,False))
    assert not cycle_no_gain(("A","B","A"),(True,False))


def test_closure_requires_zero_gap_current_coverage_and_empty_frontier():
    base=ClosureState(
        goal_gap_zero=True,
        live_frontier=frozenset(),
        coverage_current=True,
    )
    assert closure_disposition(base)=="RELATIVE_CLOSE"
    assert closure_disposition(
        ClosureState(True,frozenset({"a"}),coverage_current=True)
    )=="CONTINUE"
    assert closure_disposition(
        ClosureState(False,frozenset(),coverage_current=True)
    )=="OPEN"
    assert closure_disposition(
        ClosureState(True,frozenset(),coverage_current=False)
    )=="RETURN_REENTER"


def test_finite_fixed_basis_bound_is_state_route_product():
    assert finite_fixed_basis_execution_bound(7,11)==77


def test_episode_wide_comparison_frame_makes_three_basis_chain_transitive():
    a=s("a",basis="ba",models=("a:m1","a:m2","a:m3"),execution=ExecutionLevel.SELECTED)
    b=s("b",basis="bb",models=("b:m1","b:m2"),execution=ExecutionLevel.EXECUTED)
    c=s("c",basis="bc",models=("c:m1",),execution=ExecutionLevel.VERIFIED,goals=("c:g1",))
    frame=ComparisonFrame(
        "frame-1",
        "omega",
        {
            "ba":{"a:m1":"m1","a:m2":"m2","a:m3":"m3"},
            "bb":{"b:m1":"m1","b:m2":"m2"},
            "bc":{"c:m1":"m1","c:g1":"g1"},
        },
        evidence=("single-common-frame-audit",),
    )
    assert strict_improvement_in_frame(a,b,frame)
    assert strict_improvement_in_frame(b,c,frame)
    assert strict_improvement_in_frame(a,c,frame)
    assert frame_chain_strict((a,b,c),frame)


def test_comparison_frame_fails_closed_when_one_basis_has_no_transport():
    a=s("a",basis="ba")
    b=s("b",basis="missing")
    frame=ComparisonFrame(
        "frame-1",
        "omega",
        {"ba":{}},
        evidence=("frame-audit",),
    )
    assert not strict_improvement_in_frame(a,b,frame)
