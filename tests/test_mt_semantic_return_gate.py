from mt_semantic_return_gate import run_semantic_pass,run_mt_with_before_return_gate

def test_semantic_pass_stops_object_on_open_and_preserves_progress():
    calls=[]
    def exec_stage(tool,obj,state):
        calls.append(tool)
        if tool=="PD":
            return {**state,"pd":True},"CLOSED_RELATIVE",True
        return state,"OPEN",False
    r=run_semantic_pass({},["TERM:X"],execute_stage=exec_stage)
    assert calls==["PD","PDAudit"]
    assert r.state["pd"] is True
    assert r.open_objects==("TERM:X",)
    assert r.material is True

def test_mt_reruns_after_material_black_box_progress():
    mt_calls=[]
    def run_mt(state):
        mt_calls.append(dict(state))
        return dict(state),state.get("answer",0)
    def detect(state,result):
        return ("TERM:X",) if not state.get("resolved") else ()
    def exec_stage(tool,obj,state):
        if tool=="PD":
            return {**state,"resolved":True,"answer":1},"CLOSED_RELATIVE",True
        return state,"CLOSED_RELATIVE",False
    r=run_mt_with_before_return_gate(
        {"answer":0},
        run_mt=run_mt,
        detect_black_boxes=detect,
        execute_stage=exec_stage,
    )
    assert len(mt_calls)==2
    assert r.mt_result==1
    assert r.status=="CLOSED_RELATIVE"

def test_unresolved_black_box_can_return_open_without_full_solution():
    def run_mt(state):
        return state,"same"
    def detect(state,result):
        return ("TERM:HARD",)
    def exec_stage(tool,obj,state):
        return state,"OPEN",False
    r=run_mt_with_before_return_gate(
        {},
        run_mt=run_mt,
        detect_black_boxes=detect,
        execute_stage=exec_stage,
    )
    assert r.status=="OPEN"
    assert r.open_objects==("TERM:HARD",)
    assert r.rounds==1

def test_finite_round_budget_prevents_unbounded_resolution():
    n={"v":0}
    def run_mt(state):
        return state,n["v"]
    def detect(state,result):
        return ("TERM:X",)
    def exec_stage(tool,obj,state):
        n["v"]+=1
        return {**state,"v":n["v"]},"CLOSED_RELATIVE",True
    r=run_mt_with_before_return_gate(
        {},
        run_mt=run_mt,
        detect_black_boxes=detect,
        execute_stage=exec_stage,
        max_rounds=2,
        result_equivalent=lambda a,b:False,
    )
    assert r.rounds==2
    assert r.status=="OPEN"


def test_material_change_requires_mt_recheck_even_when_prior_answers_agree():
    calls=[]
    def run_mt(state):
        calls.append(state["phase"])
        return state,int(state["phase"]>=2)
    def detect(state,result):
        return ("TERM:X",) if state["phase"]<2 else ()
    def execute(tool,obj,state):
        if tool=="PD":
            return {"phase":state["phase"]+1},"CLOSED_RELATIVE",True
        return state,"CLOSED_RELATIVE",False
    out=run_mt_with_before_return_gate(
        {"phase":0},run_mt=run_mt,detect_black_boxes=detect,execute_stage=execute,
    )
    assert calls==[0,1,2]
    assert out.mt_result==1 and out.status=="CLOSED_RELATIVE"


def test_conflicting_semantic_stage_preserves_open_object():
    calls=[]
    def execute(tool,obj,state):
        calls.append(tool)
        return state,"CONFLICT",False
    out=run_semantic_pass({},["TERM:X"],execute_stage=execute)
    assert calls==["PD"]
    assert out.open_objects==("TERM:X",)
    assert out.receipts[0].status=="CONFLICT"


def test_mt_rejects_nonpositive_round_budget():
    import pytest
    with pytest.raises(ValueError,match="max_rounds"):
        run_mt_with_before_return_gate(
            {},run_mt=lambda state:(state,None),
            detect_black_boxes=lambda *args:(),
            execute_stage=lambda *args:None,max_rounds=0,
        )


def test_failed_and_unrecognized_semantic_stages_cannot_close():
    for status in ("FAILED","FAIL","UNKNOWN","UNRECOGNIZED"):
        calls=[]
        def execute(tool,obj,state):
            calls.append(tool)
            return state,status,False
        out=run_mt_with_before_return_gate(
            {},run_mt=lambda state:(state,"same"),
            detect_black_boxes=lambda *args:("TERM:X",),execute_stage=execute,
        )
        assert out.status=="OPEN"
        assert out.open_objects==("TERM:X",)
        assert out.semantic_receipts[0].status==status
        assert calls==["PD"]


def test_mt_nonboolean_material_evidence_cannot_authorize_progress_or_closure():
    for flag in (None,"false","OPEN",1,0):
        result=run_semantic_pass({"a":0},["TERM:X"],
            execute_stage=lambda *_:({"a":1},"CLOSED_RELATIVE",flag))
        assert result.state=={"a":0} and not result.material
        assert result.open_objects==("TERM:X",)
        assert result.receipts[0].status=="INVALID_MATERIAL_EVIDENCE"
