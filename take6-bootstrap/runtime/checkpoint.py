"""Archive completeness checkpoints for Take-6."""
from __future__ import annotations
import hashlib
import json
from typing import Any, Callable, Iterable

def _canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def cid(v: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(v)).hexdigest()

def make_checkpoint(
    *,
    object_cids: Iterable[str],
    event_ids: Iterable[str],
    prior_checkpoint_cid: str | None,
) -> dict[str, Any]:
    body = {
        "object_cids": sorted(set(map(str, object_cids))),
        "event_ids": sorted(set(map(str, event_ids))),
        "prior_checkpoint_cid": prior_checkpoint_cid,
    }
    return {"checkpoint_cid": cid(body), **body}

def verify_checkpoint(
    checkpoint: dict[str, Any],
    *,
    has_object: Callable[[str], bool],
    has_event: Callable[[str], bool],
    has_checkpoint: Callable[[str], bool] | None = None,
) -> None:
    body = {k: v for k, v in checkpoint.items() if k != "checkpoint_cid"}
    if cid(body) != checkpoint.get("checkpoint_cid"):
        raise RuntimeError("TAKE6_CHECKPOINT_HASH_MISMATCH")
    missing_objects = [x for x in body["object_cids"] if not has_object(x)]
    missing_events = [x for x in body["event_ids"] if not has_event(x)]
    if missing_objects:
        raise RuntimeError("TAKE6_CHECKPOINT_OBJECT_LOSS:" + ",".join(missing_objects))
    if missing_events:
        raise RuntimeError("TAKE6_CHECKPOINT_EVENT_LOSS:" + ",".join(missing_events))
    prior = body.get("prior_checkpoint_cid")
    if prior and has_checkpoint is not None and not has_checkpoint(prior):
        raise RuntimeError("TAKE6_CHECKPOINT_CHAIN_LOSS:" + prior)
