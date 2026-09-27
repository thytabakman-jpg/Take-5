# Tool System Stakeholders

Status: CURRENT

## Roles

| Stakeholder role | Interest | Authority |
|---|---|---|
| User / project owner | preserved functionality, low-loss continuity, correct organization | authorizes project-level changes and priorities |
| ICC / ImprovementCore | discovery, routing, repair, reentry | evidence-producing controller; no independent authority to rewrite canonical truth |
| ProjectManager | coherent project-control state and bounded change routing | observer/control assessment; mutation requires owning authority |
| Tool owners / canonical files | exact mathematics, runtime, protected behavior, lineage | own their declared mutable objects |
| Validation system | regression and capability-preservation evidence | verification only |
| Historical provenance | recovery evidence for earlier objects | evidence only; recency does not create current authority |

## Rule

Stakeholder interest does not imply mutation authority. Authority remains
object-specific and is routed by AUTHORITY_REGISTRY.md.
