# Tool Project Package Contract

Status: CURRENT PACKAGE-SCHEMA CONTRACT (repository-owned; does not promote tool semantics)

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

plus exactly 36 separately addressable Scope x ModeFace **logical coordinates** per package. The package manifest (or a typed evidence registry) may represent currently empty coordinates without 36 physical placeholder files. Any coordinate with admitted evidence retains independently addressable, append-only evidence and provenance; unknown or changed content must not be discarded. The separate directed SourceScope x TargetScope handoff structure remains distinct.

## Ownership

MATHEMATICS.md and RUNTIME.md are routing projections. They do not replace the
canonical manifest/runtime/lineage artifacts.

CURRENT_STATE.md is a disposable current projection over retained history.

DECISION_LOG.md, LESSONS_LEDGER.md, evidence/, runs/, and history/ are append-only.

A materialized coverage/*.md owns only its exact Scope x ModeFace evidence coordinate and never becomes canonical semantic truth merely because a finding appears there. Empty logical coordinates live in MANIFEST.md or an equivalent typed registry; generated placeholder files are optional.

## Curated source maps and generator ownership

The package generator owns the minimum, create-only package template. Current tool
`SOURCE_MAP.md` pages may contain separately authored, source-specific navigation
and preserved historical evidence. The existing source map, not a second generated
copy, owns those additional human-reading links.

The current-tool materializer accepts an unchanged minimum template, or a curated
source map only after verifying its exact package identity, protected configured
runtime registry/manifest/conductor references, its shared crosswalk anchor, and
its type-specific navigation distinction. It does not rewrite either source.
Missing/invalid authority or a crosswalk mismatch is a collision, not a reason
to discard provenance. The MultiObject source map remains fully generated and
byte-for-byte checked because that package has an explicit reproducibility owner.

A fresh configured package's generated minimum source map is not evidence that
the package is represented in the cross-repository crosswalk. The crosswalk's
own registry-parity gate requires a new package row, and package navigation
requires its derived source-map section before claiming discoverability.

## Historical ICC variants

Historical variants live under icc-variants/ and never enter the live configured
registry merely because a package exists.

Same-number branches remain separate until equivalence is demonstrated.

Unrecovered labels get OPEN packages rather than invented mathematics.

## Creation

The package generator is create-only. Existing differing content causes a hard
collision instead of silent replacement.
