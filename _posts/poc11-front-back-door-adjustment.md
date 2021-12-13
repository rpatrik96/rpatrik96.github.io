---
title: 'Pearls of Causality #11: Front- and Back-Door Adjustment'
date: 2021-12-13
permalink: /posts/2021/12/2021-12-13-poc11-front-back-door-adjustment.html
tags:
  - causality
  - Pearl
  - intervention
  - identifiability
  - confounding
---

Two ways to shut the door before confounding enters the scene.

### PoC Post Series
-  [PoC #10:  Interventions and Identifiability](/posts/2021/12/poc10-interventions-and-identifiability.html/)
- ➡️ [PoC #11:  Front- and Back-Door Adjustment](/posts/2021/12/poc11-front-back-door-adjustment.html/)

# Back-Door Adjustment

Last time we have seen how we can adjust for direct causes by giving conditions for which variables we need to observe: for calculating $P(y\|do(X=x))$, we need $Y, X, Pa_X$. This post gives two more general formulas that can be applied to DAGs to test whether the adjustment conditions are satisfied.

The main idea behind the generalization is the fact that not only $Pa_X$) can block the incoming paths to $X$. As these paths come from the non-descendants of $X$ and the edges point toward $X$, the whole concept is thought of as having (and to screen off confounding, blocking) a _back door_.


>A variable set $Z$ satisfies the **Back-Door Criterion** to an ordered pair of variables $(X, Y)$ in a DAG if:
>1. nodes in $Z$ are non-descendants of $X$
>2. $Z$ blocks every incoming path into $X$

The Back-Door Criterion makes a statement about an _ordered pair_; i.e., $Y$ is a descendant of $X$ (there is a path from $X$ to $Y$). The **first condition** generalizes the requirement for observing $Pa_X$, for any non-descendant of $X$ suffices to block the incoming paths into $X$ - as of the **second condition**.

That is, we are looking for a set of variables $Z$ such that every path $X \leftarrow \dots - Z - \dots - Y$ is blocked. Note that here $-$ stands for any of $\leftrightarrow, \rightarrow, \leftarrow$. The only constraint is that the path has an edge pointing into $X$. As we want to reason about the effect of $X$ on $Y$, we need to leave the paths from $X$ to $Y$ _unblocked_ but all paths _into_ $X$ _blocked_.

After understanding the Back-Door Criterion, we can apply this to calculate interventional distributions.

>If a variable set $Z$ satisfies the Back-Door Criterion relative to $(X, Y)$ then the effect of $X$ on $Y$ is given by:

$$P(y|do(X=x)) = \sum_z P(y|x,z)P(z)$$

This is the _same_ formula we had for adjusting for direct causes. Nonetheless, the scenarios where we can apply it are more general.

The formula can be interpreted as _dividing_ the data into categories by the values of $Z$ and $X$ (this is also called _stratifying_) and calculating the weighted average of the _strata_ (this is the fancy plural form expressing data categories). 
By conditioning on these two variables, we make the strata independent of each other - as $Z$ blocks the Back-Door paths, conditioning on $X$ is the same as $do(X=x)$. Note that for general $Z$ this would not be the case.

# Front-Door Adjustment

The Back-Door Adjustment formula is nice, but unfortunately it is sometimes not applicable. It can be a quite strong assumption that we can observe a sufficient set of variables that block _all_ Back-Door paths.

The intuition for the more general formula of Front-Door Adjustment comes from the _genius observation_ that houses usually have a _front entrance_, not just a back one.


>A variable set $Z$ satisfies the **Front-Door Criterion** to an ordered pair of variables $(X, Y)$ in a DAG if:
>1. $Z$ blocks every directed path from $X$ to $Y$
>2. There is no back-door path from $X$ to $Z$
>3. All back-door paths from $Z$ to $Y$ are blocked by $X$

Let's work through these three conditions. 
1. The **first condition** states the conditional independence $X\perp Y \| Z$.
2. The **second condition** postulates that $P(z\|x)=P(z\|do(X=x)$ - note that the first condition says that $Z$ must be in between $X$ and $Y$, i.e., $Z$ is a descendant of $X$.
3. The **third condition** says that $X$ acts as a Back-Door for the effect of $Z$ on $Y$. So the effect of $Z$ on $Y$ can be calculated by the Back-Door Adjustment formula.

These conditions result in a formula that applies Back-Door Adjustment twice: once for calculating the effect of $X$ on $Z$ and once for using $X$ as a Back-Door for estimating the effect of $Z$ on $Y$.

>If a variable set $Z$ satisfies the Front-Door Criterion relative to $(X, Y)$ and if $P(x,z) >0$ then the effect of $X$ on $Y$ is given by: 
$$P(y|do(X=x)) = \sum_z P(z|x)\sum_{x'}P(y|x', z)P(x')$$

The **outer sum** is effect of $X$ on $Z$; the second condition makes it sure that the conditional is the same as the interventional distribution. The **inner sum** is the effect of $Z$ on $Y$; calculated by the Back-Door Adjustment formula.

The requirement for a positive $P(x,z)$ distribution makes sure that the conditional $P(y\|x,z)$ is well-defined - meaning that all $x,z$ combinations are yielding meaningful strata.

# Summary
Our endeavor to find ways to adjust for confounding resulted in two practical formulas. Now we can fight confounding. Of course, this requires that we know that confounding is present with a specific structure.