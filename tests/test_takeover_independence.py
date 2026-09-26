from pathlib import Path
from tool_run_registry import MATERIAL_TOOLS,CONFIGURED_RUNS
from configured_run import validate_specs

def test_every_material_foundation_tool_has_configured_run_identity():
    assert len(MATERIAL_TOOLS)==len(CONFIGURED_RUNS)
    assert validate_specs(CONFIGURED_RUNS.values())

def test_every_c_capability_has_configured_run_identity():
    assert all(f"C{i:02d}" in CONFIGURED_RUNS for i in range(1,50))

def test_runtime_has_no_predecessor_repository_dependency():
    root=Path(__file__).parents[1]/"runtime"
    hits=[]
    needle="thytabakman-jpg"+"/"+"Reaserch"
    provenance_only={"icc128_legacy.py","icc128_legacy_reporting.py"}
    for p in root.glob("*.py"):
        if p.name=="foundation_snapshot.py" or p.name in provenance_only:
            continue
        txt=p.read_text()
        if needle in txt:
            hits.append(p.name)
    assert hits==[]

def test_icc128_legacy_predecessor_reference_is_provenance_not_runtime_dependency():
    root=Path(__file__).parents[1]
    loader=(root/"runtime"/"icc128_legacy.py").read_text()
    reporting=(root/"runtime"/"icc128_legacy_reporting.py").read_text()
    manifest=(root/"legacy"/"icc128-legacy"/"MANIFEST.yaml").read_text()

    assert "SNAPSHOT_ROOT" in loader
    assert '"legacy" / "icc128-legacy" / "snapshot"' in loader
    assert "api.github.com/repos/thytabakman-jpg/Reaserch" not in loader
    assert "api.github.com/repos/thytabakman-jpg/Reaserch" not in reporting
    assert "source_mutation_authorized: false" in manifest
    assert "writes_to_reaserch: false" in manifest
