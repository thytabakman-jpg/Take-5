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
    assert "configured-recurrence:HF002:RELATIVE_CLOSE:rounds=1" in out.transition_receipt.evidence["execution"]
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



def test_protected_transition_reapplies_execute_edge_under_hf2_when_local_frontier_is_live():
    spec=CONFIGURED_RUNS["RootCause"]
    calls=[]

    def execute(value,plan):
        n=int(value.get("round",0))+1
        calls.append(n)
        return (
            {"result":f"root-{n}"},
            f"execution:root:{n}",
            {
                "next_payload":{"round":n},
                "material_delta":n<2,
                "hf2_live_local":n<2,
            },
        )

    out=execute_protected_transition(
        spec,
        behavior_id="ROOT_CAUSE_ROOTNESS_SELECTOR",
        dispatch_fn=lambda plan:({"round":0},"dispatch:root"),
        execute_fn=execute,
        consume_fn=lambda value,plan:({"consumed":value},"consume:root"),
        update_fn=lambda value,plan:({"state":value},"update:root"),
        reentry_fn=lambda value,plan:({"reentered":value},"reentry:root"),
        emission_audit_fn=lambda value,plan:"emission:audited",
    )

    assert calls==[1,2]
    execution_evidence=out.transition_receipt.evidence["execution"]
    assert "configured-recurrence:HF002:RELATIVE_CLOSE:rounds=2" in execution_evidence
    assert "execution:root:1" in execution_evidence
    assert "execution:root:2" in execution_evidence


def test_hf002_protected_transition_uses_self_recurrence_not_nested_hf2():
    spec=CONFIGURED_RUNS["HF002"]
    calls=[]

    def execute(value,plan):
        calls.append(plan.recurrence_engine)
        return ("hf2-result","execution:hf2")

    out=execute_protected_transition(
        spec,
        behavior_id="HF002_LOCAL_RECURSIVE_CONTINUATION",
        dispatch_fn=lambda plan:("hf2-input","dispatch:hf2"),
        execute_fn=execute,
        consume_fn=lambda value,plan:(value,"consume:hf2"),
        update_fn=lambda value,plan:(value,"update:hf2"),
        reentry_fn=lambda value,plan:(value,"reentry:hf2"),
        emission_audit_fn=lambda value,plan:"emission:hf2",
    )

    assert calls==["SELF"]
    assert "configured-recurrence:SELF:SELF_CLOSE:rounds=1" in out.transition_receipt.evidence["execution"]
