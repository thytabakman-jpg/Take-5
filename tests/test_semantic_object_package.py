from pathlib import Path
from semantic_object_package import (
    SemanticObjectSpec,expected_transition_names,package_files,
    materialize_package,append_evidence
)

def spec():
    return SemanticObjectSpec(
        object_id="TERM:BLACK_BOX",
        term="black box",
        object_type="SEMANTIC_OBJECT",
        status="BLACK_BOX_OPEN",
        definition="A load-bearing object with at least one required semantic coordinate unresolved.",
        known=("unresolved is permitted",),
        open_coordinates=("exact admission rule",),
    )

def test_package_has_core_manifest_and_36_transition_pages():
    files=package_files(spec())
    assert len(expected_transition_names())==36
    assert len(files)==38
    assert any(p.endswith("/CORE.md") for p in files)
    assert sum("/transitions/" in p for p in files)==36

def test_unknown_cells_are_explicit_open():
    files=package_files(spec())
    transitions=[c for p,c in files.items() if "/transitions/" in p]
    assert transitions and all("Disposition: OPEN" in c for c in transitions)

def test_materialize_does_not_overwrite_existing(tmp_path:Path):
    s=spec()
    materialize_package(tmp_path,s)
    core=next(tmp_path.rglob("CORE.md"))
    core.write_text("human update",encoding="utf-8")
    materialize_package(tmp_path,s,allow_existing=True)
    assert core.read_text(encoding="utf-8")=="human update"

def test_evidence_is_append_only(tmp_path:Path):
    s=spec()
    materialize_package(tmp_path,s)
    append_evidence(tmp_path,s,"E1","first")
    try:
        append_evidence(tmp_path,s,"E1","replacement")
    except FileExistsError:
        pass
    else:
        raise AssertionError("evidence overwrite was permitted")
