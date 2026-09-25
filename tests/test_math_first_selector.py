import sys
sys.path.insert(0,"runtime")

from hf_controller import decide
from math_first_selector import (
    ToolContract,
    select_min_cost_cover,
    select_min_cost_package,
)

BASE={
    "identity":"i",
    "type":"t",
    "scope":"s",
    "job":"j",
    "readings":[],
    "result_sensitive":[],
    "selectors":[],
    "authority":[],
    "provenance":[],
    "open":[],
}


def test_exact_weighted_cover_beats_single_expensive_max_hit_tool():
    result=select_min_cost_cover(
        ("A","B"),
        (
            ToolContract("T1",frozenset({"A","B"}),cost=5.0),
            ToolContract("T2",frozenset({"A"}),cost=1.0),
            ToolContract("T3",frozenset({"B"}),cost=1.0),
        ),
    )
    assert result.status=="SELECTED"
    assert result.package==("T2","T3")
    assert result.total_cost==2.0


def test_selector_preserves_open_when_coverage_is_incomplete():
    result=select_min_cost_cover(
        ("A","B"),
        (ToolContract("T2",frozenset({"A"}),cost=1.0),),
    )
    assert result.status=="OPEN"
    assert result.uncovered==frozenset({"B"})


def test_hf_default_behavior_is_unchanged_but_math_first_is_opt_in():
    packet=dict(BASE)
    packet["obligations"]=["A","B"]
    package_index={"T1":["A","B"],"T2":["A"],"T3":["B"]}
    flags={"exact_discriminant":True,"independent_local":True}

    old=decide(packet,package_index,flags)
    assert old.package==("T1",)

    packet["tool_contracts"]={
        "T1":{"cost":5.0},
        "T2":{"cost":1.0},
        "T3":{"cost":1.0},
    }
    new=decide(
        packet,
        package_index,
        flags,
        package_selector=select_min_cost_package,
    )
    assert new.package==("T2","T3")
    assert new.action=="EXECUTE"
