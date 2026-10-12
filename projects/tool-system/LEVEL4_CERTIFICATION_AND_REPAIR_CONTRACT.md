# Level 4 — Claim Integrity, Repair, and Certification Contract

**Status:** proposed global Level 4 rule, submitted through Take-5 change control.  
**Scope:** every Level 4 review of a file or knowledge node, regardless of subject.  
**Authority boundary:** applies the current governing goal, object authority, package rules, repository governance, and source-native specialist standards; does not create a new research theorem or overwrite a tool's semantic owner.

## Governing requirements

**1.** Level 4 must establish the governing purpose and requirements of the file, verify every material claim and dependency against the authoritative knowledge nodes, and actively repair any defects it discovers.

**2.** Level 4 certification is granted only after every applicable requirement is satisfied, every material factual claim is adequately substantiated or accurately corrected, and all necessary repairs have passed reverification. Legitimate open research questions do not prevent certification; unresolved certification defects do.

These are **positive mandatory gates**, not advice or a permission to stop after documenting an error.

## The distinction that controls certification

- An **honest open question** explicitly asks what is not yet established. It makes no unsupported factual claim that the answer is known. It is a legitimate part of a knowledge node; Level 4 need not solve it.
- A **factual assertion** is a statement presented as established, current, proved, valid, implemented, or satisfied, including claims disguised by headings/status labels. It requires adequate evidence in the correct knowledge owner or an accurate, verified correction.
- A **certification defect** is a failure of a governing requirement, material factual support, necessary dependency, accuracy, source ownership, or verification. It must be repaired and reverified before PASS.
- An **accurate correction** may qualify or withdraw an unsupported statement **only when the corrected text is true-to-evidence and the file's original governing job/requirements remain satisfied**. This does not force a researcher to solve an unsolved question, but it cannot simply re-label a factual assertion `OPEN` and declare victory.
- **Unresolved defects never produce PASS.** Record `INCOMPLETE` with exact remaining issues when repair cannot be completed, so work may continue. A failure receipt is useful history and **is not a Level 4 certification**.

## Ownership in the knowledge web — all subjects

The authoritative home is determined by **the content and function of the knowledge**, not which audit, test, or tool originally exposed it. All information needed for the claim's current use and Level 4 verification must be accessible from that owning node (or its named, subordinate local proof/verification files).

- Mathematical findings and required mathematical proofs/counterexamples belong in the relevant Mathematics node/folder.
- Logical findings and native proof obligations belong in the relevant Logic node; philosophical claims, distinctions and warrants in Philosophy.
- Tool behavior and implementation evidence belong to the corresponding configured tool/runtime owners.
- Reusable research methods belong to the proper method/tool owner. A method's *history* is not the knowledge it uncovers.
- A file relying on another discipline must cite that discipline's authoritative node, not an arbitrary historical audit as a substitute.

External original publications may still be cited at exact locations. Archival audit receipts preserve discovery history, failed paths, repair provenance, and reproducibility; they are **not sole authorities for substantive knowledge**.

## Required Level 4 sequence

1. **Establish identity, owner, purpose, governing goal and requirements.** Read applicable current source contracts and dependency boundaries; do not invent a weaker goal.
2. **Enumerate material factual assertions, open questions and dependencies.** Distinguish what a statement **asserts** from labels such as `OPEN`, `PARTIAL`, `TESTED`, or `CERTIFIED`.
3. **Challenge and trace.** Validate each consequential assertion against its authoritative knowledge, proofs, counterexamples, source scope and current version. Record which requirements and claims were examined, not merely a positive score.
4. **Repair every material defect.** Correct claims, missing necessary evidence, broken links, mislocated authoritative results, inconsistent dependencies or unsafe status assertions in their **owning nodes**. Repair can include a justified factual qualification, but cannot silently drop a governing requirement, abandon essential functionality, or weaken the goal to obtain PASS.
5. **Reverify after repair.** Re-read changed bytes, rerun relevant tests/source checks and adversarial negative controls, validate affected downstream nodes, and confirm the corrected factual state. A repair plan, audit receipt, historical prior pass or file navigation success alone does not count.
6. **Decide certification strictly.** `PASS` is legal only if purpose, every applicable requirement, material claim, dependency and repair passes current verification and the integrity of genuinely OPEN questions is preserved. Otherwise return `INCOMPLETE`, with precise remaining work; do not award Level 4.

**Research completeness is not certification completeness.** Unsolved research questions may remain open; an unsupported theorem presented as solved may not.

## Fail-closed structured receipt (source-tested; not a semantic proof engine)

A configured Level 4 job can supply a `level4_certification_packet` containing:

- `target_ref`, `authority_ref`, `purpose`, `purpose_verified`, `evidence_refs`, `reviewer_ref`;
- `requirements` with stable IDs, applicability, PASS/INCOMPLETE status and checking evidence;
- `claims` with stable IDs, explicit baseline/current representation, `FACTUAL_ASSERTION` or `OPEN_RESEARCH_QUESTION` classification, and support or verified correction;
- `dependencies` identifying the actual owning knowledge node, scope, verification and evidence;
- `defects` with repair/recheck evidence, plus an `inspection_refs` trace even when no defects are found;
- `reverification_refs`, `reverified` and optional `declared_status`.

The [receipt validator](../../runtime/level4_certification.py) derives PASS or INCOMPLETE from those fields. It rejects omitted proof/check references, unresolved defects, unsupported assertions, a missing baseline for OPEN-question classification, and unverified factual-to-OPEN relabeling. It cannot verify the *truth* of a proof merely from a self-reported field; specialist/source inspection and actual execution remain mandatory. A structural validator PASS alone is **not** an independent specialist Level 4 certificate.

When the configured parent return receives `context.level4_certification_required = true` **or detects an explicit Level 4 request in its contextual `job`, `request`, or `user_request` fields**, the [parent gate](../../runtime/improvement_core_return_gate.py) must re-evaluate `state.level4_certification_packets` and reject `COMPLETE` if absent or INCOMPLETE. Producers must pass the user's actual request or the explicit selector flag. This is a fail-closed configured return check; a host omitting both a request and the flag still requires separate host-binding verification.

## Adversarial negative controls

At minimum, confirm:

1. honest OPEN research with otherwise supported claims **can** pass;
2. unsupported statement of fact **cannot** pass even if re-labeled OPEN;
3. missing source/evidence, unchecked dependency, unsatisfied governing requirement **cannot** pass;
4. an unresolved defect or repair without reverification **cannot** pass;
5. qualified/retracted unsupported factual claim with verified accurate correction **can** pass if the original file's purpose and governing requirements still hold;
6. missing Level 4 packet **blocks** a Level 4-required parent COMPLETE;
7. a receipt's self-declared PASS **cannot override** computed INCOMPLETE;
8. ordinary non-Level-4 work is not made to require a Level 4 packet by this gate.

**Certification is a verified result, not a name for a completed audit.**
