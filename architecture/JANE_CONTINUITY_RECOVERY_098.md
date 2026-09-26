# Jane Continuity Recovery 098

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE

## Recovered Jane role

Jane is continuity/currentness supervision and user-facing mediation.

Jane is not the adaptive solver and does not own substantive action selection while
ImprovementCore/ICC holds the controller lease.

The persistent Jane defect was narrower:

a new turn often received target/job/basis/current-state information from the host rather
than reconstructing enough of it from durable system evidence.

## Improvement

Jane now has a typed continuity packet:

J_t =
<Target,Job,Basis,CanonicalVersion,Protected,Open,CapabilityGaps,Evidence,Missing>.

The packet is READY only when the minimal entry coordinates are present.

Missing coordinates produce OPEN.

Jane projects this packet into controller context but does not choose the next action.

## Why this matters for anti-loss

When ImproveCore changes, recovery requires more than knowing its name.

Jane must be able to carry:

- which canonical object is current;
- what job was governing;
- what basis/currentness surface licensed that state;
- protected behavior that may not disappear;
- known OPEN coordinates;
- known capability-preservation gaps;
- evidence references needed to recover the object.

This makes continuity an explicit data object rather than an expectation that future chat
context will reconstruct it correctly.

## Runtime

runtime/jane_continuity.py

Regression:

tests/test_jane_continuity.py

## Remaining OPEN

Automatic host-wide loading of this packet at every new conversation remains outside the
repository's control.

Repository recovery can be made deterministic; universal external-host interception cannot
be claimed from repository code alone.
