#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

TEXT_EXT={".md",".py",".yaml",".yml",".json",".toml",".txt",".sh",".js",".ts"}
SKIP={".git",".venv","venv","__pycache__","node_modules"}
FORMAL=re.compile(r"(?:^|\b)(?:define[sd]?|definition|theorem|lemma|invariant|equation|math(?:ematics)?|operator|kernel|contract|law|axiom|proof|iff|forall|exists)\b",re.I)
STATUS=re.compile(r"\b(?:CURRENT|SUPERSEDED|OPEN|BLOCKED|LOCKED|PROVISIONAL|REJECTED|OBSERVED|DERIVED|IMPLEMENTED|VALIDATED|MERGED|HISTORICAL|DEPRECATED)\b")
TODO=re.compile(r"\b(?:TODO|FIXME|TBD|XXX|OPEN QUESTION|UNRESOLVED|SORT[_ -]?LATER|ORPHAN|GHOST)\b",re.I)
MDLINK=re.compile(r"\[[^\]]*\]\(([^)#?]+)(?:#[^)]+)?\)")
PATH_TOKEN=re.compile(r"(?<![A-Za-z0-9_.-])((?:\.github|architecture|integration|runtime|tests|tools|research|projects|migration|historical|provenance|audit|audits|docs|sort-later)/[A-Za-z0-9_./-]+\.(?:md|py|yaml|yml|json|toml|txt|sh|js|ts))")

def placement(p:str)->str:
    q=p.lower()
    if q.startswith(".github/workflows/") or "/test" in q or q.startswith("tests/") or "validation" in q or "benchmark" in q:
        return "VERIFICATION"
    if q.startswith("runtime/") or q.startswith("tools/") or Path(q).suffix in {".py",".js",".ts",".sh"}:
        return "EXECUTABLE"
    if q.startswith("architecture/") or any(k in q for k in ("kernel","contract","policy","charter")):
        return "ARCHITECTURE"
    if q.startswith("integration/") or "current_" in q or "current-state" in q or "current_state" in q:
        return "CURRENT_CONTROL"
    if q.startswith(("historical/","provenance/","experiments/","audits/","audit/")):
        return "EVIDENCE_HISTORY"
    if q.startswith("research/") or "/research/" in q:
        return "RESEARCH"
    if q.startswith("projects/"):
        return "PROJECT_LOCAL"
    if q.startswith("sort-later/") or "inbox" in q or "backlog" in q:
        return "UNRESOLVED_PLACEMENT"
    if Path(q).suffix in {".yaml",".yml",".json",".toml"}:
        return "STATE_CONFIG"
    if q.endswith("readme.md"):
        return "NAVIGATION"
    return "GENERAL"

def disposition(place:str,material:bool,inbound:int)->str:
    if place=="UNRESOLVED_PLACEMENT":
        return "OPEN_UNRESOLVED_PLACEMENT"
    if place in {"EVIDENCE_HISTORY","RESEARCH"}:
        return "ACCOUNTED_EVIDENCE"
    if place in {"CURRENT_CONTROL","ARCHITECTURE","EXECUTABLE","VERIFICATION","STATE_CONFIG","NAVIGATION","PROJECT_LOCAL"}:
        return "ACCOUNTED_PLACED"
    if material and inbound==0:
        return "OPEN_GENERAL_MATERIAL_REVIEW"
    return "ACCOUNTED_GENERAL"

def audit(root:Path)->dict:
    root=root.resolve()
    blobs=[]
    text_records=[]
    inbound=Counter()
    expected=defaultdict(set)
    hashpaths=defaultdict(list)

    for p in root.rglob("*"):
        if not p.is_file() or any(part in SKIP for part in p.parts):
            continue
        rel=p.relative_to(root).as_posix()
        if rel.startswith("audit/runtime/"):
            continue
        blobs.append(rel)
        if p.suffix.lower() not in TEXT_EXT and p.name!=".gitignore":
            continue
        try:
            data=p.read_bytes()
            txt=data.decode("utf-8")
        except Exception:
            continue
        h=hashlib.sha256(data).hexdigest()
        hashpaths[h].append(rel)
        lines=txt.splitlines()
        formal=statuses=todos=0
        refs=set()
        for line in lines:
            formal += bool(FORMAL.search(line))
            statuses += bool(STATUS.search(line))
            todos += bool(TODO.search(line))
            if p.suffix.lower()==".md":
                for target in MDLINK.findall(line):
                    target=target.strip()
                    if "://" in target or target.startswith(("mailto:","data:","#")):
                        continue
                    try:
                        target=(p.parent/target).resolve().relative_to(root).as_posix()
                    except Exception:
                        pass
                    refs.add(target)
            for target in PATH_TOKEN.findall(line):
                refs.add(target)
        for target in refs:
            inbound[target]+=1
            expected[target].add(rel)
        text_records.append({
            "path":rel,
            "bytes":len(data),
            "lines":len(lines),
            "sha256":h,
            "placement":placement(rel),
            "formal_signal_count":formal,
            "status_signal_count":statuses,
            "open_signal_count":todos,
            "refs":sorted(refs),
        })

    blobset=set(blobs)
    rec_by_path={r["path"]:r for r in text_records}
    records=[]
    for rel in sorted(blobs):
        r=rec_by_path.get(rel)
        place=r["placement"] if r else placement(rel)
        material=bool(r and (r["formal_signal_count"] or r["status_signal_count"] or r["open_signal_count"]))
        records.append({
            "path":rel,
            "placement":place,
            "content_scanned":r is not None,
            "material_signal":material,
            "inbound_refs":inbound[rel],
            "disposition":disposition(place,material,inbound[rel]),
        })

    expected_records=[]
    for target,sources in sorted(expected.items()):
        exists=target in blobset
        expected_records.append({
            "path":target,
            "sources":sorted(sources),
            "exists":exists,
            "disposition":"EXPECTED_PRESENT" if exists else "CONFIRMED_MISSING_EXPECTED_REFERENCE",
        })

    duplicates=[{"sha256":h,"paths":ps} for h,ps in hashpaths.items() if len(ps)>1]
    unclassified=[r for r in records if not r["disposition"]]
    missing=[r for r in expected_records if not r["exists"]]
    open_records=[r for r in records if r["disposition"].startswith("OPEN_")]

    return {
        "schema":"CORPUS_ORPHAN_ACCOUNTING/v2",
        "basis":{
            "root":str(root),
            "blob_count":len(blobs),
            "text_file_count":len(text_records),
            "line_count":sum(r["lines"] for r in text_records),
        },
        "placement_counts":dict(Counter(r["placement"] for r in records)),
        "disposition_counts":dict(Counter(r["disposition"] for r in records)),
        "records":records,
        "expected_references":expected_records,
        "exact_content_duplicates":duplicates,
        "open_records":open_records,
        "missing_expected_references":missing,
        "proof":{
            "every_blob_dispositioned":len(records)==len(blobs) and not unclassified,
            "every_declared_expected_reference_dispositioned":all(r["disposition"] for r in expected_records),
            "hidden_unclassified_count":len(unclassified),
            "accounting_complete":len(records)==len(blobs) and not unclassified and all(r["disposition"] for r in expected_records),
            "orphan_free":not missing,
        },
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    ap.add_argument("--out",default="audit/runtime/CORPUS_ORPHAN_ACCOUNTING.json")
    args=ap.parse_args()
    out=audit(Path(args.root))
    op=Path(args.out)
    op.parent.mkdir(parents=True,exist_ok=True)
    op.write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({
        "blob_count":out["basis"]["blob_count"],
        "text_file_count":out["basis"]["text_file_count"],
        "line_count":out["basis"]["line_count"],
        "open_records":len(out["open_records"]),
        "missing_expected_references":len(out["missing_expected_references"]),
        "accounting_complete":out["proof"]["accounting_complete"],
        "orphan_free":out["proof"]["orphan_free"],
    }))
    raise SystemExit(0 if out["proof"]["accounting_complete"] else 1)

if __name__=="__main__":
    main()
