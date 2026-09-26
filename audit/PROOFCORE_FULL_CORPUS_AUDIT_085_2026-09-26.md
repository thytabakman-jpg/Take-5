# ProofCore Run 085 — Full Corpus Audit

Date: 2026-09-26
Status: EXECUTED / FAIL-CLOSED / REENTRY REQUIRED
Target: ImproveCore full-corpus audit campaign
Basis: five-repository frozen audit boundary plus current repository state

## Frozen claim set

C1. The frozen repository trees were completely enumerated.
C2. Every frozen-tree file received a path-level placement record.
C3. Every Markdown document was semantically inspected.
C4. Every line of relevant code was inspected for hidden discoveries/math.
C5. Every historical audit has been reconciled into the correct current destination.
C6. Every orphan candidate has an explicit semantic disposition.
C7. Material strict gains are prevented from disappearing.
C8. The campaign did not silently overwrite concurrent ImproveCore work.
C9. The branch artifacts are current relative to their source repositories.
C10. The user's requested full complete audit is complete.

## Proof rule

For protected claim c,

Proof(c)=PASS

only when the canonical evidence reconstructs the claim and its load-bearing dependencies.

Missing execution evidence, stale basis, unresolved candidate disposition, or unexecuted verifier yields OPEN/BLOCKED/FAIL rather than inferred success.

Tool-level governing invariant:

Protected(T) subseteq Recover(CanonicalToolIdentity(T)).

Campaign-level analogue:

RequiredOutcome(A) subseteq ProvenEvidence(A).

## Proof matrix

### C1 frozen tree enumeration
PASS.

Evidence:
recursive Git trees were enumerated for Take-2, Take-3, Take-4, Take-5, and Reaserch with truncated=false at the frozen boundary.

### C2 path-level placement record
PASS relative to the frozen boundary.

Evidence:
branch-local FULL_CORPUS_PLACEMENT_MANIFEST records enumerate every frozen-tree blob.

Qualification:
placement class is a routing hypothesis, not semantic authority.

### C3 every Markdown document semantically inspected
FAIL / NOT EXECUTED.

The installed full-corpus content auditor is designed to inspect text content line-by-line, but the GitHub workflow did not execute during the campaign.
A path manifest cannot prove semantic inspection.

### C4 every relevant code line inspected for hidden discoveries/math
FAIL / NOT EXECUTED.

Same reason as C3.
File enumeration plus heuristic path classification is not line-complete code inspection.

### C5 every historical audit reconciled into the correct current destination
FAIL / OPEN.

The campaign established the routing law and detected material reconciliation candidates, but did not produce a semantic disposition for every historical audit.

### C6 every orphan candidate explicitly dispositioned
FAIL / OPEN.

Reaserch had 41 path-level UNRESOLVED_PLACEMENT candidates at the frozen branch boundary.
Those files remain a queue, not a completed disposition set.
Content-derived orphan candidates have not yet been generated because the line-complete auditor did not execute.

### C7 strict gains protected from disappearance
PARTIAL PASS.

Evidence:
- manifests make the frozen corpus addressable;
- unresolved placement is fail-closed;
- recent full-tool math and HF1/HF2 work were explicitly identified as reconciliation candidates;
- deletion is not an audit disposition.

Failure boundary:
protection from disappearance is stronger than integration.
Some candidates remain outside canonical Take-5 current control.

### C8 no silent overwrite of concurrent ImproveCore work
PASS.

Evidence:
separate audit branches and draft PRs were created for all five repositories.

### C9 audit artifacts current relative to source repositories
FAIL for global claim.

Take-2, Take-3, Take-4, and Take-5 audit bases were current when checked.

Reaserch advanced after the audit branch was cut.
The current Reaserch main tip added HF-002 universal formal-tool wrapper integration.
Therefore the Reaserch audit branch is stale relative to main and its affected dependency cone must be reopened.

### C10 requested full complete audit is complete
FAIL.

C3, C4, C5, C6, and C9 fail or remain OPEN.
Therefore a completion claim is not licensed.

## New material delta discovered by ProofCore

Reaserch main now contains a new HF-002 universal-wrapper contract after the audit branch base.

Material consequence:
the full-tool wrapper/currentness surface changed during the audit.

Therefore:
old audit basis
-> new material delta
-> invalidate affected currentness claims
-> reconcile HF-002 wrapper integration
-> rerun content/placement checks over affected cone.

This is direct evidence that the campaign's reentry law is load-bearing.

## ProofCore verdict

FULL_CORPUS_PATH_COVERAGE = PASS relative to frozen trees.

FULL_CORPUS_SEMANTIC_AUDIT = FAIL / NOT YET PROVEN.

FULL_INFORMATION_PLACEMENT = FAIL / OPEN.

CONCURRENCY_ISOLATION = PASS.

GLOBAL_CURRENTNESS = FAIL because Reaserch changed after branch freeze.

USER_REQUESTED_COMPLETE_AUDIT = FAIL-CLOSED.

## Earliest unmet dependency

The earliest unmet dependency is not more folder reorganization.

It is:

1. reconcile the audit branch with new Reaserch material;
2. execute the line-complete content auditor;
3. disposition every generated orphan/broken-link/duplicate/currentness candidate;
4. route verified strict gains;
5. rerun ProofCore on the updated corpus boundary.

Only then can completion be reconsidered.

## Status color

ProofCore itself is mathematically recovered for this job through the current invariant and full-tool identity contract.

The audited campaign is not closed.
