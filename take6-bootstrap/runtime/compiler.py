"""Deterministic Take-6 semantic-state compiler prototype."""
from __future__ import annotations

from collections import defaultdict, deque
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

def _canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def state_cid(v: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(v)).hexdigest()

def event_cid(event_without_id: dict[str, Any]) -> str:
    return state_cid(event_without_id)

def _verify_event_identity(event: dict[str, Any]) -> None:
    body = {k: v for k, v in event.items() if k != "event_id"}
    expected = event_cid(body)
    if event.get("event_id") != expected:
        raise RuntimeError("TAKE6_EVENT_IDENTITY_FAILURE:" + str(event.get("event_id")))

def _topological(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for event in events:
        _verify_event_identity(event)
    by_id = {e["event_id"]: e for e in events}
    if len(by_id) != len(events):
        raise RuntimeError("TAKE6_DUPLICATE_EVENT_ID")
    indeg = {eid: 0 for eid in by_id}
    kids: dict[str, list[str]] = defaultdict(list)
    for eid, event in by_id.items():
        for parent in event.get("parents", []):
            if parent not in by_id:
                raise RuntimeError("TAKE6_MISSING_PARENT_EVENT:" + parent)
            indeg[eid] += 1
            kids[parent].append(eid)
    q = deque(sorted(eid for eid, d in indeg.items() if d == 0))
    out: list[dict[str, Any]] = []
    while q:
        eid = q.popleft()
        out.append(by_id[eid])
        for child in sorted(kids[eid]):
            indeg[child] -= 1
            if indeg[child] == 0:
                q.append(child)
    if len(out) != len(events):
        raise RuntimeError("TAKE6_EVENT_GRAPH_CYCLE")
    return out

def compile_state(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    ordered = _topological(list(events))
    admitted: dict[str, set[str]] = defaultdict(set)
    rejected: dict[str, set[str]] = defaultdict(set)
    supersedes: dict[str, set[tuple[str, str]]] = defaultdict(set)
    boundaries: dict[str, list[str]] = defaultdict(list)

    for e in ordered:
        subject = e["subject"]
        payload = e["payload_cid"]
        kind = e["kind"]
        if kind in {"ADMIT", "PROMOTE"}:
            admitted[subject].add(payload)
        elif kind == "REJECT":
            rejected[subject].add(payload)
            admitted[subject].discard(payload)
        elif kind == "SUPERSEDE":
            admitted[subject].add(payload)
            for old in e.get("supersedes", []):
                supersedes[subject].add((old, payload))
        elif kind in {"OPEN", "BLOCK", "CONFLICT"}:
            boundaries[subject].append(kind)

    subjects = sorted(set(admitted) | set(rejected) | set(supersedes) | set(boundaries))
    compiled: dict[str, Any] = {}

    for subject in subjects:
        candidates = set(admitted[subject]) - set(rejected[subject])
        outgoing = {old for old, new in supersedes[subject] if new in candidates}
        maxima = sorted(candidates - outgoing)
        explicit = sorted(set(boundaries[subject]))

        if "CONFLICT" in explicit:
            status = "CONFLICT"
            current = None
        elif "BLOCK" in explicit:
            status = "BLOCKED"
            current = None
        elif len(maxima) == 1:
            status = "CURRENT"
            current = maxima[0]
        elif len(maxima) > 1:
            status = "CONFLICT"
            current = None
        else:
            status = "OPEN"
            current = None

        compiled[subject] = {
            "status": status,
            "current_payload_cid": current,
            "maximal_payload_cids": maxima,
            "typed_boundaries": explicit,
        }

    result = {
        "schema_version": "0.1",
        "subjects": compiled,
    }
    result["state_cid"] = state_cid(result)
    return result

def load_events(root: Path | str) -> list[dict[str, Any]]:
    paths = sorted((Path(root) / "events").glob("*.json"))
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]

def compile_to_file(ledger_root: Path | str, output: Path | str) -> dict[str, Any]:
    result = compile_state(load_events(ledger_root))
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
