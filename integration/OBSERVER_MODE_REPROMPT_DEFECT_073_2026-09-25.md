# Observer-Mode Reprompt Defect 073

Date: 2026-09-25

Status: REPAIRED IN GLOBAL TOOL CONTRACT / HOST-BINDING RESIDUAL OPEN

## Observed failure

The user explicitly stated that every requested diagnostic/controller tool must run in observer mode because they did not trust the system to preserve observer-only execution automatically.

Needing that reminder is itself a system defect.

## Root cause

Observer mode was mandatory in selected paths, especially the ICC bootstrap, but was not a universal configured-run invariant for every registered tool.

Thus:

ICC bootstrap observer enforcement != global tool observer enforcement.

The user remained an external carrier of the missing invariant.

## Repair

Global Tool Execution Contract 072 makes OBSERVER the mandatory ordinary mode for every registered tool plan.

Non-observer tool-run requests fail closed.

State-changing work is separated from analytical tool invocation and remains governed by transition/admission/commit machinery.

## Residual

Cross-chat or host surfaces that never bind through Take-5 cannot be compelled by repository code alone.

That host-entry binding problem remains OPEN and must not be described as globally solved until the host path demonstrably consumes the global execution profile.

## Observer-only diagnostic sequence used for this repair

1. ICC-128 observer-first scan.
2. Repository search on wrapper, geometry, configured-run, observer-mode, and ICC surfaces.
3. GOAL in observer mode.
4. Root analysis in observer mode.
5. What Is My Problem in observer mode.
6. Root Cause in observer mode.
7. GOAL rerun in observer mode.
8. ICC-123 observer coordination.
9. ICC-118 observer input limited to recovered runtime-authority evidence.
10. ICC-124 observer input limited to lineage ambiguity because its distinct identity remains unsupported.
11. ICC-114 retained as unresolved because no exact role was recovered; no invented control semantics were assigned.

The implementation phase followed only after the observer-only diagnosis stabilized.
