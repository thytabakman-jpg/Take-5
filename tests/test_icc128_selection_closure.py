"""ICC128 regression: whole-system tool consultation is not executed work."""

import sys
sys.path.insert(0, "runtime")

import pytest

from icc128_episode_adapter import ICC128EpisodeAdapter


@pytest.mark.parametrize("domain,required_job", [
    ("pull_requests", "cross_pr_dependency_reconciliation"),
    ("backlog", "shared_cause_discovery"),
    ("level_2_3_4", "shared_certification_dependency_verification"),
])
def test_unselected_shared_work_cannot_be_reported_complete(domain, required_job):
    # All three domains use synthetic job packets, not live PR or file certificates.
    executions = []
    adapter = ICC128EpisodeAdapter(
        generate_questions=lambda state, memory: [{"id": f"question:{domain}"}],
        generate_work=lambda questions, state, memory: [{
            "id": "isolated_item_only",
            "jobs": ("individual_item",),
            "operation_class": "OBSERVE",
            "effect_class": "EVIDENCE_ONLY",
        }],
        admit_results=lambda results, state, memory: {"results": tuple(results)},
        update_state=lambda state, memory, delta: (
            {**state, "terminal": "COMPLETE", "admitted_continuation": False},
            {**memory, "caller_claimed_complete": True},
        ),
        generic_execute=lambda item, state, memory: executions.append(item),
    )

    out = adapter({
        "identity": domain,
        "frozen_math_fingerprint": f"regression:{domain}",
        "obligations": [{"id": required_job}],
    })
    assert out.status == "OPEN"
    assert executions == []
    assert len(out.traces) == 1
    trace = out.traces[0]
    # A full registry traversal is a coverage receipt, NOT an execution receipt.
    assert trace["tool_conductor"]["coverage_complete"]
    assert trace["selected"] == []
    assert trace["results"] == []
    assert trace["admitted_delta"]["selection_status"] == "OPEN"
    assert trace["admitted_delta"]["execution_blocker"] == "ICC128_SELECTION_NOT_EXECUTED:OPEN"
    assert trace["state_after"]["terminal"] == "OPEN"
    assert trace["memory_after"]["rho_reselection_required"] is True


def test_matching_selected_work_can_still_reach_complete_with_execution():
    executions = []
    required_job = "shared_cause_discovery"

    def executor(item, state, memory):
        executions.append(item["id"])
        return {
            "status": "EXECUTED",
            "execution_truth": "IMPLEMENTATION_EXECUTED",
            "material_delta": True,
            "evidence": ("test:shared_work_executed",),
        }

    adapter = ICC128EpisodeAdapter(
        generate_questions=lambda state, memory: [{"id": "question:shared"}],
        generate_work=lambda questions, state, memory: [{
            "id": "joint_observer",
            "jobs": (required_job,),
            "operation_class": "OBSERVE",
            "effect_class": "EVIDENCE_ONLY",
        }],
        admit_results=lambda results, state, memory: {"results": tuple(results)},
        update_state=lambda state, memory, delta: (
            {**state, "terminal": "COMPLETE", "admitted_continuation": False},
            dict(memory),
        ),
        generic_execute=executor,
    )

    out = adapter({
        "identity": "backlog",
        "frozen_math_fingerprint": "positive-control",
        "obligations": [{"id": required_job}],
    })
    assert out.status == "COMPLETE"
    assert executions == ["joint_observer"]
    assert out.traces[0]["selected"][0]["id"] == "joint_observer"
    assert out.results[0]["execution_truth"] == "IMPLEMENTATION_EXECUTED"
