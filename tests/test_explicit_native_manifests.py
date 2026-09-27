import sys
sys.path.insert(0,"runtime")

from tool_manifest import OVERRIDES,manifest_for
from tool_manifest_audit import audit_tool_identities
from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS

DEDICATED=(
    "Reconciler","DelegatedExecutor","TRC","CurrentnessAudit",
    "CapabilityFoundry","EmergentAdmission","HistoricalReconstruction",
    "ZeroRequest","SolutionToMyProblem","DesiredJane","QuestionWorthAsking",
    "LambdaMath","SemanticResolutionPipeline","ToolConductor",
)

UNRESOLVED={"MTA","Architecture","PD","PDAudit"}


def test_dedicated_native_manifests_are_explicit_and_complete():
    for pid in DEDICATED:
        assert pid in OVERRIDES
        m=manifest_for(pid)
        assert m.complete()
        assert f"{pid}_EXPLICIT_NATIVE_IDENTITY" in m.behavior_ids()


def test_registry_defined_and_learning_tools_are_explicit():
    for pid in CONFIGURED_RUNS:
        if pid in UNRESOLVED:
            continue
        assert pid in OVERRIDES
        assert manifest_for(pid).complete()


def test_explicit_manifest_residual_is_exactly_unresolved_four():
    audit=audit_tool_identities(CONFIGURED_RUNS,OVERRIDES)
    assert set(audit.generic_only)==UNRESOLVED
    assert audit.status=="OPEN"


def test_strong_tool_reality_has_one_shared_exact_four_frontier():
    audit=audit_tool_reality()
    assert audit.configured_identity_status=="CLOSED_RELATIVE"
    assert set(audit.generic_only)==UNRESOLVED
    assert set(audit.native_unrecovered)==UNRESOLVED
    assert audit.explicit_manifest_status=="OPEN"
    assert audit.native_execution_status=="OPEN"
    assert audit.status=="OPEN"
