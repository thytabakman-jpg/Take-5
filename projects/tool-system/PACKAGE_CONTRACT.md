# Tool Project Package Contract

Status: CURRENT CANDIDATE

Every current configured tool and every known ICC/IC variant receives a durable
package.

## Required package pages

README.md
MANIFEST.md
AUTHORITY_REGISTRY.md
CURRENT_STATE.md
IDENTITY.md
MATHEMATICS.md
RUNTIME.md
PROTECTED_BEHAVIORS.md
DEPENDENCIES.md
SOURCE_MAP.md
OPEN_QUESTIONS.md
CHANGE_CONTROL.md
REGRESSION_CONTRACT.md
DECISION_LOG.md
LESSONS_LEDGER.md
HANDOFF_SURFACE.md
evidence/README.md
runs/README.md
history/README.md
coverage/README.md

plus exactly 36 Scope x ModeFace coverage pages.

## Ownership

MATHEMATICS.md and RUNTIME.md are routing projections. They do not replace the
canonical manifest/runtime/lineage artifacts.

CURRENT_STATE.md is a disposable current projection over retained history.

DECISION_LOG.md, LESSONS_LEDGER.md, evidence/, runs/, and history/ are append-only.

coverage/*.md owns only its exact Scope x ModeFace coordinate and never becomes
canonical semantic truth merely because a finding appears there.

## Historical ICC variants

Historical variants live under icc-variants/ and never enter the live configured
registry merely because a package exists.

Same-number branches remain separate until equivalence is demonstrated.

Unrecovered labels get OPEN packages rather than invented mathematics.

## Creation

The package generator is create-only. Existing differing content causes a hard
collision instead of silent replacement.
