"""Experimental four-quadrant projection.

This is a research projection, not a settled controller ontology.
It must not be treated as authoritative mode geometry until competing
operational-mode models survive recursive/external challenge and holdouts.
"""
MODEL_STATUS="EXPERIMENTAL_PROJECTION"

def model_status():
    return MODEL_STATUS

def select_mode(*,premature_pruning=False,exact_discriminant=False,bounded_intervention=False,broad_redesign=False):
    flags=[premature_pruning,exact_discriminant,bounded_intervention,broad_redesign]
    if sum(bool(x) for x in flags)!=1:
        return "OPEN"
    if premature_pruning: return "EXPAND_OBSERVE"
    if exact_discriminant: return "CONTRACT_OBSERVE"
    if bounded_intervention: return "CONTRACT_ACT"
    return "EXPAND_ACT"
