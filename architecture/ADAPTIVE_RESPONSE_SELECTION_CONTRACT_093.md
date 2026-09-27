# Adaptive Response Selection Contract 093

Date: 2026-09-27
Status: IMPLEMENTED REGRESSION GUARD

For conversation state \(z\), candidate responses \(a\), and admissible set \(A(z)\):

\[
A(z)
=
\{a:
IdentityMatch(a,z)
\land FormatMatch(a,z)
\land Exact(a)
\land Complete(a)
\land Unsupported(a)=0
\land Drift(a)=0
\land a\notin Reject(z)
\}.
\]

The response selector is:

\[
\pi(z)
=
\arg\min_{a\in A(z)}
Extra(a).
\]

User rejection updates state:

\[
z_{t+1}
=
U(z_t,Reject(a_t)).
\]

Thus feedback changes the next admissible response set rather than merely adding conversational commentary.

Implementation:
- runtime/adaptive_response_selector.py
- tests/test_adaptive_response_selector.py

Scope:
repository-side guard. External host-wide interception remains outside repository authority.
