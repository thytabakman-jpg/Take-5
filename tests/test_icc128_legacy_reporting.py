import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

import icc128_legacy
import icc128_legacy_reporting as reporting


def sample_result():
    return {
        "status": "COMPLETE",
        "state": {"terminal": "COMPLETE", "resolved": ["q1"]},
        "memory": {"learned": ["distinction-A"]},
        "traces": [{
            "iteration": 0,
            "questions": [{"question_id": "q1", "question": "Which model fits?"}],
            "work": [{"work_id": "w1", "question_id": "q1", "probe_or_test": "compare"}],
            "selected": [{"work_id": "w1"}],
            "results": [{"result": "A separates B"}],
            "admitted_delta": {"new_distinction": "A/B"},
            "memory_after": {"learned": ["distinction-A"]},
            "state_after": {"terminal": "COMPLETE", "resolved": ["q1"]},
            "terminal": "COMPLETE",
        }],
    }


def test_activation_marks_reporting_required():
    active = icc128_legacy.activate()
    assert active["reporting_required"] is True
    assert active["learning_persistence"] == "REPORT_ONLY_EPHEMERAL_CONTROLLER_MEMORY"
    assert active["reporting"] is reporting


def test_material_learning_report_captures_full_trace_and_ephemeral_memory():
    report = reporting.build_learning_report(
        run_id="legacy-run-001",
        run_result=sample_result(),
        initial_state={"terminal": "CONTINUE"},
        initial_memory={},
    )
    assert report["learning_status"] == "MATERIAL_LEARNING"
    assert report["admitted_deltas"] == [{"new_distinction": "A/B"}]
    assert report["final_ephemeral_memory"] == {"learned": ["distinction-A"]}
    assert report["iteration_learning"][0]["questions_generated"][0]["question_id"] == "q1"
    assert report["ephemeral_memory_disposition"] == "DISCARD_AFTER_REPORT_SUBMISSION"


def test_no_learning_run_still_requires_report():
    report = reporting.build_learning_report(
        run_id="legacy-run-002",
        run_result={"status": "OPEN", "state": {}, "memory": {}, "traces": []},
        initial_state={},
        initial_memory={},
    )
    assert report["learning_status"] == "NO_MATERIAL_LEARNING"
    assert report["report_required_even_when_no_material_learning"] is True


def test_failed_run_still_reports():
    report = reporting.build_learning_report(
        run_id="legacy-run-003",
        run_result=None,
        initial_state={"terminal": "CONTINUE"},
        initial_memory={},
        failure="example failure",
    )
    assert report["learning_status"] == "RUN_FAILED"
    assert report["failure"] == "example failure"


def test_github_receipt_is_required_for_closure():
    report = reporting.build_learning_report(
        run_id="legacy-run-004",
        run_result=sample_result(),
    )
    sha = reporting.report_sha256(report)
    receipt = reporting.require_github_receipt(
        run_id="legacy-run-004",
        report_sha256=sha,
        repository="thytabakman-jpg/Take-5",
        path="artifacts/icc128-legacy-learning/legacy-run-004.json",
        commit_sha="abc123",
    )
    # Persistence is necessary but no longer sufficient for a run-closure claim.
    assert reporting.closure_allowed(receipt) is False
    assert reporting.closure_allowed(None) is False


def test_wrong_report_destination_fails_closed():
    report = reporting.build_learning_report(
        run_id="legacy-run-005",
        run_result=sample_result(),
    )
    with pytest.raises(reporting.ICC128LegacyReportingError):
        reporting.require_github_receipt(
            run_id="legacy-run-005",
            report_sha256=reporting.report_sha256(report),
            repository="thytabakman-jpg/Reaserch",
            path="artifacts/icc128-legacy-learning/legacy-run-005.json",
            commit_sha="abc123",
        )



def test_attested_runtime_report_and_github_receipt_close_legacy_run():
    calls=[]
    def controller_run(state,memory):
        calls.append((dict(state),dict(memory)))
        return sample_result()

    run_result,report,execution_receipt=reporting.run_and_build_attested_learning_report(
        run_id="legacy-run-attested",
        controller_run=controller_run,
        initial_state={"terminal":"CONTINUE"},
        initial_memory={},
        plan_evidence="test:configured-legacy-plan",
    )
    assert calls==[({"terminal":"CONTINUE"}, {})]
    assert run_result["status"]=="COMPLETE"
    assert report["execution_claim_status"]=="VERIFIED"
    assert report["execution_claim"]["claimed_level"]=="CONSUMED"

    attested=reporting.require_attested_github_receipt(
        report=report,
        execution_receipt=execution_receipt,
        repository="thytabakman-jpg/Take-5",
        path="artifacts/icc128-legacy-learning/legacy-run-attested.json",
        commit_sha="abc123",
    )
    assert attested.execution_receipt.level().value=="VERIFIED"
    assert reporting.attested_closure_allowed(attested) is True
    assert reporting.closure_allowed(attested) is True
