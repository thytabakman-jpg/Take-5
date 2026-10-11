# Pre-Project Definition Gate

Status: CURRENT / VALIDATED / MERGED
Date: 2026-09-27

## Job

Give ProjectManager a durable state between an interesting idea and an admitted full project.

## Definition object

D0 = <G,C,K,M,R,E,B,A,O>.

G
governing goal.

C
core object or claim.

K
context binding.

M
mechanism.

R
route skeleton.

E
observable evidence.

B
boundaries and inherited protected state.

A
alternatives.

O
typed open questions.

## State machine

IDEA
-> EXPLORATION_OPEN
-> DEFINITION_READY
-> USER_APPROVAL
-> PROMOTION_READY
-> separate admitted project creation.

## Barrier

DEFINITION_READY does not create a project.

The native definition assessor treats an approval reference beginning with USER:
as syntactically valid for PROMOTION_READY. This string-prefix check alone
does not authenticate the person who approved the transition or admit a write.

No tool, controller, automated run, or confidence score grants real USER
authority. The separately governed PROMOTE operation must verify actual user
approval and its current preconditions before creating a project. This document
describes that protected admission boundary; the observer assessment does not
implement the downstream persistence transaction.

## Storage rule

A candidate can live in one compact durable definition artifact.

It does not receive the full project package until promotion.

## ImprovementCore relation

ImprovementCore can research, compare, attack, and refine a candidate.

Its handoff is evidence-only.

ProjectManager reassesses the candidate after material evidence changes.

## Existing-project protection

Exploring a new candidate does not modify an accepted project.

A new candidate and an existing project are separate managed states.


## Validation receipt

Take-5 Validation 36349707998 SUCCESS.
Capability Preservation 36349708034 SUCCESS.
Tool System Every-Tool Sweep 36349708182 SUCCESS.


## Canonical promotion

PR 170 merged as 904f1336b4226b42e51a88630581a2f507ec2304.

Post-merge Every-Tool Sweep 36349806935 SUCCESS.
Post-merge Take-5 Validation 36349806942 SUCCESS.
