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


def test_delegatedexecutor_generated_coverage_index_matches_committed_source():
    spec=next(s for s in current_tool_specs() if s.object_id=="DelegatedExecutor")
    generated=package_files(spec)["current-tools/delegatedexecutor/coverage/README.md"]
    repo_root=Path(__file__).resolve().parents[1]
    committed=(repo_root/"projects/tool-system/current-tools/delegatedexecutor/coverage/README.md").read_text(encoding="utf-8")
    assert generated==committed
    for index,scope,face in coverage_cells():
        name=f"{index:02d}_{scope.value}__{face.value}.md"
        assert generated.count(f"(./{name})")==1
    assert generated.count("](./")==36
    assert "evidence for one Scope x ModeFace coordinate" in generated


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


def test_multiobject_package_has_direct_runtime_math_and_legacy_lineage_routes():
    spec=next(x for x in current_tool_specs() if x.object_id=="MultiObject")
    generated=package_files(spec)
    root=Path(__file__).resolve().parents[1]/"projects/tool-system/current-tools/multiobject"

    def page(name):
        content=generated[f"current-tools/multiobject/{name}"]
        # Materialized organizational pages must remain reproducible from the generator.
        assert (root/name).read_text(encoding="utf-8")==content
        return content

    authority=page("AUTHORITY_REGISTRY.md")
    math=page("MATHEMATICS.md")
    runtime=page("RUNTIME.md")
    sources=page("SOURCE_MAP.md")
    deps=page("DEPENDENCIES.md")
    assert "| MultiObject native execution | runtime/multiobject.py |" in authority
    assert "| current invocation routing | runtime/portable_tool_conductor.py |" in authority
    assert "MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md" in math
    assert "multiobject_provider" in runtime
    assert "[Native relation-discovery executor](../../../../runtime/multiobject.py)" in deps
    assert "[Full-tool mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md)" in deps
    assert "runtime/multiobject.py" in runtime
    assert "492bf7da82ac346c1a17ab0acc2405adf17ae5c1" in sources
    assert "MULTI_OBJECT_CONNECTOR_PROTOCOL.md" in sources
    assert "tests/test_multiobject_fullmath_identity.py" in sources
    assert "[Configured tool registry](../../../../runtime/tool_run_registry.py)" in sources
    assert "## Moving Reaserch source locations (navigation, not authority)" in sources
    assert "blob/main/projects/pd/protocol/MULTI_OBJECT_CONNECTOR_PROTOCOL.md" in sources
    assert "blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1" in sources

def test_multiobject_batch2_coverage_and_streams_are_materialized_and_linked():
    spec=next(x for x in current_tool_specs() if x.object_id=="MultiObject")
    files=package_files(spec)
    root=Path(__file__).resolve().parents[1]/"projects/tool-system"
    prefix="current-tools/multiobject/"
    index=files[prefix+"coverage/README.md"]
    for number,scope,mode in coverage_cells():
        name=f"{number:02d}_{scope.value}__{mode.value}.md"
        path=prefix+"coverage/"+name
        expected=files[path]
        assert f"({('./'+name)})" in index
        assert "Disposition: OPEN" in expected
        assert "- none admitted yet" in expected
        assert "[all 36 coverage cells](README.md)" in expected
        assert "[authority registry](../AUTHORITY_REGISTRY.md)" in expected
        assert (root/path).read_text(encoding="utf-8")==expected
    assert index.count("](./")==36
    assert (root/(prefix+"coverage/README.md")).read_text(encoding="utf-8")==index
    for directory in ("evidence","runs","history"):
        path=prefix+directory+"/README.md"
        expected=files[path]
        assert "This directory is append-only." in expected
        assert "[Change control](../CHANGE_CONTROL.md)" in expected
        assert (root/path).read_text(encoding="utf-8")==expected


def _validate_registered_crosswalk(text:str)->tuple[tuple[str,str,str],...]:
    """Validate the navigational map against exact current configured identities.

    This checks names, links and taxonomy, not Reaserch semantics or external
    configured-run equivalence.
    """
    import re
    from tool_project_packages import package_relroot

    start="| Take-5 package | Reaserch formal object or family | Relation | Reaserch source pointer |"
    assert text.count(start)==1
    table=text.split(start,1)[1].split("### Reaserch objects without an exact Take-5 package mapping",1)[0]
    row_lines=[line for line in table.splitlines() if line.startswith("| [")]
    pattern=re.compile(
        r"^\| \[([^\]]+)\]\(current-tools/([^/]+)/README\.md\)"
        r" \| .+ \| (NAMED_CROSS_REFERENCE|ALIAS_COLLISION_OPEN|CAPABILITY_FAMILY_ONLY|UNMAPPED)"
        r" \| .+ \|$"
    )
    parsed=[]
    for line in row_lines:
        match=pattern.fullmatch(line)
        assert match is not None, f"Malformed crosswalk row: {line}"
        parsed.append(match.groups())
    specs=current_tool_specs()
    expected=[(spec.object_id,package_relroot(spec).split("/",1)[1]) for spec in specs]
    assert [(name,slug) for name,slug,_ in parsed]==expected
    assert len(parsed)==len({name for name,_,_ in parsed})==len(MATERIAL_TOOLS)
    named={
        "ImprovementCore","ICC128","MT","MTA","Architecture","PD","PDAudit",
        "HF001","HF002","TRC","RTC","MultiObject","ASSERT","GOAL","ToolConductor",
    }
    for name,slug,relation in parsed:
        required=(
            "CAPABILITY_FAMILY_ONLY" if name.startswith("C") and
            name[1:].isdigit() and 1<=int(name[1:])<=49 else
            "ALIAS_COLLISION_OPEN" if name in {"RootCause","Diagnosis"} else
            "NAMED_CROSS_REFERENCE" if name in named else "UNMAPPED"
        )
        assert relation==required, f"{name}: expected {required}, got {relation}"
    assert len(named)==15
    assert sum(relation=="NAMED_CROSS_REFERENCE" for _,_,relation in parsed)==15
    assert sum(relation=="ALIAS_COLLISION_OPEN" for _,_,relation in parsed)==2
    assert sum(relation=="CAPABILITY_FAMILY_ONLY" for _,_,relation in parsed)==49
    assert sum(relation=="UNMAPPED" for _,_,relation in parsed)==29
    assert "a navigable link" in text.lower()
    assert "identity equivalence `OPEN`" in text or "equivalence `OPEN`" in text
    return tuple(parsed)


def test_cross_repository_crosswalk_has_exact_current_inventory_and_typed_routes():
    root=Path(__file__).resolve().parents[1]
    text=(root/"projects/tool-system/SOURCE_MAP.md").read_text(encoding="utf-8")
    rows=_validate_registered_crosswalk(text)
    for _,slug,_ in rows:
        page=root/"projects/tool-system/current-tools"/slug/"SOURCE_MAP.md"
        content=page.read_text(encoding="utf-8")
        assert f"# Source map: " in content
        assert "SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer" in content
        assert "runtime/tool_run_registry.py" in content
    assert "ALIAS_COLLISION_OPEN" in text
    assert "CAPABILITY_FAMILY_ONLY" in text


def test_cross_repository_crosswalk_negative_controls_preserve_all_package_edges():
    import pytest
    root=Path(__file__).resolve().parents[1]
    text=(root/"projects/tool-system/SOURCE_MAP.md").read_text(encoding="utf-8")
    assert len(_validate_registered_crosswalk(text))==len(MATERIAL_TOOLS)
    for broken in (
        text.replace("| [C01](current-tools/c01/README.md)", "| [C01](current-tools/c02/README.md)",1),
        text.replace("| [GOAL](current-tools/goal/README.md)", "| [GOAL](current-tools/pd/README.md)",1),
        text.replace("| [C01](current-tools/c01/README.md)", "| [C01-REMOVED](current-tools/c01/README.md)",1),
        __import__("re").sub(r"(?m)^(\| \[RootCause\].+ \| )ALIAS_COLLISION_OPEN( \| .+ \|)$",r"\1NAMED_CROSS_REFERENCE\2",text,count=1),
        text.replace("| [C49](current-tools/c49/README.md)", "| [C49-REMOVED](current-tools/c49/README.md)",1),
    ):
        with pytest.raises(AssertionError):
            _validate_registered_crosswalk(broken)


def test_source_map_navigation_appendices_do_not_disable_create_only_collision(tmp_path:Path):
    spec=current_tool_specs()[0]
    materialize_package(tmp_path,spec)
    target=tmp_path/"projects/tool-system/current-tools/c01/SOURCE_MAP.md"
    original=target.read_text(encoding="utf-8")
    augmented=original+"\n## Additional human navigation\n\n- informational link\n"
    target.write_text(augmented,encoding="utf-8")
    try:
        materialize_package(tmp_path,spec)
    except ToolProjectPackageCollision:
        pass
    else:
        raise AssertionError("Create-only materializer silently accepted a divergent source-map")
    assert target.read_text(encoding="utf-8")==augmented


def test_curated_current_source_map_materialization_remains_idempotent(tmp_path:Path):
    """A single augmented package source-map must not freeze all regeneration."""
    repo=Path(__file__).resolve().parents[1]
    specimens=("C01","C21","GOAL","Architecture","RootCause","ProjectManager","L-D8")
    specs={spec.object_id:spec for spec in current_tool_specs()}
    for id in specimens:
        spec=specs[id]
        materialize_package(tmp_path,spec)
        rel=f"current-tools/{id.lower()}/SOURCE_MAP.md"
        live=(repo/"projects/tool-system"/rel).read_text(encoding="utf-8")
        local=tmp_path/"projects/tool-system"/rel
        local.write_text(live,encoding="utf-8")
        before=local.read_text(encoding="utf-8")
        assert materialize_package(tmp_path,spec)==()
        assert local.read_text(encoding="utf-8")==before


def test_curated_source_map_rejects_wrong_identity_lost_authority_and_category(tmp_path:Path):
    """Negative cases fail closed; never delete a protected navigational map."""
    repo=Path(__file__).resolve().parents[1]
    specs={spec.object_id:spec for spec in current_tool_specs()}
    for tool,poison in (
        ("GOAL", lambda s:s.replace("# Source map: GOAL", "# Source map: PD",1)),
        ("GOAL", lambda s:s.replace("runtime/tool_manifest.py","runtime/missing_manifest.py")),
        ("C21", lambda s:s.replace("related numbered capability family","unverified identical primitive")),
        ("RootCause", lambda s:s.replace("ALIAS_COLLISION_OPEN","NAMED_CROSS_REFERENCE")),
        ("L-D8", lambda s:s.replace("SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer",
                                       "SOURCE_MAP.md#dead-anchor")),
    ):
        spec=specs[tool]
        materialize_package(tmp_path,spec)
        local=tmp_path/"projects/tool-system"/f"current-tools/{tool.lower()}/SOURCE_MAP.md"
        live=(repo/"projects/tool-system"/f"current-tools/{tool.lower()}/SOURCE_MAP.md").read_text(encoding="utf-8")
        bad=poison(live)
        assert bad!=live
        local.write_text(bad,encoding="utf-8")
        try:
            materialize_package(tmp_path,spec)
        except ToolProjectPackageCollision:
            pass
        else:
            raise AssertionError(f"{tool}: invalid source-map silently admitted")
        assert local.read_text(encoding="utf-8")==bad
        local.write_text(live,encoding="utf-8")
        assert materialize_package(tmp_path,spec)==()


def _assert_canonical_tool_project_authority_links(text:str,root:Path):
    from re import findall
    mandatory={
        "current tool inventory":"[runtime/tool_run_registry.py](../../runtime/tool_run_registry.py)",
        "current protected tool identity":"[runtime/tool_manifest.py](../../runtime/tool_manifest.py)",
        "native runtime realization":"[runtime/portable_tool_conductor.py](../../runtime/portable_tool_conductor.py)",
        "derived cross-repository tool navigation":"[SOURCE_MAP.md](SOURCE_MAP.md)",
        "package schema":"[PACKAGE_CONTRACT.md](PACKAGE_CONTRACT.md)",
    }
    rows=text.splitlines()
    for job,exact_link in mandatory.items():
        candidates=[line for line in rows if line.startswith(f"| {job} |")]
        assert len(candidates)==1,f"Authority owner missing or duplicated: {job}"
        assert candidates[0]==f"| {job} | {exact_link} |",f"Wrong owner link: {job}"
    for rel in findall(r"\]\(([^)#]+)(?:#[^)]*)?\)",text):
        if "://" not in rel:
            assert (root/"projects/tool-system"/rel).exists(),f"Missing authority locator: {rel}"


def test_tool_project_authority_and_schema_contracts_have_live_sources():
    root=Path(__file__).resolve().parents[1]
    body=(root/"projects/tool-system/AUTHORITY_REGISTRY.md").read_text(encoding="utf-8")
    _assert_canonical_tool_project_authority_links(body,root)
    schema=(root/"projects/tool-system/PACKAGE_CONTRACT.md").read_text(encoding="utf-8")
    assert "Curated source maps and generator ownership" in schema
    for name in CORE_FILES:
        assert f"\n{name}\n" in schema,f"Required package page not in contract: {name}"
    assert "MultiObject source map remains fully generated" in schema
    assert "source map only after verifying its exact package identity" in schema


def test_authority_registry_negative_controls_are_discriminating():
    import pytest
    root=Path(__file__).resolve().parents[1]
    body=(root/"projects/tool-system/AUTHORITY_REGISTRY.md").read_text(encoding="utf-8")
    _assert_canonical_tool_project_authority_links(body,root)
    for broken in (
        body.replace("| current tool inventory |","| invented tool inventory |",1),
        body.replace("runtime/tool_manifest.py","runtime/missing_tool_manifest.py",1),
        body.replace("SOURCE_MAP.md](SOURCE_MAP.md)","SOURCE_MAP.md](missing_crosswalk.md)",1),
    ):
        with pytest.raises(AssertionError):
            _assert_canonical_tool_project_authority_links(broken,root)


def test_tool_registry_manifest_and_conductor_identity_trace_is_complete():
    from portable_tool_conductor import compile_repertoire
    from tool_manifest import manifest_for
    expected=tuple(MATERIAL_TOOLS)
    assert len(expected)==len(set(expected))
    observed=compile_repertoire()
    assert tuple(w.tool_id for w in observed)==expected
    for witness in observed:
        manifest=manifest_for(witness.tool_id)
        assert manifest.tool_id==witness.tool_id
        assert manifest.complete()
        assert witness.entrypoint is not None
