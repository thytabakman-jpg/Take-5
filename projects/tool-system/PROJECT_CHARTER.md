# Tool System Project Charter

Status: CURRENT CANDIDATE
Date: 2026-09-27
Controller: ImprovementCore / ICC organizational migration

## Purpose

Organize the entire Take-5 tool and ICC ecosystem so every current tool and every
known ICC/IC variant has a durable, non-overwriting project package.

## Success state

The project succeeds when:

1. every current registered tool has exactly one project package;
2. every known ICC/IC historical variant or unresolved referent has a separately
   typed package or alias routing;
3. each package has one canonical owner for package-local mutable truth;
4. each package has its own 36-cell Scope x ModeFace coverage surface;
5. the distinct SourceScope x TargetScope 36-cell handoff surface remains
   separately typed;
6. mathematics, runtime, proof, history, current projection, run evidence, and
   coverage evidence cannot silently overwrite one another;
7. evidence, decisions, lessons, runs, and history are append-only;
8. package generation fails closed on an attempted overwrite;
9. CI detects a new current tool without a package or a damaged 36-cell surface;
10. existing authoritative mathematics/runtime artifacts remain intact and are
    referenced rather than copied into a new competing authority.

## Non-goals

This project does not redefine tool mathematics merely to fit the folder layout.
It does not promote historical ICC variants into the current runtime.
It does not collapse aliases or same-number variants without an identity witness.
