from jane_continuity import recover_continuity
from jane_icc128_bridge import bind_jane_continuity

def test_ready_jane_packet_hands_control_state_to_icc128():
    p=recover_continuity(
        {
            "target":"current conversation",
            "job":"solve live failures",
            "basis":"Take-5 current",
            "canonical_version":"2026-09-27",
        },
        protected_behaviors=("exactness","format"),
        open_coordinates=("two-equation identity",),
        evidence_refs=("chat","github"),
    )
    e=bind_jane_continuity(p,rejection_memory={"rejected":["long-wrong-output"]})
    assert e.status=="READY"
    assert e.state["terminal"]=="CONTINUE"
    assert e.state["admitted_continuation"] is True
    assert e.state["recurrence_or_prior_failure"] is True
    assert e.memory["jane_continuity"]["canonical_version"]=="2026-09-27"

def test_incomplete_jane_packet_fails_open():
    p=recover_continuity({"target":"x"})
    e=bind_jane_continuity(p)
    assert e.status=="OPEN"
    assert e.state["terminal"]=="OPEN"
    assert e.state["selection_blocked"] is True
