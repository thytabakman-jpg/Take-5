# MultiObject Batch 3 — Level 1 validation closure

**Evidence ID:** B03-L1-002.  
**Status:** CLOSED_RELATIVE for all 37 original Batch 3 files at source-level triage depth.  
**Supersedes only the pending-validation disposition** in [B03-L1-001](batch-03-level1-triage.md); it does **not overwrite** or discard that original evidence record.

## Last blocker and actual repair

The unchanged research source `research/QUESTION_SEARCH_RUN_001.yaml` (blob `1f18b7271357a7157180eb260fd1e9740e384e21`) initially lacked an evidenced strict YAML parse and consumer contract test, so its Level 1 F5/D17 disposition was `BLOCKED_VALIDATION`.

Added pinned `PyYAML==6.0.2` to `requirements-dev.txt` and created `tests/test_question_search_run_yaml_contract.py` with:

- strict YAML parsing of the actual repository source;
- duplicate mapping-key rejection, with a deliberately duplicated-key negative control;
- declared research-run identity and basis-relative closure statuses;
- complete Q01–Q22 question-family roster and required string fields;
- preservation of the named `Q04 = Together Math` identity.

The original YAML source was **not edited**.

## Execution and independent evidence

- The Take-5 [validation run 38102000557](https://github.com/thytabakman-jpg/Take-5/actions/runs/38102000557) completed **SUCCESS** on test-and-dependency commit `1f08dccd4f8b29797378026e8dcd5f03fa9f5345`.
- Exact recorded test summary: **1,108 passed, 1 skipped, 1 warning**.
- The canonical whole-system audit, closed-loop fixture and zero-request check each completed **SUCCESS** in that run.
- The negative-control test establishes that the parser does not silently overwrite duplicate YAML keys; the positive-control test verifies the actual 284-line research source and Q01–Q22/Q04 structure.
- The 34 Reaserch documents were read and Level 1 triaged on main through `15ca147190f63aae3aac61160efad23c822be451`; 13 received source repairs. The three Take-5 originals were checked through `9abdfb5e710f9d2b95231a6093dfd655c85f0a94`; one received a source repair. Their previously recorded before/after blobs are retained unchanged in B03-L1-001.
- Additional reusable test infrastructure edits (dependency and new test) are outside the original 37-file roster. They are recorded rather than miscounted as two more original documents.

## Revised acceptance disposition

**D17/F5 for YAML:** PASS for strict syntax, duplicate-key and locally declared registry-contract consumption. Broader scientific validity, completeness of the question universe, and execution of unrelated external downstream readers are **not** proved.

**B1 PASS:** `37 = 14 repaired_verified + 23 passed_unchanged + 0 blocked + 0 unprocessed`.  
**B2 PASS:** All identified safe Level 1 source corrections were committed; nothing remains at P0/P1 merely as a suggestion.  
**B3 PASS:** No original Batch 3 file remains blocked at the verified source-triage depth.

**Protected limits:** `BASIS_RELATIVE_FIXED_POINT` is still basis-relative; `global_completeness: OPEN` remains OPEN, the native MultiObject relation provider remains an external requirement, historical proof/open statuses retain their original meaning, and a Level 1 source pass is not Level 2 or Level 3 mathematical verification.

**Campaign-level gate:** Batch 3 is closed relative to its selected 37 files; the full 117-file corpus's formal closure remains separately contingent on Batch 1's missing D01–D18/F1–F8 receipt and any later authoritative inventory change.
