"""Goal-decoupled generic observer for arbitrary record corpora."""
from collections import Counter,defaultdict

def observe_records(records):
    findings=[]
    ids=[]
    versions=defaultdict(list)
    refs=[]
    for i,r in enumerate(records):
        if isinstance(r,dict):
            if "id" in r: ids.append(r["id"])
            if "name" in r and "version" in r: versions[r["name"]].append(r["version"])
            for ref in r.get("refs",[]): refs.append((r.get("id",i),ref))
        else:
            ids.append(str(r))
    counts=Counter(ids)
    for x,n in sorted(counts.items(),key=lambda z:str(z[0])):
        if n>1: findings.append({"type":"DUPLICATE_ID","id":x,"count":n})
    known=set(ids)
    for source,ref in refs:
        if ref not in known: findings.append({"type":"UNRESOLVED_REF","source":source,"ref":ref})
    for name,vs in sorted(versions.items()):
        if len(set(vs))>1: findings.append({"type":"VERSION_PLURALITY","name":name,"versions":sorted(set(vs),key=str)})
    return {"status":"ACCEPT","findings":findings,"count":len(records)}
