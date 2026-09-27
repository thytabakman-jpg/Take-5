# ICC Host Ingress Contract 001

Date: 2026-09-27
Status: CANDIDATE PENDING VALIDATION

## Problem

Take-5 already owns the canonical ICC controller, bootstrap, configured tool
identity, currentness rules, and result path. An external ChatGPT host can still
receive a user turn before Take-5 code obtains control. That permits a false
surface state in which the host speaks as though ICC ran even when no canonical
repository entry occurred.

## Invariant

An external host may represent a response as repository-backed ICC only when it
holds a valid host ingress receipt for the exact request.

The receipt requires all of the following:

1. the user request explicitly invokes ICC;
2. the canonical repository is thytabakman-jpg/Take-5;
3. the canonical ref is main;
4. a concrete canonical commit SHA is known;
5. canonical repository identity was verified;
6. currentness was verified;
7. the ICC entry contract was bound;
8. the protected ASSERT then GOAL observer bootstrap completed;
9. the controller identity is ICC128;
10. ICC128 is registered current.

Missing evidence fails closed.

## Identity law

ICC prefix alone is intent, not execution.

ICC identity claim = host ingress receipt + repository-backed controller execution.

Without the receipt, an external host remains the host and cannot claim that ICC
executed.

## Receipt

The receipt binds repository, ref, commit, controller, and a digest of the
request body. The visible banner projects the controller, canonical source
commit, and receipt identifier.

## Boundary

Repository code cannot force an unrelated host to call this module. Therefore
this contract solves truthful ICC identity and fail-closed repository ingress
where the host cooperates with Take-5. Universal host interception remains an
external platform capability, not a repository capability.
