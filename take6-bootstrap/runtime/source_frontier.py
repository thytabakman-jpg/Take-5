"""Compiled migration-source frontier for the Take-6 bootstrap.

A source snapshot is immutable evidence. Current migration frontier is derived from
explicit supersession among snapshots; no hand-authored CURRENT source pointer is
authoritative.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


def _canon(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def cid(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(value)).hexdigest()


def load_source_snapshots(root: Path | str) -> list[dict[str, Any]]:
    paths = sorted(Path(root).glob("*.json"))
    out: list[dict[str, Any]] = []
    for path in paths:
        raw = json.loads(path.read_text(encoding="utf-8"))
        records = raw.get("snapshots", raw if isinstance(raw, list) else ())
        if not isinstance(records, list):
            raise RuntimeError("TAKE6_SOURCE_SNAPSHOT_FILE_INVALID:" + str(path))
        for row in records:
            if not isinstance(row, Mapping):
                raise RuntimeError("TAKE6_SOURCE_SNAPSHOT_RECORD_INVALID:" + str(path))
            out.append(dict(row))
    return out


def _validate_snapshot(row: Mapping[str, Any]) -> None:
    required = ("repository", "commit", "tree_sha")
    for key in required:
        if not str(row.get(key, "")).strip():
            raise RuntimeError("TAKE6_SOURCE_SNAPSHOT_FIELD_REQUIRED:" + key)
    if bool(row.get("recursive_tree_truncated", False)):
        raise RuntimeError(
            "TAKE6_SOURCE_SNAPSHOT_TRUNCATED:" + str(row.get("repository"))
        )
    supersedes = row.get("supersedes", ())
    if not isinstance(supersedes, list):
        raise RuntimeError("TAKE6_SOURCE_SNAPSHOT_SUPERSEDES_INVALID")


def compile_source_frontier(
    snapshots: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    rows = [dict(x) for x in snapshots]
    for row in rows:
        _validate_snapshot(row)

    by_repo: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        repo = str(row["repository"])
        commit = str(row["commit"])
        if commit in by_repo[repo]:
            prior = by_repo[repo][commit]
            if prior != row:
                raise RuntimeError(
                    "TAKE6_SOURCE_SNAPSHOT_DUPLICATE_CONFLICT:" + repo + ":" + commit
                )
            continue
        by_repo[repo][commit] = row

    compiled: dict[str, Any] = {}
    for repo in sorted(by_repo):
        records = by_repo[repo]
        superseded: set[str] = set()
        for commit, row in records.items():
            for old in row.get("supersedes", ()):
                old = str(old)
                if old not in records:
                    raise RuntimeError(
                        "TAKE6_SOURCE_SNAPSHOT_UNKNOWN_SUPERSEDED:"
                        + repo + ":" + old
                    )
                if old == commit:
                    raise RuntimeError(
                        "TAKE6_SOURCE_SNAPSHOT_SELF_SUPERSESSION:"
                        + repo + ":" + commit
                    )
                superseded.add(old)

        maxima = sorted(set(records) - superseded)
        if len(maxima) == 1:
            status = "CURRENT"
            current_commit = maxima[0]
            current = records[current_commit]
            current_tree_sha = str(current["tree_sha"])
            current_inventory = current.get("inventory")
        elif len(maxima) > 1:
            status = "CONFLICT"
            current_commit = None
            current_tree_sha = None
            current_inventory = None
        else:
            status = "OPEN"
            current_commit = None
            current_tree_sha = None
            current_inventory = None

        compiled[repo] = {
            "status": status,
            "current_commit": current_commit,
            "current_tree_sha": current_tree_sha,
            "current_inventory": current_inventory,
            "maximal_commits": maxima,
            "known_commits": sorted(records),
        }

    result = {
        "schema_version": "0.1",
        "repositories": compiled,
    }
    result["source_frontier_cid"] = cid(result)
    return result


def verify_inventory(
    snapshot: Mapping[str, Any],
    inventory: Mapping[str, Any],
) -> None:
    _validate_snapshot(snapshot)
    checks = (
        ("source_repository", "repository"),
        ("source_commit", "commit"),
        ("source_tree_sha", "tree_sha"),
    )
    for inv_key, snap_key in checks:
        if str(inventory.get(inv_key, "")) != str(snapshot.get(snap_key, "")):
            raise RuntimeError(
                "TAKE6_SOURCE_INVENTORY_MISMATCH:" + inv_key
            )
    if bool(inventory.get("recursive_tree_truncated", False)):
        raise RuntimeError("TAKE6_SOURCE_INVENTORY_TRUNCATED")
    expected_entries = snapshot.get("entry_count")
    expected_blobs = snapshot.get("blob_count")
    if expected_entries is not None and int(inventory.get("entry_count", -1)) != int(expected_entries):
        raise RuntimeError("TAKE6_SOURCE_INVENTORY_ENTRY_COUNT_MISMATCH")
    if expected_blobs is not None and int(inventory.get("blob_count", -1)) != int(expected_blobs):
        raise RuntimeError("TAKE6_SOURCE_INVENTORY_BLOB_COUNT_MISMATCH")


def frontier_matches_observed_authority(
    compiled: Mapping[str, Any],
    *,
    repository: str,
    observed_commit: str,
    observed_tree_sha: str,
) -> bool:
    row = compiled.get("repositories", {}).get(repository, {})
    return bool(
        row.get("status") == "CURRENT"
        and row.get("current_commit") == observed_commit
        and row.get("current_tree_sha") == observed_tree_sha
    )


def require_promotion_frontier_match(
    compiled: Mapping[str, Any],
    *,
    observed: Mapping[str, Mapping[str, str]],
) -> None:
    for repository, actual in sorted(observed.items()):
        if not frontier_matches_observed_authority(
            compiled,
            repository=repository,
            observed_commit=str(actual.get("commit", "")),
            observed_tree_sha=str(actual.get("tree_sha", "")),
        ):
            raise RuntimeError(
                "TAKE6_PROMOTION_SOURCE_FRONTIER_LAG:" + repository
            )
