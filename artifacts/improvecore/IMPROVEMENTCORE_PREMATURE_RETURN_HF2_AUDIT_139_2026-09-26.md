# Local HF2 Closure Was Mistaken for Permission to Return Before the Parent Job Ended

<a id="improvementcore-premature-return-and-hf2-audit-139"></a>
**Historical report title:** ImprovementCore Premature Return and HF2 Audit 139  
**Document type:** Dated Root Cause implementation audit; historical branch-level claims, not proof of present host-wide behavior  
**Audience:** ImprovementCore parent-controller, HF2, and runtime-gate maintainers  
**Goal:** Expose the parent-return gating defect, its recorded implementation, and the distinction between local closure and governing job completion  
**Source status:** Dated original; historical evidence, claimed repairs and unresolved boundaries retained without asserting current operational authority.  

## Principal finding and evidential limits

The diagnosed mechanism was a **missing independent parent-return gate**. The report states that semantic-provider COMPLETE and HF2 relative close could terminate a user-visible interaction while parent-owned work remained. It records an added `ParentReturnGate` and caller integration **on the inspected branch**; this Level 1 edit does **not** revalidate the runtime or host-wide effect.

## Contents

- [User-reported failure](#user-reported-failure)
- [Evidence audit](#evidence-audit)
- [HF2 audit](#hf2-audit)
- [Live code defect found](#live-code-defect-found)
- [Systemic repair](#systemic-repair)
- [New invariant](#new-invariant)
- [Expected behavioral consequence](#expected-behavioral-consequence)


Date: 2026-09-26
Status: ROOT DEFECT IDENTIFIED / SYSTEMIC REPAIR IMPLEMENTED ON BRANCH

## User-reported failure

The user observed that ImprovementCore sometimes returns after making one meaningful step instead of completing the whole requested job.

The requested correction is not "do more steps by default." It is:

do not expose a user-visible return while executable owned work remains.

## Evidence audit

Historical conversation and repository evidence show the same pattern repeatedly.

1. A material pass completes.
2. HF2 or another local closure mechanism reaches a relative fixed point.
3. The assistant returns.
4. The user invokes ImprovementCore again.
5. The new pass discovers another material residual.
6. The user has therefore become the outer scheduler.

Earlier repairs solved pieces of this:
- HF1 upstream invalidation;
- HF2 same-capability recurrence;
- recursive parent/child management;
- strict-progress admission;
- no-gain memory;
- Legacy no-premature-stopping behavior;
- result-sensitive reselection.

The remaining gap was the final parent user-return boundary.

## HF2 audit

Correct uses of HF2:

- reapply the same complete capability after a material local delta;
- keep recurring while the local frontier remains live;
- stop on relative local closure;
- return upstream on HF1 invalidation.

Incorrect expectation previously placed on HF2:

- prove the whole governing problem is complete.

HF2 cannot establish that by itself because local recurrence and global parent completion are different relations.

The repair therefore does not make HF2 recursively call itself forever.

Instead:

HF2[ImprovementCore]
-> ParentReturnGate
-> CONTINUE => HF2[ImprovementCore] again.

This preserves the correct separation of responsibilities.

## Live code defect found

Legacy-restored ImprovementCore accepted terminal COMPLETE from the semantic provider and its outer HF2 local-close predicate could then return RELATIVE_CLOSE without an independent whole-job closure certificate.

The fixed-stage default similarly had HF2 local saturation but no independent parent return permission layer.

## Systemic repair

Added:
runtime/improvement_core_return_gate.py

Integrated into:
- runtime/improvement_core_hf2_default.py
- runtime/improvement_core_dispatch.py
- runtime/improvement_core_legacy_restored.py
- runtime/improvement_core_restored_dispatch.py

Migrated campaign/test callers so ordinary execution cannot silently bypass the gate.

## New invariant

UserVisibleReturn
=> ParentReturnReceipt.

ParentReturnReceipt(RETURN, COMPLETE)
=> GoalClosed
and not OwnedWorkRemaining
and ConsequenceClosed
and EvidenceBound
and HF2LocalSaturated.

ParentReturnReceipt(CONTINUE)
=> no user return
and full parent reentry.

## Expected behavioral consequence

A single meaningful repair can be reported internally and persisted, but it does not end the conversation task.

ImprovementCore continues until:
- the governing job is complete;
- or no repository-owned executable work remains and the residual is typed OPEN/BLOCKED/CONFLICT.

That is the intended replacement for user-driven repeated "run ImprovementCore again" scheduling.
