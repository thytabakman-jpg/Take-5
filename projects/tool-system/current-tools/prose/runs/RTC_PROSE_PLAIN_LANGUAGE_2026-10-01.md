# RTC Prose Plain-Language Run — 2026-10-01

Status: VALIDATED / ADMITTED / CANONICAL
Tool under improvement: Prose
Improvement operator: RTC / C48 Raise Ceiling
Math prerequisite:
- architecture/PROSE_PLAIN_LANGUAGE_RTC_MATHEMATICS_005_2026-10-01.md

## Frozen basis

Preserve:
- PROSE_PROTECTED_CONTRACT_ACCEPTANCE
- PROSE_AFFIRMATIVE_FIRST_GATE
- PROSE_FIRST_MENTION_PERSON_DATES
- PROSE_NUMERIC_YEAR_DATING_GATE
- PROSE_ORDERED_ANCHOR_GATE
- PROSE_SEMANTIC_STRENGTH_NO_INFLATION_RECEIPTS
- PROSE_READER_LOAD_GATE
- PROSE_QUESTION_TERMINATION_GATE
- PROSE_JEWISH_LEXICAL_FORM_GATE
- factual/source/date authority outside Prose
- no silent rewriting

## User rule

Use the simplest words that say exactly what you mean. Use technical terms only
when simpler words would make the meaning less accurate or precise. Never make
the writing harder just to make it sound more academic.

## C48 candidate frontier

A. Hard-coded academic-word blacklist
- strict_gain: false
- preserves: false
- reason: context can make a difficult technical term necessary for precision.

B. Numerical readability threshold
- strict_gain: false
- preserves: false
- reason: a score can improve by deleting required distinctions.

C. Evidence-gated PLAIN_LANGUAGE constraint
- strict_gain: true
- preserves: true
- reason: simplicity is compared only inside the set of semantically and
  technically equivalent realizations.

D. Merge the rule into READER_LOAD
- strict_gain: false
- preserves: true
- reason: reader load and needless lexical difficulty are distinct failure modes.

## C48 result

```
{
  "status": "ACCEPT",
  "strict_gain_or_failure": [
    {
      "id": "C_EVIDENCE_GATED_PLAIN_LANGUAGE",
      "strict_gain": true,
      "preserves": true
    }
  ]
}
```

## Implemented gain

New protected behavior:
PROSE_PLAIN_LANGUAGE_GATE

Runtime constraint:
PLAIN_LANGUAGE

Default-contract behavior:
PLAIN_LANGUAGE is included in the default ProseContract.

Evidence semantics:
- PASS: no known simpler wording preserves less reader burden with equal precision,
  or the harder technical term is required for precision;
- REPAIR_REQUIRED: a known simpler wording preserves the same meaning and precision;
- OPEN: the comparison is unevidenced;
- BLOCKED: the comparison has a typed blocker.

The runtime does not use a forbidden-word list and does not use a readability
score as a substitute for semantic comparison.

## Validation and admission

PR: #190
Merge commit: 89f8f2f80b0ada1a408f3f0b6dd732f1d8e0242b

Validated green before admission:
- Take-5 Validation — success
- Capability Preservation — success
- Tool System Every-Tool Sweep — success

Admission result:
- merged to main through the governed branch -> PR -> validation -> merge path.
