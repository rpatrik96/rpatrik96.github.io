---
title: 'Pearls of Causality #1: DAGs, d-separation, conditional independence'
date: 2021-10-11
permalink: /posts/2021/10/poc1-dags-d-sep/
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

The notion of a **path** will be important later on, so let's define it:
> A **path** exists between $X$ and $Y$ if there are a set of directed edges that connects $X$ to $Y$.

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

Not so fast! The real world is a bit more complicated: even if we neglect the -rather general- case of not knowing the DAG. Otherwise, a lot of scientist would be unemployed: they are working on uncovering the DAGs of our world, e.g. what are the influencing factors of a disease or what happens when the economic policy changes in a particular way. 

We can be sure that if we investigate some phenomenon, we won't get access to every information. For this sake, we will distinguish between **observed** and **unobserved** nodes.

> An **observed** node is measured, whereas the **unobserved** one is not-and this has serious consequences.

The **observed variables** are always on the **right of the conditioning bar**-if they would be on the left, then the probability would be always 1 as these are deterministic values. **Unobserved variables can be on both sides**, depending on the query made.

Alright, we discussed all the components to understand what conditional independence means, so let's dive into the details.

$X$ is conditionally independent of $Y$ given $Z$ if it fulfills any of these three equalities:
- $P(X| Y, Z) = P(X|Z)$
- $P(Y |X, Z) = P(Y|Z)$
- $P(X, Y| Z) = P(X|Z)P(Y|Z)$

For example, the first statement means that if we have access to $Z$ then the distribution of $X$ does not depend on $Y$; with an example: when you see the train coming (this is $Z$) then your time of departure $X$ does not depend on the train schedule $Y$. Namely, your eyes give you the information about the arrival time of the train to pick you up, so the schedule cannot provide you further information about when will you depart.

>The conditional independence statement $X$ is independent of $Y$ given $Z$ is often denoted as $X\perp Y | Z$, where "$\perp$" stands for "independent of". Respectively, "$\not\perp$" means dependent of.

A special case of conditional independence is **marginal independence**, where $Z=\emptyset$, i.e., there is nothing observed. An example is that the arrival time of the train is independent from the color of the train (I hope there is no study connecting the two, because then I am screwed - I searched for it in Google Scholar I promise).

>"Independent" will mean "marginally independent"-when it is about conditional independence, I will state that explicitly.

Now we know what conditional independence means on the level of probability distributions, but what does this imply to graphs?



# d-separation
>First, what the heck is the "d" in the name?

d stands for _directional_-as you have guessed, this notion applies to directed graphs. As we talk about DAGs, we are good to go after making this quintessential point.

## Graph structures
First we need to define the building blocks of DAGs. Interestingly, with only three three-node graphs you can build anything what is allowed in DAGs. These three are:
- **Chains** ($X\rightarrow Z\rightarrow Y$):, where $Z$ is called the _mediator_ node, as it "transfers" (mediates) the effect of $X$ to $Y$ via $Z$. An example for this structure is when you set $X$ to be smoking, $Z$ to the tar deposits in the lungs, and $Y$ to lung cancer.
- **Forks** ($X\leftarrow Z \rightarrow Y$): forks represent a relationship where the $X$ and $Y$ nodes have the same parent $Z$. When you toss a coin twice, then the result of your tosses will be $X$ and $Y$, whereas $Z$ will represent the probability of the coin coming up heads 
- **v-structures** ($X\rightarrow Z \leftarrow Y$) : spoiler alert! if I would be a v-structure at Halloween, I would _always_ opt for a trick. v-structures are the most interesting and they can cause the most problems in practice, as I will elaborate in an example right in the next section. Assume that $X$ represents a broken collarbone, $Y$ a broken leg, whereas $Z$ indicates hospitalization.

## The fallacy of v-structures 

v-structures are nasty things; what they do is known under the names of **explaining away/selection bias/Berkson's paradox**. The three different phrases for the same phenomenon should show how consequential v-structures are. 

Going back to the broken collarbone ($X$)-broken leg ($Y$)-hospitalization ($Z$) example, think about the following: if you know that $Z=true$ hospitalized and $X=true,$ what can you say about $P(Y)?$

>Formulated otherwise: how do the probabilities $P(Y|X=true, Z=true)$ and $P(Y|Z=true)$ compare?

It might feel counterintuitive, but knowing that someone is hospitalized with a broken collarbone **decreases the probability* of a broken leg. As if someone broke a collarbone, then that is sufficient to be admitted to a hospital (as a broken leg also would be).

>Wait a second! Does this means that v-structures can **make formerly independent random variables dependent**? Oh, yeah, this is the trick. 

How does this work? Light can be shed by decoding two of the names. We can say that among hospitalized patients, a broken collarbone *explains away* the probability of a broken leg. Stated differently: if we _select_ hospitalized people, then we uncover a _dependence between two marginally independent phenomena_. Namely, in the general population, these two conditions are _marginally independent_. 

_Let's not dive into the discussion of "if you had an accident, it is more probable that you broke everything" - assume for this example that different bones are broken in different situations._

To summarize this example, we can say that $X$ and $Y$ are marginally independent, but they are conditionally dependent given (i.e., observing) $Z$.

Similar to you, I have also found this at first very counterintuitive - the name Berkson's paradox also supports the notion how unbelievable this phenomenon seems at first. 

I would like to encourage you to listed to the podcast below made by the incredible guys at Stuff You Should Know (SYSK), which discusses the different biases (including the very same selection bias) scientists-and, in my opinion, everyone-should be aware of. If you are not familiar with SYSK, it is not a technical podcast but it still can entertain and inform you about interesting topics.

<iframe allow="autoplay" width="100%" height="200" src="https://www.iheart.com/podcast/105-stuff-you-should-know-26940277/episode/research-bias-sort-it-out-science-87649867/?embed=true" frameborder="0"></iframe>

## d-separation
>Our goal is to make statements about the conditional independence of nodes in a DAG, given some evidence. d-separation will come handy for this purpose.

For this purpose, we need to define what an **active path** is.
> A path $p$ from $X$ to $Y$ in DAG $G$ is active if regarding all three-tuples of **adjacent** nodes
> -  the middle node of chains and forks in $p$ is not in $Z$ **and**
> - neither the middle node of a v-structure (hospitalization in our example), nor its descendants are in $Z$.

I used the notion of descendants of a node in the definition, but have not defined it before: a **descendant** of a node consists of its children and the children of children etc.

Knowing what an active path is, we can define **d-separation** as follows:
> $X$ is **d-separated** from $Y$ given $Z$ if $Z$ block all active paths between $X$ and $Y$.

Formulated in a different way: d-separation means that you cannot go from $X$ to $Y$ without _either_ going through a chain or fork whose middle node is not in $Z$ _or_ going through a v-structure whose middle node (or any of the middle node's descendants) is in $Z$.

The notation for d-separation is not unique in the literature; sometimes $d-sep(X,Y|Z)$ is used, but as there is a correspondence between conditional independence and d-separation, I will use the same notation (i.e., $X\perp Y|Z$), or if I want to stress that it holds in a graph, then I will use the symbol $\perp_G$.

_Note: Conditional independence and d-separation are **not exactly** the same - to find out more about the difference and the properties of d-separation, stay tuned for my next post!_

### Parting example
I won't leave you with the mess I probably created in your heads without an effort to clear it up, so it's time for an example!
For this purpose, I hand-crafted a particularly random DAG that includes all kinds of structures.

![Our example graph for studying d-separation](/images/_posts/d_sep_ex.svg)

>What d-separation statements can we read off this graph?

#### When $A$ is observed
There are three more forks in this case: by picking any two nodes from $\{B,E,F\}$, they will be d-separated given $A$.
For example, as $E\leftarrow A\rightarrow F$ is a fork, $E\perp_G F |A$ holds. 

#### When $B$ is observed
Observing $B$ cuts the graph into two parts by severing the active path in the chain $A\rightarrow B \rightarrow H$ so any of the following is true:
- $A \perp_G H | B$
- $A \perp_G C | B$
- $A \perp_G H | B$
- $E \perp_G C | B$
- $E \perp_G J | B$
- $E \perp_G J | B$
- $F \perp_G H | B$
- $F \perp_G C | B$
- $F \perp_G J | B$

##$## When $J$ is observed
Beware the v-structure! Athough not the middle node of the v-structure, but its child $J$ is observed, dependencies are still introduced. So:
- $A \not\perp_G C | J$
- $B \not\perp_G C | J$

# Summary

This post covered the grounds and established a common vocabulary for our journey. DAGs are a powerful building block to reason about causality, but they are not the Holy Grail. I will look into their limitations, the d-separation and conditional independence difference, and the properties of d-separation in the next post.


