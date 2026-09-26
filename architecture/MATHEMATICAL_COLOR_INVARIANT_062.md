# Mathematical Color Invariant 062

Date: 2026-09-25
Status: IMPLEMENTED CANDIDATE / VALIDATION REQUIRED

## Job

Control user-visible coloring of mathematical and formal-system objects relative to the current job.

Color is not a property of a name.
Color is a verdict on whether the object's mathematical role is completely figured out for the current job.

## Core law

For formal object x used in context J, ask exactly one binary question:

CompleteForUse_J(x) in {YES, NO}.

CompleteForUse_J(x)=YES
iff
the entire mathematics required for that exact use of x in J is figured out.

That means:
- every mathematical coordinate needed to interpret that use is explicit;
- every required relation and transition is explicit;
- every dependency needed by that use is explicit;
- no required coordinate is missing, partial, ambiguous, conflicting, OPEN, BLOCKED, or merely proposed;
- no unresolved mathematical fact can change what x means in that use.

Then:

GREEN_J(x) iff CompleteForUse_J(x)=YES.
RED_J(x) iff CompleteForUse_J(x)=NO.

There is no intermediate threshold and no appeal to sufficiency, confidence, usefulness, plausibility, or local implementation success.

## Conservative rule

The default is RED.

A name, implementation, partial role, historical meaning, local test pass, or candidate contract does not by itself license GREEN.

## Red conditions

RED is mandatory when any job-required coordinate is:

MISSING
PARTIAL
AMBIGUOUS
CONFLICT
OPEN
BLOCKED
ONLY_NAMED
CANDIDATE_ONLY
IMPLEMENTED_BUT_NOT_SEMANTICALLY_COMPLETE
SEMANTICALLY_DEFINED_BUT_NOT_BOUND_WHEN_BINDING_IS_REQUIRED
UNVERIFIED_WHEN_VERIFICATION_IS_REQUIRED.

## Green conditions

GREEN requires the entire mathematics required by the current use to be figured out.

A narrower claim can be green even when the larger object remains red.

Example:

"The runtime contains hf1_reentry_route" may be GREEN when directly verified.

"HF1 is mathematically complete" remains RED while the complete HF1 state space, transition semantics, minimality, or sufficiency remain open.

## Dependency inheritance

If a visible formal expression y depends on unresolved formal object x for its job-relevant semantics, then y is RED for that job unless y has an independently complete semantics.

Thus an unresolved HF1 can force REENTER_OBSERVE, REVERIFY, and NO_REENTRY red when their exact meanings are being asserted as parts of HF1.

## Claim-relative coloring

The same glyph can legitimately have different colors in different claims.

GREEN means the entire mathematics required by this exact use, in this exact context, is figured out. It does not mean the object is globally complete for every possible use.

## Emission gate

Before emitting a formal object:

1. identify the current job J;
2. identify the claim being made about x;
3. enumerate claim-required coordinates;
4. ask whether the entire mathematics required by this exact use is figured out;
5. emit GREEN only when the answer is YES;
6. otherwise emit RED.

No optimistic promotion from PARTIAL to GREEN.

## Current recovery / identity basis

Canonical recovery anchor:
integration/CURRENT_MATHEMATICAL_COLORING.md

Formal-label identity is now centralized in:
runtime/mathematical_color_gate.py :: FORMAL_OBJECT_ALIASES

Current critical aliases include ImproveCore and HF1 families.

The response-boundary audit:
verify_assistant_response

rejects a registered formal label that remains outside a typed colored operator glyph.

This closes the recurring failure in which a new current formal object was never added
to the older finite formal-label pattern.

## Relationship to wrapper

This contract supplies a candidate resolution for Wrapper Canonical Contract 053 open coordinate O6, human-visible-math formalization.

O6 remains not fully promoted until integration with the emission path and regression evidence are established.


## Assistant response boundary

The invariant applies before final assistant-message emission, not only inside repository runtime calls.

A response is inadmissible when a load-bearing formal object bypasses typed status emission. In particular:

- raw HTML span coloring is forbidden;
- plain-text formal labels are forbidden when status color is required;
- emoji or prefix fallbacks are forbidden;
- a formal label such as ASSERT, GOAL, WRAPPER, PD, MT, or ICC-N is rendered as a LaTeX mathematical glyph carrying its status;
- the final response receives a raw-markup audit before emission.

The response-boundary law is:

AssistantDraft
-> IdentifyFormalObjects
-> AssessStatus
-> TypedMathFragments
-> GlyphColorRender
-> FinalRawMarkupAudit
-> Emit

Any failure in this chain blocks the colored formal object from emission rather than substituting unsupported markup.

This closes the specific bypass that allowed a hand-authored HTML span to evade the repository color gate.


## Recovery rule — 2026-09-26

When coloring breaks, do not reconstruct from chat memory first.

Load:
1. integration/CURRENT_MATHEMATICAL_COLORING.md
2. runtime/mathematical_color_gate.py
3. tests/test_mathematical_color_gate.py
4. runtime/mathematical_color_recovery.py

A new load-bearing formal object is not emission-ready until its canonical identity,
aliases, typed status path, and plain-text bypass regression are registered.
