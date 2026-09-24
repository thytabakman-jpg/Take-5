"""Bias-aware mode selector from the four-quadrant control geometry."""
def select_mode(*,premature_pruning=False,exact_discriminant=False,bounded_intervention=False,broad_redesign=False):
    flags=[premature_pruning,exact_discriminant,bounded_intervention,broad_redesign]
    if sum(bool(x) for x in flags)!=1:
        return "OPEN"
    if premature_pruning: return "EXPAND_OBSERVE"
    if exact_discriminant: return "CONTRACT_OBSERVE"
    if bounded_intervention: return "CONTRACT_ACT"
    return "EXPAND_ACT"
