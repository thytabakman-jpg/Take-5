# HF2 Reapplication — Post Bound-ZIP Intake 127

Date: 2026-09-26
Capability under recurrence: ImprovementCore-selected bound-ZIP repair
Recurrence engine: HF002
Successor branch: improvecore-zip-intake-hf2-20260926
Implementation head before this receipt: 05b311901330192287c417e6fb2a0d02d9300642

## Round 0

Input successor contains:

- ImprovementCore recommendation 126;
- runtime/archive_artifact_intake.py;
- tests/test_archive_artifact_intake.py;
- Artifact-to-Work Intake Contract extension.

Material effect:

The repository-owned graph now contains the previously missing executable edge:

exact immutable GitHub artifact reference + exact ZIP bytes
-> binding verification
-> complete member accounting
-> provenance-linked text ArtifactRecords
-> existing artifact_intake.

Validation:

Take-5 Validation 36276793175: SUCCESS.
Capability Preservation 36276793174: SUCCESS.

HF2 disposition:
REAPPLY_C.

Reason:
the implementation changes the continuation state from missing transition to executable transition.

## Round 1

The two previously identified candidate GitHub Actions artifacts were reacquired through the
connected GitHub host and rechecked byte-for-byte.

Artifact 10901131588:
- byte count 1547;
- SHA-256 7dca0a234c5cd2c5ef0eb894f4582162231fe3901aa806b7b2f933059b28d3ba;
- three declared members;
- every member UTF-8 text.

Artifact 10899752487:
- byte count 1548;
- SHA-256 66afbc7d3a694b3711239b8281f65d8770504686de100df0af089910987954a7;
- three declared members;
- every member UTF-8 text.

The observed member inventory remains:
- closed_loop_receipt.json
- state/example-zero/events.jsonl
- state/example-zero/result.json

This evidence is compatible with the new adapter's admitted domain.

Material distinction preserved:

archive accounting completeness
!=
semantic sufficiency for the user's intended corpus.

The candidate archives remain validation-receipt evidence, not a substitute for a missing
substantive chat-history corpus.

HF2 disposition:
REAPPLY_C.

Reason:
actual host evidence confirms applicability of the new transition while preserving the unresolved
intended-object coordinate.

## Round 2

Search for a new local same-capability residual:

- hash/byte binding: implemented;
- duplicate-name identity: implemented;
- member accounting: implemented;
- no filesystem extraction: implemented;
- size bounds: implemented;
- text routing: implemented;
- provenance propagation: implemented;
- non-text/unreadable preservation: implemented;
- existing controller ownership: preserved.

No further local strict-gain repair is evidenced in this capability.

Still OPEN:
- positive identity of the user's intended substantive ZIP pair;
- host acquisition/interception outside repository authority;
- arbitrary binary semantic extraction.

HF2 terminal disposition:
RELATIVE_CLOSE.

Repository-owned bound-ZIP intake:
CLOSED_RELATIVE on the declared validation basis.
