---
title: 'Pearls of Causality #2: The properties of d-sep'
date: 2021-10-18
permalink: /posts/2021/10/poc2-markov-equivalence/
tags:
  - causality
  - DAG
  - conditional-independence
  - Pearl
---

This post _deliberately_ (wink) tries to confuse you about the grand scheme of DAG equivalence. What a good deal, isn't it?

# Factorization of Probability Distributions
In my last post, I left you with a cliffhanger about how d-separation and conditional independence differs. This is the post I am resolving that one.

First, we need to look into some properties of probability distributions, especially **factorization**. This section would have fit into the first post, but its length is rather daunting even in its current form.

Let $P(X)$ be a probability distribution over the variables $X=\{X_1, \dots, X_n\}$. Nothing special, we are good to go, right? _Well,_ not exactly; If we treat distributions in this general form, we will encounter problems when computing values. To illustrate this, consider that even in the simples case of having $n$ _binary_ random variables (RVs), the number of combinations grows exponentially as $2^n$.

>We need to be more clever than this.

Fortunately, _every_ probability distribution obeys the **chain rule of probabilities** (no specific assumptions needed), i.e., $P(X)$ can be factorized as:
$$
P(X) = \prod_{i=1}^n P(X_{\pi_i}|X_{\pi_1}, \dots, X_{\pi_{i-1}}),
$$
where $\pi$ is a permutation of indices. This means that $P(X_1, X_2, X_3)$ can be factorized in multiple ways, e.g.:
- $P(X_1)P(X_2|X_1) P(X_3|X_1, X_2)$
- $P(X_1)P(X_3|X_1) P(X_2|X_1, X_3)$
- $P(X_2)P(X_3|X_2) P(X_1|X_2, X_3)$
- $\dots$ - you get the idea

The takeaway here is that this factorization exploits no assumption about the causal relationship between the variables - as there aren't any. Remember, these are just probability distributions, no graph is defined.

One reason for confusion could be that in the previous post, we used probability distributions on graphs, are we screwed then? No, because when we did that, we used a more expressive model family:

> $P(X)$ has its right on its own, but when we "attach" a graph to it, we will be able to reason about more complex thing.

Formulated otherwise: probabilities can be manipulated without considering any graph, but when you define a graph that has a corresponding joint distribution, you can exploit the graph structure.


# Markov Factorization
>How can the graph structure be exploited when factorizing probability distributions?

This is the question you are probably wondering about. As we have seen in the altitude-temperature example, there is a causal factorization of the distribution, namely $P(A,T) = P(A)P(T|A)$. 

>How is this factorization constructed in general?

Even this example shows that we need the parent-child relationships. Particularly, the literature of causal inference defines the notion of Markovian parents.
>Given a set of ordered variables $\{X_1, \dots, X_n\}$, the **Markovian parents** $PA_i$ of node $X_i$ are the set of nodes that make $X_i$ independent of all its _other_ non-descendants (i.e., predecessors), i.e.
> $P(x_i\|pa_i)=P(x_i\| x_1, \dots, x_{i-1})$.

Let's dissect this definition! The mention of _ordered variables_ is important (think about this as a  Python `OrderedDict`), as this way we don't need to care about the permutation $\pi$.
> A **set of ordered variables** $\{X_1, \dots, X_n\}$, also called **causal ordering** defines a particular sequence of the variables $X_i$ such that each $X_i$ is only dependent on $X_j : j < i$. This ordering is not necessarily unique.

That is, we enumerate the nodes in the graph in such a way that when $A$ causes $B$, then the index of $A$ will be lower. We can do this always, as we have DAGs that include no cycles, so each parent-child relationship in unambiguous, we can decide which node is the child and which is the parent.

For the definition, I used the terms _predecessors/non-descendants_. These are handy when speaking about a set of nodes. **Predecessors** of a node include its parents, the parents of parents, etc. **Non-descendants** of a nodes include all nodes except its descendants - i.e., all nodes that are not the children, children of children (grandchildren).

So if we condition on the _Markovian parents_ of a node, we will get the same CPD as if we conditioned on all preceding nodes in the causal ordering. The reason is that for $X_i$, the ordered set $\{X_j\}_{j=1}^{i-1}$ includes not only the parents of $X_i$, but also the parents of the parents, and so on.

Thinking in terms of _active paths_, we can interpret this definition as follows: as a node $X_i$ has only incoming edges from its Markovian parents $PA_i$, then if we condition on those, _all active paths are blocked from its predecessors_. So only $PA_i = pa_i$ stays on the right of the conditioning bar.

Having understood the definition of Markovian parents, we can construct a factorization for the graph by conditioning all nodes on their respective Markovian parents, yielding **the chain rule of Bayesian networks**:
$$
P(X) = \prod_{i=1}^n P(X_{i}|PA_i).
$$

I should stress again: this factorization is possible because we assigned a graph to the probability distribution. We can think of the graph as some kind of "prior" for the distribution - in the sense that as priors let us incorporate expert knowledge into e.g. decision making, so does the graph imply a set of independencies.

After an example, we are ready to discuss the differences of conditional independence and d-separation.

## Example

Let's apply Markov factorization in practice on our beloved experimental DAG!

![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)

We have the joint:
$$
 P(A, B, C, E,F, H, J)
$$
with the causal ordering $\{A, B, C, E, F, H, J\}$. Notice that we can also define the causal ordering as $\{C, A, F, E, B, H, J\}$, among others. This shows that the ordering is not necessarily unique.

> You might wonder: when is the causal ordering unique? When all $X_i$ depend on all $X_j : j<i$.
> E.g. when the graph with nodes $X_1, X_2, X_3$ has edges $X_1 \rightarrow X_2, X_1 \rightarrow X_3, X_2 \rightarrow X_3$.

From the structure, we can decompose it by conditioning each node on its Markovian parents. 

$$
P(A, B, C, E,F, H, J) = P(A)P(B|A)P(C)P(E|A)P(F|A)P(H|B,C)P(J|H).
$$


# Markov Compatibility


- causal markov condition, ordered markov condition - compare

>The notion of *Markov Compatibility* is the matchmaker between DAGs and probability distributions.

Before we start, we should clear up the terminiological mess around Markov Compatibility. When probability distribution $P$ and DAG $G$ are compatible, the literature refers to this in many ways, including:
- $P$ and $G$ are compatible
- $G$ represents $P$
- $P$ is Markov relative to $G$
- $G$ is an I-map of $P$.

So don't be surprised.

Amidst this confusion, let's define Markov Compatibility:
> If a probability function $P$ admits factorization $$P(X)=\prod_i P(X_i\|PA_i)$$ relative to DAG $G$, we say $P$ is Markov relative to $G$.

So Markov Compatibility serves as a "matchmaker" between $P$ and $G$. When we say that $G$ represents $P$, then we mean that if we have DAG $G$, then we will be able to 
1. _Generate samples_ from $G$ that corresponds to samples coming from $P$ - i.e., we have a "blueprint" for $P$.
2. _Explain the data_ we collected from $P$.

Actually, Markov compatibility is a necessary and sufficient condition for the above two points. To find out what an I-map is, follow me into the next section.


## I-maps

> An **I-map** is defined as a set of independence statements that hold in DAG $G$, i.e.:
>$$I(G)=\{(X\perp_P Y | Z) : (X\perp_G Y | Z)\}$$
>If $P\vDash I(G),$ then $G$ is an I-map of $P.$

Here $X\perp_G Y \| Z$ means the d-separation of $X$ and $Y$ given $Z$ in $G$, and $\vDash$ reads as "satisfies".

This definition means that $P$ and $G$ are compatible, if **all** d-separation relations we can find in $G$ imply the conditional independence of the corresponding variables in $P$.

Formulated otherwise, if $X$ and $Y$ are d-separated by $Z$ in a DAG $G$, then $X$ is independent of $Y$ given $Z$ in **every** distribution compatible with $G$. 

If they are not d-separated, then they are dependent given $Z$ in **at least one** (almost all, as generating independence requires the careful tuning of parameters) distribution compatible with $G$.

So the relationship between d-separation and conditional independence can be summarized as follows:

>For disjoints node sets $X,Y,Z$ in DAG $G$ and $\forall P$:
>- $X\perp_G Y \|Z \implies X\perp_P Y \|Z $ if $G$ and $P$ are compatible.
> - If $X\perp_P Y \|Z$  holds $\forall P$ compatible with $G$ $\implies X\perp_G Y \|Z$ 
>
>So a d-separation relation only translates to conditional independence if $G$ is able to represent $P$, whereas a conditional independence is reflected in a graph if it is present in **all** distributions $G$ is able to represent.

Before going to visit the different species of the I-map family, let's make a detour and apply the definition for graphs $G_1, G_2$ - this is a useful way to compare the expressive power of different DAGs. Plus, it will help to put minimal and perfect I-maps into context.

>Let $I(G)$ be the set of independencies in $G$. Then
$G_1$ is an I-map of $G_2$ if $I(G_1) \subseteq I(G_2).$

The above means that $G_1$ has a _smaller_ set of independencies -i.e., more edges- than $G_2$. How can then $G_1$ still represent $G_2$? Remember, 
>$X \not\perp_G Y \| Z$ is a statement about the graph, but not the assigned $P$. The functional relationship (i.e., edge weights in the simplest case) can be still manipulated to induce $X \not\perp_P Y \| Z$.

_If you wonder what those functional relations are: I will write about them in a future post discussing Structural Equation Models (SEMs). For now, it is enough to know that they are equations describing how a parent influences its child. In our altitude-temperature example, this would be the relation that adding $200m$ to the altitude reduces the temperature by $1^\circ C$ on average._

#### Example
Let's assume that we have a joint distribution $P(X,Y)$, where:
- $X$ - Number of films Nicolas Cage appeared in
- $Y$ - Number of people who drowned falling into a pool

If you wonder, the example is from [Tyler Vigen](https://www.tylervigen.com/spurious-correlations). As these events are independent, we know that $P$ factorizes as $P(X,Y) = P(X)P(Y)$.

However, if we want to find the corresponding I-map, we will face a surprise: besides a graph $G_0$ with unconnected $X$ and $Y$ nodes, $G_1 : X\rightarrow Y$ and $G_2 : X \leftarrow Y$ are also I-maps of $P$. 

To investigate this, let's write down the sets of independencies:
- $I(P) = \{X\perp Y\}$
- $I(G_0) = \{X\perp Y\}$
- $I(G_1) = \emptyset$
- $I(G_2) = \emptyset$

As per definition the only precondition for $I(G_i)$ is that it must not contain an independency that does not hold in $P$ - it can contain less. Clearly, in this example $\forall i : I(G_i)\subseteq I(P)$; thus, they are all I-maps of $P$. 

### Minimal I-maps
> The minimal I-map is an I-map without redundant edges, but it may not capture $I(P).$ The minimal I-map is not unique.

Formulated otherwise, a minimal I-map is a graph $G$ no edge can be removed from without introducing (conditional) independencies that _do not hold_ in $P$.

In the above example $G_0$ is a minimal I-map of $P$, as we cannot remove any edge from it (it does not contain any) - in this case, $I(G_0) = I(P)$, so it is a perfect I-map. For $G_1, G_2$ - although they are also I-maps-, we can remove the edge without introducing independencies that do not hold in $P$.

On the other hand, in our temperature-altitude example, the minimal I-maps are the graphs $A\leftarrow T$ and $A\rightarrow T$, as removing the edge would mean that $A$ and $T$ are independent, although we know that they are dependent. This example also illustrates that the minimal I-map may not be unique.

I made the claim that the minimal I-map may not capture $I(P)$, but I have not provided an example - yet. I will use one from Daphne Koller's [PGM1](https://www.coursera.org/learn/probabilistic-graphical-models/lecture/dJYD6/i-maps-and-perfect-maps) course. Assume that $P$ has the independencies described by a v-structure $X\rightarrow Z \leftarrow Y$. What happens if we change the graph to contain the edges $E'=\{X\rightarrow Z , Z\rightarrow Y, X\rightarrow Y  \}$? This new graph $G'$ is still an I-map, as 
- $I(P) = \{X\perp Y\}$ 
- $I(G) = \{X\perp Y\}$ 
- $I(G') = \emptyset$.

But we cannot remove any edge, namely:
- Removing $X\rightarrow Z$ would mean that $X\perp Z$ 
- Removing $Z\rightarrow Y$ would mean that $Z\perp Y$
- Removing $X\rightarrow Y$ would mean that $X\perp Y$.
And none of these are in $I(P)$.


### Perfect I-maps

> The perfect I-map is an I-map satisfying $I(G)=I(P)$. A perfect I-map does not necessarily exist.

This definition means that a perfect I-map is a graph $G$ that represents all (conditional) independencies, derived solely from its edges. That is, irrespective of the functions assigned to the edges - so if an independence statement holds, then it is true for all quantitative relationships.

In the case of the $A,T$ example or Nicolas Cage, we were able to construct perfect I-maps, but sometimes it is not possible.

I will illustrate this using an example again from Daphne Koller's [PGM1](https://www.coursera.org/learn/probabilistic-graphical-models/lecture/dJYD6/i-maps-and-perfect-maps) course. Assume that $P$ needs to satisfy $\{(A\perp C \| B,D), (B \perp D | A, C)\}$. If we want to draw a DAG representing only these independencies, we are doomed to fail (with an undirected graph, it is possible, we just need to create a circle of the nodes). As soon as we direct the edges, we will encounter a problem. Namely, if we want to not introduce more independencies, we cannot have an isolated node. But this way, either the edges (due to their directionality) will introduce independencies, or we will have a v-structure that screws everything up.

# Markov Equivalence Class

- example of how different structures impose the same d sep (chain, fork, v-struct, no figure)
- highlight that this is a limitation of causal inference due to equivalence
- observational equivalence

> A Markov equivalence class is a set of DAGs that encode the same set of conditional independencies.

