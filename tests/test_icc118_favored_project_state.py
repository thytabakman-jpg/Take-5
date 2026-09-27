#!/usr/bin/env python3
import json
from pathlib import Path
from runtime.project_manager import assess_project, validate_project_package

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/"projects/icc118-favored-variant-recovery/PROJECT_STATE.json"

def run():
    project=json.loads(STATE.read_text(encoding="utf-8"))
    missing,gaps,authority_conflicts,package_conflicts=validate_project_package(project)
    assert missing==()
    assert gaps==()
    assert authority_conflicts==()
    assert package_conflicts==()
    assessment=assess_project(project)
    assert assessment.status=="CLOSED_RELATIVE"
    assert assessment.missing_coordinates==()
    assert assessment.authority_gaps==()
    assert assessment.authority_conflicts==()
    assert assessment.package_conflicts==()
    print("ICC118 favored recovery ProjectManager package: PASS (8/8)")

if __name__=="__main__":run()
