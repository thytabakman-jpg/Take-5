# Take-5 Tool System Project

Status: ORGANIZATIONAL MIGRATION ACTIVE
Date: 2026-09-27

This project applies the project-organization and anti-loss lessons already used
in the Sukkos Question Booklet project to the entire tool/ICC ecosystem.

## Core rule

No single Markdown file owns the whole tool system.

Each load-bearing object has its own package. Within that package each kind of
mutable truth has one owner. External semantic/runtime authorities are pointed to,
not recopied as editable truth.

## Entry order

1. CURRENT_STATE.md
2. PROJECT_CHARTER.md
3. AUTHORITY_REGISTRY.md
4. PACKAGE_CONTRACT.md
5. ANTI_LOSS_CONTRACT.md
6. REGRESSION_CONTRACT.md
7. TOOL_INDEX.md
8. ICC_VARIANT_REGISTRY.md
9. the implicated object package

## Two different 36s

Tool execution/coverage uses Scope x ModeFace = 36.

Semantic directed handoff uses SourceScope x TargetScope = 36.

They are separate mathematical objects and live on separate authority surfaces.

## Non-destructive migration

Existing architecture, runtime, integration, research, legacy, and evidence files
remain where they are. This project adds routing packages and regression guards.
