from improvement_core_route_calibration import (
    broad_observe_records,select_route,
)

def test_flat_corpus_uses_cheap_route_when_broad_adds_no_material_class():
    corpus=[
        {"id":"a","name":"A","version":1,"refs":[]},
        {"id":"b","name":"B","version":1,"refs":[]},
    ]
    out=select_route(corpus)
    assert out.route=="CHEAP"
    assert out.broad_findings==out.cheap_findings

def test_relational_cycle_forces_broad_attack_and_recovers_hidden_structure():
    corpus=[
        {"id":"a","refs":["b"]},
        {"id":"b","refs":["a"]},
    ]
    cheap=select_route(corpus)
    broad=broad_observe_records(corpus)
    assert cheap.route=="BROAD"
    assert any(x["type"]=="REFERENCE_CYCLE" for x in broad["findings"])
    assert cheap.broad_findings>cheap.cheap_findings

def test_resolved_acyclic_relation_still_routes_broad_on_current_policy():
    corpus=[
        {"id":"a","refs":["b"]},
        {"id":"b","refs":[]},
    ]
    out=select_route(corpus)
    assert out.route=="BROAD"
