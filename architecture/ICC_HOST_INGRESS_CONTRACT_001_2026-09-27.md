# ICC Host Ingress Contract 001

Date: 2026-09-27
Status: CURRENT BASIS / HARDENING IN CLEANUP CAMPAIGN

## Contents

- [Problem](#problem)
- [Invariant](#invariant)
- [Identity law](#identity-law)
- [Receipt](#receipt)
- [Validation](#validation)
- [Evidence contract](#evidence-contract)
- [Boundary](#boundary)

## Problem

Take-5 already owns the canonical ICC controller, bootstrap, configured tool
identity, currentness rules, and result path. An external ChatGPT host can still
receive a user turn before Take-5 code obtains control. That permits a false
surface state in which the host speaks as though ICC ran even when no canonical
repository entry occurred.

## Invariant

An external host may represent a response as repository-backed ICC only when it holds a structurally valid host ingress receipt for the exact request **and** a fresh authenticated attestation from a separately trusted verifier. The gateway fails closed when the verifier configuration or attestation is absent.

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

ICC identity claim = structural ingress receipt + trusted-verifier attestation of exact ingress + repository-backed controller execution.

Without the receipt, an external host remains the host and cannot claim that ICC
executed.

## Receipt

The receipt binds repository, ref, commit, controller, and a digest of the request body. Its five evidence identifiers are canonically serialized as a compact JSON array before hashing, preventing delimiter-injection aliases; receipt identity uses the V3 domain tag. Earlier V2 receipts are not authenticated under this new gate. The visible banner projects the controller, canonical source commit, and receipt identifier.

## Validation

PR #159 pre-admission head `e164235b7439f7d0829b32b66c12ee7c34255209` passed:

- Take-5 Validation run 36300397075: SUCCESS;
- Capability Preservation run 36300397054: SUCCESS.

The validation covered the full test suite, canonical whole-system audit,
closed-loop fixture, zero-request dump, and capability preservation.

## Evidence contract

Ingress evidence is carried as explicit receipt identifiers for repository
verification, currentness verification, entry binding, protected bootstrap, and
current controller registration. Naked boolean assertions do not satisfy the
host-ingress contract.

These receipts remain host-supplied evidence. Take-5 does not claim access to private external-host state that the host does not expose. The host gateway now requires a time-bounded HMAC attestation tied to the exact receipt and verified with a trusted deployment key, not supplied by the user request. A five-minute maximum lifetime limits stale-token use but does not enforce single-use replay prevention.

**Issuer obligation:** The independent trusted verifier must validate the real canonical repository/currentness, entry, ASSERT→GOAL bootstrap, and controller execution before signing. The MAC authenticates the issuer's statement but cannot itself prove the issuer honored that obligation. No trusted issuer/key configured means `OPEN/BLOCKED`, not an invented execution witness. This contract cannot compel an unrelated host to cooperate.

**Attestation encoding:** A trusted issuer signs the UTF-8 encoding of ten newline-separated fields in this fixed order: `TAKE5_HOST_EXECUTION_VERIFIER_V1`, repository, ref, full commit SHA, controller ID, request digest, evidence digest, structural receipt ID, issued-at Unix seconds, expires-at Unix seconds. The signature is lowercase HMAC-SHA256 hex using the secret provisioned as `TAKE5_TRUSTED_ICC_INGRESS_KEY` in the trusted gateway/verifier environment (minimum 32 UTF-8 bytes). The attestation names the same issuer and receipt ID. The issued-to-expiry interval cannot exceed 300 seconds; a future skew of more than 30 seconds or any expired attestation is rejected. Do not place the secret in repository files, user-supplied arguments or emitted results.

## Boundary

Repository code cannot force an unrelated host to call this module. Therefore
this contract solves truthful ICC identity and fail-closed repository ingress
where the host cooperates with Take-5. Universal host interception remains an
external platform capability, not a repository capability.
