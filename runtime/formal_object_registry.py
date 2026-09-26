"""Canonical formal-object identity registry for user-visible math/status emission.

Configured tool identities are derived from the live tool registry so adding a
configured tool cannot silently leave the color system behind. Non-tool formal
objects are declared here because they are not represented in tool_run_registry.
"""
from __future__ import annotations
import re
from tool_run_registry import MATERIAL_TOOLS

NON_TOOL_ALIASES={
    "TOOL RUN CLOSURE":"TRC",
    "C_TR":"C_TR",
    "K_PD":"K_PD",
    "KPD":"K_PD",
    "TAKE-5":"TAKE5",
    "TAKE 5":"TAKE5",
    "IC-028":"IC-028",
    "IC 028":"IC-028",
}

MANUAL_ALIASES={
    "IMPROVE CORE":"ImprovementCore",
    "IMPROVEMENT CORE":"ImprovementCore",
    "IMPROVECORE":"ImprovementCore",
    "HF1":"HF001",
    "HF-1":"HF001",
    "HF-001":"HF001",
    "HF 1":"HF001",
    "HF2":"HF002",
    "HF-2":"HF002",
    "HF-002":"HF002",
    "HF 2":"HF002",
}

def _variants(name:str):
    out={name}
    out.add(name.replace("_"," "))
    out.add(name.replace("-"," "))
    # CamelCase readable alias.
    spaced=re.sub(r"(?<=[a-z0-9])(?=[A-Z])"," ",name)
    out.add(spaced)
    return {x.strip() for x in out if x.strip()}

def formal_aliases():
    aliases={}
    for tool in MATERIAL_TOOLS:
        for alias in _variants(str(tool)):
            aliases[alias.upper()]=str(tool)
    aliases.update({k.upper():v for k,v in MANUAL_ALIASES.items()})
    aliases.update({k.upper():v for k,v in NON_TOOL_ALIASES.items()})
    return aliases

FORMAL_OBJECT_ALIASES=formal_aliases()

def canonical_formal_label(label:str)->str:
    normalized=" ".join(label.strip().upper().split())
    if re.fullmatch(r"ICC(?:[- _]?\d+)?", normalized, flags=re.IGNORECASE):
        return normalized.replace(" ","-").replace("_","-")
    value=FORMAL_OBJECT_ALIASES.get(normalized)
    if value is None:
        raise KeyError(label)
    return value

def aliases_by_length():
    return tuple(sorted(FORMAL_OBJECT_ALIASES,key=len,reverse=True))
