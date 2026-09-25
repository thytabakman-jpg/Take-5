"""Typed admission bridge from the learning-operator toolkit into Improvement Core.

The bridge does not make every mathematical lens globally applicable.  It
exposes each lens as an IC-selectable package only when the packet supplies the
typed runtime inputs required by that lens.

Costs are neutral unit priors until empirical calibration replaces them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from learning_operator_tools import (
    actor_critic_step,
    active_inference_policy,
    bayes_update,
    d6_tool,
    d8_tool,
    dikw_tool,
    functional_stack_step,
    kolb_cycle,
    ooda_step,
    predictive_processing_step,
    rate_distortion_select,
)


UNIT_COST_BASIS = "UNCALIBRATED_UNIT_COST"


@dataclass(frozen=True)
class LearningToolSpec:
    program_id: str
    obligation: str
    input_type: str
    output_type: str
    required_fields: tuple[str, ...]
    callable_fields: tuple[str, ...] = ()
    cost: float = 1.0

    @property
    def covers(self) -> frozenset[str]:
        return frozenset((self.obligation,))


SPECS = (
    LearningToolSpec(
        "L-D6",
        "SENSE_CORE_GROUND",
        "State + Sense + D4 + Ground",
        "GroundedState",
        ("state", "sense", "d4", "ground"),
        ("sense", "d4", "ground"),
    ),
    LearningToolSpec(
        "L-D8",
        "SENSE_ORIENT_CORE_GROUND_PRUNE",
        "State + Sense + Orient + D4 + Ground + Prune",
        "PrunedGroundedState",
        ("state", "sense", "orient", "d4", "ground", "prune"),
        ("sense", "orient", "d4", "ground", "prune"),
    ),
    LearningToolSpec(
        "L-KOLB",
        "EXPERIENTIAL_LEARNING_CYCLE",
        "Experience + Reflect + Abstract + Experiment + Enact",
        "KolbTrace",
        ("experience", "reflect", "abstract", "experiment", "enact"),
        ("reflect", "abstract", "experiment", "enact"),
    ),
    LearningToolSpec(
        "L-DIKW",
        "DATA_TO_ACTION_MODEL",
        "Data + Context + ModelClass + ActionSet",
        "DIKWResult",
        (
            "data", "context", "contextualize", "models", "description_length",
            "actions", "expected_utility",
        ),
        ("contextualize", "description_length", "expected_utility"),
    ),
    LearningToolSpec(
        "L-PP",
        "PREDICTION_ERROR_MODEL_REVISION",
        "Observation + Model + Predict + Error + Revise",
        "PredictiveProcessingResult",
        ("observation", "model", "predict", "prediction_error", "revise"),
        ("predict", "prediction_error", "revise"),
    ),
    LearningToolSpec(
        "L-BAYES",
        "PROBABILISTIC_BELIEF_UPDATE",
        "PriorDistribution + Likelihood",
        "PosteriorDistribution",
        ("prior", "likelihood"),
    ),
    LearningToolSpec(
        "L-ACTIVE-INFERENCE",
        "FREE_ENERGY_POLICY_SELECTION",
        "Policies + ExpectedFreeEnergy",
        "SelectedPolicy",
        ("policies", "expected_free_energy"),
        ("expected_free_energy",),
    ),
    LearningToolSpec(
        "L-ACTOR-CRITIC",
        "REWARD_DRIVEN_POLICY_VALUE_UPDATE",
        "Transition + ValueParameters + PolicyParameters",
        "ActorCriticStep",
        (
            "reward", "discount", "value_now", "value_next",
            "value_parameters", "policy_parameters",
            "critic_update", "actor_update",
        ),
        ("critic_update", "actor_update"),
    ),
    LearningToolSpec(
        "L-RATE-DISTORTION",
        "FIDELITY_CONSTRAINED_COMPRESSION",
        "RepresentationCandidates + DistortionBudget",
        "RateDistortionCandidate",
        ("candidates", "max_distortion"),
    ),
    LearningToolSpec(
        "L-OODA",
        "FEEDBACK_DECISION_ACTION",
        "OODAState + Observe + Orient + Decide + Act",
        "OODAState + OODATrace",
        ("state", "observe", "orient", "decide", "act"),
        ("observe", "orient", "decide", "act"),
    ),
    LearningToolSpec(
        "L-FUNCTIONAL-STACK",
        "COUPLED_LAYER_UPDATE",
        "FunctionalStackState + FourLayerMaps",
        "FunctionalStackState",
        (
            "state", "input_layer", "operational_layer",
            "structural_layer", "executive_layer",
        ),
        ("input_layer", "operational_layer", "structural_layer", "executive_layer"),
    ),
)

SPEC_BY_ID = {spec.program_id: spec for spec in SPECS}


def _inputs(packet: Mapping[str, Any], program_id: str) -> Mapping[str, Any]:
    all_inputs = packet.get("learning_inputs", {}) or {}
    value = all_inputs.get(program_id, {}) or {}
    return value if isinstance(value, Mapping) else {}


def availability(packet: Mapping[str, Any], spec: LearningToolSpec) -> tuple[bool, tuple[str, ...]]:
    data = _inputs(packet, spec.program_id)
    missing = []
    for field in spec.required_fields:
        if field not in data:
            missing.append(field)
    for field in spec.callable_fields:
        if field in data and not callable(data[field]):
            missing.append(f"{field}:NOT_CALLABLE")
    return (not missing, tuple(missing))


def learning_package_index() -> dict[str, tuple[str, ...]]:
    return {spec.program_id: (spec.obligation,) for spec in SPECS}


def learning_tool_contracts(packet: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Return math-first-selector metadata for every learning lens."""
    contracts = {}
    for spec in SPECS:
        ok, missing = availability(packet, spec)
        contracts[spec.program_id] = {
            "covers": (spec.obligation,),
            "cost": float(spec.cost),
            "cost_basis": UNIT_COST_BASIS,
            "input_type": spec.input_type,
            "output_type": spec.output_type,
            "applicable": ok,
            "licensed": True,
            "missing_inputs": missing,
        }
    return contracts


def install_learning_contracts(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy of packet with learning contracts merged, never overwriting caller overrides."""
    out = dict(packet)
    existing = dict(out.get("tool_contracts", {}) or {})
    generated = learning_tool_contracts(out)
    for pid, contract in generated.items():
        if pid in existing:
            merged = dict(contract)
            merged.update(existing[pid] or {})
            existing[pid] = merged
        else:
            existing[pid] = contract
    out["tool_contracts"] = existing
    return out


def _execute(program_id: str, data: Mapping[str, Any]) -> Any:
    if program_id == "L-D6":
        return d6_tool(
            sense=data["sense"],
            d4=data["d4"],
            ground=data["ground"],
        )(data["state"])

    if program_id == "L-D8":
        return d8_tool(
            sense=data["sense"],
            orient=data["orient"],
            d4=data["d4"],
            ground=data["ground"],
            prune=data["prune"],
        )(data["state"])

    if program_id == "L-KOLB":
        return kolb_cycle(
            data["experience"],
            reflect=data["reflect"],
            abstract=data["abstract"],
            experiment=data["experiment"],
            enact=data["enact"],
        )

    if program_id == "L-DIKW":
        return dikw_tool(
            data["data"],
            data["context"],
            contextualize=data["contextualize"],
            models=data["models"],
            description_length=data["description_length"],
            actions=data["actions"],
            expected_utility=data["expected_utility"],
        )

    if program_id == "L-PP":
        return predictive_processing_step(
            data["observation"],
            data["model"],
            predict=data["predict"],
            prediction_error=data["prediction_error"],
            revise=data["revise"],
        )

    if program_id == "L-BAYES":
        return bayes_update(data["prior"], data["likelihood"])

    if program_id == "L-ACTIVE-INFERENCE":
        return active_inference_policy(
            data["policies"],
            expected_free_energy=data["expected_free_energy"],
        )

    if program_id == "L-ACTOR-CRITIC":
        return actor_critic_step(
            reward=data["reward"],
            discount=data["discount"],
            value_now=data["value_now"],
            value_next=data["value_next"],
            value_parameters=data["value_parameters"],
            policy_parameters=data["policy_parameters"],
            critic_update=data["critic_update"],
            actor_update=data["actor_update"],
        )

    if program_id == "L-RATE-DISTORTION":
        return rate_distortion_select(
            data["candidates"],
            max_distortion=data["max_distortion"],
        )

    if program_id == "L-OODA":
        return ooda_step(
            data["state"],
            observe=data["observe"],
            orient=data["orient"],
            decide=data["decide"],
            act=data["act"],
        )

    if program_id == "L-FUNCTIONAL-STACK":
        return functional_stack_step(
            data["state"],
            input_layer=data["input_layer"],
            operational_layer=data["operational_layer"],
            structural_layer=data["structural_layer"],
            executive_layer=data["executive_layer"],
        )

    raise KeyError(program_id)


def make_learning_worker(program_id: str) -> Callable[[Mapping[str, Any]], dict[str, Any]]:
    spec = SPEC_BY_ID[program_id]

    def worker(packet: Mapping[str, Any]) -> dict[str, Any]:
        ok, missing = availability(packet, spec)
        if not ok:
            return {
                "learning_status": {
                    program_id: {
                        "status": "OPEN",
                        "missing_inputs": missing,
                    }
                }
            }

        result = _execute(program_id, _inputs(packet, program_id))
        results = dict(packet.get("learning_results", {}) or {})
        results[program_id] = result

        obligations = [
            o for o in packet.get("obligations", ())
            if o not in spec.covers
        ]

        status = dict(packet.get("learning_status", {}) or {})
        status[program_id] = {
            "status": "ACCEPT",
            "cost_basis": UNIT_COST_BASIS,
        }

        return {
            "learning_results": results,
            "learning_status": status,
            "obligations": obligations,
        }

    return worker


def learning_workers() -> dict[str, Callable[[Mapping[str, Any]], dict[str, Any]]]:
    return {spec.program_id: make_learning_worker(spec.program_id) for spec in SPECS}


def learning_ic_bundle(packet: Mapping[str, Any]):
    """Return (packet_with_contracts, package_index, workers) for direct IC use."""
    return (
        install_learning_contracts(packet),
        learning_package_index(),
        learning_workers(),
    )
