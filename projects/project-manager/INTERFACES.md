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
