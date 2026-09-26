# Take-6 Boot Sequence

A fresh checkout must be recoverable without chat history.

## Boot

1. Verify the bootstrap manifest and kernel CID.
2. Verify every schema CID.
3. Verify vault object hashes.
4. Verify event object hashes.
5. Compile semantic state from immutable events.
6. Reject ambiguous currentness as CONFLICT.
7. Materialize generated indexes and human views.
8. Resolve the requested controller/tool by exact compiled identity.
9. Build an invocation capsule from exact CIDs.
10. Verify all dependency and environment CIDs.
11. Execute.
12. Record execution and verification receipts as immutable evidence.
13. Append semantic events licensed by those receipts.
14. Recompile.
15. Reenter the controller on the changed state.

## Recovery test

Delete:
- compiled/
- views/
- runtime caches

Keep:
- vault/
- ledger/
- schemas/
- compiler source

A valid Take-6 checkout reconstructs the same compiled state CID.

This is the primary anti-compression recovery witness.

## Disaster test

Start with only:
- immutable source archive
- immutable event ledger
- schemas
- compiler version

Reconstruct:
- semantic object graph
- currentness
- tool identity
- protected behavior inventory
- OPEN/BLOCKED/CONFLICT state
- migration provenance

Failure to reconstruct any protected current object blocks promotion.
