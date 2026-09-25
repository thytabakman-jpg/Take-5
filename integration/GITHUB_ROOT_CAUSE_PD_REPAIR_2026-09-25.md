# GitHub Root Cause + PD Repair

Date: 2026-09-25
Status: implementation packet
Canonical target: Take-5

## Observer result

The apparent twenty GitHub mistakes reduce to six recurring generators.

1. ADMISSION_INVERSION
   Canonical state could be mutated before verification.

2. MIGRATION_CURRENTNESS_FAILURE
   Take-5 was explicitly promoted while Reaserch continued receiving new work.

3. SUPPLY_CHAIN_LOOSENESS
   Action tags and the test dependency were mutable, and dependency update automation was absent.

4. GOVERNANCE_ENFORCEMENT_GAP
   `main` had no server-side protection, CODEOWNERS, or repository-local PR contract.

5. HYGIENE_PRIVACY_GAP
   Ignore rules and explicit credential/email controls were absent.

6. LEGACY_RESOURCE_AMPLIFICATION
   The private legacy Reaserch repository ran many Actions workflows and several hourly schedules. Four hourly one-job schedules alone require at least 2,880 rounded runner-minutes in a 30-day month. That exceeds the 2,000 included private-repository minutes on GitHub Free before push CI is counted.

## Root-cause relation

```
weak currentness boundary
+ weak admission boundary
+ unbounded automation
+ mutable supply chain
= repeated drift, red legacy CI, and authority confusion
```

The red Reaserch Actions runs observed on 2026-09-25 had zero executed steps, runner_id 0, and no runner name. They therefore do not establish a repository-validator failure. They establish failure before runner assignment. Given the private-repository usage design, quota/billing exhaustion is the leading causal explanation and remains account-state dependent.

## PD / AuditCore

Target:
GitHub operating boundary for ICC.

Protected results:
- Take-5 remains canonical.
- Reaserch remains provenance/rollback evidence.
- Take lineage remains available for experiments.
- OPEN state is preserved.
- no security claim is manufactured from unavailable account settings.

Material distinctions:
- persisted vs canonical;
- legacy evidence vs current authority;
- CI validator failure vs runner-substrate failure;
- repository-file controls vs GitHub-admin controls;
- experimental Take repository vs production authority.

## ImprovementCore

Strict gain is obtained by moving enforcement toward the boundary rather than adding more internal reports.

Implemented package:
- `.gitignore`;
- CODEOWNERS;
- PR template;
- Dependabot;
- pinned pytest dependency;
- immutable Action SHAs;
- explicit workflow permissions;
- broader canonical-file validation triggers;
- governance regression tests;
- canonical GitHub governance contract;
- explicit legacy drift state.

## TransferCore

Reaserch post-cutover content is not copied wholesale.

Transfer rule:
a Reaserch result enters Take-5 only when the exact source object, provenance, target effect, duplication status, authority, and validation basis are represented.

This prevents the repair from recreating Reaserch inside Take-5.

## Tool Run Closure

Repository-file changes can close after the Take-5 validation workflow passes.

Administrative controls remain BLOCKED on the connected GitHub tool boundary because the available integration exposes repository content/PR operations but not repository/account administration writes.

Those controls are captured in the GitHub issue created with this repair.

## HF reentry

Reenter this repair when:
- Take-5 validation fails;
- a post-cutover Reaserch result proves materially absent from Take-5;
- branch protection becomes enabled;
- account security verification changes the OPEN/BLOCKED state;
- a governance regression test finds a recurrence.
