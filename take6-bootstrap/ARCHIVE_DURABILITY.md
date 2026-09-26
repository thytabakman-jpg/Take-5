# Take-6 Archive Durability

Date: 2026-09-26
Status: REQUIRED / NOT YET PROVISIONED

Content addressing detects corruption and substitution. It does not prevent total loss of one storage provider or one account.

Therefore:

[
Durable(cid)
iff
ContentVerified(cid)
land
|IndependentTrustDomains(cid)| ge 2.
]

A second clone inside the same GitHub account is not automatically an independent trust domain.

The target production archive uses at least:

1. primary versioned repository/object store;
2. independent cold replica under a distinct failure domain.

Every durable checkpoint records verified replica witnesses.

A permanence claim is blocked while the independent replica requirement is unmet.

The bootstrap runtime provides the fail-closed durability predicate in:

runtime/durability.py

Provisioning the second trust domain is a migration/promotion obligation, not something this Take-5 staging branch can falsely claim to have completed.
