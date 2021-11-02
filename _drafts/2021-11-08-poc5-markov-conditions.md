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

Before starting, let's discuss the meaning of **necessary and sufficient** conditions.
> When we have a statement that $A$ is a necessary condition of $B$ then this means that $A =false \implies B = false,$ but $A = true \implies B = ?$

That is, $A$ must hold for $B$ to be true, but when $A$ is true, this does not mean that $B$ is necessarily true. We can only be certain that when $A$ is false, then $B$ is false too. We can also think of a necessary condition in the other direction. Namely, if $B$ is true, then $A$ must be true, i.e., $B=true \implies A = true$.

> When we have a statement that $A$ is a **sufficient condition** of $B$ then this means that $A =true \implies B = true,$ but $A = false \implies B = ?$

That is, when $A$ is trues, so is $B$, but when $A$ is false, then $B$ can still be true, but it can also be false. 


## Recap: Markovian Parents

We have discussed the notion of Markovian parents back in post [PoC #2](/posts/2021/10/poc2-markov/), but for the sake of completeness, let's recap:

>When conditioning on the **Markovian parents** $PA_i$ of node $X_i$, they become independent of all other nodes, i.e., $P(x_i\|pa_i)=P(x_i\| x_1, \dots, x_{i-1})$.

In plain English, if a node has an edge pointing to $X_i$, then it belongs to $PA_i$.

## Ordered Markov Condition (OMC)

Our first candidate in the contest for Ms./Mr. Markov Universe is the **Ordered Markov Condition**:

> A necessary and sufficient condition for $P$ to be Markov relative to a DAG $G$ is that:
> 1. Each $X_i$ is independent of all its **predecessors** given $Pa_i$.
> 2. In a causal ordering of the variables. 


The two components of OMC mean the following:
1. $Pa_i$ screen off any influence from the predecessors of $X_i$ onto $X_i$.
2. It requires an ordering of the variables, where each $X_i$ depends only on $X_{j<i}$ - for the defintion see [PoC #2](/posts/2021/10/poc2-markov/)


## Parental Markov Condition (PMC)
**The importance of Markovian models is the connection it makes between causation and probabilities via the _Parental Markov Condition_, which will be discussed in the next post in detail.
[PoC #4](/posts/2021/11/poc4-causal-queries/)**

> A necessary and sufficient condition for a probability distribution $P$ to be Markov relative a DAG $G$ is that each $X_i$ should be independent of all its **nondescendants**, given $Pa_i$.

## Causal Markov Condition (CMC)

>Every Markovian causal model $M$ induces a distribution $P(x_1 , \dots , x_n )$ that satisfies the
parental Markov condition relative the causal diagram $G$ associated with $M$; that is, each variable $X_i$ is independent on all its nondescendants, given its parents $PA_i$ in $G$.



![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)




# Summary
