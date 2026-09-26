"""Post-repair RootCause recheck for Protected Transition Integrity."""
from __future__ import annotations

from protected_transition_portfolio import audit_protected_transition_portfolio
from root_cause import RootCandidate, run_root_cause_hf2


def run_post_pti_root_recheck():
    portfolio=audit_protected_transition_portfolio()
    if portfolio.status!="PASS":
        return {
            "status":"OPEN",
            "portfolio":portfolio,
            "root_result":None,
            "reason":"INTERNAL_PTI_NOT_CLOSED",
        }

    residual={"HOST_BYPASSES_TAKE5_CONFIGURED_PATH"}
    candidates=(
        RootCandidate(
            "PROTECTED_TRANSITION_INTEGRITY_FAILURE",
            "ROOT_GENERATOR",
            frozenset(residual),
            survives_representation_change=True,
            # The internal PTI repair does not remove an unrelated external host bypass.
            removal_breaks_recurrence=False,
        ),
        RootCandidate(
            "HOST_INTEGRATION_BYPASS",
            "ROOT_GENERATOR",
            frozenset(residual),
            evidence=frozenset({"TAKE5_PTI_PORTFOLIO_PASS","HOST_BOUNDARY_DECLARED_OPEN"}),
            upstream_of=frozenset({"HOST_REASONING_SUBSTITUTES_FOR_CONTROLLER"}),
            survives_representation_change=True,
            removal_breaks_recurrence=True,
        ),
    )
    root=run_root_cause_hf2(
        failure_class=residual,
        candidates=candidates,
        basis_id="POST_PTI_REPAIR_2026_09_26",
    )
    return {
        "status":"PASS" if root.status=="RELATIVE_CLOSE" else "OPEN",
        "portfolio":portfolio,
        "root_result":root,
        "reason":None,
    }


if __name__=="__main__":
    out=run_post_pti_root_recheck()
    printable={
        "status":out["status"],
        "portfolio_status":out["portfolio"].status,
        "portfolio_checked":out["portfolio"].checked,
        "root_candidates":() if out["root_result"] is None else out["root_result"].root_candidates,
        "root_status":None if out["root_result"] is None else out["root_result"].status,
    }
    print(printable)
    raise SystemExit(0 if out["status"]=="PASS" else 1)
