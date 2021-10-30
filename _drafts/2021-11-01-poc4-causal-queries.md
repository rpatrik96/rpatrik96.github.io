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

> Why are we doing this thing called "causal inference"?

The obvious answer is that it's fun _(half of the readers now closed the browser tab)_. To set aside joking: because we want to do causal queries, i.e., extract information about the cause-effect relationships between different mechanisms. 

Causal queries have their hierarchy: depending on the available data, we are presented three ways to make inferences:
>1. **Observational**: we put ourselves into the role of the observer, or if you like, the scientist who perceives the world as it is (i.e., in a passive way).
>2. **Interventional**: we put ourselves into the role of the investigator, i.e., the scientist who does the experiments.
>3. **Counterfactual**: we put ourselves into the role of the philosopher (or a toddler always asking why), contemplating what have happened if different conditions would have changed.

This is a clear hierarchy: counterfactual statements carry more information than observational ones, which are more insightful than pure observations.

> Of course, there is no free lunch: to climb the ladder from observational to interventional to counterfactual statements, more elaborate models are require.

In the following, we will dive into the different models used for causal statements. On the way, we will also discuss what an intervention and a counterfactual is.

## Observational Queries

> **Observational queries** are in terms of the joint distribution.

Making observational queries not even requires causal inference; we can do it based on samples from the joint distribution. That sounds great, but as you might have guessed, there is no free lunch.

> The price we pay for observational queries is their limited expressive power.

As mentioned in my [earlier post](/posts/2021/10/poc2-markov/), the joint distribution contains less information. Namely, multiple graphs (i.e., multiple factorizations of the distribution) can express the same joint. As you remember, in our temperature-altitude example we had two factorizations: $P(A,T) = P(A)P(T\|A)$, and $P(A,T) = P(A\|T)P(T)$. The joint is the same, but the causal meaning is exactly the opposite.

## Interventional Queries
When we want to extract more information than the joint, we need a new tool, i.e., _interventions_. With our shiny new toy, we will be able to infer the DAG. _How cool is that?_

### Interventions

> An **intervention** means that the value of a (set of) nodes $X$ is set to a specific value $x$, denoted by $do(X=x)$ - this is called _the $do$-notation_.

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
>A DAG $G$ is a **Causal Bayesian Network (CBN)** compatible with $P^*$ if and only if the following three conditions hold for every $P(v \|do(X = x) ) \in P^*$:
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
> A DAG $G$ is a **Causal Bayesian Network (CBN)** compatible with $P^*$ if and only if the following three conditions hold for all distributions $\in P^*$:
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

>1. $P(v_i \|pa_i) = P(v_i \|do(Pa_i = pa_i)) $ 
>2. $P(v_i \|do(Pa_i = pa_i, S=s)) = P(v_i \|do(Pa_i = pa_i))$ 

The _first property_ tells us that **conditioning and intervening on the parents $Pa_i$ of node $V_i$ yield identical distributions**. This happens because in both cases $Pa_i = pa_i$, and those are the only variables influencing $V_i$.

The _second property_ expresses that **intervening on $Pa_i$  makes the CPD invariant to interventions on $S\neq Pa_i$**. It does not matter whether $S$ is a non-descendant or a descendant of $V_i$: in the former case, $do(Pa_i=pa_i)$ removes any effect of $S$ by deleting the edges from $S$ to $Pa_i$; whereas in the latter case, as only paths in the form of $V_i\rightarrow \dots \rightarrow S$ exist, $S$ cannot have any effect on $V_i$.

#### Why should we care about CBNs?
Even after this long section, you might feel that CBNs are only a formalism with no special purpose. I ensure you that having a common denominator is practical to talk about interventional queries.

> When interested in $P(v_i | do(X=x)),$ Causal Bayesian Networks are the tool describing how to get the interventional distribution from the joint, what the intervened DAG will look like, and they also describe simplifications.

Similar to the properties of d-separation in the [previous post](/posts/2021/10/poc3-d-sep-prop/), CBNs extend our toolbox and increase our self-confidence for handling concepts such as the back-door adjustment, which will be the topic of a future post.

Still, CBNs are not the Holy Grail: they only inform us about the child-parent relationships in a graph. This is sufficient in many cases, but not for counterfactuals.


### Counterfactual Queries

First and foremost: what is a counterfactual?
> A **counterfactual** is a hypothetical query about an event that has not happened, given that the conditions are the same.

Such questions are crucial in medical settings, such as drug trials. Let's assume that after administering a new medication the patient gets healthy. To uncover the _potential_ causal relationship between treatment and healing, clinical investigators are interested in answering the following question: 
>Would the patient be healthy - everything else being equal -  without getting the medication?

The most robust empirical tool, the (possibly double-blind, placebo-controlled) Randomized Control Trial (RCT), is developed to answer counterfactuals. 
But RCTs expensive, enourmously expensive: 
- You need a **control group and a treatment group** (with identical participants in both), 
- You need to engineer a **clever placebo** (a substance without real effect - such as a sugar pill when investigating a medication; this is really hard if you want to investigate e.g. real foods - what tastes, looks, and smells like carrots _without_ being a carrot?)
- You need to be **double-blind** (thus, the placebo), meaning that neither the investigators nor the participants should know who got the treatment and who the placebo (i.e., there is an independent group of researchers, who do not carry out the experiments, but they know the treatment-participant assignment)

Such questions arise several fields, this year's highlight being unequivocally the [Nobel Prize in Economics](https://www.nobelprize.org/prizes/economic-sciences/2021/press-release/). Namely, half of the prize went to _Joshua D. Angrist_ and _Guido W. Imbens_ for _“for their methodological contributions to the analysis of causal relationships”_. Just imagine how hard it is to create an RCT in economics: what is the placebo for a new education/tax policy?

>Counterfactuals provide an alternative to RCTs, but they require to know the **quantitative** relationship between the nodes in the DAG.

To stress the requirement for quantitative relationships, consider the following counterfactual questions:
- How much would the savings rate of households change if the state decreased the capital tax on stock-based personal savings accounts?
- How much would the blood pressure of patients decrease with seven hours of weekly exercise?

CBNs are qualitative models; thus, insufficient: we need **equations.** This is where Structural Equation Models (SEMs) come into play.



### Structural Equation Models (SEMs)
- FIGURE SHOWING NOISE AND X VARIABLES

So we need equations? Here they are:

> A **Structural Equation Model (SEM)** is a set of equations describing the **qualitative relationship** between nodes $X_i$ and their parents $Pa_i$ in the form of:
> $$ x_i = f_i(pa_i, u_i)\qquad  \forall i, $$
> where $u_i$ are the _noise_ variables.

Before looking into $U_i$, let me draw your attention to a key point: a SEM  is a **deterministic** function from the product space of the parents and the exogenous variables to the values of the node.  This is the same idea of representing stochasticity as in VAEs with the [reparametrization trick](https://arxiv.org/abs/1312.6114).

To give you a flavour of what comes next, I might just drop the fact that SEMs are also called **Structural Causal Models (SCMs)**.

#### The zoo of variable names

The _beauty_ of science is that scientists are creative people: they like to give names to concepts, _a lot of names_. We will now discuss them _all_. Hopefully, we won't get lost in the jungle of causal terminology. I am believed that we will get away with some practical insights, so here we go.

The variables $U_i$ have several names: they are called _exogenous, independent, causal, latent, or noise variables_. They are
- **Exogenous:** as they are determined "by nature", i.e. they come "from outside" of the model 
- **Independent:** as they have no parents in the graph - their values are only determined by the (noise) distribution they are sampled from
- **Causal:** as they are the variables that are the cause of the _dependent_ variable $X_i$
- **Latent:** as they are unobserved
- **Noise/disturbance:** as they are usually parametrized as some noise distribution (e.g. Gaussian, Laplacian) - again, recall VAEs and the reparametrization trick.


You guessed it correctly, $X_i$ also have several names: _endogenous, dependent, and observed variables_. They are
- **Endogenous:** as they are determined by the model (the $f_i$ functions), i.e. they are "from inside" of the model
- **Dependent:** as they have parents in the graph - their values are determined by the values of their parents
- **Observed**: as they are the ones we can observe

**Note:** when $X_i$ causes $X_j$, then $X_i$ is also called a "causal variable". So pay attention to the _intent_ of the respective author. _(By the way, did I just ask you to be a mind-reader?)_

#### Assumptions

- MArkovian semi-markovian

- Causal Strcture
- Causal Model

![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


# Summary
