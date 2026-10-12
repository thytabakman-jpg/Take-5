# Resources

Status: CURRENT

Execution resources
Take-5 canonical repository.
Historical GitHub Actions validation receipts for the exact commits they tested.
Direct repository source inspection and read-back using connected GitHub tools.
Current registered tool stack.
External research through public standards and guidance.
Existing Sukkos project as project-management precedent.

Authority resources
Explicit user instruction.
Current Take-5 contracts.
Validated repository governance.

Constraint
A local container may not have a working GitHub network path. Connected repository
tools can inspect and update exact source blobs but do not themselves execute native
tests. Run required native tests on an available execution host and verify the tested
commit; do not treat historical CI receipts as validation of a newer source head.
If no required native validation path is available, keep the affected validation OPEN
rather than claiming that GitHub Actions ran.
