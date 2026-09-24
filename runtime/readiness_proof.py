"""Readiness proof is a conjunction of independently evidenced gates."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReadinessProof:
    architecture_current:bool
    configured_tools_complete:bool
    runtime_independent:bool
    regression_passed:bool
    closed_loop_passed:bool
    dump_passed:bool
    no_fresh_work:bool
    no_blocking_open:bool
    history_certified:bool
    migration_authorized:bool=False

    @property
    def foundation_ready(self):
        return all((
            self.architecture_current,self.configured_tools_complete,self.runtime_independent,
            self.regression_passed,self.closed_loop_passed,self.dump_passed,
            self.no_fresh_work,self.no_blocking_open,self.history_certified,
        ))

    @property
    def migration_ready(self):
        return self.foundation_ready and self.migration_authorized
