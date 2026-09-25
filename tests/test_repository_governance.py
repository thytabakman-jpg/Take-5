from pathlib import Path
import re

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
