"""Fail-closed learning-report boundary for ICC128 Legacy.

The frozen legacy controller may adapt within a run. Its learned state is not
carried into the next run. Instead, every run emits a complete report object.
Repository/host code must persist that report to GitHub and provide a commit
receipt before the run is considered closed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from pathlib import PurePosixPath
from typing import Any
import copy
import hashlib
import json

REPORT_REPOSITORY = "thytabakman-jpg/Take-5"
REPORT_DIRECTORY = "artifacts/icc128-legacy-learning"
SOURCE_COMMIT = "e4c76c595b44a35fd9efc02cde8979e656ef54e8"


class ICC128LegacyReportingError(RuntimeError):
    pass


@dataclass(frozen=True)
class LearningReportReceipt:
    run_id: str
    repository: str
    path: str
    commit_sha: str
    report_sha256: str


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, set):
        return sorted(_jsonable(v) for v in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def _extract_trace_learning(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for trace in traces:
        out.append({
            "iteration": trace.get("iteration"),
            "questions_generated": _jsonable(trace.get("questions", [])),
            "work_generated": _jsonable(trace.get("work", [])),
            "selected_work": _jsonable(trace.get("selected", [])),
            "results_observed": _jsonable(trace.get("results", [])),
            "admitted_delta": _jsonable(trace.get("admitted_delta", {})),
            "memory_after": _jsonable(trace.get("memory_after", {})),
            "state_after": _jsonable(trace.get("state_after", {})),
            "terminal": trace.get("terminal"),
        })
    return out


def build_learning_report(
    *,
    run_id: str,
    run_result: dict[str, Any] | None,
    initial_state: dict[str, Any] | None = None,
    initial_memory: dict[str, Any] | None = None,
    failure: str | None = None,
) -> dict[str, Any]:
    if not str(run_id).strip():
        raise ICC128LegacyReportingError("ICC128_LEGACY_RUN_ID_REQUIRED")

    initial_state = copy.deepcopy(initial_state or {})
    initial_memory = copy.deepcopy(initial_memory or {})
    result = copy.deepcopy(run_result or {})
    traces = _jsonable(result.get("traces", []))
    if not isinstance(traces, list):
        traces = []

    final_memory = _jsonable(result.get("memory", {}))
    final_state = _jsonable(result.get("state", {}))
    trace_learning = _extract_trace_learning(traces)

    admitted_deltas = [
        item["admitted_delta"] for item in trace_learning
        if item.get("admitted_delta")
    ]
    memory_changed = final_memory != _jsonable(initial_memory)
    state_changed = final_state != _jsonable(initial_state)
    material_learning = bool(admitted_deltas or memory_changed)

    if failure:
        learning_status = "RUN_FAILED"
    elif material_learning:
        learning_status = "MATERIAL_LEARNING"
    else:
        learning_status = "NO_MATERIAL_LEARNING"

    return {
        "schema_version": 1,
        "object_id": "TAKE5:ICC128-LEGACY-LEARNING-REPORT:001",
        "tool": "ICC128 Legacy",
        "run_id": str(run_id),
        "source_repository": "thytabakman-jpg/Reaserch",
        "source_commit": SOURCE_COMMIT,
        "learning_persistence": "REPORT_ONLY_EPHEMERAL_CONTROLLER_MEMORY",
        "learning_status": learning_status,
        "run_status": result.get("status", "FAILED" if failure else "UNKNOWN"),
        "failure": failure,
        "initial_state": _jsonable(initial_state),
        "initial_memory": _jsonable(initial_memory),
        "iteration_learning": trace_learning,
        "admitted_deltas": admitted_deltas,
        "final_state": final_state,
        "final_ephemeral_memory": final_memory,
        "memory_changed": memory_changed,
        "state_changed": state_changed,
        "ephemeral_memory_disposition": "DISCARD_AFTER_REPORT_SUBMISSION",
        "report_required_even_when_no_material_learning": True,
    }


def render_report_json(report: dict[str, Any]) -> str:
    return json.dumps(_jsonable(report), indent=2, sort_keys=True) + "\n"


def report_sha256(report: dict[str, Any]) -> str:
    return hashlib.sha256(render_report_json(report).encode("utf-8")).hexdigest()


def report_path(run_id: str) -> str:
    clean = "".join(c if c.isalnum() or c in "-_." else "_" for c in str(run_id))
    if not clean:
        raise ICC128LegacyReportingError("ICC128_LEGACY_RUN_ID_REQUIRED")
    return str(PurePosixPath(REPORT_DIRECTORY) / f"{clean}.json")


def require_github_receipt(
    *,
    run_id: str,
    report_sha256: str,
    repository: str,
    path: str,
    commit_sha: str,
) -> LearningReportReceipt:
    expected_path = report_path(run_id)
    if repository != REPORT_REPOSITORY:
        raise ICC128LegacyReportingError("ICC128_LEGACY_REPORT_WRONG_REPOSITORY")
    if path != expected_path:
        raise ICC128LegacyReportingError("ICC128_LEGACY_REPORT_WRONG_PATH")
    if not str(commit_sha).strip():
        raise ICC128LegacyReportingError("ICC128_LEGACY_REPORT_COMMIT_RECEIPT_REQUIRED")
    if not str(report_sha256).strip():
        raise ICC128LegacyReportingError("ICC128_LEGACY_REPORT_HASH_REQUIRED")
    return LearningReportReceipt(
        run_id=str(run_id),
        repository=repository,
        path=path,
        commit_sha=commit_sha,
        report_sha256=report_sha256,
    )


def closure_allowed(receipt: LearningReportReceipt | None) -> bool:
    return receipt is not None and bool(receipt.commit_sha and receipt.report_sha256)
