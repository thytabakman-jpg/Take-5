# Whole Job Stability Closure 171

Date: 2026-09-27
Status: REPAIR CANDIDATE
Scope: HF1, HF2, ImprovementCore parent completion

## Failure

The recurring observed pattern was:

tool run
-> local closure
-> user asks for another MT/overview
-> new material distinction appears
-> another apparent closure
-> another rerun finds more.

The defect is not that HF2 failed its stated current job.

HF2 currently owns same-capability local recurrence.

The defect is that local recurrence and the parent return gate could consume an
already-incomplete question/work frontier and then accept local stability without
an executable proof that a fresh whole-job observation would regenerate no new
material work.

## Recovered historical HF1 behavior

Historical HF1 included:

Generate
-> Admit
-> TypeDelta{RESULT,SEARCH,NONE,OPEN}
-> Update
-> select fairly over live continuation classes
-> retain failure/subsumption memory
-> reenter while live frontier remains
-> evaluate relative closure.

The current Take-5 HF1 runtime had compressed this boundary.

It accepted caller-constructed obligations and contained the direct law:

no obligations -> RELATIVE_CLOSE.

World/discovery/result-sensitive signatures were constructed upstream.

Therefore an incomplete upstream discovery state could be treated as closed.

## Correct division of labor

HF2

same-capability local recurrence.

HF1

fresh continuation-state regeneration/observation, invalidation classification,
earliest reentry, and basis-relative episode closure.

ImprovementCore parent

global question/work/capability selection, admission, replanning and terminality.

TRC

tool-run consequence closure.

These jobs are complementary.

## Stronger closure law

Let FRESH_J,K(x) be a whole-job observation that rebuilds the continuation-relevant
question/work frontier from normalized current state rather than inheriting the
prior local selection trace.

Define material challenge delta:

DeltaFresh
=
DeltaResult
union DeltaSearch
union DeltaDiscovery
union DeltaRepresentation
union DeltaAuthority
union DeltaExecution
union DeltaQuestion
union DeltaRelation
union DeltaCapability
union DeltaReachableWork.

Local HF2 closure is necessary but insufficient.

HF1 relative closure requires:

TRC closed
and current obligations empty
and FRESH_J,K produces no typed material delta
and a changed fresh basis is reentered rather than returned.

ImprovementCore COMPLETE additionally requires repeated fresh stability:

FreshStable_2(x)
iff
two consecutive fresh whole-job observations from reset ephemeral challenge
contexts produce no material delta and no owned executable work.

Then:

ParentComplete
iff
HF2RelativeClose
and HF1FreshRelativeClose
and FreshStable_2
and GoalClosed
and not OwnedWorkRemaining
and ConsequenceClosed
and required authority/currentness receipts are closed.

## Why two passes

A single fresh pass can itself change the discovery basis.

The first no-gain pass is not sufficient evidence that a second newly generated
overview will also find nothing.

Two consecutive no-delta passes are a bounded executable idempotence witness.

This is basis-relative, not a theorem of globally complete discovery.

## Parent reentry memory continuity

Fresh whole-job challenges can emit persistent memory patches in addition to state
patches.  A material fresh challenge that forces parent CONTINUE must carry that
memory into the next parent round.  Otherwise the next fresh re-observation can
forget discoveries, suppressions, failure/subsumption memory, or prior challenge
evidence that the closure contract explicitly treats as persistent.

Therefore parent reentry transports both:

state_(t+1) = outcome.next_state

and

memory_(t+1) = outcome.next_memory.

Resetting ephemeral challenge context does not reset persistent parent-return
memory.

## Fail closed

Missing fresh re-observer:

OPEN(FRESH_WHOLE_JOB_REOBSERVATION_REQUIRED).

Fresh material delta:

CONTINUE parent; rerun complete ImprovementCore+HF2.

Changed fresh state without a typed material delta:

OPEN(FRESH_REOBSERVATION_UNTYPED_STATE_DELTA).

A fresh observer may not smuggle a new question, frontier, authority, execution
fact, or other state change through a nominal NO_GAIN/STABLE result without
typing the change on the material-delta surface.

Missing fresh status:

OPEN(FRESH_REOBSERVATION_STATUS_REQUIRED).

A closure candidate must explicitly attest owned-work state.  Missing
owned_work_remaining cannot be interpreted as false:

OPEN(FRESH_REOBSERVATION_OWNED_WORK_ATTESTATION_REQUIRED).

This keeps absence-of-data from becoming closure evidence.

Fresh OPEN/BLOCKED/CONFLICT:

preserve the typed noncomplete boundary.

Resource exhaustion:

OPEN, never semantic completion.

## Runtime

HF1:
runtime/hf1_episode.py

Parent stability challenge:
runtime/whole_job_stability.py

Parent return:
runtime/improvement_core_return_gate.py

User-facing ImprovementCore:
runtime/improvement_core_hf2_default.py

Restored semantic path:
runtime/improvement_core_legacy_restored.py
runtime/improvement_core_restored_dispatch.py

## Nonclaim

No finite system can prove that an unknown external representation or unavailable
evidence source contains no future discovery.

The repaired claim is stronger and exact:

relative to the declared current basis and active semantic provider, a COMPLETE
return has survived fresh whole-job regeneration to a repeated no-delta fixed
point rather than merely stopping at a local HF2 fixed point.
