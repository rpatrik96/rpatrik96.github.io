---
title: 'Pearls of Causality #3: The properties of d-separation'
date: 2021-10-18
permalink: /posts/2021/10/poc3-d-sep-prop/
tags:
  - causality
  - DAG
  - d-separation
  - Pearl
---


### PoC Post Series
-  [PoC #1: DAGs, d-separation, conditional independence](/posts/2021/10/poc1-dags-d-sep/)
- [PoC #2: Markov Factorization, Compatibility, and Equivalence](/posts/2021/10/poc2-markov/)
- ➡️ [PoC #3: The properties of d-separation](/posts/2021/10/poc3-d-sep-prop/)

# Properties of d-separation

> To be able to leverage the superpowers d-separation gave us, we need to dig deeper. _Much deeper._ 

Namely, when we will be manipulating probability distributions over graphs, one of our main goals will be to simplify things. You probably remember such tricks from math class: making an expression complicated temporarily can give rise to a form that helps us in the long run. 

This is why we need to get familiar with the properties of d-separation (as you remember, there is a correspondence between graphs and probabilities via Markov compatibility).

This post will guide you through the five properties of d-separation. For each property, I will provide an explanation, a proof, and an example. 

>Why the proof?

I am believed that just dropping the property won't get the insight. Besides, seeing the proof will hopefully convince you that I am talking no non-sense. Shall we begin?

![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


## Symmetry
>$X\perp Y \| Z \implies Y\perp X \| Z$

Symmetry is the simplest property, and it won't help us much when manipulating independence statements - as it is only a property of the independence operator. Nonetheless, it is important, for not all operators are symmetric.

Symmetry means that we can exchange the quantities on both sides of the independence symbol "$\perp$" without changing the meaning of the expression.

### Proof
$$
\begin{align*}
LHS: P(X|Y,Z) &= P(X|Z) \\
RHS: P(Y|X, Z) &= \dfrac{P(X|Y,Z)P(Y|Z)}{P(X|Z)} \\
              &=_{LHS} \dfrac{P(X|Z)P(Y|Z)}{P(X|Z)} \\
              &= P(Y|Z)
\end{align*}
$$

In the proof, I start from the Right-Hand Side (RHS) and utilize the Left-Hand Side (LHS) - this is indicated by the "$LHS$" subscript of the equality sign. The goal is to get to the same (or equivalent) expression as on the right of the "$\implies$" symbol ($RHS$), which indicates our conclusion.

> Our general blueprint for the proofs is:
> 1. Accept the statement on the $LHS$ as true.
> 2. Start with an expression not exploiting any prior independence statement.
> 3. Utilize the $LHS$ when manipulating the expression.
> 4. Arrive at an expression equivalent to the $RHS$.

Step 2 is rather vague, I know. What you should keep in mind that we need a starting point that is true when there is no $RHS$. Yes, this sometimes means a lot of trial and error, but I have done that part in advance, so no worries.

In this proof, I started from the conditional $P(Y\|X, Z)$ and applied Bayes' Rule to smuggle in the $LHS$. As you see, this helped to simplify the expression. Indeed, as a result, I got to the desired conclusion.

### Example
In our beloved graph, symmetry means that $E\perp F \| A \implies F\perp E \| A$ and also $F\perp E \| A \implies E\perp F \| A$ (as we can start from any expression).


## Decomposition
>$X\perp YW \| Z \implies X\perp Y \| Z$

Decomposition means that if a variable $X$ is conditionally independent of a _set of variables_ $Y$ and $W$, then it is independent of each (note that in the expression above, the roles of $Y$ and $W$ are interchangeable - as it has no meaning which node we call $Y$ or $W$).

That is, applying decomposition gives us a _more general_ statement.

### Proof
$$
\begin{align*}
LHS: P(X|Y,W, Z) &= P(X|Z) \\
RHS: P(X,Y| Z) &= \sum_W P(X,Y,W|Z) \\
               &= \sum_W P(X|Y,W, Z)P(Y,W|Z)\\
               &=_{LHS} P(X|Z)\sum_W P(Y,W|Z)\\
               &= P(X|Z) P(Y|Z)\\
\end{align*}
$$

This proof is slightly more tricky: namely, we are interested in the relationship between $X,Y$ and $Z$, but the original statement also includes $W$. What can we do? We can introduce $W$ and _marginalize_. Thus, the expression means the same, but has a much nicer (i.e., temporarily more complicated) form. Remember Macchiavelli: the ends justify the means.

By introducing $W$, we can exploit the $LHS$ after applying the chain rule of probability. As $P(X\|Z)$ does not depend on $W$, we can take it out of the sum. As a last step, we sum out $W$ and get the $RHS$ of the property, i.e.  $X\perp Y \| Z$.

### Example


## Weak union
> $X\perp YW \| Z \implies X\perp Y \| ZW$

### Proof
$$
\begin{align*}
LHS: P(X|Y,W, Z) &= P(X|Z) \\
RHS: P(X,Y| W, Z) &= P(X|Y,W,Z)P(Y|W, Z) \\
               &=_{LHS} P(X|Z) P(Y|W, Z)\\
\end{align*}
$$

### Example

## Contraction
>$X\perp Y \| Z  \land X\perp W \| ZY \implies X\perp YW \| Z$


### Proof
$$
\begin{align*}
LHS: P(X|Y, Z) &= P(X|Z) \ \qquad (1) \\
     P(X|Y, W, Z) &= P(X|Y, Z) \quad (2)\\
RHS: P(X,Y, W| Z) &= P(X|Y, W, Z)P(Y,W|Z) \\
               &=_{LHS_2} P(X|Y, Z) P(Y,W|Z)\\
               &=_{LHS_1} P(X|Z) P(Y,W|Z)\\
\end{align*}
$$

### Example

## Intersection (for strictly positive distributions)
> $X\perp W \| ZY  \land X\perp Y \| ZW \implies X\perp YW \| Z$

### Proof
$$
\begin{align*}
LHS: P(X|Y, W, Z) &= P(X|Y, Z) \ \qquad (1) \\
     P(X|Y, W, Z) &= P(X|W, Z) \qquad (2)\\
RHS: P(X,Y, W| Z) &= P(X|Y, W, Z)P(Y,W|Z) \\
               &= \begin{cases} P(X|Y, Z) P(Y,W|Z), \mathrm{when \ using\ } LHS_1\\
               P(X|W, Z) P(Y,W|Z), \mathrm{when \ using\ } LHS_2
               \end{cases} \\
               &\Downarrow \\
               P(X|Y, Z)  &= P(X|W, Z) \quad \forall X, \underline{Y,W,} Z  \\
               P(X|Z)&= P(X|Z)\\
               &\Downarrow \\
               P(X,Y, W| Z) &= P(X|Z)P(Y,W|Z)
\end{align*}
$$

### Example




