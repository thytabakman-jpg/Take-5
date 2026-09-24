"""Mode-cube selector: breadth x direction x coupling."""
def select_mode(*,premature_pruning=False,exact_discriminant=False,bounded_intervention=False,broad_redesign=False,
                independent_local=False,coupled=False):
    base=[premature_pruning,exact_discriminant,bounded_intervention,broad_redesign]
    if sum(bool(x) for x in base)!=1 or (independent_local and coupled):
        return "OPEN"
    if premature_pruning: bd="EXPAND_OBSERVE"
    elif exact_discriminant: bd="CONTRACT_OBSERVE"
    elif bounded_intervention: bd="CONTRACT_ACT"
    else: bd="EXPAND_ACT"
    cp="DECOUPLED" if independent_local else "COUPLED"
    return bd+"_"+cp
