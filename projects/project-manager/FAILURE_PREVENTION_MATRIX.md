# ProjectManager Failure Prevention Matrix

Date: 2026-09-30
Status: CANDIDATE / FAILURE-HISTORY-BOUND

## Table of contents

- [Governing rule](#governing-rule)
- [Seventeen failure-control classes](#seventeen-failure-control-classes)
- [Five root invariants](#five-root-invariants)
- [Transform preflight](#transform-preflight)
- [Closure gate](#closure-gate)
- [Raise-the-Ceiling criterion](#raise-the-ceiling-criterion)

Source audit:
thytabakman-jpg/Take-2/audits/PROJECT_MANAGEMENT_FAILURE_HISTORY_READONLY_2026-09-30.md

## Governing rule

A known management failure is not considered prevented merely because a lesson,
document, or protocol exists.

For each failure class k, ProjectManager requires a durable control entry:

Control_k = <status, owner, evidence, tests, reason?>

CURRENT requires one owner, durable evidence, and regression verification.
NOT_APPLICABLE requires one owner, durable evidence, and an explicit reason.
OPEN, BLOCKED, STALE, PENDING, UNKNOWN, UNVERIFIED, invalid, or missing controls
prevent relative project closure.
CONFLICT produces project CONFLICT.

Known failures are therefore converted from historical memory into executable
closure obligations.

## Seventeen failure-control classes

| Control id | Historical cluster | Minimum protected result |
|---|---|---|
| canonical_authority | canonical authority and source of truth | one typed owner; recency never grants authority |
| state_currentness | state, currentness, version, freshness | current state cannot silently use stale/superseded projections |
| project_entry_continuity | resume, handoff, continuity | reentry resolves durable state before substantive continuation |
| goal_scope_object | goal, scope, semantic object | exact project object and governing goal remain typed |
| adaptive_planning | planning, sequencing, replanning | material deltas invalidate stale plans and force reentry |
| ownership_control | responsibility and boundaries | every mutable project object has one canonical owner |
| execution_truth | execution truth | selection/representation/runtime/receipt/admission remain distinct |
| change_propagation | change control and regression | every transform has impact mapping and regression verification |
| closure_verification | closure and validation | local/task closure cannot silently become project/global closure |
| artifact_production | images, PDFs, documents, artifact topology | exact source, output topology, preservation, and acceptance remain controlled |
| research_evidence | sources, evidence, claims | claims remain traceable to exact evidential status |
| information_architecture | discoverability, migration, anti-loss | preserved information remains findable, currentness-typed, and non-authorizing until promoted |
| recursive_audit_stopping | recursive audit and meta-work | bounded audit scope, stopping rule, and state-relative rerouting remain explicit |
| cross_project_transfer | cross-project learning | transfer remains target-authority preserving and dispositioned |
| concurrency_promotion | branches, PRs, concurrent repair | promotion checks current base/precondition and does not strand unique fixes |
| human_orchestration | human scheduler/historian burden | project continuity does not depend on the user manually restoring state or detecting routine regressions |
| known_holdouts | lower-frequency and future known regressions | every known project-specific holdout is explicit or typed NOT_APPLICABLE |

## Five root invariants

1. representation_authority_execution_separated

Represented != authoritative != selected != executable != executed != consumed !=
verified != persisted != recoverable.

2. state_externalized_before_action

No result-sensitive project fact may exist only in chat or implicit reconstruction
when it can alter execution.

3. mandatory_transition_path

Material work follows:

discovery
-> identity/type
-> authority/currentness
-> plan/selection
-> execution
-> verification
-> admission
-> propagation
-> persistence
-> reentry.

4. closure_scope_typed

Task, artifact, page, project, repository, runtime, host, and global closure are
different claim scopes.

5. human_not_final_integration_layer

The user may supply goals, authority, acceptance, or decisions, but normal continuity,
state recovery, propagation, routine verification, and regression detection cannot
depend on the user acting as scheduler, historian, or reconciler.

## Transform preflight

TARGET_TRANSFORM is not READY unless all are present:

- transform operation class;
- explicit authority_ref;
- explicit impact map;
- explicit regression-verification tests;
- precondition fingerprint.

An empty impact map is not an implicit claim of no impact. A caller may record an
explicit no-additional-impact disposition, but it must be represented.

## Closure gate

ProjectManager may emit CLOSED_RELATIVE only when:

- the 21-coordinate project package is structurally valid;
- no authoritative coordinate is OPEN/BLOCKED/STALE/PENDING/UNKNOWN/UNVERIFIED/CONFLICT;
- the 17 failure controls are closed;
- the five root invariants are closed;
- no legal executable work remains;
- no blocked work remains;
- no authority conflict remains;
- no unprocessed transform remains;
- the management spine closes on the same current basis.

## Raise-the-Ceiling criterion

Let PM003 be the prior ProjectManager and PM004 this successor.

PM004 is a strict gain only when:

1. every protected PM003 behavior is preserved;
2. every known failure cluster gains an explicit fail-closed control;
3. malformed or missing controls generate bounded remediation work rather than false closure;
4. transforms without impact/verification evidence fail OPEN;
5. executable work prevents closure;
6. the full ICC128/ToolConductor/all-tools campaign still closes relatively;
7. repository capability-preservation and validation suites pass.

The intended guarantee is not metaphysical impossibility of external failure.
It is stronger and operational:

Within ProjectManager-managed execution, every currently known project-management
failure class must either be prevented, detected and blocked, or remain explicitly
OPEN/CONFLICT. It cannot silently pass as valid project closure.
