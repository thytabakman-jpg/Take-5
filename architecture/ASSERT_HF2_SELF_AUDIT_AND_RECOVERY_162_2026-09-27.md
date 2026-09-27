# ASSERT + HF002 Self-Audit and Recovery Record 162

Date: 2026-09-27
Status: RECORDED EVIDENCE / OPEN REPAIR FRONTIER
Controller: ICC / current configured ASSERT with HF002 recurrence
Branch: fix/improvecore-red-closure-20260927

## Purpose

Durably preserve the findings from the current conversation before further repair.
This record is evidence for ImprovementCore. It does not promote unresolved mathematics merely because it is recorded.

## Recovered math pair

### A. Cheap 36-face pre-wrapper candidate

```text
PD^36_cheap(Q,X)
=
RS_Q(
  union_{ell in A_Q(X)}
  D^+_ell(X)
)
```

Intended execution shape:

```text
36 cheap face probes
-> one union
-> one result-sensitivity filter
```

Current status: OPEN / CANDIDATE.

Reasons:
- RS_Q is not yet fully reduced to executable primitive mathematics.
- D^+_ell is not yet fully reduced to executable primitive mathematics.
- A_Q(X) is not yet fully reduced to executable primitive mathematics.
- the equivalence between union-then-filter and filter-then-union is not proved;
- the cheapness claim is not yet closed because active-face detection itself has a cost.

Recovered geometry:

```text
L_36 = S_6 x M_6
|L_36| = 36
```

### B. Show-Me-the-Math characteristic equation

```text
Sigma = 1_{Delta intersect Omega intersect Phi intersect Xi}
```

Current status: SOURCE-BACKED / IMPLEMENTED.

Current runtime implementation:
runtime/show_me_the_math_portable.py

The four runtime conditions are:
- DefinitionClosed
- ObligationClosed
- RealizerAvailable
- ProtectedEquivalent

## Current ASSERT identity

Current full ASSERT is:

```text
ASSERT*
=
Fix[
  ASSERT
  -> COMPARE
  -> RESOLVE
  -> HERE
  -> COMPARE
  -> INQUIRE
  -> REASSERT
]
```

Current configured ASSERT requires typed D36_C and all three surfaces:

1. Layer 1
   - seven protected ASSERT stages x 36 cells

2. Layer 2
   - Q01 through Q22 x 36 cells

3. Cognitive 36
   - DIFFERENTIATE
   - RELATE
   - RECONSTRUCT
   - STRENGTHEN
   - each x 36 cells

## ASSERT self-audit under HF002

HF002 re-applies the same capability to a materially changed normalized successor while the upstream basis remains stable.

The self-run exposed two current defects.

### D1. Coverage-plan / semantic-execution split

runtime/assert_full36.py constructs the full 36 plan.

runtime/assert_compound.py executes the seven-stage fixed-point engine.

The current evidence does not establish that every planned 36 cell is actually supplied as a semantic input to every protected stage/question/cognitive operator during one bound configured ASSERT execution.

Therefore:

```text
Full-36 coverage declaration
!=
Full-36 semantic execution
```

until the binding is made executable and regression-tested.

### D2. Closure contract / shell-default split

The ASSERT contract requires:

```text
Verified
and ResultStable
and DiscoveryStable
and QuestionClosed
and ResidualClosed
```

before relative closure.

The generic orchestration shell in runtime/assert_compound.py permits closure_gate=None.

Therefore a configured ASSERT path must not be allowed to inherit the generic optional gate.
The configured ASSERT adapter must supply a mandatory closure gate matching the stronger contract.

## Required repair

1. Bind the D36_C plan into actual semantic ASSERT execution.
2. Make the strong ASSERT closure gate mandatory for configured ASSERT.
3. Preserve Layer 1, Layer 2 and Cognitive 36 as distinct required surfaces.
4. Run ASSERT through HF002 after every material discovery delta until the same full object stabilizes.
5. Reverify any prior claim that specifically depended on full semantic 36 execution.

## Affected-cone rule

Prior claims are not automatically false.

Use:

```text
depends_on_full_semantic_ASSERT36(claim)
=> NEEDS_REVERIFY
```

Claims independent of this defect retain their existing status.

## Current strong tool-reality frontier

On validated post-PR-161 main, the exact generic-only/native-unrecovered peer-tool frontier is:

- MTA
- Architecture
- PD
- PDAudit

This is the current first ImprovementCore closure target.

Do not synthesize identities merely to make the audit green.
Recovery requires an independently grounded native semantic identity plus executable realization and regression evidence.

## Anti-loss note

An earlier conversational claim said a Markdown file containing the recovered pair had already been saved and committed.
Repository inspection did not confirm that claimed file.
This record supersedes that unsupported save claim and is the durable recovery anchor for the conversation findings.
