# Math-First Wrapper Closure 039

Date: 2026-09-25
Status: IMPLEMENTED_VALIDATED
Scope: IC + Jane + wrapper completion
Production authority: unchanged
Legacy wrapper: preserved for rollback/comparison

## Decision

The observer-mode all-tools sweep is closed relative to the frozen job.

- Improvement Core was not rebuilt.
- Jane was not rebuilt.
- The wrapper was rebuilt from the mathematics up.
- IC received only backward-compatible optional extension points.
- Jane received no primary action-selection responsibility.
- Tool Run Closure and HF delta reentry routing now have separate identities.
- Exact least-cost sufficient-cover selection is available as an opt-in IC selector.
- Frozen mathematical objects are protected against silent mutation.
- External user job/target and derived operational goal are distinct.
- Jane synchronization occurs only for admitted material continuity-relevant deltas.
- OPEN and BLOCKED remain typed non-closure states.
- The old wrapper remains available.

## Final equation

Let beta be Jane's bound entry contract.

    beta = B_J(u)

For each recursive round:

    o_n    = O_beta(z_n)
    m_n    = Phi(o_n, beta)
    mbar_n = Freeze(m_n)
    g_n    = G(mbar_n, beta)
    a_n    = A(mbar_n, g_n, z_n, beta)
    y_n    = IC(a_n, z_n; T)
    (c_n, chi_n) = C_TR(z_n, y_n)
    z_(n+1) = U(z_n, c_n, chi_n)

Jane synchronization:

    j_(n+1) =
        U_J(j_n, Delta z_n)  when S_J(Delta z_n; mbar_n, beta)=1
        j_n                  otherwise

Wrapper composition:

    W_beta
      = Sync_J
        o U
        o C_TR
        o IC
        o A
        o G
        o Freeze
        o Phi
        o O_beta

Guarded recursion:

    (z_(n+1), j_(n+1)) = W_beta(z_n, j_n)

Relative closure requires:

    chi_n = CLOSED
    R_Q(z_(n+1)) ==_Q R_Q(z_n)
    no live reentry trigger

OPEN and BLOCKED terminate the current episode as non-closure states.

## IC selection mathematics

Historical max-hit selection remains the default for compatibility.

The new selector implements:

    P*(m)
      in argmin over P
      sum_{T_i in P} c_i(m)

subject to:

    union_{T_i in P} C_i(m) contains O_exec(m)

and applicability/licensing constraints.

The implementation uses exact dynamic programming over reachable obligation subsets.

## Protected role equations

IC remains:

    K_PD
      -> obligations
      -> mode
      -> package selection
      -> execution
      -> delta reentry routing
      -> K_PD / reverification

Jane remains:

    entry binding
      + continuity supervision
      + capability visibility
      + question frontier
      + delegation packaging
      + admitted-delta synchronization

Jane is not the primary action selector while IC owns the controller lease.

## Validation evidence

Merged implementation PR:
- PR #4 — Math-first wrapper around protected IC and Jane

Squash merge:
- a567245bc62e3746f4fe5eaeec769a7d65245b72

Main validation run:
- GitHub Actions run 36154766223
- conclusion: SUCCESS

The passing gate included:
- full pytest suite;
- canonical whole-system audit;
- closed-loop fixture;
- zero-request dump.

New evidence includes:
- exact weighted selector test;
- historical-selector compatibility test;
- selector-through-IC integration test;
- wrapper stage-order test;
- external job/target protection;
- frozen-math mutation rejection;
- OPEN preservation;
- Jane supervisory sync test;
- unfamiliar recursive holdout.

## Tool placement after closure

IC-selectable mathematical lenses:
- D4
- D6
- D8
- Kolb
- DIKW
- Predictive Processing
- Bayesian Update
- Active Inference
- Actor-Critic
- Rate-Distortion
- OODA
- Functional Stack
- C01-C49 and existing PD/MT/root-cause/audit/architecture capabilities

These tools are admitted for selection only when their typed applicability and runtime inputs exist. Domain-specific tools that require likelihoods, utilities, distortion functions, environment dynamics, or grounding sources remain unbound until those inputs are supplied. Their mathematics does not need to be reinvented later.

Jane-owned capabilities:
- entry contract/controller lease;
- currentness/provenance supervision;
- question frontier;
- capability visibility;
- delegation packaging;
- receipts/map anti-loss;
- continuity-relevant admitted-delta synchronization.

Wrapper-owned capabilities:
- nonmutating observation;
- formalization;
- FreezeMath;
- operational-goal derivation;
- architecture compilation;
- Tool Run Closure boundary;
- admitted update;
- Jane sync;
- relative fixed-point termination.

## Remaining OPEN work

No blocking item remains for the frozen IC/Jane/wrapper job.

Nonblocking future work:
- bind additional domain-specific learning lenses when a live problem supplies their required typed inputs;
- empirically calibrate tool costs used by the least-cost selector;
- compare efficiency across larger real workloads;
- retire the legacy wrapper only after a separate explicit cleanup decision.

These are expansion/calibration tasks, not missing wrapper mathematics.


## 2026-09-25 Take Two discovery-reentry addendum

The earlier statement that no blocking item remained for wrapper mathematics was too strong relative
to the protected original Take Two behavior.

A closure gap was later demonstrated:

unchanged admitted world state
+ unchanged protected result
+ material representation/view/candidate-universe discovery
could be treated as relative closure by the wrapper's default state-delta reentry rule.

This is reopened and repaired by:
architecture/TAKE_TWO_DISCOVERY_REENTRY_INTEGRATION_001.md

The corrected closure condition requires discovery stability in addition to protected-result and
admitted-state stability.  Take-2 remains untouched as the historical behavioral baseline.
