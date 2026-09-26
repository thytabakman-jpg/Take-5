from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import GOAL_DIRECTED_STAGES

def handlers():
    out={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
                "supervisory_relevant":False,
            }
        out[stage]=fn
    out["REENTER"]=lambda state:{"state":state,"terminal":True}
    return out

HOLDOUTS=(
    (
        "dependency_graph",
        [
            {"id":"g1","refs":["g2"]},
            {"id":"g2","refs":[]},
        ],
    ),
    (
        "version_plurality",
        [
            {"id":"v1","name":"Model","version":1,"refs":[]},
            {"id":"v2","name":"Model","version":2,"refs":[]},
        ],
    ),
    (
        "unstructured_text",
        [
            "alpha narrative",
            "beta narrative",
            "gamma narrative",
        ],
    ),
)

def run(name,corpus):
    resolution,out=dispatch_improvement_core(
        "Run ImproveCore",
        corpus=corpus,
        state={"holdout":name},
        handlers=handlers(),
    )
    return resolution,out

def test_unlike_zero_request_corpora_all_enter_governed_improvecore():
    for name,corpus in HOLDOUTS:
        resolution,out=run(name,corpus)
        assert resolution.controller=="IC-028"
        assert out.status=="COMPLETE"
        assert out.result.state["upstream_discovery"]["status"]=="OBSERVED"
        assert out.result.state["upstream_discovery"]["corpus_size"]==len(corpus)
        assert out.receipt.entry_receipt
        assert "GENERATE_WORK" in out.receipt.stages
        assert "VERIFY" in out.receipt.stages

def test_relational_holdout_uses_broad_route_and_admits_reference_relation():
    _,out=run(*HOLDOUTS[0])
    d=out.result.state["upstream_discovery"]
    assert d["route"]=="BROAD"
    rel=d["relation_state"]
    assert rel["generator_ids"]
    assert rel["licensed"]
    assert rel["licensed"][0]["relation_id"]=="REFERENCES"
    assert rel["licensed"][0]["arguments"]==("g1","g2")

def test_flat_version_holdout_uses_cheap_route():
    _,out=run(*HOLDOUTS[1])
    assert out.result.state["upstream_discovery"]["route"]=="CHEAP"
