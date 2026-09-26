# Assistant Response Emission Boundary 065

Date: 2026-09-25
Status: CURRENT EMISSION BOUNDARY CONTRACT

## Problem

Repository rendering rules can be correct while a conversational response bypasses them by hand-authoring presentation markup.

That happened when a formal tool label was emitted through a raw HTML span even though the repository color gate already rejected raw spans.

## Root cause

The protected color path ended at repository runtime output rather than at the final assistant-message boundary.

The defect is therefore a boundary bypass:

semantic status -> protected renderer

was enforced inside Take-5, while

assistant draft -> final user-visible message

was not forced through the same invariant.

## Goal

No load-bearing formal object reaches the user without:

1. job-relative mathematical status;
2. typed formal-object classification;
3. glyph-level red/green projection;
4. raw-markup rejection;
5. a final response audit.

## Required pipeline

AssistantDraft
-> FormalObjectScan
-> StatusAssessment
-> TypedMathEmission
-> GlyphColorProjection
-> ResponseBoundaryAudit
-> UserVisibleMessage

## Hard prohibitions

- no hand-authored HTML span color;
- no plain-text substitute for a status-bearing formal object;
- no emoji/prefix substitute;
- no status promotion from local implementation success;
- no bypass merely because the text was generated outside repository runtime.

## Chat rendering projection

For registered formal labels, use the same LaTeX glyph-color path as mathematical expressions.

Example representation:

RECOVERED formal label -> colored operatorname glyph
UNRESOLVED formal label -> colored operatorname glyph

The status is semantic; the LaTeX color is the current chat projection.

## Closure test

This defect is relatively closed only when:

- the runtime rejects raw HTML;
- the runtime can render registered formal labels through typed LaTeX glyph coloring;
- regression tests cover both;
- the canonical invariant explicitly includes the assistant response boundary;
- future assistant responses use that path rather than hand-authored HTML.


## Current implementation update — 2026-09-26

The final audit is now explicitly implemented as verify_assistant_response.

It masks supported typed colored formal-label glyphs and then scans the remaining
response for registered formal labels.

Any remaining registered label fails with:
UNTYPED_FORMAL_LABEL_AT_RESPONSE_BOUNDARY.

The registered identity basis is centralized in FORMAL_OBJECT_ALIASES so current
objects such as ImproveCore and HF1 cannot depend on an unrelated older regex list.

Recovery anchor:
integration/CURRENT_MATHEMATICAL_COLORING.md
