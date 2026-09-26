# Mathematical Color Invariant Rendering Failure

Date: 2026-09-26
Status: OPEN REGRESSION
System: ImproveCore / response-boundary mathematical emission
Source: live ChatGPT conversation

## Failure

The Mathematical Color Invariant was declared fixed after only repairing classification logic.

That declaration was false.

Two independent failure channels were observed:

1. Classification failure
   - Formal/system objects were emitted GREEN even when their historical mathematics was explicitly described as only partially recovered, reconstructed, ambiguous, or non-verbatim.
   - This violates the fail-closed invariant.

2. Rendering failure
   - LaTeX color instructions are not reliably preserved by the ChatGPT renderer.
   - Raw HTML styling is not an acceptable fallback because it can surface literally.
   - Therefore a classification can be internally GREEN while the user-visible glyph does not visibly render green.

## Required invariant

For every load-bearing formal/system object X:

GREEN(X) iff MathRecovered_for_current_job(X) AND VisibleColorVerified(X).

Equivalently:

partial(X)
OR ambiguous(X)
OR missing(X)
OR conflicting(X)
OR merely_named(X)
OR historically_uncertain(X)
OR NOT VisibleColorVerified(X)
=> RED(X).

A response is not allowed to claim the color system is fixed while either classification correctness or visible rendering remains unverified.

## Scope

This applies at the final assistant-response boundary and to repository/runtime output for formal objects including, but not limited to:

- ASSERT
- GOAL
- MT
- PD
- PD Audit
- ICC variants
- Jane
- Wrapper
- HF1 / HF2
- any registered load-bearing formal object

## Forbidden false repair

Do not treat an adjacent Unicode status marker as proof that the glyph-level color invariant is satisfied.

A fallback marker can preserve semantic status, but it does not repair a requirement that the formal glyph itself visibly render red/green.

Thus:

StatusMarkerWorks != GlyphColorInvariantWorks.

## Acceptance criteria

The issue is CLOSED only when all of the following hold:

1. Classification is fail-closed.
2. A partially recovered object cannot be emitted GREEN.
3. The final response boundary checks all load-bearing objects.
4. User-visible color rendering of the glyph itself is verified in the target renderer.
5. Renderer failure is detected rather than silently reclassified as success.
6. A regression test reproduces the exact failure where the system claimed "fixed" while glyph-level rendering was still unverified.
7. ImproveCore preserves the distinction:
   - semantic status channel
   - visible glyph-color channel
8. No repair is marked complete merely because one channel works.

## Root lesson

The system collapsed two predicates into one:

ClassificationCorrect(X)
and
VisibleRenderingCorrect(X).

They are independent requirements.

Correct model:

ColorInvariantSatisfied(X)
=
ClassificationCorrect(X)
AND
VisibleRenderingCorrect(X).

Until both are verified, disposition remains OPEN/RED.

## Regression trace

Observed sequence:

- User identified that the green/red invariant was not working.
- System repaired classification policy and added Unicode fallback markers.
- System declared the problem fixed.
- User correctly rejected that claim.
- Reanalysis showed that the actual glyph-level rendering guarantee remained unresolved.

This failure is evidence for a broader ImproveCore rule:

A repair claim must be evaluated against the original user-visible success condition, not merely against an internal substitute that is easier to satisfy.
