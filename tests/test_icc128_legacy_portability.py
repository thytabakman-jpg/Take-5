import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0,"runtime")

from icc128_legacy_portable import (
    PORTABLE_MATH,
    F128,
    portable_core_package,
    take5_activation_closed,
)
from show_me_the_math_contract import assess_show_math_package


def test_single_file_executes_in_isolated_fresh_directory(tmp_path):
    src=Path("runtime/icc128_legacy_portable.py")
    dst=tmp_path/"icc128_legacy_portable.py"
    shutil.copyfile(src,dst)
    proc=subprocess.run(
        [sys.executable,str(dst)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode==0, proc.stdout+proc.stderr
    assert '"portable_core": "PASS"' in proc.stdout
    assert '"exact_take5_activation_without_github_receipt": "BLOCKED"' in proc.stdout


def test_show_me_the_math_closes_for_portable_core_when_host_primitives_exist():
    package=portable_core_package(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=True,
    )
    out=assess_show_math_package(package)
    assert out.complete
    assert out.unresolved_symbols==()
    assert out.hidden_dependencies==()
    assert out.unavailable_primitives==()
    assert out.unsatisfied_obligations==()


def test_show_me_the_math_fails_closed_without_semantic_reasoner():
    package=portable_core_package(
        semantic_reasoner_available=False,
        execution_interface_available=True,
        controller_bindings_available=True,
    )
    out=assess_show_math_package(package)
    assert not out.complete
    assert "semantic_reasoner" in out.unavailable_primitives


def test_math_preserves_frozen_controller_signature_and_capability_family():
    assert "ICC_128 = C_128(Z_t,F_128,MI_t)" in PORTABLE_MATH
    assert "Q_t = rho_128(Z_t,MI_t) subseteq F_128" in PORTABLE_MATH
    assert "Y_t = Run_128(Q_t,Z_t,MI_t)" in PORTABLE_MATH
    assert "MI_(t+1) = Sync_128(MI_t,Y_t)" in PORTABLE_MATH
    assert "Z_(t+1) = U_128(Z_t,Y_t,MI_(t+1))" in PORTABLE_MATH
    assert F128==("L","O","R_123","D_PD","G","A","M_MT","T_2","E","V")


def test_exact_take5_activation_remains_distinct_from_portable_core():
    assert not take5_activation_closed(None)
    assert take5_activation_closed({
        "repository":"thytabakman-jpg/Take-5",
        "path":"artifacts/icc128-legacy-learning/x.json",
        "commit_sha":"abc",
        "report_sha256":"def",
    })


def test_show_me_the_math_fails_closed_without_higher_order_controller_bindings():
    package=portable_core_package(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=False,
    )
    out=assess_show_math_package(package)
    assert not out.complete
    for name in ("package_compiler","admission_binding","update_binding","discovery_closure_binding"):
        assert name in out.unavailable_primitives
