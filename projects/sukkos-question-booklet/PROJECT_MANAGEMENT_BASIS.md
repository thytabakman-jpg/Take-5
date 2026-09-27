# Project Management Basis

Status: CURRENT EXTERNAL-COMPARATOR RECORD
Date checked: 2026-09-27

## Adopted practices

### Deliverable-oriented decomposition

PMI work-breakdown guidance treats a WBS as a deliverable-oriented decomposition of total project scope, with change control after baselining.

Project use:
WBS.md decomposes durable project outputs rather than mixing them into a to-do list.

Reference:
https://www.pmi.org/learning/library/developing-elaborating-work-breakdown-structures-7241

### Change control

PMI configuration-management guidance separates baseline identity from later change and uses explicit controls to track changes to the technical baseline.

Project use:
CHANGE_CONTROL.md requires a typed delta, owner, dependencies, tests, and receipt.

Reference:
https://www.pmi.org/learning/library/configuration-management-help-controlling-changes-7842

### Lessons captured near the event

PMI lessons-learned guidance emphasizes capturing lessons near the learning opportunity and feeding them back into project execution.

Project use:
LESSONS_LEDGER.md is append-only and updated before the implicated workstream closes.

Reference:
https://www.pmi.org/learning/library/lessons-learned-early-often-6746

### Project information, risks, issues, and change

ISO 21502 covers planning and control practices including risks, issues, change control, and project information across delivery approaches.

Project use:
RAID.md, CURRENT_STATE.md, CHANGE_CONTROL.md, and the authority registry provide explicit control surfaces without committing to one rigid delivery method.

Reference:
https://www.iso.org/standard/74947.html

### Single source of truth

A single authoritative knowledge location reduces duplication and conflicting project information.

Project use:
one canonical owner per mutable project object, referenced elsewhere rather than copied as editable truth.

Reference:
https://www.atlassian.com/work-management/knowledge-sharing/documentation/building-a-single-source-of-truth-ssot-for-your-team

## Project-specific synthesis

Stable authority and change control are predictive.
Question discovery, route testing, and visual exploration are iterative.
Only admitted results move into canonical authority.
