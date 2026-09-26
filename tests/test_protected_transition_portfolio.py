import pytest

from global_tool_execution import (
    ToolExecutionBlocked,
    execute_protected_transition,
)
from protected_transition_portfolio import audit_protected_transition_portfolio
from tool_run_registry import CONFIGURED_RUNS


def test_every_configured_tool_inherits_protected_transition_integrity():
    out=audit_protected_transition_portfolio()
    assert out.status=="PASS"
    assert out.failures==()
    assert out.checked==len(CONFIGURED_RUNS)


def test_end_to_end_configured_execution_returns_verified_pti_receipt():
    spec=CONFIGURED_RUNS["RootCause"]

    out=execute_protected_transition(
        spec,
        behavior_id="ROOT_CAUSE_ROOTNESS_SELECTOR",
        dispatch_fn=lambda plan:({"dispatched":True},"dispatch:root"),
        execute_fn=lambda value,plan:({"result":"root"},"execution:root"),
        consume_fn=lambda value,plan:({"consumed":value},"consume:root"),
        update_fn=lambda value,plan:({"state":value},"update:root"),
        reentry_fn=lambda value,plan:({"reentered":value},"reentry:root"),
        emission_audit_fn=lambda value,plan:"emission:audited",
    )

    assert out.transition_receipt.object_id=="RootCause"
    assert all(
        str(v.value if hasattr(v,"value") else v)=="VERIFIED"
        for v in out.transition_receipt.coordinates.values()
    )


def test_end_to_end_configured_execution_fails_if_any_edge_has_no_witness():
    spec=CONFIGURED_RUNS["RootCause"]

    with pytest.raises(ToolExecutionBlocked,match="PTI_REENTRY_WITNESS_MISSING"):
        execute_protected_transition(
            spec,
            behavior_id="ROOT_CAUSE_ROOTNESS_SELECTOR",
            dispatch_fn=lambda plan:("x","dispatch"),
            execute_fn=lambda value,plan:("x","execution"),
            consume_fn=lambda value,plan:("x","consume"),
            update_fn=lambda value,plan:("x","update"),
            reentry_fn=lambda value,plan:("x",""),
            emission_audit_fn=lambda value,plan:"emission",
        )
