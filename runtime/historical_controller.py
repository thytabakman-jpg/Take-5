"""Resolve locally migrated historical Improvement Core controllers.

Historical controllers are callable semantic challengers. They do not regain mutation or
promotion authority merely by being invoked.
"""
from dataclasses import dataclass
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"historical_controllers"
ALIASES={
"IC22":"IC022.yaml","IC-022":"IC022.yaml","IC022":"IC022.yaml",
"IC23":"IC023.yaml","IC-023":"IC023.yaml","IC023":"IC023.yaml",
"IC24":"IC024.yaml","IC-024":"IC024.yaml","IC024":"IC024.yaml",
"IC24-G1":"IC024-G1.yaml","IC24-G2":"IC024-G2.yaml","IC24-G3":"IC024-G3.yaml",
"IC28":"IC028_CANONICAL_CURRENT_STATE.md","IC-028":"IC028_CANONICAL_CURRENT_STATE.md","IC028":"IC028_CANONICAL_CURRENT_STATE.md",
}

@dataclass(frozen=True)
class HistoricalController:
    requested:str
    path:Path
    authority:str="challenger_only"

def resolve(name):
    key=name.strip().upper()
    if key not in ALIASES:
        raise KeyError(f"unknown historical controller: {name}")
    path=ROOT/ALIASES[key]
    if not path.exists():
        raise FileNotFoundError(path)
    return HistoricalController(name,path)

def load(name):
    h=resolve(name)
    return h,h.path.read_text()
