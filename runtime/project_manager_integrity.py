"""ProjectManager known-failure prevention envelope.

This module converts the cross-project management failure history into a
fail-closed project-control surface. It does not claim that external systems
cannot malfunction. It guarantees that a ProjectManager-managed project cannot
silently report relative closure while a known management-control class is
missing, stale, conflicted, or unsupported.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


FAILURE_CONTROL_IDS = (
    "canonical_authority",
    "state_currentness",
    "project_entry_continuity",
    "goal_scope_object",
    "adaptive_planning",
    "ownership_control",
    "execution_truth",
    "change_propagation",
    "closure_verification",
    "artifact_production",
    "research_evidence",
    "information_architecture",
    "recursive_audit_stopping",
    "cross_project_transfer",
    "concurrency_promotion",
    "human_orchestration",
    "known_holdouts",
)

ROOT_INVARIANT_IDS = (
    "representation_authority_execution_separated",
    "state_externalized_before_action",
    "mandatory_transition_path",
    "closure_scope_typed",
    "human_not_final_integration_layer",
)

CONTROL_TO_COORDINATE = {
    "canonical_authority": "authority",
    "state_currentness": "lifecycle",
    "project_entry_continuity": "handoffs",
    "goal_scope_object": "goal",
    "adaptive_planning": "changes",
    "ownership_control": "authority",
    "execution_truth": "verification",
    "change_propagation": "changes",
    "closure_verification": "verification",
    "artifact_production": "deliverables",
    "research_evidence": "evidence",
    "information_architecture": "communications",
    "recursive_audit_stopping": "changes",
    "cross_project_transfer": "handoffs",
    "concurrency_promotion": "changes",
    "human_orchestration": "communications",
    "known_holdouts": "raid",
}

ROOT_TO_COORDINATE = {
    "representation_authority_execution_separated": "authority",
    "state_externalized_before_action": "lifecycle",
    "mandatory_transition_path": "changes",
    "closure_scope_typed": "verification",
    "human_not_final_integration_layer": "communications",
}

CLOSED_STATUSES = {"CURRENT", "NOT_APPLICABLE"}
OPEN_STATUSES = {"OPEN", "BLOCKED", "STALE", "PENDING", "UNKNOWN", "UNVERIFIED"}
CONFLICT_STATUSES = {"CONFLICT"}


@dataclass(frozen=True)
class IntegrityWork:
    work_id: str
    target_coordinate: str
    target_object: str
    success: str


@dataclass(frozen=True)
class ProjectIntegrityAssessment:
    status: str
    missing_controls: tuple[str, ...]
    open_controls: tuple[str, ...]
    conflict_controls: tuple[str, ...]
    invalid_controls: tuple[str, ...]
    missing_root_invariants: tuple[str, ...]
    open_root_invariants: tuple[str, ...]
    conflict_root_invariants: tuple[str, ...]
    invalid_root_invariants: tuple[str, ...]
    evidence: tuple[str, ...]
    remediation: tuple[IntegrityWork, ...]


def _nonempty_sequence(value: Any) -> bool:
    return isinstance(value, (list, tuple, set, frozenset)) and any(
        str(x).strip() for x in value
    )


def _entry_state(entry: Any) -> tuple[str, str | None]:
    if not isinstance(entry, Mapping):
        return "INVALID", "ENTRY_MAPPING_REQUIRED"

    status = str(entry.get("status", "")).strip().upper()
    owner = str(entry.get("owner", "")).strip()
    evidence = entry.get("evidence", ())
    tests = entry.get("tests", ())
    reason = str(entry.get("reason", "")).strip()

    if status in CONFLICT_STATUSES:
        return "CONFLICT", None
    if status in OPEN_STATUSES:
        return "OPEN", None
    if status not in CLOSED_STATUSES:
        return "INVALID", "STATUS_INVALID"
    if not owner:
        return "INVALID", "OWNER_REQUIRED"
    if not _nonempty_sequence(evidence):
        return "INVALID", "EVIDENCE_REQUIRED"
    if status == "NOT_APPLICABLE":
        if not reason:
            return "INVALID", "NOT_APPLICABLE_REASON_REQUIRED"
        return "CLOSED", None
    if not _nonempty_sequence(tests):
        return "INVALID", "TEST_EVIDENCE_REQUIRED"
    return "CLOSED", None


def _remediation(
    *,
    missing_controls: tuple[str, ...],
    open_controls: tuple[str, ...],
    invalid_controls: tuple[str, ...],
    missing_roots: tuple[str, ...],
    open_roots: tuple[str, ...],
    invalid_roots: tuple[str, ...],
) -> tuple[IntegrityWork, ...]:
    work = []
    seen = set()

    for control in missing_controls + open_controls + invalid_controls:
        if control in seen:
            continue
        seen.add(control)
        work.append(
            IntegrityWork(
                work_id=f"PM-INTEGRITY-CONTROL-{control}",
                target_coordinate=CONTROL_TO_COORDINATE.get(control, "changes"),
                target_object=f"failure-control:{control}",
                success=(
                    f"{control} has one owner, typed CURRENT/NOT_APPLICABLE status, "
                    "durable evidence, and regression verification"
                ),
            )
        )

    for root in missing_roots + open_roots + invalid_roots:
        if root in seen:
            continue
        seen.add(root)
        work.append(
            IntegrityWork(
                work_id=f"PM-INTEGRITY-ROOT-{root}",
                target_coordinate=ROOT_TO_COORDINATE.get(root, "changes"),
                target_object=f"root-invariant:{root}",
                success=(
                    f"{root} is explicit, owned, evidenced, verified, and no longer OPEN"
                ),
            )
        )

    return tuple(work)


def assess_project_integrity(project: Mapping[str, Any]) -> ProjectIntegrityAssessment:
    controls_raw = project.get("failure_controls", {})
    roots_raw = project.get("root_invariants", {})
    controls = controls_raw if isinstance(controls_raw, Mapping) else {}
    roots = roots_raw if isinstance(roots_raw, Mapping) else {}

    missing_controls = tuple(x for x in FAILURE_CONTROL_IDS if x not in controls)
    missing_roots = tuple(x for x in ROOT_INVARIANT_IDS if x not in roots)

    extra_controls = tuple(sorted(set(controls) - set(FAILURE_CONTROL_IDS)))
    extra_roots = tuple(sorted(set(roots) - set(ROOT_INVARIANT_IDS)))

    open_controls = []
    conflict_controls = []
    invalid_controls = list(extra_controls)
    open_roots = []
    conflict_roots = []
    invalid_roots = list(extra_roots)
    evidence = []

    for control in FAILURE_CONTROL_IDS:
        if control not in controls:
            continue
        state, reason = _entry_state(controls[control])
        if state == "OPEN":
            open_controls.append(control)
        elif state == "CONFLICT":
            conflict_controls.append(control)
        elif state == "INVALID":
            invalid_controls.append(
                control if reason is None else f"{control}:{reason}"
            )
        else:
            entry = controls[control]
            evidence.extend(str(x) for x in entry.get("evidence", ()) if str(x).strip())

    for root in ROOT_INVARIANT_IDS:
        if root not in roots:
            continue
        state, reason = _entry_state(roots[root])
        if state == "OPEN":
            open_roots.append(root)
        elif state == "CONFLICT":
            conflict_roots.append(root)
        elif state == "INVALID":
            invalid_roots.append(root if reason is None else f"{root}:{reason}")
        else:
            entry = roots[root]
            evidence.extend(str(x) for x in entry.get("evidence", ()) if str(x).strip())

    conflict_controls_t = tuple(conflict_controls)
    conflict_roots_t = tuple(conflict_roots)
    invalid_controls_t = tuple(invalid_controls)
    invalid_roots_t = tuple(invalid_roots)
    open_controls_t = tuple(open_controls)
    open_roots_t = tuple(open_roots)

    if conflict_controls_t or conflict_roots_t:
        status = "CONFLICT"
    elif (
        missing_controls
        or missing_roots
        or open_controls_t
        or open_roots_t
        or invalid_controls_t
        or invalid_roots_t
    ):
        status = "OPEN"
    else:
        status = "CURRENT"

    remediation = _remediation(
        missing_controls=missing_controls,
        open_controls=open_controls_t,
        invalid_controls=tuple(x.split(":", 1)[0] for x in invalid_controls_t),
        missing_roots=missing_roots,
        open_roots=open_roots_t,
        invalid_roots=tuple(x.split(":", 1)[0] for x in invalid_roots_t),
    )

    return ProjectIntegrityAssessment(
        status=status,
        missing_controls=missing_controls,
        open_controls=open_controls_t,
        conflict_controls=conflict_controls_t,
        invalid_controls=invalid_controls_t,
        missing_root_invariants=missing_roots,
        open_root_invariants=open_roots_t,
        conflict_root_invariants=conflict_roots_t,
        invalid_root_invariants=invalid_roots_t,
        evidence=tuple(dict.fromkeys(evidence)),
        remediation=remediation,
    )
