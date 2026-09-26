from improvement_core import improve

BASE={"identity":"x","type":"system","scope":"local","job":"improve","readings":[],"result_sensitive":[],"selectors":[],"authority":["observe"],"local_authority":["observe"],"provenance":[],"open":[]}

def focus(_): return {"exact_discriminant":True,"independent_local":True}

def test_improvement_core_delegates_and_reenters_until_obligation_closes():
    p=dict(BASE); p["obligations"]=["CHECK_IDENTITY"]
    def c02(x):
        y=dict(x); y["obligations"]=[]; y["identity_checked"]=True; return y
    r=improve(p,{"C02":["CHECK_IDENTITY"]},{"C02":c02},focus)
    assert r.status=="CLOSED_RELATIVE"
    assert r.final_packet["identity_checked"] is True
    assert r.results[0][0]=="C02"

def test_improvement_core_preserves_open_without_reachable_capability():
    p=dict(BASE); p["obligations"]=["UNKNOWN"]
    assert improve(p,{}, {},focus).status=="OPEN"

def test_improvement_core_does_not_loop_same_unresolved_state():
    p=dict(BASE); p["obligations"]=["CHECK_IDENTITY"]
    r=improve(p,{"C02":["CHECK_IDENTITY"]},{"C02":lambda x:dict(x)},focus)
    assert r.status=="CLOSED_RELATIVE" or r.status=="OPEN"
    assert r.rounds<=1

def test_inquiry_is_prepared_before_package_selection():
    p=dict(BASE); p["obligations"]=["CHECK_IDENTITY"]
    seen=[]
    def selector(obligations,package_index,packet):
        seen.append((
            packet.get("inquiry_prepared"),
            packet.get("question_frontier"),
            packet.get("question_tool_map"),
        ))
        return ("C02",)
    def c02(x):
        y=dict(x); y["obligations"]=[]; return y
    r=improve(
        p,
        {"C02":["CHECK_IDENTITY"]},
        {"C02":c02},
        focus,
        package_selector=selector,
    )
    assert r.status=="CLOSED_RELATIVE"
    assert seen
    prepared,frontier,qmap=seen[0]
    assert prepared is True
    assert frontier[0]["obligations"]==("CHECK_IDENTITY",)
    assert qmap==( ("obligation:1",("C02",)), )

def test_explicit_unmapped_question_blocks_package_selection():
    p=dict(BASE)
    p["obligations"]=["CHECK_IDENTITY"]
    p["question_frontier"]=[
        {"question_id":"q-live","issue":"What hidden distinction matters?","obligations":["DISCOVER_HIDDEN"]}
    ]
    called=[]
    def selector(*args):
        called.append(True)
        return ("C02",)
    r=improve(
        p,
        {"C02":["CHECK_IDENTITY"]},
        {"C02":lambda x:x},
        focus,
        package_selector=selector,
    )
    assert r.status=="OPEN"
    assert r.final_packet["unmapped_questions"]==("q-live",)
    assert called==[]

def test_explicit_question_maps_to_tool_before_selection():
    p=dict(BASE)
    p["obligations"]=["DISCOVER_HIDDEN"]
    p["question_frontier"]=[
        {"question_id":"q-hidden","issue":"What hidden dependency exists?","obligations":["DISCOVER_HIDDEN"]}
    ]
    def c07(x):
        y=dict(x); y["obligations"]=[]; y["answered_question"]="q-hidden"; return y
    r=improve(
        p,
        {"C07":["DISCOVER_HIDDEN"]},
        {"C07":c07},
        focus,
    )
    assert r.status=="CLOSED_RELATIVE"
    assert r.final_packet["answered_question"]=="q-hidden"
    assert r.final_packet["question_tool_map"]==( ("q-hidden",("C07",)), )
