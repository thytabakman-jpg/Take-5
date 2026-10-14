"""Native adversarial checks for opt-in empty-package-page compaction."""
from pathlib import Path
import sys
import pytest

sys.path.insert(0, "runtime")
import tool_package_sparse_migration as sparse
from tool_project_packages import current_tool_specs, coverage_cells, coverage_name, render_coverage_cell


@pytest.fixture
def one_cell(tmp_path: Path, monkeypatch):
    spec = current_tool_specs()[0]  # C01; not MultiObject or GOAL
    idx, scope, mode = coverage_cells()[0]
    monkeypatch.setattr(sparse, "all_project_specs", lambda: (spec,))
    monkeypatch.setattr(sparse, "coverage_cells", lambda: ((idx, scope, mode),))
    folder = tmp_path / "projects/tool-system/current-tools/c01/coverage"
    folder.mkdir(parents=True)
    path = folder / coverage_name(idx, scope, mode)
    return tmp_path, spec, idx, scope, mode, path


def test_exact_empty_template_is_candidate_and_does_not_delete(one_cell):
    root, spec, idx, scope, mode, path = one_cell
    source = render_coverage_cell(spec, idx, scope, mode)
    path.write_text(source, encoding="utf-8")
    result = sparse.candidate_plan(root)
    assert result["dispositions"]["EMPTY_TEMPLATE"] == 1
    assert result["delete_authorized"] is False
    assert result["current_project_goal_unchanged"] is True
    assert path.is_file() and path.read_text(encoding="utf-8") == source


def test_nonempty_evidence_is_preserved_even_if_most_of_template_is_unchanged(one_cell):
    root, spec, idx, scope, mode, path = one_cell
    source = render_coverage_cell(spec, idx, scope, mode)
    path.write_text(source.replace("- none admitted yet", "- W001: witness admitted"), encoding="utf-8")
    result = sparse.candidate_plan(root)
    assert result["dispositions"]["PRESERVE"] == 1
    assert str(path.relative_to(root)) in result["protected_paths"]
    assert result["candidate_empty_file_paths"] == []


def test_semantic_change_and_even_single_byte_change_are_never_silently_removed(one_cell):
    root, spec, idx, scope, mode, path = one_cell
    path.write_text(render_coverage_cell(spec, idx, scope, mode) + "\n", encoding="utf-8")
    assert sparse.candidate_plan(root)["dispositions"]["PRESERVE"] == 1


def test_unknown_cell_name_is_protected_and_reported(one_cell):
    root, spec, idx, scope, mode, path = one_cell
    path.write_text(render_coverage_cell(spec, idx, scope, mode), encoding="utf-8")
    other = path.parent / "37_EXTRA__EXPAND.md"
    other.write_text("nonmatching provenance", encoding="utf-8")
    out = sparse.candidate_plan(root)
    assert out["dispositions"]["UNKNOWN_CELL"] == 1
    assert str(other.relative_to(root)) in out["protected_paths"]


def test_missing_physical_page_is_not_represented_as_present(one_cell):
    root, spec, idx, scope, mode, path = one_cell
    out = sparse.candidate_plan(root)
    assert out["dispositions"]["MISSING"] == 1
    assert str(path.relative_to(root)) in out["missing_coordinates"]
    assert out["candidate_empty_file_paths"] == []


def test_goals_curated_link_variant_is_only_admitted_when_exact(one_cell, monkeypatch):
    root, spec, idx, scope, mode, path = one_cell
    from dataclasses import replace
    goal = replace(spec, object_id="GOAL", display_name="GOAL")
    monkeypatch.setattr(sparse, "all_project_specs", lambda: (goal,))
    goalpath = root / "projects/tool-system/current-tools/goal/coverage" / path.name
    goalpath.parent.mkdir(parents=True)
    rendered = render_coverage_cell(goal, idx, scope, mode)
    link_format = rendered.replace(sparse.BASE_ENDING, sparse.LINK_ONLY_GOAL_ENDING)
    assert link_format != rendered
    goalpath.write_text(link_format, encoding="utf-8")
    assert sparse.candidate_plan(root)["dispositions"]["EMPTY_TEMPLATE"] == 1
    goalpath.write_text(link_format + "extra findings", encoding="utf-8")
    assert sparse.candidate_plan(root)["dispositions"]["PRESERVE"] == 1


def test_existing_markdown_reader_is_recorded_before_compaction(one_cell):
    root, spec, idx, scope, mode, path = one_cell
    path.write_text(render_coverage_cell(spec, idx, scope, mode), encoding="utf-8")
    consumer = path.parent / "README.md"
    consumer.write_text(f"[important witness link](./{path.name})\\n", encoding="utf-8")
    out = sparse.candidate_plan(root)
    assert str(consumer.relative_to(root)) in out["existing_markdown_readers_requiring_migration"]
    assert path.is_file()  # a plan must not touch either source or consumer


def test_sparse_core_projection_preserves_curated_substance_and_originals(one_cell):
    root, spec, idx, scope, mode, page = one_cell
    folder = page.parent.parent
    manifest = folder / "MANIFEST.md"
    regression = folder / "REGRESSION_CONTRACT.md"
    index = page.parent / "README.md"
    name = page.name
    manifest.write_text(
        "# Manifest\\nCoverage cells: 36\\n## Coverage pages\\n"
        f"- [coverage/{name}](coverage/{name})\\n## Curated proof of identity\\nunchanged\\n",
        encoding="utf-8",
    )
    regression.write_text(
        "- exactly 36 Scope x ModeFace coverage pages exist\\n"
        "## Native protected invariants\\nnever overwrite authored findings\\n",
        encoding="utf-8",
    )
    index.write_text(f"- [{idx:02d} {mode.value}](./{name})\\n", encoding="utf-8")
    before = [p.read_bytes() for p in (manifest, regression, index)]
    edits = sparse.proposed_sparse_core_updates(root)
    assert "## Reserved logical coverage coordinates" in edits[str(manifest.relative_to(root))]
    assert f"- coverage/{name}" in edits[str(manifest.relative_to(root))]
    assert "## Curated proof of identity\\nunchanged" in edits[str(manifest.relative_to(root))]
    assert "## Native protected invariants" in edits[str(regression.relative_to(root))]
    assert "physical cell files are reserved for admitted evidence" in edits[str(regression.relative_to(root))]
    assert "reserved logical coordinate" in edits[str(index.relative_to(root))]
    assert [p.read_bytes() for p in (manifest, regression, index)] == before


def test_frozen_repository_coverage_scan_precedes_deletion():
    """Run directly in a full checkout; never interpret a partial corpus as safe."""
    root = Path(__file__).resolve().parents[1]
    plan = sparse.candidate_plan(root)
    assert plan["total_logical_coordinates"] == 5040
    assert plan["dispositions"]["EMPTY_TEMPLATE"] == 5040
    assert plan["dispositions"]["PRESERVE"] == 0
    assert plan["dispositions"]["MISSING"] == 0
    assert plan["dispositions"]["UNKNOWN_CELL"] == 0
    assert plan["delete_authorized"] is False
