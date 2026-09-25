# Migration Runbook

Status: MIGRATION CANDIDATE

## Goal

Make distributed research recoverable without requiring reconstruction from chat history and without accidental promotion.

## Required migration loop

[
Harvest
ightarrow Normalize
ightarrow Type
ightarrow Reconcile
ightarrow Link
ightarrow Validate
ightarrow Persist
ightarrow Reindex
ightarrow Reenter.
]

## Harvest

Collect every known artifact, formula, result, map, tool definition, wrapper rule, test result, open blocker, and superseded claim from the September 24 lineages.

Do not discard uncertain or rejected objects.

## Normalize

Give every object a stable identity, type, source, date, status, authority plane, dependency list, and successor or supersession relation.

## Type

At minimum distinguish

promoted runtime authority

current semantic candidate

executable candidate

research hypothesis

historical provenance

open validation obligation

## Reconcile

Detect contradictions among chats, main, branches, PRs, registries, mathematics maps, and runtime selectors.

Never resolve a conflict by recency alone.

## Link

Every mathematical result must link to affected tools, maps, controllers, validators, runtimes, and consumer projects.

Every tool must link back to its semantic basis.

## Validate

Run basis change revalidation whenever shared mathematics changes.

Run semantic drift checks across current maps, registries, runtime bindings, and historical successor state.

Run candidate universe audits before making closure claims.

## Persist

Write reconciled state into the repository in both human readable and machine readable forms.

Chat history is provenance, not the database of record.

## Reindex

Maintain a small canonical start object that points to the current state, current mathematics, current runtime authority, current candidate architecture, current tool registry, and open validation frontier.

Repository search availability is not a substitute for this index.

## Reenter

After migration, regenerate obligations.

A structural change that affects candidate generation, tool identity, scope transitions, or continuation state forces reanalysis and regression.

## Migration completion test

Migration is complete only when a fresh session can answer all of the following without reconstructing prior chats:

What is current runtime authority?

What is the strongest semantic candidate?

What mathematics governs HF001 and Tool Run Closure?

What are the six scopes and why are there 36 transitions?

Which claims were superseded?

Which tools are executable candidates versus promoted?

What remains open?

Which files contain the evidence?

Until all are answerable from repository state, migration remains OPEN.
