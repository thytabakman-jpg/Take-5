"""Exact-byte ingestion of frozen predecessor repository snapshots into Take-6 vault.

This module performs no semantic admission. It verifies Git blob identity against the
frozen inventories, stores exact bytes under SHA-256 CIDs, preserves one provenance
record per source path, and emits a corpus checkpoint/manifest.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
from typing import Any, Iterable, Mapping

from runtime.archive import Vault, cid_json
from runtime.checkpoint import make_checkpoint, verify_checkpoint
from runtime.source_frontier import (
    compile_source_frontier,
    load_source_snapshots,
    verify_inventory,
)


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def _read_worktree_blob(path: Path, mode: str) -> bytes:
    if mode == "120000":
        if not path.is_symlink():
            raise RuntimeError("TAKE6_INGEST_EXPECTED_SYMLINK:" + str(path))
        return os.readlink(path).encode("utf-8")
    if not path.is_file():
        raise RuntimeError("TAKE6_INGEST_FILE_MISSING:" + str(path))
    return path.read_bytes()


def _media_type(path: str) -> str:
    guessed, _ = mimetypes.guess_type(path)
    return guessed or "application/octet-stream"


@dataclass(frozen=True)
class RepositoryIngestReceipt:
    repository: str
    commit: str
    tree_sha: str
    inventory: str
    blobs_expected: int
    blobs_ingested: int
    unique_payloads: int
    total_bytes: int


def ingest_repository_snapshot(
    *,
    snapshot: Mapping[str, Any],
    inventory: Mapping[str, Any],
    checkout_root: Path | str,
    vault: Vault,
) -> tuple[RepositoryIngestReceipt, list[dict[str, Any]]]:
    verify_inventory(snapshot, inventory)
    root = Path(checkout_root)
    records: list[dict[str, Any]] = []
    seen_payloads: set[str] = set()
    total_bytes = 0

    entries = inventory.get("entries", ())
    if not isinstance(entries, list):
        raise RuntimeError("TAKE6_INGEST_INVENTORY_ENTRIES_INVALID")

    for entry in entries:
        if not isinstance(entry, Mapping) or entry.get("type") != "blob":
            continue
        rel = str(entry.get("path", ""))
        mode = str(entry.get("mode", ""))
        expected_git_sha = str(entry.get("sha", ""))
        data = _read_worktree_blob(root / rel, mode)

        observed_git_sha = git_blob_sha1(data)
        if observed_git_sha != expected_git_sha:
            raise RuntimeError(
                "TAKE6_INGEST_GIT_BLOB_MISMATCH:"
                + str(snapshot["repository"])
                + ":"
                + rel
                + ":"
                + expected_git_sha
                + ":"
                + observed_git_sha
            )

        stored = vault.put_bytes(data)
        seen_payloads.add(stored.cid)
        total_bytes += stored.size

        source = {
            "kind": "GIT",
            "locator": (
                str(snapshot["repository"])
                + "@"
                + str(snapshot["commit"])
                + ":"
                + rel
            ),
            "repository": str(snapshot["repository"]),
            "ref": str(snapshot["commit"]),
            "original_path": rel,
            "git_blob_sha": expected_git_sha,
            "git_mode": mode,
            "tree_sha": str(snapshot["tree_sha"]),
        }
        record = {
            "artifact_id": (
                "git:"
                + str(snapshot["repository"])
                + "@"
                + str(snapshot["commit"])
                + ":"
                + rel
            ),
            "payload_cid": stored.cid,
            "byte_count": stored.size,
            "media_type": _media_type(rel),
            "source": source,
            "ingestion_disposition": "INGESTED",
            "extracted_cids": [],
            "duplicate_payload_of": None,
        }
        records.append(record)

    expected = int(inventory.get("blob_count", -1))
    if len(records) != expected:
        raise RuntimeError(
            "TAKE6_INGEST_BLOB_COUNT_MISMATCH:"
            + str(snapshot["repository"])
            + ":"
            + str(expected)
            + ":"
            + str(len(records))
        )

    receipt = RepositoryIngestReceipt(
        repository=str(snapshot["repository"]),
        commit=str(snapshot["commit"]),
        tree_sha=str(snapshot["tree_sha"]),
        inventory=str(snapshot.get("inventory", "")),
        blobs_expected=expected,
        blobs_ingested=len(records),
        unique_payloads=len(seen_payloads),
        total_bytes=total_bytes,
    )
    return receipt, records


def _inventory_loader(bootstrap_root: Path):
    def load(path: str) -> dict[str, Any]:
        return json.loads((bootstrap_root / path).read_text(encoding="utf-8"))
    return load


def _current_snapshot_map(
    snapshots: Iterable[Mapping[str, Any]],
    compiled: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    by_key = {
        (str(x["repository"]), str(x["commit"])): dict(x)
        for x in snapshots
    }
    out: dict[str, dict[str, Any]] = {}
    for repo, row in compiled.get("repositories", {}).items():
        if row.get("status") != "CURRENT":
            raise RuntimeError("TAKE6_INGEST_SOURCE_FRONTIER_NOT_CURRENT:" + repo)
        commit = str(row.get("current_commit", ""))
        key = (str(repo), commit)
        if key not in by_key:
            raise RuntimeError("TAKE6_INGEST_CURRENT_SNAPSHOT_MISSING:" + repo)
        out[str(repo)] = by_key[key]
    return out


def ingest_current_repository_frontier(
    *,
    bootstrap_root: Path | str,
    input_root: Path | str,
    output_root: Path | str,
) -> dict[str, Any]:
    bootstrap = Path(bootstrap_root)
    inputs = Path(input_root)
    output = Path(output_root)
    output.mkdir(parents=True, exist_ok=True)

    snapshot_root = bootstrap / "migration" / "source_snapshots"
    snapshots = load_source_snapshots(snapshot_root)
    loader = _inventory_loader(bootstrap)
    compiled = compile_source_frontier(
        snapshots,
        inventory_loader=loader,
    )
    current = _current_snapshot_map(snapshots, compiled)

    vault = Vault(output / "vault")
    all_records: list[dict[str, Any]] = []
    receipts: list[RepositoryIngestReceipt] = []

    for repository in sorted(current):
        snapshot = current[repository]
        inventory = loader(str(snapshot["inventory"]))
        checkout = inputs / repository.rsplit("/", 1)[-1]
        receipt, records = ingest_repository_snapshot(
            snapshot=snapshot,
            inventory=inventory,
            checkout_root=checkout,
            vault=vault,
        )
        receipts.append(receipt)
        all_records.extend(records)

    all_records.sort(key=lambda x: x["artifact_id"])
    object_cids = sorted({str(x["payload_cid"]) for x in all_records})
    checkpoint = make_checkpoint(
        object_cids=object_cids,
        event_ids=(),
        prior_checkpoint_cid=None,
    )
    verify_checkpoint(
        checkpoint,
        has_object=vault.has,
        has_event=lambda _: False,
    )

    records_path = output / "artifact-records.jsonl"
    records_path.write_text(
        "".join(json.dumps(x, sort_keys=True) + "\n" for x in all_records),
        encoding="utf-8",
    )

    manifest_body = {
        "schema_version": "0.1",
        "source_frontier_cid": compiled["source_frontier_cid"],
        "repositories": [asdict(x) for x in receipts],
        "artifact_records": len(all_records),
        "unique_payload_cids": len(object_cids),
        "total_bytes": sum(x.total_bytes for x in receipts),
        "checkpoint": checkpoint,
        "artifact_records_sha256": hashlib.sha256(
            records_path.read_bytes()
        ).hexdigest(),
    }
    manifest = {
        "manifest_cid": cid_json(manifest_body),
        **manifest_body,
    }
    (output / "corpus-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output / "checkpoint.json").write_text(
        json.dumps(checkpoint, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-root", required=True)
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    manifest = ingest_current_repository_frontier(
        bootstrap_root=args.bootstrap_root,
        input_root=args.input_root,
        output_root=args.output_root,
    )
    print(json.dumps({
        "manifest_cid": manifest["manifest_cid"],
        "source_frontier_cid": manifest["source_frontier_cid"],
        "artifact_records": manifest["artifact_records"],
        "unique_payload_cids": manifest["unique_payload_cids"],
        "total_bytes": manifest["total_bytes"],
        "checkpoint_cid": manifest["checkpoint"]["checkpoint_cid"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
