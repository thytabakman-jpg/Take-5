"""Self-contained foundation registry for takeover readiness.
No runtime dependency on the predecessor repository.
"""
FOUNDATION={
"semantic_algebra":"T=<K,S,O,G,M,C,R,U>",
"controller":"KPD->Obligations->Package->ModeCube->DelegateExecute->Verify->TRC->Reenter",
"configured_run":"Envelope->Round->Closure->Update->HFReentry->ExternalEscape",
"mode_cube":("EXPAND","CONTRACT","OBSERVE","ACT","DECOUPLED","COUPLED"),
"terminal":("RELATIVE_CLOSE","OPEN","BLOCKED"),
"authority_rule":"admission/evidence/persistence do not grant authority",
"execution_rule":"available!=selected!=bound!=dispatched!=started!=executed!=captured!=consumed",
"currentness_rule":"local preservation + obligation equivalence + dependent revalidation",
"historical_scope":"CAP001-CAP033 recovered ledger",
"behavior_scope":"B01-B58",
"capability_scope":"C01-C49",
}
def self_contained():
    text=" ".join(str(v) for v in FOUNDATION.values())
    return "Reaserch/" not in text and "thytabakman-jpg/Reaserch" not in text
