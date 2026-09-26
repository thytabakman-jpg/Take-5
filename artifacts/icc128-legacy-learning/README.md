# ICC128 Legacy learning reports

This directory is the append-only durable learning ledger for ICC128 Legacy.

Each Legacy run receives one JSON report named by its run ID. A run with no
material learning still receives a report. Failed runs also receive a report.

The reports preserve what the frozen controller learned during a run while the
controller itself starts future runs with fresh ephemeral memory.

Reports are evidence only. They do not mutate or retrain the frozen ICC128 Legacy
snapshot and do not automatically update current ImprovementCore.
