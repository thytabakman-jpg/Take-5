# Take-5 Tool System Project

Status: CURRENT NONDESTRUCTIVE TOOL-SYSTEM ORGANIZATION; ongoing reconciliations are explicit
Created: 2026-09-27
Navigation reviewed: 2026-10-12, America/Toronto

This project applies the project-organization and anti-loss lessons already used
in the Sukkos Question Booklet project to the entire tool/ICC ecosystem.

## Core rule

No single Markdown file owns the whole tool system.

Each load-bearing object has its own package. Within that package each kind of
mutable truth has one owner. External semantic/runtime authorities are pointed to,
not recopied as editable truth.

## Entry order

1. [CURRENT_STATE.md](CURRENT_STATE.md)
2. [PROJECT_CHARTER.md](PROJECT_CHARTER.md)
3. [AUTHORITY_REGISTRY.md](AUTHORITY_REGISTRY.md)
4. [PACKAGE_CONTRACT.md](PACKAGE_CONTRACT.md)
5. [ANTI_LOSS_CONTRACT.md](ANTI_LOSS_CONTRACT.md)
6. [REGRESSION_CONTRACT.md](REGRESSION_CONTRACT.md)
7. [TOOL_INDEX.md](TOOL_INDEX.md)
8. [SOURCE_MAP.md](SOURCE_MAP.md) — reconciled cross-repository navigation, not formal or runtime authority
9. [ICC_VARIANT_REGISTRY.md](ICC_VARIANT_REGISTRY.md)
10. the implicated object package

## Two different 36s

Tool execution/coverage uses Scope x ModeFace = 36.

Semantic directed handoff uses SourceScope x TargetScope = 36.

They are separate mathematical objects and live on separate authority surfaces.

## Non-destructive migration

Existing architecture, runtime, integration, research, legacy, and evidence files
remain where they are. This project adds routing packages and regression guards.

## Live identity versus navigation

The [configured-run registry](../../runtime/tool_run_registry.py) owns current Take-5 tool IDs; the [manifest](../../runtime/tool_manifest.py) owns their protected behavior reconstruction, and the [conductor](../../runtime/portable_tool_conductor.py) owns configured orchestration. [TOOL_INDEX.md](TOOL_INDEX.md) and [SOURCE_MAP.md](SOURCE_MAP.md) are derived navigational views.

A Take-5 configured tool and a similarly named Reaserch formal object may legitimately have different classification, semantics or execution readiness. Neither repository silently promotes the other's source. The [source map](SOURCE_MAP.md) retains unresolved correspondences, including RootCause/Diagnosis, rather than merging them.

A change that adds or renames a configured tool must reconcile the index, package, crosswalk, and affected validation before completion. See [change control](CHANGE_CONTROL.md).
