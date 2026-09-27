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
    verify_inventory,
)


SNAPSHOT_ROOT = ROOT / "migration" / "source_snapshots"


def test_repository_snapshot_history_compiles_unique_frontier():
    snapshots = load_source_snapshots(SNAPSHOT_ROOT)
    compiled = compile_source_frontier(snapshots)

    take5 = compiled["repositories"]["thytabakman-jpg/Take-5"]
    assert take5["status"] == "CURRENT"
    assert take5["current_commit"] == "a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2"
    assert take5["current_tree_sha"] == "104d50432a0aead4508890ef1a410fa7356e41c4"
    assert take5["known_commits"] == [
        "853c7f92dae62747d3f8f42a38b6d4b77e194ad2",
        "a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2",
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
        and x["commit"] == "a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2"
    )
    inv_path = ROOT / current["inventory"]
    inventory = json.loads(inv_path.read_text(encoding="utf-8"))
    verify_inventory(current, inventory)
    assert inventory["entry_count"] == 905
    assert inventory["blob_count"] == 859
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
                "commit": "a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2",
                "tree_sha": "104d50432a0aead4508890ef1a410fa7356e41c4",
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
