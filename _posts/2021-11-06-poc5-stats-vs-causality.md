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

This can be the mean of a Gaussian, the domain of a uniform distribution, or the shape of a Gamma distribution.

#### Statistical Parameters

The subtle difference of **statistical parameters** comes from the empirical (observational) nature of statistics. We can only reason about what we observe; thus, **statistical parameters** are constrained to the **joint distribution of the observed variables**. 

For example, when we use linear regression to predict $A$ from $B$, then the regression coefficient $r_{AB}$ is a statistical parameter.

>**Statistical parameters** are _agnostic_ to the latent variables: they are the same if there are no latents or if there are many.

As both probabilistic and statistical parameters are defined in terms of a joint distribution, we can use all probabilistic parameters as statistical ones:

> **Statistical parameters** are probabilistic parameters  of the joint distribution of observed variables.

_Remember:_ statisticians work from measurements (i.e., what they can observe via measurement devices).

#### Causal Parameters

Now let's turn to causal parameters. 

>A **causal parameter** is a parameter of a SEM that is not a statistical parameter.

I wasn't very helpful with this definition... Why is it so strange? Because we need to be _consistent:_ as SEMs are a superset of DAGs that are a superset of joint distributions (see the figure above), we cannot allow us to call the mean of a distribution in one case a statistical, in another a causal parameter. So statistical parameters are still statistical parameters in SEMs. 

For SEMs are a richer model class, there will be some parameters left. Those are the causal parameters, such as the number of parents or the coefficients of the equations in the SEM.

You surely noticed that I used the adjective _statistical_ and not _probabilistic_ in the definition of causal parameters. Pearl reasons that excluding the latents from statistical parameters is necessary; otherwise, causal assumptions could be disguised by those unobserved variables. We will discuss what this means in the next section.



|  Concept | Scope  | Examples |
|---|---|---|
| Probabilistic parameter  |  Joint distribution |  - Mean<br> - Domain<br> - Shape |
| Statistical parameter  |  Joint distribution of observed variables|  - _Mean_<br> - _Domain_<br> - _Shape_<br>- Regression coefficient<br>- Value of a density function |
| Causal parameter  |  SEM |  - Number of parents<br> - Coefficients of the equations |


### Assumptions
> How do our assumptions differ?

The types we discuss here are the same:
- Probabilistic
- Statistical
- Causal

>**Probabilistic assumptions** impose constraints on the joint distribution of all variables - for example that they are normally distributed.

The distinction between **probabilistic** and **statistical** assumptions is the same as for parameters:

> **Statistical assumptions** are probabilistic assumptions of the joint distribution of observed variables.

Although such assumptions are defined in terms of the joint, they include statements like $P$ is Markov relative to $G$. Why? Because this statement - although refers to a graph - has purely probabilistic consequences for the joint . Formulated otherwise, we can make a statement that has the same effect on the joint without mentioning _any graph_. Namely, that it factorizes in a specific way.

>**Causal assumptions** are those constraints of the SEM that cannot be formulated as statistical assumptions.

These include the functional form of $f_i$ in the SEM or that the _unobserved_ exogenous variables $U_i\neq U_j$ are uncorrelated.

>Isn't correlation a statistical concept?

Yes, it is. But as it concerns _unobserved_ variables, we cannot formulate this constraint statistically. Namely, we will not be able to measure $U_i, U_j$. This is the difference I promised I explain at the end of last section.

Causality treats us with two more concepts: _testable/falsifiable_ and _non-testable_ assumptions.

When a causal assumption has statistical consequences, it is called _testable_. When experiments can be used as means of falsification (this is not always the case), then we say that the assumption is _experimentally testable_. Reasoning about the effect of $X$ on $E(Y)$ is empirically testable, but the same statement w.r.t. a _particular_ subject is not.

For the latter, imagine the following scenario: we treat a patient with drug $X$ and we are interested whether $X$ can cure the patient. Let's say that we observe outcome $Y=healthy$. Can we say the $X$ was the cause of $Y$? No, we cannot, as other factors could have contributed to $Y$ (such as genetics). We would need to answer the counterfactual question "Would the patient be cured without administering $X$?"

|  Concept | Scope  | Examples |
|---|---|---|
| Probabilistic assumption  |  Joint distribution |  - Gaussian distribution<br>- Isotropic covariance matrix |
| Statistical assumption  |  Joint distribution of observed variables|  - _Gaussian distribution_<br>- _Isotropic covariance matrix_ <br>- Markov compatibility
| Causal assumption  |  SEM |  - Functional form of $f_i$<br>- Unobserved exogenous variables are uncorrelated|

## Why causal inference?

After the casual mumbo-jumbo of me throwing definitions (again) at you, let's dive into why we need causal inference.

> First, the disclaimer: causal inference is not the Holy Grail. 

Namely, as the model class is larger (remember the figure at the beginning of the post), learning causal models is much harder. Sometimes we are only able to identify the graph up to its Markov equivalence class. Often even this is not possible.

But if we succeed, we will be able to make richer statements - and hopefully will avoid suspecting [Nicolas Cage]((https://www.tylervigen.com/spurious-correlations)).


### Markov Factorization
We discussed Markov factorizations in [PoC #2](/posts/2021/10/poc2-markov/), the only thing I will mention here is that _statistical inference can also use Markov factorizations, but there it is optional._ 

Why would statisticians still use Markov factorization? Because of data efficiency (see example in the next section).

Nonetheless, _in causal inference, it is essential_, as the Markov factorization (via Markov compatibility) describes the dependencies in the graph between parents and their children. Without this, we could not reason about interventions.


### Data-efficiency
I must admit that I am writing this post mainly because of this section. I got a message on Twitter yesterday about why causal models are said to be more data efficient than correlational/statistical models. So let me answer that one.

The reason is twofold: because of Markov factorization and the [Independent Mechanism Principle](/posts/2021/10/poc1-dags-d-sep/).

First, Markov factorization ensures that the joint can be written in a product form
$$
P(X) = \prod_{i=1}^n P(X_{i}|PA_i).
$$
Thus, we need less parameters.

Namely, if we have a joint with $n$ binary random variables, then it would have $2^n-1$ _independent_ parameters (the last one is determined to make the sum equal to $1$). If we have $k$ factors with $n/k$ variables each, then we would have $k(2^{(n/k)}-1)$ _independent_ parameters. For $n=20, k=4$ the numbers are $1,048,576$ vs $124$. I guess you are convinced for now.


Second, the Independent Mechanism Principle ensures that the mechanisms (factors) do not influence each other. So in the case of a distributional shift (think about global warming and our temperature-altitude example), only a few mechanisms need to be retrained-in the example only $P(T\|A)$. 



# Summary
I can surely be accused of being subjective _(just check the name of this blog again)_.

>Despite the fact that causal inference can deliver us more powerful inferences and is also more data-efficient, it is not the hammer that makes us entitled to see nails everywhere.

Statistical inference is often the only way to success. We can have limited data, no clue about the underlying graph, or no time to investigate what the possible cause-effect relationships are.

>There are also situations when we **really don't care about cause and effect**.

For example, imagine an industrial inspection system of car parts. If you notice the statistical relationship between discoloration and bad quality, you don't need to know whether they are cause and effect or they have a common cause. At least, for quality management it is sufficient to throw the discolored parts out.

Of course, if you want to improve the output of the factory, you need to identify why some parts are defective.