---
title: 'Pearls of Causality #4: Causal Queries'
date: 2021-11-01
permalink: /posts/2021/11/poc4-sem/
tags:
  - causality
  - DAG
  - SEM
  - SCM
  - BN
  - Pearl
---

A top-secret guide to d-separation. We will go deep, ready?

### PoC Post Series
- [PoC #3: The properties of d-separation](/posts/2021/10/poc3-d-sep-prop/)
- ➡️ [PoC #4: Causal Queries](/posts/2021/11/poc4-causal-queries/)

# Causal Queries

> Why are doing this thing called "causal inference"?

The obvious answer is that it's fun _(half of the readers now closed the browser tab)_. To set aside joking: because we want to do causal queries, i.e., extract information about the cause-effect relationships between different mechanisms. 

Causal queries have their hierarchy: depending on the available data, we are presented three ways to make inferences:
>1. **Observational**: we put ourselves into the role of the observer, or if you like, the scientist who perceives the world as it is (i.e., in a passive way).
>2. **Interventional**: we put ourselves into the role of the investigator, i.e., the scientist who does the experiments.
>3. **Counterfactual**: we put ourselves into the role of the philosopher (or a toddler always asking why), contemplating what have happened if different conditions would have changed.

This is a clear hierarchy: counterfactual statements carry more information than observational ones, which are more insightful than pure observations.

> Of course, there is no free lunch: to climb the ladder from observational to interventional to counterfactual statements, more elaborate models are require.

In the following, we will dive into the different models used for causal statements. On the way, we will also discuss what an intervention and a counterfactual is.

## Observational Queries

> Observational queries are in terms of the joint distribution.

Making observational queries not even requires causal inference; we can do it based on samples from the joint distribution. That sounds great, but as you might have guessed, there is no free lunch.

> The price we pay for observational queries is their limited expressive power.

As mentioned in my [earlier post](/posts/2021/10/poc2-markov/), the joint distribution contains less information. Namely, multiple graphs (i.e., multiple factorizations of the distribution) can express the same joint. As you remember, in our temperature-altitude example we had two factorizations: $P(A,T) = P(A)P(T\|A)$, and $P(A,T) = P(A\|T)P(T)$. The joint is the same, but the causal meaning is exactly the opposite.

## Interventional Queries
When we want to extract more information than the joint, we need a new tool, i.e., _interventions_. With our shiny new toy, we will be able to infer the DAG. _How cool is that?_

### Interventions

> An intervention means that the value of a (set of) nodes $X$ is set to a specific value $x$, denoted by $do(X=x)$ - this is called _the $do$-notation_.

Importantly, we **need the DAG** to carry out interventions, as it changes the edge structure.

> Intervening on a (set of) nodes $X$ changes the graph by removing all **incoming** edges into $X$.

If we intervene on $X$, then **all of its parents are removed**. This is because by setting $X=x$, we make it independent of its parents. In our example, when we change the temperature by turning up the heat, $T$ will cease to depend on $A$.

> V-structures make no trouble: they obey to interventions as any other node.

Hmmm, there is something where the charm of v-structures is broken. _How deliberating!_

### Causal Bayesian Networks (CBNs)
The notion of intervention brings about some changes in the properties of DAGs, so it makes sense to formalize its effect. This is done by defining **Causal Bayesian Networks (CBNs)**.

#### Notation
I will use the following notation in the definition:
- $V$: a set of nodes (vertices, thus, the $V$)
- $X$ : a set of nodes in $V$ (i.e., $X \subset V$) - note that $X\neq V$, as we need a variable on the left of the conditioning bar
- $P(v)$: the probability distribution over $V$
- $P^*(v) = P(v \|do(X = x) )$: the set of all interventional distributions, including the no intervention, i.e., $P(v)$


#### Definition
>A DAG $G$ is a Causal Bayesian Network (CBN) compatible with $P^*$ if and only if the following three conditions hold for every $P(v \|do(X = x) ) \in P^*$:
>1.  $P(v \|do(X = x))$ is compatible with $G$
>2. $P(v_i \|do(X = x) )=1 , \forall V_i \in X$ whenever $v_i$ is consistent with $X = x$ 
>3. $P(v_i \|do(X = x), pa_i )=P(v_i \| pa_i ) , \forall V_i \not\in X$, whenever $pa_i$ is consistent with $X = x$; i.e., each $P(v_i \| pa_i )$ is invariant to interventions not involving $V_i$.

Now let's make sense of the definition. 
1. The first condition means that even after the intervention, $G$ is able to represent $P$.
2. The second condition means that intervening on the _same_ variable as on the left on the conditioning bar (this is the $V_i \in X$ part) collapses it to a point mass. Consistency of $v_i$ and $x$ means that you only get a probability of $1$, when $v_i=x$, i.e., if you set $T=25^\circ C$, then 
$$P(T=t| do(T=25^\circ C)) =  \begin{cases}1, t=25^\circ C\\
0, t\neq 25^\circ C \end{cases}$$
3.



#### Consequences
This enforces constraints on the space $P^*$.
$$P(v_i \|do(X = x)) = \prod_{i : V_i \not\in X} P(v_i \|pa_i )$$
 , for all $v$ consistent with $x$.

If $G$ is a causal Bayes network, two properties hold:
$P(v_i \|pa_i) = P(v_i \|do(X = pa_i)) $ - every parent set $pa_i$ is exogenous to its child $V_i$ (the conditional probability equals the effect of setting $PA_i=pa_i$ by control).
$P(v_i \|pa_i, s) = P(v_i \|do(X = pa_i)) $ - invariance: controling direct causes $PA_i,$ no other interventions affect $V_i.$





### Counterfactual Queries

### Structural Equation Models (SEMs)
- SCMs



![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


# Summary
