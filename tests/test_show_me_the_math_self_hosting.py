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
