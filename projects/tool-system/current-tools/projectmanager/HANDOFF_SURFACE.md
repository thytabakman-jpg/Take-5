# Handoff surface: ProjectManager

The package coverage directory uses:

Scope x ModeFace = 6 x 6 = 36.

The separate semantic handoff surface is:

SourceScope x TargetScope = 6 x 6 = 36.

Equal cardinality does not make these the same object.

When ProjectManager has result-sensitive directed handoff semantics, those
belong in the semantic-object package / directed-handoff authority, not in the
Scope x ModeFace coverage pages.


## Candidate admission handoff

ProjectDefinitionCandidate -> ImprovementCore
is evidence-only and grants no project authority.

ImprovementCore -> ProjectDefinitionCandidate
returns research or improvement evidence for reassessment.

ProjectDefinitionCandidate -> ManagedProject
is not an automatic handoff.
It requires DEFINITION_READY plus explicit USER approval, followed by a separately admitted PROMOTE transition.

The 6 x 6 directed scope handoff surface remains distinct from this lifecycle transition.

## Concrete runtime handoff boundary

The native ImprovementCoreHandoff has project_id, project_fingerprint,
`work` (the actual serialized executable_frontier), authority=NONE and
effect_class=EVIDENCE_ONLY. Candidate-admission handoffs use candidate_id,
candidate_fingerprint and blocking_open; they do not create a ManagedProject.
TransferEvidenceCandidate grants_authority=false even if a recovered identity
later makes a payload a candidate for target-side admission.

The nine-coordinate candidate definition becomes PROMOTION_READY only after
its syntax-level USER: approval guard; an independently authorized, separately
admitted PROMOTE must still validate the real user approval and the unchanged
project precondition. Neither this descriptive page nor any Scope x ModeFace
coverage shell supplies such authorization. Consumer owners remain
runtime/project_manager.py and projects/project-manager/HANDOFFS.md.
