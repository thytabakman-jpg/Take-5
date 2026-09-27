# Dependency Graph

Status: CURRENT
Date: 2026-09-27

## Core graph

PROJECT_CHARTER
→ GOAL
→ LEARNER_MODEL

QUESTION_MODEL
→ LEARNER_MODEL
→ ROUTE_LOCK

IS_OUGHT_BOUNDARY
→ JEWISH_OPERATION

JEWISH_OPERATION
+ SOURCE_LOCK
→ PAGE_2

QUESTION_MODEL
+ SOURCE_LOCK
+ SUKKOS_EMBODIMENT
→ PAGE_3

PAGE_1
+ PAGE_2
+ PAGE_3
→ PAGE_4

PAGE_1
+ PAGE_2
+ PAGE_3
+ PAGE_4
→ FOUR_PAGE_ARCHITECTURE
→ STUDENT_SPEC

STUDENT_SPEC
+ ACTIVITY_MODEL
+ SOURCE_LOCK
→ EXACT_COPY

FOUR_PAGE_ARCHITECTURE
+ STUDENT_SPEC
+ EXACT_COPY
→ VISUAL_MASTER

EXACT_COPY
+ VISUAL_MASTER
+ ACTIVITY_MODEL
+ SOURCE_LOCK
→ ARTIFACT_SPEC

ARTIFACT_SPEC
→ RENDER
→ PAGE_QA
→ SET_QA
→ CLASSROOM_VALIDATION
→ RELEASE

## Control graph

ASSERT_BASELINE
+ GOAL
+ CURRENT_STATE
→ CONTROLLER

Any admitted material delta
→ CHANGE_CONTROL
→ owning authority
→ dependency descendants
→ ACCEPTANCE_GATES
→ CURRENT_STATE

Any failure
→ LESSONS_LEDGER
→ controller learning state.

## Reentry rules

A change to GOAL reopens every downstream object.

A change to QUESTION_MODEL reopens learner model, route lock, Pages 1 through 4, student spec, copy, visual master, artifact spec, and acceptance.

A change to SOURCE_LOCK reopens the page and application using that source, then downstream copy and artifact state.

A change to SUKKOS_EMBODIMENT reopens Page 3, Page 4 handoff, route lock, copy, visual master, and artifact spec.

A pure spelling correction in locked copy reopens render QA but not the learner model.

A purely decorative visual correction reopens visual and render QA but not copy or source state.

No dependency descendant is silently edited.
