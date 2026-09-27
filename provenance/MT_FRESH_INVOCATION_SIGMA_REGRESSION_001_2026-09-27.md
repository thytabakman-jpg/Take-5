# MT Fresh Invocation Sigma Regression 001

Date: 2026-09-27
Status: EXECUTED / CI VERIFIED / BASIS-RELATIVE PASS
Equation under test:

```math
Σ = 𝟙_{Δ ∩ Ω ∩ Φ ∩ Ξ}
```

Target failure class:
A direct user command such as `run MT` silently degrades to a stripped/bare MT instead of the current full configured MT.

## Test object

Current Take-5 registered MT identity reached through:

`runtime/direct_tool_command_gateway.py`

Dedicated regression test:

`tests/test_mt_fresh_invocation_sigma_regression_20260927.py`

Test commit:

`2bdc98a94964d6864a4423f59002fa3f63fd2290`

## Fresh-environment condition

The validation ran on a fresh GitHub Actions Ubuntu runner after repository checkout.

The regression test supplied only:

- direct command `run MT`
- minimal state `{"round": 0}`
- a local semantic adapter used only to witness configured execution

It supplied no conversation history, prior chat, saved memory, or reconstructed conversation corpus.

Therefore this test checks repository-owned direct invocation without chat-history rescue.

## Four-gate result

### Δ — definition/reconstruction closed

PASS.

Evidence:

- `CONFIGURED_RUNS["MT"].complete()` returned true.
- the MT manifest reconstructs its declared MT-specific protected behavior plus:
  - PROTECTED_TRANSITION_INTEGRITY
  - CONFIGURED_HF2_RECURRENCE
  - FULL_CONFIGURED_INVOCATION_PROFILE

Result:

`Δ = 1`

### Ω — obligations closed

PASS.

The direct `run MT` binding produced the current full configured plan with:

- wrapper required
- OBSERVER mode
- D36_C geometry
- 36 cells
- 22 x 36 = 792 question projections
- 4 x 36 = 144 cognitive projections
- HF002 recurrence required
- FULL_CONFIGURED_HF2_V1 invocation profile
- SHARED_GATE configured HF2 execution

Result:

`Ω = 1`

### Φ — realizer available

PASS.

The actual direct-tool command gateway executed MT through the configured bridge.

Observed terminal state:

- batch status EXECUTED
- direct-tool status EXECUTED_FULL_CONFIGURED
- exactly one MT execution receipt

Result:

`Φ = 1`

### Ξ — protected behavior preserved

PASS.

Evidence:

- MT_BLACK_BOX_SEMANTIC_RETURN_GATE remains part of the registered MT protected behaviors.
- the current MT manifest reconstructs that protected behavior.
- execution used recurrence engine HF002.
- recurrence closed as RELATIVE_CLOSE.
- two MT rounds executed under material local change:
  - round 1: MT / 36 cells / wrapper true
  - round 2: MT / 36 cells / wrapper true

Result:

`Ξ = 1`

## Integrated result

```math
Σ
=
𝟙_{1 ∩ 1 ∩ 1 ∩ 1}
=
1
```

Disposition:

PASS for the repository-owned direct invocation path.

## Negative control

The same direct command was executed with no MT semantic adapter.

Expected fail-closed behavior occurred:

- status OPEN
- blocker CONFIGURED_TOOL_ADAPTER_REQUIRED:MT

The system did not silently substitute a weaker implementation.

This is evidence that the positive result is not produced merely because the string `run MT` is recognized.

## GitHub Actions receipt

Workflow:

Take-5 Validation

Run ID:

`36295822154`

Conclusion:

SUCCESS

Validated steps included:

- Take-5 test suite
- canonical whole-system audit
- closed-loop fixture
- zero-request dump

All completed successfully.

## What this establishes

Within the current Take-5 repository-owned route:

`run MT`

resolves to the current full configured MT package rather than a bare/core substitute, and that result satisfies the four-gate Sigma classifier under this test basis.

## What this does not establish

It does not establish universal interception of every external ChatGPT host or every future environment.

An unrelated host that never enters the Take-5 direct-tool gateway remains outside repository authority.

Therefore the correct status is:

REPOSITORY DIRECT-INVOCATION REGRESSION: CLOSED_RELATIVE / PASS

UNIVERSAL HOST INTERCEPTION: OPEN / EXTERNAL_NOT_OWNED
