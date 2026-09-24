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
