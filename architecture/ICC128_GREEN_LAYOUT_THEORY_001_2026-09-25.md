# ICC-128 Green Layout Theory 002

Date 2026-09-25
Status CANDIDATE / NON-CANONICAL
Scope output rendering contract

## Purpose

This artifact defines how ICC reconstruction state is rendered.

The prior version failed because it described GREEN and RED with symbols and prose instead of requiring the mathematical characters themselves to carry color.

This version fixes the rendering contract without changing the meaning of GREEN or RED.

## Existing recovery semantics

GREEN keeps its existing meaning.

A mathematical component is GREEN only when its variables, domains, relation or operator, load-bearing conditions, and required GitHub artifact are fully known.

RED keeps its existing meaning.

A mathematical component is RED when mathematical reconstruction remains incomplete.

The renderer does not decide these states. It receives them from the audited object.

## Hard rendering rule

For every smallest mathematically meaningful rendered component, the characters of that component must carry their state color.

Allowed GREEN form:

[
\color{green}{R_{123}}
]

Allowed RED form:

[
\color{red}{G}
]

Not allowed:

- a green square placed before black text;
- a red square placed before black text;
- a whole equation colored because one subcomponent is GREEN;
- a whole box colored because its contents are understood;
- prose saying “this item is green” while the item itself remains black;
- a legend that substitutes for component coloring.

## Smallest-component rule

Color is applied independently to every mathematically meaningful atom.

Example:

[
\color{red}{C_{128}}
(
\color{red}{L},
\color{red}{O},
\color{green}{R_{123}},
\color{green}{D_{PD}},
\color{red}{G},
\color{red}{A},
\color{red}{M_{MT}},
\color{red}{T_2},
\color{red}{E},
\color{red}{V}
)
]

The expression is not assigned one overall color.

## Relation rendering

When a recovered relation is rendered, each mathematical component receives its own color.

Example:

[
\color{green}{ICC128}
\;\color{green}{\rightarrow}\;
\color{green}{ICC123}
\;\color{green}{\rightarrow}\;
\color{green}{R_{123}}
]

This rendering is permitted only when all three components and both displayed relations are already GREEN in the audited source.

If an internal relation is not recovered, do not invent a relation symbol merely to improve layout.

Use indentation or grouping instead.

## Provenance layout

The visual hierarchy distinguishes direct capability ownership from delegated capability supply.

Native capability is displayed directly beneath the tool.

Invoked tool is displayed beneath the parent tool.

Capabilities supplied by an invoked tool are displayed beneath that invoked tool.

This hierarchy is presentation structure. It does not create new mathematics.

## Surface reliability rule

The renderer must use a color-capable representation.

For ChatGPT or MathJax-capable Markdown, use explicit inline or display math color commands such as:

[
\color{green}{x}
]

and

[
\color{red}{x}
]

For GitHub diagrams or any surface where inline math color is not reliably preserved, use an SVG where the text element itself has the required fill color.

Do not fall back to colored status squares.

## SVG fallback rule

In SVG output, the actual text glyph receives the fill property.

GREEN example:

`<text fill="#198754">R₁₂₃</text>`

RED example:

`<text fill="#dc3545">G</text>`

The color belongs to the letters themselves.

## Section structure

The reusable output structure is:

1. Tool identity
2. Core mathematics
3. Native capabilities
4. Invokable tools
5. Capabilities nested under each invoked tool
6. Open reconstruction frontier
7. Provenance and artifact references

These are presentation sections, not mathematical operators.

## Renderer constraint

The renderer may change visual presentation.

It may not change:

- component identity;
- GREEN or RED state;
- capability ownership;
- invocation provenance;
- mathematical relation type;
- artifact provenance.

## Admission rule for the layout itself

Every newly introduced rendering rule in this artifact is explicit and artifact-backed here.

The renderer may display inherited RED components.

It may not introduce a new RED mathematical component.

## Failure test

The renderer fails when any mathematical component that has a GREEN or RED state is displayed in ordinary black text while relying on a nearby square, legend, heading, or prose statement to communicate its state.

That failure invalidates the rendered output.
