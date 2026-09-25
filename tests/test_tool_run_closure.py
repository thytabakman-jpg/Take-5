import sys
sys.path.insert(0,"runtime")

from tool_run_closure import (
    Consequence,
    ConsumerState,
    Disposition,
    StageResult,
    run_tool_run_closure,
)

def q(name, *, version="v1"):
    return Consequence(
        referent=name,
        effect_class="UPDATE",
        target_state="CURRENT",
        authority_scope="LOCAL",
        source_version=version,
        protected_class="RESULT",
    )

def test_trc_recursively_closes_induced_consequences():
    def harvest(result,pre,post):
        return (q("A"),)

    def disposition(c,state):
        return Disposition.REALIZE

    def realize(c,state):
        nxt={**state,"realized":tuple(state.get("realized",()))+(c.referent,)}
        induced=(q("B"),) if c.referent=="A" else ()
        return StageResult(nxt,status="COMPLETED_UNVERIFIED",induced=induced,evidence=(f"realize:{c.referent}",))

    def verify(c,state):
        return StageResult(state,status="VERIFIED",evidence=(f"verify:{c.referent}",))

    def consume(c,state):
        nxt={**state,"consumed":tuple(state.get("consumed",()))+(c.referent,)}
        return StageResult(nxt,status=ConsumerState.CONSUMED.value,evidence=(f"consume:{c.referent}",))

    out=run_tool_run_closure(
        tool_result={"x":1},
        pre_state={},
        post_state={},
        harvest_fn=harvest,
        disposition_fn=disposition,
        realize_fn=realize,
        verify_fn=verify,
        consume_fn=consume,
        harvest_basis="test",
    )
    assert out.certificate.status=="CLOSED"
    assert out.certificate.accounted_count==2
    assert out.certificate.settled_count==2
    assert out.state["consumed"]==("A","B")

def test_trc_exact_duplicate_is_reversibly_subsumed():
    same=q("A")
    out=run_tool_run_closure(
        tool_result=None,
        pre_state={},
        post_state={},
        harvest_fn=lambda r,p,s:(same,same),
        disposition_fn=lambda c,s:Disposition.CERTIFIED_NO_EFFECT,
        realize_fn=lambda c,s:s,
        verify_fn=lambda c,s:s,
        consume_fn=lambda c,s:s,
        harvest_basis="same-basis",
    )
    assert out.certificate.status=="CLOSED"
    assert out.certificate.accounted_count==1
    assert len(out.certificate.duplicate_subsumptions)==1
    witness=out.certificate.duplicate_subsumptions[0]
    assert witness.witness=="EXACT_CID_EQUIVALENCE"
    assert witness.invalidation_trigger=="ANY_CID_COORDINATE_CHANGES"

def test_trc_pending_authority_is_accounted_but_open():
    out=run_tool_run_closure(
        tool_result=None,
        pre_state={},
        post_state={},
        harvest_fn=lambda r,p,s:(q("A"),),
        disposition_fn=lambda c,s:Disposition.PENDING_AUTHORIZATION,
        realize_fn=lambda c,s:s,
        verify_fn=lambda c,s:s,
        consume_fn=lambda c,s:s,
    )
    assert out.certificate.status=="OPEN"
    assert out.certificate.accounted_count==1
    assert out.certificate.settled_count==0
    assert out.certificate.pending_coordinates
    assert out.certificate.records[0].resume_condition=="AUTHORITY_GRANTED"

def test_trc_consumer_unknown_blocks_false_close():
    out=run_tool_run_closure(
        tool_result=None,
        pre_state={},
        post_state={},
        harvest_fn=lambda r,p,s:(q("A"),),
        disposition_fn=lambda c,s:Disposition.REALIZE,
        realize_fn=lambda c,s:StageResult(s,status="COMPLETED_UNVERIFIED"),
        verify_fn=lambda c,s:StageResult(s,status="VERIFIED"),
        consume_fn=lambda c,s:StageResult(s,status="UNKNOWN"),
    )
    assert out.certificate.status=="OPEN"
    assert out.certificate.settled_count==0
