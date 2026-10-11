# Interfaces

Status: CURRENT

ProjectManager -> project authority files
Read current truth, route bounded deltas, never overwrite unrelated owners.

ProjectManager -> configured tools
Select or hand off bounded work. Tool output returns as evidence.

ProjectManager -> ImprovementCore
Emit project fingerprint plus executable evidence-only work frontier.
ImprovementCore does not acquire project authority from the handoff.

ImprovementCore -> ProjectManager
Return result, evidence, and consequence metadata.
ProjectManager routes any proposed project-state change through the owning authority.

ProjectManager -> TransferCore
Evidence candidate only while TransferCore full identity is OPEN.
No target mutation and no authority grant.

ProjectManager -> Git or repository
State-changing writes remain under repository change governance and validation.


ProjectManager -> ProjectDefinitionCandidate
Assess the compact nine-coordinate definition object before any full project package exists.

ProjectDefinitionCandidate -> ImprovementCore
Send blocking opens and research work as evidence-only. ImprovementCore gains no promotion authority.

ProjectDefinitionCandidate -> ManagedProject
A separate PROMOTE transition is available only after DEFINITION_READY plus explicit USER approval.
The native USER:-prefixed approval field is a syntactic readiness guard; a separate
owner-side operation must establish real authority and recheck the state fingerprint
before writing a ManagedProject. PROMOTION_READY alone grants no mutation.

ProjectManager -> known-failure integrity consumer
runtime/project_manager_integrity.py checks the 17 control classes and five root
invariants; an OPEN/CONFLICT assessment contributes bounded remediation work or
blocks relative closure. No integrity receipt automatically admits a project delta.

ProjectManager -> full-campaign verification
The development every-tool sweep is valuable route and regression evidence, but
it may use synthetic or fixture-level semantic witnesses. Exact full semantic
ICC128/RTC/ToolConductor coverage is an independently typed verification claim,
currently tracked as VERIFICATION.md V50 / OPEN_QUESTIONS.md Q5.
