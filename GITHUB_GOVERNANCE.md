# GitHub Governance

Status: CURRENT CANONICAL REPOSITORY CONTROL
Date: 2026-09-25
Canonical repository: `thytabakman-jpg/Take-5`

## Authority

Take-5 is the canonical working repository for ICC.

`thytabakman-jpg/Reaserch` is the rollback/provenance baseline declared by `MIGRATION_STATE.yaml`. Post-cutover writes in Reaserch do not regain canonical authority merely because they exist.

Take-2, Take-3, and Take-4 are lineage and experimental systems unless a later explicit migration changes their authority.

## Mutation path

Material canonical changes use:

```
branch
-> pull request
-> validation
-> review/admission
-> merge
-> branch retirement
```

Direct writes to `main` are a governance defect.

GitHub server-side branch protection is the preferred enforcement boundary. Until that repository setting is enabled, this file and the governance regression tests provide an internal guard but do not replace server enforcement.

### Protected-core Level 1 triage gate

This is a stricter **mutation gate**, not a replacement for the existing Level 1
document checks and process acceptance. For kernel, controller, authority,
migration, admission, execution, state, and other load-bearing core surfaces,
apply the complete applicable D01–D18 and A/F/B/P checks of the established
first-pass triage procedure, while keeping the file **unchanged by default**.
Risk follows the actual consumer and effect, not the filename or format.

Before proposing a change, bind the exact source blob, applicable authority,
known live consumers, and protected behavior. Distinguish founding intent,
present authorized responsibility, observed implementation, and future target.
None independently authorizes rewriting another. A historical goal, a recently
observed behavior, or a clearer proposed architecture is not a replacement
authority. An unresolved discrepancy stays explicit; Level 1 does not resolve
it by selecting whichever wording appears most current.

Authorize a Level 1 core edit only for a **specific established defect** with a
uniquely supported correction, identified owner, and affirmative non-interference
evidence for all relevant known consumers. A link, heading, status, YAML field,
TOC anchor, and explanatory note can all be load-bearing: never assume they
are cosmetic. Preserve deliberately historical references, unknown consumers,
all information and meaningful dependencies. Do not remove, relocate, retitle,
or reconcile material merely to fit an inferred goal.

Use the existing branch -> PR -> validation -> admission path; compare the
accepted before-state with the proposed change, test affected references and
native consumers, and reread the saved blob. Syntax-only success, a documented
plan, an unmerged PR, or a passing test that omits the affected behavior is
not proof of a completed repair. If authority, consumer impact, or validation
remains uncertain, leave the original intact and record a precise deferred
disposition in the existing triage workstream. Do not claim that unresolved
mandatory checks passed. This Level 1 safeguard does **not** prohibit later
explicitly authorized Level 2/3 substantive work.

## Admission invariant

A change is not canonical merely because it was persisted.

```
persisted != validated != admitted != canonical
```

The repository implementation of the system rule is:

```
VERIFY -> ADMIT -> MAIN
```

not:

```
MAIN -> VERIFY
```

## CI

The canonical validation workflow runs for both pull requests and relevant pushes.

External Actions are pinned to immutable commit SHAs.

Workflow permissions remain explicit and least-privilege.

Development dependencies are pinned in `requirements-dev.txt` and maintained through Dependabot.

## Branch lifecycle

Merged or abandoned short-lived branches are retired after their evidence is preserved in the pull request or canonical artifacts.

Long-lived branches require an explicit role. Historical provenance belongs in commits, tags, pull requests, or designated artifacts rather than an indefinitely growing set of active branches.

## Repository roles

The canonical repository remains compact relative to the legacy Reaserch corpus. Historical evidence can remain external when copying it would recreate the same multi-authority problem.

Material post-migration Reaserch changes enter Take-5 only through an explicit TransferCore-style reconciliation. A legacy commit is evidence, not authority.

## Security and privacy

Repository files never contain credentials or private environment data.

Public commit metadata can expose the configured Git author email. Account-level commit-email privacy is therefore part of the operating security baseline.

## Administrative enforcement

The following controls live in GitHub repository/account settings rather than repository files:

- protect `main`;
- require a pull request before merge;
- require the `Take-5 Validation / validate` status check;
- require conversation resolution;
- block force pushes and branch deletion on `main`;
- enable automatic deletion of merged head branches;
- archive/freeze Reaserch after drift reconciliation;
- verify account 2FA/passkeys, private commit email, token inventory, and secret-protection settings.

Unverified admin settings remain explicit OPEN/BLOCKED state rather than being represented as complete.
