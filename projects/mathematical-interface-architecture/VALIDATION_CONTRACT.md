# Mathematical Interface Architecture Validation Contract

Status CURRENT
Date 2026-09-25

## Four independent gates

A MIA artifact is not accepted merely because one gate passes.

### Semantic gate

The artifact preserves the frozen mathematical object and its reconstruction state.

### Artifact gate

Identity, version, provenance, source disposition, imports, and currentness are explicit.

### Render gate

The visible surface preserves natural mathematical form and direct glyph status without exposing renderer syntax as user content.

### Integration gate

The artifact agrees with the registry, source manifest, gap ledger, and all other affected project artifacts.

## Required acceptance evidence

Every material change records

- changed object
- changed artifact
- affected artifacts
- mathematical delta or explicit NONE
- reconstruction-status delta
- currentness delta
- rendering delta
- validation result
- unresolved OPEN items

## Failure semantics

A semantic pass does not override a render failure.

A render pass does not override a mathematical change.

A test pass does not establish global currentness.

A current artifact with unresolved dependencies remains OPEN rather than silently complete.

## Closure

Relative project closure requires

- all eight core artifact roles present
- no broken registry references
- one declared mathematical baseline
- all discovered current MIA sources dispositioned
- color specimen renderable
- no raw renderer syntax in the canonical visible specimen
- every live friction item repaired or typed OPEN
- validation check passing on the current branch
