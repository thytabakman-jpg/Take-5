"""Recovery validator for current ImprovementCore.

Currentness is versioned against the live regime rather than frozen to one merge
hash. Historical merge/validation receipts remain provenance, while behavioral
identity is checked against the executable regime surface.
"""
from __future__ import annotations

import json
from pathlib import Path

from improvement_core_dispatch import resolve_improvement_core_invocation
from improvement_core_regime import CURRENT_REGIME
from improvement_core_restored_dispatch import resolve_restored_improvement_core_invocation
from current_portfolio_identity import audit_current_portfolio_identity
from historical_replay_audit import audit_historical_replays
from relation_kernel import current_relation_basis
from repertoire_reachability import audit_current_repertoire_reachability

ROOT=Path(__file__).resolve().parents[1]

REQUIRED_FILES=(
    "integration/CURRENT_IMPROVEMENT_CORE.md",
    "architecture/IMPROVEMENT_CORE_RECOVERY_MANIFEST_082.json",
    "architecture/IMPROVEMENT_CORE_ACTIVATION_083.md",
    "architecture/IMPROVEMENT_CORE_MATHEMATICS_086.md",
    "runtime/improvement_core_math.py",
    "runtime/improvement_core_math_spine.py",
    "tests/test_improvement_core_math_spine.py",
    "architecture/IMPROVEMENT_CORE_MATH_CORPUS_INTEGRATION_090.md",
    "tests/test_improvement_core_math_086.py",
    "runtime/improvement_core_dispatch.py",
    "runtime/improvement_core_hf2_default.py",
    "tests/test_improvement_core_hf2_default.py",
    "architecture/IMPROVEMENT_CORE_DEFAULT_HF2_118.md",
    "runtime/improvement_core_return_gate.py",
    "tests/test_improvement_core_return_gate.py",
    "architecture/IMPROVEMENT_CORE_PARENT_RETURN_CLOSURE_139.md",
    "artifacts/improvecore/IMPROVEMENTCORE_PREMATURE_RETURN_HF2_AUDIT_139_2026-09-26.md",
    "tests/test_improvement_core_mode_profile.py",
    "runtime/improvement_core_upstream.py",
    "runtime/improvement_core_external_acquisition.py",
    "architecture/ARTIFACT_TO_WORK_INTAKE_CONTRACT_001_2026-09-25.md",
    "runtime/artifact_intake.py",
    "runtime/archive_artifact_intake.py",
    "tests/test_archive_artifact_intake.py",
    "tests/test_improvement_core_external_acquisition.py",
    "runtime/improvement_core_tool_bridge.py",
    "architecture/IMPROVEMENT_CORE_CONFIGURED_TOOL_EXECUTION_109.md",
    "runtime/improvement_core_regime.py",
    "runtime/improvement_core_manager.py",
    "runtime/ic028_operator.py",
    "runtime/improvement_core_recursive_manager.py",
    "runtime/improvement_core_learning_memory.py",
    "integration/IMPROVEMENT_CORE_DURABLE_LEARNING_110.json",
    "runtime/improvement_core_knowledge_ledger.py",
    "integration/IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json",
    "architecture/IMPROVEMENT_CORE_MATERIAL_KNOWLEDGE_CAPTURE_113.md",
    "architecture/IMPROVEMENT_CORE_LEGACY_RESTORATION_TARGET_129.md",
    "integration/IC128_LEGACY_BEHAVIOR_BENCHMARK_129.yaml",
    "runtime/recovery_corpus_manifest.py",
    "tests/test_recovery_corpus_manifest.py",
    "tests/test_ic128_legacy_behavior_benchmark_129.py",
    "runtime/improvement_core_legacy_candidate.py",
    "tests/test_improvement_core_legacy_candidate.py",
    "runtime/improvement_core_legacy_restored.py",
    "tests/test_improvement_core_legacy_restored.py",
    "runtime/improvement_core_restored_dispatch.py",
    "tests/test_improvement_core_restored_dispatch.py",
    "integration/IMPROVECORE_LEGACY_SEMANTIC_HOLDOUT_PACKET_132.json",
    "artifacts/improvecore/LEGACY_CANDIDATE_CONTROL_HOLDOUT_131_2026-09-26.md",
    "artifacts/improvecore/LEGACY_RESTORED_SEMANTIC_HOLDOUT_132_2026-09-26.md",
    "artifacts/improvecore/IMPROVEMENTCORE_LEGACY_RESTORATION_CLOSURE_133_2026-09-26.md",
    "runtime/improvement_core_progress_relation.py",
    "architecture/IMPROVEMENT_CORE_CANONICAL_PROGRESS_MATHEMATICS_001_2026-09-26.md",
    "architecture/IMPROVEMENT_CORE_ANTI_REPEAT_110.md",
    "tests/test_improvement_core_progress_relation.py",
    "tests/test_improvement_core_anti_repeat_110.py",
    "architecture/IMPROVEMENT_CORE_MAXIMIZATION_081.md",
    "architecture/CROSS_REPOSITORY_IMPROVEMENTCORE_LINEAGE_CHOICE_080.md",
    "research/IMPROVEMENT_CORE_USAGE_AUDIT_078_2026-09-26.md",
    "integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md",
    "architecture/IMPROVEMENT_CORE_FRONTIER_CLOSURE_106.md",
    "architecture/RELATION_BASIS_AND_ADMISSION_001_2026-09-26.md",
    "architecture/HOST_INTERCEPTION_AUTHORITY_BOUNDARY_001_2026-09-26.md",
    "integration/IMPROVEMENTCORE_HISTORICAL_REPLAY_BASIS_001.json",
    "runtime/relation_kernel.py",
    "runtime/improvement_core_route_calibration.py",
    "runtime/current_portfolio_identity.py",
    "runtime/repertoire_reachability.py",
    "runtime/historical_replay_audit.py",
)

def _read(rel:str)->str:
    return (ROOT/rel).read_text(encoding="utf-8")

def validate_recovery()->dict:
    missing=tuple(p for p in REQUIRED_FILES if not (ROOT/p).exists())
    failures=[]
    resolution=resolve_improvement_core_invocation("ImproveCore, recover current state")
    restored_resolution=resolve_restored_improvement_core_invocation(
        "ImproveCore, recover restored state",None
    )

    if missing:
        failures.append("MISSING_RECOVERY_SURFACES")
    if resolution.controller!="IC-028":
        failures.append("CONTROLLER_IDENTITY_DRIFT")
    if not resolution.entrypoint.endswith("run_improvement_core_with_hf2"):
        failures.append("DISPATCH_REGIME_DRIFT")
    if restored_resolution.controller!="IC-028":
        failures.append("RESTORED_CONTROLLER_IDENTITY_DRIFT")
    if not restored_resolution.entrypoint.endswith("dispatch_improvement_core_restored"):
        failures.append("RESTORED_DISPATCH_ENTRYPOINT_DRIFT")
    if CURRENT_REGIME.controller!="IC-028":
        failures.append("REGIME_CONTROLLER_DRIFT")
    if "improvement_core_manager" not in CURRENT_REGIME.stage_manager:
        failures.append("STAGE_MANAGER_MISSING")
    if "recursive_manager" not in CURRENT_REGIME.recursive_manager:
        failures.append("RECURSIVE_MANAGER_MISSING")
    if "learning_memory" not in CURRENT_REGIME.learning_memory:
        failures.append("LEARNING_MEMORY_MISSING")
    if "external_acquisition" not in CURRENT_REGIME.external_acquisition:
        failures.append("EXTERNAL_ACQUISITION_MISSING")
    if "improvement_core_tool_bridge" not in CURRENT_REGIME.configured_tool_bridge:
        failures.append("CONFIGURED_TOOL_BRIDGE_MISSING")
    if "improvement_core_progress_relation" not in CURRENT_REGIME.canonical_progress:
        failures.append("CANONICAL_PROGRESS_RUNTIME_MISSING")
    if "IMPROVEMENT_CORE_DURABLE_LEARNING_110.json" not in CURRENT_REGIME.durable_learning:
        failures.append("DURABLE_LEARNING_SURFACE_MISSING")
    if "IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json" not in CURRENT_REGIME.knowledge_ledger:
        failures.append("KNOWLEDGE_LEDGER_SURFACE_MISSING")
    if CURRENT_REGIME.default_local_recurrence!="HF002":
        failures.append("DEFAULT_HF002_LOCAL_RECURRENCE_MISSING")

    if not missing:
        manifest=json.loads(_read("architecture/IMPROVEMENT_CORE_RECOVERY_MANIFEST_082.json"))
        if manifest.get("status")!="CURRENT":
            failures.append("RECOVERY_MANIFEST_NOT_CURRENT")
        if manifest.get("controller")!="IC-028":
            failures.append("RECOVERY_MANIFEST_CONTROLLER_DRIFT")
        if manifest.get("invocation",{}).get("entrypoint")!="runtime.improvement_core_hf2_default.run_improvement_core_with_hf2":
            failures.append("RECOVERY_MANIFEST_ENTRYPOINT_DRIFT")
        if str(manifest.get("regime_version"))!=str(CURRENT_REGIME.version):
            failures.append("RECOVERY_MANIFEST_REGIME_VERSION_DRIFT")

        math_state=manifest.get("math",{})
        if math_state.get("current_surface")!="architecture/IMPROVEMENT_CORE_MATHEMATICS_086.md":
            failures.append("IMPROVEMENT_CORE_MATH_SURFACE_DRIFT")
        if math_state.get("preferred_controller")!="C_PLUS_JK":
            failures.append("IMPROVEMENT_CORE_MATH_IDENTITY_DRIFT")
        if math_state.get("runtime")!="runtime/improvement_core_math.py":
            failures.append("IMPROVEMENT_CORE_MATH_RUNTIME_DRIFT")
        if math_state.get("progress_relation")!="runtime/improvement_core_progress_relation.py":
            failures.append("IMPROVEMENT_CORE_PROGRESS_RELATION_DRIFT")
        if math_state.get("durable_learning")!="integration/IMPROVEMENT_CORE_DURABLE_LEARNING_110.json":
            failures.append("IMPROVEMENT_CORE_DURABLE_LEARNING_DRIFT")

        invocation=manifest.get("invocation",{})
        if invocation.get("restored_dispatcher")!="runtime/improvement_core_restored_dispatch.py":
            failures.append("RESTORED_DISPATCHER_MANIFEST_MISSING")
        if invocation.get("restored_entrypoint")!="runtime.improvement_core_restored_dispatch.dispatch_improvement_core_restored":
            failures.append("RESTORED_ENTRYPOINT_MANIFEST_MISSING")
        if invocation.get("restored_semantic_provider")!="EXPLICIT_REQUIRED_HOST_BINDING":
            failures.append("RESTORED_SEMANTIC_PROVIDER_CONTRACT_MISSING")

        upstream=manifest.get("invocation",{}).get("upstream_discovery")
        if upstream!="runtime/improvement_core_upstream.py":
            failures.append("UPSTREAM_DISCOVERY_RUNTIME_MISSING")

        regime=manifest.get("regime",{})
        if regime.get("legacy_restored_core")!="runtime/improvement_core_legacy_candidate.py":
            failures.append("LEGACY_RESTORED_CORE_RUNTIME_MISSING")
        if regime.get("legacy_restored_wrapper")!="runtime/improvement_core_legacy_restored.py":
            failures.append("LEGACY_RESTORED_WRAPPER_RUNTIME_MISSING")
        if regime.get("external_acquisition")!="runtime/improvement_core_external_acquisition.py":
            failures.append("EXTERNAL_ACQUISITION_RUNTIME_MISSING")
        if regime.get("configured_tool_bridge")!="runtime/improvement_core_tool_bridge.py":
            failures.append("CONFIGURED_TOOL_BRIDGE_RUNTIME_MISSING")
        if regime.get("artifact_intake")!="runtime/artifact_intake.py":
            failures.append("ARTIFACT_INTAKE_RUNTIME_MISSING")
        if regime.get("archive_artifact_intake")!="runtime/archive_artifact_intake.py":
            failures.append("ARCHIVE_ARTIFACT_INTAKE_RUNTIME_MISSING")
        if regime.get("external_bound_zip_runtime")!="runtime/improvement_core_external_acquisition.py":
            failures.append("EXTERNAL_BOUND_ZIP_RUNTIME_MISSING")
        if regime.get("canonical_progress")!="runtime/improvement_core_progress_relation.py":
            failures.append("CANONICAL_PROGRESS_RUNTIME_DRIFT")
        if regime.get("durable_learning")!="integration/IMPROVEMENT_CORE_DURABLE_LEARNING_110.json":
            failures.append("DURABLE_LEARNING_RUNTIME_DRIFT")
        if regime.get("knowledge_ledger")!="integration/IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json":
            failures.append("KNOWLEDGE_LEDGER_RUNTIME_DRIFT")
        if regime.get("default_local_recurrence")!="HF002":
            failures.append("DEFAULT_HF002_RUNTIME_DRIFT")
        if regime.get("parent_return_gate")!="runtime/improvement_core_return_gate.py":
            failures.append("PARENT_RETURN_GATE_RUNTIME_MISSING")
        if regime.get("recursive_activation")!="LIVE_CONTINUATION":
            failures.append("RECURSIVE_ACTIVATION_CONTRACT_MISSING")
        if regime.get("learning_activation")!="RECURSIVE_ROUTE_GATE_AND_STAGE_LEARNING_EVENTS":
            failures.append("LEARNING_ACTIVATION_CONTRACT_MISSING")

        max_doc=_read("architecture/IMPROVEMENT_CORE_MAXIMIZATION_081.md")
        if "Status: IMPLEMENTED / VALIDATED / MERGED" not in max_doc:
            failures.append("MAXIMIZATION_STATUS_STALE")

        anchor=_read("integration/CURRENT_IMPROVEMENT_CORE.md")
        if f"Current regime version:\n- {CURRENT_REGIME.version}" not in anchor:
            failures.append("RECOVERY_ANCHOR_REGIME_VERSION_DRIFT")
        if "selected formal tool must cross the configured execution bridge" not in anchor:
            failures.append("CONFIGURED_TOOL_EXECUTION_ANCHOR_MISSING")
        if "canonical strict progress, not raw artifact novelty, governs recursive gain" not in anchor:
            failures.append("CANONICAL_PROGRESS_ANCHOR_MISSING")
        if "certified negative route learning is durable" not in anchor:
            failures.append("DURABLE_LEARNING_ANCHOR_MISSING")
        if "default local same-capability recurrence" not in anchor:
            failures.append("DEFAULT_HF002_ANCHOR_MISSING")
        if "exact external ZIP evidence is fail-closed" not in anchor:
            failures.append("BOUND_ZIP_INTAKE_ANCHOR_MISSING")
        if "every declared ZIP member is accounted for" not in anchor:
            failures.append("ZIP_MEMBER_ACCOUNTING_ANCHOR_MISSING")
        if "Active Legacy restoration objective" not in anchor:
            failures.append("LEGACY_RESTORATION_OBJECTIVE_ANCHOR_MISSING")
        if "full-history archive is durable evidence/memory" not in anchor:
            failures.append("LEGACY_RESTORATION_MEMORY_BOUNDARY_MISSING")
        if "typed BOUND_ZIP external-acquisition outputs execute exact binding" not in anchor:
            failures.append("EXTERNAL_BOUND_ZIP_EXECUTION_ANCHOR_MISSING")
        if "bound-ZIP processing failures convert the external acquisition to OPEN_GAP" not in anchor:
            failures.append("EXTERNAL_BOUND_ZIP_FAIL_CLOSED_ANCHOR_MISSING")
        if "## Legacy-restored repository entrypoint" not in anchor:
            failures.append("LEGACY_RESTORED_ENTRYPOINT_ANCHOR_MISSING")
        if "RESTORED_SEMANTIC_PROVIDER_REQUIRED" not in anchor:
            failures.append("RESTORED_SEMANTIC_PROVIDER_FAIL_OPEN_ANCHOR_MISSING")
        if "Repository restoration status:\nCLOSED_RELATIVE." not in anchor:
            failures.append("LEGACY_RESTORATION_CLOSURE_ANCHOR_MISSING")
        if "Unchanged repair routes are NO_GAIN." not in anchor:
            failures.append("LEGACY_RESTORATION_ANTI_CHURN_ANCHOR_MISSING")
        if "## Parent user-return closure" not in anchor:
            failures.append("PARENT_RETURN_CLOSURE_ANCHOR_MISSING")
        if "one strict gain is not permission to return to the user" not in anchor:
            failures.append("ONE_STRICT_GAIN_NOT_PARENT_COMPLETION_ANCHOR_MISSING")
        if "PARENT_RETURN_GATE_REQUIRED" not in anchor:
            failures.append("PARENT_RETURN_GATE_FAIL_CLOSED_ANCHOR_MISSING")

        protected=set(manifest.get("protected_behaviors",[]))
        for required_behavior in (
            "BOUND_ZIP_EXTERNAL_OUTPUT_EXECUTES_INTAKE_BEFORE_MANAGER",
            "BOUND_ZIP_PROCESSING_FAILURE_PRESERVES_EXTERNAL_OPEN_GAP",
            "BOUND_ZIP_RAW_BYTES_AND_GENERATORS_NOT_PERSISTED",
        ):
            if required_behavior not in protected:
                failures.append("BOUND_ZIP_RUNTIME_PROTECTED_BEHAVIOR_MISSING:"+required_behavior)
        for required_behavior in (
            "PARENT_RETURN_GATE_REQUIRED_FOR_USER_VISIBLE_TERMINALITY",
            "ONE_STRICT_GAIN_NOT_PARENT_COMPLETION",
            "HF2_RELATIVE_CLOSE_NOT_PARENT_COMPLETION",
            "PARENT_CONTINUE_REENTERS_COMPLETE_IMPROVEMENTCORE_WITH_HF2",
            "RETURN_COMPLETE_REQUIRES_GOAL_NO_OWNED_WORK_CONSEQUENCE_EVIDENCE",
            "RETURN_NONCOMPLETE_REQUIRES_TYPED_BLOCKER_AND_NO_OWNED_WORK",
        ):
            if required_behavior not in protected:
                failures.append("PARENT_RETURN_PROTECTED_BEHAVIOR_MISSING:"+required_behavior)
        for required_behavior in (
            "LEGACY_ENDOGENOUS_QUESTION_WORK_LOOP",
            "LEGACY_CHEAP_DIRECT_ROUTING",
            "LEGACY_RESULT_SENSITIVE_RESELECTION",
            "LEGACY_NO_PREMATURE_TERMINALITY",
            "RESTORED_SEMANTIC_PROVIDER_REQUIRED_FAILS_OPEN",
            "RESTORED_NO_FIXED_STAGE_FALLBACK_UNDER_RESTORED_CLAIM",
            "RESTORED_MODERN_GUARDS_PRESERVED",
            "FULL_HISTORY_ARCHIVE_NOT_ACTIVE_CONTEXT",
        ):
            if required_behavior not in protected:
                failures.append("LEGACY_RESTORED_PROTECTED_BEHAVIOR_MISSING:"+required_behavior)

        if manifest.get("open") not in ([], ()):
            failures.append("RECOVERY_MANIFEST_OPEN_COORDINATES_STALE")
        external_limits=set(manifest.get("external_limits",[]))
        if "UNIVERSAL_HOST_INTERCEPTION_EXTERNAL_NOT_OWNED" not in external_limits:
            failures.append("HOST_AUTHORITY_BOUNDARY_MISSING")
        if "AUTOMATIC_UNIVERSAL_CHAT_HOST_SEMANTIC_BINDING_EXTERNAL_NOT_OWNED" not in external_limits:
            failures.append("RESTORED_HOST_SEMANTIC_BINDING_BOUNDARY_MISSING")
        if "MASTER_THREE_MONTH_ARCHIVE_NOT_YET_ADDRESSABLE" not in external_limits:
            failures.append("MASTER_ARCHIVE_BOUNDARY_MISSING")
        if not current_relation_basis().complete():
            failures.append("RELATION_BASIS_INCOMPLETE")
        identity=audit_current_portfolio_identity()
        if identity.status!="CLOSED_RELATIVE":
            failures.append("CURRENT_PORTFOLIO_IDENTITY_OPEN")
        reach=audit_current_repertoire_reachability()
        if reach.status!="CLOSED_RELATIVE":
            failures.append("CURRENT_REPERTOIRE_REACHABILITY_OPEN")
        replay=audit_historical_replays()
        if replay.status!="PASS":
            failures.append("HISTORICAL_REPLAY_BASIS_OPEN")

        handoff=_read("integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md")
        if "1. `integration/CURRENT_IMPROVEMENT_CORE.md`" not in handoff:
            failures.append("HANDOFF_CURRENT_ANCHOR_MISSING")

    return {
        "status":"PASS" if not failures else "FAIL",
        "missing":missing,
        "failures":tuple(failures),
        "controller":resolution.controller,
        "entrypoint":resolution.entrypoint,
        "restored_entrypoint":restored_resolution.entrypoint,
        "regime_version":CURRENT_REGIME.version,
    }

if __name__=="__main__":
    result=validate_recovery()
    print(result)
    raise SystemExit(0 if result["status"]=="PASS" else 1)
