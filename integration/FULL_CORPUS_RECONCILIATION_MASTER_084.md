# Full Corpus Reconciliation Master 084

Date: 2026-09-26
Status: AUDIT BRANCH / NON-PROMOTING
Canonical working repository: Take-5

## Corpus boundary

This campaign freezes and indexes five repositories:

- Take-2
- Take-3
- Take-4
- Take-5
- Reaserch

At audit start the recursive trees contained 2,561 files in total, including 1,929 Markdown files.

Repository counts:
- Take-2: 23 files, 17 Markdown
- Take-3: 7 files, 5 Markdown
- Take-4: 50 files, 34 Markdown
- Take-5: 547 files, 353 Markdown
- Reaserch: 1,934 files, 1,520 Markdown

Each repository now has a branch-local full-corpus placement manifest and a line-complete content-auditor implementation.

## Authority model

Take-5 remains the current working substrate.

Take-2 contributes compact kernel and transition discipline.
Take-3 contributes strict-gain/minimality discipline.
Take-4 contributes cumulative autonomy, reselection, and goal reconstruction evidence.
Reaserch contributes high-recall provenance, audit history, tool lineage, and candidate strict gains.

No repository self-promotes by chronology.

## Placement invariant

Every discovered artifact receives exactly one audit disposition relative to its current job:

CURRENT_CONTROL
ARCHITECTURE
EXECUTABLE
VERIFICATION
STATE_CONFIG
RESEARCH
PROJECT_LOCAL
EVIDENCE_HISTORY
NAVIGATION
UNRESOLVED_PLACEMENT
GENERAL

Placement is not authority. A historical artifact can contain a current strict-gain candidate. A current-looking filename can still be stale.

## Information routing law

For every material finding F:

source artifact
-> exact source freeze
-> job/referent identity
-> provenance
-> conflict/currentness comparison
-> DUPLICATE | STRICT_GAIN | CONFLICT | HISTORICAL_ONLY | OPEN
-> destination layer
-> authorized transition
-> verification
-> currentness propagation
-> reentry.

A raw file move is never a substitute for this chain.

## Privacy boundary

Reaserch is private while Take-5 is public. Private source text is not copied into Take-5 merely because it is relevant. Public promotion requires a separate declassification-safe synthesis or an already-public equivalent.

## Orphan rule

Unlinked or oddly placed material is not deleted. The audit distinguishes:

1. unreviewed coverage gap;
2. confirmed orphan;
3. historical evidence with no current inbound link;
4. duplicate content;
5. broken reference;
6. strict-gain candidate lacking canonical destination;
7. stale currentness claim.

Only category 6 demands promotion work. Categories 2, 4, and 5 demand repair. Historical evidence can remain intentionally unlinked when provenance requires it.

## Execution truth

The repository manifests prove path coverage.

The installed content auditor is designed to read every text line and report:
- hashes and line counts;
- Markdown headings;
- formal/math signals;
- status/currentness signals;
- TODO/OPEN/orphan signals;
- relative links and broken links;
- exact duplicates;
- unlinked Markdown candidates.

The newly added GitHub workflow did not auto-start during this campaign. Therefore line-complete CI execution is OPEN and is not represented as completed.

## Immediate reconciliation frontier

1. execute the content auditor in each repository;
2. disposition every reported orphan candidate;
3. review every broken reference;
4. compare every exact duplicate whose copies claim different authority/currentness;
5. review private-source strict-gain candidates through the privacy boundary rather than copying them wholesale;
6. update canonical Take-5 contracts only after verified admission;
7. rerun currentness propagation and closure.

## Anti-regression

No future ImproveCore run can claim repository-wide information closure from tool count, file count, or one current-state document alone. Closure is indexed to a frozen corpus plus explicit dispositions and reentry on new material evidence.
