# Protected Transition Integrity

A capability can exist locally and still be lost across the path that makes it useful.

For protected behavior b, require a witnessed chain:

canonical identity
-> configured dispatch
-> execution
-> result consumption
-> state update
-> reentry
-> user-visible boundary.

Every coordinate must be VERIFIED for an end-to-end protected execution claim.

OPEN or missing coordinates keep the chain OPEN.
A BLOCKED coordinate blocks the chain.

This invariant complements capability preservation:

Protected Transition Integrity asks whether one configured execution survives end to end.

Capability Preservation additionally asks whether the capability's semantics, selection basis,
future reachability, and recovery witness survive successor changes.

Neither local success nor source-code presence substitutes for the complete chain.
