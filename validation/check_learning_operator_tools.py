"""Self-tests for runtime.learning_operator_tools."""
from runtime.learning_operator_tools import (
    FunctionalStackState,
    OODAState,
    RateDistortionCandidate,
    bayes_update,
    d6_tool,
    d8_tool,
    functional_stack_step,
    ooda_step,
    rate_distortion_select,
)


def run():
    # D6/D8 composition order.
    d4 = lambda x: x + ["D4"]
    sense = lambda x: x + ["S"]
    orient = lambda x: x + ["O"]
    ground = lambda x: x + ["G"]
    prune = lambda x: x + ["P"]
    assert d6_tool(sense=sense, d4=d4, ground=ground)([]) == ["S", "D4", "G"]
    assert d8_tool(sense=sense, orient=orient, d4=d4, ground=ground, prune=prune)([]) == ["S", "O", "D4", "G", "P"]

    # Bayes normalization.
    posterior = bayes_update({"h1": 0.5, "h2": 0.5}, {"h1": 0.8, "h2": 0.2})
    assert abs(posterior["h1"] - 0.8) < 1e-12
    assert abs(sum(posterior.values()) - 1.0) < 1e-12

    # Functional stack uses one frozen pre-state.
    s0 = FunctionalStackState(1, 2, 3, 4)
    s1 = functional_stack_step(
        s0,
        input_layer=lambda s: s.input_layer + s.executive_layer,
        operational_layer=lambda s: s.operational_layer + s.input_layer,
        structural_layer=lambda s: s.structural_layer + s.operational_layer,
        executive_layer=lambda s: s.executive_layer + s.structural_layer,
    )
    assert s1 == FunctionalStackState(5, 3, 5, 7)

    # OODA feedback transition.
    o0 = OODAState(world=1, orientation=0)
    o1, trace = ooda_step(
        o0,
        observe=lambda world: world * 2,
        orient=lambda observation, memory: observation + memory,
        decide=lambda orientation: orientation + 1,
        act=lambda world, decision: world + decision,
    )
    assert trace.observation == 2
    assert trace.orientation == 2
    assert trace.decision == 3
    assert o1 == OODAState(world=4, orientation=2)

    # Finite R(D) selector.
    best = rate_distortion_select(
        [
            RateDistortionCandidate("a", 4.0, 0.1),
            RateDistortionCandidate("b", 2.0, 0.2),
            RateDistortionCandidate("c", 1.0, 0.5),
        ],
        max_distortion=0.25,
    )
    assert best.representation == "b"

    print("learning_operator_tools: OK")


if __name__ == "__main__":
    run()
