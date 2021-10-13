---
title: 'Pearls of Causality #3: The properties of d-separation'
date: 2021-10-18
permalink: /posts/2021/10/poc3-d-sep-prop/
tags:
  - causality
  - DAG
  - d-separation
  - Pearl
---

This post _deliberately_ (wink) tries to confuse you about the grand scheme of DAG equivalence, but at least it explains the properties of d-separation with examples. What a good deal, isn't it?


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





