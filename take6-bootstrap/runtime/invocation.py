"""Exact invocation-capsule construction and validation for Take-6."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Callable

def _canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def cid(v: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(v)).hexdigest()

def make_invocation_capsule(
    *,
    kernel_cid: str,
    state_cid: str,
    tool_cid: str,
    input_cids: list[str],
    basis_cid: str,
    environment_cid: str,
) -> dict[str, Any]:
    body = {
        "kernel_cid": kernel_cid,
        "state_cid": state_cid,
        "tool_cid": tool_cid,
        "input_cids": sorted(input_cids),
        "basis_cid": basis_cid,
        "environment_cid": environment_cid,
    }
    return {"invocation_cid": cid(body), **body}

def verify_invocation_capsule(
    capsule: dict[str, Any],
    *,
    has_cid: Callable[[str], bool],
) -> None:
    body = {k: v for k, v in capsule.items() if k != "invocation_cid"}
    if cid(body) != capsule.get("invocation_cid"):
        raise RuntimeError("TAKE6_INVOCATION_CAPSULE_HASH_MISMATCH")
    refs = [
        body["kernel_cid"],
        body["state_cid"],
        body["tool_cid"],
        body["basis_cid"],
        body["environment_cid"],
        *body.get("input_cids", []),
    ]
    missing = [x for x in refs if not has_cid(x)]
    if missing:
        raise RuntimeError("TAKE6_INVOCATION_MISSING_CIDS:" + ",".join(sorted(missing)))
