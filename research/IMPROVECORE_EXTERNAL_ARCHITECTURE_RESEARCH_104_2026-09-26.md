# ImproveCore External Architecture Research 104

Date: 2026-09-26
Status: EXTERNAL EVIDENCE PACKET
Purpose: Give current ImproveCore outside evidence for self-study and strict-gain improvement discovery.

## Sources consulted

### LangGraph persistence
Source: https://docs.langchain.com/oss/python/langgraph/persistence
Observed:
- separates thread-scoped checkpoints from cross-thread durable stores;
- checkpoints support continuity, human-in-the-loop, time travel, and fault tolerance;
- stores support durable information across threads;
- production persistence is distinct from in-memory persistence.

### Temporal durable execution
Sources:
- https://docs.temporal.io/
- https://docs.temporal.io/ai
- https://docs.temporal.io/workflow-definition
- https://docs.temporal.io/child-workflows
Observed:
- workflow event history enables recovery/resumption after process/infrastructure failure;
- nondeterministic external work is separated from deterministic replay logic;
- parent/child workflow semantics and parent-close behavior are explicit;
- AI-agent patterns emphasize durable long-running loops, retries, checkpoints, and human waits.

### AutoGen Core runtime
Source: https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/framework/agent-and-agent-runtime.html
Observed:
- agent runtime owns lifecycle, routing, communication, security boundaries, monitoring, and debugging;
- agent identity/type is distinct from implementation class;
- runtime manages agent instances rather than application code directly;
- runtime has explicit start/idle/stop/close lifecycle.

### OpenAI Agents SDK
Sources:
- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/tracing/
- https://openai.github.io/openai-agents-python/multi_agent/
- https://openai.github.io/openai-agents-python/guardrails/
Observed:
- small primitive set: agents, tools/handoffs, guardrails, sessions, tracing;
- manager-vs-handoff ownership is explicit;
- tracing records end-to-end workflow events, including model calls, tool calls, handoffs, guardrails, and custom events;
- guardrails are explicit workflow-boundary checks;
- sessions provide persistent working context.

### Microsoft Agent Governance Toolkit / Agent Control Specification
Sources:
- https://microsoft.github.io/agent-governance-toolkit/packages/agent-control-specification/
- https://microsoft.github.io/agent-governance-toolkit/packages/agent-runtime/
Observed:
- stateless fail-closed policy checks operate at explicit intervention points;
- runtime supervision separates execution privileges/governance from agent reasoning;
- telemetry can be structured and content-redacted;
- orchestration and policy enforcement are explicit runtime concerns.

### Reflexion
Source: https://arxiv.org/abs/2303.11366
Observed:
- agents can improve across trials using linguistic feedback stored in episodic memory without weight updates;
- feedback can come from external or internally simulated signals.

### Voyager
Source: https://arxiv.org/abs/2305.16291
Observed:
- combines automatic curriculum, an expanding executable skill library, environment feedback, and self-verification;
- composable learned skills reduce repeated reinvention and support lifelong accumulation.

### SWE-agent
Source: https://arxiv.org/abs/2405.15793
Observed:
- agent-computer interface design materially affects agent performance;
- specialized interfaces for navigation, editing, and execution can outperform generic interfaces.

## Questions for ImproveCore

Do not treat outside popularity as proof of strict gain.

Compare these patterns against current ImproveCore and its historical lineages.

Test at least:
1. durable execution checkpoint/event-history/replay;
2. separation of execution checkpoints from cross-run learning memory;
3. structured trace/telemetry export;
4. host capability/adapter discovery instead of manual adapter injection;
5. lifecycle identity and runtime-state semantics;
6. explicit boundary/intervention policy checks;
7. executable reusable skill/capability library;
8. reflective episodic evidence richer than route disposition alone;
9. interface-quality evaluation for tools and host adapters;
10. parent/child cancellation, failure, retry, and resume semantics.

For every candidate classify:
- already present;
- partially present;
- absent but strict-gain candidate;
- redundant;
- conflicting;
- unsupported/open.

Preserve provenance and counterevidence.
