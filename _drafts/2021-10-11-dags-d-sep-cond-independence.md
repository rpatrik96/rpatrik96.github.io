---
title: 'Pearls of Causality #1: DAGs, d-separation, conditional independence'
date: 2021-10-11
permalink: /posts/2021/10/poc1-dags-d-sep-cond-independence/
tags:
  - causality
  - DAG
  - d-separation
  - conditional-independence
  - Pearl
---

d-separation is the bread and butter for deciding about conditional independence in DAGs. What is a DAG, anyway?


# Directed Acyclic Graphs (DAGs)
It is great that we have developed the language to reason about cause and effect. Nonetheless, putting this behind fancy mathematics has its niche, too - okay, I need to admit that having concise notation and a formal framework is something I consider more useful.

Now, as I have frightened the less motivated readers, we can get to the business: we want to express cause and effect with mathematics. First, to exploit the cool stuff of other branches of mathematics; second, to be able to write cryptic (but concise) statements.

## The "G"

Graphs seem to be the straightforward choice for our goal, as a graph $G= \{V, E\}$ is a set of vertices (nodes) $V$ and edges $E$. Vertices are the phenomena we want to express relationship in between, whereas edges are our tool of choice to express those relationships. You can think of **nodes as random variables/probability distributions**.

Thus, the "G" is motivated from "DAG", there is two more to come - with examples.

## The "D"
If we want to express that altitude $A$ has an effect of temperature $T$ then we can construct the following graph. 

![A graph of the causal relationship of altitude $A$ and temperature $T$.](/images/_posts/dag_a_t.svg)

The arrow in the above image expresses our knowledge that altitude causes temperature change (all other conditions being equal). 

We say that $A$ is a **parent** of $T$, whereas $T$ is called the **child** of **A**.

>Edge directionality implies how the joint distribution over the random variables in $V$ factorize.

In the example, we have $$P(A,T) = P(A)P(T|A),$$
and not $P(T)P(A|T)$. You can read this **Conditional Probability Distribution (CPD)** off the graph with the following procedure:
1. For each node $X$, write the variable(s) -as a node might contain multiple variables-on the _left_ of the conditioning bar
2. Then write the variables of the _parent nodes_ (the nodes with an incoming edge into $X$) to the _right_ of the conditioning bar-if none exists, as in the case of $P(A)$ in our example, the conditioning bar can be neglected. _To see that having no parents is a special case, we can also write $P(A|\emptyset)$, where we condition on the empty set $\emptyset$.


>Did you notice?

Yes, we already cleared the "D" as well: **directed means that we put arrowhead on the edges.** _(For those interested: undirected graphs can be useful e.g. for image segmentations with nodes of pixels and edges expressing when pixels are adjacent.)_

**Note:** reading the factorization off the graph gives the causal mechanisms. If we _do not know_ $G$ then we also could have factorized in the non-causal way. So the directed edges gives us the additional information we need to establish cause-effect relationship. But this is only **qualitative**, i.e., it determines child-parent relationships, but does not describe the _(quantitative)_ equations governing them. How that is done, will be left for a future post.

### Independent Causal Mechanisms (ICM)

The factorization above expresses the principle of **Independent Causal Mechanisms (ICM)** meaning that how altitude and temperature change is described by two processes: the first gives how $A$ is distributed on Earth, and the second one how $T$ evolves given a specific altitude $A=a$.

>The _"independent"_ in ICM implies that the **causal processes** (in our case, $P(A)$ and $P(T|A)$) **do not influence each other** and **they cannot provide information about each other** when **conditioned on their parents**.

The _no influence_ part implies that if you change the surface of the Earth in our example (say you want to have the biggest mountain in your backyard) then the temperature CPD $P(T|A)$ still remains the same. That is, the temperature in your backyard will change, but this is solely due to the fact of a different altitude-formulated otherwise: the temperature would be the same at a different place with the same altitude. So $P(T|A)$ **generalizes** well. 

The _no information_ claim of the ICM implies that knowing the temperature will not tell anything about the altitude-clearly, global warming also does not help. This work in the other direction as well: when knowing $T$ at a given $A=a$, we will have no clue about the location. 



## The "A"
You might wonder whether I have an unorthodox taste for spelling "DAG". Unfortunately, I do not - the only reason is that the concepts build upon each other this way. Thus, spelling bees, please forgive me.

>Acyclicity means that within a graph you cannot come back to node $A$ by following the arrowheads. Alternatively, the graph has no loops.

Imagine what would happen with our example if there would be a second edge from $T$ to $A$. This would mean that $A$ causes $T$ causes $A$ causes $T$ causes $A$ causes $T$ causes $A$ causes $T$ causes... I am feeling dizzy now and I don't like this. 

To ensure that your health won't compromise, we remove loops from causal graphs. As an additional benefit, we also cut the Gordian knot: this makes possible to distinguish cause from effect.


# Conditional independence
Now we have our common language to express causal relationships. It is straightforward to decide whether $X$ causes $Y$, we just need to look for a directed path $X\rightarrow Y$.

>Not so fast!

The real world is a bit more complicated: even if we neglect the -rather general- case of not knowing the DAG. Otherwise, a lot of scientist would be unemployed: they are working on uncovering the DAGs of our world, e.g. what are the influencing factors of a disease or what happens when the economic policy changes in a particular way. 

We can be sure that if we investigate some phenomenon, we won't get access to every information. For this sake, we will distinguish between **observed** and **unobserved** nodes.

> An **observed** node is measured, whereas the **unobserved** one is not-and this has serious consequences.

The **observed variables** are always on the **right of the conditioning bar**-if they would be on the left, then the probability would be always 1 as these are deterministic values. **Unobserved variables can be on both sides**, depending on the query made.

Assume that $Z$ is observed and we are interested in 

- cond ind with distributions

# d-separation
>First, what the heck is the "d" in the name?

d stands for _directional_-as you have guessed, this notion applies to directed graphs. As we talk about DAGs, we are good to go after making this quintessential point.

## Graph structures

- chains
- forks
- v-structures (Berkson's paradox, selection bias)

- d-sep vs cond ind

- d-sep properties with **intuitive examples**

