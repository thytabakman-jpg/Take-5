# CURRENT MATHEMATICAL COLORING — Recovery Anchor 085

Date: 2026-09-26
Status: CURRENT RECOVERY AUTHORITY
Canonical repository: thytabakman-jpg/Take-5

## Purpose

This is the first recovery surface when mathematical/formal-system coloring breaks.

The recurring failure class is not merely a rendering bug. It is a boundary-bypass
bug: a formal object can be mathematically classified correctly in repository code and
still reach the user as an untyped plain-text label if the final response bypasses the
typed emission path.

## Governing invariant

For a formal object x used in job J:

CompleteForUse_J(x) is binary.

GREEN_J(x) iff every mathematical coordinate required by that exact use is recovered,
admitted, or verified.

Otherwise RED_J(x).

No confidence threshold, familiarity, implementation presence, or local test pass can
promote an incomplete object to green.

Default is RED.

## Current implementation

runtime/mathematical_color_gate.py

One central alias registry now owns formal-label identity:

FORMAL_OBJECT_ALIASES

It includes current critical objects and aliases including:

- ASSERT
- GOAL
- WRAPPER
- MT
- PD
- ICC-N
- ImproveCore / Improve Core / ImprovementCore / Improvement Core
- HF1 / HF-1 / HF001 / HF-001

Aliases normalize to one canonical formal object identity before rendering.

## Required response path

AssistantDraft
-> IdentifyFormalObjects
-> AssessStatus
-> TypedMathFragments
-> GlyphColorRender
-> ResponseBoundaryAudit
-> Emit

The supported formal-label renderer is:

render_formal_label(label,status)

The response-boundary audit is:

verify_assistant_response(rendered)

A registered formal label that remains outside a typed colored operator glyph fails with:

UNTYPED_FORMAL_LABEL_AT_RESPONSE_BOUNDARY

## Recovery test

Run:

tests/test_mathematical_color_gate.py

Critical regressions include:

- raw HTML color rejected;
- emoji/prefix fallback rejected;
- plain formal labels rejected;
- ImproveCore aliases registered;
- HF1 aliases registered;
- typed colored ImproveCore/HF1 accepted;
- unspecified mathematical coordinates fail closed RED.

## Why the bug recurred

The earlier gate registered only a finite older set of names. ImproveCore and HF1 were
not in that registry even though they had become central formal objects.

Therefore the repository had a strong invariant with an incomplete identity basis.

The repair moves identity normalization into a single explicit alias registry and makes
current critical aliases regression-tested.

## Anti-loss rule

When a new load-bearing formal/system object becomes current, it must be added to
FORMAL_OBJECT_ALIASES in the same change that makes it user-visible.

A new formal object is not emission-ready until:

1. its canonical identity is registered;
2. its aliases are registered;
3. its recovery coordinates are defined for the intended claim;
4. red/green rendering tests exist;
5. plain-text response-boundary bypass is tested.

## Host boundary

Take-5 can fail closed only when the host uses the Take-5 emission/audit path.

An unrelated chat host that never invokes the repository audit cannot be mathematically
forced by GitHub code.

Therefore "permanent" means fail-closed, regression-tested, recoverable, and current
inside the canonical system, with the external host boundary explicitly OPEN.

## Recovery load order

1. integration/CURRENT_MATHEMATICAL_COLORING.md
2. architecture/MATHEMATICAL_COLOR_INVARIANT_062.md
3. architecture/ASSISTANT_RESPONSE_EMISSION_BOUNDARY_065.md
4. runtime/mathematical_color_gate.py
5. tests/test_mathematical_color_gate.py
6. runtime/mathematical_color_recovery.py
7. tests/test_mathematical_color_recovery.py


## Validated implementation evidence

PR #55
- merge 39ca5616d3d8e23042f0ac887d0a447e24ec8ddf
- validation 36221315384
- full Take-5 test suite passed
- canonical whole-system audit passed
- closed-loop fixture passed
- zero-request dump passed
