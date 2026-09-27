"""Generated, non-authoritative semantic views for the Take-6 bootstrap.

The authoritative chain is:
immutable evidence/events -> deterministic compiled state -> generated view.

A view never becomes an independent source of currentness.  It is a receipt-bound
projection of one exact compiled state.  CURRENT/CANONICAL/EXACT_CURRENT formal
claims receive additional dependency and composition checks.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping

from runtime.compiler import state_cid


AUTHORITATIVE_SCOPES = frozenset({
    "CURRENT",
    "CANONICAL",
    "EXACT_CURRENT",
    "CURRENT_FULL",
})

DEPENDENCY_DISPOSITIONS = frozenset({
    "CURRENT",
    "ADMITTED_FROZEN",
})


def _canon(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def cid(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(value)).hexdigest()


def _norm(value: Any) -> str:
    return str(value or "").strip().upper()


def verify_compiled_state(compiled_state: Mapping[str, Any]) -> None:
    state = dict(compiled_state)
    supplied = str(state.get("state_cid", ""))
    if not supplied:
        raise RuntimeError("TAKE6_VIEW_STATE_CID_REQUIRED")
    body = {k: v for k, v in state.items() if k != "state_cid"}
    expected = state_cid(body)
    if supplied != expected:
        raise RuntimeError("TAKE6_VIEW_COMPILED_STATE_HASH_MISMATCH")
    if not state.get("compiler_cid"):
        raise RuntimeError("TAKE6_VIEW_COMPILER_CID_REQUIRED")
    if not state.get("authority_policy_cid"):
        raise RuntimeError("TAKE6_VIEW_AUTHORITY_POLICY_CID_REQUIRED")
    if not isinstance(state.get("subjects"), Mapping):
        raise RuntimeError("TAKE6_VIEW_SUBJECTS_REQUIRED")


def _subject_row(compiled_state: Mapping[str, Any], subject: str) -> Mapping[str, Any]:
    subjects = compiled_state.get("subjects", {})
    row = subjects.get(subject) if isinstance(subjects, Mapping) else None
    if not isinstance(row, Mapping):
        raise RuntimeError("TAKE6_VIEW_SUBJECT_NOT_COMPILED:" + subject)
    return row


def _normalize_dependencies(
    dependencies: Iterable[Mapping[str, Any]],
) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for raw in dependencies:
        if not isinstance(raw, Mapping):
            raise RuntimeError("TAKE6_VIEW_DEPENDENCY_MAPPING_REQUIRED")
        subject = str(raw.get("subject", "")).strip()
        payload_cid = str(raw.get("payload_cid", "")).strip()
        disposition = _norm(raw.get("disposition"))
        admitted_by = str(
            raw.get("admitted_by_authority_policy_cid", "")
        ).strip()
        if not subject:
            raise RuntimeError("TAKE6_VIEW_DEPENDENCY_SUBJECT_REQUIRED")
        if not payload_cid:
            raise RuntimeError(
                "TAKE6_VIEW_DEPENDENCY_PAYLOAD_REQUIRED:" + subject
            )
        if disposition not in DEPENDENCY_DISPOSITIONS:
            raise RuntimeError(
                "TAKE6_VIEW_DEPENDENCY_DISPOSITION_INVALID:"
                + subject
                + ":"
                + disposition
            )
        rows.append({
            "subject": subject,
            "payload_cid": payload_cid,
            "disposition": disposition,
            "admitted_by_authority_policy_cid": admitted_by or None,
        })
    rows.sort(
        key=lambda x: (
            x["subject"],
            x["disposition"],
            x["payload_cid"],
        )
    )
    return tuple(rows)


def _verify_dependencies(
    compiled_state: Mapping[str, Any],
    dependencies: Iterable[Mapping[str, Any]],
) -> None:
    authority_policy_cid = str(compiled_state["authority_policy_cid"])
    for dep in dependencies:
        subject = str(dep["subject"])
        payload = str(dep["payload_cid"])
        disposition = _norm(dep["disposition"])
        if disposition == "CURRENT":
            row = _subject_row(compiled_state, subject)
            if _norm(row.get("status")) != "CURRENT":
                raise RuntimeError(
                    "TAKE6_VIEW_CURRENT_DEPENDENCY_NOT_CURRENT:" + subject
                )
            if str(row.get("current_payload_cid") or "") != payload:
                raise RuntimeError(
                    "TAKE6_VIEW_CURRENT_DEPENDENCY_PAYLOAD_MISMATCH:" + subject
                )
        elif disposition == "ADMITTED_FROZEN":
            admitted_by = str(
                dep.get("admitted_by_authority_policy_cid") or ""
            )
            if admitted_by != authority_policy_cid:
                raise RuntimeError(
                    "TAKE6_VIEW_FROZEN_DEPENDENCY_NOT_ADMITTED:" + subject
                )


def project_subject_view(
    compiled_state: Mapping[str, Any],
    *,
    subject: str,
    claim_scope: str = "RECOVERY",
    authoritative_formal: bool = False,
    dependencies: Iterable[Mapping[str, Any]] = (),
    dependency_closure: str = "OPEN",
    composition_typecheck: str = "OPEN",
) -> dict[str, Any]:
    """Project one subject from one exact compiled state.

    The returned object is a generated projection, never an authority source.
    When authoritative_formal=True and claim_scope is authoritative, the root
    must be CURRENT and the dependency/type closure checks must all pass.
    """
    verify_compiled_state(compiled_state)

    subject = str(subject).strip()
    if not subject:
        raise RuntimeError("TAKE6_VIEW_SUBJECT_REQUIRED")

    row = _subject_row(compiled_state, subject)
    scope = _norm(claim_scope)
    deps = _normalize_dependencies(dependencies)

    if authoritative_formal and scope in AUTHORITATIVE_SCOPES:
        if _norm(row.get("status")) != "CURRENT":
            raise RuntimeError(
                "TAKE6_VIEW_AUTHORITATIVE_ROOT_NOT_CURRENT:" + subject
            )
        if not row.get("current_payload_cid"):
            raise RuntimeError(
                "TAKE6_VIEW_AUTHORITATIVE_ROOT_PAYLOAD_REQUIRED:" + subject
            )
        if _norm(dependency_closure) != "PASS":
            raise RuntimeError(
                "TAKE6_VIEW_AUTHORITATIVE_DEPENDENCY_CLOSURE_OPEN"
            )
        if _norm(composition_typecheck) != "PASS":
            raise RuntimeError(
                "TAKE6_VIEW_AUTHORITATIVE_COMPOSITION_TYPECHECK_OPEN"
            )
        _verify_dependencies(compiled_state, deps)

    body = {
        "schema_version": "0.1",
        "projection_kind": "TAKE6_GENERATED_SUBJECT_VIEW",
        "authority": "PROJECTION_ONLY",
        "state_cid": str(compiled_state["state_cid"]),
        "compiler_cid": str(compiled_state["compiler_cid"]),
        "authority_policy_cid": str(compiled_state["authority_policy_cid"]),
        "subject": subject,
        "subject_status": str(row.get("status", "OPEN")),
        "current_payload_cid": row.get("current_payload_cid"),
        "maximal_payload_cids": list(row.get("maximal_payload_cids", ())),
        "typed_boundaries": list(row.get("typed_boundaries", ())),
        "claim_scope": scope,
        "authoritative_formal": bool(authoritative_formal),
        "dependencies": list(deps),
        "dependency_closure": _norm(dependency_closure),
        "composition_typecheck": _norm(composition_typecheck),
    }
    return {"view_cid": cid(body), **body}


def verify_subject_view(
    view: Mapping[str, Any],
    compiled_state: Mapping[str, Any],
) -> None:
    """Fail closed when a generated view is tampered with or stale."""
    verify_compiled_state(compiled_state)

    body = {k: v for k, v in dict(view).items() if k != "view_cid"}
    if cid(body) != str(view.get("view_cid", "")):
        raise RuntimeError("TAKE6_VIEW_HASH_MISMATCH")

    if str(view.get("state_cid", "")) != str(compiled_state["state_cid"]):
        raise RuntimeError("TAKE6_VIEW_STATE_STALE")

    subject = str(view.get("subject", ""))
    row = _subject_row(compiled_state, subject)
    if str(view.get("subject_status", "")) != str(row.get("status", "OPEN")):
        raise RuntimeError("TAKE6_VIEW_SUBJECT_STATUS_STALE:" + subject)
    if view.get("current_payload_cid") != row.get("current_payload_cid"):
        raise RuntimeError("TAKE6_VIEW_SUBJECT_PAYLOAD_STALE:" + subject)

    deps = tuple(
        x for x in view.get("dependencies", ())
        if isinstance(x, Mapping)
    )
    if bool(view.get("authoritative_formal")) and _norm(
        view.get("claim_scope")
    ) in AUTHORITATIVE_SCOPES:
        if _norm(view.get("dependency_closure")) != "PASS":
            raise RuntimeError(
                "TAKE6_VIEW_AUTHORITATIVE_DEPENDENCY_CLOSURE_OPEN"
            )
        if _norm(view.get("composition_typecheck")) != "PASS":
            raise RuntimeError(
                "TAKE6_VIEW_AUTHORITATIVE_COMPOSITION_TYPECHECK_OPEN"
            )
        _verify_dependencies(compiled_state, deps)


def render_human_view(view: Mapping[str, Any]) -> str:
    """Render a deterministic human-readable projection with provenance visible."""
    return (
        f"# {view['subject']}\n\n"
        f"Authority: GENERATED_PROJECTION_ONLY\n"
        f"State CID: {view['state_cid']}\n"
        f"View CID: {view['view_cid']}\n"
        f"Status: {view['subject_status']}\n"
        f"Current payload CID: {view.get('current_payload_cid')}\n"
        f"Claim scope: {view.get('claim_scope')}\n"
    )
