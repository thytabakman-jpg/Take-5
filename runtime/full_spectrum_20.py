"""Candidate FULL-SPECTRUM-20 configured ensemble.

Explicit FullSpectrum runs treat unknown relevance as a reason to probe.
NON_APPLICABLE requires a positive basis.
"""
FAMILIES=(
"GOAL_TARGET_FREEZE","DOS_OBSERVE","MTA","MT_MODE_SWEEP","PD","PD_AUDIT",
"MULTI_OBJECT_MOMT","ARCHITECTURE","ROOT_CAUSE","ARA_ARTIFACT_REALITY",
"ORPHAN_GHOST_CONFLICT","CURRENTNESS","ROLE_ASSIGNMENT_OWNER_CLOSURE",
"CONSEQUENCE_AFFECTED_CONE","RTC_RAISE_CEILING","MTOS","TRANSFER_CORE",
"EXECUTION_TRUTH_ACTIVATION","A16_HOLDOUT_ABLATION","GOAL_COMPLETION_CERT"
)
TERMINAL=("SELECT","PROBE","NON_APPLICABLE","BLOCKED","OPEN")
def disposition(selected=(),non_applicable=(),blocked=(),open_families=()):
    sel,na,bl,op=map(set,(selected,non_applicable,blocked,open_families))
    out={}
    for f in FAMILIES:
        if f in sel: out[f]="SELECT"
        elif f in na: out[f]="NON_APPLICABLE"
        elif f in bl: out[f]="BLOCKED"
        elif f in op: out[f]="OPEN"
        else: out[f]="PROBE"
    return out
