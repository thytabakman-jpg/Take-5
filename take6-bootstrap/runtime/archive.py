"""Minimal Take-6 immutable content-addressed evidence store."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

def _canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def cid_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()

def cid_json(value: Any) -> str:
    return cid_bytes(_canon(value))

@dataclass(frozen=True)
class StoredObject:
    cid: str
    path: Path
    size: int

class Vault:
    def __init__(self, root: Path | str):
        self.root = Path(root)

    def _path(self, cid: str) -> Path:
        algo, digest = cid.split(":", 1)
        if algo != "sha256" or len(digest) != 64:
            raise ValueError("TAKE6_INVALID_CID")
        return self.root / "objects" / algo / digest[:2] / digest

    def put_bytes(self, data: bytes) -> StoredObject:
        cid = cid_bytes(data)
        path = self._path(cid)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            existing = path.read_bytes()
            if existing != data:
                raise RuntimeError("TAKE6_CONTENT_ADDRESS_COLLISION")
        else:
            path.write_bytes(data)
        return StoredObject(cid=cid, path=path, size=len(data))

    def put_json(self, value: Any) -> StoredObject:
        return self.put_bytes(_canon(value))

    def get_bytes(self, cid: str) -> bytes:
        path = self._path(cid)
        data = path.read_bytes()
        if cid_bytes(data) != cid:
            raise RuntimeError("TAKE6_VAULT_INTEGRITY_FAILURE")
        return data

    def has(self, cid: str) -> bool:
        path = self._path(cid)
        return path.is_file() and cid_bytes(path.read_bytes()) == cid

def append_event(ledger_root: Path | str, event_without_id: dict[str, Any]) -> dict[str, Any]:
    root = Path(ledger_root)
    body = dict(event_without_id)
    body.pop("event_id", None)
    event_id = cid_json(body)
    event = {"event_id": event_id, **body}
    path = root / "events" / (event_id.split(":", 1)[1] + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(event, indent=2, sort_keys=True) + "\n"
    if path.exists():
        prior = json.loads(path.read_text(encoding="utf-8"))
        if prior != event:
            raise RuntimeError("TAKE6_EVENT_IMMUTABILITY_FAILURE")
    else:
        path.write_text(encoded, encoding="utf-8")
    return event
