"""Folder refinery prototype: inventory/identity/duplicate/relation normalization packet.

This is a semantic behavior scaffold. It does not mutate source folders.
"""
from dataclasses import dataclass
from hashlib import sha256

@dataclass(frozen=True)
class FileRecord:
    path:str
    content:str
    role:str|None=None
    referent:str|None=None
    currentness:str|None=None

@dataclass(frozen=True)
class RefineryResult:
    inventory:tuple
    exact_duplicate_groups:tuple
    semantic_review_groups:tuple
    residual:tuple

def refine(records):
    by_hash={}
    by_ref={}
    for r in records:
        h=sha256(r.content.encode()).hexdigest()
        by_hash.setdefault(h,[]).append(r.path)
        if r.referent:
            by_ref.setdefault(r.referent,[]).append(r.path)
    exact=tuple(tuple(v) for v in by_hash.values() if len(v)>1)
    semantic=tuple((k,tuple(v)) for k,v in by_ref.items() if len(v)>1)
    residual=tuple(r.path for r in records if not r.referent or not r.role or not r.currentness)
    return RefineryResult(tuple(r.path for r in records),exact,semantic,residual)
