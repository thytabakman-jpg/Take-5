# GOAL + HF2 — Two GitHub ZIP Evidence Run 123

Date: 2026-09-26
Repository basis: thytabakman-jpg/Take-5 main @ 566d7dc519e650fd2d5c4742d16a0bb252d455f3
Invocation profile: FULL_CONFIGURED_HF2_V1
Configured tool: GOAL
Recurrence: HF002
Mode: OBSERVER ordinary mode
Geometry: D36_C
Status: RELATIVE_CLOSE_WITH_OPEN_INPUT_BINDING

## User request

Treat two ZIP files said to exist inside GitHub as evidence.
Run current full GOAL with all current wrappers.
Apply HF2 afterward.
Then pass the result to ImprovementCore.

## External evidence actually acquired

Repository research inspected the connected GitHub installation.

Accessible repositories:
- thytabakman-jpg/Reaserch
- thytabakman-jpg/Take-2
- thytabakman-jpg/Take-3
- thytabakman-jpg/Take-4
- thytabakman-jpg/Take-5

Observed:
- no literal .zip path exists on the default branch tree of any of the five repositories;
- no GitHub Release asset exists in those repositories;
- repository issue search returned no user-repository issue containing the claimed ZIP pair;
- relevant branches checked by compare did not add a .zip file:
  - Reaserch: improvecore/whole-history-pass-20260926
  - Take-5: improvecore/chat-export-github-105
  - Take-5: improvecore/chat-history-4mo-2026-09-26
  - Take-5: improvecore/full-corpus-placement-audit-20260926
- GitHub Actions contains many downloadable ZIP-form workflow artifacts, including repeated take5-validation-receipts and improvecore-self-study-104 artifacts, so "two ZIP files inside GitHub" is not uniquely identifying.

The exact pair still lacks stable identifiers such as two filenames, artifact IDs, archive URLs, blob SHAs, or hashes.

## GOAL round 0

Initial target:

Use the two claimed GitHub archives as first-class evidence for the current system, inspect them without silent loss, and let downstream ImprovementCore use what they actually establish.

Material distinction:

The target cannot be satisfied by guessing which GitHub ZIP objects the user means.

HF2:
REAPPLY_C.

## GOAL round 1

Separate four obligations:

1. archive identity and acquisition;
2. byte/content traversal;
3. semantic extraction and admission;
4. ImprovementCore selection/action.

Existing owners already cover:
- external acquisition policy: runtime/improvement_core_external_acquisition.py
- admitted artifact traversal/extraction: runtime/artifact_intake.py
- global work selection/action: current ImprovementCore / IC-028 regime 091.

The live gap is prior to those owners: the claimed pair is not positively bound to two immutable GitHub objects.

HF2:
REAPPLY_C.

## GOAL round 2 — governing goal

Resolve and bind the exact two GitHub archives, then use them losslessly as evidence in the current ImprovementCore system.

Success requires:

A. Exact archive binding
For each archive Z_i:
GitHub object class + stable object identifier + repository/context + observed name + byte count + content hash.

B. Acquisition truth
The bytes actually retrieved correspond to the bound object.

C. No-skip traversal
Every admitted archive member receives a traversal/accounting receipt.

D. Semantic non-loss
Every material extracted candidate receives a durable typed disposition:
ADMITTED_CURRENT,
MERGED_OR_SUBSUMED,
REJECTED_WITH_GROUNDS,
RESEARCH,
OPEN_WITH_REENTRY,
BLOCKED_WITH_OWNER,
or HISTORICAL_ONLY.

E. Provenance
Every derived claim remains linked to archive/member/span provenance.

F. Controller freedom
Once evidence is admitted, ImprovementCore owns selection, ordering, action, reentry, and stopping.
The user's requested sequence is evidence, not a forced architecture.

G. Persistence
Material results and unresolved obligations become durable interconnected artifacts rather than remaining only in chat history.

## Reentry condition

The goal is stable.
The remaining OPEN coordinate is input identity, not goal ambiguity.

Reenter acquisition/traversal immediately when the exact two archive identities become addressable through the GitHub host surface.

## HF2 terminal disposition

No further same-capability goal refinement changes the governing target.

HF2[GOAL]:
RELATIVE_CLOSE.

Input binding:
OPEN.
