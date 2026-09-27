# Tool Operational Identity Contract 172

Date: 2026-09-27
Status: CANDIDATE REPAIR / CURRENT-REPERTOIRE EXHAUSTIVE TARGET

## Problem

The system had strong FullMath, wrapper, geometry, protected-behavior and runtime
contracts, but several design dimensions repeatedly used in actual tool work were
not enforced as one exhaustive current inventory.

Most importantly:

tool name != question != job != responsibility != mathematical object.

A tool can retain its runtime while losing part of its job through compression.
HF1 exposed this failure directly.

## Required operational nucleus

For every current configured tool T define:

Nucleus(T)
=
<Question_T, Job_T, Responsibility_T, Species_T>.

Question_T is the result-sensitive question/probe family the tool exists to answer.

Job_T is the transformation/analysis/control operation it performs.

Responsibility_T states the state/decision boundary it owns and the authority it
explicitly does not own.

Species_T identifies the mathematical object/operator class.

These are distinct coordinates.  No one coordinate is reconstructed merely from
the tool name.

## Full enforced projection

The operational nucleus is joined with the existing FullMath/configured identity:

IdentityProjection(T)
=
<
Question,
Job,
Responsibility,
MathematicalObject,
NativeSemantics,
Wrapper,
Geometry,
ProtectedBehavior,
Closure,
Reentry,
Recurrence,
LineageCurrentnessRuntime
>.

Canonical runtime audit:

runtime/tool_identity_dimensions.py

The audit must have exact set parity with runtime/tool_run_registry.py::MATERIAL_TOOLS.

Missing or empty coordinates make the repertoire OPEN.

## Source rules

C01-C49 project Question/Job/Responsibility from the already-authoritative
ProgramSpec job and protected outputs.

Learning tools project from their typed LearningToolSpec obligation and
input/output contract.

Named tools use explicit operational nuclei.  These projections do not replace
their native/full mathematical authority.

## HF1/HF2 distinction

HF1 question:
after verified work and fresh re-observation, has the governing continuation
basis changed, and where must execution reenter?

HF1 responsibility:
episode-level continuation invalidation, fresh-closure challenge and reentry.

HF2 question:
after one capability changes local normalized state, does that same capability
have live local material work?

HF2 responsibility:
same-capability local recurrence only.

Therefore:

HF2 local fixed point != HF1 whole-job/fresh-observation closure.

## Regression law

A new tool cannot enter the current registered repertoire without a complete
operational nucleus and full projection.

A future compression that deletes Question, Job, Responsibility or Species is a
regression even when runtime tests still execute.
