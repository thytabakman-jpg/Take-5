# Runtime pointer: ProjectManager

Current runtime realization is owned by:
- runtime/project_manager.py
- runtime/portable_tool_conductor.py
- current dedicated runtime modules referenced by runtime/tool_manifest.py

This package records organization and source routing only.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.


## Current pre-project branch

runtime/project_manager.py distinguishes ProjectDefinitionCandidate from ManagedProject.
A candidate can reach EXPLORATION_OPEN, DEFINITION_READY, or PROMOTION_READY.
The observer adapter never creates a full project package.
A candidate and a managed project cannot be bound simultaneously as one state.
