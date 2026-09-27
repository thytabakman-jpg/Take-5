import sys
from pathlib import Path
import tempfile

sys.path.insert(0,"runtime")

from tool_project_packages import (
    CORE_FILES, ICC_ALIASES, ToolProjectPackageCollision,
    all_project_specs, append_record, audit_materialized,
    coverage_cells, current_tool_specs, icc_variant_specs,
    materialize_all, materialize_package, package_files,
)
from tool_run_registry import MATERIAL_TOOLS


def test_current_tool_inventory_has_exact_package_spec_parity():
    assert tuple(x.object_id for x in current_tool_specs())==tuple(MATERIAL_TOOLS)


def test_every_object_package_has_required_core_and_exactly_36_coverage_pages():
    for spec in all_project_specs():
        files=package_files(spec)
        for rel in CORE_FILES:
            assert any(path.endswith("/"+rel) for path in files)
        coverage=[
            path for path in files
            if "/coverage/" in path and not path.endswith("/coverage/README.md")
        ]
        assert len(coverage)==36


def test_coverage_surface_is_scope_x_modeface_and_distinct_from_handoff_surface():
    cells=coverage_cells()
    assert len(cells)==36
    assert len({(scope.value,face.value) for _,scope,face in cells})==36
    sample=package_files(current_tool_specs()[0])[
        next(p for p in package_files(current_tool_specs()[0]) if p.endswith("coverage/01_SYSTEM__EXPAND.md"))
    ]
    assert "Scope: SYSTEM" in sample
    assert "Mode face: EXPAND" in sample
    assert "SourceScope x TargetScope" not in sample


def test_materializer_refuses_to_overwrite_changed_existing_content(tmp_path:Path):
    spec=current_tool_specs()[0]
    materialize_package(tmp_path,spec)
    p=tmp_path/"projects/tool-system"/"current-tools"/"c01"/"CURRENT_STATE.md"
    p.write_text("human/evidence change",encoding="utf-8")
    try:
        materialize_package(tmp_path,spec)
    except ToolProjectPackageCollision:
        pass
    else:
        raise AssertionError("package overwrite was silently allowed")
    assert p.read_text(encoding="utf-8")=="human/evidence change"


def test_append_stream_records_are_immutable(tmp_path:Path):
    spec=current_tool_specs()[0]
    materialize_package(tmp_path,spec)
    append_record(tmp_path,spec,"evidence","E001","first")
    try:
        append_record(tmp_path,spec,"evidence","E001","replacement")
    except FileExistsError:
        pass
    else:
        raise AssertionError("append-only evidence record was replaced")


def test_icc_aliases_do_not_duplicate_package_identity():
    variant_ids={x.object_id for x in icc_variant_specs()}
    for alias,target in ICC_ALIASES.items():
        assert target in variant_ids or target=="ICC-128-CURRENT"
        assert alias not in variant_ids


def test_unrecovered_icc_referents_remain_explicit_open_states():
    rows={x.object_id:x.status for x in icc_variant_specs()}
    assert rows["ICC-107"]=="MENTIONED_UNRECOVERED"
    assert rows["ICC-108"]=="MENTIONED_UNRECOVERED"
    assert rows["ICC-118"]=="UNRECOVERED_FORMAL_OBJECT"
    assert rows["IC-016"]=="UNRECOVERED_GAP"
    assert rows["IC-027"]=="UNRECOVERED_GAP"


def test_repository_materialization_is_complete():
    root=Path(__file__).resolve().parents[1]
    out=audit_materialized(root)
    assert out["status"]=="CLOSED_RELATIVE"
    assert out["current_tool_count"]==len(MATERIAL_TOOLS)
    assert out["missing"]==()
    assert out["bad_coverage"]==()
    assert out["registry_parity"] is True
