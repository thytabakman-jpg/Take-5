import sys
sys.path.insert(0,"runtime")
from tool_manifest import OVERRIDES,manifest_for
from tool_manifest_audit import audit_tool_identities
from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS

DEDICATED=("Reconciler","DelegatedExecutor","TRC","CurrentnessAudit","CapabilityFoundry",
"EmergentAdmission","HistoricalReconstruction","ZeroRequest","SolutionToMyProblem",
"DesiredJane","QuestionWorthAsking","LambdaMath","SemanticResolutionPipeline","ToolConductor")

def test_dedicated_native_manifests_are_explicit_and_complete():
    for pid in DEDICATED:
        assert pid in OVERRIDES
        m=manifest_for(pid)
        assert m.complete()
        assert f"{pid}_EXPLICIT_NATIVE_IDENTITY" in m.behavior_ids()

def test_every_current_configured_identity_is_explicit():
    audit=audit_tool_identities(CONFIGURED_RUNS,OVERRIDES)
    assert audit.status=="CLOSED_RELATIVE"
    assert audit.generic_only==()

def test_strong_tool_reality_closes_current_finite_repertoire():
    audit=audit_tool_reality()
    assert audit.configured_identity_status=="CLOSED_RELATIVE"
    assert audit.explicit_manifest_status=="CLOSED_RELATIVE"
    assert audit.native_execution_status=="CLOSED_RELATIVE"
    assert audit.generic_only==()
    assert audit.native_unrecovered==()
    assert audit.status=="CLOSED_RELATIVE"
