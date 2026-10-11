# Handoffs

Status: CURRENT

## ImprovementCore handoff

Runtime payload from improvementcore_handoff(assessment)
project_id
project_fingerprint
work = assessment.executable_frontier
effect_class = EVIDENCE_ONLY
authority = NONE

The name `work` is the serialized runtime field; the executable work frontier
is its *meaning*, not a separate payload key. Work remains subject to
licensing, dependency and ownership checks before any separate execution.

Returned ImprovementCore outputs re-enter as evidence and do not bypass project authority.

For a ProjectDefinitionCandidate, the observer adapter uses a separate
candidate handoff with candidate_id, candidate_fingerprint, blocking_open,
authority = NONE and effect_class = EVIDENCE_ONLY. Candidate exploration
cannot implicitly create or change the 21-coordinate ManagedProject.

## Transfer handoff

Payload
project_id
project_fingerprint
reusable evidence or lesson candidate
transfercore_identity_status
effect_class = EVIDENCE_ONLY
grants_authority = false

Current status
OPEN_TRANSFERCORE_IDENTITY.

The native transfer_evidence_candidate() emits a candidate payload, not a
project mutation. Even after identity recovery its status is only
CANDIDATE_FOR_ADMISSION and grants_authority stays false; target-side
admission remains independently governed.

## Domain tool handoff

Each selected formal tool uses the normal Take-5 configured invocation path.
Its native result returns to ProjectManager as evidence plus consequences.
Neither a successful native run nor a completed configured invocation is an
admitted project delta. Verify its claimed effect and route any change through
the owning project authority, impact map, regression checks and separately
admitted write path.
