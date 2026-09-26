from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.archive import Vault, append_event
from runtime.compiler import compile_state
from runtime.invocation import make_invocation_capsule, verify_invocation_capsule

def fake_cid(ch: str) -> str:
    return "sha256:" + ch * 64

def event(kind, subject, payload, eid, supersedes=()):
    return {
        "event_id": fake_cid(eid),
        "kind": kind,
        "subject": subject,
        "payload_cid": payload,
        "parents": [],
        "basis_cid": fake_cid("b"),
        "authority": "TEST",
        "effects": [],
        "supersedes": list(supersedes),
    }

def test_vault_content_addressing(tmp_path):
    v = Vault(tmp_path / "vault")
    a = v.put_bytes(b"same")
    b = v.put_bytes(b"same")
    assert a.cid == b.cid
    assert v.get_bytes(a.cid) == b"same"

def test_current_is_compiled_not_recency():
    old = fake_cid("1")
    new = fake_cid("2")
    s = compile_state([
        event("ADMIT", "TOOL:X", old, "3"),
        event("SUPERSEDE", "TOOL:X", new, "4", supersedes=[old]),
    ])
    assert s["subjects"]["TOOL:X"]["status"] == "CURRENT"
    assert s["subjects"]["TOOL:X"]["current_payload_cid"] == new

def test_incomparable_maxima_are_conflict():
    a = fake_cid("1")
    b = fake_cid("2")
    s = compile_state([
        event("ADMIT", "TOOL:X", a, "3"),
        event("ADMIT", "TOOL:X", b, "4"),
    ])
    assert s["subjects"]["TOOL:X"]["status"] == "CONFLICT"
    assert s["subjects"]["TOOL:X"]["current_payload_cid"] is None

def test_invocation_is_exact_and_fail_closed():
    refs = {fake_cid(x) for x in "123456"}
    cap = make_invocation_capsule(
        kernel_cid=fake_cid("1"),
        state_cid=fake_cid("2"),
        tool_cid=fake_cid("3"),
        input_cids=[fake_cid("4")],
        basis_cid=fake_cid("5"),
        environment_cid=fake_cid("6"),
    )
    verify_invocation_capsule(cap, has_cid=refs.__contains__)
    cap["tool_cid"] = fake_cid("7")
    try:
        verify_invocation_capsule(cap, has_cid=refs.__contains__)
    except RuntimeError:
        pass
    else:
        raise AssertionError("tampered invocation did not fail closed")
