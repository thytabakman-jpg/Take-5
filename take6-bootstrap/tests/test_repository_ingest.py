from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.archive import Vault
from runtime.repository_ingest import (
    git_blob_sha1,
    ingest_repository_snapshot,
)


def _snapshot():
    return {
        "repository": "example/repo",
        "commit": "abc1234",
        "tree_sha": "tree1234",
        "recursive_tree_truncated": False,
        "entry_count": 3,
        "blob_count": 3,
        "inventory": "inventory.json",
        "supersedes": [],
    }


def _inventory(files):
    entries = []
    for path, mode, data in files:
        entries.append({
            "path": path,
            "mode": mode,
            "type": "blob",
            "sha": git_blob_sha1(data),
            "size": len(data),
        })
    return {
        "schema_version": "0.1",
        "source_repository": "example/repo",
        "source_commit": "abc1234",
        "source_tree_sha": "tree1234",
        "recursive_tree_truncated": False,
        "entry_count": len(entries),
        "blob_count": len(entries),
        "tree_count": 0,
        "entries": entries,
    }


def test_exact_repository_ingest_preserves_bytes_and_provenance(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir()

    a = b"alpha\n"
    b = b"alpha\n"
    link_target = "a.txt"
    link_bytes = link_target.encode("utf-8")

    (checkout / "a.txt").write_bytes(a)
    (checkout / "duplicate.txt").write_bytes(b)
    os.symlink(link_target, checkout / "link.txt")

    files = [
        ("a.txt", "100644", a),
        ("duplicate.txt", "100644", b),
        ("link.txt", "120000", link_bytes),
    ]
    inventory = _inventory(files)
    snapshot = _snapshot()
    vault = Vault(tmp_path / "vault")

    receipt, records = ingest_repository_snapshot(
        snapshot=snapshot,
        inventory=inventory,
        checkout_root=checkout,
        vault=vault,
    )

    assert receipt.blobs_expected == 3
    assert receipt.blobs_ingested == 3
    assert receipt.unique_payloads == 2
    assert len(records) == 3

    by_path = {x["source"]["original_path"]: x for x in records}
    assert by_path["a.txt"]["payload_cid"] == by_path["duplicate.txt"]["payload_cid"]
    assert by_path["link.txt"]["byte_count"] == len(link_bytes)
    assert vault.get_bytes(by_path["link.txt"]["payload_cid"]) == link_bytes

    for record in records:
        assert record["source"]["repository"] == "example/repo"
        assert record["source"]["ref"] == "abc1234"
        assert record["source"]["git_blob_sha"]
        assert vault.has(record["payload_cid"])


def test_git_blob_mismatch_fails_closed(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / "a.txt").write_bytes(b"changed\n")

    inventory = _inventory([("a.txt", "100644", b"expected\n")])
    snapshot = _snapshot()
    snapshot["entry_count"] = 1
    snapshot["blob_count"] = 1
    vault = Vault(tmp_path / "vault")

    try:
        ingest_repository_snapshot(
            snapshot=snapshot,
            inventory=inventory,
            checkout_root=checkout,
            vault=vault,
        )
    except RuntimeError as exc:
        assert "INGEST_GIT_BLOB_MISMATCH" in str(exc)
    else:
        raise AssertionError("changed source bytes were ingested")


def test_missing_source_file_fails_closed(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    inventory = _inventory([("missing.txt", "100644", b"x")])
    snapshot = _snapshot()
    snapshot["entry_count"] = 1
    snapshot["blob_count"] = 1

    try:
        ingest_repository_snapshot(
            snapshot=snapshot,
            inventory=inventory,
            checkout_root=checkout,
            vault=Vault(tmp_path / "vault"),
        )
    except RuntimeError as exc:
        assert "INGEST_FILE_MISSING" in str(exc)
    else:
        raise AssertionError("missing source file was silently accepted")


def test_inventory_blob_count_mismatch_fails_closed(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    data = b"x"
    (checkout / "x.txt").write_bytes(data)
    inventory = _inventory([("x.txt", "100644", data)])
    inventory["blob_count"] = 2
    snapshot = _snapshot()
    snapshot["entry_count"] = 1
    snapshot["blob_count"] = 2

    try:
        ingest_repository_snapshot(
            snapshot=snapshot,
            inventory=inventory,
            checkout_root=checkout,
            vault=Vault(tmp_path / "vault"),
        )
    except RuntimeError as exc:
        assert "INGEST_BLOB_COUNT_MISMATCH" in str(exc)
    else:
        raise AssertionError("partial corpus passed byte-accounting closure")
