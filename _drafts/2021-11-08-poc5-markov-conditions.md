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



# Probabilistic implications of d-separation
If sets $X$ and $Y$ are d-separated by $Z$ in a DAG $G$, then $X$ is independent of $Y$ given $Z$ in every distribution compatible with $G$. 

If they are not d-separated, then they are dependent given $Z$ in at least one (almost all, as generating independence requires the careful tuning of parameters) distribution compatible with $G$.

Notation
Probabilistic notion of conditional independence: $X\perp_P Y |Z$
Graphical notion of d-separation: $X\perp_G Y |Z$
Reformulating the above: for disjoints node sets $X,Y,Z$ in DAG $G$ and for all probability functions $P$
$X\perp_G Y |Z \implies X\perp_P Y |Z $ if $G$ and $P$ are compatible.
If $X\perp_P Y |Z$  holds in all distributions compatible with $G$ $\implies X\perp_G Y |Z$ 

# Markov Conditions

## Recap: Markovian Parents

[PoC #2](/posts/2021/10/poc2-markov/)
>When conditioning on the **Markovian parents** $PA_i$ of node $X_i$, they become independent of all other nodes, i.e., $P(x_i\|pa_i)=P(x_i\| x_1, \dots, x_{i-1})$.

## Ordered Markov Condition
> A necessary and sufficient condition for a probability distribution $P$ to be Markov relative
a DAG $G$ is that, conditional on its parents in $G$, each variable be independent of all
its predecessors in some ordering of the variables that agrees with the arrows of $G$.

## Parental Markov Condition
The importance of Markovian models is the connection it makes between causation and probabilities via the _Parental Markov Condition_, which will be discussed in the next post in detail.
[PoC #4](/posts/2021/11/poc4-causal-queries/)

> A necessary and sufficient condition for a probability distribution $P$ to be Markov relative
a DAG $G$ is that every variable be independent of all its nondescendants (in $G$),
conditional on its parents.

## Causal Markov Condition

>Every Markovian causal model $M$ induces a distribution $P(x_1 , \dots , x_n )$ that satisfies the
parental Markov condition relative the causal diagram $G$ associated with $M$; that is, each variable $X_i$ is independent on all its nondescendants, given its parents $PA_i$ in $G$.



![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)




# Summary
