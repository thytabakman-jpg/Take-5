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

The current live manifest includes (merged PR 173):

PROJECTMANAGER_MANDATORY_MANAGEMENT_SPINE

It requires every normal ProjectManager assessment to be preceded by full configured
ASSERT, GOAL_PRE, MT, PD, PDAudit, GOAL_POST, CurrentnessAudit, and QuestionWorthAsking execution.


## Failure-immunity protection

The current live manifest includes (merged PR 187):

- PROJECTMANAGER_FAILURE_PREVENTION_ENVELOPE
- PROJECTMANAGER_TRANSFORM_IMPACT_VERIFICATION_GATE
- PROJECTMANAGER_NO_FALSE_CLOSE_WITH_FRONTIER
- PROJECTMANAGER_HISTORICAL_FAILURE_HOLDOUT_GATE

These protections bind the cross-project failure history to executable
ProjectManager closure semantics rather than leaving it as a lessons-only artifact.
The runtime/manifest own the live behavior; this package records only its routing.
PR 187 merged as `caadd8d8a41904bec9e0e0b0507af476969aade0`.
For the exact validation and historic candidate lineage see `SOURCE_MAP.md`.
