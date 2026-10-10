"""Regression controls for read-only historical RootCause consultation."""
from pathlib import Path

from root_cause_knowledge_lookup import SUBJECTS, BASE, consult_root_cause_knowledge
from root_cause_managed import run_root_cause_child


def _fixture(tmp_path: Path) -> Path:
    base = tmp_path / BASE
    base.mkdir(parents=True)
    for name in SUBJECTS:
        (base / name).write_text(
            "# " + name + "\n## Bounded historical research\n"
            "No new cause is admitted merely because a document was found.\n",
            encoding="utf-8",
        )
    (base / "WORK_FRONTIER_AND_CLOSURE.md").write_text(
        "# Work frontiers and closure\n"
        "## Premature parent campaign closure\n"
        "A child repair can complete while parent campaign obligations remain OPEN. "
        "A premature parent closure requires a live obligation check. "
        "[D3](evidence/EXECUTION_AND_CLOSURE_SOURCES.md#d3)\n",
        encoding="utf-8",
    )
    (base / "EVIDENCE_STATUS_AND_TESTS.md").write_text(
        "# Evidence and tests\n"
        "## Runner failure contrasted with validator passes\n"
        "A workflow runner allocation failure occurs before steps, but a direct "
        "validator pass tests a different boundary. These remain rival explanations. "
        "[H4](evidence/CI_OBSERVATION_AND_PARENT_RETURN_FINDINGS.md#h4) "
        "[H5](evidence/CI_OBSERVATION_AND_PARENT_RETURN_FINDINGS.md#h5)\n",
        encoding="utf-8",
    )
    (base / "CAUSAL_INFERENCE_AND_ROOTNESS.md").write_text(
        "# Causal inquiry\n## Library evidence and private originals\n"
        "The G11 private Library original is a locator; historical confirmation "
        "cannot be inferred without access. "
        "[G11](evidence/LIBRARY_ROOT_CAUSE_SOURCE_REGISTER.md#g11)\n",
        encoding="utf-8",
    )
    return tmp_path


def test_real_source_style_match_stays_read_only_and_open(tmp_path):
    root = _fixture(tmp_path)
    result = consult_root_cause_knowledge(
        observed_failure=["premature parent campaign closure"], research_root=root
    )
    assert result["status"] == "CANDIDATES"
    assert result["candidates"][0]["subject"] == "WORK_FRONTIER_AND_CLOSURE.md"
    assert result["admission"] == "NOT_ADMITTED"
    assert result["candidates"][0]["source_refs"][0]["anchor"] == "d3"
    assert result["candidates"][0]["source_sha256"]
    assert result["required_next_step"].startswith("CHECK_ORIGINAL")


def test_false_friend_and_private_boundary(tmp_path):
    root = _fixture(tmp_path)
    runner = consult_root_cause_knowledge(
        observed_failure=["runner allocation failed but direct validator passed"],
        research_root=root,
    )
    assert runner["status"] == "CANDIDATES"
    assert runner["candidates"][0]["subject"] == "EVIDENCE_STATUS_AND_TESTS.md"
    assert runner["admission"] == "NOT_ADMITTED"
    assert {r["anchor"] for r in runner["candidates"][0]["source_refs"]} == {"h4", "h5"}
    private = consult_root_cause_knowledge(
        observed_failure=["private Library original access"], research_root=root
    )
    assert private["status"] == "CANDIDATES"
    matching = next(x for x in private["candidates"]
                    if x["subject"] == "CAUSAL_INFERENCE_AND_ROOTNESS.md")
    assert matching["source_refs"][0]["access"] == "PRIVATE_LIBRARY_ORIGINAL_UNVERIFIED"


def test_unknown_scope_and_no_match(tmp_path):
    root = _fixture(tmp_path)
    assert consult_root_cause_knowledge(
        observed_failure=["recipe pumpkin bread"], research_root=root
    )["status"] == "NO_MATCH"
    assert consult_root_cause_knowledge(
        observed_failure=["parent closure"], research_root=None
    )["status"] == "NO_ACCESS"
    assert consult_root_cause_knowledge(
        observed_failure=[], research_root=root
    )["status"] == "SKIPPED_NO_OBSERVATION"
    (root / BASE / SUBJECTS[0]).unlink()
    assert consult_root_cause_knowledge(
        observed_failure=["parent closure"], research_root=root
    )["status"] == "NO_ACCESS"


def test_native_root_cause_remains_independent_of_historical_candidates(tmp_path):
    root = _fixture(tmp_path)
    args = dict(
        job_id="knowledge-independent",
        child_id="rootcause",
        failure_class=["premature parent campaign closure"],
        candidates=(),
        basis_id="exact-observed-failure",
    )
    prior = run_root_cause_child(**args)
    consulted = run_root_cause_child(**args, research_root=root)
    assert "historical_knowledge" not in prior.result
    assert prior.result["local_status"] == consulted.result["local_status"] == "OPEN"
    assert prior.result["root_candidates"] == consulted.result["root_candidates"] == ()
    assert prior.result["parent_handoff"] == consulted.result["parent_handoff"]
    assert consulted.result["historical_knowledge"]["status"] == "CANDIDATES"


def test_command_interface_is_data_only_and_fails_closed(tmp_path, capsys):
    from root_cause_knowledge_lookup import main
    root = _fixture(tmp_path)
    assert main(["--research-root", str(root), "premature parent campaign closure"]) == 0
    data = capsys.readouterr().out
    assert '"status": "CANDIDATES"' in data
    assert '"admission": "NOT_ADMITTED"' in data
    assert main(["--research-root", str(root / "absent"), "parent closure"]) == 2
    assert '"status": "NO_ACCESS"' in capsys.readouterr().out


def test_verified_outcome_capture_uses_existing_ledgers_and_guardrails():
    from types import SimpleNamespace
    from root_cause_knowledge_lookup import record_verified_root_cause_outcome

    class MaterialLedger:
        def __init__(self):
            self.events = []
        def record(self, **event):
            self.events.append(event)
            return SimpleNamespace(knowledge_id="K-CHECK")

    class NegativeMemory:
        def __init__(self):
            self.events = []
        def record(self, **event):
            self.events.append(event)

    material, negative = MaterialLedger(), NegativeMemory()
    context = dict(
        owner_admitted=True,
        verification_refs=["current-effect-receipt"],
        source_episode="ep1",
        basis_id="frozen-basis",
        route_id="repair-case",
        consultation={"candidates": [{"subject": "WORK_FRONTIER_AND_CLOSURE.md"}]},
        dependency_footprint=["owner"],
    )
    assert record_verified_root_cause_outcome(
        **{**context, "owner_admitted": False}, outcome="VERIFIED_GAIN",
        knowledge_ledger=material,
    )["written"] is False
    assert record_verified_root_cause_outcome(
        **{**context, "verification_refs": []}, outcome="VERIFIED_GAIN",
        knowledge_ledger=material,
    )["written"] is False
    assert not material.events
    gain = record_verified_root_cause_outcome(
        **context, outcome="VERIFIED_GAIN", knowledge_ledger=material,
    )
    assert gain["knowledge_id"] == "K-CHECK"
    assert material.events[0]["disposition"] == "CAPTURED"
    assert material.events[0]["metadata"]["consulted_subjects"] == (
        "WORK_FRONTIER_AND_CLOSURE.md",
    )
    loss = record_verified_root_cause_outcome(
        **context, outcome="FAILED", negative_learning_memory=negative,
    )
    assert loss["status"] == "NEGATIVE_ROUTE_RECORDED"
    assert negative.events[0]["disposition"] == "FAILED"
    assert record_verified_root_cause_outcome(
        **context, outcome="OPEN", negative_learning_memory=negative,
    )["written"] is False
    assert len(material.events) == len(negative.events) == 1
