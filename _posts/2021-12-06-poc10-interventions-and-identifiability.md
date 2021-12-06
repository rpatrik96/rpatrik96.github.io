---
title: 'Pearls of Causality #10: Interventions and Identifiability'
date: 2021-12-06
permalink: /posts/2021/11/2021-12-06-poc10-interventions-and-identifiability.html
tags:
  - causality
  - Pearl
  - intervention
  - identifiability
---

Interventions in disguise.

### PoC Post Series
- [PoC #9: Potential, Genuine, Temporal Causes and Spurious Association](/posts/2021/11/poc9-causes/)
- ➡️ [PoC #10:  Interventions and Identifiability](/posts/2021/12/poc10-interventions-and-identifiability.html/)

# Interventions

We will revisit interventions in this post. As discussed in [PoC #4](/posts/2021/11/poc4-causal-queries/), interventions can provide more information than observational data only. How does this "more information" look like? Recall that for interventions we need a DAG besides the joint distribution. When we intervene, we modify the DAG by removing the incoming edges of the intervened node. This has an effect on the Markov factorization, which can be expressed in multiple ways, each offering a different interpretation.

Before we start, let me share a quote with you from Jonas Peter's [lecture on causality](https://www.youtube.com/watch?v=zvrcyqcN9Wo&ab_channel=BroadInstitute) at MIT in 2017. He calls this MUTE, the Most Useful Tautology:
> If we intervene only on $X$, we intervene only on $X$.

This will help us as MUTE means that all other conditional distributions will not change, so it is not hopeless to calculate interventional distributions from observational data. Believe me, you will see it soon.


## Causal Effect with do-calculus

First, let's define a causal effect with do-calculus.

> Given disjoint sets of variables, $X$ and $Y$, the **causal effect** of $X$ on $Y$ is denoted by $P(y \| do(X=x))$. It gives the probability of $Y = y, \forall x$ in the SEM with all incoming edges of the node $X$ and the equation $x = f(pa_x, u_x)$ _deleted_ and setting $X = x$ in the remaining equations.

This definition contains nothing new, it uses the $do$-notation to express the probability of $Y$ when we intervene on $X$. There are multiple ways to calculate and to conceptualize this causal effect, as we will see in the next sections.

## Interventions as Variables

We can think of interventions $do(X_i = x_i')$ in a DAG with variables $X_1, \dots, X_n$ as if we flipped a switch to make $X_i := x_i'$. That is, there are two mechanisms to determine the value of $X_i$: the conditional $P(x_i\|pa_i)$ and the intervention $do(Xi = x_i')$. Of course, the ther-are-two-mechanisms-view has the same effect, it only differs in interpretation. The main advantage being that we can explicitly **incorporate the intervention in a single DAG**; i.e., no need to mess around with deleting edges.

To do this, we augment node $X_i$ in the DAG with an additional parent $F_i$, yielding  $Pa_i' = Pa \bigcup \{F_i\}$, where $F_i \in \{do(X_i = x_i'), idle\}$ - meaning that $F_i$ is the "switch between the two mechanisms" determining $X_i$.

The intervention is encoded via the added edge $F_i \rightarrow X_i$, yielding the conditional

$$P\left(x_i | pa_i'\right) = \begin{cases}P(x_i | pa_i), \ \ \qquad\quad \mathrm{if} \ \ F_i =idle \\
0, \qquad\qquad\qquad\quad \mathrm{if} \ \ F_i = do(X_i = x_i') \wedge x_i \neq x_i' \\
1, \qquad\qquad\qquad\quad \mathrm{if} \ \ F_i = do(X_i = x_i') \wedge x_i = x_i'
\end{cases}$$

The reason why we need to differentiate between $x_i \neq x_i'$ and $x_i = x_i'$ in the case of the intervention is to remain consistent (as if we set $X_i$ to $x_i'$ then all $x_i\neq x_i'$ have 0 probability).

## Interventions as Truncated Factorization
Having discussed the effect of an intervention, we can now express the joint distribution in the case of $do(X_i = x_i')$. The straightforward way is to start from the Markov factorization $\prod_{j} P(x_j\|pa_j)$ and leave out the factor $P(x_i \| pa_i)$. We can do this as by intervening on $X_i$ we have $P(x_i \| pa_i, do(X_i = x_i'))= P(x_i' \| pa_i, do(X_i = x_i'))=1$

$$P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) = \begin{cases}\prod_{j\neq i} P(x_j|pa_j), \quad \mathrm{if} \ \ x_i = x_i' \\
0,  \qquad\qquad\qquad\quad \mathrm{if} \ \  x_i \neq x'_i
\end{cases}$$

> This expression shows the [ICM Pinciple](/posts/2021/10/poc1-dags-d-sep/) at work: only the mechanisms intervened on changes, everything else remains the same.

### Compound Interventions

This notation can also handle **compound interventions**, i.e., when we intervene on multiple variables at the same time. If we denote the set of variables we intervene on with $S$, then we can write

$$P\left(x_1, \dots, x_n | do(S=s)\right) = \begin{cases}\prod_{i : X_i \not\in S}P(x_i|pa_i), \qquad\quad \mathrm{if} \ \ X \mathrm{\ consistent\ with\ } S\\
0, \qquad\quad \ \ \mathrm{otherwise}
\end{cases}$$



## Interventions and the Preinterventional Distribution
It's also interesting to figure out the relationship between the interventional and the original _(preinterventional)_ distribution. The expression follows from the truncated factorization by extending the expression with $\frac{P(x_i'\|pa_i)}{P(x_i'\|pa_i)}$ and then noticing that we have all factors of the joint in the nominator. The nominator will be the joint distribution _before the intervention_ $P\left(x_1, \dots, x_n\right), \mathrm{s.t.} \ x_i = x_i'$ - thus the name _preinterventional_ distribution. The denominator will be the actor $P(x_i'\|pa_i)$. Note that we need to tie $x_i = x_i'$, as otherwise the expression would be inconsistent with $do(X_i = x_i'$).

$$P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) = \begin{cases}\dfrac{P\left(x_1, \dots, x_n\right)}{P(x_i'|pa_i)}, \ \qquad\quad \mathrm{if} \ \ x_i = x_i' \\
0, \qquad\qquad\qquad\qquad\quad \mathrm{if} \ \ x_i \neq x'_i
\end{cases}$$

>Besides satisfying our intrinsic strive for mathematical diversity and beauty, this expression makes the difference clear between interventions and conditioning. Except when intervening on leaf nodes - i.e., when $Pa_i = \emptyset$ -, where $P(x_i'\|pa_i=\emptyset) = P(x_i\|pa_i=\emptyset, do(X_i = x_i'))=P(x_i')$ -, when both are the same (cf. Causal Bayesian Networks in [PoC #4](/posts/2021/11/poc4-causal-queries/)).


When conditioning on $X_i = x_i'$, then what we do can be thought as a two-step process:
1. **Reduction** of the probability distribution (dropping the entries in the joint inconsistent with $X_i \neq x'_i$).
2. **Renormalization** of the probabilities to get a distribution.

> This means that conditioning distributes the probability mass over **all remaining values** (i.e., where in the joint we have $X_i = x_i'$) **equally** in the sense that the same normalizing factor is applied in each case. 

The situation could not have been more different when we intervene on $X_i$.

>In the interventional case, each excluded point (where $x_i \neq x_i'$) transfers its probability to a **subset of points** sharing the same value of $pa_i$. That is, depending on $pa_i$, **different normalization constants** are applied.

### Example
Assume that we have a graph $X\rightarrow Y\rightarrow Z$ with all variables being binary. We need to ensure that the conditional independence hold in the joint distribution (to ensure that the Markov factorization is the one implied by the graph, or more precisely, that the graph is a perfect I-map), we need the marginal for $X$:

| $X$ | $P(X)$ |
|-----|---------|
| $0$ | $0.6$   |
| $1$ | $0.4$   |

The second ingredient is the conditional for $Y$ ensuring $P(Y\|X) = P(Y\|X,Z)$:

| $X$ | $Y$ | $P(Y\|X)$ |
|-----|-----|---------|
| $0$ | $0$ | $0.8$     |
| $0$ | $1$ | $0.2$     |
| $1$ | $0$ | $0.5$     |
| $1$ | $1$ | $0.5$     |

And the third one is the conditional for $Z$ ensuring $P(Z\|Y) = P(Z\|X,Y)$:

| $Y$ | $Z$ | $P(Z\|Y)$ |
|-----|-----|---------|
| $0$ | $0$ | $0.9$     |
| $0$ | $1$ | $0.1$     |
| $1$ | $0$ | $0.3$     |
| $1$ | $1$ | $0.7$     |

That is, the probabilities populate the following table with eight entries:

|  $X$ | $Y$  | $Z$ |  $P(X,Y,Z)$ | $P(X,Y,Z\|Y=1)$| $P(X,Y,Z\|do(Y=1))$| 
|---|---|---|---|---|---|
| $0$ | $0$ |  $0$ | $0.432$  | $0$ | $0$ |   
| $0$ | $0$ |  $1$ | $0.048$  | $0$ | $0$ |   
| $0$ | $1$ |  $0$ | $0.036$ | $0.036/0.32=0.1125$ | $0.036/0.2=0.6*0.3=0.18$ |   
| $0$ | $1$ |  $1$ | $0.084$ | $0.084/0.32=0.2625$ | $0.084/0.2=0.6*0.7=0.42$ |   
| $1$ | $0$ |  $0$ | $0.18$ | $0$ | $0$ |   
| $1$ | $0$ |  $1$ | $0.02$ | $0$ | $0$ |   
| $1$ | $1$ |  $0$ | $0.06$ | $0.06/0.32=0.1875$ | $0.06/0.5=0.4*0.3=0.12$ |   
| $1$ | $1$ |  $1$ | $0.14$ | $0.14/0.32=0.4375$ | $0.14/0.5=0.4*0.7=0.28$ |   

We can calculate the marginal for $P(Y=1) = 0.036+0.084+0.06+0.14 =0.32$ that we will need for calculating interventions from the preinterventional distribution. I included in the fourth column _(you thought a CS guy will start indexing from 1?)_ the probabilities when conditioning on $Y=1$, whereas the fifth column includes the interventional probabilities (calculated both from the preinterventional distribution and with the truncated factorization).

Notice that in the interventional case, we divide the probabilities with different values (depending on the parent of $Y$, i.e., $X$). A sanity check is that in both the conditioning and interventional cases the probabilities add up to 1.




## Interventions as Conditioning
Although generally intervening on $X_i$ is different from conditioning on $X_i$, we can use conditioning to express the intervention as well.

We start from the joint distribution, then by using the chain rule of Bayesian networks, we "extract" $P(x_i'|pa_i)$ and $P(pa_i$). As the intervention makes $P(x_i'|pa_i) =1$, we can simplify the expression:
$$
\begin{align*}
P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) &= P\left(x_1, \dots, x_n|x_i',pa_i\right)P(x_i'|pa_i)P(pa_i) \\
&= P\left(x_1, \dots, x_n|x_i',pa_i\right)P(pa_i)
\end{align*}
$$

Our manipulation requires that $x_i = x_i'$, so the resulting expression includes two cases:
$$P\left(x_1, \dots, x_n | do(X_i=x'_i)\right) = \begin{cases}P\left(x_1, \dots, x_n|x_i',pa_i\right)P(pa_i), \ \ \quad \mathrm{if} \ \ x_i = x_i' \\
0, \qquad\qquad\qquad\qquad\qquad\qquad\quad \mathrm{if} \ \ x_i \neq x'_i
\end{cases}$$


> If you now focus on the formulas we came up with in this section, you will realize that they express interventions **without** using any interventional distribution. This means that in specific cases, we are able to **calculate the effect of an interventions from observational distributions**.




# Adjustment for Direct Causes
We will use the last formulation - interventions as conditioning - to calculate the effect of an intervention from observational data. This is called **adjustment for direct causes**.

> Let $PA_i$ the set of direct causes (parents) of $X_i$ and $Y$ be any set, disjoint of $\{X_i \bigcup PA_i\}$. The effect of the intervention $do(X_i = x_i') $ on $Y$ is

$$P\left(y | do(X_i=x'_i)\right) = \sum_{pa_i}P(y|x_i',pa_i)P(pa_i)$$

Additionally, we need to marginalize over $Pa_i$ as we are interested in $P\left(y \| do(X_i=x'_i)\right)$. We can use this formula as $Pa_i$ screen off any effect on $X$ coming from other nondescendants of $X$ - i.e., if we know the value $Pa_i = pa_i$, then all other variables do not matter, we have the information to determine the value/distribution for $X$.

# Identifiability of Causal Effects 

We have seen that we can do some black magic with the observational distributions to get the effect of an intervention. However, this is not always possible. In this section, we will get acquainted with the formal notion of identifiability, then discuss conditions for causal effect identifiability.

## Identifiability

**Identifiability** in a general sense states that **some quantity** (intervention, likelihood, mean, etc.) **can be computed uniquely**.

> Let $Q(M)$ be any computable quantity of a model $M$. $Q$ is identifiable in a model class $\mathcal{M}$ if, for any model pairs $M_1,M_2 \in \mathcal{M}$ it holds that $Q(M_1) = Q(M_2)$ whenever $P_{M_1}(v) = P_{M_2}(v)$. 

The definition implies that we have an "identifiability mapping" from probability distributions of models to the space of a quantity $h(M,v) : P_{M}(v) \rightarrow Q(M)$ where the same $P_M(v)$ values map to the same $Q(M)$.

The definition can be extended to the case when there are hidden variables, then we use thr _observed_ subset of $P_M(v)$. 

##  Causal Effect Identifiability

For causal effects, identifiability is defined as follows:

>The causal effect of $X$ on $Y$ is identifiable from a graph $G$ if  $P(y \| do(X=x))$ can be computed **uniquely** from any positive probability distribution of the **observed variables**, i.e $P_{M_1}(y \| do(X=x))=P_{M_2}(y \| do(X=x))$ for every pair of modeIs $M_1$ and $M_2$ with $P_{M_1}(v) = P_{M_2} (v) > 0$ and $G (M_1) = G (M_2) = G$.

Again, uniqueness is the key in the definition - the positivity assumption is required to exclude edge cases (e.g., when dividing by 0). The identifiability of $P(y \| do(X=x))$ ensures inferring the effect $do(X = x)$ on $Y$ from:
1. passive observations, given by the observational distribution $P(v)$; and
2. the causal graph $G$, which specifies (qualitatively) the mechanisms/parent-child relationships

This definition mirrors the adjustment for direct causes, where we used knowledge both from observations and the graph.

## Causal Effect Identifiability in Markovian Models
Looking into a more specialized model class, namely, Markovian Models (where we have a DAG and the noises are _jointly_ independent), we can state the following result:

> In a Markovian causal model  $M = <G, \theta_G>$ with a subset $V$ of all variables being observed, the causal effect $P(y\|do(X=x))$ is identifiable whenever $\{X\bigcup Y\bigcup Pa_X\}\subseteq V$.

We need observability of $X, Y, Pa_X$ to use the adjustment for direct causes. This is required to calculate the quantities in the adjustment formula above.

> When all variables are measured (i.e., when we are _extremeley lucky_), the causal effect can be calculated via the truncated factorization.


# Summary

This post opened up the door into the most intricate details of calculating interventions, discussing various ways and interpretations. At the end, we also touched on the topic on identifiability. 

However, we have not yet covered the case of confounding - an undoubtedly more realistic scenario. You can probably figure out what comes next then.