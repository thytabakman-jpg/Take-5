# Mathematics Model — Mutual Information

Status: LOCKED_RELATIVE FOR CURRENT ROUTE

## Formal object

I(X;Y) = H(X) - H(X|Y)

Equivalent symmetric form:
I(X;Y) = H(Y) - H(Y|X)

Interpretation:
mutual information measures how much learning Y reduces uncertainty about X.

## Classroom model

Target X:
which of eight cards is hidden.

Question answer Y1:
"Is the card striped?"

When the eight-card set is constructed so four are striped and four are not, the answer gives 1 bit of information about X.

Question answer Y0:
"Is the card made of paper?"

When every live card is paper, the answer is always yes.
It gives 0 bits of information about which card is hidden.

## Student contrast

Useful for this target:
an answer that changes the live target possibilities.

Irrelevant for this target:
an answer that leaves the target possibilities unchanged.

## Accuracy boundary

Mutual information is a statistical relationship between variables, not a moral ranking of questions or people.

A question can be interesting but have little information about the chosen target.

The formula remains visible without requiring entropy arithmetic from students.

## Student sentence

"Information is useful for a target when learning it changes what you know about that target."