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
It is great that we have developed the language to reason about cause and effect. Nonetheless, putting this behind fancy mathematics has its niche, too - okay, I need to admit that having concise notation and a formal framework is something I consider useful.

Now, as I have frightened the less motivated readers, we can get to the business: we want to express cause and effect with mathematics. First, to exploit the cool stuff of other branches of mathematics; second, to be able to write cryptic (but concise) statements.

## The "G"

Graphs seem to be the straightforward choice for our goal. 
>A graph $G= \{V, E\}$ is a set of vertices (nodes) $V$ and edges $E$.

Vertices are the phenomena we want to express relationship in between, whereas edges are our tool of choice to express those relationships. You can think of **nodes as random variables/probability distributions**.

The notion of a **path** will be important later on, so let's define it too:
> A **path** exists between $X$ and $Y$ if there are a set of  edges that connects $X$ to $Y$.

Thus, the "G" is motivated from "DAG", there is two more to come - with examples.

## The "D"
If we want to express that altitude $A$ has an effect of temperature $T$ then we can construct the following graph. 

![A graph of the causal relationship of altitude $A$ and temperature $T$.](/images/_posts/dag_a_t.svg)

The arrow in the above image expresses our knowledge that altitude causes temperature change (all other conditions being equal). 

We say that $A$ is a **parent** of $T$, whereas $T$ is called the **child** of **A**.

>Edge directionality implies how the joint distribution over the random variables in $V$ factorize.

In the example, we have $$P(A,T) = P(A)P(T|A),$$
and not $P(T)P(A|T)$. You can read this **Conditional Probability Distribution (CPD)** off the graph with the following procedure:
1. For each node $X$, write the variable(s)-as a node might contain multiple variables-on the _left_ of the conditioning bar
2. Then write the variables of the _parent nodes_ (the nodes with an incoming edge into $X$) to the _right_ of the conditioning bar-if none exists, as in the case of $P(A)$ in our example, the conditioning bar can be neglected. _To see that having no parents is a special case, we can also write $P(A|\emptyset)$, where we condition on the empty set $\emptyset$.


>Did you notice?

Yes, we already cleared the "D" as well: **directed means that we put arrowheads on the edges.** With this notion, we can define extend our definitions, e.g. _directed_ paths require that we go from $X$ to $Y$ by following arrowheads.  _(For those interested: undirected graphs can be useful e.g. for image segmentations with nodes of pixels and edges connecting adjacent pixels.)_

**Note:** reading the factorization off the graph gives us the causal mechanisms. If we _do not know_ $G$ then we also could have factorized in the non-causal way. So the directed edges give us the additional information we need to establish cause-effect relationships. But this is only **qualitative**, i.e., it determines child-parent relationships, but does not describe the _(quantitative)_ equations governing them. How that is done, will be left for a future post.

### Independent Causal Mechanisms (ICM)

The factorization above expresses the principle of **Independent Causal Mechanisms (ICM)** meaning that how altitude and temperature change is described by two processes: the first gives how $A$ is distributed on Earth, and the second one how $T$ evolves given a specific altitude $A=a$.

>The _"independent"_ in ICM implies that the **causal processes** (in our case, $P(A)$ and $P(T|A)$) **do not influence each other** and **they cannot provide information about each other** when **conditioned on their parents**.

The _no influence_ part implies that if you change the surface of the Earth in our example (say you want to have the biggest mountain in your backyard) then the temperature CPD $P(T|A)$ still remains the same. That is, the temperature in your backyard will change, but this is solely due to the fact of a different altitude-formulated otherwise: the temperature would be the same at a different place with the same altitude. So $P(T|A)$ **generalizes** well. 

The _no information_ claim of the ICM implies that knowing the temperature will not tell anything about the altitude-clearly, global warming also does not help. This works in the other direction as well: when knowing $T$ at a given $A=a$, we will have no clue about the location. 



## The "A"
You might wonder whether I have an unorthodox taste for spelling "DAG". Unfortunately, I do not - the only reason is that the concepts build upon each other this way. Thus, spelling bees, please forgive me.

>Acyclicity means that the graph has no loops. 

Alternatively, within a graph you cannot come back to node $A$ by following the edges and not using an edge twice. 

Imagine what would happen with our example if there would be a second edge from $T$ to $A$. This would mean that $A$ causes $T$ causes $A$ causes $T$ causes $A$ causes $T$ causes $A$ causes $T$ causes... I am feeling dizzy now and I don't like this. 

To ensure that your health won't compromise, we remove loops from causal graphs. As an additional benefit, we also cut the Gordian knot: this helps to distinguish cause from effect.


# Conditional independence
Now we have our common language to express causal relationships. It is straightforward to decide whether $X$ causes $Y$, we just need to look for a directed path $X\rightarrow Y$.

Not so fast! The real world is a bit more complicated: even if we neglect the -rather general- case of not knowing the DAG. Otherwise, a lot of scientists would be unemployed: they are working on uncovering the DAGs of our world, e.g., the influencing factors of a disease or the effects of changing economic policy. 

We can be sure that if we investigate some phenomenon, we won't get access to every information. For this sake, we will distinguish between **observed** and **unobserved** nodes.

> An **observed** node is measured, whereas the **unobserved** one is not-and this has serious consequences.

The **observed variables** are always on the **right of the conditioning bar**-if they would be on the left, then the probability would be always 1 as these are deterministic values. **Unobserved variables can be on both sides**, depending on the query made.


## Definition

So far, we discussed all the components to understand what conditional independence means, so let's dive into the details.

>$X$ is conditionally independent of $Y$ given $Z$ if it fulfills any of these three equalities:
>- $P(X| Y, Z) = P(X|Z)$
>- $P(Y |X, Z) = P(Y|Z)$
>- $P(X, Y| Z) = P(X|Z)P(Y|Z)$

### Example

For example, the first statement means that if we have access to $Z$ then the distribution of $X$ does not depend on $Y$; with an example: when you see the train coming (this is $Z$) then the time of arrival $X$ does not depend on the train schedule $Y$. Namely, your eyes give you the information about the arrival time of the train to pick you up, so the schedule cannot provide you further information. 

This does not mean that the schedule is useless, only that seeing the train gives you all information the schedule could have provided. If the weather is foggy and you neither see nor hear the train, then your only help is the schedule.

### Notation
Congratulations, you have made it so far! You are about to come across the first proof of why I like mathematics: they figure out concise ways to express concepts. Here comes how it is done with condtional independence. 

>The conditional independence statement $X$ is independent of $Y$ given $Z$ is often denoted as $X\perp Y | Z$, where "$\perp$" stands for "independent of". Respectively, "$\not\perp$" means dependent of.



## Marginal independence

A special case of conditional independence is **marginal independence**, where $Z=\emptyset$, i.e., there is nothing observed but some independencies still hold. An example is that the arrival time of the train is independent from the color of the train (I hope there is no study connecting the two, because then I am screwed - I searched for it in Google Scholar I promise).

>"Independent" will mean "marginally independent"-when it is about conditional independence, I will state that explicitly.

Now we know what conditional independence means on the level of probability distributions, but what does this imply to graphs?



# d-separation
>First, what the heck means the "d" in the name?

d stands for _directional_-as you have guessed, this notion applies to directed graphs. As we talk about DAGs, we are good to go after making this _quintessential_ point.

## Graph structures
First we need to define the building blocks of DAGs. Interestingly, with only three three-node graphs you can build anything that is allowed in DAGs. These three are:
- **Chains** ($X\rightarrow Z\rightarrow Y$):, where $Z$ is called the _mediator_ node, as it "transfers" (mediates) the effect of $X$ to $Y$ via $Z$. An example for this structure is when you set $X$ to be smoking, $Z$ to the tar deposits in the lungs, and $Y$ to lung cancer.
- **Forks** ($X\leftarrow Z \rightarrow Y$): forks represent a relationship where the $X$ and $Y$ nodes have the same parent $Z$. When you toss a coin twice, then the result of your tosses will be $X$ and $Y$, whereas $Z$ will represent the probability of the coin coming up heads. 
- **v-structures** ($X\rightarrow Z \leftarrow Y$) : spoiler alert! if I would be a v-structure at Halloween, I would _always_ opt for a trick. v-structures are the most interesting and they can cause problems in practice, as I will elaborate in an example right in the next section. An example for a v-structure is when $X$ represents a broken collarbone, $Y$ severe bronchitis whereas $Z$ indicates hospitalization, i.e., the effect has multiple causes.

## The fallacy of v-structures 

v-structures are nasty things; what they do is known under the names of **explaining away/selection bias/Berkson's paradox**. The three different phrases for the same phenomenon should imply how consequential v-structures are. 

Going back to the broken collarbone ($X$)-bronchitis ($Y$)-hospitalization ($Z$) example, think about the following: if you know that $Z=true$ (someone is hospitalized) and $X=true,$ (broken collarbone) what can you say about the conditional probabilities, horribile dictu, the independencies of the graph?

>Formulated otherwise: how do the probabilities $P(Y|X=true, Z=true)$ and $P(Y|Z=true)$ compare?

It might feel counterintuitive, but knowing that someone is hospitalized with a broken collarbone **decreases the probability* of a severe bronchitis. As if someone broke a collarbone, then that is sufficient to be admitted to a hospital (as severe bronchitis also would be).

>Wait a second! Does this mean that v-structures can **make formerly independent random variables dependent**? Oh, yeah, this is the trick. 

### Example

How does this work? Light can be shed by decoding two of the names. We can say that among hospitalized patients, a broken collarbone *explains away* the probability of severe bronchitis - as we know that some hospitalized patient broke her/his collarbone, then we can be quite certain that (s)he has no bronchitis.

>You might ask: why?

To answer this, I will walk you through the hospitalization example numerically. All of the variables $X, Y, Z$ are binary ($1$ means that the condition is present and $0$ means that it is absent); we will assume the following truth table:



|  $X$ | $Y$  |  $P(Z\|X,Y)$| 
|---|---|---|
| $0$  |  $0$ |  $0.002$   |   
|  $0$ | $1$  |  $0.5$     |   
|  $1$ |  $0$ |  $0.8$     |   
|  $1$ | $1$  |  $0.95$    |   


Also assume that we know the marginal probability of hospitalization in the general population, $P(Z=1)=0.01$. That is, if any of $X$ or $Y$ is present, then the patient is hospitalized with an increased probability, but if none is present, then the probability of hospitalization decreases, as we would expect. 

What we are interested in is the _relationship_ of the probability of a broken collarbone given a hospitalized patient and bronchitis -$P(X=1|Y=1, Z=1)$- and the probability of a broken collarbone in a hospitalized patient - $P(X=1|Z=1)$. 

Before writing down equations, let's ask the question: 
>What do we expect? 

If we believe that v-structures work just as I mentioned above, then $P(X=1|Y=1, Z=1)$ should be smaller than $P(X=1|Z=1)$.

What we need is to write down their ratio and use Bayes' Rule

$$\begin{align*} \dfrac{P(X=1|Y=1, Z=1)}{P(X=1|Z=1)} &= \dfrac{\dfrac{P(Z=1|X=1, Y=1)P(X=1|Y=1)}{P(Z=1|Y=1)}}{\dfrac{P(Z=1|X=1)P(X=1)}{P(Z=1)}}
\end{align*}
$$

As we have a v-structure in the form of $X \rightarrow Z \leftarrow Y$, this implies that $P(X|Y) = P(X)$ - although $Z$ is observed, it is not in this expression, so we don't need to worry about that. 

The above expression simplifies to:
$$\begin{align*} \dfrac{P(X=1|Y=1, Z=1)}{P(X=1|Z=1)} &= \dfrac{\dfrac{P(Z=1|X=1, Y=1)\sout{P(X=1|Y=1)}}{P(Z=1|Y=1)}}{\dfrac{P(Z=1|X=1)\sout{P(X=1)}}{P(Z=1)}}\\
&= \dfrac{P(Z=1|X=1, Y=1)}{P(Z=1|Y=1)}\dfrac{P(Z=1)}{P(Z=1|X=1)}
\end{align*}
$$ 

Before substituting in the numbers, let's do two things:
1. **Investigate both fractions:** the _first fraction_ is clearly **bigger than $1$** as if someone has _both_ bronchitis and a broken collarbone, then it is more probable that (s)he gets hospitalized than  someone with "only" bronchitis. The second fraction is **less than $1$** as the probability of hospitalization without any condition is less than the probability of hospitalization if there is a broken collarbone.
2. **Look into the edge case:** let's assume that the healthcare system where the hospitalization of the patient is considered is extremely well-equipped, well-funded, and has the best medical staff (both professionally and personally). As they want to help everyone, if someone has any of $X$ or $Y$, then the patient will be admitted to the hospital. I.e., $Z$ becomes $X \vee Y$, meaning that if any of $X$ or $Y$ equals 1, then $Z$ occurs with probability one. For our numerical example, this means that $P(Z=1|X=1, Y=1) = P(Z=1|X=1) =P(Z=1| Y=1) =1.$ What remains is $P(Z)$ in the above fraction, which is less than 1. So even in this edge case, we have shown that $P(X=1|Y=1, Z=1)<P(X=1|Z=1)$.

Coming back to the numerical example, when we calulcate the above fractions, we get:

$$\begin{align*} \dfrac{P(Z=1|X=1, Y=1)}{P(Z=1|Y=1)}\dfrac{P(Z=1)}{P(Z=1|X=1)} &= \dfrac{0.95}{0.5}\times \dfrac{0.01}{0.9}\\
&=1.9\times 0.0125 = \underline{0.02375}
\end{align*}
$$

> So v-structures _really_ introduce dependencies when we condition on the middle node.

 Stated differently: if we _select_ hospitalized people, then we introduce a _dependence between two marginally independent phenomena_. The counterintuitive nature arises from these two conditions being _marginally independent_ in the general population. 


To summarize this example, we can say that $X$ and $Y$ are marginally independent, but they are conditionally dependent given (i.e., observing) $Z$.

Similar to you, I have also found this at first very counterintuitive - the name Berkson's paradox also supports the notion how unbelievable this phenomenon seems at first. 

_I would like to encourage you to listen to the podcast below made by the incredible guys at Stuff You Should Know (SYSK), which discusses the different biases (including the very same selection bias) scientists-and, in my opinion, everyone-should be aware of. If you are not familiar with SYSK, it is not a technical podcast but it still can entertain and inform you about interesting topics. Disclaimer: I have no affiliation with SYSK, I am just a listener who enjoys what they do and who stands up for making science accessible to everyone._

<iframe allow="autoplay" width="100%" height="200" src="https://www.iheart.com/podcast/105-stuff-you-should-know-26940277/episode/research-bias-sort-it-out-science-87649867/?embed=true" frameborder="0"></iframe>

## d-separation
>Our goal is to make statements about the conditional independence of nodes in a DAG, given some evidence. d-separation will come handy for this purpose.

First, we need to define what a **blocked path** is.
> A path $p$ from $X$ to $Y$ in DAG $G$ is blocked given $Z$ if regarding all three-tuples of **adjacent** nodes
> -  the middle node of chains and forks in $p$ is in $Z$ **and**
> - either the middle node of a v-structure (hospitalization in our example), or its descendants are not in $Z$.
>
> _Note:_ $Z$ can be a set of nodes, not just a single node.

I used the notion of descendants of a node in the definition, but have not defined it before: 
>A **descendant** of a node consists of its children and the children of children etc.

Knowing what a blocked path is, we can define **d-separation** as follows:
> $X$ is **d-separated** from $Y$ given $Z$ if $Z$ blocks all paths between $X$ and $Y$.

Formulated in a different way: d-separation means that you cannot go from $X$ to $Y$ without _either_ going through a chain or fork whose middle node is in $Z$ _or_ going through a v-structure whose middle node (or any of the middle node's descendants) is not in $Z$.

The notation for d-separation is not unique in the literature; sometimes $d-sep(X,Y|Z)$ is used, but as there is a correspondence between conditional independence and d-separation, I will use the same notation (i.e., $X\perp Y|Z$), or if I want to stress that it holds in a graph, then I will use the symbol $\perp_G$.

_Note: Conditional independence and d-separation are **not exactly** the same - to find out more about the difference and the properties of d-separation, stay tuned for my next post!_

### Parting example
I won't leave you with the mess I probably created in your heads without an effort to clear it up, so it's time for an example!
For this purpose, I hand-crafted a particularly random DAG that includes all kind of structures.

![Our example graph for studying d-separation](/images/_posts/d_sep_ex.svg)

>What d-separation statements can we read off this graph?

We need to apply the definition to figure this out, given the (set of) observed nodes.

#### When $A$ is observed
There are three affected forks in this case: by picking any two nodes from $\{B,E,F\}$, they will be d-separated given $A$.
For example, as $E\leftarrow A\rightarrow F$ is a fork, $E\perp_G F |A$ holds. So do
- $B\perp_G E |A$ and
- $B\perp_G F |A$.

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

You get the idea.

#### When $J$ is observed
Beware the v-structure! Although not the middle node of the v-structure, but its child $J$ is observed, dependencies are still introduced. So:
- $A \not\perp_G C | J$
- $B \not\perp_G C | J$



# Summary

This post covered the grounds and established a common vocabulary for our journey. DAGs are a powerful building block to reason about causality, but they are not the Holy Grail. I will look into their limitations and the properties of d-separation in the next post. As I promised, I will also highlight the difference between d-separation and conditional independence.


