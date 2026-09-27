# Anti-Loss Contract

Status: CURRENT CANDIDATE

## Invariants

A1 one mutable truth has one owner.
A2 current projections never substitute for retained history.
A3 new evidence is appended under a unique record ID.
A4 package generation cannot overwrite a changed existing file.
A5 coverage cells are dimension-owned and cannot overwrite neighboring cells.
A6 current tool inventory and package inventory remain in exact parity.
A7 aliases route to an existing object and do not create duplicate authority.
A8 unresolved mathematics/runtime/currentness stays typed OPEN.
A9 historical ICC branches are preserved as distinct objects when identity differs.
A10 organization does not change semantics.
A11 plan, configured identity, runtime entrypoint, execution, receipt, and closure remain distinct.
A12 the two 36-cell structures are never merged by cardinality.
A13 a material change triggers affected-cone review instead of clean rebuild.
A14 source pointers preserve legacy provenance without copying it into a competing current owner.
A15 a new tool is not project-complete until its package is materialized and validated.

## Fail-closed rule

Any violation keeps the organizational migration OPEN.
