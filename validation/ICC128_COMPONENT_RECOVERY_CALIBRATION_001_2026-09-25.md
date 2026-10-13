# ICC-128 Component Recovery Calibration 001

Date 2026-09-25  
Status CANDIDATE / NON-CANONICAL; dated historical calibration, not live tool authority  

**Scope of evidence:** This calibration records an implementation-relative observation at the September 25, 2026 source boundary. The canonical runtime and policy remain the live source files; this record does not promote a candidate theorem or tool, authorize a changed binding, or establish current universal execution correctness. Subsequent code revisions require fresh validation.
Target `runtime/activation_bridge.py`  
Tests `tests/test_activation_bridge.py`

## Recommendation

Use `activation_bridge` as the calibration specimen for component-level reconstruction coloring.

Reason

It has executable code and tests, most of its control relation is explicit, and the remaining unresolved pieces are narrow enough to expose exactly where GREEN must stop.

This corrects the earlier coarse claim that the whole activation bridge can be treated as green.

## Color rule

A component is GREEN only when all five conditions hold

\[
\operatorname{Green}(c)
\iff
V_c\land D_c\land O_c\land C_c\land A_c
\]

where

\[
V_c=\text{variables known}
\]

\[
D_c=\text{domains known}
\]

\[
O_c=\text{operator or relation known}
\]

\[
C_c=\text{load-bearing conditions known}
\]

\[
A_c=\text{GitHub artifact exists}
\]

Otherwise

\[
\operatorname{Red}(c)\iff\neg\operatorname{Green}(c)
\]

## Recovered activation-complete relation

The executable relation in `activation_complete` is

\[
\color{green}{AC}
(
\color{green}{s},
\color{green}{b},
\color{green}{e}
)
\color{green}{\iff}
\]

\[
\color{green}{b.episode=s.episode}
\;\color{green}{\land}\;
\color{green}{b.selection\_id=s.selection\_id}
\;\color{green}{\land}\;
\color{green}{b.program\_id=s.program\_id}
\]

\[
\color{green}{\land}\;
\color{green}{b.authority\_out\subseteq b.authority\_in}
\;\color{green}{\land}\;
\color{green}{e.contract\_id=b.contract\_id}
\]

\[
\color{green}{\land}\;
\color{green}{e.dispatched}
\;\color{green}{\land}\;
\color{green}{e.started}
\;\color{green}{\land}\;
\color{green}{e.executed}
\;\color{green}{\land}\;
\color{green}{e.result\_captured}
\;\color{green}{\land}\;
\color{green}{e.consumed}
\]

The variables are typed in the repository artifacts

\[
\color{green}{s\in Selection}
\]

\[
\color{green}{b\in BindingReceipt}
\]

\[
\color{green}{e\in ExecutionReceipt}
\]

and the Boolean codomain is explicit

\[
\color{green}{AC:Selection\times BindingReceipt\times ExecutionReceipt\to\{0,1\}}
\]

## Recovered binding invariants

The binding operator has the following fully explicit guards

\[
\color{green}{a_{out}\subseteq a_{in}}
\]

\[
\color{green}{t'=t}
\]

\[
\color{green}{j'=j}
\]

\[
\color{green}{p'=p}
\]

\[
\color{green}{obs_{in}=1\Rightarrow obs_{out}=1}
\]

The implementation artifact is `runtime/activation_bridge.py`.  
The executable witnesses are in `tests/test_activation_bridge.py`.

## Remaining RED components

The bridge is not literally all green.

### Environment

\[
\color{red}{environment\in str}
\]

The storage type is known, but the mathematical domain is not. No admissible-environment set, environment semantics, or transition relation is defined.

### Failure stage

\[
\color{red}{failure\_stage\in str\cup\{None\}}
\]

The storage type is known, but the valid failure-stage set and its semantics are not fully specified.

The implementation uses

\[
\color{red}{failure\_stage\neq None}
\Rightarrow
\color{green}{Stage.BLOCKED}
\]

The implication itself is executable, but the left-hand semantic object remains underspecified.

### Stage precedence

The executable ordering is

\[
\color{green}{CONSUMED}
>
\color{green}{RESULT\_CAPTURED}
>
\color{green}{EXECUTED}
>
\color{green}{STARTED}
>
\color{green}{DISPATCHED}
>
\color{green}{BOUND}
\]

when no failure stage exists.

But

\[
\color{red}{>}
\]

is RED if interpreted as a semantic lifecycle order rather than merely Python branch precedence. The code establishes evaluation precedence. It does not independently establish that this is the complete intended lifecycle order.

### Contract identifier semantics

The construction is explicit

\[
\color{green}{contract\_id}
=
\color{green}{episode}
:
\color{green}{selection\_id}
:
\color{green}{program\_id}
\]

The concatenation rule is recovered.

But

\[
\color{red}{ContractIdentity}
\]

remains RED as a broader mathematical object. The artifact does not prove that this string construction is globally injective, canonical across all systems, or sufficient as the complete identity relation.

### Cross-object receipt consistency (additional OPEN guard)

The actual `activation_complete` implementation checks selection/binding episode and selected binding identifiers, and compares execution's `contract_id` with binding. It **does not independently compare** `execution.episode` with `selection.episode`, or revalidate binding target/job equality in the `activation_complete` function. Ordinary `bind` construction enforces the target/job invariants, but receipt objects can also be constructed without `bind`. Do not infer that a green reconstruction of the listed Boolean expression is proof of a comprehensive admission/security contract. This is an **OPEN cross-object validation question**, not a tested exploit or a repair of the runtime.

## Calibration result

The smallest-component audit therefore yields

\[
\boxed{
\text{activation bridge}
=
\text{mostly GREEN}
+
\text{bounded RED frontier}
}
\]

The bounded RED frontier is

\[
\boxed{
\{
\color{red}{EnvironmentSemantics},
\color{red}{FailureStageDomain},
\color{red}{LifecycleOrderSemantics},
\color{red}{GlobalContractIdentity}
\}
}
\]

This is the correct calibration case because it proves both sides of the rule

\[
\text{executable and tested}\not\Rightarrow\text{everything GREEN}
\]

and

\[
\text{unresolved local semantics}\not\Rightarrow\text{whole tool RED}
\]

## Reconstruction transition rule

A RED component may become GREEN only by a separate candidate reconstruction

\[
\color{red}{c}
\rightarrow
c'
\rightarrow
\operatorname{Verify}(c')
\rightarrow
\operatorname{Artifact}(c')
\rightarrow
\color{green}{c'}
\]

The baseline artifact remains unchanged during that process.

## ICC-128 recommendation

Adopt this audit pattern as the calibration standard before applying the same process to MTA, PD, Goal, Architect, or ICC itself.

The next high-value target after calibration is MTA because its unresolved components are precisely the kind this method is designed to expose.

<!-- ICC27_RESEARCH_EXTRACTION_LINK_20261013 -->
## Scientific research extraction (2026-10-13)

[ICC128-06 research packet](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/research/icc-research-web/source-intake/ICC128-06.md) records the reusable source-specific scientific findings, evidence status and falsifiable checks. [Twenty-seven-source research intake](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/research/icc-research-web/source-intake/README.md) links the research web. This source remains the full historical/evidence owner and is not converted into a current runtime or Level certificate.
