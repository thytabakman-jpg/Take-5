from mode_selector import select_mode

def test_mode_geometry_routes_distinct_information_loss_risks():
    assert select_mode(premature_pruning=True)=="EXPAND_OBSERVE"
    assert select_mode(exact_discriminant=True)=="CONTRACT_OBSERVE"
    assert select_mode(bounded_intervention=True)=="CONTRACT_ACT"
    assert select_mode(broad_redesign=True)=="EXPAND_ACT"

def test_mode_selector_preserves_ambiguity():
    assert select_mode()=="OPEN"
    assert select_mode(premature_pruning=True,exact_discriminant=True)=="OPEN"
