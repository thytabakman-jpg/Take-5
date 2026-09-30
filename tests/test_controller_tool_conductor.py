import sys
sys.path.insert(0,"runtime")

from controller_tool_conductor import consult_registered_repertoire
from tool_run_registry import MATERIAL_TOOLS


def _rows():
    return tuple({
        "tool_id":tool_id,
        "status":"OPEN",
        "result":{"reason":"fixture"},
        "configured_plan":{"tool_id":tool_id},
    } for tool_id in MATERIAL_TOOLS)


def test_complete_traversal_is_admitted_even_when_individual_factors_are_open():
    def runner(packet,adapters=None):
        rows=_rows()
        return {
            "status":"OPEN",
            "tool_count":len(rows),
            "results":rows,
            "open_tools":tuple(MATERIAL_TOOLS),
        }

    out=consult_registered_repertoire(
        {"job":"test"},
        active_controller="ImprovementCore",
        conductor_runner=runner,
    )
    assert out.coverage_complete
    assert out.status=="COMPLETE"
    assert out.conductor_status=="OPEN"
    assert out.open_tools==tuple(MATERIAL_TOOLS)


def test_active_controller_adapter_is_not_forwarded_into_nested_conductor():
    seen={}
    def runner(packet,adapters=None):
        seen["adapters"]=dict(adapters or {})
        rows=_rows()
        return {
            "status":"OPEN",
            "tool_count":len(rows),
            "results":rows,
            "open_tools":tuple(MATERIAL_TOOLS),
        }

    out=consult_registered_repertoire(
        {},
        active_controller="ImprovementCore",
        adapters={
            "ImprovementCore":lambda x:x,
            "RootCause":lambda x:x,
        },
        conductor_runner=runner,
    )
    assert out.coverage_complete
    assert "ImprovementCore" not in seen["adapters"]
    assert "RootCause" in seen["adapters"]


def test_missing_registered_factor_fails_consultation_coverage():
    def runner(packet,adapters=None):
        rows=_rows()[:-1]
        return {
            "status":"OPEN",
            "tool_count":len(rows),
            "results":rows,
            "open_tools":tuple(row["tool_id"] for row in rows),
        }

    out=consult_registered_repertoire(
        {},
        active_controller="ICC128",
        conductor_runner=runner,
    )
    assert not out.coverage_complete
    assert out.status=="OPEN"
    assert out.blocker=="TOOL_CONDUCTOR_TOOL_COUNT_MISMATCH"


def test_reordered_factor_identity_fails_closed():
    def runner(packet,adapters=None):
        rows=list(_rows())
        rows[0],rows[1]=rows[1],rows[0]
        return {
            "status":"OPEN",
            "tool_count":len(rows),
            "results":tuple(rows),
            "open_tools":tuple(row["tool_id"] for row in rows),
        }

    out=consult_registered_repertoire(
        {},
        active_controller="ICC128",
        conductor_runner=runner,
    )
    assert not out.coverage_complete
    assert out.blocker=="TOOL_CONDUCTOR_REGISTERED_ORDER_OR_IDENTITY_MISMATCH"
