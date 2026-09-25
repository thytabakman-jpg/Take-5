"""Typed learning/operator toolkit.

This module implements generic composition and numeric primitives for the
formal tools documented in architecture/LEARNING_OPERATOR_TOOLKIT_035.md.

Domain-specific semantics remain callbacks.  The code deliberately does not
invent likelihoods, utilities, distortion functions, grounding tests, or
environment dynamics.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Any, Callable, Hashable, Iterable, Mapping, MutableMapping, Sequence, TypeVar

X = TypeVar("X")
E = TypeVar("E")
R = TypeVar("R")
C = TypeVar("C")
A = TypeVar("A")
Z = TypeVar("Z")
H = TypeVar("H", bound=Hashable)

Endo = Callable[[X], X]


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Return standard right-to-left mathematical composition."""
    def run(value: Any) -> Any:
        out = value
        for fn in reversed(functions):
            out = fn(out)
        return out
    return run


def d6_tool(*, sense: Endo[X], d4: Endo[X], ground: Endo[X]) -> Endo[X]:
    """D6 = Ground o D4 o Sense."""
    return compose(ground, d4, sense)


def d8_tool(
    *,
    sense: Endo[X],
    orient: Endo[X],
    d4: Endo[X],
    ground: Endo[X],
    prune: Endo[X],
) -> Endo[X]:
    """D8 = Prune o Ground o D4 o Orient o Sense."""
    return compose(prune, ground, d4, orient, sense)


@dataclass(frozen=True)
class KolbTrace:
    experience_in: Any
    reflection: Any
    concept: Any
    experiment: Any
    experience_out: Any


def kolb_cycle(
    experience: E,
    *,
    reflect: Callable[[E], R],
    abstract: Callable[[R], C],
    experiment: Callable[[C], A],
    enact: Callable[[A], E],
) -> KolbTrace:
    """One E -> R -> C -> A -> E experiential-learning cycle."""
    r = reflect(experience)
    c = abstract(r)
    a = experiment(c)
    e2 = enact(a)
    return KolbTrace(experience, r, c, a, e2)


@dataclass(frozen=True)
class DIKWResult:
    information: Any
    model: Any
    action: Any
    model_score: float
    action_score: float


def dikw_tool(
    data: Any,
    context: Any,
    *,
    contextualize: Callable[[Any, Any], Any],
    models: Iterable[Any],
    description_length: Callable[[Any, Any], float],
    actions: Iterable[Any],
    expected_utility: Callable[[Any, Any], float],
) -> DIKWResult:
    """Project DIKW formalization: context -> MDL model -> max-EU action."""
    information = contextualize(data, context)
    model, mscore = min(
        ((m, float(description_length(m, information))) for m in models),
        key=lambda pair: pair[1],
    )
    action, ascore = max(
        ((a, float(expected_utility(model, a))) for a in actions),
        key=lambda pair: pair[1],
    )
    return DIKWResult(information, model, action, mscore, ascore)


@dataclass(frozen=True)
class FunctionalStackState:
    input_layer: Any
    operational_layer: Any
    structural_layer: Any
    executive_layer: Any


def functional_stack_step(
    state: FunctionalStackState,
    *,
    input_layer: Callable[[FunctionalStackState], Any],
    operational_layer: Callable[[FunctionalStackState], Any],
    structural_layer: Callable[[FunctionalStackState], Any],
    executive_layer: Callable[[FunctionalStackState], Any],
) -> FunctionalStackState:
    """Synchronous coupled update: every layer reads the same frozen state."""
    return FunctionalStackState(
        input_layer=input_layer(state),
        operational_layer=operational_layer(state),
        structural_layer=structural_layer(state),
        executive_layer=executive_layer(state),
    )


@dataclass(frozen=True)
class OODAState:
    world: Any
    orientation: Any


@dataclass(frozen=True)
class OODATrace:
    observation: Any
    orientation: Any
    decision: Any
    world_out: Any


def ooda_step(
    state: OODAState,
    *,
    observe: Callable[[Any], Any],
    orient: Callable[[Any, Any], Any],
    decide: Callable[[Any], Any],
    act: Callable[[Any, Any], Any],
) -> tuple[OODAState, OODATrace]:
    """One feedback OODA transition."""
    observation = observe(state.world)
    orientation = orient(observation, state.orientation)
    decision = decide(orientation)
    world_out = act(state.world, decision)
    return (
        OODAState(world_out, orientation),
        OODATrace(observation, orientation, decision, world_out),
    )


def bayes_update(
    prior: Mapping[H, float],
    likelihood: Mapping[H, float],
) -> dict[H, float]:
    """Discrete posterior p(h|o) proportional to p(o|h)p(h)."""
    weights = {h: float(prior[h]) * float(likelihood[h]) for h in prior}
    evidence = sum(weights.values())
    if evidence <= 0.0:
        raise ValueError("Bayesian update requires positive evidence.")
    return {h: w / evidence for h, w in weights.items()}


def kl_divergence(q: Mapping[H, float], p: Mapping[H, float]) -> float:
    """D_KL(q || p) for finite discrete distributions."""
    total = 0.0
    for h, qh in q.items():
        if qh < 0.0:
            raise ValueError("Probabilities must be nonnegative.")
        if qh == 0.0:
            continue
        ph = float(p.get(h, 0.0))
        if ph <= 0.0:
            return float("inf")
        total += qh * log(qh / ph)
    return total


def variational_free_energy(
    q: Mapping[H, float],
    prior: Mapping[H, float],
    neg_log_likelihood: Mapping[H, float],
) -> float:
    """Accuracy/complexity form: E_q[-log p(o|h)] + KL(q||prior)."""
    accuracy_cost = sum(float(q[h]) * float(neg_log_likelihood[h]) for h in q)
    return accuracy_cost + kl_divergence(q, prior)


def active_inference_policy(
    policies: Sequence[Any],
    *,
    expected_free_energy: Callable[[Any], float],
) -> Any:
    """Deterministic argmin policy under supplied expected free energy."""
    if not policies:
        raise ValueError("At least one policy is required.")
    return min(policies, key=lambda p: float(expected_free_energy(p)))


def softmax_negative(values: Mapping[H, float], precision: float = 1.0) -> dict[H, float]:
    """P(k) proportional to exp(-precision * value[k])."""
    if precision <= 0.0:
        raise ValueError("precision must be positive.")
    if not values:
        raise ValueError("values cannot be empty.")
    scaled = {k: -precision * float(v) for k, v in values.items()}
    m = max(scaled.values())
    weights = {k: exp(v - m) for k, v in scaled.items()}
    z = sum(weights.values())
    return {k: w / z for k, w in weights.items()}


@dataclass(frozen=True)
class ActorCriticStep:
    td_error: float
    value_parameters: Any
    policy_parameters: Any


def actor_critic_step(
    *,
    reward: float,
    discount: float,
    value_now: float,
    value_next: float,
    value_parameters: Any,
    policy_parameters: Any,
    critic_update: Callable[[Any, float], Any],
    actor_update: Callable[[Any, float], Any],
) -> ActorCriticStep:
    """Generic one-step actor-critic using TD error as the shared signal.

    The gradient parameterization is delegated to critic_update and actor_update.
    """
    if not 0.0 <= discount <= 1.0:
        raise ValueError("discount must be in [0,1].")
    delta = float(reward) + discount * float(value_next) - float(value_now)
    return ActorCriticStep(
        td_error=delta,
        value_parameters=critic_update(value_parameters, delta),
        policy_parameters=actor_update(policy_parameters, delta),
    )


@dataclass(frozen=True)
class RateDistortionCandidate:
    representation: Any
    mutual_information: float
    expected_distortion: float


def rate_distortion_select(
    candidates: Iterable[RateDistortionCandidate],
    *,
    max_distortion: float,
) -> RateDistortionCandidate:
    """Finite candidate approximation to R(D): min I subject to distortion <= D."""
    feasible = [c for c in candidates if c.expected_distortion <= max_distortion]
    if not feasible:
        raise ValueError("No representation satisfies the distortion constraint.")
    return min(feasible, key=lambda c: c.mutual_information)


@dataclass(frozen=True)
class PredictiveProcessingResult:
    prediction: Any
    error: Any
    revised_model: Any
    objective: float


def predictive_processing_step(
    observation: Any,
    model: Any,
    *,
    predict: Callable[[Any], Any],
    prediction_error: Callable[[Any, Any], Any],
    revise: Callable[[Any, Any, Any], tuple[Any, float]],
) -> PredictiveProcessingResult:
    """Generic predict -> error -> model-revision step.

    revise receives (model, observation, error) and must return
    (revised_model, objective_value).  The caller chooses the exact
    variational/prediction-error objective.
    """
    prediction = predict(model)
    error = prediction_error(observation, prediction)
    revised, objective = revise(model, observation, error)
    return PredictiveProcessingResult(
        prediction=prediction,
        error=error,
        revised_model=revised,
        objective=float(objective),
    )
