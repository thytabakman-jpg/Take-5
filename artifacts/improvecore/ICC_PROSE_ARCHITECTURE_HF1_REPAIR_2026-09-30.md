# ICC PROSE + ARCHITECTURE HF1 Repair Run

Date: 2026-09-30
Status: VALIDATED / MERGED
Branch: fix/prose-architecture-reader-load-20260930
Math basis: architecture/PROSE_ARCHITECTURE_READER_LOAD_MATHEMATICS_004_2026-09-30.md

## ASSERT

Observed claim: PROSE and ARCHITECTURE were both able to accept a Canonical Authority
passage that remained semantically correct but was reader-clunky and structurally compressed.

Disposition: CONFIRMED.

The failure decomposes into two distinct coordinates:
- PROSE lacked reader-processing-load acceptance.
- ARCHITECTURE lacked a native unit-job-purity invariant.

## PD + MT

Result-sensitive perturbations:
- same semantics and structure, different reader load -> prose result changes;
- same sentences and semantics, different paragraph/job partition -> architecture result changes.

MT boundary:
- word count is not a sufficient proxy for clunkiness;
- reader load therefore requires evidence-bearing evaluation;
- paragraph purpose remains environment-bound architecture evidence.

## ARCHITECT

Ownership split admitted:
- PROSE owns READER_LOAD.
- ARCHITECTURE owns UNIT_JOB_PURITY.

The Canonical Authority example resolves into two units:
1. STATE_RESEARCH_QUESTION.
2. DELIMIT_SCOPE_EXCLUSIONS.

## Raise the Ceiling

Strict-gain candidate admitted because it preserves existing prose gates, semantic-strength
receipts, Architecture OPEN/BLOCKED behavior, configured identity, and result carrier while
adding the two missing coordinates.

Rejected alternative:
- fixed word-count or punctuation heuristics as a universal clunkiness detector.

## HF1 bundle

Repair obligations:
- PROSE_READER_LOAD
- ARCHITECTURE_UNIT_JOB_PURITY

One sufficient repair package covers both. A result-sensitive delta requires REVERIFY before
relative close.

Regression witness:
- tests/test_hf1_episode.py::test_hf1_bundles_prose_reader_load_and_architecture_unit_job_repair

## Implementation witnesses

- runtime/prose.py
- runtime/architecture_analysis.py
- runtime/tool_manifest.py
- runtime/tool_run_registry.py
- tests/test_prose.py
- tests/test_prose_transition_layers.py
- tests/test_hf1_episode.py

## Closure

HF1 repair disposition: RELATIVE_CLOSE.

Validation evidence:
- Take-5 Validation run 36724235054: SUCCESS
- Capability Preservation run 36724235102: SUCCESS
- Tool System Every-Tool Sweep run 36724234958: SUCCESS
- PR #185: MERGED
- merge commit: ea5898b40ede0b4ef456d94d3d5e4b99ae2b6d06

The observed regression now has explicit result-sensitive ownership in both Prose and
Architecture. Missing reader-load or unit-job evidence fails open rather than passing
silently.
