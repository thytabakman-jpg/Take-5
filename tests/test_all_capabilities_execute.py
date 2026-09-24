import pytest
from capability_runtime import execute_capability

PAYLOADS={
"C01":{"admissible_typings":["task"]},"C02":{"same_lineage":True},"C03":{"versions":[{"id":"v","authoritative":True}]},
"C04":{"source_id":"s","claim":"c"},"C05":{"target":"t","protected":["p"]},"C06":{"dependencies":[{"availability":"present"}]},
"C07":{"candidate_edges":[{"material":True}]},"C08":{"spines":[["a"]]},"C09":{"edges":[{"relation_type":"depends"}]},
"C10":{"representations":[{"result":1},{"result":1}]},"C11":{"coordinates":[{"id":"x","changed_result":True}]},
"C12":{"sensitivity_maps":[["x"],["x"]]},"C13":{"edges":[{"attribution":"source"}]},
"C14":{"findings":[{"material":True}]},"C15":{"source_effects":["x"],"target_effects":["x"]},
"C16":{"protected":["p"],"candidates":[{"preserves":["p"]}]},"C17":{"failures":[{"mechanism":"m"}]},
"C18":{"causal_chain":[{"evidence":True,"terminal":True}]},"C19":{"seed_frontier":["a"],"graph":{"a":["b"]}},
"C20":{"rivals":[{"id":"r"}]},"C21":{"candidates":[{"id":"c"}]},"C22":{"improvement_frontier":[{"id":"c"}]},
"C23":{"typed_relation":"TRANSFER"},"C24":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},
"C25":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},"C26":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},
"C27":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},"C28":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},
"C29":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},"C30":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},
"C31":{"candidate":{"id":"c"},"protected":["p"],"preserves":["p"]},"C32":{"routes":[{"licensed":True,"reachable":True}]},
"C33":{"strict_gain":True,"preserves":True},"C34":{"protected_before":["p"],"protected_after":["p"]},
"C35":{"candidates":[{"id":"a"},{"id":"b"}]},"C36":{"affected_update":["x"]},"C37":{"provenance_chain":["s"]},
"C38":{"license_disposition":"LICENSED"},"C39":{"target_effect":"CONSTRAIN"},"C40":{"coverage":["x"]},
"C41":{"rescue_disposition":"RESCUED"},"C42":{"transfer_status":"ACCEPT"},"C43":{"handoff":{"target":"x"}},
"C44":{"expected":1,"actual":1},"C45":{"preregistered":True,"pass":True},"C46":{"with_component":1,"without_component":0},
"C47":{"blocking_open":[]},"C48":{"candidates":[{"strict_gain":True,"preserves":True}]},"C49":{"visited":[{"id":"x","task_relevant":True}]},
}

@pytest.mark.parametrize("pid",[f"C{i:02d}" for i in range(1,50)])
def test_every_c_capability_executes(pid):
    out=execute_capability(pid,PAYLOADS[pid])
    assert isinstance(out,dict)
    assert out.get("status") in {"ACCEPT","OPEN","NOOP","FAIL"}
