"""Function-first configured-tool IR experiment.

This module operationalizes the September 25-26 function-first discovery without
changing PD's canonical goal or claiming that every semantic object is an
ordinary deterministic function.

Underlying semantics may remain relational/set-valued:

    R_{T,K}: X_T \rightrightarrows Y_T

The canonical configured surface is:

    T^cfg_{J,K}: I_T -> R_T

with branch-coupled results:

    B_T = Y_T x Sigma_T x D^b_T x W^b_T
    R_T = P(B_T) x D^i_T x W^i_T x Receipt_T

The experiment derives as much of that identity as current Take-5 evidence
permits and leaves missing identity/runtime coordinates OPEN/BLOCKED.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any

from portable_tool_conductor import compilation_witness
from tool_manifest import OVERRIDES, manifest_for
from tool_run_registry import CONFIGURED_RUNS


HOLDOUT = (
    "PD",
    "PDAudit",
    "MT",
    "Architecture",
    "ICC123",
    "ICC128",
    "ImprovementCore",
    "ToolConductor",
)


@dataclass(frozen=True)
class FunctionIRIdentity:
    object_id: str
    registered: bool
    semantic_relation: str
    configured_function: str
    input_carrier: str
    branch_carrier: str
    output_carrier: str
    expression: tuple[tuple[str, Any], ...]
    configured_identity_status: str
    realization_status: str
    runtime_entrypoint: str | None
    required_environment: tuple[str, ...]
    residuals: tuple[str, ...]

    def payload(self) -> dict[str, Any]:
        return asdict(self)

    def stable_hash(self) -> str:
        raw=json.dumps(self.payload(),sort_keys=True,separators=(",",":"),default=str)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _symbol(tool_id: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in tool_id)


def blocked_unregistered(object_id: str) -> FunctionIRIdentity:
    sym=_symbol(object_id)
    return FunctionIRIdentity(
        object_id=object_id,
        registered=False,
        semantic_relation=f"R_{{{sym},K}}: X_{{{sym}}} \\rightrightarrows Y_{{{sym}}}",
        configured_function=f"{sym}^cfg_{{J,K}}: I_{{{sym}}} -> R_{{{sym}}}",
        input_carrier=f"I_{{{sym}}}=X_{{{sym}}} x Sigma_{{{sym}}} x Context_{{{sym}}}",
        branch_carrier=f"B_{{{sym}}}=Y_{{{sym}}} x Sigma_{{{sym}}} x D^b_{{{sym}}} x W^b_{{{sym}}}",
        output_carrier=f"R_{{{sym}}}=P(B_{{{sym}}}) x D^i_{{{sym}}} x W^i_{{{sym}}} x Receipt_{{{sym}}}",
        expression=(("BLOCKED","UNREGISTERED_NAMED_OBJECT"),),
        configured_identity_status="BLOCKED",
        realization_status="BLOCKED",
        runtime_entrypoint=None,
        required_environment=(),
        residuals=("UNREGISTERED_NAMED_OBJECT",),
    )


def encode_registered_tool(tool_id: str) -> FunctionIRIdentity:
    if tool_id not in CONFIGURED_RUNS:
        return blocked_unregistered(tool_id)

    spec=CONFIGURED_RUNS[tool_id]
    manifest=manifest_for(tool_id)
    witness=compilation_witness(tool_id)
    sym=_symbol(tool_id)

    residuals=[]
    explicit_manifest=tool_id in OVERRIDES
    if not explicit_manifest:
        residuals.append("GENERIC_ONLY_MANIFEST")
    if not spec.complete():
        residuals.append("CONFIGURED_RUN_INCOMPLETE")

    configured_status="CLOSED_RELATIVE" if not residuals else "OPEN"

    if witness.entrypoint is None:
        realization_status="UNRECOVERED"
        residuals.append("NATIVE_RUNTIME_UNRECOVERED")
    elif witness.required_environment:
        realization_status="ENVIRONMENT_BOUND"
    else:
        realization_status="SELF_CONTAINED"

    expression=(
        ("NATIVE",manifest.native_semantics),
        ("WRAP",tuple(b.behavior_id for b in manifest.bindings)),
        ("LIFT",spec.geometry),
        ("MODE",spec.default_mode),
        ("RECUR",bool(spec.recursive)),
        ("CLOSE",bool(spec.closure_required)),
        ("REENTRY",bool(spec.reentry_required)),
        ("CHALLENGE",spec.external_challenge),
        ("PROTECTED_TRANSITION",bool(spec.protected_transition_required)),
        ("COMPILE",witness.entrypoint or "OPEN"),
    )

    return FunctionIRIdentity(
        object_id=tool_id,
        registered=True,
        semantic_relation=f"R_{{{sym},K}}: X_{{{sym}}} \\rightrightarrows Y_{{{sym}}}",
        configured_function=f"{sym}^cfg_{{J,K}}: I_{{{sym}}} -> R_{{{sym}}}",
        input_carrier=f"I_{{{sym}}}=X_{{{sym}}} x Sigma_{{{sym}}} x Context_{{{sym}}}",
        branch_carrier=f"B_{{{sym}}}=Y_{{{sym}}} x Sigma_{{{sym}}} x D^b_{{{sym}}} x W^b_{{{sym}}}",
        output_carrier=f"R_{{{sym}}}=P(B_{{{sym}}}) x D^i_{{{sym}}} x W^i_{{{sym}}} x Receipt_{{{sym}}}",
        expression=expression,
        configured_identity_status=configured_status,
        realization_status=realization_status,
        runtime_entrypoint=witness.entrypoint,
        required_environment=tuple(witness.required_environment),
        residuals=tuple(residuals),
    )


def encode(object_id: str) -> FunctionIRIdentity:
    return encode_registered_tool(str(object_id))


def audit_holdout(objects=HOLDOUT) -> dict[str, Any]:
    rows=tuple(encode(object_id) for object_id in objects)
    blocked=tuple(r.object_id for r in rows if r.configured_identity_status=="BLOCKED")
    open_identity=tuple(r.object_id for r in rows if r.configured_identity_status=="OPEN")
    environment_bound=tuple(r.object_id for r in rows if r.realization_status=="ENVIRONMENT_BOUND")
    unrecovered_runtime=tuple(r.object_id for r in rows if r.realization_status=="UNRECOVERED")
    self_contained=tuple(r.object_id for r in rows if r.realization_status=="SELF_CONTAINED")

    return {
        "schema":"FUNCTION_FIRST_CONFIGURED_IR_001",
        "equations":{
            "semantic":"R_{T,K}: X_T \\rightrightarrows Y_T",
            "configured":"T^cfg_{J,K}: I_T -> R_T",
            "input":"I_T=X_T x Sigma_T x Context_T",
            "branch":"B_T=Y_T x Sigma_T x D^b_T x W^b_T",
            "output":"R_T=P(B_T) x D^i_T x W^i_T x Receipt_T",
        },
        "rows":tuple(r.payload() | {"stable_hash":r.stable_hash()} for r in rows),
        "blocked_unregistered":blocked,
        "open_configured_identity":open_identity,
        "environment_bound":environment_bound,
        "unrecovered_runtime":unrecovered_runtime,
        "self_contained":self_contained,
        "promotion_ready":not (blocked or open_identity or unrecovered_runtime),
        "pd_goal_changed":False,
    }
