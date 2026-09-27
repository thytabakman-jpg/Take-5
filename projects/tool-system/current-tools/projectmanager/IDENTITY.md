# Identity: ProjectManager

Object ID: ProjectManager
Species: CURRENT_CONFIGURED_TOOL
Status: CURRENT
Aliases: none

## Identity rule

Names are routing labels. Identity is not inferred from lexical similarity,
shared numbering, or equal cardinality of structures.


## Current capability extension

The same ProjectManager identity now accepts two typed control states:

- ProjectDefinitionCandidate
- ManagedProject

This is a sum-type extension of the input domain, not a new ProjectManager identity or alias.
