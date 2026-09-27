from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.source_frontier import (
    compile_source_frontier,
    frontier_matches_observed_authority,
    load_source_snapshots,
    require_promotion_frontier_match,
    resolve_snapshot_inventory,
    verify_inventory,
)


SNAPSHOT_ROOT = ROOT / "migration" / "source_snapshots"


def _load_inventory(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _compiled_with_inventories():
    return compile_source_frontier(
        load_source_snapshots(SNAPSHOT_ROOT),
        inventory_loader=_load_inventory,
    )


def _current_take5():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    compiled = compile_source_frontier(snapshots, inventory_loader=_load_inventory)
    commit = compiled["repositories"]["thytabakman-jpg/Take-5"]["current_commit"]
    snapshot = next(
        x for x in snapshots
        if x["repository"] == "thytabakman-jpg/Take-5"
        and x["commit"] == commit
    )
    return snapshot, resolve_snapshot_inventory(snapshot, _load_inventory)


def test_repository_snapshot_history_compiles_unique_frontier():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    compiled = compile_source_frontier(snapshots, inventory_loader=_load_inventory)

    take5 = compiled["repositories"]["thytabakman-jpg/Take-5"]
    assert take5["status"] == "CURRENT"
    assert take5["current_commit"] == "ca732202c5eef65fcddea0fe73cff1999bd2f165"
    assert take5["current_tree_sha"] == "141bd97d4c64233fbc11af60ede0077dd7a66726"
    assert take5["current_scope_digest"].startswith("sha256:")
    assert take5["known_commits"] == [
        "2c2ad4de79a6a5484bc1c7631a83e342fe0b53ac",
        "4085f5d3479e6c02929026011bb377179d7f2303",
        "45ba1b8ffae50d20a96b9c3cd5904d7b120b66aa",
        "53b28a36d9998e4fe76f49b231695216fe419bdd",
        "853c7f92dae62747d3f8f42a38b6d4b77e194ad2",
        "91cc65b5379b9354036254c5dcff24d08490ae87",
        "a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2",
        "ca732202c5eef65fcddea0fe73cff1999bd2f165",
    ]

    for repo in (
        "thytabakman-jpg/Reaserch",
        "thytabakman-jpg/Take-2",
        "thytabakman-jpg/Take-3",
        "thytabakman-jpg/Take-4",
    ):
        assert compiled["repositories"][repo]["status"] == "CURRENT"


def test_take5_frontier_inventory_matches_exact_snapshot():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    current = next(
        x for x in snapshots
        if x["repository"] == "thytabakman-jpg/Take-5"
        and x["commit"] == "ca732202c5eef65fcddea0fe73cff1999bd2f165"
    )
    inventory = resolve_snapshot_inventory(current, _load_inventory)
    verify_inventory(current, inventory)
    assert inventory["entry_count"] == 934
    assert inventory["blob_count"] == 887
    assert inventory["derived_from_inventory"] == "migration/inventories/TAKE5_TREE_INVENTORY_004.json"
    assert inventory["applied_delta"] == "migration/inventory_deltas/TAKE5_TREE_DELTA_008.json"
    assert inventory["recursive_tree_truncated"] is False


def test_old_take5_cutoff_is_not_current_frontier_after_supersession():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    compiled = compile_source_frontier(snapshots)
    assert not frontier_matches_observed_authority(
        compiled,
        repository="thytabakman-jpg/Take-5",
        observed_commit="853c7f92dae62747d3f8f42a38b6d4b77e194ad2",
        observed_tree_sha="6bb206f9c22776b595e62bb3c1ab19197df0f395",
    )


def test_promotion_frontier_match_passes_for_compiled_snapshot():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    compiled = compile_source_frontier(snapshots)
    require_promotion_frontier_match(
        compiled,
        observed={
            "thytabakman-jpg/Take-5": {
                "commit": "ca732202c5eef65fcddea0fe73cff1999bd2f165",
                "tree_sha": "141bd97d4c64233fbc11af60ede0077dd7a66726",
            }
        },
    )


def test_promotion_frontier_lag_fails_closed():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    compiled = compile_source_frontier(snapshots)
    try:
        require_promotion_frontier_match(
            compiled,
            observed={
                "thytabakman-jpg/Take-5": {
                    "commit": "future-unimported-commit",
                    "tree_sha": "future-unimported-tree",
                }
            },
        )
    except RuntimeError as exc:
        assert "PROMOTION_SOURCE_FRONTIER_LAG" in str(exc)
    else:
        raise AssertionError("promotion accepted an unimported predecessor delta")


def test_incomparable_source_snapshots_compile_conflict():
    snapshots = [
        {
            "repository": "example/repo",
            "commit": "a",
            "tree_sha": "ta",
            "recursive_tree_truncated": False,
            "supersedes": [],
        },
        {
            "repository": "example/repo",
            "commit": "b",
            "tree_sha": "tb",
            "recursive_tree_truncated": False,
            "supersedes": [],
        },
    ]
    compiled = compile_source_frontier(snapshots)
    row = compiled["repositories"]["example/repo"]
    assert row["status"] == "CONFLICT"
    assert row["current_commit"] is None
    assert row["maximal_commits"] == ["a", "b"]


def test_unknown_superseded_snapshot_fails_closed():
    snapshots = [
        {
            "repository": "example/repo",
            "commit": "b",
            "tree_sha": "tb",
            "recursive_tree_truncated": False,
            "supersedes": ["a"],
        }
    ]
    try:
        compile_source_frontier(snapshots)
    except RuntimeError as exc:
        assert "UNKNOWN_SUPERSEDED" in str(exc)
    else:
        raise AssertionError("unknown predecessor source snapshot was silently accepted")


def test_truncated_snapshot_cannot_enter_frontier():
    snapshots = [
        {
            "repository": "example/repo",
            "commit": "a",
            "tree_sha": "ta",
            "recursive_tree_truncated": True,
            "supersedes": [],
        }
    ]
    try:
        compile_source_frontier(snapshots)
    except RuntimeError as exc:
        assert "SOURCE_SNAPSHOT_TRUNCATED" in str(exc)
    else:
        raise AssertionError("truncated source inventory entered migration frontier")


def test_successor_only_host_changes_do_not_stale_predecessor_frontier():
    compiled = _compiled_with_inventories()
    _, inventory = _current_take5()
    observed = json.loads(json.dumps(inventory))

    workflow = next(
        x for x in observed["entries"]
        if x["path"] == ".github/workflows/take6-bootstrap-validation.yml"
    )
    workflow["sha"] = "successor-only-workflow-change"
    observed["entries"].append({
        "path": "take6-bootstrap/future-successor-only.txt",
        "mode": "100644",
        "type": "blob",
        "sha": "successor-only-blob",
        "size": 1,
    })

    require_promotion_frontier_match(
        compiled,
        observed={
            "thytabakman-jpg/Take-5": {
                "commit": "later-host-commit",
                "tree_sha": "later-host-tree",
                "inventory": observed,
            }
        },
    )


def test_real_predecessor_surface_change_stales_frontier():
    compiled = _compiled_with_inventories()
    inventory = _load_inventory(
        "migration/inventories/TAKE5_TREE_INVENTORY_004.json"
    )
    observed = json.loads(json.dumps(inventory))
    runtime_entry = next(
        x for x in observed["entries"]
        if x["path"] == "runtime/formal_claim_admission.py"
    )
    runtime_entry["sha"] = "changed-predecessor-runtime"

    try:
        require_promotion_frontier_match(
            compiled,
            observed={
                "thytabakman-jpg/Take-5": {
                    "commit": "later-real-predecessor-commit",
                    "tree_sha": "later-real-predecessor-tree",
                    "inventory": observed,
                }
            },
        )
    except RuntimeError as exc:
        assert "PROMOTION_SOURCE_FRONTIER_LAG" in str(exc)
    else:
        raise AssertionError("real predecessor semantic delta was excluded as host noise")
