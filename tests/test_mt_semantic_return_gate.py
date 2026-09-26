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
