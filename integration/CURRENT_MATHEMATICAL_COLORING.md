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

Canonical identity registry:
runtime/formal_object_registry.py

Rendering and enforcement:
runtime/mathematical_color_gate.py

The formal-object registry derives the configured tool population directly from:
runtime/tool_run_registry.py

FORMAL_OBJECT_ALIASES is therefore a projection of the live configured system plus the explicitly declared non-tool formal primitives, not a private hand-maintained vocabulary inside the renderer.

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

The root repair separates identity from rendering.

Configured system identities are derived automatically from the live configured-run registry. Non-tool mathematical/system primitives are declared in the formal-object registry. The renderer consumes that registry and does not maintain an independent object list.

Portfolio regression now iterates every configured system identity and proves both:
- typed colored emission is accepted;
- the same identity in plain text is rejected.

## Anti-loss rule

When a new configured tool becomes current, color governance is inherited automatically from the live configured-tool registry.

A non-tool load-bearing mathematical/system primitive must be added to runtime/formal_object_registry.py in the same change that makes it user-visible.

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
4. runtime/formal_object_registry.py
5. runtime/mathematical_color_gate.py
6. runtime/tool_run_registry.py
7. tests/test_mathematical_color_gate.py
8. runtime/mathematical_color_recovery.py
9. tests/test_mathematical_color_recovery.py


## Validated implementation evidence

PR #55
- merge 39ca5616d3d8e23042f0ac887d0a447e24ec8ddf
- validation 36221315384
- full Take-5 test suite passed
- canonical whole-system audit passed
- closed-loop fixture passed
- zero-request dump passed


## Root-fix validation evidence

PR #60
- merge 2fa3b50102c0f7ce1017b763e4a85ce40e26a7ff
- validation 36221898366
- full configured system portfolio color-governed
- full Take-5 test suite passed
- canonical whole-system audit passed
- closed-loop fixture passed
- zero-request dump passed


## SHOW_ME_THE_MATH job specialization

The request contract in:

integration/CURRENT_SHOW_ME_THE_MATH.md

is a stricter exact-use specialization of CompleteForUse_J.

When J = SHOW_ME_THE_MATH, GREEN requires recursive portability closure, not merely
sufficient local semantics for the current conversation.

For a formal symbol s:

GREEN_(J,showmath)(s)

iff s and every load-bearing dependency reachable from s are defined in the supplied
mathematical package or terminate in an explicitly typed and available external
primitive, and the claim-relevant initialization/runtime/persistence/equivalence
obligations are satisfied.

Otherwise RED_(J,showmath)(s).

Therefore:
- a repository pointer does not make a symbol green;
- prior conversation memory does not make a symbol green;
- a named operator with an unrecovered definition stays red;
- a source-recoverable but unbundled dependency stays red for standalone portability;
- executable availability and formal reconstruction must be distinguished.

Canonical formal definition:
architecture/FULL_TOOL_MATHEMATICAL_IDENTITY_CONTRACT_002_2026-09-26.md

Operational checker:
runtime/show_me_the_math_contract.py
