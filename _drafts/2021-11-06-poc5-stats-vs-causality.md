---
title: 'Pearls of Causality #5: Statistical vs Causal Inference'
date: 2021-11-06
permalink: /posts/2021/11/poc5-stats-vs-causality/
tags:
  - causality
  - statistics
  - Pearl
---



### PoC Post Series
- [PoC #4: Causal Queries](/posts/2021/11/poc4-causal-queries/)
- ➡️ [PoC #5: Statistical vs Causal Inference](/posts/2021/11/stats-vs-causality/)

# Statistical vs Causal Inference

Today we step into rough territory. Namely, there is a bit of a tension among statistics and causality people. To say the least, I will try to be objective - this won't be that hard. For here holds the same as in every walks of life: everything has its upside and downside.

Let's keep in mind the figure showing the relationship between the model classes of joint distributions, DAGs, and SEMs from [PoC #4](/posts/2021/11/poc4-causal-queries/). This will help us visualizing the differences. 
![Relationship of joint distributions, DAGs, and SEMs](/images/posts/joint_dag_sem.svg)

## Terminological Catechism
Woaaaa, I just dropped "Terminological Catechism" as a section title. I did because we will talk about the conceptual differences of statistical and causal inference in terms of definitions (thus, the terminological part). The catechism part expresses my goal to do this similar to the question-answer blueprint of religious or philosophical principles.

> Our cookbook has **parameters** and **assumptions** as ingredients. As a world-class chef is able to differentiate between the use-cases of cooking, steaming, and [sautéing](https://en.wikipedia.org/wiki/Saut%C3%A9ing) (I just looked up this word), so should we between statistics and causality.


### Parameters
> What are the scopes of different parameters?

We will discuss three types of parameters:
- Probabilistic
- Statistical
- Causal

#### Probabilistic Parameters

>A **probabilistic parameter** is attached to a **joint distribution**. 

This can be the mean of a Gaussian, the domain of a uniform distribution, or the shape of a gamma distribution.

#### Statistical Parameters

The subtle difference of **statistical parameters** comes from empirical (observational) nature of statistics. We can only reason about what we observe; thus, **statistical parameters** are constrained to the **joint distribution of the observed variables**. 

For example, when we use linear regression to predict $A$ from $B$, then the regression coefficient $r_{AB}$ is a statistical parameter.

>**Statistical parameters** are _agnostic_ to the latent variables: they are the same if there are no latents or if there are many.

As both probabilistic and statistical parameters are defined in terms of a joint distribution, we can use all probabilistic parameters as statistical ones:
> **Statistical parameters** are probabilistic parameters applied of the joint distribution of observed variables.

#### Causal Parameters

Now let's turn to causal parameters. 

>A **causal parameter** is a parameter of a SEM that is not a statistical parameter.

I wasn't very helpful with this definition... Why is it so strange? Because we need to be _consistent:_ as SEMs are a superset of DAGs that are a superset of joint distributions (see the figure above), we cannot allow to call the mean of a distribution in one case a statistical, in another a causal parameter. So statistical parameters are still statistical parameters in SEMs.

For SEMs are a richer model class, there will be some parameters left. Those are the causal parameters, such as the number of parents or the coefficients of the equations in the SEM.

You surely noticed that I used _statistical_ and not _probabilistic_ parameters in the definition of causal parameters.





|  Concept | Scope  | Examples |
|---|---|---|
| Probabilistic parameter  |  Joint distribution |  - Mean<br> - Domain<br> - Shape |
| Statistical parameter  |  Joint distribution of observed variables|  - _Mean_<br> - _Domain_<br> - _Shape_<br>- Regression coefficient<br>- Value of a density function |
| Causal parameter  |  SEM |  - Number of parents<br> - Coefficients of the equations |


### Assumptions



## Other stuff 

- Spurious correlations
- Markov factorization
- ICM 



# Summary
