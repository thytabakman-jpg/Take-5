from endogenous_work import WorkItem,generate_obligations,select_work,closure_status,WorkStatus
from research_system import ResearchState,closure_certificate
from reflexive_currentness import current_basis,ArchitectureBasis,basis_delta
from state_commit import CommitRequest,StateRole,authorize_commit

def _research_receipt(effect="ADMIT_CLAIM"):
    return authorize_commit(
        CommitRequest(
            role=StateRole.RESEARCH_CONTROL,
            effect=effect,
            target="research",
            job="research-control",
            baseline="test",
            authority_before=frozenset({"admit"}),
            authority_after=frozenset({"admit"}),
            evidence=("evidence",),
            provenance=("test",),
            verification_receipt="verified",
        ),
        require_verification=True,
        require_evidence=True,
    )

def test_job_conditioned_and_zero_request_are_distinct_entry_modes():
    state={"obligations":[WorkItem("w1","repair")]}
    assert generate_obligations(state,job="j")[0].work_id=="w1"
    assert generate_obligations({},discover=lambda s:[WorkItem("w2","discover")])[0].work_id=="w2"

def test_selection_preserves_incomparable_plurality():
    xs=[WorkItem("a","A"),WorkItem("b","B")]
    s=select_work(xs)
    assert len(s.selected)==2 and len(s.incomparable)==2

def test_bounded_stop_is_not_closure_when_fresh_work_remains():
    xs=[WorkItem("a","A"),WorkItem("b","B")]
    assert closure_status(xs,{"a"})==WorkStatus.ACTIVE

def test_open_after_work_exhaustion_is_paused_open_not_closed():
    xs=[WorkItem("a","A")]
    assert closure_status(xs,{"a"},open_coordinates=("q",))==WorkStatus.PAUSED_OPEN

def test_history_based_closure_requires_admitted_claim_evidence():
    s=ResearchState()
    try:
        s.record_claim("c","ADMITTED",evidence=())
        assert False
    except PermissionError:
        pass
    s=ResearchState(); s.record_claim("c","ADMITTED",evidence=("receipt",),commit_receipt=_research_receipt())
    cert=closure_certificate(s,[])
    assert cert["closed"]

def test_reflexive_currentness_blocks_component_audit_on_architecture_delta():
    latest=current_basis()
    old=ArchitectureBasis("old","TOOL_COLLECTION","IC_IS_WHOLE_SYSTEM","NO_OBLIGATIONS","STATE_ONLY")
    assert set(basis_delta(old,latest))=={"system_identity","controller_role","closure_law","state_model"}
