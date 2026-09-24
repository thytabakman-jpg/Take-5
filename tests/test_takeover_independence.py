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
    for p in root.glob("*.py"):
        if p.name=="foundation_snapshot.py":
            continue
        txt=p.read_text()
        if needle in txt:
            hits.append(p.name)
    assert hits==[]
