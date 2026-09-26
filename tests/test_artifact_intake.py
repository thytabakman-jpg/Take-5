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
            "semantic_package_current": True,
        }]
    r = intake([artifact], {"g": g})
    assert candidate_admission(r.candidates[0]) == Admission.ACCEPT
