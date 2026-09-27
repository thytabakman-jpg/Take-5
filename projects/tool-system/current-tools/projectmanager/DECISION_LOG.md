# Decision log: ProjectManager

Append-only.

## 2026-09-27 D001

Created the non-destructive project package. Existing semantic/runtime authority
was preserved in place; this package owns organization, routing, and retained
package-local state only.


## 2026-09-27 D002

Synced the validated pre-project admission capability into the current ProjectManager package.

The package now explicitly routes the ProjectDefinitionCandidate branch, promotion barrier,
runtime, protected behavior, regression surface, and canonical FullMath 002 authority without
duplicating their editable semantics.
