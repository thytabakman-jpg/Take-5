# Reaserch Post-Migration Drift

Date: 2026-09-25
Status: OPEN RECONCILIATION RECORD

## Authority baseline

`MIGRATION_STATE.yaml` records Take-5 as CANONICAL_WORKING and names Reaserch as preserved read-only rollback/provenance state.

## Observed defect

Reaserch continued receiving commits after the migration.

Therefore:

```
newer_in_Reaserch != canonical
```

and

```
post_cutover_Reaserch_change
-> candidate evidence
-> explicit transfer/admission
-> Take-5
```

## Material drift already observed

The September 25 Reaserch stream includes new object-recovery work around:

- pre-math object hypothesis recovery;
- Observer entry when object identity is unresolved;
- MathPacket integration;
- HCC solver integration;
- conversation/event receipts for that discovery.

This material is not silently promoted here because its exact overlap with current Take-5 kernel/alignment work requires a typed comparison.

## Reconciliation contract

For each post-cutover Reaserch object:

1. identify the exact source path/commit;
2. determine whether Take-5 already reconstructs the behavior;
3. classify the delta as DUPLICATE, STRICT_GAIN, CONFLICT, HISTORICAL_ONLY, or OPEN;
4. transfer only STRICT_GAIN material with provenance;
5. preserve conflicts/OPEN explicitly;
6. validate the resulting Take-5 behavior;
7. only then mark the source item reconciled.

Reaserch does not regain working authority during this process.

## Administrative closure

After material drift is reconciled, Reaserch can be archived in GitHub to enforce the already-authorized read-only rollback role. Archiving is an administrative repository setting and is not performed by this content change.
