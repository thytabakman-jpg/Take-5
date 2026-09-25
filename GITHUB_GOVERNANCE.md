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
