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

# Markov Compatibility

## I-maps

### Minimal I-maps

### Perfect I-maps

# Properties of d-separation

![Our example graph for studying d-separation](/images/_posts/d_sep_ex.svg)

- d-sep vs cond ind


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





