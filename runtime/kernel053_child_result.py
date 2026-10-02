"""Typed delegated-child result projection for Kernel 053.

A delegated controller returns evidence/delta to ICC128.  Child-local state,
selector decisions and terminality do not acquire parent-controller authority.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Iterable, Mapping


_PARENT_AUTHORITY_KEYS = frozenset({
    "state",
    "memory",
    "parent_state",
    "state_after_execution",
    "selected_work",
    "selected_works",
    "selected_tools",
    "selected_tool_ids",
    "selected_action",
    "selected_job",
    "selected_next_candidate",
    "terminal",
    "admitted_continuation",
})


def _plain(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    return value


def _sanitize(value: Any) -> Any:
    value = _plain(value)
    if isinstance(value, Mapping):
        return {
            str(k): _sanitize(v)
            for k, v in value.items()
            if str(k) not in _PARENT_AUTHORITY_KEYS
        }
    if isinstance(value, (list, tuple)):
        return tuple(_sanitize(v) for v in value)
    return value


def _execution_fields(executions: Iterable[Any]):
    evidence = []
    bindings = []
    recurrence = []
    material = False
    truths = []
    for raw in executions:
        item = _plain(raw)
        if not isinstance(item, Mapping):
            continue
        material = material or bool(item.get("material_delta", False))
        truths.append(str(item.get("execution_truth", "")))
        evidence.extend(str(x) for x in item.get("evidence", ()) if str(x))
        binding = item.get("binding")
        if binding:
            bindings.append(_sanitize(binding))
        if item.get("recurrence_engine") or item.get("recurrence_status"):
            recurrence.append({
                "engine": str(item.get("recurrence_engine", "")),
                "status": str(item.get("recurrence_status", "")),
                "rounds": int(item.get("recurrence_rounds", 0) or 0),
            })
    return material, tuple(evidence), tuple(bindings), tuple(recurrence), tuple(x for x in truths if x)


def project_child_result(
    child_id: str,
    child_result: Any,
    *,
    executions: Iterable[Any] = (),
) -> dict[str, Any]:
    raw = _plain(child_result)
    if isinstance(raw, Mapping):
        status = str(raw.get("status", "EXECUTED"))
        truth = str(raw.get("execution_truth", ""))
        result = raw.get("result", raw.get("output", raw))
        direct_evidence = tuple(str(x) for x in raw.get("evidence", ()) if str(x))
        direct_material = bool(raw.get("material_delta", False))
        changed = tuple(str(x) for x in raw.get("changed_coordinates", ()) if str(x))
    else:
        status = "EXECUTED"
        truth = "IMPLEMENTATION_EXECUTED"
        result = raw
        direct_evidence = ()
        direct_material = True
        changed = ()

    exec_material, exec_evidence, bindings, recurrence, truths = _execution_fields(executions)
    if not truth:
        truth = truths[-1] if truths else (
            status if status in {"OPEN", "BLOCKED", "CONFLICT"}
            else "IMPLEMENTATION_EXECUTED"
        )

    delta = {
        "child_id": str(child_id),
        "child_status": status,
        "execution_truth": truth,
        "child_result": _sanitize(result),
        "child_evidence": tuple(dict.fromkeys(direct_evidence + exec_evidence)),
        "configured_bindings": bindings,
        "recurrence": recurrence,
        "changed_coordinates": changed,
        "material_result_delta": bool(direct_material or exec_material),
    }
    if status == "OPEN":
        delta["new_OPEN"] = True
    elif status == "BLOCKED":
        delta["child_BLOCKED"] = True
    elif status == "CONFLICT":
        delta["child_CONFLICT"] = True
    return delta
