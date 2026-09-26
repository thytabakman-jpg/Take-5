#!/usr/bin/env python3
"""ImproveCore self-study 104.

Runs the current ImproveCore dispatcher over its own canonical/runtime surfaces plus
an externally researched architecture packet. The output is evidence, not a new
canonical authority.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from improvement_core_regime import CURRENT_REGIME, REGIME_VERSION
from improvement_core_learning_memory import VALID_DISPOSITIONS
from improvement_core_external_acquisition import DEFAULT_PRIORITY
from ic028_operator import OBSERVER_FIRST_STAGES
from entry_contract import preflight_mode_profile
from root_cause import RootCandidate, run_root_cause_hf2
from question_worth_asking import QuestionCandidate, select_question
from currentness_audit import assess
from assert_compound import AssertState, AssertStages, run_to_fixed_point

INPUT = ROOT / "integration/IMPROVECORE_SELF_STUDY_INPUT_104_2026-09-26.md"
RESEARCH = ROOT / "research/IMPROVECORE_EXTERNAL_ARCHITECTURE_RESEARCH_104_2026-09-26.md"
CURRENT = ROOT / "integration/CURRENT_IMPROVEMENT_CORE.md"

CORE_FILES = {
    "dispatch": ROOT / "runtime/improvement_core_dispatch.py",
    "regime": ROOT / "runtime/improvement_core_regime.py",
    "manager": ROOT / "runtime/improvement_core_manager.py",
    "operator": ROOT / "runtime/ic028_operator.py",
    "recursive_manager": ROOT / "runtime/improvement_core_recursive_manager.py",
    "learning_memory": ROOT / "runtime/improvement_core_learning_memory.py",
    "external_acquisition": ROOT / "runtime/improvement_core_external_acquisition.py",
    "math_spine": ROOT / "runtime/improvement_core_math_spine.py",
    "capability_foundry": ROOT / "runtime/capability_foundry.py",
    "tool_manifest": ROOT / "runtime/tool_manifest.py",
    "controller_lease": ROOT / "runtime/controller_lease.py",
    "tool_bridge": ROOT / "runtime/improvement_core_tool_bridge.py",
}

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def file_inventory():
    runtime = sorted((ROOT / "runtime").glob("*.py"))
    tests = sorted((ROOT / "tests").glob("test_*.py"))
    return {
        "runtime_python_files": len(runtime),
        "test_python_files": len(tests),
        "improvecore_runtime_files": sorted(
            str(p.relative_to(ROOT))
            for p in runtime
            if "improvement_core" in p.name or p.name == "ic028_operator.py"
        ),
    }

def capability_snapshot():
    texts = {name: read(path) for name, path in CORE_FILES.items()}
    regime = texts["regime"]
    operator = texts["operator"]
    memory = texts["learning_memory"]
    external = texts["external_acquisition"]
    recursive = texts["recursive_manager"]
    foundry = texts["capability_foundry"]
    tool_bridge = texts["tool_bridge"]

    checkpoint_tokens = ("checkpoint", "event_history", "resume_from", "replay_from")
    persistent_checkpoint = any(tok in (regime + operator).lower() for tok in checkpoint_tokens)

    structured_receipts = "OperatorReceipt" in operator and "ManagerTrace" in recursive
    durable_trace_export = any(
        tok in (regime + operator + recursive).lower()
        for tok in ("trace_export", "otel", "opentelemetry", "persist_trace")
    )

    host_adapter_injection = "external_adapters" in regime and "adapters:Mapping" in external
    adapter_auto_discovery = any(
        tok in (regime + external).lower()
        for tok in ("discover_adapters", "adapter_registry", "capability_discovery")
    )

    route_learning = "RouteEvidence" in memory and "unchanged_rerun_blocked" in memory
    execution_position_memory = any(
        tok in memory.lower()
        for tok in ("stage_index", "checkpoint", "resume_stage", "event_history")
    )

    capability_generation = "CapabilityFoundry" in foundry
    parent_child = "RecursiveImprovementCoreManager" in recursive
    explicit_retry = any(tok in recursive.lower() for tok in ("retry_policy", "retry_count", "backoff"))
    cancellation = any(tok in recursive.lower() for tok in ("cancel", "cancellation"))
    resume = any(tok in recursive.lower() for tok in ("resume", "checkpoint"))

    return {
        "controller": CURRENT_REGIME.controller,
        "regime_version": REGIME_VERSION,
        "stage_manager": CURRENT_REGIME.stage_manager,
        "recursive_manager": CURRENT_REGIME.recursive_manager,
        "learning_memory": CURRENT_REGIME.learning_memory,
        "external_acquisition": CURRENT_REGIME.external_acquisition,
        "observer_mode": preflight_mode_profile(
            "ImproveCore audit whole system", observer_risk=True
        ).mode_id,
        "learning_dispositions": sorted(VALID_DISPOSITIONS),
        "external_priority": list(DEFAULT_PRIORITY),
        "capabilities": {
            "basis_relative_route_learning": "PRESENT" if route_learning else "UNRESOLVED",
            "recursive_parent_child_management": "PRESENT" if parent_child else "UNRESOLVED",
            "capability_foundry": "PRESENT" if capability_generation else "UNRESOLVED",
            "structured_in_memory_receipts": "PRESENT" if structured_receipts else "UNRESOLVED",
            "durable_trace_export": "PRESENT" if durable_trace_export else "PARTIAL_OR_ABSENT",
            "durable_execution_checkpoint_replay": "PRESENT" if persistent_checkpoint else "ABSENT_IN_CORE_RUNTIME",
            "execution_position_memory_distinct_from_learning_memory": (
                "PRESENT" if execution_position_memory else "ABSENT_IN_LEARNING_MEMORY"
            ),
            "host_adapter_injection": "PRESENT" if host_adapter_injection else "UNRESOLVED",
            "automatic_host_adapter_discovery": "PRESENT" if adapter_auto_discovery else "ABSENT_IN_CORE_RUNTIME",
            "recursive_retry_policy": "PRESENT" if explicit_retry else "ABSENT_IN_RECURSIVE_MANAGER",
            "recursive_cancellation_semantics": "PRESENT" if cancellation else "ABSENT_IN_RECURSIVE_MANAGER",
            "recursive_resume_semantics": "PRESENT" if resume else "ABSENT_IN_RECURSIVE_MANAGER",
            "configured_tool_runtime_bridge": (
                "PRESENT"
                if "execute_bound_tools" in tool_bridge and "CONFIGURED_TOOL_ADAPTER_REQUIRED" in tool_bridge
                else "ABSENT"
            ),
        },
    }

def improvement_candidates(snapshot):
    caps = snapshot["capabilities"]
    return [
        {
            "id": "IC-DURABLE-RUN-JOURNAL",
            "classification": "STRICT_GAIN_CANDIDATE",
            "current_state": caps["durable_execution_checkpoint_replay"],
            "basis": [
                "current OperatorReceipt/ManagerTrace are execution evidence but are not a persistent replay checkpoint",
                "LearningMemory records route outcomes rather than execution position",
                "LangGraph separates checkpoints from long-term stores",
                "Temporal uses event history for durable resume/replay",
            ],
            "minimal_form": "append-only run event journal + checkpoint cursor, kept separate from learning memory",
            "risk": "MEDIUM",
            "implementation_status": "OPEN_DESIGN_REQUIRED",
        },
        {
            "id": "IC-TRACE-EXPORT",
            "classification": "STRICT_GAIN_CANDIDATE",
            "current_state": caps["durable_trace_export"],
            "basis": [
                "current runtime already emits typed receipts and recursive traces",
                "no first-class normalized durable trace-export surface is present in the core runtime",
                "OpenAI Agents SDK treats end-to-end tracing as a production runtime primitive",
            ],
            "minimal_form": "pure projection from existing receipts to a stable structured trace schema",
            "risk": "LOW",
            "implementation_status": "ADMISSION_READY_CANDIDATE",
        },
        {
            "id": "IC-HOST-CAPABILITY-DISCOVERY",
            "classification": "STRICT_GAIN_CANDIDATE",
            "current_state": caps["automatic_host_adapter_discovery"],
            "basis": [
                "external acquisition already supports adapters but requires host injection",
                "current recovery anchor leaves universal host interception OPEN",
                "agent runtimes/frameworks commonly expose explicit runtime/tool registries",
            ],
            "minimal_form": "typed adapter registry/discovery contract without self-authorizing use",
            "risk": "MEDIUM",
            "implementation_status": "OPEN_HOST_BOUNDARY",
        },
        {
            "id": "IC-RUNTIME-LIFECYCLE-FAILURE-SEMANTICS",
            "classification": "STRICT_GAIN_CANDIDATE",
            "current_state": {
                "retry": caps["recursive_retry_policy"],
                "cancel": caps["recursive_cancellation_semantics"],
                "resume": caps["recursive_resume_semantics"],
            },
            "basis": [
                "current recursive manager validates child returns and no-progress but does not expose retry/cancel/resume policy",
                "Temporal and AutoGen model runtime lifecycle/failure behavior explicitly",
            ],
            "minimal_form": "typed child execution lifecycle policy composed with the durable journal",
            "risk": "MEDIUM_HIGH",
            "implementation_status": "OPEN_DESIGN_REQUIRED",
        },
        {
            "id": "IC-REFLECTION-EVIDENCE-SCHEMA",
            "classification": "COMPOSE_EXISTING_FIRST",
            "current_state": caps["basis_relative_route_learning"],
            "basis": [
                "LearningMemory already stores arbitrary evidence per route outcome",
                "Reflexion suggests useful value in explicit linguistic feedback/episodic reflection",
            ],
            "minimal_form": "extend evidence conventions before creating a new memory subsystem",
            "risk": "LOW",
            "implementation_status": "SUBSUME_OR_SMALL_EXTENSION",
        },
        {
            "id": "IC-CAPABILITY-SKILL-PROMOTION",
            "classification": "PARTIAL_EXISTING",
            "current_state": caps["capability_foundry"],
            "basis": [
                "CapabilityFoundry and ToolManifest already govern typed capability candidates",
                "Voyager shows compounding value from reusable executable skill libraries",
                "new skill-library architecture would be redundant unless current foundry/manifest cannot express promotion and reuse",
            ],
            "minimal_form": "test whether repeated successful child routes can promote through existing foundry/manifest",
            "risk": "MEDIUM",
            "implementation_status": "EXPERIMENT_BEFORE_ARCHITECTURE",
        },
        {
            "id": "IC-INTERFACE-QUALITY-BENCHMARK",
            "classification": "STRICT_GAIN_CANDIDATE",
            "current_state": "NO_STANDARDIZED_INTERFACE_ABLATION_FOUND_IN_CORE_RUNTIME",
            "basis": [
                "SWE-agent reports material performance effects from agent-computer interface design",
                "ImproveCore depends on host adapters/tool surfaces and already uses matched/holdout evaluation elsewhere",
            ],
            "minimal_form": "matched benchmark of equivalent tasks across alternative tool/adapter interfaces",
            "risk": "LOW_MEDIUM",
            "implementation_status": "EXPERIMENT_READY",
        },
    ]

def configured_tool_adapters():
    """Bind real native tool runtimes used by the self-study.

    Every adapter receives the full configured D36_C execution plan. The native
    tool result is returned into controller state and consumed by later stages.
    """

    def currentness_adapter(state,plan):
        result=assess(
            component="ImproveCore formal-tool execution path",
            built_basis="regime-088:configured-plan-only",
            latest_basis="regime-089:configured-tool-execution-bridge",
            protected=("selected formal tool identity","full configured wrapper","OPEN preservation"),
            delta=("selected tools were not forced through native runtime adapters",),
            behavior_preserved=True,
            local_patch_available=True,
            evidence=("runtime/ic028_operator.py","runtime/improvement_core_tool_bridge.py"),
            obligations=("verify real adapter invocation","verify missing adapter remains OPEN"),
            dependents=("repertoire reachability","self-study execution"),
            reverified=False,
        )
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":asdict(result),
            "evidence":(
                f"configured-plan:{plan.tool_id}:{len(plan.cells)}",
                "native:currentness_audit.assess",
            ),
            "material_delta":True,
        }

    def root_cause_adapter(state,plan):
        failure_class={
            "formal_tool_selected_without_native_execution",
            "generic_execute_callback_substitutes_for_tool_runtime",
            "plan_reachability_mislabeled_as_execution_reachability",
        }
        candidates=(
            RootCandidate(
                "HARDCODED_SELF_STUDY_HANDLERS",
                "LOCAL_MECHANISM",
                frozenset({"generic_execute_callback_substitutes_for_tool_runtime"}),
                survives_representation_change=False,
                removal_breaks_recurrence=False,
            ),
            RootCandidate(
                "PLAN_ONLY_REACHABILITY_AUDIT",
                "ENABLING_CONDITION",
                frozenset({"plan_reachability_mislabeled_as_execution_reachability"}),
                survives_representation_change=True,
                removal_breaks_recurrence=False,
            ),
            RootCandidate(
                "TOOL_SELECTION_EXECUTION_SEAM_MISSING",
                "ROOT_GENERATOR",
                frozenset(failure_class),
                upstream_of=frozenset({
                    "HARDCODED_SELF_STUDY_HANDLERS",
                    "PLAN_ONLY_REACHABILITY_AUDIT",
                }),
                survives_representation_change=True,
                removal_breaks_recurrence=True,
            ),
        )
        result=run_root_cause_hf2(
            failure_class=failure_class,
            candidates=candidates,
            basis_id="improvecore-tool-use-109",
        )
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":asdict(result),
            "evidence":(
                f"configured-plan:{plan.tool_id}:{len(plan.cells)}",
                "native:root_cause.run_root_cause_hf2",
            ),
            "material_delta":True,
        }

    def question_adapter(state,plan):
        questions=(
            QuestionCandidate(
                "q-execution",
                "Does a selected formal tool cross into its configured native runtime before EXECUTE can close?",
                1.0,1.0,1.0,1.0,0.15,0.05,
            ),
            QuestionCandidate(
                "q-registry",
                "Are powerful tools registered?",
                0.45,0.35,0.2,0.3,0.1,0.05,
            ),
            QuestionCandidate(
                "q-more-tools",
                "Can more tools be added?",
                0.2,0.2,0.1,0.1,0.6,0.4,
            ),
        )
        result=select_question(questions)
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":asdict(result),
            "evidence":(
                f"configured-plan:{plan.tool_id}:{len(plan.cells)}",
                "native:question_worth_asking.select_question",
            ),
            "material_delta":True,
        }

    def assert_adapter(state,plan):
        def assert_stage(x):
            return replace(x,assertions=(
                "selected registered formal tool requires configured adapter execution",
                "missing adapter preserves OPEN",
            ))
        def compare_stage(x):
            return replace(x,comparisons=(
                "selection identity matches configured registry",
                "execution receipt names the native tool",
                "configured plan has 36 cells",
            ))
        def resolve_stage(x):
            return replace(x,resolutions=("semantic selection is not execution",))
        def here_stage(x):
            return replace(x,here=(
                "runtime/improvement_core_tool_bridge.py",
                "runtime/ic028_operator.py",
            ))
        def inquire_stage(x):
            return replace(x,inquiries=(
                "Was the adapter called?",
                "Was its result consumed into controller state?",
            ))
        def reassert_stage(x):
            return replace(x,metadata={"bridge_required":True,"fail_open":True})

        result=run_to_fixed_point(
            AssertState(),
            AssertStages(
                assert_stage,
                compare_stage,
                resolve_stage,
                here_stage,
                inquire_stage,
                reassert_stage,
            ),
            max_rounds=3,
            closure_gate=lambda x: bool(x.here and x.assertions),
        )
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":asdict(result),
            "evidence":(
                f"configured-plan:{plan.tool_id}:{len(plan.cells)}",
                "native:assert_compound.run_to_fixed_point",
            ),
            "material_delta":True,
        }

    return {
        "CurrentnessAudit":currentness_adapter,
        "RootCause":root_cause_adapter,
        "QuestionWorthAsking":question_adapter,
        "ASSERT":assert_adapter,
    }


def handlers():
    snap = capability_snapshot()
    inventory = file_inventory()
    candidates = improvement_candidates(snap)

    def make(stage):
        def handle(state):
            s = dict(state or {})
            trace = list(s.get("self_study_stage_trace", ()))
            trace.append(stage)
            s["self_study_stage_trace"] = trace

            if stage == "OBSERVE":
                s["self_inventory"] = inventory
                s["capability_snapshot"] = snap
                s["sources_loaded"] = {
                    "input": str(INPUT.relative_to(ROOT)),
                    "external_research": str(RESEARCH.relative_to(ROOT)),
                    "current_anchor": str(CURRENT.relative_to(ROOT)),
                }
            elif stage == "OBSERVE_RECONCILE":
                s["reconciliation"] = {
                    "documented_current_regime_matches_runtime_version": (
                        f"Current regime version:\n- {REGIME_VERSION}" in read(CURRENT)
                    ),
                    "external_research_is_evidence_not_authority": True,
                }
            elif stage == "OBSERVE_TRC":
                s["truth_constraints"] = {
                    "no_external_pattern_self_authorizes": True,
                    "no_candidate_is_current_until independently admitted and tested": True,
                    "host_boundary_remains distinct from repository correctness": True,
                }
            elif stage == "RECOVER_GOAL":
                s["governing_goal"] = (
                    "reconstruct current ImproveCore, identify evidence-backed strict gains, "
                    "prefer composition/recovery over layer proliferation"
                )
            elif stage == "CURIOSITY_PD":
                s["question_frontier"] = tuple(
                    c["id"] for c in candidates
                )
            elif stage == "FORMALIZE":
                s["formal_self_model"] = {
                    "identity": "ImproveCore / IC-028 / regime " + REGIME_VERSION,
                    "execution_chain": [
                        "dispatch",
                        "upstream discovery when coordinates absent",
                        "regime external-acquisition preflight",
                        "stage manager",
                        "recursive manager when live continuation",
                        "learning-memory update",
                    ],
                    "state_kinds_to_keep_distinct": [
                        "execution state",
                        "learning memory",
                        "external evidence",
                        "protected contribution/currentness",
                    ],
                }
            elif stage == "PLAN_ORDER":
                s["plan"] = [
                    "inventory current runtime",
                    "separate present/partial/absent",
                    "compare external patterns",
                    "collapse redundant candidates",
                    "preserve unresolved design coordinates OPEN",
                    "identify low-coupling admission-ready gains",
                ]
            elif stage == "OBJECTIFY":
                s["candidate_objects"] = candidates
            elif stage == "GENERATE_WORK":
                s["generated_work"] = [
                    "trace export minimal strict-gain experiment",
                    "durable journal design experiment",
                    "host adapter discovery contract experiment",
                    "tool-interface matched ablation",
                    "foundry/manifest skill-promotion subsumption test",
                ]
            elif stage == "SELECT":
                s["selected_tools"] = (
                    "CurrentnessAudit",
                    "RootCause",
                    "QuestionWorthAsking",
                    "ASSERT",
                )
                s["selected_next_candidate"] = {
                    "id": "IC-TRACE-EXPORT",
                    "reason": (
                        "uses already-existing receipts, adds observability without changing controller semantics, "
                        "and has the lowest coupling among identified strict-gain candidates"
                    ),
                }
            elif stage == "BIND":
                s["selection_binding"] = {
                    "authority": "self-study and candidate selection only",
                    "canonical_mutation_authorized": False,
                }
            elif stage == "EXECUTE":
                tool_outputs=tuple(s.get("configured_tool_outputs",()))
                by_tool={x["tool_id"]:x for x in tool_outputs}
                root_result=by_tool.get("RootCause",{}).get("result",{})
                question_result=by_tool.get("QuestionWorthAsking",{}).get("result",{})
                assert_result=by_tool.get("ASSERT",{}).get("result",{})
                s["self_study_result"] = {
                    "architecture_reconstructed": True,
                    "configured_tools_used":tuple(by_tool),
                    "tool_driven_findings":{
                        "root_candidates":root_result.get("root_candidates",()),
                        "question_status":question_result.get("status"),
                        "assert_status":assert_result.get("status"),
                    },
                    "candidate_count": len(candidates),
                    "candidates": candidates,
                    "admission_ready": ["IC-TRACE-EXPORT"],
                    "open_design": [
                        "IC-DURABLE-RUN-JOURNAL",
                        "IC-HOST-CAPABILITY-DISCOVERY",
                        "IC-RUNTIME-LIFECYCLE-FAILURE-SEMANTICS",
                    ],
                    "experiment_ready": [
                        "IC-INTERFACE-QUALITY-BENCHMARK",
                        "IC-CAPABILITY-SKILL-PROMOTION",
                    ],
                    "compose_existing": ["IC-REFLECTION-EVIDENCE-SCHEMA"],
                }
                return {"state": s, "material_delta": True}
            elif stage == "ADMIT":
                s["admission"] = {
                    "admitted_for_next_implementation_experiment": ["IC-TRACE-EXPORT"],
                    "not_yet_admitted": [
                        c["id"] for c in candidates if c["id"] != "IC-TRACE-EXPORT"
                    ],
                }
            elif stage == "RECONCILE":
                s["architecture_decision"] = (
                    "No new master controller or memory layer. Keep checkpointing distinct from learning memory. "
                    "Test trace export first; keep larger runtime changes OPEN."
                )
            elif stage == "PROPAGATE_AFFECTED_CONE":
                s["affected_cone"] = [
                    "ImproveCore observability",
                    "host-visible verification",
                    "future durable execution design",
                    "external adapter boundary",
                    "tool-interface evaluation",
                ]
            elif stage == "PERSIST":
                s["persistence_target"] = "self-study report artifact"
            elif stage == "VERIFY":
                s["verification"] = {
                    "core_files_present": all(p.is_file() for p in CORE_FILES.values()),
                    "research_packet_present": RESEARCH.is_file(),
                    "input_present": INPUT.is_file(),
                    "trace_candidate_uses_existing_receipts": snap["capabilities"]["structured_in_memory_receipts"] == "PRESENT",
                    "checkpoint_candidate_not_confused_with_learning_memory": (
                        snap["capabilities"]["execution_position_memory_distinct_from_learning_memory"]
                        == "ABSENT_IN_LEARNING_MEMORY"
                    ),
                    "configured_tool_execution_evidence": (
                        len(tuple(s.get("configured_tool_outputs",())))==4
                    ),
                    "all_configured_tools_full_36": all(
                        x.get("binding",{}).get("cell_count")==36
                        for x in tuple(s.get("configured_tool_outputs",()))
                    ),
                }
            elif stage == "COMPLETE":
                s["terminal_disposition"] = "RELATIVE_CLOSE_WITH_STRICT_GAIN_CANDIDATES"
                return {"state": s, "terminal": True}
            return {"state": s}
        return handle

    out = {stage: make(stage) for stage in OBSERVER_FIRST_STAGES}
    out["REENTER"] = lambda state: {"state": state, "terminal": True}
    return out

def run(output: Path):
    corpus = [
        {"id": "input-104", "text": read(INPUT)},
        {"id": "research-104", "text": read(RESEARCH)},
        {"id": "current-anchor", "text": read(CURRENT)},
    ]
    resolution, result = dispatch_improvement_core(
        "ImproveCore, audit yourself, learn how you work, research outside systems, and find strict-gain improvements",
        state={
            "research_needed": True,
            "external_dependency": True,
            "external_evidence": ({"status": "SATISFIED_BY_PRELOADED_RESEARCH_PACKET"},),
        },
        handlers=handlers(),
        corpus=corpus,
        observer_risk=True,
        allow_external_gap=False,
        configured_tool_adapters=configured_tool_adapters(),
    )
    state = result.result.state
    report = {
        "controller": resolution.controller,
        "entrypoint": resolution.entrypoint,
        "regime_version": REGIME_VERSION,
        "regime_status": result.status,
        "terminal": result.result.terminal,
        "mode": state.get("controller_mode"),
        "stage_trace": state.get("self_study_stage_trace"),
        "capability_snapshot": state.get("capability_snapshot"),
        "self_study_result": state.get("self_study_result"),
        "admission": state.get("admission"),
        "architecture_decision": state.get("architecture_decision"),
        "verification": state.get("verification"),
        "terminal_disposition": state.get("terminal_disposition"),
        "configured_tool_outputs": state.get("configured_tool_outputs"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    if not result.result.terminal:
        raise SystemExit("ImproveCore self-study did not reach relative close")
    if not report["verification"]["core_files_present"]:
        raise SystemExit("ImproveCore self-study core file verification failed")
    if not report["verification"]["configured_tool_execution_evidence"]:
        raise SystemExit("ImproveCore self-study did not execute configured formal tools")
    if not report["verification"]["all_configured_tools_full_36"]:
        raise SystemExit("ImproveCore self-study tool execution lost full D36_C binding")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        default=str(ROOT / "runtime/state/improvecore-self-study-104/report.json"),
    )
    args = p.parse_args()
    run(Path(args.output))

if __name__ == "__main__":
    main()
