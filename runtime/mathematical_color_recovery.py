"""Executable recovery check for the mathematical color invariant."""
from mathematical_color_gate import (
    MathStatus,
    canonical_formal_label,
    render_formal_label,
    verify_assistant_response,
)
from tool_run_registry import MATERIAL_TOOLS

REQUIRED_ALIASES={
    "ImproveCore":"ImprovementCore",
    "Improvement Core":"ImprovementCore",
    "HF1":"HF001",
    "HF-001":"HF001",
    "ASSERT":"ASSERT",
    "GOAL":"GOAL",
    "MT":"MT",
    "PD":"PD",
    "Tool Run Closure":"TRC",
    "K_PD":"K_PD",
    "C_TR":"C_TR",
    "Take-5":"TAKE5",
    "IC-028":"IC-028",
}

def validate_color_recovery():
    failures=[]
    for alias,canonical in REQUIRED_ALIASES.items():
        try:
            if canonical_formal_label(alias)!=canonical:
                failures.append(f"ALIAS_DRIFT:{alias}")
        except Exception:
            failures.append(f"ALIAS_MISSING:{alias}")

    for tool_id in MATERIAL_TOOLS:
        try:
            if canonical_formal_label(tool_id)!=tool_id:
                failures.append(f"TOOL_IDENTITY_DRIFT:{tool_id}")
                continue
            rendered=render_formal_label(tool_id,MathStatus.UNRESOLVED)
            verify_assistant_response("Current "+rendered+" remains unresolved.")
            try:
                verify_assistant_response("Current "+tool_id+" remains unresolved.")
            except Exception:
                pass
            else:
                failures.append(f"PLAIN_TOOL_BYPASS_OPEN:{tool_id}")
        except Exception as exc:
            failures.append(f"TOOL_COLOR_PATH_FAILED:{tool_id}:{type(exc).__name__}")

    return {"status":"PASS" if not failures else "FAIL","failures":tuple(failures)}

if __name__=="__main__":
    out=validate_color_recovery()
    print(out)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
