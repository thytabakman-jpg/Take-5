import sys
sys.path.insert(0,"runtime")

from improvement_core import improve
from learning_tool_bridge import (
    SPEC_BY_ID,
    UNIT_COST_BASIS,
    availability,
    install_learning_contracts,
    learning_ic_bundle,
    learning_package_index,
    learning_tool_contracts,
    learning_workers,
)
from math_first_selector import select_min_cost_package


BASE={
    "identity":"learning-test",
    "type":"analysis",
    "scope":"local",
    "job":"apply-lens",
    "readings":[],
    "result_sensitive":[],
    "selectors":[],
    "authority":[],
    "local_authority":[],
    "provenance":[],
    "open":[],
}


def focus(_):
    return {"exact_discriminant":True,"independent_local":True}


def test_missing_runtime_inputs_make_lens_inapplicable_not_fake_executable():
    packet=dict(BASE)
    contracts=learning_tool_contracts(packet)
    bayes=contracts["L-BAYES"]
    assert bayes["applicable"] is False
    assert set(bayes["missing_inputs"])=={"prior","likelihood"}
    assert bayes["cost_basis"]==UNIT_COST_BASIS


def test_only_supplied_typed_lens_inputs_become_applicable():
    packet={
        **BASE,
        "learning_inputs":{
            "L-BAYES":{
                "prior":{"h1":0.5,"h2":0.5},
                "likelihood":{"h1":0.8,"h2":0.2},
            }
        },
    }
    contracts=learning_tool_contracts(packet)
    assert contracts["L-BAYES"]["applicable"] is True
    assert contracts["L-DIKW"]["applicable"] is False


def test_bayes_runs_through_protected_ic_and_discharges_obligation():
    packet={
        **BASE,
        "obligations":["PROBABILISTIC_BELIEF_UPDATE"],
        "learning_inputs":{
            "L-BAYES":{
                "prior":{"h1":0.5,"h2":0.5},
                "likelihood":{"h1":0.8,"h2":0.2},
            }
        },
    }
    packet,index,workers=learning_ic_bundle(packet)
    result=improve(
        packet,
        index,
        workers,
        focus,
        package_selector=select_min_cost_package,
    )
    assert result.status=="CLOSED_RELATIVE"
    assert result.final_packet["obligations"]==[]
    posterior=result.final_packet["learning_results"]["L-BAYES"]
    assert abs(posterior["h1"]-0.8)<1e-12
    assert abs(posterior["h2"]-0.2)<1e-12
    assert result.results[0][0]=="L-BAYES"


def test_missing_inputs_preserve_open_at_ic_selection_boundary():
    packet={
        **BASE,
        "obligations":["PROBABILISTIC_BELIEF_UPDATE"],
        "learning_inputs":{},
    }
    packet,index,workers=learning_ic_bundle(packet)
    result=improve(
        packet,
        index,
        workers,
        focus,
        package_selector=select_min_cost_package,
    )
    assert result.status=="OPEN"
    assert result.final_packet["obligations"]==["PROBABILISTIC_BELIEF_UPDATE"]


def test_d6_bridge_preserves_composition_order():
    packet={
        **BASE,
        "obligations":["SENSE_CORE_GROUND"],
        "learning_inputs":{
            "L-D6":{
                "state":[],
                "sense":lambda x:x+["S"],
                "d4":lambda x:x+["D4"],
                "ground":lambda x:x+["G"],
            }
        },
    }
    packet,index,workers=learning_ic_bundle(packet)
    result=improve(
        packet,
        index,
        workers,
        focus,
        package_selector=select_min_cost_package,
    )
    assert result.status=="CLOSED_RELATIVE"
    assert result.final_packet["learning_results"]["L-D6"]==["S","D4","G"]


def test_caller_contract_override_can_change_cost_without_rewriting_bridge():
    packet={
        **BASE,
        "learning_inputs":{
            "L-BAYES":{
                "prior":{"h":1.0},
                "likelihood":{"h":1.0},
            }
        },
        "tool_contracts":{
            "L-BAYES":{"cost":0.25}
        },
    }
    installed=install_learning_contracts(packet)
    assert installed["tool_contracts"]["L-BAYES"]["cost"]==0.25
    assert installed["tool_contracts"]["L-BAYES"]["applicable"] is True


def test_all_learning_specs_have_unique_ids_and_obligations():
    ids=[x.program_id for x in SPEC_BY_ID.values()]
    obligations=[x.obligation for x in SPEC_BY_ID.values()]
    assert len(ids)==len(set(ids))
    assert len(obligations)==len(set(obligations))
    assert set(learning_package_index())==set(ids)
    assert set(learning_workers())==set(ids)
