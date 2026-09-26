# ImproveCore Run 087 — Whole-Chat Audit Reentry

Date: 2026-09-26
Status: EXECUTED / MATERIAL IMPROVEMENT / CLOSURE OPEN
Input: MT Whole-Chat Run 086
Manager: current ImproveCore regime
Target: make the five-repository audit architecture capable of proving the user's requested completion condition

## Governing goal

Produce a corpus audit whose completion claim means:

every in-scope artifact is addressable;
every text artifact is traversed;
every material semantic finding is surfaced;
every material finding receives a provenance/currentness-aware disposition;
every strict gain reaches its canonical destination;
references and authority conflicts are repaired;
the final state is current;
ProofCore passes relative to the final frozen corpus.

## Root failure

The current campaign conflates three stages that must remain separate:

1. addressability;
2. candidate detection;
3. semantic disposition.

The manifests solve 1.
The content auditor partially solves 2.
Nothing yet closes 3 at corpus scale.

A second failure is temporal:
the source corpus can change during the audit.

A third failure is configured-tool currentness:
HF-002 became load-bearing after the original audit branch was cut.

## Architecture improvement

Define the audit as a typed state machine:

A0 FREEZE
A1 ENUMERATE
A2 TRAVERSE
A3 EXTRACT_CANDIDATES
A4 SEMANTIC_DECOMPOSE
A5 CLASSIFY_LOAD_BEARINGNESS
A6 RECONCILE_PROVENANCE_CURRENTNESS
A7 DISPOSITION
A8 APPLY_AUTHORIZED_REPAIRS
A9 VERIFY_DESTINATIONS
A10 CURRENTNESS_REBASE
A11 PROOFCORE
A12 TERMINAL_OR_REENTER.

Transition law:

A_i -> A_(i+1)

only with a receipt proving the prior state's obligations are closed or typed OPEN/BLOCKED.

Any new material repository delta after A0 invalidates the affected cone and reenters at the earliest affected stage.

## New completion object

AuditReceipt =
<CorpusBoundary,
 PathCoverage,
 TraversalCoverage,
 CandidateLedger,
 SemanticDispositionLedger,
 RepairLedger,
 DestinationVerification,
 CurrentnessState,
 ProofReceipt,
 OpenBlocked>.

Complete(Audit)
iff
all claim-relevant coordinates are terminal
and ProofReceipt=PASS.

## Orphan definition repair

A confirmed orphan is not merely an unlinked Markdown file.

ConfirmedOrphan(x)
requires:

x is in reviewed scope
and x contains or constitutes material information
and no valid canonical destination/reference relation currently accounts for it.

An unlinked historical evidence file can be intentional.
An unreviewed file is a coverage gap.
A duplicate with conflicting authority is a conflict.
A strict-gain candidate without destination is an unresolved promotion candidate.

## Scanner role correction

The existing scanner becomes CandidateExtractor, not Auditor.

Its output is evidence for A3 only.

Rename at the semantic level:

full_corpus_placement_audit.py
role = CandidateExtractor + structural checks

until semantic A4-A7 are actually implemented.

No completion claim may cite scanner output alone.

## Black-box integration

Every candidate requiring interpretation enters BlackBoxDecomposition.

Required return:

SemanticCandidate =
<Source,
 ClaimOrObject,
 Relation,
 MathOrConstraint,
 LoadBearingness,
 Provenance,
 Currentness,
 CandidateDestinations,
 Conflicts,
 Evidence,
 Open>.

Unknown load-bearingness remains OPEN.
It never collapses to false.

## HF-002 integration

Every formal audit-stage tool receives HF2Applicability.

For CandidateExtractor:
HF2 is REQUIRED only when its own changed successor/input state exposes new structural candidates.

For SemanticDecomposer:
HF2 is REQUIRED while the same semantic object has a live local material frontier.

For ProofCore:
HF2 follows the current full-tool contract and re-applies only when ProofCore's local successor remains type-compatible and materially live.

ImproveCore remains the parent manager.

## Currentness repair

The active audit branch cannot be declared current while Reaserch main contains post-freeze validated HF-002 work.

Required action:
reconcile source delta first, then regenerate affected manifests/receipts.

Do not overwrite the older branch history.
Create a new current audit episode or explicitly rebase/reconcile with provenance.

## Strict-gain routing

Material discoveries from private Reaserch do not move verbatim into public Take-5.

For every strict gain:

private exact source
-> provenance hash/pointer
-> declassification-safe abstraction
-> same-job comparison
-> regression witness
-> public canonical destination when licensed.

## Immediate execution frontier

1. treat the existing scanner as candidate extraction only;
2. add SemanticDispositionLedger as a required artifact;
3. reconcile the latest Reaserch delta including HF-002;
4. run the extractor over the current corpus boundary;
5. feed every material candidate through semantic decomposition;
6. resolve the 41 known unresolved-placement candidates;
7. repair broken references/authority conflicts discovered by the scan;
8. route strict gains;
9. rerun MT under HF-002 on the changed audit architecture;
10. run ProofCore on the final receipt.

## ImprovementCore result

STRICT_GAIN:
the audit now has a proof-capable state model and a precise completion object.

PRESERVED:
all prior path manifests, isolation branches, ProofCore failure evidence, privacy boundaries, and anti-loss rules remain valid.

REJECTED:
file-count completion, path-classification completion, and scanner-only completion.

OPEN:
actual corpus-wide semantic execution and final disposition remain unfinished.

## Stop state

RELATIVE_OPEN.

The system has a better architecture and a precise next frontier, but the user's original complete-audit goal is not yet satisfied.
