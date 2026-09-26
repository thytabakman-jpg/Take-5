import copy
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from show_me_the_math_portable import (
    REQUEST_CONTRACT,
    SELF_ENVIRONMENT,
    SELF_PACKAGE,
    assess,
    self_assess,
)
from mt_semantic_return_gate import run_mt_with_before_return_gate
from portable_tool_conductor import run_tool_conductor
from tool_run_registry import MATERIAL_TOOLS


def test_show_me_the_math_self_application_is_green():
    result=self_assess()
    assert result.complete is True
    assert result.status=="GREEN"
    assert result.missing_fields==()
    assert result.unresolved_symbols==()
    assert result.unavailable_primitives==()
    assert result.unsatisfied_obligations==()
    assert result.realizer_errors==()
    assert result.equivalence_errors==()


def test_show_me_the_math_is_request_contract_not_tool():
    assert SELF_PACKAGE["kind"]==REQUEST_CONTRACT
    assert "run_spec" not in SELF_PACKAGE
    assert SELF_PACKAGE["obligations"]["tool_run_spec"]["status"]=="NOT_APPLICABLE"
    assert SELF_PACKAGE["obligations"]["tool_run_spec"]["witness"]


def test_hidden_dependency_still_fails_closed():
    broken=copy.deepcopy(SELF_PACKAGE)
    broken["definitions"]["SHOW_ME_THE_MATH"]["dependencies"].append("HIDDEN_X")
    result=assess(broken,SELF_ENVIRONMENT)
    assert result.complete is False
    assert "HIDDEN_X" in result.unresolved_symbols


def test_missing_request_obligation_fails_closed():
    broken=copy.deepcopy(SELF_PACKAGE)
    del broken["obligations"]["evaluation"]
    result=assess(broken,SELF_ENVIRONMENT)
    assert result.complete is False
    assert "evaluation" in result.unsatisfied_obligations


def test_single_file_fresh_environment_execution(tmp_path):
    source=ROOT/"runtime"/"show_me_the_math_portable.py"
    isolated=tmp_path/"show_me_the_math_portable.py"
    isolated.write_bytes(source.read_bytes())

    proc=subprocess.run(
        [sys.executable,str(isolated)],
        cwd=tmp_path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode==0, proc.stderr
    assert '"complete": true' in proc.stdout.lower()


def test_portable_realizer_has_no_take5_or_legacy_imports():
    text=(ROOT/"runtime"/"show_me_the_math_portable.py").read_text()
    assert "from tool_" not in text
    assert "import tool_" not in text
    assert "from show_me_" not in text
    assert "Reaserch" not in text


def test_current_mt_gate_closes_on_repaired_self_package():
    def run_mt(state):
        result=self_assess()
        return dict(state), result.payload()

    def detect_black_boxes(state,result):
        residue=(
            tuple(result.get("unresolved_symbols",()))
            + tuple(result.get("unavailable_primitives",()))
            + tuple(result.get("unsatisfied_obligations",()))
            + tuple(result.get("realizer_errors",()))
            + tuple(result.get("equivalence_errors",()))
        )
        return residue

    def execute_stage(tool_id,object_id,state):
        return dict(state), "OPEN", False

    out=run_mt_with_before_return_gate(
        {"target":"SHOW_ME_THE_MATH"},
        run_mt=run_mt,
        detect_black_boxes=detect_black_boxes,
        execute_stage=execute_stage,
    )
    assert out.status=="CLOSED_RELATIVE"
    assert out.open_objects==()
    assert out.rounds==1
    assert out.mt_result["complete"] is True


def test_tool_conductor_exhaustively_visits_current_repertoire_for_self_hosting_target():
    out=run_tool_conductor({
        "target":"SHOW_ME_THE_MATH",
        "math_package":SELF_PACKAGE,
        "environment":SELF_ENVIRONMENT,
    })
    assert out["tool_count"]==len(MATERIAL_TOOLS)
    assert tuple(r["tool_id"] for r in out["results"])==tuple(MATERIAL_TOOLS)
    assert len({r["tool_id"] for r in out["results"]})==len(MATERIAL_TOOLS)
    tool_conductor=[r for r in out["results"] if r["tool_id"]=="ToolConductor"]
    assert len(tool_conductor)==1
    assert tool_conductor[0]["status"]=="EXECUTED_SELF_WITNESS"
