---
title: 'Where is the nature of the relationship expressed in causal models?'
date: 2022-06-28
permalink: /posts/2022/06/2022-06-28-sem-nature-of-relationships
tags:
  - causality
  - SEM
---

Graphs don't tell about the nature of dependence, only about its (non-)existence.

# Where is the type of dependence encoded in an SEM?

I came accross a question about how can you express, e.g., a logical AND relationship in SEMs (Structural Equation Models). Let's look into this.

Assume that you would like to visit your friend and you have a motorcycle you wish to use. To be able to undertake the journey, you need both the motorcycle and fuel (if you can afford it, anyways...).
Clearly, you require both conditions, leading to a logical AND condition. How do you describe this in the language of SEMs?

We have the following *binary* variables:
- $X$ - access to the motorcycle
- $Y$ - access to sufficient fuel
- $Z$ - a successful visit

$Z$ depends on both $X$ and $Y$, so this will be a collider/v-structure in the form $X\to Z\leftarrow Y$.

> But this graph does not say anything about the nature of the dependency, it only says that there is some.

This is not a bug, as graphs on their own are only designed to express the (non-)existence of a cause-effect relationship, but it will not say anything about its functional form. For that, we need to level up our game to SEMs - we need the "equation" part of the SEM. 

In a SEM, each of $X,Y,Z$ has a corresponding function that maps from the exogenous variables $U_i$ to the observed ones.
For simplicity, assume that
$$ \begin{align} X&=U_X \\
Y&=U_Y\end{align}$$

Now lets look into $Z$. There, the relationship will be of form 
$$ Z = f(X,Y, U_Z),$$
as $Z$ depends on both $X$ and $Y$. To express the logical AND relationship, we might construct $f$ as 
$$  Z = f(X,Y, U_Z) = X*Y*U_Z,$$
which requires that $X$ and $Y$ are both present (expressed with the multiplication; $U_Z$ is not important here), meaning that 
> the nature of the relationship is expressed with the functional relationships, but not by the graph structure itself.