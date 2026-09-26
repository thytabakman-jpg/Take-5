# ImprovementCore + HF2 Observer — Two GitHub ZIP Evidence 124

Date: 2026-09-26
Controller: ImprovementCore / IC-028
Regime: 091
Mode: OBSERVE_DECOUPLED
Recurrence: HF002
Domain mutation: forbidden
Input:
- GOAL_TWO_GITHUB_ZIPS_HF2_RUN_123_2026-09-26.md
- current Take-5 recovery anchors
- connected GitHub evidence gathered in this run

## Round 0

Observation:

The system already has the two downstream owners needed after bytes are available:

- runtime/artifact_intake.py
- runtime/improvement_core_external_acquisition.py

Therefore a new archive-analysis controller would duplicate ownership.

Material delta:
separate missing input binding from already-owned traversal and controller logic.

HF2:
REAPPLY_C.

## Round 1

Observation:

The recurring failure is addressability.

The phrase "the two ZIP files in GitHub" does not currently resolve to two unique immutable GitHub objects.

Default-branch trees, releases, repository issues, and the most relevant history/chat branches do not supply the pair.
GitHub Actions exposes multiple downloadable ZIP-form artifacts, so choosing two from that set would be speculative.

Material delta:
the missing seam is GitHub object binding, not ZIP parsing or semantic extraction.

HF2:
REAPPLY_C.

## Round 2

Observer recommendation:

Do not create another controller.

Use a minimal evidence-binding receipt at the host/repository boundary:

GitHubArtifactRef =
<repository,
 object_class,
 stable_id,
 source_ref,
 observed_name,
 byte_count,
 content_hash,
 observed_at>.

Then route:

GitHubArtifactRef
-> acquire exact bytes
-> ArtifactRecord / archive-member traversal receipts
-> artifact_intake
-> currentness/admission
-> ImprovementCore
-> persistence/reentry.

Important:
The binding receipt does not self-authorize evidence.
It only prevents object confusion and repeated search.

## Recommended next action

First resolve the pair to exact GitHub object identities.
Then ingest both archives completely through existing owners.
Only add runtime structure when a measured residual remains after that composition.

## HF2 terminal disposition

The recommendation is stable under another observer recurrence.

HF2[ImprovementCore observer]:
RELATIVE_CLOSE.

Mutation:
false.

Recommendation:
BIND_EXACT_GITHUB_OBJECTS_THEN_REUSE_EXISTING_INTAKE.
