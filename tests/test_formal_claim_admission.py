import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from formal_claim_admission import (
    FormalCompositionPacket,
    FormalObjectBinding,
    assess_formal_claim,
)


def binding(**overrides):
    base=dict(
        object_id="ImprovementCore",
        version_id="regime-091",
        basis_id="take5-main",
        authority_id="CURRENT_IMPROVEMENT_CORE",
        role="ROOT",
        identification_status="IDENTIFIED",
        currentness_status="CURRENT",
        required_coordinates=frozenset({"math","wrapper","closure"}),
        recovered_coordinates=frozenset({"math","wrapper","closure"}),
        invariant_coordinates=frozenset(),
        source_refs=("integration/CURRENT_IMPROVEMENT_CORE.md",),
        dependency_disposition="CURRENT",
        admitted_by_authority=None,
        load_bearing=True,
    )
    base.update(overrides)
    return FormalObjectBinding(**base)


def packet(*bindings, **overrides):
    base=dict(
        claim_scope="CURRENT",
        bindings=tuple(bindings) or (binding(),),
        composition_typecheck="PASS",
        dependency_closure="PASS",
        authority_consistency="PASS",
        source_consistency="PASS",
    )
    base.update(overrides)
    return FormalCompositionPacket(**base)


def test_current_authoritative_claim_passes_only_with_exact_current_root():
    r=assess_formal_claim(packet(binding()))
    assert r.status=="PASS"
    assert r.green_licensed


def test_stale_root_cannot_be_emitted_as_current_math():
    stale=binding(
        version_id="regime-086",
        currentness_status="SUPERSEDED",
        source_refs=("architecture/IMPROVEMENT_CORE_MATHEMATICS_086.md",),
    )
    r=assess_formal_claim(packet(stale))
    assert r.status=="OPEN"
    assert not r.green_licensed
    assert any(x.startswith("ROOT_CURRENTNESS_MISMATCH") for x in r.residuals)


def test_frozen_historical_dependency_is_legal_only_when_current_root_admits_it():
    root=binding(
        object_id="ICC128LegacyActivation",
        version_id="take5-legacy-activation-001",
        authority_id="CURRENT_ICC128_LEGACY_MATH",
        source_refs=("integration/CURRENT_ICC128_LEGACY_MATH.md",),
    )
    frozen=binding(
        object_id="ICC128FrozenCore",
        version_id="reaserch-e4c76c5",
        basis_id="frozen-reaserch",
        authority_id="FROZEN_ICC128_CORE",
        role="DEPENDENCY",
        currentness_status="HISTORICAL",
        source_refs=("legacy/icc128-legacy/snapshot/math/ICC128_FULL_TOOL_MATH_002_2026-09-26.md",),
        dependency_disposition="ADMITTED_FROZEN",
        admitted_by_authority="CURRENT_ICC128_LEGACY_MATH",
    )
    r=assess_formal_claim(packet(root,frozen))
    assert r.status=="PASS"


def test_unadmitted_frozen_dependency_blocks_current_composition():
    root=binding(
        object_id="ICC128LegacyActivation",
        authority_id="CURRENT_ICC128_LEGACY_MATH",
        source_refs=("integration/CURRENT_ICC128_LEGACY_MATH.md",),
    )
    frozen=binding(
        object_id="LegacyMT",
        version_id="legacy",
        role="DEPENDENCY",
        currentness_status="HISTORICAL",
        dependency_disposition="ADMITTED_FROZEN",
        admitted_by_authority="SOME_OTHER_AUTHORITY",
        source_refs=("legacy/mt.md",),
    )
    r=assess_formal_claim(packet(root,frozen))
    assert r.status=="OPEN"
    assert "FROZEN_DEPENDENCY_NOT_ADMITTED_BY_ROOT_AUTHORITY:LegacyMT" in r.residuals


def test_current_composition_must_typecheck():
    r=assess_formal_claim(packet(binding(),composition_typecheck="OPEN"))
    assert r.status=="OPEN"
    assert "COMPOSITION_TYPECHECK_NOT_PASS:OPEN" in r.residuals


def test_missing_load_bearing_coordinate_blocks_green():
    root=binding(
        required_coordinates=frozenset({"math","wrapper","closure","parent_return"}),
        recovered_coordinates=frozenset({"math","wrapper","closure"}),
    )
    r=assess_formal_claim(packet(root))
    assert not r.green_licensed
    assert "UNRECOVERED_COORDINATE:ImprovementCore:parent_return" in r.residuals


def test_exact_historical_claim_can_be_green_without_pretending_to_be_current():
    historical=binding(
        object_id="ICC128FrozenCore",
        version_id="reaserch-e4c76c5",
        authority_id="FROZEN_ICC128_CORE",
        currentness_status="SUPERSEDED",
        source_refs=("legacy/icc128-legacy/snapshot/math/ICC128_FULL_TOOL_MATH_002_2026-09-26.md",),
    )
    r=assess_formal_claim(packet(historical,claim_scope="HISTORICAL"))
    assert r.status=="PASS"
    assert r.green_licensed


def test_non_load_bearing_old_evidence_does_not_define_current_identity():
    root=binding()
    evidence=binding(
        object_id="OldCandidate",
        version_id="v1",
        role="EVIDENCE",
        currentness_status="SUPERSEDED",
        required_coordinates=frozenset(),
        recovered_coordinates=frozenset(),
        source_refs=("history/old-candidate.md",),
        dependency_disposition="EVIDENCE_ONLY",
        load_bearing=False,
    )
    r=assess_formal_claim(packet(root,evidence))
    assert r.status=="PASS"


def test_mapping_input_fails_closed_without_authority_and_version():
    r=assess_formal_claim({
        "claim_scope":"CURRENT",
        "composition_typecheck":"PASS",
        "dependency_closure":"PASS",
        "authority_consistency":"PASS",
        "source_consistency":"PASS",
        "bindings":[{
            "object_id":"ImprovementCore",
            "role":"ROOT",
            "identification_status":"IDENTIFIED",
            "currentness_status":"CURRENT",
            "required_coordinates":["math"],
            "recovered_coordinates":["math"],
            "source_refs":["integration/CURRENT_IMPROVEMENT_CORE.md"],
        }],
    })
    assert not r.green_licensed
    assert any(x.startswith("VERSION_ID_REQUIRED") for x in r.residuals)
    assert any(x.startswith("BASIS_ID_REQUIRED") for x in r.residuals)
    assert any(x.startswith("AUTHORITY_ID_REQUIRED") for x in r.residuals)


def test_formal_system_math_request_requires_claim_receipt():
    from formal_claim_admission import request_requires_formal_claim_receipt
    assert request_requires_formal_claim_receipt(
        "Give me the current math for ImprovementCore",
        target="ImprovementCore",
        job="recover current controller mathematics",
    )


def test_unrelated_math_question_does_not_trigger_formal_system_receipt():
    from formal_claim_admission import request_requires_formal_claim_receipt
    assert not request_requires_formal_claim_receipt(
        "What is 2 plus 2?",
        target="arithmetic",
        job="calculate",
    )


def test_canonical_state_admission_stores_normalized_receipt():
    from formal_claim_admission import admit_formal_claim_to_state
    state,receipt=admit_formal_claim_to_state({},packet(binding()))
    assert receipt.status=="PASS"
    assert len(state["authoritative_formal_claims"])==1
    row=state["authoritative_formal_claims"][0]
    assert row["status"]=="PASS"
    assert row["root_object_id"]=="ImprovementCore"
    assert row["root_version_id"]=="regime-091"


def test_new_math_for_named_system_requires_claim_receipt():
    from formal_claim_admission import request_requires_formal_claim_receipt
    assert request_requires_formal_claim_receipt(
        "Give me the new math",
        target="ImprovementCore",
        job="reconstruct controller",
    )


def test_math_named_evidence_context_does_not_require_output_receipt():
    from formal_claim_admission import request_requires_formal_claim_receipt
    assert not request_requires_formal_claim_receipt(
        "ImproveCore observer mode. Use the MT results as evidence, not as a draft.",
        target="prior full-system Show-Me-the-Math campaign closure",
        job="evaluate MT evidence and determine licensed next work",
    )
