"""Executable dispatch for the complete C01-C49 capability registry."""
from a5_programs import run_orient,run_map,run_attack,run_generic

def execute_capability(program_id,payload):
    n=int(program_id[1:]) if program_id.startswith("C") and program_id[1:].isdigit() else -1
    if 1<=n<=6: return run_orient(program_id,payload)
    if 7<=n<=13 or n==49: return run_map(program_id,payload)
    if 14<=n<=19: return run_attack(program_id,payload)
    if 20<=n<=48: return run_generic(program_id,payload)
    raise KeyError(program_id)
