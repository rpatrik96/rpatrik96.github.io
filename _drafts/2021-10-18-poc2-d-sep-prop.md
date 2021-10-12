---
title: 'Pearls of Causality #2: The properties of d-sep'
date: 2021-10-18
permalink: /posts/2021/10/poc2-d-sep/
tags:
  - causality
  - DAG
  - d-separation
  - conditional-independence
  - Pearl
---

d-separation is the bread and butter for deciding about conditional independence in DAGs. What is a DAG, anyway?

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

# Properties of d-separation

![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)

- d-sep vs cond ind
- proofs for the properties?


with **intuitive examples**

## Symmetry
>$X\perp Y | Z \implies Y\perp X | Z$



## Decomposition
>$X\perp YW | Z \implies X\perp Y | Z$



## Weak union
> $X\perp YW | Z \implies X\perp Y | ZW$




## Contraction
>$X\perp Y | Z  \land X\perp W | ZY \implies X\perp YW | Z$




## Intersection (for strictly positive distributions)
> $X\perp W | ZY  \land X\perp Y | ZW \implies X\perp YW | Z$





