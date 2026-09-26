# Legacy Candidate Control Holdout Receipt 131

Date: 2026-09-26
Status: EXECUTED / PASS
Candidate: runtime/improvement_core_legacy_candidate.py

## Execution evidence

GitHub Actions run:
36278954818

Artifact:
improvecore-legacy-holdouts-131

Artifact id:
10918046287

Artifact digest:
sha256:a7cb7f0f6426a531e4b3e0c5a93e5d9f92b5dcfe7f1d1d4cc647c56f1621997f

Take-5 Validation on the same PR successor:
36278954823 SUCCESS

Capability Preservation on the same PR successor:
36278954772 SUCCESS

## Holdout results

1. formal_research
- activation: CHEAP_DIRECT
- selected only counterexample_check rather than the heavier full-spectrum package
- result: COMPLETE
- PASS

2. artifact_work
- first activation: FIRE
- preserved structure_probe and copy_probe as a nondominated plural frontier
- material representation delta changed the state
- second activation: CHEAP_DIRECT
- selected finalize_structure
- result: COMPLETE
- PASS

3. external_archive_recovery
- unavailable master archive remained OPEN
- no invented object identity
- PASS

4. system_debug
- missing configured RootCause adapter remained OPEN
- no generic execution substitution
- PASS

## Ablation results

Question-generation ablation:
ICC128_LIVENESS_FAILURE:G_Q_empty_with_admitted_continuation
PASS as causal guard evidence.

Result-sensitive-update ablation:
ICC128_RESOURCE_BOUND:max_iterations
PASS as causal guard evidence that unchanged state cannot masquerade as progress.

## Aggregate

Control holdouts:
4/4 PASS.

Causal ablations:
2/2 PASS.

Current fixed-stage ImprovementCore baseline:
16 serial goal-directed stages.

Candidate semantic-effectiveness evidence:
PARTIAL_EVIDENCE_ONLY.

Promotion remains:
OPEN_PENDING_UNLIKE_OPEN_ENDED_SEMANTIC_HOLDOUTS
and full modern-guard wrapper verification.

This receipt is evidence, not self-authorizing promotion.
