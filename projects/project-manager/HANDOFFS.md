# Handoffs

Status: CURRENT

## ImprovementCore handoff

Payload
project_id
project_fingerprint
executable work frontier
effect_class = EVIDENCE_ONLY
authority = NONE

Returned ImprovementCore outputs re-enter as evidence and do not bypass project authority.

## Transfer handoff

Payload
project_id
project_fingerprint
reusable evidence or lesson candidate
transfercore_identity_status
effect_class = EVIDENCE_ONLY
grants_authority = false

Current status
TRANSFERCORE_CURRENT_CANDIDATE_UNDER_VALIDATION.

ProjectManager emits non-authoritative transfer evidence.
TransferCore determines the typed source-target relation.
Target mutation still requires a unique target authority binding and separate explicit authorization.

## Domain tool handoff

Each selected formal tool uses the normal Take-5 configured invocation path.
Its native result returns to ProjectManager as evidence plus consequences.
