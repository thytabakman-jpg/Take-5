"""Validate Level 4 evidence/repair receipts; not a substitute for expert review."""
from collections.abc import Mapping

def refs(x):
    return isinstance(x,(list,tuple)) and bool(x) and all(isinstance(v,str) and v.strip() for v in x)

def nonblank(x):
    return isinstance(x,str) and bool(x.strip())

def assess_level4(packet):
    """Return (PASS|INCOMPLETE, residuals), computed rather than self-declared."""
    if not isinstance(packet,Mapping):
        return "INCOMPLETE",("MISSING_LEVEL4_PACKET",)
    issues=[]
    for field in ("target_ref","authority_ref","purpose","reviewer_ref"):
        if not nonblank(packet.get(field)): issues.append("MISSING_"+field.upper())
    for field in ("purpose_verified","claim_inventory_verified","reverified"):
        if packet.get(field) is not True: issues.append("NOT_VERIFIED_"+field.upper())
    for field in ("evidence_refs","inspection_refs","reverification_refs"):
        if not refs(packet.get(field)): issues.append("MISSING_"+field.upper())
    reqs=packet.get("requirements")
    if not isinstance(reqs,list) or not reqs: issues.append("REQUIREMENTS_NOT_ENUMERATED")
    else:
        for i,r in enumerate(reqs):
            if not isinstance(r,Mapping) or not nonblank(r.get("id")): issues.append(f"INVALID_REQUIREMENT:{i}");continue
            if r.get("applicable") is True:
                if r.get("status")!="PASS" or not refs(r.get("evidence_refs")): issues.append("REQUIREMENT_UNSATISFIED:"+r["id"])
            elif r.get("applicable") is False:
                if not nonblank(r.get("reason")) or not refs(r.get("evidence_refs")): issues.append("REQUIREMENT_NOT_JUSTIFIED:"+r["id"])
            else: issues.append("APPLICABILITY_UNKNOWN:"+r["id"])
    # An audit/report pointer is provenance, not substantive residence.
    # These receipts are structural: the reviewer still checks actual owner bytes.
    def check_residence(row, ident):
        residence=row.get("residence")
        if not isinstance(residence,Mapping):
            issues.append("MISSING_LOCAL_EVIDENCE_RESIDENCE:"+ident)
            return
        if (not nonblank(residence.get("owner_ref"))
                or not refs(residence.get("inspection_refs"))
                or not refs(residence.get("local_evidence_refs"))
                or residence.get("verified") is not True):
            issues.append("LOCAL_EVIDENCE_NOT_VERIFIED:"+ident)
        # A well-formed audit locator is still not owner-resident evidence.
        local_refs=residence.get("local_evidence_refs")
        if refs(local_refs):
            audit_prefixes=("audit:","report:","historical:","validation:","provenance:")
            if all(str(ref).lower().startswith(audit_prefixes)
                   or "/audits/" in str(ref).lower()
                   or "/validation/" in str(ref).lower()
                   for ref in local_refs):
                issues.append("HISTORICAL_AUDIT_ONLY:"+ident)
        status=residence.get("status")
        if status=="ALREADY_LOCAL":
            return
        if status=="REPAIRED_AND_VERIFIED":
            if not (refs(residence.get("discovered_source_refs"))
                    and refs(residence.get("transfer_refs"))
                    and refs(residence.get("post_transfer_recheck_refs"))):
                issues.append("LOCAL_EVIDENCE_TRANSFER_NOT_VERIFIED:"+ident)
            elif (set(residence["discovered_source_refs"])
                  == set(residence["local_evidence_refs"])
                  and set(residence["transfer_refs"])
                  == set(residence["local_evidence_refs"])):
                issues.append("HISTORICAL_AUDIT_ONLY:"+ident)
            return
        issues.append("UNKNOWN_LOCAL_EVIDENCE_STATUS:"+ident)

    claims=packet.get("claims")
    if not isinstance(claims,list): issues.append("CLAIMS_NOT_ENUMERATED")
    else:
        for i,c in enumerate(claims):
            if not isinstance(c,Mapping) or not nonblank(c.get("id")): issues.append(f"INVALID_CLAIM:{i}");continue
            cid=c["id"]; kind=c.get("kind");base=c.get("baseline_kind")
            if not nonblank(c.get("text")):issues.append("MISSING_CLAIM_TEXT:"+cid)
            if kind=="FACTUAL_ASSERTION" or base=="FACTUAL_ASSERTION":
                check_residence(c,cid)
            if kind=="OPEN_RESEARCH_QUESTION":
                if c.get("asserted_as_fact") is not False:issues.append("OPEN_ASSERTS_FACT:"+cid)
                if base=="FACTUAL_ASSERTION":
                    if c.get("correction_verified") is not True or not refs(c.get("correction_refs")) or not nonblank(c.get("prior_text")) or c.get("prior_text")==c.get("text"):issues.append("FACT_RELABELED_OPEN:"+cid)
                elif base!="OPEN_RESEARCH_QUESTION":issues.append("UNKNOWN_OPEN_BASELINE:"+cid)
            elif kind=="FACTUAL_ASSERTION":
                if base!="FACTUAL_ASSERTION":issues.append("UNKNOWN_FACT_BASELINE:"+cid)
                if c.get("disposition")=="SUBSTANTIATED":
                    if not refs(c.get("evidence_refs")):issues.append("UNSUPPORTED_FACT:"+cid)
                elif c.get("disposition")=="CORRECTED":
                    if c.get("correction_verified") is not True or not refs(c.get("correction_refs")) or not refs(c.get("evidence_refs")) or not nonblank(c.get("prior_text")) or c.get("prior_text")==c.get("text"):issues.append("UNVERIFIED_CORRECTION:"+cid)
                else:issues.append("UNRESOLVED_FACT:"+cid)
            else:issues.append("UNKNOWN_CLAIM_KIND:"+cid)
    deps=packet.get("dependencies")
    if not isinstance(deps,list):issues.append("DEPENDENCIES_NOT_ENUMERATED")
    else:
        for i,d in enumerate(deps):
            if not isinstance(d,Mapping) or not nonblank(d.get("id")) or not nonblank(d.get("owner_ref")) or d.get("status")!="VERIFIED" or not refs(d.get("evidence_refs")):issues.append(f"UNVERIFIED_DEPENDENCY:{i}")
    # A dependency can be reachable via a valid link yet be empty locally.
    if isinstance(deps,list):
        for i,d in enumerate(deps):
            if isinstance(d,Mapping) and (not refs(d.get("local_evidence_refs"))
                                         or d.get("local_residence_verified") is not True):
                issues.append(f"DEPENDENCY_LOCAL_EVIDENCE_MISSING:{i}")
    defects=packet.get("defects")
    if not isinstance(defects,list):issues.append("DEFECTS_NOT_ENUMERATED")
    else:
        for i,d in enumerate(defects):
            if not isinstance(d,Mapping) or not nonblank(d.get("id")) or d.get("status")!="RESOLVED" or not refs(d.get("repair_refs")) or not refs(d.get("recheck_refs")):issues.append(f"UNRESOLVED_DEFECT:{i}")
    if packet.get("declared_status") not in (None,"PASS"):issues.append("DECLARED_NONPASS")
    return ("INCOMPLETE" if issues else "PASS",tuple(issues))

def level4_required_for_request(text):
    import re
    return bool(re.search(r"\b(?:level\s*[- ]?4|level\s+four|l4)\b",text,re.I))
