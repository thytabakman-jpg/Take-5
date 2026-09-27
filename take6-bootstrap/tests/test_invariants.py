from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.archive import Vault, append_event, cid_json
from runtime.authority import make_authorizer, policy_cid
from runtime.checkpoint import make_checkpoint, verify_checkpoint
from runtime.compiler import compile_state, compile_to_file
from runtime.durability import ReplicaWitness, verify_durable
from runtime.invocation import make_invocation_capsule, verify_invocation_capsule
from runtime.propagation import affected_cone, require_consequence_dispositions
from runtime.promotion import verify_promotion

def fake_cid(ch: str) -> str:
    return "sha256:" + ch * 64

POLICY = {
    "rules": {
        "TEST": {
            "kinds": ["ADMIT", "PROMOTE", "SUPERSEDE", "REJECT", "OPEN", "BLOCK", "CONFLICT", "RELATE"],
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

def test_vault_content_addressing(tmp_path):
    v = Vault(tmp_path / "vault")
    a = v.put_bytes(b"same")
    b = v.put_bytes(b"same")
    assert a.cid == b.cid
    assert v.get_bytes(a.cid) == b"same"

def test_current_is_compiled_not_recency():
    old = fake_cid("1")
    new = fake_cid("2")
    first = event("ADMIT", "TOOL:X", old)
    second = event("SUPERSEDE", "TOOL:X", new, parents=[first["event_id"]], supersedes=[old])
    s = compile([second, first])
    assert s["subjects"]["TOOL:X"]["status"] == "CURRENT"
    assert s["subjects"]["TOOL:X"]["current_payload_cid"] == new
    assert s["compiler_cid"] == COMPILER_CID
    assert s["authority_policy_cid"] == POLICY_CID

def test_incomparable_maxima_are_conflict():
    a = fake_cid("1")
    b = fake_cid("2")
    s = compile([
        event("ADMIT", "TOOL:X", a),
        event("ADMIT", "TOOL:X", b),
    ])
    assert s["subjects"]["TOOL:X"]["status"] == "CONFLICT"
    assert s["subjects"]["TOOL:X"]["current_payload_cid"] is None

def test_unauthorized_event_fails_closed():
    e = event("ADMIT", "TOOL:X", fake_cid("1"), authority="ROGUE")
    try:
        compile([e])
    except RuntimeError as exc:
        assert "UNAUTHORIZED_EVENT" in str(exc)
    else:
        raise AssertionError("unauthorized semantic event compiled")

def test_damaged_event_identity_fails_closed():
    e = event("ADMIT", "TOOL:X", fake_cid("1"))
    e["payload_cid"] = fake_cid("2")
    try:
        compile([e])
    except RuntimeError as exc:
        assert "EVENT_IDENTITY_FAILURE" in str(exc)
    else:
        raise AssertionError("tampered event compiled")

def test_missing_parent_fails_closed():
    e = event("ADMIT", "TOOL:X", fake_cid("1"), parents=[fake_cid("f")])
    try:
        compile([e])
    except RuntimeError as exc:
        assert "MISSING_PARENT_EVENT" in str(exc)
    else:
        raise AssertionError("event with missing parent compiled")

def test_fresh_reconstruction_same_state_cid(tmp_path):
    ledger = tmp_path / "ledger"
    first = append_event(ledger, {
        "kind": "ADMIT",
        "subject": "TOOL:X",
        "payload_cid": fake_cid("1"),
        "parents": [],
        "basis_cid": fake_cid("b"),
        "authority": "TEST",
        "effects": [],
        "supersedes": [],
    })
    append_event(ledger, {
        "kind": "SUPERSEDE",
        "subject": "TOOL:X",
        "payload_cid": fake_cid("2"),
        "parents": [first["event_id"]],
        "basis_cid": fake_cid("b"),
        "authority": "TEST",
        "effects": [],
        "supersedes": [fake_cid("1")],
    })
    generated = tmp_path / "compiled" / "current.json"
    kwargs = dict(
        compiler_cid=COMPILER_CID,
        authority_policy_cid=POLICY_CID,
        authorize=AUTHORIZE,
    )
    s1 = compile_to_file(ledger, generated, **kwargs)
    shutil.rmtree(tmp_path / "compiled")
    s2 = compile_to_file(ledger, generated, **kwargs)
    assert s1["state_cid"] == s2["state_cid"]
    assert json.loads(generated.read_text())["state_cid"] == s1["state_cid"]

def test_checkpoint_detects_historical_loss():
    objects = {fake_cid("1"), fake_cid("2")}
    events = {fake_cid("3"), fake_cid("4")}
    cp = make_checkpoint(object_cids=objects, event_ids=events, prior_checkpoint_cid=None)
    verify_checkpoint(cp, has_object=objects.__contains__, has_event=events.__contains__)
    objects.remove(fake_cid("2"))
    try:
        verify_checkpoint(cp, has_object=objects.__contains__, has_event=events.__contains__)
    except RuntimeError as exc:
        assert "CHECKPOINT_OBJECT_LOSS" in str(exc)
    else:
        raise AssertionError("checkpoint failed to detect deleted object")

def test_affected_cone_requires_every_disposition():
    reverse = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    cone = affected_cone(["A"], reverse)
    assert cone == ("A", "B", "C", "D")
    require_consequence_dispositions(cone, {
        "A": "COVERED", "B": "NO_EFFECT", "C": "OPEN", "D": "SUPERSEDED"
    })
    try:
        require_consequence_dispositions(cone, {"A": "COVERED"})
    except RuntimeError as exc:
        assert "UNDISPOSITIONED" in str(exc)
    else:
        raise AssertionError("partial consequence accounting passed")

def test_promotion_blocks_silent_behavior_loss():
    try:
        verify_promotion(
            predecessor_protected=["A", "B"],
            successor_preserved=["A"],
            consequence_closed=True,
            predecessor_specification_status="PASS",
            successor_specification_status="PASS",
            source_frontier_verified=True,
            source_frontier_cid=fake_cid("f"),
        )
    except RuntimeError as exc:
        assert "SILENT_BEHAVIOR_LOSS" in str(exc)
    else:
        raise AssertionError("silent behavior loss promoted")

def test_promotion_can_preserve_typed_open_without_false_pass():
    receipt = verify_promotion(
        predecessor_protected=["A", "B"],
        successor_preserved=["A"],
        typed_open=["B"],
        validations=["HOLDOUT"],
        required_validations=["HOLDOUT"],
        consequence_closed=True,
        predecessor_specification_status="PASS",
        successor_specification_status="PASS",
        source_frontier_verified=True,
        source_frontier_cid=fake_cid("f"),
    )
    assert receipt.status == "OPEN"
    assert receipt.typed_open_behaviors == ("B",)

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


def test_durability_requires_independent_failure_domains():
    target = fake_cid("9")
    same_account = [
        ReplicaWitness("repo-a", "github-account-A", frozenset({target})),
        ReplicaWitness("repo-b", "github-account-A", frozenset({target})),
    ]
    try:
        verify_durable(target, same_account)
    except RuntimeError as exc:
        assert "DURABILITY_REPLICATION_OPEN" in str(exc)
    else:
        raise AssertionError("same failure domain counted as independent durability")

def test_durability_passes_two_independent_domains():
    target = fake_cid("9")
    replicas = [
        ReplicaWitness("primary", "github-account-A", frozenset({target})),
        ReplicaWitness("cold", "independent-cold-store-B", frozenset({target})),
    ]
    receipt = verify_durable(target, replicas)
    assert receipt.status == "PASS"
    assert len(receipt.independent_trust_domains) == 2


def test_promotion_blocks_unrecovered_object_specification():
    try:
        verify_promotion(
            predecessor_protected=["A"],
            successor_preserved=["A"],
            consequence_closed=True,
            predecessor_specification_status="OPEN",
            successor_specification_status="PASS",
            source_frontier_verified=True,
            source_frontier_cid=fake_cid("f"),
        )
    except RuntimeError as exc:
        assert "PROMOTION_SPECIFICATION_OPEN" in str(exc)
    else:
        raise AssertionError("unrecovered predecessor specification promoted")
