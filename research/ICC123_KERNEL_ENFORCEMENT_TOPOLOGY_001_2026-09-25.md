# ICC-123 Kernel Enforcement Topology 001

Date: 2026-09-25
Status: RESEARCH CANDIDATE / NO RUNTIME EFFECT
Authority effect: NONE
Source controller: ICC-123 observer-first run
Admission partner: ICC-128
Major-change freeze: PRESERVED

## Observation

The live Take-5 question is not which operating-system or notebook kernel to adopt.

The load-bearing question is:

What enforcement boundary must every authoritative state-changing path cross so protected ICC behavior cannot be bypassed?

The current Take-5 kernel contract primarily specifies laws. Enforcement of those laws is distributed across:
- entry_contract.py;
- activation_bridge.py;
- math_first_wrapper.py;
- tool_run_closure.py;
- emergent_admission.py;
- system_loop.py;
- lineage_state.py;
- research_system.py;
- related controller/state machinery.

Examples of direct mutation surfaces remain outside one unique gate:
- system_loop.py updates current state from IC final packets;
- lineage_state.py applies deltas directly to durable lineage state;
- research_system.py mutates claim/discharge state;
- math_first_wrapper.py delegates persistence to a caller-supplied update_fn.

Therefore the present system has protected invariant mathematics and many guards, but complete mediation by one non-bypassable effect boundary is not yet established.

## External comparison

External systems are evidence, not authority.

### seL4/L4 microkernel principle

The L4/seL4 microkernel criterion tolerates a concept inside the kernel only when moving it outside would prevent required functionality. Higher-level policy belongs outside the privileged minimal mechanism.

Useful transfer:
kernel placement is an externalizability question, not a file-size or naming question.

Source:
https://sel4.systems/About/FAQ.html

### seL4 capability model

seL4 authorizes operations through capabilities that combine object reference with access rights.

Useful transfer:
authority must travel as an explicit unforgeable/effect-limiting grant rather than arise from evidence or discovery.

Source:
https://docs.sel4.systems/Tutorials/capabilities.html

### NIST reference-monitor criterion

NIST describes a reference validation mechanism as always invoked/complete mediation, tamperproof, and sufficiently constrained to support assured analysis and testing. NIST SP 800-160 also makes non-bypassability explicit for trustworthy system control.

Useful transfer:
a protected law is not an effective kernel law merely because it is written centrally. The enforcement mechanism has to dominate every protected effect path.

Sources:
https://csrc.nist.gov/glossary/term/reference_monitor
https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf

### Jupyter provisioner boundary

Jupyter kernel provisioners separate application/kernel-management logic from the concrete environment in which a kernel process is launched and managed.

Useful transfer:
execution substrate should be replaceable behind a typed provisioning interface rather than fused to controller semantics.

Source:
https://jupyter-client.readthedocs.io/en/latest/provisioning.html

## Mathematical reconstruction

Let the effect graph be:

G_E = (V,E)

Let:
- P be nodes that can produce proposed actions/deltas;
- Z be authoritative/persistent state sinks;
- Paths(P,Z) be all executable paths from proposals to protected state effects.

For an enforcement set B subseteq V:

CompleteMediation(B)
iff
for every p in Paths(P,Z), p intersects B.

Equivalently, B is a dominator/cut for every protected mutation sink relative to proposal sources.

Let L be the protected law set.

EffectiveKernel(B,L)
iff
CompleteMediation(B)
AND NonBypassable(B)
AND Enforces(B,L)
AND Verifiable(B,L).

This changes the kernel question from:

How many laws are in K?

to:

Which laws require enforcement at the complete-mediation boundary, and does such a boundary actually dominate every authoritative effect path?

## Two objects that were previously conflated

### K_law

K_law is the protected law specification.

The current candidate includes laws for:
- entry/binding;
- identity;
- surface admission;
- transition;
- authority;
- observation;
- freeze;
- execution truth;
- admission;
- OPEN/INCOMPARABLE preservation;
- closure;
- lineage;
- reentry;
- promotion.

### K_exec

K_exec is the privileged effect-validation mechanism.

Its job is not to perform every policy operation. Its job is to mediate every protected authoritative effect.

Candidate contract:

Commit(z,delta,beta,evidence)
is legal only when:
1. target/job/reference continuity is established;
2. requested effect authority is a subset of bound authority;
3. the effect has a typed transition/admission disposition;
4. execution claims have execution evidence when execution is required;
5. OPEN/BLOCKED/INCOMPARABLE states are not silently coerced into success;
6. the resulting state delta is provenance-bearing and reenterable.

No claim is made yet that this list is minimal or complete.

## Architecture constitution is separate

Some protected behavior governs how architecture itself may evolve rather than each ordinary runtime state mutation.

Candidate architecture-constitution content includes:
- Distinct(a,b) does not imply SeparateOperatingSurface(a,b);
- new surfaces require strict gain when an existing view/composition preserves behavior;
- capabilities migrate by demonstrated behavior rather than file identity;
- changing one mathematical factor cannot silently redefine another;
- recovered evidence does not self-authorize;
- successor claims require protected witness preservation;
- major mathematical change is frozen before implementation.

These rules remain load-bearing without automatically belonging inside K_exec.

## Provisioning boundary

Let Pi_e be an execution provisioner for environment e.

Pi_e:
Binding -> <Result,ExecutionReceipt>

Candidate environments can include:
- local Python;
- GitHub Actions;
- notebook/Jupyter execution;
- remote workers;
- future execution substrates.

Controller semantics remain invariant across e when the same binding, authority, result, and receipt contracts are preserved.

The current activation bridge already provides much of the lifecycle vocabulary:

SELECTED
-> BOUND
-> DISPATCHED
-> STARTED
-> EXECUTED
-> RESULT_CAPTURED
-> CONSUMED.

The remaining architectural question is whether execution environments can become genuine replaceable provisioners without weakening effect mediation.

## ICC-123 result

The kernel-selection problem is reframed as an enforcement-topology problem.

Do not replace Take-5 with Linux, Jupyter, seL4, FreeRTOS, or another external kernel.

Do not yet reduce the current 14-law K to a smaller law set.

First establish the state-effect graph and complete-mediation boundary.

## ICC-128 disposition

Disposition:
RESEARCH / ADMISSIBLE_AS_OPEN_ARCHITECTURE_WORK.

Not admitted as runtime architecture.
No kernel equation is replaced.
No current wrapper/controller/Jane behavior is changed.
No production promotion is licensed.

Reentry trigger:
a mutation-surface inventory and dominator analysis that establishes which current state-changing paths are mediated and which can bypass the candidate effect gate.

## Next experiment

E1 enumerate every function/path capable of authoritative or persistent mutation.

E2 type each source and sink:
PROPOSAL,
BINDING,
EXECUTION,
VERIFICATION,
ADMISSION,
AUTHORITATIVE_STATE,
LINEAGE_STATE,
PROJECT_LOCAL_STATE,
DERIVED_VIEW.

E3 construct the directed mutation/effect graph.

E4 test whether existing TRC/admission/update machinery dominates every protected sink.

E5 for every bypass path, determine whether:
- the path is legitimate and must be incorporated into K_exec;
- the path is a derived/non-authoritative mutation;
- the path is an architecture defect.

E6 only after E1-E5 run the externalizability test on each K_law invariant.

E7 preserve OPEN where the graph does not discriminate.

## Stopping condition

This research episode closes only when:
- the reframed object is recorded;
- external evidence is separated from authority;
- no runtime/kernel change is made under unresolved enforcement topology;
- the next falsifiable experiment is explicit.

Those conditions are met by this artifact.
