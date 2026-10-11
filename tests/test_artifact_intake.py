from artifact_intake import (
    ArtifactRecord,
    intake,
    to_work_items,
    candidate_admission,
    generator_basis_changed,
)
from emergent_admission import Admission


def test_every_artifact_gets_full_traversal_receipt():
    artifacts = [
        ArtifactRecord("a", "alpha"),
        ArtifactRecord("b", "beta"),
    ]
    r = intake(artifacts, {})
    assert r.traversal_complete
    assert {x.artifact_id for x in r.traversal} == {"a", "b"}
    assert {x.bytes_covered for x in r.traversal} == {4, 5}


def test_every_generator_is_accounted_for_per_artifact():
    artifacts = [ArtifactRecord("a", "x")]

    def ok(a):
        return [{
            "candidate_id": "c1",
            "candidate_type": "SEMANTIC_PRIMITIVE",
            "source_span": "x",
            "load_bearing": True,
        }]

    def bad(a):
        raise RuntimeError("boom")

    r = intake(artifacts, {"bad": bad, "ok": ok})
    assert {(x.generator_id, x.status) for x in r.generator_receipts} == {
        ("bad", "ERROR"),
        ("ok", "COMPLETE"),
    }
    assert r.unresolved_extraction == ("a:bad:RuntimeError",)


def test_material_candidate_enters_existing_work_lifecycle():
    artifact = ArtifactRecord("a", "x", provenance=("p",))

    def g(a):
        return [{
            "candidate_id": "c1",
            "candidate_type": "MECHANISM_OR_CAPABILITY",
            "source_span": "line:1",
            "load_bearing": True,
        }]

    r = intake([artifact], {"g": g})
    work = to_work_items(r)
    assert len(work) == 1
    assert work[0].target == "c1"
    assert "a" in work[0].provenance
    assert work[0].obligation.startswith("OPEN:")


def test_non_load_bearing_and_known_equivalent_do_not_multiply_work():
    artifact = ArtifactRecord("a", "x")

    def g(a):
        return [
            {
                "candidate_id": "filler",
                "candidate_type": "SEMANTIC_PRIMITIVE",
                "source_span": "x",
                "load_bearing": False,
            },
            {
                "candidate_id": "alias",
                "candidate_type": "SEMANTIC_PRIMITIVE",
                "source_span": "x",
                "load_bearing": True,
                "known_equivalent": "existing",
            },
        ]

    r = intake([artifact], {"g": g})
    assert to_work_items(r) == ()


def test_unbound_executable_claim_remains_open_work():
    artifact = ArtifactRecord("a", "x")

    def g(a):
        return [{
            "candidate_id": "exec",
            "candidate_type": "RUNTIME_BINDING_OR_TRIGGER",
            "source_span": "x",
            "load_bearing": True,
            "executable_claim": True,
            "bound": False,
        }]

    r = intake([artifact], {"g": g})
    c = r.candidates[0]
    assert candidate_admission(c) == Admission.OPEN
    work = to_work_items(r)
    assert len(work) == 1
    assert work[0].obligation.startswith("OPEN:")


def test_generator_basis_change_requires_recheck():
    assert not generator_basis_changed(["g1", "g2"], ["g2", "g1"])
    assert generator_basis_changed(["g1"], ["g1", "g2"])


def test_material_candidate_accepts_only_after_semantic_package_exists():
    artifact = ArtifactRecord("a", "x")
    def g(a):
        return [{
            "candidate_id": "captured",
            "candidate_type": "SEMANTIC_PRIMITIVE",
            "source_span": "x",
            "load_bearing": True,
        }]
    r = intake([artifact], {"g": g})
    assert candidate_admission(r.candidates[0], package_verifier=lambda oid: oid=="captured") == Admission.ACCEPT


def test_missing_load_bearing_is_open_not_rejected():
    artifact = ArtifactRecord("a", "x")
    def g(a):
        return [{
            "candidate_id": "unknown-lb",
            "candidate_type": "SEMANTIC_PRIMITIVE",
            "source_span": "x",
        }]
    r = intake([artifact], {"g": g})
    assert r.candidates[0].load_bearing is None
    assert candidate_admission(r.candidates[0]) == Admission.OPEN

def test_candidate_cannot_self_assert_package_currentness():
    artifact = ArtifactRecord("a", "x")
    def g(a):
        return [{
            "candidate_id": "self-claimed",
            "candidate_type": "SEMANTIC_PRIMITIVE",
            "source_span": "x",
            "load_bearing": True,
        }]
    r = intake([artifact], {"g": g})
    assert candidate_admission(r.candidates[0]) == Admission.OPEN
    assert candidate_admission(r.candidates[0], package_verifier=lambda oid: True) == Admission.ACCEPT


# Discovery and object admission create visible work, never execution license.
import pytest
from endogenous_work import activate, select_work, WorkStatus, WorkItem
from delegation_officer import plan_delegation

@pytest.mark.parametrize("verified", [False, True])
def test_extracted_candidate_never_self_licenses(verified):
    artifact = ArtifactRecord("evidence", "x")
    def extract(a):
        return [{"candidate_id": "candidate", "candidate_type": "MECHANISM_OR_CAPABILITY",
                 "source_span": "line:1", "load_bearing": True}]
    result = intake([artifact], {"extract": extract})
    work, = to_work_items(result, package_verifier=(lambda _: verified))
    assert work.obligation.startswith("ACCEPT:" if verified else "OPEN:")
    assert work.status is WorkStatus.CANDIDATE
    assert not work.licensed
    assert select_work((work,)).selected == ()
    assert plan_delegation((work,)).assignments == ()
    with pytest.raises(PermissionError):
        activate(work, "owner")


def test_separately_licensed_candidate_retains_execution_path():
    artifact = ArtifactRecord("evidence", "x")
    result = intake([artifact], {"extract": lambda a: [{
        "candidate_id": "candidate", "candidate_type": "MECHANISM_OR_CAPABILITY",
        "source_span": "line:1", "load_bearing": True}]})
    candidate, = to_work_items(result, package_verifier=lambda _: True)
    licensed = WorkItem(**{**candidate.__dict__, "licensed": True,
                          "authority": ("owner",)})
    assert plan_delegation((licensed,)).assignments[0].work_id == candidate.work_id
    assert activate(licensed, "owner").status is WorkStatus.ACTIVE


@pytest.mark.parametrize("coordinate", ["load_bearing", "executable_claim", "bound"])
def test_text_false_never_becomes_true_in_intake(coordinate):
    artifact = ArtifactRecord("a", "x")
    def unsafe_generator(a):
        return [{"candidate_id": "x", "candidate_type": "RUNTIME_BINDING_OR_TRIGGER",
                 "source_span": "line:1", "load_bearing": True,
                 "executable_claim": True, "bound": False,
                 coordinate: "false"}]
    result = intake([artifact], {"unsafe": unsafe_generator})
    assert result.candidates == ()
    assert result.unresolved_extraction == ("a:unsafe:TypeError",)
    assert result.generator_receipts[0].status == "ERROR"
    assert to_work_items(result) == ()


def test_real_false_bound_is_preserved_and_not_executable():
    result = intake([ArtifactRecord("a", "x")], {"safe": lambda a: [{
        "candidate_id": "x", "candidate_type": "RUNTIME_BINDING_OR_TRIGGER",
        "source_span": "line:1", "load_bearing": True,
        "executable_claim": True, "bound": False}]})
    assert len(result.candidates) == 1
    assert result.candidates[0].bound is False
    assert candidate_admission(result.candidates[0], package_verifier=lambda oid: True) == Admission.OPEN


def test_actual_boolean_true_preserves_admitted_candidate():
    result = intake([ArtifactRecord("a", "x")], {"safe": lambda a: [{
        "candidate_id": "x", "candidate_type": "RUNTIME_BINDING_OR_TRIGGER",
        "source_span": "line:1", "load_bearing": True,
        "executable_claim": True, "bound": True}]})
    assert candidate_admission(result.candidates[0], package_verifier=lambda oid: True) == Admission.ACCEPT


@pytest.mark.parametrize("conflict", [
    {"load_bearing": False},
    {"bound": False},
    {"executable_claim": False},
    {"known_equivalent": "existing-other"},
])
def test_conflicting_generators_cannot_pick_authority_by_sort_order(conflict):
    first = {"candidate_id": "collision", "candidate_type": "RUNTIME_BINDING_OR_TRIGGER",
             "source_span": "line:1", "load_bearing": True,
             "executable_claim": True, "bound": True}
    second = {**first, **conflict}
    artifact = ArtifactRecord("evidence", "x")
    result = intake([artifact], {"first": lambda a: [first], "second": lambda a: [second]})
    assert result.candidates == ()
    assert result.unresolved_extraction == (
        "evidence:collision:CONFLICTING_ADMISSION_COORDINATES",
    )
    assert to_work_items(result, package_verifier=lambda oid: True) == ()
    assert all(r.status == "COMPLETE" for r in result.generator_receipts)


def test_consistent_duplicate_candidate_does_not_multiply_work():
    record = {"candidate_id": "same", "candidate_type": "MECHANISM_OR_CAPABILITY",
              "source_span": "line:1", "load_bearing": True}
    result = intake([ArtifactRecord("evidence", "x")],
                    {"a": lambda a: [record], "b": lambda a: [dict(record)]})
    assert result.unresolved_extraction == ()
    assert len(result.candidates) == 1
    assert len(to_work_items(result)) == 1
