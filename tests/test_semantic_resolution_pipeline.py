from semantic_resolution_pipeline import (
    plan_black_box_resolution,configured_work_obligations,unexplained_residuals,runtime_gaps
)

def test_mandatory_black_box_spine():
    p=plan_black_box_resolution("TERM:X")
    assert tuple(s.tool_id for s in p.stages)==("PD","PDAudit","MTA","MT","PDAudit","C47")
    assert configured_work_obligations(p)==(
        "RUN_CONFIGURED:PD:TERM:X",
        "RUN_CONFIGURED:PDAudit:TERM:X",
        "RUN_CONFIGURED:MTA:TERM:X",
        "RUN_CONFIGURED:MT:TERM:X",
        "RUN_CONFIGURED:PDAudit:TERM:X",
        "RUN_CONFIGURED:C47:TERM:X",
    )

def test_conditional_tools_are_residual_driven():
    p=plan_black_box_resolution("TERM:X",("TYPE_OPEN","CAUSE_OPEN","DISCOVERY_OPEN"))
    assert tuple(s.tool_id for s in p.stages[-3:])==("C01","Diagnosis","C19")

def test_unknown_residual_stays_visible():
    p=plan_black_box_resolution("TERM:X",("SOMETHING_NEW",))
    assert unexplained_residuals(p)==("SOMETHING_NEW",)


def test_reality_residual_is_explicit_runtime_gap():
    p=plan_black_box_resolution("TERM:X",("REALITY_OPEN",))
    assert runtime_gaps(p)
    assert "Reality Check" in runtime_gaps(p)[0][1]
