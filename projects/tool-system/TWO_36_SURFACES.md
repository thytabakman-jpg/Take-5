# The Two 36-Cell Structures

Status: CURRENT

## Execution / coverage surface

Scope x ModeFace

6 scopes x 6 faces = 36 cells.

This is the per-tool coverage surface materialized under each package's coverage/.

## Directed handoff surface

SourceScope x TargetScope

6 scopes x 6 target scopes = 36 cells.

This surface belongs to typed semantic handoff packages and remains separate.

## Navigation and ownership

- [Tool-system authority registry](AUTHORITY_REGISTRY.md)
- [Goal package coverage example](current-tools/goal/coverage/README.md)
- [Semantic-object package contract](../../architecture/LOAD_BEARING_SEMANTIC_OBJECT_PACKAGE_CONTRACT_064.md)

## Invariant

36 = 36 does not imply role identity.

No renderer, generator, audit, or migration may write evidence from one surface
into the other merely because their cardinalities match.
