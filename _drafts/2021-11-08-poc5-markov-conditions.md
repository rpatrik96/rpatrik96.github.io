---
title: 'Pearls of Causality #5: Markov Conditions'
date: 2021-11-08
permalink: /posts/2021/11/poc5-markov-conditions/
tags:
  - causality
  - DAG
  - Markov
  - Pearl
---

The model zoo of Markovian conditions is ~~fascinating~~ confusing. Let there be light!

### PoC Post Series
- [PoC #4: Causal Queries](/posts/2021/11/poc4-causal-queries/)
- ➡️ [PoC #5: Markov Conditions](/posts/2021/11/poc5-markov-conditions/)

# Markov Conditions

In this post we continue our enterprise of making sense of causal taxonomy. This time, Markov conditions are the next.

> Markov conditions express the connection between causal relationships (i.e., graphs) and probabiliies.
> There is three of them:
> - Ordered Markov Condition
> - Parental Markov Condition
> - Causal Markov Condition

Why would we do such a thing if we already made the connection in [PoC #2](/posts/2021/10/poc2-markov/)? As you recall, we expressed how and when d-separation and conditional independence relate.

> Those statements were about the consequences of $P$ being compatible with $G$. However, **Markov conditions are about when $P$ and $G$ are compatible**.

This means that we first need to check one of the Markov conditions before drawing conclusions about $P$ and $G$.  

## Necessary and sufficient conditions

Before starting, let's discuss the meaning of **necessary and sufficient** conditions.
> When we have a statement that $A$ is a necessary condition of $B$ then this means that $A =false \implies B = false,$ but $A = true \implies B = ?$

That is, $A$ must hold for $B$ to be true, but when $A$ is true, this does not mean that $B$ is necessarily true. We can only be certain that when $A$ is false, then $B$ is false too. We can also think of a necessary condition in the other direction. Namely, if $B$ is true, then $A$ must be true, i.e., $B=true \implies A = true$.

> When we have a statement that $A$ is a **sufficient condition** of $B$ then this means that $A =true \implies B = true,$ but $A = false \implies B = ?$

That is, when $A$ is true, so is $B$, but when $A$ is false, then $B$ can still be true, but it can also be false. 


## Recap: Markovian Parents

We have discussed the notion of Markovian parents back in  [PoC #2](/posts/2021/10/poc2-markov/), but for the sake of completeness, let's recap:

>When conditioning on the **Markovian parents** $PA_i$ of node $X_i$, they become independent of all other nodes, i.e., $P(x_i\|pa_i)=P(x_i\| x_1, \dots, x_{i-1})$.

In plain English, if a node has an edge pointing to $X_i$, then it belongs to $PA_i$.

## Ordered Markov Condition (OMC)

Our first candidate in the contest for Ms./Mr. Markov Universe is the **Ordered Markov Condition**:

> A necessary and sufficient condition for $P$ to be Markov relative to a DAG $G$ is that:
> 1. Each $X_i$ is independent of all its **nondescendants** given $Pa_i$.
> 2. In a causal ordering of the variables. 


The two components of the OMC mean the following:
1. $Pa_i$ screen off any influence from the nondescendants of $X_i$ onto $X_i$.
2. It requires a variable ordering that reflects the edges in $G$, where each $X_i$ depends only on $X_{j<i}$ - for the defintion see [PoC #2](/posts/2021/10/poc2-markov/)


## Parental Markov Condition (PMC)

Our next candidate is the **Parental Markov Condition**:

> A necessary and sufficient condition for a probability distribution $P$ to be Markov relative a DAG $G$ is that each $X_i$ should be independent of all its **nondescendants**, given $Pa_i$.

The PMC includes less clutter than the OMC: there is no mention of a variable ordering. This seems to make our life easier, but - I paraphrase here Pearl again - the OMC is easier to use in practice.

>Why would that be?

My _intuition_ is that having a causal ordering makes the check simpler. Namely, we can put all edges into an adjacency matrix that will be triangular. This provides a predefined data structure (it will always be triangular given that we use the causal ordering) that can be exploited when writing code for independence checks.

By the way, the PMC is also called the Local Markov Condition - as we only need to check the parents of $X_i$, which are "close" to $X_i$; thus, the name local.

## Causal Markov Condition (CMC)

I paraphrased Pearl in [PoC #4](/posts/2021/11/poc4-causal-queries/) and said that _"The importance of Markovian models is the connection they make between causation and probabilities via the Parental Markov Condition."_ This is formalized via the Causal Markov Condition (CMC).

Let's figure out what Pearl meant.

Remember, Markovian in this context means that we have a DAG with independent noise variables. 

>Every Markovian causal model $M= <G, \theta_G>$ induces a distribution $P(x_1 , \dots , x_n )$ that satisfies the
Parental Markov Condition relative to $G$; that is, each  $X_i$ is independent on all its nondescendants, given its parents $Pa_i$.

We can see that the **CMC is the Parental Markov Condition applied to Markovian models**. This ensures that by constructing a Markovian SEM, we will get a distribution that is Markov relative to the DAG. Thus, the connection is made.

> That is, **the CMC defines a blueprint how to create a distribution that is Markov relative to a DAG**.

In contrast, both the OMC and the PMC only define the boundary conditions to check whether $P$ is compatible with $G$ - they are not constructive.

# Summary
In this post, we investigated three different Markov Conditions. The takeaway is that t**he Ordered and Parental Markov Conditions enable checking Markov compatibility** in a slightly different way, but they are interchangeable. With any of them, we can check Markov compatibility, but **we do not know how to construct such a $P$.**

The **Causal Markov Condition** takes a step further and gives us an **instruction manual about how to get a compatible pair of $G$ and $P$**.
