# Question Worth Asking Contract 056

Date: 2026-09-25
Status: CURRENT WORKING DESIGN CANDIDATE

Purpose: formalize the tool whose user-facing question is "What question here is worth asking?"

## Core
Given live question frontier Q under frozen goal g and evidence state z, identify the live question whose answer has the greatest justified expected effect on the goal-relevant continuation.

Each q carries
<id,text,result_sensitivity,information_gain,dependency_unlock,actionability,answer_cost,narrowing_risk,blocked>
with numeric coordinates normalized to [0,1].

Value(q)=result_sensitivity+information_gain+dependency_unlock+actionability
Burden(q)=answer_cost+narrowing_risk
Worth(q)=Value(q)/(1+Burden(q))

A blocked question remains visible but cannot be selected.

## Dominance guard
q is dominated when another answerable question is at least as strong on every benefit coordinate, no worse on every burden coordinate, and strictly better on at least one coordinate.

Let ND(Q) be the nondominated answerable frontier.

Best(Q)=argmax_{q in ND(Q)} Worth(q)

Legal outputs:
SELECTED = exactly one maximizer
TIE = more than one maximizer
OPEN = no answerable question
EMPTY = no live questions

The tool never invents a unique winner from a tie.

## Placement
Observe -> Formalize -> Freeze -> Goal -> Discover Question Frontier -> QuestionWorthAsking -> Ask/Investigate -> Admit Answer -> HF1 -> Reenter

Inside ASSERT*, it can refine INQUIRE's question frontier before expensive investigation. It does not replace INQUIRE because generation and valuation are distinct.

## Reentry
After an admitted answer, regenerate Q and rerun QuestionWorthAsking. The previous winner is not reused automatically.

## OPEN
- empirical calibration of value/burden coordinates
- domain-specific information-gain and answer-cost estimators
- possible lexicographic necessity gates
- exact geometry assignment
- integration with canonical route triggers

## Runtime
runtime/question_worth_asking.py
Configured-run identity: QuestionWorthAsking

Regression requirements:
- dominant question wins
- dominated question cannot win
- ties preserved
- blocked visible but unselected
- zero-cost defined
- empty frontier returns EMPTY
