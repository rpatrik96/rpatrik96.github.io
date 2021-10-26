---
title: 'Pearls of Causality #4: Causal Queries'
date: 2021-11-01
permalink: /posts/2021/11/poc4-sem/
tags:
  - causality
  - DAG
  - SEM
  - SCM
  - BN
  - Pearl
---

A top-secret guide to d-separation. We will go deep, ready?

### PoC Post Series
- [PoC #3: The properties of d-separation](/posts/2021/10/poc3-d-sep-prop/)
- ➡️ [PoC #4: Causal Queries](/posts/2021/11/poc4-causal-queries/)

# Causal Queries

> Why are doing this thing called "causal inference"?

The obvious answer is that it's fun _(half of the readers now closed the browser tab)_. To set aside joking: because we want to do causal queries, i.e., extract information about the cause-effect relationships between different mechanisms. 

Causal queries have their hierarchy: depending on the available data, we are presented three ways to make inferences:
>1. **Observational**: we put ourselves into the role of the observer, or if you like, the scientist who perceives the world as it is (i.e., in a passive way).
>2. **Interventional**: we put ourselves into the role of the investigator, i.e., the scientist who does the experiments.
>3. **Counterfactual**: we put ourselves into the role of the philosopher (or a toddler always asking why), contemplating what have happened if different conditions would have changed.

This is a clear hierarchy: counterfactual statements carry more information than observational ones, which are more insightful than pure observations.

> Of course, there is no free lunch: to climb the ladder from observational to interventional to counterfactual statements, more elaborate models are require.

In the following, we will dive into the different models used for causal statements. On the way, we will also discuss what an intervention and a counterfactual is.

## Observational Queries

> Observational queries are in terms of the joint distribution.

- cite  [PoC #2: Markov Factorization, Compatibility, and Equivalence](/posts/2021/10/poc2-markov/) where I talked about that the joint contains the least info

## Interventional Queries

### Interventions

### Causal Bayesian Networks (CBNs)


### Counterfactual Queries

### Structural Equation Models (SEMs)
- SCMs



![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


# Summary
