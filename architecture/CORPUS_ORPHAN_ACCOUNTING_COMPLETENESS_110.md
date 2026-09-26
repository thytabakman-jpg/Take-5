# Corpus Orphan Accounting Completeness 110

Date: 2026-09-26
Status: CURRENT CANDIDATE / PROOFABLE BASIS-RELATIVE REPLACEMENT FOR OPEN-WORLD ORPHAN COMPLETENESS

## Problem

"Global orphan completeness" is not a valid unqualified completion predicate for an open,
changing repository universe. A file that never existed leaves no path witness, and a future
artifact can always change the basis.

The correct proof object freezes the corpus and expected-object basis.

## Frozen basis

B =
<RepositoryTips,
 ObservedBlobs,
 TextTraversal,
 DeclaredExpectedReferences,
 PlacementBasis,
 MaterialSignalBasis,
 AuthorityCurrentnessBasis>.

Observed_B is every blob reachable from the frozen repository tips.

Expected_B is every declared repository-relative artifact reference recovered from the
frozen text corpus plus any explicit registry/manifest expectations supplied by the basis.

Universe:

U_B = Observed_B union Expected_B.

## Total accounting

Every x in U_B receives exactly one typed accounting disposition.

Observed artifacts receive a placement/disposition such as:

ACCOUNTED_PLACED
ACCOUNTED_EVIDENCE
ACCOUNTED_GENERAL
OPEN_UNRESOLVED_PLACEMENT
OPEN_GENERAL_MATERIAL_REVIEW.

Expected artifacts receive:

EXPECTED_PRESENT
CONFIRMED_MISSING_EXPECTED_REFERENCE.

OPEN is a terminal accounting disposition. It is not semantic resolution.

## Completeness theorem

OrphanAccountingComplete(B)

iff

1. every observed blob has a typed disposition;
2. every declared expected reference has a typed disposition;
3. hidden_unclassified_count = 0.

This proves accounting completeness relative to B.

It does not imply:

OrphanFree(B).

OrphanFree(B) additionally requires no confirmed missing expected artifact and no
other admitted orphan/ghost conflict.

The distinction is load-bearing:

accounting completeness answers "did anything in the frozen declared basis disappear
from the audit?"

orphan freedom answers "are all represented/expected obligations actually satisfied?"

## Expected-but-never-created boundary

No finite repository scan can prove completeness over an unspecified expectation universe.
Expected-object generation is therefore basis-relative and explicit.

A stronger claim requires an independently justified Expected_B generator. New registry,
manifest, project contract, or semantic obligation evidence reopens B.

## Executable witness

tools/corpus_orphan_audit.py

The auditor:
- enumerates every blob;
- scans every supported text line;
- uses corrected formal/status/open signal detection;
- extracts Markdown and repository-relative path references;
- assigns every blob a typed disposition;
- assigns every expected reference a typed disposition;
- preserves unresolved placement as OPEN;
- separates accounting_complete from orphan_free.

Regression:
tests/test_corpus_orphan_audit.py

## ProofCore consequence

The invalid open-world requirement is retired.

ProofCore may PASS the exact claim

OrphanAccountingComplete(B_frozen)

when the executable receipt has accounting_complete=true and hidden_unclassified_count=0.

ProofCore may not turn that PASS into open-world orphan freedom.
