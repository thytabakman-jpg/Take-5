# ICC-128 Green Layout Theory 001

Date 2026-09-25
Status CANDIDATE / NON-CANONICAL
Scope output-layout theory only

## Purpose

This artifact defines the layout machinery used to render ICC reconstruction outputs.

The layout machinery itself is GREEN by construction.

It does not redefine GREEN.

## Existing GREEN admission rule

A newly introduced layout component is admitted only when all five existing conditions are satisfied.

🟩 variables are fully specified  
🟩 domains are fully specified  
🟩 relation or operator is fully specified  
🟩 load-bearing conditions are fully specified  
🟩 a GitHub artifact exists

Any proposed layout component failing one of those conditions is not admitted into the layout.

## Layout ontology

The layout contains exactly six section types.

🟩 Tool Identity  
Domain: one identified tool or controller object.  
Role: names the object being rendered.  
Load-bearing condition: the identity must resolve to a specific artifact, controller, or historical object.

🟩 Core Mathematics  
Domain: the recovered mathematical representation of that tool.  
Role: displays only mathematics already present in the audited object or already reconstructed elsewhere.  
Load-bearing condition: color is applied at the smallest mathematically meaningful component level. No whole-expression coloring by overall meaning.

🟩 Native Capabilities  
Domain: functions implemented directly by the displayed tool.  
Role: separates direct functionality from delegated functionality.  
Load-bearing condition: a capability appears here only when provenance shows the displayed tool itself implements it.

🟩 Invokable Tools  
Domain: tools that the displayed tool can invoke.  
Role: shows delegation as a parent-child relation.  
Load-bearing condition: the invoked tool is not flattened into the native-capability list.

🟩 Supplied Capabilities  
Domain: capabilities obtained through one specific invoked tool.  
Role: nests those capabilities directly under the tool that supplies them.  
Load-bearing condition: provenance remains visible. A supplied capability is never presented as native unless independent evidence establishes native implementation.

🟩 Open Reconstruction Frontier  
Domain: unresolved components of the audited object.  
Role: displays RED content that belongs to the inspected object.  
Load-bearing condition: RED here is diagnostic content, not a RED layout component.

## Color semantics

The layout machinery is GREEN.

The audited object can contain GREEN and RED components.

Therefore the rendering distinction is:

🟩 layout component = fully specified rendering structure with this GitHub artifact

🟩 audited component = recovered mathematical component satisfying the existing GREEN rule

🟥 audited component = missing, underspecified, ambiguous, conflicting, verbal-only, tool-name-only, or internally unresolved mathematics

No new RED mathematical object is introduced by the layout.

## Provenance rule

Every displayed capability has exactly one displayed provenance class:

🟩 native to the displayed tool

or

🟩 supplied by a named invokable tool

or

🟥 unresolved provenance in the audited object

The layout never silently converts the second or third class into the first.

## Nesting rule

Invoked-tool capabilities are displayed beneath the tool that supplies them.

Example structure:

ICC-128
- Native Capabilities
- Invokable Tools
  - ICC-123
    - Supplied Capabilities
  - PD
    - Supplied Capabilities
  - Goal
    - Supplied Capabilities
  - Architect
    - Supplied Capabilities
  - MT
    - Supplied Capabilities
  - Take Two
    - Supplied Capabilities

This is a presentation hierarchy, not a new mathematical claim about the internal equations of those tools.

## Admission boundary

The layout can render unresolved mathematics, but the layout may not create unresolved mathematics.

Therefore:

- existing RED content can be shown;
- new RED operators, equations, categories, or hierarchy relations cannot be invented;
- any newly introduced layout relation must be fully specified here and backed by this artifact before use.

## Multi-page rule

A rendered ICC output may span multiple pages or sections.

The default order is:

1 Tool Identity
2 Core Mathematics
3 Native Capabilities
4 Invokable Tools with nested Supplied Capabilities
5 Open Reconstruction Frontier
6 Provenance and artifact references

This order is presentation structure only. It does not imply execution order.
