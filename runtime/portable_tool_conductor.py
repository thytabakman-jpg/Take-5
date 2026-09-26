"""Portable, fail-closed Tool Conductor.

Tool Conductor is an exhaustive product operator over the registered tool
repertoire. It does not select, improve, or globally control the tools.

A compilation witness distinguishes:
1. program semantics recovered enough to name an executable entrypoint;
2. environment inputs still required by that program;
3. no native executable realization currently recovered.

The conductor always emits one disposition per registered tool. Missing
semantics or bindings are OPEN/BLOCKED, never silently substituted.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Mapping

from capability_runtime import execute_capability
from learning_tool_bridge import SPECS, make_learning_worker
from tool_run_registry import MATERIAL_TOOLS


@dataclass(frozen=True)
class CompilationWitness:
    tool_id: str
    status: str
    entrypoint: str | None
    required_environment: tuple[str, ...]
    self_contained: bool
    evidence: str

    def payload(self) -> dict[str, Any]:
        return asdict(self)


# Native repository entrypoints that were recovered without claiming signature
# uniformity. A portable host may bind these through adapters.
NATIVE_ENTRYPOINTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "ImprovementCore": (
        "improvement_core_dispatch.dispatch_improvement_core",
        ("handlers", "authority", "controller_context"),
    ),
    "MT": (
        "mt_semantic_return_gate.run_mt_with_before_return_gate",
        ("mt_runner", "semantic_resolver"),
    ),
    "Reconciler": ("reconcile.reconcile", ()),
    "DelegatedExecutor": ("delegation.delegate", ("worker",)),
    "HF001": ("hf1_episode.run_hf1_episode", ("execution_callbacks",)),
    "HF002": ("hf002_recursive_continuation.HF002RecursiveContinuation", ("capability_runner",)),
    "RootCause": ("root_cause.run_root_cause_hf2", ("candidate_generator",)),
    "TRC": ("tool_run_closure.run_tool_run_closure", ("consumer_bindings",)),
    "CurrentnessAudit": ("currentness_audit.assess", ()),
    "CapabilityFoundry": ("capability_foundry.CapabilityFoundry", ("foundry_callbacks",)),
    "EmergentAdmission": ("emergent_admission.admit", ()),
    "HistoricalReconstruction": ("historical_reconstruction.compare", ()),
    "ZeroRequest": ("zero_request_episode.zero_request_episode", ("observation_source",)),
    "ASSERT": ("assert_compound.run_to_fixed_point", ("assert_stage_bindings",)),
    "SolutionToMyProblem": ("solution_to_my_problem.solve", ()),
    "DesiredJane": ("desired_jane.recover_desired_jane", ()),
    "QuestionWorthAsking": ("question_worth_asking.select_question", ()),
    "LambdaMath": ("lambda_math.reconstruct", ()),
    "SemanticResolutionPipeline": (
        "semantic_resolution_pipeline.plan_black_box_resolution",
        ("semantic_resolution_workers",),
    ),
}


def _learning_spec(tool_id: str):
    for spec in SPECS:
        if spec.program_id == tool_id:
            return spec
    return None


def compilation_witness(tool_id: str) -> CompilationWitness:
    if tool_id == "ToolConductor":
        return CompilationWitness(
            tool_id,
            "SELF_WITNESS",
            "portable_tool_conductor.run_tool_conductor",
            (),
            True,
            "anti-recursive self execution is represented by a self receipt",
        )

    if tool_id.startswith("C") and tool_id[1:].isdigit() and 1 <= int(tool_id[1:]) <= 49:
        return CompilationWitness(
            tool_id,
            "PROGRAM_RECOVERED",
            "capability_runtime.execute_capability",
            (),
            True,
            "Take-5 capability runtime directly dispatches C01-C49",
        )

    spec = _learning_spec(tool_id)
    if spec is not None:
        env = tuple(spec.callable_fields)
        return CompilationWitness(
            tool_id,
            "PROGRAM_RECOVERED" if not env else "PROGRAM_WITH_ENVIRONMENT",
            f"learning_tool_bridge.make_learning_worker:{tool_id}",
            env,
            not env,
            "learning operator runtime is executable; caller-supplied semantic functions remain explicit inputs",
        )

    native = NATIVE_ENTRYPOINTS.get(tool_id)
    if native is not None:
        entrypoint, env = native
        return CompilationWitness(
            tool_id,
            "PROGRAM_RECOVERED" if not env else "PROGRAM_WITH_ENVIRONMENT",
            entrypoint,
            tuple(env),
            not env,
            "native Take-5 runtime entrypoint recovered",
        )

    return CompilationWitness(
        tool_id,
        "OPEN_NATIVE_RUNTIME",
        None,
        (),
        False,
        "no native executable realization recovered without semantic substitution",
    )


def compile_repertoire() -> tuple[CompilationWitness, ...]:
    return tuple(compilation_witness(tool_id) for tool_id in MATERIAL_TOOLS)


def portability_open_set() -> tuple[str, ...]:
    return tuple(
        w.tool_id for w in compile_repertoire()
        if not w.self_contained
    )


def portability_closed() -> bool:
    return not portability_open_set()


def _run_learning(tool_id: str, packet: Mapping[str, Any]) -> dict[str, Any]:
    worker = make_learning_worker(tool_id)
    raw = worker(packet)
    status = (raw.get("learning_status", {}).get(tool_id, {}) or {}).get("status", "OPEN")
    return {
        "tool_id": tool_id,
        "status": "EXECUTED" if status == "ACCEPT" else "OPEN",
        "result": raw,
        "witness": compilation_witness(tool_id).payload(),
    }


def run_tool_conductor(
    packet: Mapping[str, Any],
    *,
    adapters: Mapping[str, Callable[[Mapping[str, Any]], Any]] | None = None,
) -> dict[str, Any]:
    """Attempt every registered tool exactly once at the conductor layer.

    Tool-specific recurrence remains owned by each configured tool. The
    conductor itself does not recursively call itself.
    """
    adapters = dict(adapters or {})
    capability_inputs = packet.get("capability_inputs", {}) or {}
    results = []

    for tool_id in MATERIAL_TOOLS:
        witness = compilation_witness(tool_id)

        if tool_id == "ToolConductor":
            results.append({
                "tool_id": tool_id,
                "status": "EXECUTED_SELF_WITNESS",
                "result": {"self_application": "represented_without_recursive_spawn"},
                "witness": witness.payload(),
            })
            continue

        if tool_id.startswith("C") and tool_id[1:].isdigit() and 1 <= int(tool_id[1:]) <= 49:
            payload = capability_inputs.get(tool_id, {})
            try:
                out = execute_capability(tool_id, payload)
                status = "EXECUTED"
            except Exception as exc:
                out = {"error": type(exc).__name__, "message": str(exc)}
                status = "BLOCKED"
            results.append({
                "tool_id": tool_id,
                "status": status,
                "result": out,
                "witness": witness.payload(),
            })
            continue

        if _learning_spec(tool_id) is not None:
            results.append(_run_learning(tool_id, packet))
            continue

        adapter = adapters.get(tool_id)
        if adapter is not None:
            try:
                out = adapter(packet)
                status = "EXECUTED"
            except Exception as exc:
                out = {"error": type(exc).__name__, "message": str(exc)}
                status = "BLOCKED"
            results.append({
                "tool_id": tool_id,
                "status": status,
                "result": out,
                "witness": witness.payload(),
            })
            continue

        results.append({
            "tool_id": tool_id,
            "status": "OPEN" if witness.entrypoint else "BLOCKED",
            "result": {
                "reason": "PORTABLE_ADAPTER_REQUIRED" if witness.entrypoint else "NATIVE_PROGRAM_UNRECOVERED",
                "required_environment": witness.required_environment,
            },
            "witness": witness.payload(),
        })

    seen = tuple(r["tool_id"] for r in results)
    if seen != tuple(MATERIAL_TOOLS):
        raise RuntimeError("TOOL_CONDUCTOR_COVERAGE_MISMATCH")

    open_tools = tuple(r["tool_id"] for r in results if r["status"] in {"OPEN", "BLOCKED"})
    return {
        "status": "COMPLETE" if not open_tools else "OPEN",
        "tool_count": len(results),
        "results": tuple(results),
        "open_tools": open_tools,
        "portability_closed": portability_closed(),
        "portability_open_set": portability_open_set(),
    }
