"""Native Kernel/Jane regression checks: status, entry, discovery-only continuity."""
from pathlib import Path
import sys

import yaml
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from jane import begin_icc128_turn
from jane_relevance import supervisory_relevance
from math_first_wrapper import run_math_first_wrapper
from icc_bootstrap import ICCBootstrapReceipt, ToolRunReceipt
from representation_discovery import DiscoveryDelta
from dataclasses import dataclass


def test_kernel_repository_authority_agrees_with_migration_without_host_promotion():
    kernel = yaml.safe_load((ROOT / "KERNEL.yaml").read_text(encoding="utf-8"))
    migration = yaml.safe_load((ROOT / "MIGRATION_STATE.yaml").read_text(encoding="utf-8"))
    assert kernel["status"] == migration["status"] == "CANONICAL_WORKING"
    assert kernel["target_status"] == "CANONICAL_WORKING"
    assert kernel["working_authority"] == migration["current_repository"]
    assert kernel["working_authority_source"] == "MIGRATION_STATE.yaml"
    assert kernel["legacy_authority"] == migration["legacy_baseline"]["repository"]
    assert kernel["legacy_authority_role"] == "rollback_and_provenance_only"
    assert kernel["production_authority"] == "none"
    assert kernel["promotion"]["self_promotion"] == "prohibited"


def _currentness(**overrides):
    data = {
        "target": "research-system",
        "job": "repair-continuity",
        "basis": "Take-5/main",
        "canonical_version": "verified-source-revision",
    }
    data.update(overrides)
    return data


def test_jane_guarded_current_entry_preserves_controller_ownership_and_memory():
    binding, handoff = begin_icc128_turn(
        "ICC repair native continuity",
        target="research-system", job="repair-continuity", basis="Take-5/main",
        currentness=_currentness(),
        rejection_memory={"rejected": ("lost-dependency",)},
        open_coordinates=("unverified-external-host",),
    )
    assert binding.contract.controller == binding.lease.controller == "ICC128"
    assert handoff.status == "READY"
    assert handoff.state["target"] == binding.contract.frozen_target
    assert handoff.state["job"] == binding.lease.job
    assert handoff.memory["rejected"] == ("lost-dependency",)
    assert handoff.state["open_coordinates"] == ("unverified-external-host",)
    assert "selected_action" not in handoff.state


@pytest.mark.parametrize("missing", ("target", "job", "basis", "canonical_version"))
def test_jane_guarded_entry_rejects_missing_continuity(missing):
    with pytest.raises(RuntimeError, match="JANE_CONTINUITY_OPEN"):
        begin_icc128_turn(
            "ICC repair", target="research-system", job="repair-continuity",
            basis="Take-5/main", currentness=_currentness(**{missing: None}),
        )


@pytest.mark.parametrize("coordinate", ("target", "job", "basis"))
def test_jane_guarded_entry_rejects_identity_mismatch(coordinate):
    with pytest.raises(RuntimeError, match="JANE_CONTINUITY_IDENTITY_MISMATCH:" + coordinate):
        begin_icc128_turn(
            "ICC repair", target="research-system", job="repair-continuity",
            basis="Take-5/main", currentness=_currentness(**{coordinate: "wrong"}),
        )


def test_new_dependency_and_discovery_coordinates_are_supervisory():
    for key in ("discovery_delta", "dependency_graph", "representation_basis", "view_changed"):
        assert supervisory_relevance({"changed": (key,)}).relevant
    assert not supervisory_relevance({"changed": ("answer",)}).relevant


@dataclass(frozen=True)
class Cert:
    status: str


@dataclass(frozen=True)
class DiscoveryClosure:
    state: dict
    certificate: Cert
    discovery_delta: DiscoveryDelta


def _bootstrap(state, binding):
    a = ToolRunReceipt("ASSERT", True, True, True, True, True, True, {"asserted": True})
    g = ToolRunReceipt("GOAL", True, True, True, True, True, True, {"goal": "observed"})
    return ICCBootstrapReceipt(a, g, True, ("ASSERT_OBSERVER", "GOAL_OBSERVER"))


def test_discovery_only_wrapper_round_notifies_jane_without_target_mutation():
    binding, _ = begin_icc128_turn(
        "ICC repair", target="research-system", job="repair-continuity",
        basis="Take-5/main", currentness=_currentness(),
    )
    rounds = {"n": 0}

    def close(pre, ic_result, packet):
        rounds["n"] += 1
        return DiscoveryClosure(
            dict(pre),
            Cert("CLOSED"),
            DiscoveryDelta(candidate_universe_changed=(rounds["n"] == 1)),
        )

    def sync_jane(jane_state, delta):
        out = dict(jane_state)
        out["received"] = out.get("received", ()) + (
            (delta.changed, delta.material, delta.before_fingerprint == delta.after_fingerprint),
        )
        return out

    result = run_math_first_wrapper(
        binding,
        {"answer": "stable"}, {"received": ()},
        bootstrap_fn=_bootstrap,
        observe_fn=lambda s, b: s,
        formalize_fn=lambda o, b: {"fixed": 1},
        goal_fn=lambda m, b: "preserve-answer",
        architect_fn=lambda m, g, s, b: {
            "type": "system", "scope": "local", "readings": [],
            "result_sensitive": [], "selectors": [], "provenance": [],
            "open": [], "obligations": [],
        },
        ic_fn=lambda p: dict(p),
        closure_fn=close,
        update_fn=lambda p, c: c.state,
        jane_update_fn=sync_jane,
        result_fn=lambda s: s["answer"],
    )
    assert result.status == "CLOSED_RELATIVE"
    assert result.state == {"answer": "stable"}
    assert len(result.rounds) == 2
    assert result.rounds[0].jane_synced
    assert not result.rounds[1].jane_synced
    assert len(result.jane_state["received"]) == 1
    fields, target_mutated, fingerprints_equal = result.jane_state["received"][0]
    assert "discovery_delta" in fields
    assert not target_mutated
    assert fingerprints_equal
