"""Fail-closed learning-report boundary for ICC128 Legacy.

The frozen legacy controller may adapt within a run. Its learned state is not
carried into the next run. Instead, every run emits a complete report object.
Repository/host code must persist that report to GitHub and provide a commit
receipt before the run is considered closed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path, PurePosixPath
from typing import Any
import copy
import hashlib
import json

from execution_claim_integrity import (
    ExecutionClaimLevel,
    ExecutionClaimReceipt,
    extend_execution_claim,
    require_execution_claim,
)

REPORT_REPOSITORY = "thytabakman-jpg/Take-5"
REPORT_DIRECTORY = "artifacts/icc128-legacy-learning"
SOURCE_COMMIT = "e4c76c595b44a35fd9efc02cde8979e656ef54e8"
MANIFEST = Path(__file__).resolve().parents[1] / "legacy" / "icc128-legacy" / "MANIFEST.yaml"

def _manifest_source_repository() -> str:
    in_source = False
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if raw and not raw.startswith(" "):
            in_source = raw.strip() == "source:"
            continue
        if in_source:
            stripped = raw.strip()
            if stripped.startswith("repository:"):
                return stripped.split(":", 1)[1].strip().strip('"')
    raise RuntimeError("ICC128_LEGACY_MANIFEST_SOURCE_REPOSITORY_MISSING")


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
        "source_repository": _manifest_source_repository(),
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


@dataclass(frozen=True)
class AttestedLearningReportReceipt:
    learning_receipt: LearningReportReceipt
    execution_receipt: ExecutionClaimReceipt


def _runtime_result_digest(run_result: dict[str, Any]) -> str:
    raw=json.dumps(_jsonable(run_result),sort_keys=True,separators=(",",":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def run_and_build_attested_learning_report(
    *,
    run_id: str,
    controller_run,
    initial_state: dict[str, Any],
    initial_memory: dict[str, Any],
    plan_evidence: str,
):
    """Invoke the supplied controller runtime and causally bind its result to a report.

    The function itself owns the dispatch -> execution -> consumption chain.
    A caller cannot obtain an attested report from a prewritten narrative object
    without crossing the controller_run callable here.
    """
    if not callable(controller_run):
        raise ICC128LegacyReportingError("ICC128_LEGACY_CONTROLLER_RUN_CALLABLE_REQUIRED")
    if not str(plan_evidence).strip():
        raise ICC128LegacyReportingError("ICC128_LEGACY_PLAN_EVIDENCE_REQUIRED")

    run_result=controller_run(
        copy.deepcopy(initial_state),
        copy.deepcopy(initial_memory),
    )
    if not isinstance(run_result,dict):
        raise ICC128LegacyReportingError("ICC128_LEGACY_RUNTIME_RESULT_MAPPING_REQUIRED")

    execution_digest=_runtime_result_digest(run_result)
    dispatch_ref=(
        str(getattr(controller_run,"__module__","runtime"))
        +"."+str(getattr(controller_run,"__qualname__",getattr(controller_run,"__name__","controller_run")))
    )

    execution_receipt=ExecutionClaimReceipt(
        object_id="ICC128 Legacy",
        claim_id=str(run_id),
        claimed_level=ExecutionClaimLevel.CONSUMED,
        evidence={
            "identity":f"icc128-legacy-source:{SOURCE_COMMIT}",
            "plan":str(plan_evidence),
            "dispatch":dispatch_ref,
            "execution":f"run-result-sha256:{execution_digest}",
            "consumption":"icc128_legacy_reporting.run_and_build_attested_learning_report",
        },
    )
    require_execution_claim(
        execution_receipt,
        minimum_level=ExecutionClaimLevel.CONSUMED,
    )

    report=build_learning_report(
        run_id=run_id,
        run_result=run_result,
        initial_state=initial_state,
        initial_memory=initial_memory,
    )
    report["execution_claim"]=execution_receipt.payload()
    report["execution_claim_status"]="VERIFIED"
    report["execution_result_sha256"]=execution_digest
    return run_result,report,execution_receipt


def require_attested_github_receipt(
    *,
    report: dict[str, Any],
    execution_receipt: ExecutionClaimReceipt,
    repository: str,
    path: str,
    commit_sha: str,
) -> AttestedLearningReportReceipt:
    """Upgrade a causal runtime/report receipt through persistence and verification."""
    run_id=str(report.get("run_id",""))
    expected_hash=report_sha256(report)
    learning=require_github_receipt(
        run_id=run_id,
        report_sha256=expected_hash,
        repository=repository,
        path=path,
        commit_sha=commit_sha,
    )

    persisted=extend_execution_claim(
        execution_receipt,
        claimed_level=ExecutionClaimLevel.PERSISTED,
        evidence={"persistence":f"github:{repository}@{commit_sha}:{path}"},
    )
    verified=extend_execution_claim(
        persisted,
        claimed_level=ExecutionClaimLevel.VERIFIED,
        evidence={"verification":f"report-sha256:{expected_hash}"},
    )
    require_execution_claim(verified,minimum_level=ExecutionClaimLevel.VERIFIED)
    return AttestedLearningReportReceipt(learning,verified)


def _learning_persistence_receipt_valid(receipt: LearningReportReceipt | None) -> bool:
    return receipt is not None and bool(receipt.commit_sha and receipt.report_sha256)


def attested_closure_allowed(receipt: AttestedLearningReportReceipt | None) -> bool:
    if receipt is None:
        return False
    try:
        require_execution_claim(
            receipt.execution_receipt,
            minimum_level=ExecutionClaimLevel.VERIFIED,
        )
    except Exception:
        return False
    return _learning_persistence_receipt_valid(receipt.learning_receipt)


def closure_allowed(receipt) -> bool:
    """Normal Legacy closure is now fail-closed on causal execution attestation.

    A bare GitHub learning-report receipt proves persistence only.  It no longer
    proves that the reported run actually crossed the controller runtime.
    """
    return (
        isinstance(receipt,AttestedLearningReportReceipt)
        and attested_closure_allowed(receipt)
    )
