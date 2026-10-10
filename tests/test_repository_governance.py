from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "a5-tests.yml"


def test_governance_files_exist():
    required = [
        ROOT / ".gitignore",
        ROOT / ".github" / "CODEOWNERS",
        ROOT / ".github" / "dependabot.yml",
        ROOT / ".github" / "pull_request_template.md",
        ROOT / "GITHUB_GOVERNANCE.md",
        ROOT / "SECURITY.md",
        ROOT / "requirements-dev.txt",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    assert not missing, f"missing governance files: {missing}"


def test_canonical_repository_is_take5():
    migration = (ROOT / "MIGRATION_STATE.yaml").read_text()
    assert "current_repository: thytabakman-jpg/Take-5" in migration
    assert "new_work_entry: Take-5" in migration
    assert "disposition: preserved_intact_read_only_rollback_and_provenance" in migration


def _checked_migration_drift_fields(text):
    """Read the flat drift-control mapping, rejecting hidden or repeated keys.

    This guards the present scalar structure; it is not a general YAML parser
    or a substitute for a real runtime migration-authority consumer.
    """
    lines = text.splitlines()
    assert lines.count("drift_control:") == 1
    start = lines.index("drift_control:") + 1
    fields = {}
    for line in lines[start:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            break
        assert line.startswith("  ") and not line.startswith("   "), line
        key, separator, value = line[2:].partition(": ")
        assert separator and re.fullmatch(r"[a-z][a-z0-9_]*", key), line
        assert key not in fields, f"duplicate drift control key: {key}"
        assert value.strip() and r"\n" not in value, line
        fields[key] = value
    assert fields["transfer_rule"] == (
        "exact_source_plus_target_effect_plus_validation_before_admission"
    )
    assert fields["future_reopen_rule"] == (
        "only_new_material_post_cutover_evidence_reopens_its_affected_cone"
    )
    assert fields["authority_rule"] == (
        "post_cutover_legacy_writes_do_not_regain_canonical_authority"
    )
    return fields


def test_migration_drift_control_has_separate_usable_fields():
    migration = (ROOT / "MIGRATION_STATE.yaml").read_text()
    fields = _checked_migration_drift_fields(migration)
    assert fields["detected"] == "true"
    assert fields["status"] == "RECONCILED_DECLARED_DRIFT_SET"


@pytest.mark.parametrize(
    "defect",
    ("fused_key", "duplicate_key", "nested_key", "missing_key"),
)
def test_migration_drift_control_rejects_original_and_structural_regressions(defect):
    original = (ROOT / "MIGRATION_STATE.yaml").read_text()
    future = "  future_reopen_rule: only_new_material_post_cutover_evidence_reopens_its_affected_cone"
    assert original.count(future) == 1
    if defect == "fused_key":
        bad = original.replace("\n" + future, r"\n" + future)
    elif defect == "duplicate_key":
        bad = original.replace(future, future + "\n" + future)
    elif defect == "nested_key":
        bad = original.replace(future, "  " + future)
    else:
        bad = original.replace("\n" + future, "")
    with pytest.raises((AssertionError, KeyError)):
        _checked_migration_drift_fields(bad)


def test_readme_navigation_exposes_active_kernel_math_before_review_only_ancestor():
    readme = (ROOT / "README.md").read_text()
    current = "architecture/KERNEL_MATH_CONTRACT_053.yaml"
    historical = "architecture/KERNEL_MATH_CONTRACT_052.yaml"
    assert readme.count(current) == 1
    assert readme.index(current) < readme.index(historical)
    assert (ROOT / current).is_file()
    assert (ROOT / historical).is_file()

    assert "## Contents" in readme
    for target in ("icc", "start-here", "authority-rule", "current-architecture",
                   "github-operating-boundary"):
        assert f"](#{target})" in readme
    start = readme.split("## Start here\n", 1)[1].split("\n## ", 1)[0]
    first_two = [line for line in start.splitlines() if line.startswith("1. ")][:2]
    assert "`MIGRATION_STATE.yaml`" in first_two[0]
    assert "`GITHUB_GOVERNANCE.md`" in first_two[1]

    targets = set(re.findall(
        r"`((?:architecture|integration|runtime|projects|validation|tests)/"
        r"[A-Za-z0-9_./-]*|MIGRATION_STATE\.yaml|GITHUB_GOVERNANCE\.md)`",
        readme,
    ))
    assert targets
    for target in targets:
        assert (ROOT / target).exists(), f"README points to absent target: {target}"


def test_successor_charter_keeps_founding_goal_and_labels_historical_authority():
    charter = (ROOT / "SUCCESSOR_CHARTER.md").read_text()
    assert "**Document goal:**" in charter
    assert "## Governing goal" in charter
    assert "Create a system that can accept a governing research goal" in charter
    assert "## Authority at founding (historical)" in charter
    assert "## Architecture status at founding (historical)" in charter
    for source in ("MIGRATION_STATE.yaml", "KERNEL.yaml"):
        assert f"]({source})" in charter
        assert (ROOT / source).is_file()



def test_workflow_has_explicit_read_permissions():
    text = WORKFLOW.read_text()
    prefix = text.split("\njobs:", 1)[0]
    assert re.search(r"(?m)^permissions:\s*\n\s+contents:\s+read\s*$", prefix)


def test_external_actions_are_immutable_sha_pinned():
    text = WORKFLOW.read_text()
    uses = re.findall(r"(?m)^\s*-\s+uses:\s+([^\s#]+)", text)
    assert uses
    for spec in uses:
        if spec.startswith("./") or spec.startswith("docker://"):
            continue
        assert "@" in spec, spec
        revision = spec.rsplit("@", 1)[1]
        assert re.fullmatch(r"[0-9a-f]{40}", revision), spec


def test_no_privileged_pull_request_target():
    assert "pull_request_target" not in WORKFLOW.read_text()


def test_dev_dependencies_are_exactly_pinned():
    lines = [
        line.strip()
        for line in (ROOT / "requirements-dev.txt").read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert lines
    assert all("==" in line for line in lines)


def test_load_bearing_control_paths_trigger_validation():
    text = WORKFLOW.read_text()
    for required in [
        "KERNEL.yaml",
        "MIGRATION_STATE.yaml",
        "architecture/**",
        "integration/**",
        "migration/**",
        "runtime/**",
        "tests/**",
    ]:
        assert required in text


def test_workflow_has_no_scheduled_loop():
    assert re.search(r"(?m)^\s*schedule\s*:", WORKFLOW.read_text()) is None
