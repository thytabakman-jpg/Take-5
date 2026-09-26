import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from global_tool_execution import build_tool_execution_plan
from portable_tool_conductor import portability_open_set, run_tool_conductor
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS


MATH_PATH=ROOT/"artifacts"/"full-system-campaign"/"SHOW_ME_THE_MATH_FULL_SYSTEM_MATH_001_2026-09-26.md"
REPORT_PATH=ROOT/"artifacts"/"full-system-campaign"/"FULL_SYSTEM_SHOW_ME_THE_MATH_CAMPAIGN_REPORT_001_2026-09-26.md"
LEGACY_REPORT_PATH=ROOT/"artifacts"/"icc128-legacy-learning"/"icc128-legacy-full-system-show-math-20260926-004.json"


def test_mt_full_configured_plan_has_all_bells_and_whistles():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    assert plan.complete
    assert len(plan.cells)==36
    assert len(plan.questions)==22*36
    assert len(plan.cognitive)==4*36
    assert plan.wrapper_required is True
    assert plan.mode=="OBSERVER"


def test_goal_configured_plan_is_full_36_observer_wrapper():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["GOAL"])
    assert plan.complete
    assert len(plan.cells)==36
    assert len(plan.questions)==22*36
    assert len(plan.cognitive)==4*36
    assert plan.wrapper_required is True
    assert plan.mode=="OBSERVER"


def test_everything_tool_conductor_covers_current_registered_repertoire():
    out=run_tool_conductor({
        "target":"full current conversation and user campaign request",
        "campaign":"full-system-show-math-campaign-20260926",
    })
    assert len(MATERIAL_TOOLS)==91
    assert out["tool_count"]==91
    assert tuple(r["tool_id"] for r in out["results"])==tuple(MATERIAL_TOOLS)
    assert len({r["tool_id"] for r in out["results"]})==91
    tc=[r for r in out["results"] if r["tool_id"]=="ToolConductor"]
    assert len(tc)==1
    assert tc[0]["status"]=="EXECUTED_SELF_WITNESS"
    assert len(out["portability_open_set"])==31
    assert tuple(out["portability_open_set"])==tuple(portability_open_set())
    assert out["status"]=="OPEN"


def test_icc130_is_not_silently_invented_or_substituted():
    assert "ICC130" not in MATERIAL_TOOLS
    assert "ICC-130" not in MATERIAL_TOOLS
    assert "ICC 130" not in MATERIAL_TOOLS


def test_icc128_legacy_portable_reference_executes():
    source=ROOT/"runtime"/"icc128_legacy_portable.py"
    proc=subprocess.run(
        [sys.executable,str(source)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode==0,proc.stderr
    assert '"portable_core": "PASS"' in proc.stdout
    assert '"exact_take5_activation_without_github_receipt": "BLOCKED"' in proc.stdout


def test_legacy_learning_report_is_present_and_typed():
    report=json.loads(LEGACY_REPORT_PATH.read_text())
    assert report["tool"]=="ICC128 Legacy"
    assert report["run_id"]=="icc128-legacy-full-system-show-math-20260926-004"
    assert report["run_status"]=="COMPLETE"
    assert report["learning_status"]=="MATERIAL_LEARNING"
    assert report["final_state"]["icc130"]=="BLOCKED_IDENTITY_UNRECOVERED"
    assert report["report_required_even_when_no_material_learning"] is True


def test_giant_report_and_math_markdown_are_present():
    report=REPORT_PATH.read_text()
    math=MATH_PATH.read_text()
    assert "Full System Show-Me-the-Math Campaign Report 001" in report
    assert "ICC130\n=\nBLOCKED(IDENTITY_UNRECOVERED)" in math
    assert "TC_I(x,c)" in math
    assert "ICC_128" in math
    assert "Σ = 𝟙_{Δ ∩ Ω ∩ Φ ∩ Ξ}" in math
