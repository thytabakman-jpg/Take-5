from a5_core import ProgramSpec

def test_configured_run_defaults_to_incomplete():
    p=ProgramSpec("X","src","job",("K",),("out",),"fixture",True)
    assert not p.configured_run_complete()

def test_configured_run_requires_all_wrapper_coordinates():
    p=ProgramSpec(
        "X","src","job",("K",),("out",),"fixture",True,
        "RECURSIVE_EPISODE",
        "PACKAGE_OWNER",
        "CROSS_CHILD",
        "FAILURE_MODE_DISTINCT_CHALLENGE",
    )
    assert p.configured_run_complete()


def test_validate_specs_checks_one_shot_iterable_completeness():
    from dataclasses import replace
    from configured_run import validate_specs
    from tool_run_registry import CONFIGURED_RUNS

    valid = CONFIGURED_RUNS["MT"]
    invalid = replace(valid, closure_required=False)
    assert validate_specs(iter([valid]))
    assert not validate_specs(iter([invalid]))
    assert not validate_specs(iter([valid, valid]))
