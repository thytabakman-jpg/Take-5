# Canonical Tool Identity Repair 076

Date: 2026-09-26
Status: IMPLEMENTED ON BRANCH / VALIDATION REQUIRED
Branch: ic-tool-identity-repair-20260926

## Failure witness

MT's black-box semantic-return behavior remained implemented and tested but was
not structurally recoverable from the generic configured-run identity.

This allowed a later reconstruction to preserve MT's name and generic wrapper
coordinates while omitting a protected intra-tool behavior.

## Root class

DISTRIBUTED_IDENTITY_WITHOUT_RECONSTRUCTION_CLOSURE

A protected behavior existing somewhere in the repository is not preservation.

Preservation requires:

CanonicalIdentity(T)
-> Recover(T)
-> ProtectedWitnessVerification(T)

## Repair

A canonical per-tool manifest now records protected behavior bindings by phase:

- PRE
- INTRA
- POST
- CROSS

The manifest references implementation and witness surfaces rather than copying
their semantics.

ConfiguredRunSpec now carries:

- manifest_id
- protected_behaviors

and its completeness check requires the canonical manifest to reconstruct every
listed protected behavior.

## MT binding

MT now declares:

MT_BLACK_BOX_SEMANTIC_RETURN_GATE

and binds it to:

- runtime/mt_semantic_return_gate.py
- tests/test_mt_semantic_return_gate.py

The behavior is typed as INTRA.

A configured MT that loses this binding fails its completeness check.

## General law

For every configured tool T:

Protected(T) <= Recover(CanonicalManifest(T))

Missing protected reconstruction fails closed.

## Current scope

The mechanism is general and all registered tools receive the common configured
wrapper/closure/reentry/OPEN bindings.

Only MT's newly demonstrated tool-specific protected binding has been explicitly
backfilled in this repair.

Other tools still require a portfolio backfill of tool-specific protected
behaviors from historical lineage and witness evidence.

## OPEN

- full tool-specific manifest backfill for ASSERT, GOAL, PD/PDAudit, HF001,
  GDOS, ImprovementCore, and other historical major tools;
- automated artifact-path existence verification;
- historical witness reconciliation before claiming portfolio completeness;
- validation workflow result for this branch.
