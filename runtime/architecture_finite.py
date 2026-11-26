"""Bounded intervention evaluator for Architecture, not the full Architect identity.

A provider supplies an explicit finite family of observations on typed component
coordinates. Comparisons use only those observations; graph edges alone never
establish dependency. Missing coverage is always OPEN beyond the supplied basis.
"""
from dataclasses import dataclass
from itertools import combinations

from architecture_analysis import run_architecture_analysis


@dataclass(frozen=True)
class Observation:
    identity: str
    context: str
    state: tuple[str, ...]
    obligations: frozenset[str]  # satisfied obligations
    protected: tuple[str, ...]  # ordered protected observation projection
    evidence: str


@dataclass(frozen=True)
class FiniteContract:
    components: tuple[str, ...]
    obligations: frozenset[str]
    baseline_ids: tuple[str, ...]  # one baseline per context
    authority: str
    candidates: tuple[tuple[str, tuple[str, ...]], ...] = ()  # candidate id, observation ids


def _admit_observations(rows, c):
    if (not isinstance(c, FiniteContract) or not c.authority or not c.components
            or len(set(c.components)) != len(c.components) or not c.obligations
            or not c.baseline_ids or not rows):
        raise ValueError('FINITE_ARCHITECTURE_CONTRACT_REQUIRED')
    by_id = {}
    by_state = {}
    protected_widths = {}
    for row in rows:
        if (not isinstance(row, Observation) or not row.identity or not row.context
                or not row.evidence or len(row.state) != len(c.components)
                or not row.obligations <= c.obligations or row.identity in by_id):
            raise ValueError('FINITE_ARCHITECTURE_OBSERVATION_INVALID')
        if protected_widths.setdefault(row.context, len(row.protected)) != len(row.protected):
            raise ValueError('FINITE_ARCHITECTURE_PROJECTION_MISMATCH')
        key = (row.context, row.state)
        outcome = (row.obligations, row.protected)
        if key in by_state and by_state[key] != outcome:
            raise ValueError('FINITE_ARCHITECTURE_OBSERVATION_CONFLICT')
        by_state[key] = outcome
        by_id[row.identity] = row
    baselines = {by_id[i].context: by_id[i] for i in c.baseline_ids}
    if len(baselines) != len(c.baseline_ids) or set(baselines) != {r.context for r in rows}:
        raise ValueError('FINITE_ARCHITECTURE_BASELINE_CONTEXT_MISMATCH')
    return by_id, by_state, baselines


def _localize_and_recover_dependencies(rows, c):
    supports = {q: {} for q in c.obligations}
    dependencies = []
    for a, b in combinations(rows, 2):
        if a.context != b.context:
            continue
        changed = frozenset(n for n, x, y in zip(c.components, a.state, b.state) if x != y)
        if not changed:
            continue
        for q in a.obligations ^ b.obligations:
            supports[q].setdefault(changed, []).append((a.identity, b.identity))
        if len(changed) == 1:
            for q in sorted(a.obligations ^ b.obligations):
                dependencies.append((next(iter(changed)), q, a.identity, b.identity))
            for i, (x, y) in enumerate(zip(a.protected, b.protected)):
                if x != y:
                    dependencies.append((next(iter(changed)), f'protected:{i}', a.identity, b.identity))
    localization = {q: tuple((tuple(sorted(s)), tuple(witnesses)) for s, witnesses in sorted(
        families.items(), key=lambda item: (len(item[0]), sorted(item[0])))
        if not any(t < s for t in families)) for q, families in sorted(supports.items())}
    return localization, dependencies


def _evaluate_interactions(rows, by_state, baselines):
    # Joint effects under a declared set-union algebra of newly satisfied obligations.
    # A joint observation is tested only if every proper nonempty sub-intervention
    # has an observation at the same baseline/context with exactly matching values.
    interactions = []
    context_sizes = {k: sum(ctx == k for ctx, _ in by_state) for k in baselines}
    for row in rows:
        base = baselines[row.context]
        indices = tuple(i for i, (x, y) in enumerate(zip(base.state, row.state)) if x != y)
        if len(indices) < 2 or (1 << len(indices)) > context_sizes[row.context]:
            continue
        lower = set()
        covered = True
        for k in range(1, len(indices)):
            for subset in combinations(indices, k):
                state = tuple(row.state[i] if i in subset else base.state[i] for i in range(len(base.state)))
                value = by_state.get((row.context, state))
                if value is None:
                    covered = False
                    break
                lower.update(value[0] - base.obligations)
            if not covered:
                break
        if covered and row.obligations - base.obligations != lower:
            interactions.append((base.identity, row.identity, tuple(sorted(row.obligations-base.obligations)), tuple(sorted(lower))))
    return interactions


def _evaluate_successors(c, by_id, baselines):
    admitted = {}
    rejected = {}
    seen = set()
    for candidate, identities in c.candidates:
        if not candidate or candidate in seen:
            raise ValueError('FINITE_ARCHITECTURE_CANDIDATE_ID_INVALID')
        seen.add(candidate)
        selected = {by_id[i].context: by_id[i] for i in identities}
        if len(selected) != len(identities) or set(selected) != set(baselines):
            rejected[candidate] = 'OPEN_CONTEXT_COVERAGE'
            continue
        if any(r.protected != baselines[k].protected or not baselines[k].obligations <= r.obligations
               for k, r in selected.items()):
            rejected[candidate] = 'PROTECTED_REGRESSION'
            continue
        gain = frozenset((k,q) for k,r in selected.items() for q in r.obligations-baselines[k].obligations)
        if not gain:
            rejected[candidate] = 'NO_STRICT_GAIN_ON_BASIS'
            continue
        admitted[candidate] = gain
    frontier = tuple(sorted(k for k,v in admitted.items() if not any(v < w for w in admitted.values())))
    return admitted, rejected, frontier


def analyze_finite_architecture(observations, contract):
    """Compute witnessed support, dependency and a same-job finite frontier.

    No candidate generation, unobserved intervention or causal inference is
    asserted. The authority is a basis reference, not a mutation grant.
    """
    rows = tuple(observations)
    c = contract
    by_id, by_state, baselines = _admit_observations(rows, c)
    localization, dependencies = _localize_and_recover_dependencies(rows, c)
    interactions = _evaluate_interactions(rows, by_state, baselines)
    admitted, rejected, frontier = _evaluate_successors(c, by_id, baselines)
    return {
        'ArchClass': 'FINITE_OBSERVED_INTERVENTION_FRAME',
        'Violations': {k: tuple(sorted(c.obligations-r.obligations)) for k,r in baselines.items()},
        'LocalizationFamilies': localization,
        'DependencyState': tuple(dependencies),
        'InteractionState': tuple(interactions),
        'TransformationFrontier': {'observed_preserving_gain_candidates': tuple(sorted(admitted)), 'rejected': rejected},
        'SuccessorFrontier': frontier,
        'Coverage': {'observations': len(rows), 'contexts': tuple(sorted(baselines)),
                     'interaction_algebra': 'UNION_OF_NEWLY_SATISFIED_OBLIGATIONS'},
        'OpenConflictBlocked': {'OPEN': ('UNOBSERVED_INTERVENTIONS_AND_TRANSFORMATIONS',
                                        'FULL_DIRECTED_SCOPE_COVERAGE_UNCERTIFIED',
                                        'CONTINUATION_EQUIVALENCE_UNCERTIFIED',
                                        'TRANSFORMATION_ADMISSION_UNCERTIFIED')},
        'Provenance': {'authority': c.authority, 'observations': {r.identity:r.evidence for r in rows}},
    }


def run_finite_architecture(observations, contract):
    return run_architecture_analysis(observations, contract, analyze_architecture=analyze_finite_architecture)
