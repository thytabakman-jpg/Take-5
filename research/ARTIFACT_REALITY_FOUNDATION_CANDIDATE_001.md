# Artifact Reality Protection Primitive — Foundation Candidate 001

Date: 2026-09-24
Status: FOUNDATIONAL CANDIDATE / PLACEMENT OPEN BETWEEN KERNEL AND SYSTEM CORE
Origin: successful ARA-001 project-mathematics repair

## Discovery

Artifact reality is not merely an audit tool.

Any system that persists named load-bearing objects across episodes can silently diverge between:
- the object the controller believes exists;
- the semantics distributed across artifacts;
- the declared canonical object;
- the actually executable object.

Therefore artifact-reality protection is a candidate foundational invariant.

## Candidate invariant

For every current load-bearing persistent object o:

Current(o) -> (
  Identity(o)
  and Canon(o)
  and Currentness(Canon(o))
  and Authority(Canon(o))
  and Deps(o) subseteq Cover(o)
  and ArtifactDelta(o) = emptyset_or_typed_residual
).

Persistence or registration alone is insufficient.

Persisted(o) !=> Reconstructible(o).
Registered(o) !=> Canonical(o).
Specified(o) !=> Executable(o).

## Transition guard

Any material transition that creates or changes a load-bearing persistent object must execute:

identify -> reconstruct dependencies -> update canonical object/imports -> update registry/index -> verify ArtifactDelta -> persist typed residuals -> permit completion.

A failed guard blocks completion language for that transition. It does not necessarily block unrelated work.

## Placement hypothesis

This behavior belongs at least in SYSTEM CORE because removing it recreates demonstrated silent-fragmentation failures.

Whether the entire mechanism belongs in KERNEL is OPEN.

Strong kernel candidate:
- invariant/guard that current persistent load-bearing objects must be reconstructible, current, authority-typed, and artifact-delta closed or typed OPEN.

Likely non-kernel implementation:
- repository enumeration;
- semantic matching;
- PD execution;
- repair algorithm;
- registry writes;
- recursive audit implementation.

Thus:
Kernel candidate = protection contract + transition legality.
Core/foundation = protection contract + discovery/repair/verification machinery.
Runtime = concrete scanners/writers/executors.

## PD test required

Run independent Core/Kernel PD and ablation:
1 remove invariant but keep ARA tool;
2 keep invariant but move scanner/repair outside kernel;
3 test whether every episode requires the guard or only persistence-changing transitions;
4 test ephemeral/nonpersistent objects;
5 compare with external integrity, transactional, type-safety, provenance, package-lock and durable-workflow mechanisms.

Do not freeze placement before those tests.
