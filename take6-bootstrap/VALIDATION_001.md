# Take-6 Bootstrap Validation 001

Date: 2026-09-26
Status: PROTOTYPE CORE PASS / PRODUCTION PROMOTION OPEN

## Validation run

The bootstrap runtime was reconstructed in an isolated local test directory and executed without relying on Take-5 runtime imports.

Result:

14 passed.

Validated behaviors:

1. byte content addressing is stable;
2. currentness is compiled from supersession rather than recency;
3. incomparable admitted maxima compile to CONFLICT;
4. unauthorized state-changing events fail closed;
5. tampered event identities fail closed;
6. missing parent events fail closed;
7. deleting generated compiled state and rebuilding produces the same state CID;
8. historical object deletion is detected by checkpoint verification;
9. affected dependency cones require a disposition for every member;
10. silent protected-behavior loss blocks promotion;
11. typed OPEN behavior does not become a false PASS;
12. tampered invocation capsules fail closed;
13. two replicas in one failure domain do not satisfy durability;
14. two verified independent trust domains satisfy the durability predicate.

## What this proves

It proves the bootstrap primitives implement the declared local invariants on the tested fixtures.

## What this does not prove

It does not establish:
- production authority;
- full predecessor corpus migration;
- all-tool behavioral equivalence;
- external host interception;
- independent cold-replica provisioning;
- full archive disaster recovery on real data;
- Take-6 repository creation.

Those remain promotion obligations.
