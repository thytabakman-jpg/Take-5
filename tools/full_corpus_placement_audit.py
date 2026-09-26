#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

TEXT_EXT={".md",".py",".yaml",".yml",".json",".toml",".txt",".sh",".js",".ts"}
SKIP={".git",".venv","venv","__pycache__","node_modules"}
FORMAL=re.compile(r"(?:^|\\b)(?:define[sd]?|definition|theorem|lemma|invariant|equation|math(?:ematics)?|operator|kernel|contract|law|axiom|proof|iff|⇒|→|⊢|\\\\forall|\\\\exists)\\b",re.I)
STATUS=re.compile(r"\\b(?:CURRENT|SUPERSEDED|OPEN|BLOCKED|LOCKED|PROVISIONAL|REJECTED|OBSERVED|DERIVED|IMPLEMENTED|VALIDATED|MERGED|HISTORICAL|DEPRECATED)\\b")
TODO=re.compile(r"\\b(?:TODO|FIXME|TBD|XXX|OPEN QUESTION|UNRESOLVED|SORT[_ -]?LATER|ORPHAN)\\b",re.I)
LINK=re.compile(r"\\[[^\\]]*\\]\\(([^)#?]+)(?:#[^)]+)?\\)")

def placement(p):
    q=p.lower()
    if q.startswith(".github/workflows/") or "/test" in q or q.startswith("tests/") or "validation" in q or "benchmark" in q: return "VERIFICATION"
    if q.startswith("runtime/") or q.startswith("tools/") or Path(q).suffix in {".py",".js",".ts",".sh"}: return "EXECUTABLE"
    if q.startswith("architecture/") or any(k in q for k in ("kernel","contract","policy","charter")): return "ARCHITECTURE"
    if q.startswith("integration/") or "current_" in q or "current-state" in q or "current_state" in q: return "CURRENT_CONTROL"
    if q.startswith(("historical","provenance/","experiments/","audits/")): return "EVIDENCE_HISTORY"
    if q.startswith("research/") or "/research/" in q: return "RESEARCH"
    if q.startswith("projects/"): return "PROJECT_LOCAL"
    if q.startswith("sort-later/") or "inbox" in q or "backlog" in q: return "UNRESOLVED_PLACEMENT"
    if Path(q).suffix in {".yaml",".yml",".json",".toml"}: return "STATE_CONFIG"
    if q.endswith("readme.md"): return "NAVIGATION"
    return "GENERAL"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    ap.add_argument("--out",default="audit/runtime/FULL_CORPUS_CONTENT_AUDIT.json")
    args=ap.parse_args()
    root=Path(args.root).resolve()
    records=[]; inbound=Counter(); broken=[]; hashpaths=defaultdict(list); all_paths=set()
    for p in root.rglob("*"):
        if not p.is_file() or any(part in SKIP for part in p.parts): continue
        rel=p.relative_to(root).as_posix()
        if rel.startswith("audit/runtime/"): continue
        all_paths.add(rel)
        if p.suffix.lower() not in TEXT_EXT and p.name!=".gitignore": continue
        try:
            data=p.read_bytes(); txt=data.decode("utf-8")
        except Exception:
            continue
        lines=txt.splitlines(); sha=hashlib.sha256(data).hexdigest(); hashpaths[sha].append(rel)
        headings=[]; formal=[]; statuses=[]; todos=[]; refs=[]
        for i,line in enumerate(lines,1):
            if p.suffix.lower()==".md" and line.lstrip().startswith("#"): headings.append({"line":i,"text":line.strip()[:240]})
            if FORMAL.search(line): formal.append({"line":i,"text":line.strip()[:300]})
            sm=STATUS.findall(line)
            if sm: statuses.append({"line":i,"tokens":sm,"text":line.strip()[:300]})
            if TODO.search(line): todos.append({"line":i,"text":line.strip()[:300]})
            if p.suffix.lower()==".md":
                for target in LINK.findall(line):
                    target=target.strip()
                    if "://" in target or target.startswith(("mailto:","data:")): continue
                    try: drel=(p.parent/target).resolve().relative_to(root).as_posix()
                    except ValueError: drel=target
                    refs.append({"line":i,"target":drel}); inbound[drel]+=1
        records.append({"path":rel,"placement":placement(rel),"bytes":len(data),"lines":len(lines),"sha256":sha,
                        "headings":headings,"formal_signals":formal,"status_signals":statuses,"todo_open_signals":todos,"relative_refs":refs})
    for r in records:
        for ref in r["relative_refs"]:
            if ref["target"] not in all_paths: broken.append({"source":r["path"],**ref})
    duplicates=[{"sha256":h,"paths":ps} for h,ps in hashpaths.items() if len(ps)>1]
    md=[r for r in records if r["path"].lower().endswith(".md")]
    canonical=("readme","current","architecture","kernel","contract","policy","manifest","registry","index","state","ledger","audit")
    orphans=[]
    for r in md:
        if inbound[r["path"]]==0 and not any(t in Path(r["path"]).name.lower() for t in canonical):
            orphans.append({"path":r["path"],"placement":r["placement"],"lines":r["lines"],
                            "formal_signal_count":len(r["formal_signals"]),"status_signal_count":len(r["status_signals"]),
                            "open_signal_count":len(r["todo_open_signals"])})
    out={"schema":"FULL_CORPUS_CONTENT_AUDIT/v1","text_files_scanned":len(records),"markdown_files_scanned":len(md),
         "total_lines_scanned":sum(r["lines"] for r in records),"placement_counts":dict(Counter(r["placement"] for r in records)),
         "broken_relative_links":broken,"exact_content_duplicates":duplicates,"unlinked_markdown_candidates":orphans,"records":records}
    op=Path(args.out); op.parent.mkdir(parents=True,exist_ok=True); op.write_text(json.dumps(out,indent=2),encoding="utf-8")
    op.with_suffix(".md").write_text(
        "# Full Corpus Content Audit\n\n"+
        "\n".join([
          f"Text files scanned: {out['text_files_scanned']}",
          f"Markdown files scanned: {out['markdown_files_scanned']}",
          f"Total lines scanned: {out['total_lines_scanned']}",
          f"Broken relative links: {len(broken)}",
          f"Exact duplicate groups: {len(duplicates)}",
          f"Unlinked Markdown candidates: {len(orphans)}"
        ])+
        "\n\nDetection evidence only. Source material is not automatically deleted, moved, superseded, or promoted.\n",
        encoding="utf-8")
    print(json.dumps({"text_files_scanned":len(records),"markdown_files_scanned":len(md),"total_lines_scanned":sum(r["lines"] for r in records),
                      "broken_relative_links":len(broken),"exact_content_duplicates":len(duplicates),"unlinked_markdown_candidates":len(orphans)}))

if __name__=="__main__": main()
