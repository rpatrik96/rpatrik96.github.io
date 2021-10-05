---
title: 'DAGs, d-separation, conditional independence'
date: 2021-10-11
permalink: /posts/2021/10/dags-d-sep-cond-independence/
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

Graphs seem to be the straightforward choice for our goal, as a graph $G= \{V, E\}$ is a set of vertices (nodes) $V$ and edges $E$. Vertices are the phenomena we want to express relationship in between, whereas edges are our tool of choice to express those relationships. 

The "G" is motivated from "DAG", there is two more to come - with examples.

## The "D"
If we want to express that altitude $A$ has an effect of temperature $T$ then we can construct the following graph. 

![A graph of the causal relationship of altitude $A$ and temperature $T$.](/images/_posts/dag_a_t.svg)

The arrow in the above image expresses our knowledge that altitude causes temperature change (all other conditions being equal).

>Did you notice?

Yes, we already cleared the "D" as well: directed means that we put arrowhead on the edges. _(For those interested: undirected graphs can be useful e.g. for image segmentations with nodes of superpixels and edges expressing when superpixels are adjacent.)_

## The "A"
You might wonder whether I have an unorthodox taste for spelling "DAG". Unfortunately, I do not - the only reason is that the concepts build upon each other this way. Thus, spelling bees, please forgive me.

>Acyclicity means that within a graph you cannot come back to node $A$ by following the arrowheads. Alternatively, the graph has no loops.

Imagine what would happen with our example if there would be a second edge from $T$ to $A$. This would mean that $A$ causes $T$ causes $A$ causes $T$ causes $A$ causes $T$ causes $A$ causes $T$ causes... I am feeling dizzy now. 

To ensure that your health won't compromise, we remove loops from causal graphs. As an additional benefit, we also cut the Gordian knot: this makes possible to distinguish cause from effect.


# Conditional independence

# d-separation
>First, what the heck is the "d" in the name?

