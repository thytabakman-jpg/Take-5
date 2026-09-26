import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0,"runtime")

from icc128_legacy_portable import (
    PORTABLE_MATH,
    F128,
    portable_core_package,
    portable_core_environment,
    exact_take5_activation_package,
    exact_take5_activation_environment,
    take5_activation_closed,
)
from show_me_the_math_portable import assess, surface_value, SURFACE_EQUATION


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
    package=portable_core_package()
    environment=portable_core_environment(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=True,
    )
    out=assess(package,environment)
    assert out.complete
    assert out.unresolved_symbols==()
    assert out.unavailable_primitives==()
    assert out.unsatisfied_obligations==()
    assert out.realizer_errors==()
    assert out.equivalence_errors==()
    assert surface_value(package,environment)==1
    assert SURFACE_EQUATION=="Σ=𝟙_{Δ∩Ω∩Φ∩Ξ}"


def test_show_me_the_math_fails_closed_without_semantic_reasoner():
    package=portable_core_package()
    environment=portable_core_environment(
        semantic_reasoner_available=False,
        execution_interface_available=True,
        controller_bindings_available=True,
    )
    out=assess(package,environment)
    assert not out.complete
    assert "semantic_reasoner" in out.unavailable_primitives
    assert surface_value(package,environment)==0


def test_math_preserves_frozen_controller_signature_and_capability_family():
    assert "ICC_128 = C_128(Z_t,F_128,MI_t)" in PORTABLE_MATH
    assert "Q_t = rho_128(Z_t,MI_t) subseteq F_128" in PORTABLE_MATH
    assert "Y_t = Run_128(Q_t,Z_t,MI_t)" in PORTABLE_MATH
    assert "MI_(t+1) = Sync_128(MI_t,Y_t)" in PORTABLE_MATH
    assert "Z_(t+1) = U_128(Z_t,Y_t,MI_(t+1))" in PORTABLE_MATH
    assert F128==("L","O","R_123","D_PD","G","A","M_MT","T_2","E","V")


def test_exact_take5_activation_remains_distinct_from_portable_core():
    assert not take5_activation_closed(None)
    assert not take5_activation_closed({
        "repository":"thytabakman-jpg/Take-5",
        "path":"artifacts/icc128-legacy-learning/x.json",
        "commit_sha":"abc",
        "report_sha256":"def",
    })
    assert take5_activation_closed({
        "repository":"thytabakman-jpg/Take-5",
        "path":"artifacts/icc128-legacy-learning/x.json",
        "commit_sha":"abc",
        "report_sha256":"def",
        "execution_claim_level":"VERIFIED",
        "execution_claim_evidence_sha256":"ghi",
    })


def test_show_me_the_math_fails_closed_without_higher_order_controller_bindings():
    package=portable_core_package()
    environment=portable_core_environment(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=False,
    )
    out=assess(package,environment)
    assert not out.complete
    for name in ("package_compiler","admission_binding","update_binding","discovery_closure_binding"):
        assert name in out.unavailable_primitives
    assert surface_value(package,environment)==0


def test_current_show_me_the_math_proves_exact_take5_activation_needs_report_sink():
    package=exact_take5_activation_package()
    no_sink=exact_take5_activation_environment(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=True,
        github_report_sink_available=False,
    )
    out=assess(package,no_sink)
    assert not out.complete
    assert "github_report_commit_receipt" in out.unavailable_primitives
    assert surface_value(package,no_sink)==0

    with_sink=exact_take5_activation_environment(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=True,
        github_report_sink_available=True,
    )
    still_open=assess(package,with_sink)
    assert not still_open.complete
    assert "execution_claim_receipt" in still_open.unavailable_primitives

    with_sink_and_attestor=exact_take5_activation_environment(
        semantic_reasoner_available=True,
        execution_interface_available=True,
        controller_bindings_available=True,
        github_report_sink_available=True,
        execution_claim_attestor_available=True,
    )
    closed=assess(package,with_sink_and_attestor)
    assert closed.complete
    assert surface_value(package,with_sink)==1
