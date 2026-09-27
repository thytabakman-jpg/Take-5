# Sigma / Router Equation Recovery 001

Date: 2026-09-27
Status: RECOVERY + AUDIT; preserves candidates without silently promoting them
Purpose: prevent loss of the September 24 equation sequence and distinguish the remembered choosing equation from surrounding Sigma/state mathematics.

## Recovered conversational clue

On 2026-09-24 the user identified the visually large Greek symbol as capital Sigma (Σ), described as the symbol that "kind of looks like an E."

Later in the same recovered sequence the user described the desired equation as the one that was "making its own choices" and helping Improvement Core figure out what to do with a difficult problem.

## Strongest match to the choosing equation

\[
R_K(s)
=
ND_{\preceq_R}
\{q\in Q_K(s):Elig_K(s,q)\}.
\]

Canonical shorthand recovered in the repository:

\[
R_K(s)=ND_{\preceq_R}A_R(s).
\]

Interpretation:
1. construct the currently eligible action/configuration set;
2. compare eligible candidates under the declared partial preference/leverage relation;
3. retain the nondominated/maximal frontier;
4. do not invent a scalar winner when several incomparable candidates survive.

This is the recovered equation that actually performs choice/routing.

## Sigma equation immediately surrounding the remembered sequence

Historical captured form:

\[
\Sigma_K
=
Hist_K/\!\sim^S_K.
\]

This models controller state as equivalence classes of histories that cannot be distinguished by protected future behavior.

Later strengthened canonical continuation form:

\[
Q^*_{J,K}
=
Hist_K/\!\equiv_{J,K},
\]

where

\[
h_1\equiv_{J,K}h_2
\iff
\forall p\in P_{J,K},
\quad
Obs_{J,K}(h_1,p)
\approx_{J,K}
Obs_{J,K}(h_2,p).
\]

A representation q is continuation-sufficient exactly when

\[
\ker(q)\subseteq\equiv_{J,K},
\]

and coarsest/minimal exactly when

\[
\ker(q)=\equiv_{J,K}.
\]

## Adaptive controller coupling

The router becomes adaptive when its choice is coupled to generated work, evaluation, persistent state update, and reselection:

\[
q_n\in R_K(S_n),
\]

\[
X_n\in G_{q_n}(K,S_n,I_n),
\]

\[
Y_n=M_{q_n}[O_{q_n}](K,S_n,I_n,X_n),
\]

\[
A_n=C_{q_n}(K,S_n,Y_n),
\]

\[
S_{n+1}=U_K(S_n,q_n,Y_n,A_n,e_n),
\]

then recompute

\[
q_{n+1}\in R_K(S_{n+1}).
\]

This is the mechanism behind the remembered behavior:
result changes state -> changed state changes eligible/preferred choices -> router is recomputed -> next work can differ.

## Fixed-point equation from the same family

A recovered related candidate was

\[
\Sigma^*=F_K(\Sigma^*).
\]

This describes a settled/fixed state, but the recovered conversation evidence points to the router equation, not this fixed-point equation, as the equation the user described as "making its own choices."

## Mathematical audit of the router

The choice rule is mathematically coherent as a partial/set-valued correspondence.

Let

\[
E_s=\{q\in Q_K(s):Elig_K(s,q)\}.
\]

Then the safe router is

\[
R_K(s)=Max_{\preceq_R}(E_s)
\]

when maximal elements exist.

For arbitrary infinite partially ordered candidate spaces, existence is not automatic. The existing repository repair therefore uses:

\[
R_K(s)
=
\begin{cases}
Max_{\preceq_R}(E_s),&Max_{\preceq_R}(E_s)\neq\varnothing,\\
OPEN(NO\_FRONTIER\_EXISTENCE),&\text{otherwise.}
\end{cases}
\]

A finite nonempty eligible set guarantees at least one maximal element.

### What the equation does establish

- set-valued rational routing under explicit eligibility and partial preference;
- preservation of incomparable candidates instead of forcing an unsupported scalar ranking;
- adaptive reselection when state changes and the eligible/preference structure is state-conditioned.

### What it does not establish

- a unique selected action when the frontier contains several elements;
- the correctness or completeness of Elig_K;
- the correctness or completeness of the preference relation \preceq_R;
- automatic discovery of the job, criteria, evidence basis, or action universe;
- global convergence or global optimality.

Those require surrounding controller, observation, evidence, update, and closure mathematics.

## Mathematical audit of the Sigma/continuation quotient

The quotient theorem is valid relative to fixed J, K, continuation universe, protected observation map, and observation equivalence.

For any continuation-sufficient representation q:

\[
q(h_1)=q(h_2)
\Rightarrow
h_1\equiv_{J,K}h_2,
\]

hence

\[
\ker(q)\subseteq\equiv_{J,K}.
\]

Therefore the canonical quotient is the coarsest safe representation, up to isomorphism.

The repository includes a finite partition-refinement fixture. On a finite transition system, partition refinement terminates because each strict refinement increases the number of blocks and the finite partition lattice cannot refine indefinitely.

The general infinite-state/computability problem remains OPEN.

## Failed recent recovery candidates preserved for audit

The following equations appeared in the 2026-09-27 recovery conversation but are not supported as the remembered September 24 target:

\[
S\in Det_\lambda
\iff
\ker(\lambda_S)\subseteq\ker(q)
\]

and related factorization/transversal forms.

\[
Z^*
=
Fix_{\equiv_J}
[U_Q\circ C_Q\circ E_Q\circ G_Q](Z_0).
\]

\[
\rho(\theta,s)
=
(\nu(\theta),\mu(\theta,s)).
\]

They are retained as false-match history, not silently deleted.

## Recovery verdict

Best match to "the equation making its own choices":

\[
\boxed{
R_K(s)
=
ND_{\preceq_R}
\{q\in Q_K(s):Elig_K(s,q)\}
}
\]

The large Sigma clue belongs to the immediately surrounding state/quotient mathematics:

\[
\boxed{
\Sigma_K=Hist_K/\!\sim^S_K
}
\]

and its later stronger continuation-relative form:

\[
\boxed{
Q^*_{J,K}=Hist_K/\!\equiv_{J,K}
}
\]

These objects are related but not identical. The router chooses; the quotient defines what state distinctions need to survive; the update changes state; recomputing the router creates the adaptive loop.
