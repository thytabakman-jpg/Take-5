# Capability Mode Coverage Map 001

Date: 2026-09-24
Status: FIRST PRIMARY-MODE CLASSIFICATION
Authority: research only

This is a primary-mode classification, not a claim that each behavior/tool can operate in only one mode.
Secondary-mode membership remains important and will be tested separately.

## Behavior families B01-B58

### EO-D (6)
B05, B07, B11, B30, B34, B35

### EO-C (7)
B06, B08, B09, B13, B29, B44, B47

### CO-D (13)
B01, B02, B03, B04, B12, B26, B27, B41, B43, B48, B51, B52, B53

### CO-C (13)
B15, B17, B19, B20, B23, B24, B25, B39, B40, B42, B46, B50, B57

### EA-D (5)
B10, B14, B21, B37, B54

### EA-C (8)
B16, B22, B31, B33, B36, B38, B45, B56

### CA-D (1)
B32

### CA-C (5)
B18, B28, B49, B55, B58

Primary octant counts:
{
  "EO-D": 6,
  "EO-C": 7,
  "CO-D": 13,
  "CO-C": 13,
  "EA-D": 5,
  "EA-C": 8,
  "CA-D": 1,
  "CA-C": 5
}

Aggregated 2x2 counts:
{
  "EXPAND+OBSERVE": 13,
  "CONTRACT+OBSERVE": 26,
  "EXPAND+ACT": 13,
  "CONTRACT+ACT": 6
}

## C-tools C01-C49

### EO-D (4)
C07, C10, C12, C49

### EO-C (5)
C08, C09, C20, C23, C35

### CO-D (15)
C01, C02, C03, C04, C05, C06, C11, C13, C15, C37, C38, C39, C40, C45, C46

### CO-C (11)
C14, C17, C18, C19, C22, C33, C34, C41, C42, C44, C47

### EA-D (1)
C21

### EA-C (8)
C26, C27, C29, C30, C31, C32, C36, C48

### CA-D (0)
NONE

### CA-C (4)
C24, C25, C28, C43

Primary octant counts:
{
  "EO-D": 4,
  "EO-C": 5,
  "CO-D": 15,
  "CO-C": 11,
  "EA-D": 1,
  "EA-C": 8,
  "CA-D": 0,
  "CA-C": 4
}

Aggregated 2x2 counts:
{
  "EXPAND+OBSERVE": 9,
  "CONTRACT+OBSERVE": 26,
  "EXPAND+ACT": 9,
  "CONTRACT+ACT": 4
}

## Interpretation

The old 2x2 view alone says:
- OBSERVE is heavily represented, especially CONTRACT+OBSERVE;
- EXPAND+ACT has substantial system-improvement machinery;
- CONTRACT+ACT is thinner.

The 3D cube reveals the sharper fact:
- CONTRACT+ACT+DECOUPLED is almost empty.
- Only B32 (execution-truth recording) sits there naturally at the behavior layer, and it is not itself a delegated-execution transform.
- No C01-C49 tool is primarily a real bounded delegated executor.

Therefore the strongest underrepresentation is not a counting artifact.
It is a functional hole:
local specialist autonomy + actual execution + faithful reintegration.

Second underrepresentation:
EA-D has only one primary C-tool (C21 Successor Candidate Generation), although several behaviors contribute to it.

Third:
EO-C has several analytical ingredients but no explicit Reconciler program.

## Caveat

Primary classification can undercount multi-mode capabilities.
The next validation should assign secondary modes and test whether apparent gaps are reconstructible from cross-mode composition.
