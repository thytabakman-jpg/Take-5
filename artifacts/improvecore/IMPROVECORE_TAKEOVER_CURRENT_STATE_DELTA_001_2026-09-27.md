# ImproveCore Takeover Current-State Delta 001

Date: 2026-09-27
Repository: thytabakman-jpg/Take-5
Basis commit: a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2
Status: CURRENTNESS DELTA / BASIS-RELATIVE CLOSURE / GLOBAL CLOSURE NOT CLAIMED

## Trigger

User instruction: "Improve core. Take over."

The immediately preceding ASSERT state was used as evidence. ImproveCore then re-read the live runtime rather than preserving the prior audit's red frontier by inertia.

## Material state changes

### 1. Exact D36_C axes are recovered

Current runtime authority:

- Scope axis
  - SYSTEM
  - SUBSYSTEM
  - COMPONENT
  - INTERFACE
  - BOUNDARY_DECOMPOSITION
  - CROSS_LAYER

- Mode-face axis
  - EXPAND
  - CONTRACT
  - INWARD
  - OUTWARD
  - ISOLATE
  - COUPLE

Therefore:

D36_C = Scope x ModeFace

with 6 x 6 = 36 cells.

### 2. D36_H is a current typed geometry

runtime/run_request.py currently defines:

- D36_C = Scope x ModeFace
- D36_H = SourceScope x TargetScope
- D216 = SourceScope x TargetScope x ModeFace
- D288 = SourceScope x TargetScope x FullMode

The earlier audit status that treated D36_H as unrecovered is superseded.

### 3. Ordinary direct tool invocation is fail-closed against downgrade

runtime/run_request.py defines ordinary "run TOOL" as the current configured recursive run with wrapper, typed geometry, closure, and reentry. Bare/core execution requires explicit user wording.

runtime/global_tool_execution.py enforces the global configured-run profile:

- OBSERVER mode
- wrapper required
- D36_C geometry
- recurrence required
- HF002 recurrence for ordinary registered tools
- FULL_CONFIGURED_HF2_V1 invocation profile
- 36 coverage cells
- Q01-Q22 over all 36 cells
- DIFFERENTIATE / RELATE / RECONSTRUCT / STRENGTHEN over all 36 cells
- declared native layer(s) over all 36 cells

tests/test_run_request.py, tests/test_global_tool_execution.py, and tests/test_direct_tool_command_gateway.py regression-test this behavior.

### 4. Direct-tool execution uses the same configured HF2 bridge

tests/test_direct_tool_command_gateway.py verifies that "run MT":

- resolves to MT
- binds a complete configured plan
- has wrapper_required = True
- has geometry = D36_C
- has 36 cells
- has 22 x 36 question-family coverage
- has 4 x 36 cognitive coverage
- has HF002 recurrence
- reaches RELATIVE_CLOSE in the fixture
- records EXECUTED_FULL_CONFIGURED

Missing adapters preserve OPEN rather than falling back to prose or host imitation.

### 5. Current validation is green

At basis commit a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2, GitHub Actions run 36293682595 ("Take-5 Validation") completed successfully.

The workflow runs:

- the entire tests directory
- runtime/system_audit.py
- runtime/closed_loop_v2.py
- the zero-request dump fixture

This supports repository-relative execution closure for the currently tested runtime.

## ICC-123 identity disposition

Do not register ICC123 as a generic configured formal tool merely from the existence of runtime/ic123_math_recovery_campaign.py.

Recovered current object:

IC123-coordinated math recovery campaign.

The direct tool gateway intentionally tests that "run ICC123" fails closed as DIRECT_TOOL_NOT_REGISTERED.

Therefore:

ICC123_campaign != generic_registered_tool

until a distinct formal identity, manifest contract, configured run specification, and semantic execution adapter are admitted.

The prior unrestricted residual-generator completeness problem also remains open.

## Current tool-run invariant

For registered tool T:

ordinary_run(T)
=> configured(T)
and wrapper_required(T)
and geometry(T) = D36_C
and recursive(T)
and closure_required(T)
and reentry_required(T)
and recurrence(T) = HF002

except HF002 itself, whose recurrence engine is SELF.

Bare/core behavior is licensed only by explicit bare/core wording.

## Remaining red frontier after this delta

Still open or not globally established:

- automatic universal ChatGPT host interception across every future chat
- unrestricted ICC-123 residual-generator completeness
- generic registered-tool identity for ICC123
- exact semantic meanings/provenance of Q01-Q22 beyond their current registered family identities
- Q36 as a distinct current formal object
- unrestricted FullMath for several historical/research tool families
- host semantic-provider closure for restored open-ended ImprovementCore execution
- complete whole-system mutation mediation
- global regression-proof persistence outside repository-owned enforcement boundaries

## ImproveCore disposition

Do not modify the already-enforced direct-tool downgrade guard.

Do not invent ICC123 tool identity.

Preserve the recovered D36_C and D36_H currentness update.

Next work is to reduce the remaining red frontier by evidence, not by adding aliases or duplicate wrappers.

## Terminal

BASIS-RELATIVE CURRENTNESS UPDATE: CLOSED

GLOBAL SYSTEM CLOSURE: OPEN
