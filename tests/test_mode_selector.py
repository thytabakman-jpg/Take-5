from mode_selector import select_mode

def test_mode_cube_routes_distinct_information_loss_risks():
    assert select_mode(premature_pruning=True,independent_local=True)=="EXPAND_OBSERVE_DECOUPLED"
    assert select_mode(exact_discriminant=True,independent_local=True)=="CONTRACT_OBSERVE_DECOUPLED"
    assert select_mode(bounded_intervention=True,independent_local=True)=="CONTRACT_ACT_DECOUPLED"
    assert select_mode(broad_redesign=True,coupled=True)=="EXPAND_ACT_COUPLED"

def test_mode_selector_preserves_ambiguity():
    assert select_mode()=="OPEN"
    assert select_mode(premature_pruning=True,exact_discriminant=True)=="OPEN"
    assert select_mode(exact_discriminant=True,independent_local=True,coupled=True)=="OPEN"
