# HF Currentness Reentry 019

Date 2026-09-24
Parent MT_ARCH_HF_CURRENTNESS_AUDIT_018
Mode recursive currentness

## Round 4 after implementation

Implemented:
K_PD projection with routing-relevant distinction preservation;
obligation exposure;
behaviorally adequate package selection;
four-quadrant mode selection on HF path;
TRC material-delta reentry;
Currentness Audit obligations/dependents/reverified coordinates.

## Dependency propagation

Affected:
controller routing
HF/reentry
PD admission surface
mode orchestration
currentness closure
readiness.

Unaffected load-bearing bases:
T=<K,S,O,G,M,C,R,U>;
activation bridge stage truth;
C01-C49 program semantics;
authority/evidence separation;
historical CAP compositional witnesses;
zero-request observation principle.

## HF residual

One remaining architectural mismatch is explicit:
capability_router.py still provides direct trigger-tag -> C-program routing.
This can remain as an implementation adapter only if governing HF routing treats its output as a candidate package index rather than semantic truth.

Disposition PATCH_IN_PLACE, not rebuild.

Current controller also has two loops:
old run_episode activation loop;
new hf_controller governing decision/reentry loop.
They are compatible but not yet physically composed into one function.
Disposition PATCH_IN_PLACE.

Readiness 016 remains prior-basis evidence until composition and full regression pass.

HF continues because material residual remains.
