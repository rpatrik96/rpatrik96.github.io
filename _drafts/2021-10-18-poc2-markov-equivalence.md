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

Formulated otherwise: probabilities can be manipulated without considering any graph, but when you define a model with a graph and a corresponding joint distribution, you can exploit the graph structure.


## Markov Factorization




# Markov Equivalence Class

- factorization of p : chain rule, DAGs
- example of how different structures impose the same d sep (chain, fork, v-struct, no figure)
- highlight that this is a limitation of causal inference due to equivalence



# Markov Compatibility

- definiotion
- causal markov condition, ordered markov condition - compare


## I-maps
- def with P and G
- def with G1 G2
- example for both (for P,G I can use my previous figure)

### Minimal I-maps
- def
- example

### Perfect I-maps
- def example

