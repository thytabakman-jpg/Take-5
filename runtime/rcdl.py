"""Factored RCDL helper: regenerate views/candidate universe and expose material reentry."""
from dataclasses import dataclass
from representation_discovery import generate_views,candidate_universe,compare_discovery

@dataclass(frozen=True)
class RCDLResult:
    views:tuple
    universe:object
    delta:object

def regenerate(state,view_generators,candidate_generators,prior_views=(),prior_universe=None,relation_changed=False,state_changed=False):
    views=generate_views(state,view_generators)
    universe=candidate_universe(state,views,candidate_generators)
    if prior_universe is None:
        prior_universe=candidate_universe(state,tuple(prior_views),candidate_generators)
    delta=compare_discovery(tuple(prior_views),views,prior_universe,universe,
                            relation_changed=relation_changed,state_changed=state_changed)
    return RCDLResult(views,universe,delta)
