---
title: 'Pearls of Causality #7: Latent Structures, Stability, and Inferred Causation'
date: 2021-11-15
permalink: /posts/2021/11/poc7-latents-stability-ic/
tags:
  - causality
  - DAG
  - Latents
  - Pearl
  - Stability
  - Faithfulness
---

DAGs like to play hide-and-seek. But we are more clever.

### PoC Post Series
- [PoC #6: Markov Conditions](/posts/2021/11/poc6-markov-conditions/)
- ➡️ [PoC #7: Latents and Inferred Causation](/posts/2021/11/poc6-latents-stability-ic/)

# Latent Structures

Until now, we lived in an imaginary world with its profound simplicity. But it is time to grow up and face reality. What I am talking about is our imperfect senses. This is not just about illusions, but also about causal inference.

Namely, there will be mechanisms we do not know about (we can call these unknown unknowns). As we don't know they exist, there is not much to do - before Steve Jobs invented the iPhone, people did not know that they _desperately_ need it. Although I enjoy philosophical topics, this post does not lead there; thus, we will discuss only _known unknowns_. That is, **latent-variable models**.

They are known unknowns as we know-or at least, suspect- that there is a mechanism in play, but we cannot observe it. For example, before discovering gravity, mankind only knew that apples fall from trees. In causal terms, gravity $G$ causes apple $A$ to fall down, i.e. $G \to A$. It also makes the Earth $(E)$ rotate around the Sun $(S)$, so $G\to E$ and $G\to S$. Before gravity, we did not know that all these phenomena have an unobserved common cause.

>An **unobserved common cause** of $X,Y$ is $Z$ when $X\leftarrow Z\rightarrow Y$ and $Z$ is not observed. $Z$ is also called a **confounder**.

Before jumping into latent structures, let's summarize the notation:
- $G$: a DAG
- $V$: a set of nodes (vertices, thus, the $V$)
- $O$: the _observable_ subset of nodes in $V$ (i.e., $O\subseteq V$) 
- $P_{[O]}$: observational distribution over $O$
- $\mathcal{P}_{[O]}$: set of observational distributions over $O$
- $\theta_G$: parameters of $G$ in the causal model (these describe the SEM)
- $\mathcal{L}$: a class of latent structures 

>A **latent structure** is a pair $L = <G, O>$ with DAG $G$  over nodes $V$ and where $O\subseteq V$ is a set of observed variables.

So $L$ is a DAG where we attach labels to the nodes that are observed. So far so good. 

>Why do we need latent structures?

Because they can represent our hypotheses about the world. Imagine ourselves in 20th century. We are physicists looking for the secrets of the universe. Some of us might still think that Newtonian physics is the way to go, some of us is a supporter of Einstein's theory of relativity, whereas others believe in [string theory](https://en.wikipedia.org/wiki/String_theory). Each of us can observe the same, but our mental model is different. I.e., we have a class of latent structures.

>How can we compare latent structures? Which one is better?



## Latent Structure Preference
This question leads us to the notion of **latent structure preference**.


>Latent structure $L = <G, O>$ is preferred to another $L' = <G', O>$ (written $L  \preceq L'$) if and only if 
$G'$ can represent _at least_ the same observational distributions as $G$. 
> $$ \mathcal{P}_{[O]}(<G, \theta_G>) \subseteq \mathcal{P}_{[O]}(<G', \theta'_{G'}>) $$


That is, for each  $\theta_G,$ there is a $\theta'_{G'}$ such that $$P_{[O]} (<G', \theta'_{G'}>) = P_{[O]} (<G, \theta_G>).$$

But there can be a $\theta'_{G'}$ so that $L$ is not able to express the same observational distribution.

>The order of $L$ and $L'$ is crucial in the definition.

Namely, we impose the constraint on $L'$ that it should represent _all observational distributions_ of $L$, but it can be _more expressive_.

>Preference is the [Occam's razor](https://en.wikipedia.org/wiki/Occam%27s_razor) of latent structures.

That is, it prefers the simplest $L$. Note that **simplicity is meant in terms of expressive power** (i.e., how big the class of distributions that can be represented), **not in parameters number**.

We can still prefer $L$ to $L'$ - even if $L$ has more parameters - if $L'$ is more expressive than $L$.

The edge case is when both latent structures represent the same  $\mathcal{P}_{[O]}$, i.e., they are **equivalent**. In terms of preference: both is preferred to the other, i.e.:
$$L' \equiv L \Leftrightarrow L \preceq L' \wedge L \succeq L'$$




## Minimality of Latent Structures
>A latent structure $L$ is minimal with respect to a class $\mathcal{L}$ of latent structures if and only if there is no member of $\mathcal{L}$: that is strictly preferred to $L$ -that is, if and only if for every $L' \in \mathcal{L}$: we have $L \equiv L'$ whenever $L' \preceq L$ .

## Consistency of Latent Structures

>A latent structure $L = <G, O>$ is consistent with a distribution $\hat{P}$ over $O$ if $G$ can accommodate some model that generates $\hat{P}$ - that is, if there exists a parameterization $\theta_G : P_{[O]}(<G, \theta_G>)=\hat{P}$.

## Projection of Latent Structures
>A latent structure $L_{[O]} = (G_{[O]}, O)$ is a projection of another latent structure $L$ if and only if:
> 1. every unobservable variable of $G_{[O]}$ is a parentless common cause of exactly two nonadjacent observable variables; and
> 2. for every stable distribution $P$ generated by $L$, there exists a stable distribution $P'$ generated by $L_{[O]}$ such that $I(P_{[O]}) = I(P'_{[O]})$

A Theorem:
> Any latent structure has at least one projection.


# Stable Distributions
- Faithfulness
> Let $I(P)$ denote the set of all conditional independence relationships embodied in $P$. A causal model $M = <G, \theta_G>$ generates a stable distribution if and only if $P(<G, \theta_G>)$ contains no extraneous independences-that is, if and only if $I[P(<G, \theta_G>)]\subseteq I[P(<G, \theta'_G>)]$ for any set of parameters $\theta'_G$.

# Inferred Causation
>Given $\hat{P}$, a variable $C$ has a causal influence on variable $E$ if and only if there exists a directed path from $C$ to $E$ in every minimal latent structure consistent with $\hat{P}$.


# Summary

