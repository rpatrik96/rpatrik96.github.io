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

The following section discusses the definition in its full technical glory, as those subtleties really make a difference. If you are interested only in the intuitive definition of CBNs (I won't blame you, I promise), use your flux capacitor to jump into the wormhole leading to the [second next section](#definition-intuitive).


#### Definition (Technical)
>A DAG $G$ is a Causal Bayesian Network (CBN) compatible with $P^*$ if and only if the following three conditions hold for every $P(v \|do(X = x) ) \in P^*$:
>1.  $P(v \|do(X = x))$ is compatible with $G$
>2. $P(v_i \|do(X = x) )=1 , \forall V_i \in X$ whenever $v_i$ is consistent with $X = x$ 
>3. $P(v_i \|do(X = x), pa_i )=P(v_i \| pa_i ) , \forall V_i \not\in X$, whenever $pa_i$ is consistent with $X = x$; i.e., each $P(v_i \| pa_i )$ is invariant to interventions not involving $V_i$.

Now let's make sense of the definition. 
1. The first condition means that even after the intervention, $G$ is able to represent $P$. With all the incoming edges into $X$ removed, we will have new independencies in the graph. The reason why this still does not hurt Markov compatibility is that we establish only such independencies that are added to $P(v)$ by the intervention $do(X=x)$. Without changing the distriburtion, there is no guarantee, as by definition $I(G) \subseteq I(P)$ should hold. And increasing only $I(G)$ by adding new independencies could hurt the relationship, but changing both in the same way cannot. 
2. The second condition means that intervening on the _same_ variable as on the left on the conditioning bar (this is the $V_i \in X$ part) collapses it to a point mass. Consistency of $v_i$ and $x$ means that you only get a probability of $1$, when $v_i=x$, i.e., if you set $T=25^\circ C$, then 
$$P(T=t| do(T=25^\circ C)) =  \begin{cases}1, t=25^\circ C\\
0, t\neq 25^\circ C \end{cases}$$
3. The third condition is the most interesting one. It states that when the node $V_i$ is conditioned on its parents $Pa_i$, then **interventions have no effect on the CPD**. The conditions formalize that the intervention cannot be on $V_i$ (in that case the parent cannot screen off the effect). The consistency requirement of the assignments $X=x$ and $Pa_i = pa_i$ ensure that the scenario is admitted by $P$. That is, the condition only holds for such $x, pa_i$ combinations that have nonzero probability. 

#### Definition (Intuitive)
> A DAG $G$ is a Causal Bayesian Network (CBN) compatible with $P^*$ if and only if the following three conditions hold for all distributions $\in P^*$:
> 1. Each $P \in P^*$ is compatible with $G$
> 2. Intervening on variable $X$ with $do(X=x)$ makes that event certain, i.e., $P(X=x \|do(X=x)) = 1$
> 3. When conditioning on the parents of a node $X$, interventions (not on $X$) have no effect on the CPD $P(X | Pa_X)$.


#### Consequences
Although the definition does a great job hiding its goodies, we cannot be stopped uncovering them!

Namely, after making an intervention, we will have access to a nice, _truncated_ factorization of $\forall P \in P^*$, i.e.:

$$P(v \|do(X = x)) = \prod_{i : V_i \not\in X} P(v_i \|pa_i ).$$
Again, for $v$ should be consistent with $x$ (only such $v,x$ pairs can occur that have nonzero probability). 

This is particularly pleasing, you might wonder... Actually, it is: this factorization drops (thus the adjective "truncated") all factors from the original distribution that included nodes that are intervened on (i.e., $V_i \in X$). So what remains are $V_i \not\in X$ - remember, as of condition two, when you intervene on $X$, it will be collapsed to a point mass. Multiplying by 1 will not change the product, so those factors can be dropped. As a result, we get a simpler distribution with less parameters.

Although Christmas is quite far away, but CBNs do not suffer from supply chain issues of container ships, so we got shipped two additional properties (disclaimer: these are valid not just during Christmas holidays):


SPLIT PROPERTIES AND EXPLANANTIONS

>1. $P(v_i \|pa_i) = P(v_i \|do(Pa_i = pa_i)) $ - conditioning and intervening on the parents $Pa_i$ of node $V_i$ has the same effect. This is because  ?????
>2. $P(v_i \|do(Pa_i = pa_i, S=s)) = P(v_i \|do(Pa_i = pa_i))$ - intervening on the parents $Pa_i$ of node $V_i$ makes the CPD invariant to interventions on other nodes $S$ (as $Pa_i$ screen off every possible effect of $do(S=s)$ if $S$ belongs to the non-descendants of $V_i$; if $S$ belongs to the descendants, they cannot have any effect, even without intervening on $Pa_i$). If 




### Counterfactual Queries

### Structural Equation Models (SEMs)
- SCMs



![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


# Summary
