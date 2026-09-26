import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from show_me_the_math_contract import (
    assess_show_math_package,
    is_show_me_the_math_request,
    status_for_symbol,
)

def complete_package():
    return {
        "full_math":"<N,W,G,P,L>",
        "run_spec":"<T,W,G,R,C,H>",
        "definitions":{
            "T":{"dependencies":["rho","state"]},
            "rho":{"dependencies":["primitive_add"]},
            "state":{"dependencies":[]},
        },
        "load_bearing_symbols":["T"],
        "initialization":{"defined":True},
        "runtime_primitives":{
            "primitive_add":{"typed_contract":"R x R -> R","available":True}
        },
        "persistence":{"specified":True},
        "protected_behavior":["same-output"],
        "equivalence_tests":["protected-observable-equivalence"],
    }

def test_phrase_resolves_to_show_math_job():
    assert is_show_me_the_math_request("Please show me the math for this tool")
    assert is_show_me_the_math_request("Give me the actual math")

def test_recursive_symbol_closure_passes_when_definitions_bottom_out():
    result=assess_show_math_package(complete_package())
    assert result.complete
    assert result.unresolved_symbols==()

def test_hidden_symbol_fails_closed():
    package=complete_package()
    package["definitions"]["rho"]={"dependencies":["mystery"]}
    result=assess_show_math_package(package)
    assert not result.complete
    assert "mystery" in result.unresolved_symbols
    assert "mystery" in result.hidden_dependencies

def test_untyped_or_unavailable_primitive_fails_closed():
    package=complete_package()
    package["runtime_primitives"]["primitive_add"]={"typed_contract":"","available":False}
    result=assess_show_math_package(package)
    assert not result.complete
    assert "primitive_add" in result.unresolved_symbols
    assert "primitive_add" in result.unavailable_primitives

def test_symbol_color_is_job_relative_and_fail_closed():
    package=complete_package()
    assert status_for_symbol(package,"T")=="GREEN"
    assert status_for_symbol(package,"unknown")=="RED"
