from pathlib import Path
from current_portfolio_identity import audit_current_portfolio_identity
from tool_run_registry import CONFIGURED_RUNS

def test_every_current_configured_tool_has_reconstructible_current_identity():
    out=audit_current_portfolio_identity()
    assert out.status=="CLOSED_RELATIVE"
    assert out.failures==()
    assert out.checked==len(CONFIGURED_RUNS)


def test_current_identity_audit_rejects_registered_key_to_other_tool_spec(monkeypatch):
    from dataclasses import replace
    import current_portfolio_identity as owner
    spec=CONFIGURED_RUNS["MT"]
    monkeypatch.setattr(owner,"CONFIGURED_RUNS",{"MT":replace(spec,tool_id="GOAL")})
    out=owner.audit_current_portfolio_identity()
    assert out.status=="OPEN"
    assert out.checked==1
    assert "MT:CONFIGURED_IDENTITY_MISMATCH" in out.failures


def test_current_identity_audit_rejects_wrong_manifest_identity(monkeypatch):
    from dataclasses import replace
    import current_portfolio_identity as owner
    original=owner.manifest_for
    monkeypatch.setattr(owner,"CONFIGURED_RUNS",{"MT":CONFIGURED_RUNS["MT"]})
    monkeypatch.setattr(owner,"manifest_for",
        lambda name:replace(original(name),tool_id="GOAL"))
    out=owner.audit_current_portfolio_identity()
    assert out.status=="OPEN"
    assert "MT:MANIFEST_INCOMPLETE" in out.failures


def test_current_identity_empty_repertoire_cannot_claim_relative_closure(monkeypatch):
    import current_portfolio_identity as owner
    monkeypatch.setattr(owner,"CONFIGURED_RUNS",{})
    out=owner.audit_current_portfolio_identity()
    assert out.status=="OPEN"
    assert out.checked==0
    assert "EMPTY_CONFIGURED_REPERTOIRE" in out.failures


def _assert_live_tool_index(index:str,root:Path):
    import re
    from tool_run_registry import MATERIAL_TOOLS
    from tool_project_packages import slug
    assert index.startswith("# Current Tool Package Index\n")
    rows=re.findall(r"(?m)^- \[([^\]]+)\]\((current-tools/[^)]+/README\.md)\)$",index)
    assert tuple(label for label,_ in rows)==tuple(MATERIAL_TOOLS)
    assert len(rows)==len(set(label for label,_ in rows))
    for label,rel in rows:
        assert rel==f"current-tools/{slug(label)}/README.md"
        assert (root/"projects/tool-system"/rel).is_file()
    assert "derived" not in index.lower() or "navigation" in index.lower()
    assert "SOURCE_MAP.md" in index
    assert "runtime/tool_run_registry.py" in index


def test_current_tool_index_parity_and_authority_owner_are_live():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    text=(root/"projects/tool-system/TOOL_INDEX.md").read_text(encoding="utf-8")
    _assert_live_tool_index(text,root)


def test_tool_index_negative_mutations_are_detected():
    import pytest
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    text=(root/"projects/tool-system/TOOL_INDEX.md").read_text(encoding="utf-8")
    for mutant in (
        text.replace("- [C01](current-tools/c01/README.md)\n","",1),
        text.replace("- [C01](current-tools/c01/README.md)","- [C01](current-tools/c02/README.md)",1),
        text.replace("- [MT](current-tools/mt/README.md)","- [MT](current-tools/goal/README.md)",1),
        text.replace("- [C02](current-tools/c02/README.md)","- [C01](current-tools/c02/README.md)",1),
    ):
        assert mutant!=text
        with pytest.raises(AssertionError):
            _assert_live_tool_index(mutant,root)
