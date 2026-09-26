"""Authority registry for executable result paths.

Exactly one path is the default protected RESULT path. Alternate facades remain
available for comparison/regression but do not acquire result authority by existence.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResultPath:
    name:str
    module:str
    authority:str
    role:str

PATHS=(
    ResultPath("math_first","math_first_wrapper","DEFAULT_RESULT_AUTHORITY","CURRENT_DEFAULT"),
    ResultPath("recursive_episode","recursive_episode","NO_DEFAULT_RESULT_AUTHORITY","COMPARATOR"),
    ResultPath("inquiry_session","inquiry_session","NO_DEFAULT_RESULT_AUTHORITY","COMPARATOR"),
)

def default_result_path()->ResultPath:
    xs=[p for p in PATHS if p.authority=="DEFAULT_RESULT_AUTHORITY"]
    if len(xs)!=1:
        raise RuntimeError("RESULT_PATH_AUTHORITY_NOT_UNIQUE")
    return xs[0]

def result_path(name:str)->ResultPath:
    return next(p for p in PATHS if p.name==name)
