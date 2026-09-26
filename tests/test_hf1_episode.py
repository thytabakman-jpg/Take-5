from hf1_episode import (
    HF1Closure,HF1Execution,HF1Terminal,
    classify_delta,run_hf1_episode,select_sufficient_package,
)

BASE={
    "identity":"i","type":"t","scope":"s","job":"j",
    "readings":[],"result_sensitive":[],"selectors":[],
    "authority":[],"provenance":[],"open":[],
    "world_state":"w0","discovery_state":"d0","result_sensitive_state":"r0",
}

def test_exact_package_selection_requires_full_obligation_cover():
    p=select_sufficient_package(
        ("A","B"),
        {"P1":["A"],"P2":["B"],"P3":["A","B"]},
        {"P1":1,"P2":1,"P3":3},
    )
    assert p==("P1","P2")

def test_delta_coordinates_have_exact_equality_semantics():
    nxt={**BASE,"world_state":"w1"}
    d=classify_delta(BASE,nxt)
    assert d.world_changed and not d.discovery_changed and not d.result_sensitive_delta

def test_hf1_closes_immediately_when_projection_has_no_obligations():
    out=run_hf1_episode(
        BASE,
        package_index={},
        mode_flags={"exact_discriminant":True,"independent_local":True},
        execute_fn=lambda *args: (_ for _ in ()).throw(AssertionError("must not execute")),
        closure_fn=lambda *args: (_ for _ in ()).throw(AssertionError("must not close")),
    )
    assert out.terminal==HF1Terminal.RELATIVE_CLOSE

def test_hf1_composes_execution_closure_delta_and_reentry():
    start={**BASE,"obligations":["CHECK"]}
    calls=[]
    def execute(package,mode,packet):
        calls.append(("execute",package,mode))
        return HF1Execution({**packet,"obligations":[],"world_state":"w1"},"done")
    def close(execution,previous):
        calls.append(("close",execution.value))
        return HF1Closure(execution.packet,"CLOSED")

    out=run_hf1_episode(
        start,
        package_index={"P":["CHECK"]},
        mode_flags={"exact_discriminant":True,"independent_local":True},
        execute_fn=execute,
        closure_fn=close,
    )
    assert out.terminal==HF1Terminal.RELATIVE_CLOSE
    assert out.receipts[-1].reentry_action=="REENTER_OBSERVE"
    assert calls[0][0]=="execute" and calls[1][0]=="close"

def test_hf1_requires_reverification_for_result_sensitive_only_delta():
    start={**BASE,"obligations":["CHECK"]}
    def execute(package,mode,packet):
        return HF1Execution({**packet,"obligations":[],"result_sensitive_state":"r1"})
    out=run_hf1_episode(
        start,
        package_index={"P":["CHECK"]},
        mode_flags={"exact_discriminant":True,"independent_local":True},
        execute_fn=execute,
        closure_fn=lambda execution,previous:HF1Closure(execution.packet,"CLOSED"),
        verify_fn=lambda packet:True,
    )
    assert out.terminal==HF1Terminal.RELATIVE_CLOSE
    assert out.receipts[-1].reentry_action=="REVERIFY"

def test_hf1_fails_open_when_live_obligations_have_no_material_delta():
    start={**BASE,"obligations":["CHECK"]}
    out=run_hf1_episode(
        start,
        package_index={"P":["CHECK"]},
        mode_flags={"exact_discriminant":True,"independent_local":True},
        execute_fn=lambda package,mode,packet:HF1Execution(dict(packet)),
        closure_fn=lambda execution,previous:HF1Closure(execution.packet,"CLOSED"),
    )
    assert out.terminal==HF1Terminal.OPEN
    assert out.blocker=="NO_PROGRESS_WITH_LIVE_OBLIGATIONS"
