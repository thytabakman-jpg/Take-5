# Execution Claim Integrity 117

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE / THINK-BIG REPAIR
Origin:
- Full configured MT audit 004
- ImprovementCore + HF2 observer campaign 115
- ImprovementCore + HF2 command: "Think big, fix this."

## Problem

Take-5 already has validated Protected Transition Integrity for configured-tool execution.

PTI protects:

identity
-> configured dispatch
-> execution
-> result consumption
-> state update
-> reentry
-> user-visible boundary.

The recurring execution-truth failure that remains repository-owned appears outside that
configured path, especially in campaign and Legacy artifacts that can assert that a run
occurred.

A persisted report, a plan, a tool name, or a CI pass cannot by itself establish that the
claimed run crossed the causal runtime path.

## Scope

Execution Claim Integrity governs execution claims made by repository artifacts outside the
configured-tool PTI path.

It does not replace PTI.

Configured tools continue to use PTI.

A verified PTI receipt can be projected into this generic claim surface when another artifact
needs to refer to the configured run.

## Ordered causal coordinates

Let

E =
<
i,
p,
d,
x,
c,
s,
v
>

where:

i = identity evidence.
p = plan evidence.
d = dispatch evidence.
x = execution evidence.
c = consumption evidence.
s = persistence evidence.
v = verification evidence.

Claim levels form the order:

IDENTIFIED
<
PLANNED
<
DISPATCHED
<
EXECUTED
<
CONSUMED
<
PERSISTED
<
VERIFIED.

Let prefix(l) be the coordinates required up to claim level l.

Then:

ECI(r,l)=VERIFIED

iff

for every k in prefix(l),
Evidence_r(k) is nonempty.

Otherwise:

ECI(r,l)=OPEN(Missing_r(l)).

A higher claim cannot be established by a later coordinate while an earlier causal coordinate
is missing.

Examples:

GitHub persistence without execution evidence cannot establish EXECUTED.

A report hash without controller dispatch cannot establish VERIFIED.

## PTI projection

Let P be a VERIFIED ProtectedTransitionReceipt.

The generic consumed-level execution claim is:

Project_PTI(P,q)
=
<
identity = P.canonical_identity,
plan = q,
dispatch = P.configured_dispatch,
execution = P.execution,
consumption = P.result_consumption
>.

PTI remains authoritative for the configured transition.

The projection only prevents downstream artifacts from discarding the already-verified causal
evidence.

## ICC128 Legacy application

Prior rule:

LegacyRunClosed(r)
iff
GitHubReportCommitReceipt(r) exists.

That rule proved persistence but did not prove that the report was causally generated from the
claimed controller run.

New rule:

LegacyRunClosed(r)

iff

ExecutionClaim(r)=VERIFIED

and

GitHubReportCommitReceipt(r) exists.

The causal Legacy path is:

controller runtime invocation
-> run_result
-> report consumption
-> GitHub persistence
-> report verification.

Runtime:

runtime/execution_claim_integrity.py

Legacy integration:

runtime/icc128_legacy_reporting.py

Portable activation:

runtime/icc128_legacy_portable.py

## Host boundary

This repair covers repository-owned execution claims.

It cannot compel an unrelated external host that never invokes Take-5.

Therefore:

UNIVERSAL_HOST_INTERCEPTION
=
EXTERNAL_NOT_OWNED.

That external boundary is preserved, not renamed as a repository backlog.

## HF2 role

The repair was selected after an observer-only ImprovementCore capability was reapplied under an
explicit HF2 campaign composition until the local representation stabilized.

The action pass then reapplies the same ImprovementCore capability under HF2 after implementation
evidence changes.

This validates the campaign composition.

It does not by itself promote HF2 as a universal wrapper for every ImprovementCore invocation.

## Closure target

The repository-owned seam is CLOSED_RELATIVE only when:

1. incomplete execution claims fail closed;
2. a bare persisted Legacy report cannot close a run;
3. an actual controller invocation can generate an attested report;
4. persistence and verification can upgrade that same causal receipt to VERIFIED;
5. portable Legacy activation requires both report sink and execution attestor;
6. existing configured-tool PTI tests remain preserved;
7. Take-5 Validation and Capability Preservation pass.
