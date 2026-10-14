# Take-5 Architecture

**Job:** Orient readers to architecture decisions, mathematical specifications, candidate constructions, and preserved design constraints without treating every historical design as simultaneously governing.

## Start from the authority-bearing surfaces

- [Repository entry](../README.md) — ordered navigation and operating boundaries.
- [Migration state](../MIGRATION_STATE.yaml) and [GitHub governance](../GITHUB_GOVERNANCE.md) — repository-level status and admission rules.
- [Kernel contract](../KERNEL.yaml) — machine-readable protected transition invariants; [Kernel 053 mathematics](KERNEL_MATH_CONTRACT_053.yaml) specifies the current factored design.
- [Jane interface](../runtime/jane.py), [continuity recovery](../runtime/jane_continuity.py), and [current ICC128 handoff](../runtime/jane_icc128_bridge.py) — executable supervisory route and typed controller separation.
- [Canonical foundation](CANONICAL_FOUNDATION_034.md) — admitted foundational distinctions, subject to its exact scope and later binding checks.
- [Kernel math contract](KERNEL_MATH_CONTRACT_053.yaml) — source contract; runtime authority depends on the configured selection.
- [Tool-system project](../projects/tool-system/README.md) — packages, their separate roles, and local authority routing.
- [DesiredJane contract discovery](../runtime/desired_jane.py) is a separately configured tool for recovering the requested Jane role; it is not the runtime Jane supervisor or its governing identity. See [DesiredJane package](../projects/tool-system/current-tools/desiredjane/README.md).
- [Runtime implementations](../runtime/) and [tests](../tests/) — executable and verification surfaces.

## Boundary

A file in this folder may be a proposal, historical analysis, validated design, or current contract. Resolve its own declared status, source version, registered consumers, executable binding and later supersession before treating it as an authority. Do not infer equivalence among designs from names, dates or shared mathematical dimensions. No specifications are migrated or promoted here.
