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
Emit typed non-authoritative transfer evidence into the current TransferCore relation pipeline.
Transfer admission grants no target state-change authority; target authority binding and explicit authorization remain separate.

ProjectManager -> Git or repository
State-changing writes remain under repository change governance and validation.


ProjectManager -> ProjectDefinitionCandidate
Assess the compact nine-coordinate definition object before any full project package exists.

ProjectDefinitionCandidate -> ImprovementCore
Send blocking opens and research work as evidence-only. ImprovementCore gains no promotion authority.

ProjectDefinitionCandidate -> ManagedProject
A separate PROMOTE transition is available only after DEFINITION_READY plus explicit USER approval.
