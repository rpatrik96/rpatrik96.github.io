---
title: 'Pearls of Causality #10: Interventions and Identifiability'
date: 2021-11-29
permalink: /posts/2021/11/2021-12-06-poc10-interventions-and-identifiability.html
tags:
  - causality
  - Pearl
  - intervention
  - identifiability
---

Hitting the nail on its arrowhead, a.k.a. when does $X$ cause $Y$?

### PoC Post Series
- [PoC #9: Potential, Genuine, Temporal Causes and Spurious Association](/posts/2021/11/poc9-causes/)
- ➡️ [PoC #10:  Interventions and Identifiability](/posts/2021/12/poc10-interventions-and-identifiability.html/)

# Interventions

We will revisit interventions in this post. As discussed in [PoC #4](/posts/2021/11/poc4-causal-queries/), interventions can provide more information than observational data only. How does this "more information" look like? Recall that for interventions we need a DAG besides the joint. When we intervene, we modify the DAG by removing the incoming edges of the intervened node. This has an effect on the Markov factorization - this can be expressed in multiple ways, each offering a different interpretation.



## Causal Effect with do-calculus

First, let's define a causal effect with do-calculus.

> Given disjoint sets of variables, $X$ and $Y$, the **causal effect** of $X$ on $Y$ is denoted by $P(y \| do(X=x))$. It gives the probability of $Y = y, \forall x$ in the SEM with all incoming edges and the equation $x = f(pa_x, u_x)$ deleted and setting $X = x$ in the remaining equations.

This definition contains nothing new to us, it uses the do-notation to express the probability of $Y$ when we intervene on $X$. There are multiple ways to calculate and to conceptualize this causal effect, as we will see in the next sections.

## Interventions as Variables

We can think of interventions $do(Xi = x_i')$ in a DAG with variables $X_1, \dots, X_n$ as if we flipped a switch to make $X_i := x_i'$. That is, there are two mechanisms to determine the value of $X_i$: the conditional $P(x_i|pa_i)$ and the intervention $do(Xi = x_i')$. Of course, this has the same effect, it only differs in interpretation. The main advantage of this approach is that we can explicitly incorporate the intervention in a single DAG.

To be able to do this, we augment the DAG network with an additional parent $F_i$, yielding  $Pa_i' = Pa \bigcup \{F_i\}$, where $F_i \in \{do(X_i = x_i'), idle\}$ - meaning that $F_i$ is the "switch between the two mechanisms" determining $X_i$.

The intervention is encoded via the added edge $F_i \rightarrow X_i$, yielding the conditional

$$P\left(x_i | pa_i'\right) = \begin{cases}P(x_i | pa_i), F_i =idle \\
0, F_i = do(X_i = x_i') \wedge x_i \neq x_i' \\
1, F_i = do(X_i = x_i') \wedge x_i = x_i'
\end{cases}$$

The reason why we need to differentiate between $x_i \neq x_i'$ and $x_i = x_i'$ in the case of the intervention is to remain consistent (as if we set $X_i$ to $x_i'$ then all $x_i\neq x_i'$ has 0 probability).

## Interventions as Truncated Factorization
Having discussed the effect of an intervention, we can now express the joint distribution in the case of the intervention $do(X_i = x_i')$. The straightforward way is to start from the Markov factorization $\prod_{j} P(x_j\|pa_j)$ and leave out the factor $P(x_i \| pa_i)$.

$$P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) = \begin{cases}\prod_{j\neq i} P(x_j|pa_j), x_i = x_i' \\
0, x_i \neq x'_i
\end{cases}$$

> This expression shows the [ICM Pinciple](/posts/2021/10/poc1-dags-d-sep/) at work: only the mechanisms intervened on changes, everything else remains the same.


## Interventions and the Preinterventional Distribution
It's also interesting to figure out the relationship between the interventional and the original (preinterventional) distribution. The expression follows from the truncated factorization by extending the expression with $\frac{P(x_i'\|pa_i)}{P(x_i'\|pa_i)}$. The nominator will be the joint distribution before the intervention $P\left(x_1, \dots, x_n\right), x_i = x_i'$- thus the name _preinterventional_ distribution. The denominator will be factor $P(x_i'\|pa_i)$. Note that we need to tie $x_i = x_i'$, as otherwise the expression would be inconsistent with $do(X_i = x_i'$).

$$P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) = \begin{cases}\dfrac{P\left(x_1, \dots, x_n\right)}{P(x_i'|pa_i)}, x_i = x_i' \\
0, x_i \neq x'_i
\end{cases}$$

>Besides satisfying our intrinsic strive for mathematical diversity and beauty, this expression makes the difference clear between interventions and conditioning (except when intervening on leaf nodes - i.e., when $Pa_i = \emptyset$ -, where $P(x_i'\|pa_i=\emptyset) = P(x_i\|pa_i=\emptyset, do(X_i = x_i')=P(x_i'))$ -, when both are the same).

---
An example would be great here
----
In standard Bayes conditionalization, each excluded point $(x_i \neq x'_i)$ transfers its mass to the entire set of preserved points through renormalization. 
In the interventional case, each excluded point transfers its mass to a select set of points that share the same value of $pa_i$ .

## Interventions as Conditioning
$$P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) = \begin{cases}P\left(x_1, \dots, x_n|x_i',pa_i\right)P(pa_i), x_i = x_i' \\
0, x_i \neq x'_i
\end{cases}$$


## Compound Interventions

$$P\left(x_1, \dots, x_n | do(S=s)\right) = \begin{cases}\prod_{i : X_i \not\in S}P(x_i|pa_i), X \mathrm{\ consistent\ with\ } S\\
0, \mathrm{otherwise}
\end{cases}$$

# Adjustment for Direct Causes
> Let $PA_i$ the set of direct causes (parents) of $X_i$ , and $Y$ be any set, disjoint of $\{X_i \bigcup PA_i\}$. The effect of the intervention $do(X_i = x_i') $ on $Y$ is

$$P\left(y | do(X_i=x'_i)\right) = \sum_{pa_i}P(y|x_i',pa_i)P(pa_i)$$

# Identifiability of Causal Effects 

## Identifiability

> Let $Q(M)$ be any computable quantity of a model $M$. $Q$ is identifiable in a model class $\mathcal{M}$ if, for any model pairs $M_1,M_2 \in \mathcal{M}$ $Q(M_1) = Q(M_2)$ whenever $P_{M_1}(v) = P_{M_2}(v)$. 

If observations are limited and permit only a partial set of features  $F_M$(of $P_{M}(v) $) to be estimated, $Q$ is identifiable from $F_M$ if 
$Q(M_1) = Q(M_2)$ whenever $F_{M_1} = F_{M_2}$. 

##  Causal Effect Identifiability

>The causal effect of $X$ on $Y$ is identifiable from a graph $G$ if  $P(y | do(X=x))$ can be computed uniquely from any positive probability of the observed variables, i.e $P_{M_1}(y | do(X=x))=P_{M_2}(y | do(X=x))$ for every pair of modeIs $M_1$ and $M_2$ with $P_{M_1}(v) = P_{M_2} (v) > 0$ and $G (M_1) = G (M_2) = G$.


The identifiability of $P(y | do(X=x))$ ensures inferring the effect $do(X = x)$ on $Y$ from:
passive observations, given by $P(v)$; and
the causal graph $G$, which specififies (qualitatively) the mechanisms/parent-child relationships

## Causal Effect Identifiability in Markovian Models
> In a Markovian causal model  $M = <G, \theta_G>$ with a subset $V$ of all variables being observed, the causal effect $P(y|do(X=x)$ is identifiable whenever $\{X\bigcup Y\bigcup Pa_X\}\subseteq V$



When all variables are measured. In this case, the causal effect can be calculated via the truncated factorization.