from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.archive import cid_json
from runtime.authority import make_authorizer, policy_cid
from runtime.compiler import compile_state
from runtime.views import (
    project_subject_view,
    render_human_view,
    verify_subject_view,
)


def fake_cid(ch: str) -> str:
    return "sha256:" + ch * 64


POLICY = {
    "rules": {
        "TEST": {
            "kinds": [
                "ADMIT",
                "PROMOTE",
                "SUPERSEDE",
                "REJECT",
                "OPEN",
                "BLOCK",
                "CONFLICT",
                "RELATE",
            ],
            "subject_prefixes": ["TOOL:", "PROJECT:"],
        }
    }
}
AUTHORIZE = make_authorizer(POLICY)
POLICY_CID = policy_cid(POLICY)
COMPILER_CID = fake_cid("c")


def event(kind, subject, payload, *, parents=(), supersedes=(), authority="TEST"):
    body = {
        "kind": kind,
        "subject": subject,
        "payload_cid": payload,
        "parents": list(parents),
        "basis_cid": fake_cid("b"),
        "authority": authority,
        "effects": [],
        "supersedes": list(supersedes),
    }
    return {"event_id": cid_json(body), **body}


def compile(events):
    return compile_state(
        events,
        compiler_cid=COMPILER_CID,
        authority_policy_cid=POLICY_CID,
        authorize=AUTHORIZE,
    )


def current_state():
    root = event("ADMIT", "TOOL:X", fake_cid("1"))
    dep = event("ADMIT", "TOOL:Y", fake_cid("2"))
    return compile([root, dep])


def test_generated_view_binds_exact_compiled_state_and_payload():
    state = current_state()
    view = project_subject_view(
        state,
        subject="TOOL:X",
        claim_scope="CURRENT",
        authoritative_formal=True,
        dependency_closure="PASS",
        composition_typecheck="PASS",
    )
    assert view["authority"] == "PROJECTION_ONLY"
    assert view["state_cid"] == state["state_cid"]
    assert view["current_payload_cid"] == fake_cid("1")
    verify_subject_view(view, state)


def test_rebuilt_same_compiled_state_revalidates_same_view():
    state1 = current_state()
    state2 = current_state()
    assert state1["state_cid"] == state2["state_cid"]
    view = project_subject_view(
        state1,
        subject="TOOL:X",
        claim_scope="CURRENT",
        authoritative_formal=True,
        dependency_closure="PASS",
        composition_typecheck="PASS",
    )
    verify_subject_view(view, state2)


def test_view_becomes_stale_after_subject_supersession():
    first = event("ADMIT", "TOOL:X", fake_cid("1"))
    state1 = compile([first])
    view = project_subject_view(
        state1,
        subject="TOOL:X",
        claim_scope="CURRENT",
        authoritative_formal=True,
        dependency_closure="PASS",
        composition_typecheck="PASS",
    )

    second = event(
        "SUPERSEDE",
        "TOOL:X",
        fake_cid("2"),
        parents=[first["event_id"]],
        supersedes=[fake_cid("1")],
    )
    state2 = compile([first, second])

    try:
        verify_subject_view(view, state2)
    except RuntimeError as exc:
        assert "VIEW_STATE_STALE" in str(exc)
    else:
        raise AssertionError("stale generated view remained valid")


def test_hand_editing_generated_view_breaks_receipt():
    state = current_state()
    view = project_subject_view(
        state,
        subject="TOOL:X",
        claim_scope="CURRENT",
        authoritative_formal=True,
        dependency_closure="PASS",
        composition_typecheck="PASS",
    )
    view["subject_status"] = "HISTORICAL"
    try:
        verify_subject_view(view, state)
    except RuntimeError as exc:
        assert "VIEW_HASH_MISMATCH" in str(exc)
    else:
        raise AssertionError("tampered view remained valid")


def test_authoritative_formal_view_requires_type_and_dependency_closure():
    state = current_state()
    try:
        project_subject_view(
            state,
            subject="TOOL:X",
            claim_scope="CURRENT",
            authoritative_formal=True,
            dependency_closure="OPEN",
            composition_typecheck="PASS",
        )
    except RuntimeError as exc:
        assert "DEPENDENCY_CLOSURE_OPEN" in str(exc)
    else:
        raise AssertionError("open dependency closure admitted")

    try:
        project_subject_view(
            state,
            subject="TOOL:X",
            claim_scope="CURRENT",
            authoritative_formal=True,
            dependency_closure="PASS",
            composition_typecheck="OPEN",
        )
    except RuntimeError as exc:
        assert "COMPOSITION_TYPECHECK_OPEN" in str(exc)
    else:
        raise AssertionError("open composition type check admitted")


def test_current_dependency_must_match_compiled_current_payload():
    state = current_state()
    dep = {
        "subject": "TOOL:Y",
        "payload_cid": fake_cid("9"),
        "disposition": "CURRENT",
    }
    try:
        project_subject_view(
            state,
            subject="TOOL:X",
            claim_scope="CURRENT",
            authoritative_formal=True,
            dependencies=[dep],
            dependency_closure="PASS",
            composition_typecheck="PASS",
        )
    except RuntimeError as exc:
        assert "CURRENT_DEPENDENCY_PAYLOAD_MISMATCH" in str(exc)
    else:
        raise AssertionError("wrong current dependency payload admitted")


def test_frozen_dependency_requires_current_authority_policy_admission():
    state = current_state()
    bad = {
        "subject": "TOOL:LEGACY",
        "payload_cid": fake_cid("8"),
        "disposition": "ADMITTED_FROZEN",
        "admitted_by_authority_policy_cid": fake_cid("9"),
    }
    try:
        project_subject_view(
            state,
            subject="TOOL:X",
            claim_scope="CURRENT",
            authoritative_formal=True,
            dependencies=[bad],
            dependency_closure="PASS",
            composition_typecheck="PASS",
        )
    except RuntimeError as exc:
        assert "FROZEN_DEPENDENCY_NOT_ADMITTED" in str(exc)
    else:
        raise AssertionError("unadmitted frozen dependency passed")

    admitted = dict(bad)
    admitted["admitted_by_authority_policy_cid"] = POLICY_CID
    view = project_subject_view(
        state,
        subject="TOOL:X",
        claim_scope="CURRENT",
        authoritative_formal=True,
        dependencies=[admitted],
        dependency_closure="PASS",
        composition_typecheck="PASS",
    )
    verify_subject_view(view, state)


def test_noncurrent_subject_cannot_make_authoritative_current_claim():
    a = event("ADMIT", "TOOL:X", fake_cid("1"))
    b = event("ADMIT", "TOOL:X", fake_cid("2"))
    state = compile([a, b])
    assert state["subjects"]["TOOL:X"]["status"] == "CONFLICT"

    try:
        project_subject_view(
            state,
            subject="TOOL:X",
            claim_scope="CURRENT",
            authoritative_formal=True,
            dependency_closure="PASS",
            composition_typecheck="PASS",
        )
    except RuntimeError as exc:
        assert "AUTHORITATIVE_ROOT_NOT_CURRENT" in str(exc)
    else:
        raise AssertionError("conflicted root emitted as current")


def test_human_render_is_explicitly_projection_only_and_receipt_bound():
    state = current_state()
    view = project_subject_view(
        state,
        subject="TOOL:X",
        claim_scope="CURRENT",
        authoritative_formal=True,
        dependency_closure="PASS",
        composition_typecheck="PASS",
    )
    rendered = render_human_view(view)
    assert "GENERATED_PROJECTION_ONLY" in rendered
    assert state["state_cid"] in rendered
    assert view["view_cid"] in rendered
