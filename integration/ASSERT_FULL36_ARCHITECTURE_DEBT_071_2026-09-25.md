# ASSERT Full-36 Architecture Debt 071

Date: 2026-09-25

Status: OPEN — LARGER SYSTEM PROBLEM

## Immediate compatibility repair

Normal full ASSERT is now required to expose three current-use surfaces under typed D36_C:

1. ASSERT Layer 1
   - ASSERT
   - COMPARE_1
   - RESOLVE
   - HERE
   - COMPARE_2
   - INQUIRE
   - REASSERT
   - every stage receives all 36 D36_C cells

2. ASSERT Layer 2
   - current question-family basis Q01 through Q22
   - every family receives all 36 D36_C cells

3. Cognitive 36
   - DIFFERENTIATE
   - RELATE
   - RECONSTRUCT
   - STRENGTHEN
   - every operator receives all 36 D36_C cells

This compatibility contract is executable in runtime/assert_full36.py and is bound into the configured ASSERT identity.

## Why this does not close the larger problem

The repository did not contain an authoritative historical artifact explicitly naming "ASSERT Layer 1" and "ASSERT Layer 2" before this repair.

The exact historical provenance and intended nesting of the four cognitive operators is not fully recovered.

The exact relationship among D36_C, D36_H, D216 and D288 remains governed by an OPEN geometry-selection problem.

The current patch therefore guarantees the requested full-36 execution surface for ASSERT without claiming that the global geometry architecture or original historical semantics have been reconstructed.

## Larger unresolved problem

The system still permits architecture to be discussed or remembered at a richer level than the executable configured-run contract.

That produces the recurring failure:

design remembered
-> wrapper partially encoded
-> configured run loses a layer or geometry
-> later chat rediscovers the missing behavior

The larger repair must establish one authoritative typed execution specification from which:
- user-visible tool descriptions,
- wrapper semantics,
- configured-run identity,
- runtime expansion,
- tests,
- and cross-chat invocation

are all generated or verified.

Until that exists, this issue remains OPEN even though current ASSERT use is locally repaired.

## Required later work

- recover or reject the original historical Layer 1 / Layer 2 semantics from the full corpus;
- recover or reject the exact historical cognitive four-operator equation;
- settle D36_C versus D36_H ownership and the exact geometry-selection law;
- decide whether full-36 is mandatory for other configured tools or only ASSERT;
- bind host/chat invocation to the same typed configured-run contract;
- add holdouts proving that no future wrapper compression can drop Layer 1, Layer 2, or Cognitive 36.
