# External Architecture Comparison 001

Date 2026-09-24
Status FIRST RESEARCH PASS

## Question

What established architecture research changes the Take-5 foundation before migration?

## Microkernel result

L4 and seL4 support a strong distinction between the privileged minimal mechanism and the larger useful system. seL4 explicitly minimizes the privileged trusted base and moves broader services outside the microkernel. Its assurance story also separates specification, implementation, authority distribution, and system initialization.

Take-5 consequence:
Kernel should not mean all important functionality. The kernel candidate should be minimized around globally privileged invariants and transition/authority mechanisms. Rich operators, planning, memory interpretation, domain workers, and most adaptive policy require positive evidence before kernel admission.

Sources:
- Jochen Liedtke, On micro-kernel construction, SOSP 1995.
- Klein et al., seL4: Formal Verification of an OS Kernel, SOSP 2009.
- seL4 Foundation white paper and verification material.

## Durable workflow result

Temporal separates durable orchestration/history from application workers. Event history permits reconstruction/replay after failure; workflow decisions and side-effecting activities have distinct contracts.

Take-5 consequence:
Persistent event history should be foundational. Controller decisions and substantive workers should remain separable. Replay/reconstruction is stronger than relying on mutable local state. Idempotency/exact execution identity matters for retried actions.

Source:
- Temporal architecture and workflow lifecycle documentation.

## Agent architecture result

ReAct provides evidence for interleaving reasoning, action, observation, and plan update rather than a one-shot plan/execution split.

Generative Agents separates observation/memory, reflection, retrieval, and planning, with ablation evidence that architecture components contribute differently.

Planning surveys organize agent planning around decomposition, plan selection, external modules, reflection, and memory. Recent agent surveys likewise distinguish memory, planning, and tool use.

Take-5 consequence:
The controller loop needs observation-driven reentry and must not collapse memory, planning, tool execution, and evaluation into one semantic-worker object.

Sources:
- Yao et al., ReAct, ICLR 2023.
- Park et al., Generative Agents, UIST 2023.
- Huang et al., Understanding the planning of LLM agents, 2024.
- Li, Review of Prominent Paradigms for LLM-Based Agents, COLING 2025.
- Luo et al., From Storage to Experience, ACL Findings 2026.

## First synthesis

External work independently supports four current Take-5 hypotheses:
1 kernel is narrower than foundation/core;
2 durable history/state and replay deserve first-class treatment;
3 orchestration/controller and workers are distinct;
4 reasoning/planning, action/tool use, memory, and verification benefit from explicit interfaces.

External work also challenges one current simplification:
our state model must distinguish append-only execution/event history from derived current state and higher-level learned/abstracted experience.

This becomes a direct W1-W5 research/build coordinate.
