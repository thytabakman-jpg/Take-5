# Self-management

Status: CURRENT

The first managed project is ProjectManager itself.

The self-instance has no privileged bypass.

It satisfies the same control questions applied to any project

what is this project
what is its goal
what is in and out of scope
who owns each mutable object
what deliverables exist
what is scheduled
what resources exist
what depends on what
what interfaces and risks exist
what remains unknown
what evidence decisions and lessons exist
what changes are admissible
what is the current lifecycle state
what verification remains
what communications and handoffs exist

Any ProjectManager change is first a proposed delta to this project.
Implementation success is evidence.
Canonical promotion remains subject to Take-5 repository governance and validation.


The self-instance also carries the same 17 known-failure controls and five root
invariants required of managed project packages. Missing or stale self-controls fail
OPEN; ProjectManager cannot exempt itself from its own failure-prevention envelope.

## Self-instance evidence and admission boundary

The checked-in PROJECT_STATE.json is a nonauthoritative runtime input projection.
It carries 21 owned project coordinates, 17 failure-control entries and five
root-invariant entries; the owner documents, source state and native tests stay
separate. The existence of all projection keys does not prove currentness of
every represented claim or authorize a write.

Use tests/test_project_manager_failure_immunity.py to validate the self-instance
integrity envelope and replay the native regression suite against a known head.
A clean observer run is evidence, not automatic project or repository closure.
The separate user-approved promotion and stale-precondition commit gate is still
an exact-evidence question (OPEN_QUESTIONS.md Q4); full semantic campaign V50
also remains independently OPEN. Reenter through the ordinary owner files,
not a self-project exception or a new duplicate controller.
