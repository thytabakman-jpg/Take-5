# Take-6 Frozen Repository Inventory Validation 001

Date: 2026-09-26
Status: PASS / CURRENTNESS-REPAIRED

Five frozen repository trees are enumerated recursively from exact tree SHAs.

| Source | Tree entries | Blobs |
| --- | ---: | ---: |
| Reaserch | 2383 | 2281 |
| Take-2 | 37 | 23 |
| Take-3 | 10 | 7 |
| Take-4 | 64 | 50 |
| Take-5 migration cutoff | 875 | 831 |
| Total | 3369 | 3192 |

Every recursive tree response reports non-truncated coverage.

The Take-5 migration cutoff is:

853c7f92dae62747d3f8f42a38b6d4b77e194ad2

with tree:

6bb206f9c22776b595e62bb3c1ab19197df0f395

This cutoff includes the restored Legacy ImprovementCore control law and modern-guard implementation. It intentionally precedes the source-freeze commit itself so the source manifest does not become self-referential.

The inventories preserve path, Git object type, Git SHA, mode, and available byte size.

This is structural member accounting, not semantic admission. Every blob remains evidence until Take-6 ingestion and semantic reconstruction assign a typed disposition.

The inventories provide the migration baseline needed to detect:
- missing files;
- changed paths;
- substituted blobs;
- files omitted by semantic filtering;
- predecessor objects that never receive a migration disposition.

The two intended external ZIP objects remain outside this repository-tree inventory and remain OPEN until exact object identities and byte/hash bindings are recovered.

## Currentness repair

The first source-freeze pass pointed Take-6 at Take-5 commit 360b93b66f307ff800299d3a2122a00d336c66a3.

That was stale because the Legacy restoration subsequently present in the parent chain at 853c7f92dae62747d3f8f42a38b6d4b77e194ad2 was not inside that frozen migration basis.

ICC-123 verification detected the backwards pointer.

ImprovementCore repaired the cutoff and removed duplicate source-ref authority from BOOTSTRAP_MANIFEST.json. Repository/archive source identity is now owned only by SOURCE_MANIFEST_001.json.
