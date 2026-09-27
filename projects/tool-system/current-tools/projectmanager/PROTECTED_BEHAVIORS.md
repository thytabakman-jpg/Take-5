# Protected behaviors: ProjectManager

Current protected behavior is owned by runtime/tool_manifest.py and its cited
implementation/witness surfaces for current configured tools.

Historical variants retain their protected-behavior evidence through SOURCE_MAP.md
without promotion into the live manifest.

## Rule

This page routes authority. It does not duplicate editable protected behavior.


## Current ProjectManager-specific admission protection

The live manifest includes:

PROJECTMANAGER_PREPROJECT_ADMISSION_GATE

This protects the result-sensitive distinctions:

IDEA != PROJECT
DEFINITION_READY != HUMAN_APPROVED
EVIDENCE_ONLY != TARGET_TRANSFORM
CANDIDATE_STATE != FULL_PROJECT_STATE
EXPLORATION_PERSISTENCE != PROJECT_PROMOTION

Authoritative implementation and witness remain owned by runtime/tool_manifest.py and its cited files.


## Mandatory management protection

Candidate live manifest adds:

PROJECTMANAGER_MANDATORY_MANAGEMENT_SPINE

It requires every normal ProjectManager assessment to be preceded by full configured
ASSERT, GOAL_PRE, MT, PD, PDAudit, GOAL_POST, CurrentnessAudit, and QuestionWorthAsking execution.
