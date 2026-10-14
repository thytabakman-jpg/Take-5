from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "projects" / "mathematical-interface-architecture"
REG = P / "ARTIFACT_REGISTRY.yaml"

CORE = {
    "PROJECT_CHARTER.md",
    "CANONICAL_MODEL.md",
    "MATHEMATICAL_COLOR_INVARIANT.md",
    "ARTIFACT_REGISTRY.yaml",
    "CURRENTNESS_SOURCE_MANIFEST.md",
    "FRICTION_GAP_LEDGER.md",
    "VALIDATION_CONTRACT.md",
    "NEW_PROJECT_ARTIFACT_SOP.md",
}

def test_all_eight_core_artifacts_exist():
    missing = [name for name in CORE if not (P / name).exists()]
    assert not missing, missing

def test_registry_declares_exactly_eight_core_roles_and_paths_exist():
    data = yaml.safe_load(REG.read_text(encoding="utf-8"))
    assert data["core_role_count"] == 8
    core = data["core_artifacts"]
    assert len(core) == 8
    for item in core:
        assert (ROOT / item["path"]).exists(), item["path"]

def test_frozen_candidate_v4_equation_is_preserved():
    expected = "ICC₁₂₈ = C₁₂₈(Zₜ, F₁₂₈, MIₜ)"
    assert expected in (P / "PROJECT_CHARTER.md").read_text(encoding="utf-8")
    assert expected in (P / "CANONICAL_MODEL.md").read_text(encoding="utf-8")
    data = yaml.safe_load(REG.read_text(encoding="utf-8"))
    assert data["protected_baseline"]["version"] == "Candidate V4"
    assert data["protected_baseline"]["equation"] == expected

def test_color_invariant_has_preview_safe_specimen_and_no_raw_color_commands():
    text = (P / "MATHEMATICAL_COLOR_INVARIANT.md").read_text(encoding="utf-8")
    assert "mathematical-color-invariant-specimen.svg" in text
    assert r"\color{" not in text
    assert (ROOT / "assets/mia/mathematical-color-invariant-specimen.svg").exists()

def test_visual_assets_color_glyphs_directly():
    for name in [
        "icc128-v4-core.svg",
        "icc128-v4-family.svg",
        "mathematical-color-invariant-specimen.svg",
    ]:
        text = (ROOT / "assets/mia" / name).read_text(encoding="utf-8")
        assert "#1a7f37" in text or "#cf222e" in text
        assert "<text" in text or "<tspan" in text

def test_currentness_manifest_dispositions_v4_v5_v6():
    text = (P / "CURRENTNESS_SOURCE_MANIFEST.md").read_text(encoding="utf-8")
    assert "Candidate V4 controls" in text
    assert "Candidate V5" in text
    assert "Candidate V6" in text
    assert "does not regain authority by recency alone" in text

def test_friction_ledger_covers_known_failure_families():
    text = (P / "FRICTION_GAP_LEDGER.md").read_text(encoding="utf-8")
    for marker in [
        "Math changes during layout work",
        "Color semantics exist but output remains black",
        "Raw rendering syntax appears on the visible surface",
        "Commentary enters the artifact",
        "multiple incompatible current versions",
        "Load-bearing term exists without canonical artifact",
        "Filename, internal version, and references diverge",
        "Semantic success is mistaken for rendered or executable success",
    ]:
        assert marker in text
