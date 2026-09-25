# Artifact-to-Work Intake Contract 001

Date: 2026-09-25
Status: CANDIDATE INTERFACE CONTRACT / NOT YET IMPLEMENTED
Source campaign: integration/ICC123_THREE_DAY_RECOVERY_CAMPAIGN_001_2026-09-25.md

## Job

Bridge admitted corpus evidence into existing Take-5 object-admission and endogenous-work machinery.

This is not a new controller or peer analysis tool.

Existing owners remain:
- inventory: take5_dump / corpus traversal;
- identity/currentness: refinery/currentness machinery;
- candidate semantics: emergent admission + typed analysis tools;
- work lifecycle: endogenous_work;
- discovery regeneration: RCDL/representation_discovery;
- execution/admission/closure: IC/TRC/HF/Jane.

## Objects

Let A be the admitted artifact set.

For artifact a in A, let Seg(a) be the set of inspected evidence segments.
A traversal receipt is:

T(a)=<artifact_id,hash,segments_inspected,bytes_covered,parser_status,provenance>.

Traversal completeness means every admitted artifact has a receipt and every byte/declared segment is
accounted for.

Traversal completeness does not imply semantic completeness.

Let candidate classes be:

K={
SEMANTIC_PRIMITIVE,
EQUATION_OR_MAP,
GOAL_OR_SUCCESS_CONDITION,
MECHANISM_OR_CAPABILITY,
RELATION_OR_DEPENDENCY,
STATUS_OR_AUTHORITY_CHANGE,
OPEN_OR_BLOCKED_OBLIGATION,
RUNTIME_BINDING_OR_TRIGGER,
OTHER_LOAD_BEARING_OBJECT
}.

Let G={g_1,...,g_n} be the currently admitted extraction generators.

For artifact a:

Cand_G(a)=union_i g_i(a).

Each candidate c carries:

C(c)=
<id,
 class,
 source_span,
 provenance,
 candidate_referent,
 candidate_type,
 load_bearing_status,
 confidence_or_OPEN,
 affected_objects,
 generator_ids>.

No candidate may govern state merely because it was extracted.

## Intake transform

I_G(A)
=
<TraversalReceipts,
 CandidateSet,
 GeneratorCoverage,
 UnresolvedExtraction,
 Provenance>.

CandidateSet
=
union_{a in A} Cand_G(a).

Then:

CandidateSet
-> identity/currentness
-> emergent admission
-> existing Work/currentness state
-> applicability/disposition
-> binding/execution when required
-> consumer/verification
-> reentry.

## Coverage truth

The system may claim NO_SKIP_TRAVERSAL only when every admitted artifact/segment has a traversal receipt.

The system may not claim COMPLETE_SEMANTIC_EXTRACTION from traversal alone.

Semantic extraction closure is basis-relative:

ClosedExtract_B
iff
all labeled/material witnesses in validation basis B are recovered or explicitly missed
AND no admitted generator on B yields an undispositioned material candidate.

A stronger completeness claim requires an explicit stronger evidence basis.

## Generator evolution

Discovery can add or revise extraction generators.

When G changes materially:

G_t != G_(t+1)
=>
re-run affected artifacts or produce a justified unaffected certificate.

This preserves the Take Two/RCDL rule that a changed representation/generator can change the candidate universe.

## Anti-loss

Every material extracted candidate receives exactly one durable outcome:

ADMITTED_CURRENT
MERGED_OR_SUBSUMED
REJECTED_WITH_GROUNDS
RESEARCH
OPEN_WITH_REENTRY
BLOCKED_WITH_OWNER
HISTORICAL_ONLY.

No extracted material candidate may disappear because its exact destination is unresolved.

## Surface-minimality result

Do not create a separate "UIF" registry by default.

Unresolved extracted candidates should first be represented as typed Work/currentness state with:
- reason_not_integrated;
- reopen_condition;
- affected relations/consumers;
- provenance;
- binding/integration status.

A new storage surface requires proof that existing state plus a derived view cannot preserve this behavior.

## Validation obligations

V1 no-skip artifact traversal on a frozen corpus.
V2 recovery of known load-bearing-word fixtures.
V3 recovery of known equation/map fixtures.
V4 recovery of hidden policy/stopping-rule fixtures.
V5 synonym/duplicate case merges rather than multiplying objects.
V6 OPEN candidate persists and reopens on a matching delta.
V7 generator change triggers affected re-scan.
V8 extracted executable claim cannot become executable without binding.
V9 all admitted candidates reach Work/currentness or a typed terminal disposition.
V10 false-negative holdout on unfamiliar artifacts.

## Current disposition

Mathematical/interface contract: SPECIFIED.
Runtime implementation: OPEN.
Global semantic completeness: NOT CLAIMED.
