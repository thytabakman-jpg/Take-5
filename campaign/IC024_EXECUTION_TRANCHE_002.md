# IC-024 Execution Tranche 002 — Ablation and Zero-Request Evidence

Date: 2026-09-24
Status: MATERIAL EVIDENCE DELTA
Production authority change: none

## Placement ablations F1-F5

The ablation question is whether protected behavior requires the entire historical module to occupy one layer, or whether behavior survives a factorized placement.

### F1 behavioral quotient / preservation x kernel
Protected requirement: replacement must preserve declared behavior.
Ablation: remove quotient computation from kernel while retaining a kernel preservation obligation and an external verification witness.
Result: no identified protected behavior requires the quotient algorithm itself to be a kernel primitive. Kernel needs the invariant/acceptance contract; quotient construction/testing can remain epistemic/verification machinery.
Status: SUPPORTED FACTORIZATION, subject to executable replacement benchmark.

### F2 delegation x kernel/controller
Protected requirement: child authority cannot exceed licensed grant; revocation/return/conflict remain typed.
Ablation: move adaptive selection of A,Gamma,tau out of kernel while retaining grant legality/inheritance constraints.
Result: legal-authority behavior is preserved by kernel contract while adaptive delegation policy remains controller behavior. Runtime authority remains separately bound.
Status: SUPPORTED FACTORIZATION.

### F3 PD distinction generation x epistemic/controller
Protected requirement: discover result-sensitive distinctions without silently manufacturing authority.
Ablation: keep distinction operation epistemic and expose generated candidate work to controller admission rather than making candidate generation itself a kernel transition.
Result: preserves distinction discovery and no-smuggling while separating evidence production from work selection.
Status: SUPPORTED FACTORIZATION; exact PD suboperation minimality remains OPEN.

### F4 dynamics/reentry x kernel/controller/state
Protected requirement: legal updates, durable state, evidence-sensitive reselection and stop.
Ablation: separate transition legality, persistent state, and adaptive reentry policy.
Result: no current evidence requires these to be one primitive/module. Kernel protects admissible transition constraints; state persists; controller reselects/stops.
Status: SUPPORTED FACTORIZATION; convergence theorem remains OPEN.

### F5 map capture x state/controller
Protected requirement: discovered maps are not lost even if rejected/superseded.
Ablation: make capture/lineage monotonic persistent state while leaving connect/attack/adjudicate adaptive.
Result: anti-loss survives without making epistemic acceptance monotonic.
Status: SUPPORTED FACTORIZATION.

## Cross-cut result

The old binary question PD-in-kernel / ICC-above-kernel is too coarse for all five tested boundaries.

Current evidence favors factor placement:
protected invariant | epistemic operation | adaptive policy | executable binding | persistent record | verification witness.

This is not yet a final Take-5 architecture because runtime/holdout preservation remains required.

## Zero-request independent evidence

A prior uncontaminated Take-4 Experiment 010 exists on PR branch zero-request-full-corpus-001, commit 517a94da8e01acc4c20a29413831d2bfa0f4ef08.

The supplied input was corpus only; substantive_job_input=None.

Its corpus-derived frontier was:
1 trace semantic/runtime boundary;
2 recover PD/ICC functional relation;
3 test endogenous work selection;
4 recover unresolved map frontier.

It selected the first discovered job, selected its own generic corpus relation scan, executed non-destructively, verified corpus-derived origin, updated state, and reentered with the remaining frontier.

GitHub Actions run 36026299003 completed successfully and uploaded artifact zero-request-full-corpus-result. This is implementation evidence for endogenous work-frontier construction on that frozen fixture, not evidence of general autonomous stewardship.

Important independent convergence:
without being given the current directed Take-5 execution contract, the zero-request treatment independently surfaced semantic/runtime boundary, PD/ICC relation, endogenous work selection and map anti-loss — all live Take-5 coordinates.

## Execution binding evidence

Take-4 Experiment 004 supplies a small executable witness:
controller selection -> typed authority change -> worker action -> post-state observation -> verification -> state update -> reselection/termination.

GitHub Actions run 36016995011 completed successfully.

This establishes that the architecture pattern is executable in a fixture. It does not establish Take-5 general binding or production runtime authority.

## Current effect on gate

C05 placement evidence advances materially.
C10 zero-request evidence advances to VERIFIED_FOR_FIXTURE, generalization remains OPEN.
C06/C07 have executable fixture evidence but Take-5 binding remains PARTIAL.
C09 remains PARTIAL until global map-register/file reconciliation is rerun after maps 113-121.

## Next automatic work

Build currentness/capability preservation matrix, reconcile map register, compile minimal Take-5 factor architecture from supported placements, then bind an executable Take-5 fixture and return to IC-023.
