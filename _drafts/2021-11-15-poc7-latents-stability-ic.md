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
- $M = <G, \theta_G>$: a causal model 
- $L$: a latent structure
- $\mathcal{L}$: a class of latent structures 
- $I(P)$:  the set of all conditional independencies in $P$.

>A **latent structure** is a pair $L = <G, O>$ with DAG $G$  over nodes $V$ and where $O\subseteq V$ is a set of observed variables.

So $L$ is a DAG where we attach labels to the nodes that are observed. So far so good. 

>Why do we need latent structures?

Because they can represent our hypotheses about the world. Imagine ourselves in 20th century. We are physicists looking for the secrets of the universe. Some of us might still think that Newtonian physics is the way to go, some of us is a supporter of Einstein's theory of relativity, whereas others believe in [string theory](https://en.wikipedia.org/wiki/String_theory). Each of us can observe the same, but our mental model is different. I.e., we have a class of latent structures.

>How can we compare latent structures? Which one is better?



## Latent Structure Preference
This question leads us to the notion of **latent structure preference**.


>Latent structure $L = <G, O>$ is preferred to another $L' = <G', O>$ (written $L  \preceq L'$) if and only if 
$G'$ can represent _at least_ the same family of observational distributions as $G$. 
> $$ \mathcal{P}_{[O]}(<G, \theta_G>) \subseteq \mathcal{P}_{[O]}(<G', \theta'_{G'}>) $$


That is, for each  $\theta_G,$ there is a $\theta'_{G'}$ such that (note the difference of $\mathcal{P}$ and $P$):
$$P_{[O]} (<G', \theta'_{G'}>) = P_{[O]} (<G, \theta_G>).$$

But there can be a $\theta'_{G'}$ so that $L$ is not able to express the same observational distribution.

>The order of $L$ and $L'$ is crucial in the definition.

Namely, we impose the constraint on $L'$ that it should represent _all observational distributions_ of $L$, but it can be _more expressive_.

>Preference is the [Occam's razor](https://en.wikipedia.org/wiki/Occam%27s_razor) of latent structures.

That is, it prefers the simplest $L$. Note that **simplicity is meant in terms of expressive power** (i.e., how big the class of distributions that can be represented), **not in parameters number**.

We can still prefer $L$ to $L'$ - even if $L$ has more parameters - if $L'$ is more expressive than $L$.

The edge case is when both latent structures represent the same  $\mathcal{P}_{[O]}$, i.e., they are **equivalent**. In terms of preference: both is preferred to the other, i.e.:
$$L' \equiv L \Leftrightarrow L \preceq L' \wedge L \succeq L'$$

Similar to inequalities, we will use the symbol $\prec$ for strict preference-i.e., excluding equivalence.


## Minimality of Latent Structures

Latent structures cannot escape our desire to look for the best. Minimality is the concept that quantifies this greatness.

>A latent structure $L$ is **minimal** in a class of latent structures $\mathcal{L}$ if and only if there is no member of $\mathcal{L}$ that is strictly preferred to $L$.
> $$ \not\exists L' \in \mathcal{L} : L \prec L' $$


The implication is that if we find an $L' : L' \preceq L \implies L \equiv L'.$ This is because by the definition $L \not\prec L'$; thus $L \preceq L'$ holds. As new now have both $L \preceq L'$  and $L' \preceq L$, we get $L' \equiv L$.

> Minimality expresses the "efficiency" of a latent structure. That is, a minimal $L$ is the most economical in terms of expressive power.



## Consistency of Latent Structures

We can have a minimal $L$ and still fail to make use of it: while striving for an -in a sense of having a possibly small space of observational distributions- compact structure, we should ask:

>Is $L$ able to represent the specific observational distribution $\hat{P}$ we care about?

Otherwise, our effort are futile. Fortunately, we can answer by checking the **consistency** of $L$ and $\hat{P}$.

>A latent structure $L = <G, O>$ is **consistent** with a distribution $\hat{P}$ over $O$ if there are parameters $\theta_G$ such that $G$ represents $\hat{P}$.
>$$\exists \theta_G : P_{[O]}(<G, \theta_G>)=\hat{P}$$

Consistency embodies the checks and balances in contrast to minimality.
>Practically, it serves as a lower bound on the expressive power of $L$.

The following scenarios are possible:
- $L$ is **consistent** with $\hat{P}$ but **minimal** w.r.t. $\mathcal{L}$: this is the best case, as $L$ is expressive enough to represent $\hat{P}$ over $O$ and it does not waste expressive power.
- $L$ is **consistent** with $\hat{P}$ but **not minimal** w.r.t. $\mathcal{L}$: $L$ is still able to represent $\hat{P}$ over $O$, but it wastes expressive power by not being minimal.
- $L$ is **not consistent** with $\hat{P}$ but **minimal** w.r.t. $\mathcal{L}$: this configuration makes $L$ practically useless as if it cannot represent $\hat{P}$ over $O$, then minimality does not matter.
- $L$ is **not consistent** with $\hat{P}$ but **not minimal** w.r.t. $\mathcal{L}$: this is like buying a sports car for rural road use. It cannot be used and it is very expensive.


## Projection of Latent Structures

When latent variables enter the game, they raise the following question:
> If we don't know how many latent variables there are that influence the dependencies of the observed variables, how can we uncover the causal graph over the observables?

This is a problem of **unknown unknowns**, namely, we don't know what we don't know about the latents, as-by definition-we cannot observe them.

The practical consequence _seems to be_ the need for checking all possible latent structures. But there are infinitely many of them...

Fortunately, there is an alternative. It is enough to check the **projection** of latent structures. Projections have _the same dependencies over_ $O$  as the original latent structure, they are characterized by the following definition:

_**Note**: for the definition of stable distributions, see the [next section](#stable-distributions-faithfulness)._

>A latent structure $L_{[O]} = <G_{[O]}, O>$ is a **projection** of another latent structure $L$ if and only if:
> 1. Every unobservable variable of $G_{[O]}$ is a parentless common cause of exactly two nonadjacent observable variables; and
> 2. For every stable distribution $P$ generated by $L$, there exists a stable distribution $P'$ generated by $L_{[O]}$ such that $I(P_{[O]}) = I(P'_{[O]})$





A Theorem:
> Any latent structure has at least one projection.



# Stable Distributions (Faithfulness)

>**Stability** or **faithfulness** (less frequently used alternatives are _DAG-isomorphism_ and _perfect-mapness_) answers the question of how "reliable" an independence statement is.

_Note to self: add these names to the [Causal Dictionary](posts/2021/10/poc-causal-dictionary/)._

To understand what "reliability" means, we first need to consider the two types of independence statements.

## The nature of independence

Let's imagine that we observed $X\perp_P Y | Z$ in the distribution $P$ generated by $G$.
We _could_ think that this means any of the following (assume that there are only three nodes in $G$):
- $X\rightarrow Z\rightarrow Y$
- $X\leftarrow Z\rightarrow Y$
- $X\leftarrow Z\leftarrow Y$

>These are **not** the only possible scenarios.

The reason is in the definition of I-maps. As it requires that $I(G) \subseteq I(P)$, it is possible that observing $X\perp_P Y | Z$ does not mean $X\perp_G Y | Z$. 

But we said that $P$ is generated by $G$, so the observations we made cannot contradict all the above structures as otherwise we would have $X\not\perp_P Y | Z$.

>However intuitive, this reasoning misses a point: the **nature of independencies**.

We can differentiate two types of independencies:
- **Structural**: when both $X\perp_G Y | Z$ and $X\perp_P Y | Z$ hold.
- **Functional**: when $X\not\perp_G Y | Z$ but $X\perp_P Y | Z$ holds in the distribution $P$.

>From the two, **structural independencies** are straightforward. It means that $I(G)$ contains the d-separation statement that induces conditional independence in $P$. 

This is when $X\perp_G Y | Z$ holds; thus, any of the above three structures are present in the graph.


>On the other hand, **functional independencies cannot be read off $G$**. They are encoded in the structural equations (i.e., in $f_i$).


### Example

![Example for functional independencies](/images/posts/func_indep.svg)

Consider the graph in the image above. It is described by the following SEM:
- $ X = U_1$
- $ Z = aX + U_2$
- $ Y = bX + cZ + U_3$

Clearly, $X \not\perp_G Y$ and even $X \not\perp_G Y |Z.$ But setting $b = -ac$ makes $X$ and $Y$ _independent_. If $b=0$, then $X$ and $Y$ are _conditionally independent_ given $Z$.

Thus, observing the (conditional) independence of $X$ and $Y$ is a matter of luck, as there are only very few combinations of $a,b,c$ that (conditional) independence holds.

## Definition

>$P$ is a **stable distribution** of a causal model $M= <G, \theta_G>$ if and only if **$G$ is a perfect I-map of $P$
.**
>$$(X \perp_G Y|Z)  \Leftrightarrow (X \perp_P Y|Z)$$ 

That is, $P$ maps the structure of $G$, and even varying the parameters $\theta_G$ does not destroy any independence in $P$. 

This remark let's us formulate the definition in an equivalent way. 
>Namely, a causal model $M$ generates a **stable distribution** $P$ if and only if $P(<G, \theta_G>)$ **contains no extraneous independences**.
>$$\forall \theta'_G : I[P(<G, \theta_G>)]\subseteq I[P(<G, \theta'_G>)]$$ 

That is, **only structural independencies count**. Both definitions **exclude functional independencies**. The first definition does this by postulating the $\perp_G \rightarrow \perp_P$ mapping to be **bijective**. For $G$ cannot reflect functional independencies, there cannot be any in $P$ as there is no equivalent in $G$. 

The second definition forces $\theta_G$ not to introduce any new independencies. If $\theta_G$ would generate a new indepdency, then there would exist a $\theta_G^*$ so that $[P(<G, \theta_G^*>)]\subseteq I[P(<G, \theta_G>)],$ which contradicts the definition.

Let's close this section with my whim, i.e., terminology. To be honest, I think that the name _faithfulness_ is not very descriptive of what the definition really stands for. _Stability_ is a bit better (at least, compared to faithfulness), as it expresses that no matter how the parameters change, the independencies in $P$ remain the same. These are the two most commonly used names for the concept. Nonetheless, the other two are much better. _DAG-isomorphism_ explicitly states that we are talking about graphs with a _fixed_ structure-but it still does not make the connection between $P$ and $G$. 

>_In my opinion_, _perfect-mapness_ is the best name. It makes very clear that $G$ and the distribution $P$ generated by $M$ have the same set of independencies.



# Inferred Causation
>Given $\hat{P}$, a variable $C$ has a causal influence on variable $E$ if and only if there exists a directed path from $C$ to $E$ in every minimal latent structure consistent with $\hat{P}$.


# Summary

