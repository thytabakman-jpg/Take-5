# ImprovementCore ProjectManager Mandatory Spine 001

Date: 2026-09-27
Status: CURRENT / VALIDATED / MERGED

## Problem

ProjectManager had strong state control but normal invocation did not guarantee that the
governing goal and core structural distinctions were freshly recovered every time.

## ImprovementCore disposition

Think-big repair:

do not add another controller.
Make a management spine part of ProjectManager's ordinary execution identity.

Mandatory spine:

ASSERT
-> GOAL_PRE
-> MT
-> PD
-> PDAudit
-> GOAL_POST
-> CurrentnessAudit
-> QuestionWorthAsking.

Each factor uses the current full configured wrapper and HF002.

Keep MultiObject, Architecture, RootCause, Diagnosis, RTC, and the exhaustive all-tools
campaign adaptive rather than mandatory.

## Why this is the larger repair

The project manager now checks:

what is true,
what goal governs,
what structure is present,
which distinctions change results,
whether the discrimination survives audit,
whether the goal changed after discovery,
whether the basis is current,
and which live question is worth asking.

Only then does native project-state assessment return.

## Current project application

The Sukkos structured-gap candidate remains EXPLORATION_OPEN.

The next dependency frontier is FORMALIZE_STRUCTURED_GAP:
resolve the definition and mathematics of a structured gap before testing the Sukkos analogy,
Jewish conceptual operation, or page route.


## Validation closure

PR 173 merged as 225d4edb956bb29de3e3eb0433f0c9ada84feb11.

PR validation:
Capability Preservation 36350713599 SUCCESS.
Every-Tool Sweep 36350713637 SUCCESS.
Take-5 Validation 36350713639 SUCCESS.

Post-merge:
Every-Tool Sweep 36350803983 SUCCESS.
Take-5 Validation 36350803988 SUCCESS.

## Historical receipt and live-consumer boundary (Level 2, 2026-10-10)

PR 173 merged the eight-stage ordinary-run spine as
`225d4edb956bb29de3e3eb0433f0c9ada84feb11`. The initial
Sukkos structured-gap `EXPLORATION_OPEN` observation and the original
CI run IDs above describe that specific historical check; they do not
claim an up-to-date Sukkos state or automatically grant project authority.

The present stage order and configured identities resolve from
`runtime/project_manager_management_spine.py`, `runtime/tool_run_registry.py`,
`runtime/tool_manifest.py` and their regression tests. This receipt remains
execution/provenance evidence only. Exact failure-immunity campaign coverage
is a later, separate V50 question; this original PR 173 pass alone cannot
close it or certify the current repository head.
