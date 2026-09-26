# Take-6 Migration Source Freeze 001

Date: 2026-09-26

Status: REPOSITORY SOURCE FREEZE PASS / EXTERNAL ZIP PAIR OPEN

## ImprovementCore selection

After the Take-6 bootstrap merged, ImprovementCore selected source freezing as the next promotion prerequisite because migration against moving predecessor state would recreate currentness drift.

## Freeze law

For a Git repository source:

[
SourceFrozen(s)
iff
Repository(s)
land CommitSHA(s)
land TreeSHA(s).
]

A branch name alone is not a frozen source.

For an external archive:

[
ArchiveFrozen(a)
iff
StableObjectID(a)
land ByteCount(a)
land SHA256(a).
]

A filename or conversational phrase is not sufficient.

## Frozen repository sources

The machine-readable manifest freezes current observed refs for:

- Reaserch
- Take-2
- Take-3
- Take-4
- Take-5

It also preserves the declared frozen legacy ImprovementCore behavioral reference at:

thytabakman-jpg/Reaserch@e4c76c595b44a35fd9efc02cde8979e656ef54e8

## Two intended ZIP archives

The historical Take-5 evidence explicitly concluded that the phrase "the two ZIP files in GitHub" did not uniquely resolve to two immutable GitHub objects.

That remains true in the preserved evidence.

Take-5 later implemented exact bound-ZIP ingestion and fail-closed byte/hash validation, which solves the ingestion mechanism.

It does not identify which two external objects the user meant.

Therefore:

[
oxed{ZIPPairIdentity=OPEN}
]

No pair is invented for Take-6 migration.

## Consequence

Take-6 can begin deterministic repository ingestion against exact frozen commits immediately.

The two intended external archives remain a separate acquisition edge and cannot silently block or contaminate repository-source migration.

## Current migration frontier

Closed:
- repository lineage source identity;
- current Take-5 source identity;
- legacy behavioral benchmark commit identity.

Open:
- exact identity of the intended two external GitHub ZIP objects;
- byte/hash manifest for those two archives;
- actual Take-6 vault ingestion;
- semantic reconstruction and tool-capsule migration.
