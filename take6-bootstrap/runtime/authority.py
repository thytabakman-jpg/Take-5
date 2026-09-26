"""Fail-closed authority policy for Take-6 semantic events."""
from __future__ import annotations
import hashlib
import json
from typing import Any, Mapping

def _canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def policy_cid(policy: Mapping[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canon(dict(policy))).hexdigest()

def make_authorizer(policy: Mapping[str, Any]):
    rules = dict(policy.get("rules", {}))
    def authorize(event: dict[str, Any]) -> bool:
        authority = str(event.get("authority", ""))
        kind = str(event.get("kind", ""))
        subject = str(event.get("subject", ""))
        row = rules.get(authority)
        if not isinstance(row, Mapping):
            return False
        kinds = set(str(x) for x in row.get("kinds", ()))
        prefixes = tuple(str(x) for x in row.get("subject_prefixes", ()))
        if kind not in kinds:
            return False
        if prefixes and not subject.startswith(prefixes):
            return False
        return True
    return authorize
