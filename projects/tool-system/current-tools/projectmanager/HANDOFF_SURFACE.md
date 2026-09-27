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
