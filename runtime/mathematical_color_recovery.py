"""Executable recovery check for the mathematical color invariant."""
from mathematical_color_gate import (
    MathStatus,
    canonical_formal_label,
    render_formal_label,
    verify_assistant_response,
)

REQUIRED_ALIASES={
    "ImproveCore":"IMPROVECORE",
    "Improvement Core":"IMPROVECORE",
    "HF1":"HF1",
    "HF-001":"HF1",
    "ASSERT":"ASSERT",
    "GOAL":"GOAL",
    "MT":"MT",
    "PD":"PD",
}

def validate_color_recovery():
    failures=[]
    for alias,canonical in REQUIRED_ALIASES.items():
        try:
            if canonical_formal_label(alias)!=canonical:
                failures.append(f"ALIAS_DRIFT:{alias}")
        except Exception:
            failures.append(f"ALIAS_MISSING:{alias}")

    try:
        rendered=render_formal_label("ImproveCore",MathStatus.UNRESOLVED)
        verify_assistant_response("Current "+rendered+" remains unresolved.")
    except Exception:
        failures.append("TYPED_RESPONSE_PATH_FAILED")

    try:
        verify_assistant_response("Current ImproveCore remains unresolved.")
    except Exception:
        pass
    else:
        failures.append("PLAIN_LABEL_BYPASS_OPEN")

    return {"status":"PASS" if not failures else "FAIL","failures":tuple(failures)}

if __name__=="__main__":
    out=validate_color_recovery()
    print(out)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
