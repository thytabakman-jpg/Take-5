# PROSE Plain-Language RTC36 + HF2 Mathematics 006

Date: 2026-10-01
Status: GREEN / FROZEN BEFORE ADMISSION
Tool under improvement: Prose
Improvement operator: RTC / C48 Raise Ceiling
Geometry: D36_C
Recurrence: HF002
Parent:
- architecture/PROSE_PLAIN_LANGUAGE_RTC_MATHEMATICS_005_2026-10-01.md

## Preserved basis

The successor preserves:
- semantic preservation before readability optimization;
- earned claim strength;
- no unsupported inflation;
- required logical and technical distinctions;
- exact mathematics, code, quotations, and source-exact forms where fidelity requires them;
- PLAIN_LANGUAGE as distinct from READER_LOAD;
- no silent rewriting;
- typed PASS / REPAIR_REQUIRED / OPEN / BLOCKED outcomes.

## Raised rule

Use the clearest ordinary wording that keeps the exact meaning. Prefer simpler
words and sentences when they are equally precise. Keep technical terms when
they are needed. When a plain-language explanation makes a necessary technical
term easier to understand without changing the claim, keep the term and add the
explanation.

"Simple" means easier for the intended reader to understand. It does not mean
shorter, fewer syllables, or fewer words.

## Successor mathematics

Let A be the intended reader context and let Alt_A(p) be the realizations that
preserve the frozen semantic content, claim strength, qualifications, formal
relations, and required technical distinctions.

Let L_A(q) be reader burden for q relative to A.

PlainLanguage_A(p) iff there is no q in Alt_A(p) such that

L_A(q) < L_A(p)

while every protected semantic coordinate remains equal.

A longer q can dominate a shorter p when q lowers reader burden while
preserving the same meaning. This licenses ordinary-language glosses for
necessary technical terms without weakening the formal term itself.

If the reader baseline needed for a comparison is unresolved, the judgment
remains OPEN rather than being treated as universal.

## 36-dimensional observer pass

| # | Scope | Mode face | Finding |
|---:|---|---|---|
| 1 | SYSTEM | EXPAND | Treat plain language as a property of wording, not isolated vocabulary only. |
| 2 | SYSTEM | CONTRACT | Define simplicity as lower reader burden among equally exact realizations, not shorter text. |
| 3 | SYSTEM | INWARD | Freeze meaning, claim strength, qualifications, and required distinctions before comparing simplicity. |
| 4 | SYSTEM | OUTWARD | Carry PROSE_PLAIN_LANGUAGE_GATE through every configured Prose invocation; a registry omission was found. |
| 5 | SYSTEM | ISOLATE | Keep technical terms, quotations, code, and formal notation exact when precision requires them. |
| 6 | SYSTEM | COUPLE | Couple plain-language evidence to semantic-preservation and no-inflation receipts; accuracy remains prior. |
| 7 | SUBSYSTEM | EXPAND | Allow a required technical term to remain while adding a plain-language gloss when that lowers reader burden. |
| 8 | SUBSYSTEM | CONTRACT | A gloss is a gain only when it preserves the claim and adds no new commitment. |
| 9 | SUBSYSTEM | INWARD | Judge alternatives comparatively; do not use a forbidden-word list. |
| 10 | SUBSYSTEM | OUTWARD | Keep formal mathematics exact and simplify the explanatory prose around it. |
| 11 | SUBSYSTEM | ISOLATE | Keep PLAIN_LANGUAGE distinct from READER_LOAD; either can fail independently. |
| 12 | SUBSYSTEM | COUPLE | Use both gates together when a passage is lexically plain but structurally difficult, or vice versa. |
| 13 | COMPONENT | EXPAND | Check needless academic phrases and nominalizations as well as single words. |
| 14 | COMPONENT | CONTRACT | Protect logical operators, scope, modality, quantifiers, and terms of art. |
| 15 | COMPONENT | INWARD | A rewrite is admissible only inside the semantic-equivalence class. |
| 16 | COMPONENT | OUTWARD | When a term must remain, an ordinary-language explanation can be the lower-burden realization. |
| 17 | COMPONENT | ISOLATE | Brevity is not the objective; a longer explanation can be easier to understand. |
| 18 | COMPONENT | COUPLE | Regression evidence must include both necessary-term cases and simple-equivalent replacement cases. |
| 19 | INTERFACE | EXPAND | Ordinaryness is relative to the intended reader; evidence must make the reader baseline explicit enough to support the judgment. |
| 20 | INTERFACE | CONTRACT | Unresolved audience assumptions remain OPEN rather than silently treated as universal. |
| 21 | INTERFACE | INWARD | REPAIR evidence should name the simpler equivalent or the exact source of avoidable burden. |
| 22 | INTERFACE | OUTWARD | Expose PASS, REPAIR_REQUIRED, OPEN, and BLOCKED without silent rewriting. |
| 23 | INTERFACE | ISOLATE | Keep the tool evaluative; rewriting remains a separate action. |
| 24 | INTERFACE | COUPLE | Default-contract additions can mask other regression tests; one negative-first test passed for the wrong reason because PLAIN_LANGUAGE evidence was missing. |
| 25 | BOUNDARY_DECOMPOSITION | EXPAND | Separate exact source/formal layers from editable explanatory prose. |
| 26 | BOUNDARY_DECOMPOSITION | CONTRACT | Do not simplify quoted wording, equations, code, or canonical labels that require exact reproduction. |
| 27 | BOUNDARY_DECOMPOSITION | INWARD | Apply the simplicity comparison only to editable reader-facing prose. |
| 28 | BOUNDARY_DECOMPOSITION | OUTWARD | Permit a separate explanatory layer after formalism instead of altering the formalism itself. |
| 29 | BOUNDARY_DECOMPOSITION | ISOLATE | Retain rejection of word blacklists and mechanical readability thresholds. |
| 30 | BOUNDARY_DECOMPOSITION | COUPLE | Evidence can jointly witness exact formal content and a lower-burden explanation. |
| 31 | CROSS_LAYER | EXPAND | Direct commands, ImprovementCore, PTI, and ToolConductor all need the plain-language behavior in their configured identity. |
| 32 | CROSS_LAYER | CONTRACT | The configured-run protected list must include the canonical plain-language gate. |
| 33 | CROSS_LAYER | INWARD | The canonical manifest contains the gate while tool_run_registry omits it: concrete cross-layer mismatch. |
| 34 | CROSS_LAYER | OUTWARD | Add a regression test so the full-invocation audit cannot silently miss this Prose-specific omission again. |
| 35 | CROSS_LAYER | ISOLATE | Retain the 005 artifact as historical evidence; successor 006 owns the refinements. |
| 36 | CROSS_LAYER | COUPLE | HF2 reapplies RTC36 after the repair; close only after the successor pass finds no further strict gain. |

## C48 candidate frontier

### G1 — configured-run protection closure

Add PROSE_PLAIN_LANGUAGE_GATE to the Prose protected-behavior list used by
CONFIGURED_RUNS and lock it with a full-invocation regression test.

strict_gain = true
preserves = true

Disposition: ACCEPT.

### G2 — regression-test isolation

The final-emission negative-first test uses the default Prose contract but did
not supply PLAIN_LANGUAGE PASS evidence. It can therefore pass because the new
plain-language gate is OPEN instead of proving that NOT_MERELY caused the
block.

Supply plain-language PASS evidence and assert that the exception contains
NOT_MERELY.

strict_gain = true
preserves = true

Disposition: ACCEPT.

### G3 — clarity over brevity

Make explicit that reader burden, not word count, is the optimization target.
A necessary technical term can remain exact while an ordinary-language gloss
is added when the gloss lowers burden without altering the claim.

strict_gain = true
preserves = true

Disposition: ACCEPT.

This refines the mathematics and interpretation of the existing
PROSE_PLAIN_LANGUAGE_GATE. It does not create a second gate.

### Rejected / OPEN successor classes

- forbidden academic-word lists: reject; context can make a difficult term necessary;
- mechanical readability thresholds: reject; they can reward loss of precision;
- automatic replacement of technical terms: reject; it can erase distinctions;
- mandatory shortening: reject; shorter can be harder to understand;
- a new mandatory audience-schema field: OPEN / no demonstrated strict gain yet.
  The current evidence channel can state the reader baseline; promote a new field
  only after a concrete failure shows that the evidence channel is insufficient.

## HF2 recurrence

### Round 1

Input: 005 successor state.

RTC36 result:
- material result delta: true;
- live local frontier: true;
- accepted gains: G1, G2, G3.

Disposition: REAPPLY_C.

### Round 2

Input: successor with G1, G2, and G3 applied.

All 36 cells were re-observed against the preserved basis.

Result:
- no additional strict-gain candidate established;
- no protected coordinate weakened;
- no upstream invalidation;
- local frontier closed relative to the current Prose contract and repository-owned invocation routes.

Disposition: RELATIVE_CLOSE.

## New current lineage

No new behavior ID is introduced.

Current protected behavior remains:

PROSE_PLAIN_LANGUAGE_GATE

with the stronger 006 interpretation above.
