"""Deterministic Take-6 semantic-state compiler prototype."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

def _canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def state_cid(v: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(v)).hexdigest()

@dataclass(frozen=True)
class CompiledSubject:
    subject: str
    status: str
    current_payload_cid: str | None
    maximal_payload_cids: tuple[str, ...]

def _topological(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {e["event_id"]: e for e in events}
    indeg = {eid: 0 for eid in by_id}
    kids: dict[str, list[str]] = defaultdict(list)
    for eid, event in by_id.items():
        for parent in event.get("parents", []):
            if parent in by_id:
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
    opens: dict[str, list[str]] = defaultdict(list)

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
            opens[subject].append(kind)

    subjects = sorted(set(admitted) | set(rejected) | set(supersedes) | set(opens))
    compiled: dict[str, Any] = {}

    for subject in subjects:
        candidates = set(admitted[subject]) - set(rejected[subject])
        outgoing = {old for old, new in supersedes[subject] if new in candidates}
        maxima = sorted(candidates - outgoing)
        if len(maxima) == 1:
            status = "CURRENT"
            current = maxima[0]
        elif len(maxima) > 1:
            status = "CONFLICT"
            current = None
        else:
            status = "OPEN" if opens[subject] or not candidates else "BLOCKED"
            current = None
        compiled[subject] = {
            "status": status,
            "current_payload_cid": current,
            "maximal_payload_cids": maxima,
            "typed_boundaries": sorted(opens[subject]),
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
