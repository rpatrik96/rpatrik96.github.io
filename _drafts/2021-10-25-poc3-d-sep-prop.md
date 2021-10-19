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




# Properties of d-separation

![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


## Symmetry
>$X\perp Y \| Z \implies Y\perp X \| Z$

### Proof
$$
\begin{align*}
LHS: P(X|Y,Z) &= P(X|Z) \\
RHS: P(Y|X, Z) &= \dfrac{P(X|Y,Z)P(Y|Z)}{P(X|Z)} \\
              &=_{LHS} \dfrac{P(X|Z)P(Y|Z)}{P(X|Z)} \\
              &= P(Y|Z)
\end{align*}
$$

### Example



## Decomposition
>$X\perp YW \| Z \implies X\perp Y \| Z$

### Proof
$$
\begin{align*}
LHS: P(X|Y,W, Z) &= P(X|Z) \\
RHS: P(X,Y| Z) &= \sum_W P(X,Y,W|Z) \\
               &=_{LHS} P(X|Z)\sum_W P(Y,W|Z)\\
               &= P(X|Z) P(Y|Z)\\
\end{align*}
$$

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




