from pathlib import Path
import sys
sys.path.insert(0,"runtime")

from specification_before_transformation import SpecificationPacket, assess_transformation


IDENTITY_PATH="architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md"


def test_multiobject_fullmath_recovers_five_top_level_coordinates():
    text=Path(IDENTITY_PATH).read_text(encoding="utf-8")
    for token in (
        "FullMath_(J,K)(MultiObject)",
        "N_MO",
        "W_MO",
        "G_MO",
        "P_MO",
        "L_MO",
        "MO_core^2",
        "G_rel^MO",
        "C_rel^MO",
        "H_n",
        "D36_C",
        "HF002",
        "EXTERNAL_NOT_OWNED",
    ):
        assert token in text


def test_multiobject_runtime_build_can_preserve_open_factor_minimality():
    required=frozenset({
        "N_MO","W_MO","G_MO","P_MO","L_MO","FACTOR_MINIMALITY_MO"
    })
    packet=SpecificationPacket(
        object_id="MultiObject",
        basis_id="MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27",
        identification_status="IDENTIFIED",
        required_coordinates=required,
        resolved_coordinates=frozenset({
            "N_MO","W_MO","G_MO","P_MO","L_MO"
        }),
        open_coordinates=frozenset({"FACTOR_MINIMALITY_MO"}),
        invariant_coordinates=frozenset({"FACTOR_MINIMALITY_MO"}),
    )
    receipt=assess_transformation(packet,"BUILD")
    assert receipt.status=="PASS"
    assert receipt.licensed


def test_multiobject_identity_keeps_runtime_and_global_claims_open():
    text=Path(IDENTITY_PATH).read_text(encoding="utf-8")
    assert "Native Take-5 runtime:" in text
    assert "OPEN" in text
    assert "Global semantic minimality/completeness:" in text
    assert "Universal external-host interception:" in text
    assert "EXTERNAL_NOT_OWNED" in text


def test_multiobject_identity_pins_legacy_evidence_basis():
    text=Path(IDENTITY_PATH).read_text(encoding="utf-8")
    assert "492bf7da82ac346c1a17ab0acc2405adf17ae5c1" in text
