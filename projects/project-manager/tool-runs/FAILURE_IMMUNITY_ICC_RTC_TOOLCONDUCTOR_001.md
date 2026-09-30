# ProjectManager Failure-Immunity Upgrade Campaign 001

Date: 2026-09-30
Controller: ICC / ImprovementCore
Escalation: Raise the Ceiling / RTC
Exhaustive verifier: ToolConductor all-tools campaign
Target: ProjectManager

## Input

Cross-project failure report:
thytabakman-jpg/Take-2/audits/PROJECT_MANAGEMENT_FAILURE_HISTORY_READONLY_2026-09-30.md

## Frozen goal

Upgrade ProjectManager so every currently known project-management failure class is
prevented, detected and blocked, or preserved as explicit OPEN/CONFLICT during managed
execution rather than silently passing as valid closure.

## Governing sequence

ASSERT
-> GOAL
-> MT
-> PD
-> PDAudit
-> MultiObject over {ProjectManager, failure history, project lifecycle}
-> Architecture
-> RootCause
-> RTC / Raise the Ceiling
-> implementation
-> self-management
-> ICC128
-> ToolConductor exhaustive campaign
-> capability preservation
-> repository validation
-> Currentness
-> closure.

## Raise-the-Ceiling result

The strict-gain successor is not “add more lessons.”

The required gain is an executable failure-prevention envelope:

- 17 historical cluster controls;
- 5 root invariants;
- missing/open control -> bounded remediation frontier;
- TARGET_TRANSFORM -> authority + impact map + regression verification;
- nonempty executable frontier -> no project closure;
- explicit bad coordinate state -> no project closure;
- self-instance receives no exemption.

## Promotion criterion

Do not promote on architecture quality alone.

Promotion requires all new regression tests, prior ProjectManager tests, the
93-tool ProjectManager campaign including ICC128 and ToolConductor, capability
preservation, and repository validation to pass on the same head.
