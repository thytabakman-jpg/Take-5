"""OPEN Architect candidate: exhaustive finite model intervention search.

This computes predictions, not empirical observations or transformation authority.
No existing Architect dispatch, closure, or protected-behaviour gate is replaced.
"""
from itertools import product
from math import prod


def search_model(domains, writable, baselines, obligations, protected, admissible,
                 *, authority, max_trials=4096):
    """Search shared coordinate assignments across all declared contexts.

    Domains: component -> nonempty tuple of strings; writable: permitted components.
    Baselines: context -> full state mapping. Rules: name -> DNF (tuple of clauses),
    each clause a mapping of component -> required value. Admission: DNF.
    Empty DNF is false; one empty clause is true. Contexts have distinct baselines
    but share rules; context-specific rules are not claimed. The identity assignment
    is excluded. Every candidate is evaluated, not inferred from observed edits.
    """
    if not isinstance(authority, str) or not authority.strip():
        raise ValueError('MODEL_AUTHORITY_REQUIRED')
    if type(max_trials) is not int or not 1 <= max_trials <= 4096:
        raise ValueError('MODEL_TRIAL_LIMIT_INVALID')
    if not domains or not baselines or not obligations or not protected:
        raise ValueError('MODEL_CONTRACT_INCOMPLETE')
    def valid_name(x):
        return isinstance(x, str) and bool(x.strip())
    for key, values in domains.items():
        if not valid_name(key) or not isinstance(values, (tuple, list)) or not values or any(
                not valid_name(v) for v in values) or len(set(values)) != len(values):
            raise ValueError('MODEL_DOMAIN_INVALID')
    writable = tuple(writable)
    if not writable or len(set(writable)) != len(writable) or not set(writable) <= domains.keys():
        raise ValueError('MODEL_WRITABLE_INVALID')
    def check_clause(clause):
        if not isinstance(clause, dict) or any(k not in domains or v not in domains[k] for k, v in clause.items()):
            raise ValueError('MODEL_RULE_INVALID')
    def check_dnf(rule):
        if not isinstance(rule, (tuple, list)):
            raise ValueError('MODEL_RULE_INVALID')
        for clause in rule:
            check_clause(clause)
    for context, state in baselines.items():
        if not valid_name(context) or not isinstance(state, dict) or state.keys() != domains.keys():
            raise ValueError('MODEL_BASELINE_INVALID')
        check_clause(state)
    for rules in (obligations, protected):
        for name, rule in rules.items():
            if not valid_name(name):
                raise ValueError('MODEL_RULE_NAME_INVALID')
            check_dnf(rule)
    check_dnf(admissible)
    def holds(rule, state):
        return any(all(state[k] == v for k, v in clause.items()) for clause in rule)
    def outcome(state):
        return (frozenset(q for q, rule in obligations.items() if holds(rule, state)),
                tuple((p, holds(rule, state)) for p, rule in sorted(protected.items())))
    if any(not holds(admissible, s) for s in baselines.values()):
        raise ValueError('MODEL_BASELINE_INADMISSIBLE')
    keys = tuple(sorted(writable))
    choices = tuple((None, *sorted(domains[k])) for k in keys)
    trials = prod(map(len, choices)) - 1
    opens = ('MODEL_EMPIRICAL_VALIDITY_UNCERTIFIED', 'CONTINUATION_EQUIVALENCE_UNCERTIFIED',
             'FULL_DIRECTED_SCOPE_COVERAGE_UNCERTIFIED', 'REAL_TRANSFORMATION_ADMISSION_UNCERTIFIED')
    if trials > max_trials:
        return {'status': 'OPEN', 'reason': 'MODEL_SEARCH_BUDGET_EXCEEDED',
                'required_trials': trials, 'evaluated': 0, 'frontier': (), 'OPEN': opens}
    base = {c: outcome(s) for c, s in baselines.items()}
    accepted = []
    rejected = {'inadmissible': 0, 'regression': 0, 'no_gain': 0}
    for values in product(*choices):
        edit = tuple((k, v) for k, v in zip(keys, values) if v is not None)
        if not edit:
            continue
        successor = {c: dict(s, **dict(edit)) for c, s in baselines.items()}
        if any(not holds(admissible, s) for s in successor.values()):
            rejected['inadmissible'] += 1
            continue
        observed = {c: outcome(s) for c, s in successor.items()}
        if any(p != base[c][1] or not base[c][0] <= q for c, (q, p) in observed.items()):
            rejected['regression'] += 1
            continue
        gain = frozenset((c, q) for c, (qs, _) in observed.items() for q in qs - base[c][0])
        if not gain:
            rejected['no_gain'] += 1
            continue
        accepted.append((edit, gain))
    gains = set(g for _, g in accepted)
    nondominated = {g for g in gains if not any(g < other for other in gains)}
    return {'status': 'OPEN', 'authority': authority, 'evidence': 'DECLARED_MODEL_PREDICTION',
            'required_trials': trials, 'evaluated': trials, 'rejected': rejected,
            'accepted': len(accepted), 'frontier': tuple((e, tuple(sorted(g))) for e, g in accepted if g in nondominated),
            'OPEN': opens}
