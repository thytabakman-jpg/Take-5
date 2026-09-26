# Take-6 Frozen Repository Inventory Validation 001

Date: 2026-09-26
Status: PASS

Five frozen repository trees were enumerated recursively from their exact tree SHAs.

| Source | Tree entries | Blobs |
| --- | ---: | ---: |
| Reaserch | 2383 | 2281 |
| Take-2 | 37 | 23 |
| Take-3 | 10 | 7 |
| Take-4 | 64 | 50 |
| Take-5 | 858 | 814 |
| Total | 3352 | 3175 |

Every recursive tree response reported non-truncated coverage.

The inventories preserve path, Git object type, Git SHA, mode, and available byte size.

This is structural member accounting, not semantic admission. Every blob remains evidence until Take-6 ingestion and semantic reconstruction assign a typed disposition.

The inventories provide the migration baseline needed to detect:
- missing files;
- changed paths;
- substituted blobs;
- files omitted by semantic filtering;
- predecessor objects that never receive a migration disposition.

The two intended external ZIP objects remain outside this repository-tree inventory and remain OPEN until exact object identities and byte/hash bindings are recovered.
