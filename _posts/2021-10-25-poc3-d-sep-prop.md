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

A top-secret guide to d-separation. We will go deep, ready?

### PoC Post Series
-  [PoC #1: DAGs, d-separation, conditional independence](/posts/2021/10/poc1-dags-d-sep/)
- [PoC #2: Markov Factorization, Compatibility, and Equivalence](/posts/2021/10/poc2-markov/)
- ➡️ [PoC #3: The properties of d-separation](/posts/2021/10/poc3-d-sep-prop/)

# Properties of d-separation

> To be able to leverage the superpowers d-separation gave us, we need to dig deeper. _Much deeper._ 

Namely, when we manipulate probability distributions over graphs, one of our main goals is to simplify things. You probably remember such tricks from math class: making an expression complicated temporarily can give rise to a form that helps us in the long run. 

This is why we need to get familiar with the properties of d-separation (as you remember, there is a correspondence between graphs and probabilities via Markov compatibility).

This post will guide you through the five properties of d-separation. For each property, I will provide an explanation, a proof, and an example. 

>Why the proof?

I am believed that just dropping the property won't provide the insight. Besides, seeing the proof will hopefully convince you that I am talking no non-sense. Shall we begin?


As a reminder, let me show our example graph again.

![Our example graph for studying d-separation](/images/posts/d_sep_ex.svg)


## Symmetry
>$X\perp Y \| Z \implies Y\perp X \| Z$

Symmetry is the simplest property, and it won't help us much when manipulating independence statements. Nonetheless, it is important, for not all operators are symmetric.

Symmetry means that we can exchange the quantities on both sides of the independence symbol "$\perp$" without changing the meaning of the expression.

### Proof
$$
\begin{align*}
LHS: P(X|Y,Z) &= P(X|Z) \\
RHS: P(Y|X, Z) &=_{Bayes} \dfrac{P(X|Y,Z)P(Y|Z)}{P(X|Z)} \\
              &=_{LHS} \dfrac{P(X|Z)P(Y|Z)}{P(X|Z)} \\
              &= P(Y|Z)
\end{align*}
$$

In the proof, I start from the _Right-Hand Side (RHS)_ and utilize the _Left-Hand Side (LHS)_ - this is indicated by the "$LHS$" subscript of the equality sign. The goal is to get to the same (or equivalent) expression as on the right of the "$\implies$" symbol ($RHS$), which indicates our desired conclusion.

> Our general blueprint for the proofs is:
> 1. Accept the statement on the $LHS$ as true.
> 2. Start with an expression not exploiting any prior independence statement.
> 3. Utilize the $LHS$ when manipulating the expression.
> 4. Arrive at an expression equivalent to the $RHS$.

Step 2 is rather vague, I know. What you should keep in mind is that we need a starting point that is true when there is no $RHS$. Yes, this sometimes means a lot of trial and error, but I have done that part in advance (mostly the error part), so no worries.

In this proof, I started from the conditional $P(Y\|X, Z)$ and applied Bayes' Rule to smuggle in the $LHS$. As you see, this helped to simplify the expression. Indeed, as a result, we got to the desired conclusion.

### Example
In our beloved graph, symmetry means that $E\perp F \| A \implies F\perp E \| A$ and also $F\perp E \| A \implies E\perp F \| A$.


## Decomposition
>$X\perp YW \| Z \implies X\perp Y \| Z$

Decomposition means that if a variable $X$ is conditionally independent of a _set of variables_ $Y$ and $W$, then it is independent of each (note that in the expression above, the roles of $Y$ and $W$ are interchangeable - as it has no meaning which node we call $Y$ or $W$).

That is, applying decomposition gives us a _more general_ statement. Pearl describes this as if $Y$ and $W$ are together irrelevant w.r.t. $X$, then each of them (separately) is also irrelevant.

### Proof
$$
\begin{align*}
LHS: P(X|Y,W, Z) &= P(X|Z) \\
RHS: P(X,Y| Z) &= \sum_W P(X,Y,W|Z) \\
               &=_{CR} \sum_W P(X|Y,W, Z)P(Y,W|Z)\\
               &=_{LHS} \sum_W P(X|Z) P(Y,W|Z)\\
               &=P(X|Z)\sum_W P(Y,W|Z)\\
               &= P(X|Z) P(Y|Z)\\
\end{align*}
$$

This proof is slightly more tricky: namely, we are interested in the relationship between $X,Y$ and $Z$, but the original statement also includes $W$. What can we do? We can introduce $W$ and _marginalize_. Thus, the expression means the same, but has a much nicer (i.e., temporarily more complicated) form. Remember Macchiavelli: the ends justify the means.

By introducing $W$, we can exploit the $LHS$ after applying the chain rule of probability $(CR)$. Then we can notice that $P(X\|Z)$ does not depend on $W$; thus, we can take it out of the sum. As a last step, we sum out $W$ and arrive at the $RHS$, i.e.  $X\perp Y \| Z$.

### Example
The example network gives rise to the following decomposition: we can split $E \perp FB \|A$ into $E \perp B \|A$ and $E \perp F \|A$.


## Weak union
> $X\perp YW \| Z \implies X\perp Y \| ZW$

Weak union means that a variable can be moved to the right of the conditioning bar. Or as Pearl puts it: learning irrelevant (i.e., independent) information $W$ cannot make the irrelevant information $Y$ relevant to $X$. You might wonder whether _any_ variable can be introduced as evidence. Well, the problem is again the presence of v-structures.

>When an arbitrary variable is conditioned on, it may introduce additional dependencies - and weak union should hold for _all_ variables.

More precisely, if for a set of variables $X,Y, Z, W$ the relation $X\perp YW \| Z$ holds, then $X\perp Y \| ZW$ should be _always_ true. So there will be combinations where $X\not\perp YW \| Z$ - then we can say nothing about $X\perp Y \| ZW$.

How does weak union circumvent the above issue? Because $W$ is moved from the left of the conditioning bar to the right of the conditioning bar, it requires to be independent of $X$ given $Z$.
Namely, using decomposition, we can rewrite the original expression as $X\perp W \| Z$.

This statement excludes v-structures. Let's prove this by contradiction. _From now on, I will use nodes from our example._ Assume that $W=H$, i.e.,  middle node in a v-structure, whereas $X=B$ is the left node. Then, they should be dependent conditioned on _any_ variable (as there is an edge between them). So $B\not\perp H \| Z : \forall Z$ (although to falsify, we only need to find a single $Z$); thus, we have a contradiction. As a result, we cannot exploit weak union in the case of v-structures. 

>Keep in mind: the exclusion of v-structures is encoded in the formulation of weak union.

What happens if $W=K$ is a descendant of the middle node of a v-structure? Then $B\not\perp K \| Z$ still holds $\forall Z$. If $Z$ is also a descendant of the v-structure node but a parent of $W$ (i.e., $Z=J$), then $B\not\perp Y \| J$ if $Y=C$, i.e. when it is also a node in the v-structure.


### Proof
$$
\begin{align*}
LHS: P(X|Y,W, Z) &= P(X|Z) \\
RHS: P(X,Y| W, Z) &=_{CR} P(X|Y,W,Z)P(Y|W, Z) \\
               &=_{LHS} P(X|Z) P(Y|W, Z)\\
               &=_{Decomposition} P(X|W, Z) P(Y|W, Z)\\
\end{align*}
$$
The proof uses the chain rule of probability $(CR)$ to extract the $LHS$ from the $RHS$. Then we can apply the $LHS$. In the last step, we apply decomposition to smuggle in $W$. Namely, $X\perp YW \| Z$ implies $X\perp W \| Z$, i.e. $P(X|Z)=P(X|W, Z)$.

### Example
Weak union can also be demonstrated in our example graph. For example, $A \perp CK \| B$ implies that $A \perp C\|BK$ and $A \perp K\|BC$. In the former consequence, the $B\rightarrow H \leftarrow C$ v-structure becomes activated, but $B$ blocks the active path from $A$ to $K$.

## Contraction
>$X\perp Y \| Z  \land X\perp W \| ZY \implies X\perp YW \| Z$

To put the meaning of contraction into words (as of Judea Pearl): when $W$ is irrelevant to $X$ after learning the also irrelevant $Y$, then it should be irrelevant even before learning $Y$. Note that applying decomposition makes the last part of the sentence more clear, for $X\perp YW \| Z \implies X\perp W \| Z$. 

>Thus, we can say that _weak union and contraction together_ express that learning irrelevant information does not alter the relevance of any other variable.

Contraction can be thought of as the **reverse of weak union with some extras.** Namely, according to weak union,  $X\perp YW \| Z$ implies $ X\perp W \| ZY$. But as we can see, the **reverse direction needs more information**, namely $X\perp Y \| Z$. 


I think about contraction as something similar to the chain rule of probabilities. When we factorize a joint $P(X,Y) = P(X)P(Y\|X)$, then variables are on the right-hand side of the conditioning bar in some factors, whereas they also need to be on the left-hand side in some factors - remember: $P(X) = P(X\|\emptyset)$.

Writing contraction in terms of probabilities, we can observe a similar, but not identical, behavior: $P(X,Y\|Z)P(X, W\|Y, Z) \propto P(X,Y,W\|Z)$.

### Proof

#### "Similarity" to the chain rule of probabilities
$$
\begin{align*}
LHS: P(X,Y|Z) &= P(X|Z) P(Y|Z) \ \ \ \qquad\qquad (1) \\
P(X, W|Y, Z) &= P(X|Y,Z) P(W|Y,Z) \qquad (2)\\
&=_{LHS_1} P(X|Z)P(W|Y,Z)\\
RHS: P(X,Y,W|Z) &= P(X|Z) P(Y,W|Z)
 \\
 \\
P(X,Y|Z)P(X, W|Y, Z) &=  P(X|Z) P(Y|Z)P(X|Y,Z) P(W|Y,Z)\\
&= P(W|Y,Z)P(Y|Z)P(X|Z)P(X|Y,Z)\\
&=_{CR} P(Y,W|Z) P(X|Z)P(X|Y,Z)\\
&=_{LHS_1} P(Y,W|Z) P(X|Z)P(X|Z) \\
&\propto RHS \\
\end{align*}
$$

The first "proof" tries to shed light on this similarity. It starts with the product of the two expressions on the $LHS$, then uses the chain rule $(CR)$ and $LHS_1$ to produce factors present on the $RHS$. Indeed, the resulting expression has the same factors as the $RHS$ - note that as the product of the $LHS$ expressions is not the same, one factor is  included twice. 

$$
\begin{align*}
LHS: P(X|Y, Z) &= P(X|Z) \ \qquad (1) \\
     P(X|Y, W, Z) &= P(X|Y, Z) \quad (2)\\
RHS: P(X,Y, W| Z) &=_{CR} P(X|Y, W, Z)P(Y,W|Z) \\
               &=_{LHS_2} P(X|Y, Z) P(Y,W|Z)\\
               &=_{LHS_1} P(X|Z) P(Y,W|Z)\\
\end{align*}
$$

Let's prove the property itself. We start with the chain rule of probability $(CR)$ again to introduce $LHS_2$ into the $RHS$. Having applied $LHS_2$, we can now exploit $LHS_1$ to produce the $RHS$.

### Example

To show an example why the extra information is required to "reverse the weak union property", let's consider $F\perp C\|BH$. It is clear to see that $F\not\perp BC|H$ as $B$ is now not blocking the new active path the v-structure activated. We need to search for an additional conditional independence relation to apply contraction.

By checking $F\perp B\|H$ and $F\perp H\|B$ shows that $F\perp H\|B$ holds, but $F\not\perp B\|H$, so we can only apply the contraction property as $F \perp H\|B \land F\perp C\|BH \implies F \perp CH \|B$.

## Intersection (for strictly positive distributions)
> $X\perp W \| ZY  \land X\perp Y \| ZW \implies X\perp YW \| Z$

If we are not vigilant enough, we might mistakenly think that intersection is the same as contraction. Well, they are related for sure. 

>But which one is more general: intersection or contraction?

 Looking into the formulas, we might conclude that intersection is less general than contraction, as we require additional observations on the right of the conditioning bar: instead of $X\perp Y \| Z$, we have $X\perp Y \| ZW$. Plus, there is a restriction on the distribution as well. Not so fast - I hope you did not forget the black sheep of graphs? Yes, it's about v-structures _again_.

1. First, **intersection only applies for positive probability distributions**, i.e., when $\forall v\in V : P(V=v)>0$. From now on, we focus on discussing generality in the case of strictly positive distributions. As otherwise, contraction is more general, as it applies also to distributions where $P(v)=0$ is allowed.
2. In the case of intersection, extra evidence is required for $Y$ to be independent of $X$.
3. This extra evidence can establish a **less general** scenario if $W$ blocks a chain or a fork on the path between $X$ and $Y$. I.e., without conditioning on $W$, $X$ would be dependent on $Y$. This case is less general as we _need_ $W$ to induce the independence of $X$ and $Y$.
4. But conditioning on $W$ can be mean that conditional independence holds **more generally.** Namely, if it opens up a v-structure, dropping $W$ would make the independence "more strong" (what I mean here is that the $X-Y$ path would be blocked at more nodes, including at $W$). This case is more general as the independence of $X$ and $Y$ holds _despite_ conditioning on $W$.

>So neither intersection nor contraction is more general for strictly positive distributions. 

They are different. 

>The first crucial difference is that intersection requires positive distributions. You might wonder, why?

I have spent some time pondering about the same question; I tried to dig up an answer in textbooks, but I could not find any. Nevertheless, I am believed that for understanding this property, this is very important. In the following, I will try to justify this requirement during the proof.


### Proof
$$
\begin{align*}
LHS: P(X|Y, W, Z) &= P(X|Y, Z) \ \qquad (1) \\
     P(X|Y, W, Z) &= P(X|W, Z) \qquad (2)\\
RHS: P(X,Y, W| Z) &=_{CR} P(X|Y, W, Z)P(Y,W|Z) \\
               &= \begin{cases} P(X|Y, Z) P(Y,W|Z), \mathrm{when \ using\ } LHS_1\\
               P(X|W, Z) P(Y,W|Z), \mathrm{when \ using\ } LHS_2
               \end{cases} \\
               &\Downarrow \\
               P(X|Y, Z)  &= P(X|W, Z) \quad \forall X, \underline{Y,W,} Z  \\
               P(X|Z)&= P(X|Z)\\
               &\Downarrow \\
               P(X,Y, W| Z) &= P(X|Z)P(Y,W|Z)
\end{align*}
$$

The last proof of this post is a bit different from the above. This boils down to the special nature of intersection, namely, the requirement of strictly positive distributions.

We start from the $RHS$ and apply the $LHS$ - up to this point, everything is business as usual. First, we utilize the chain rule of probabilities $(CR)$- after that, things follow their own way.

The first observation we should make is that the two statements on the $LHS$ involve the same variables; hence, their starting expression (I hope not to confuse you by saying: "the $LHS$ of  $LHS_1$ and $LHS_2$" - i.e., $P(X|Y, W, Z)$) is identical.

This fact predicts that there will be two cases to investigate, as both $LHS_1$ and $LHS_2$ can be applied in the same situation. The second step in the proof investigates exactly these two cases. The implication here is that as we had a single expression - $P(X,Y, W| Z)$-, then produced two equivalent expressions - $P(X|Y, Z) P(Y,W|Z)$ and $P(X|W, Z) P(Y,W|Z)$, we can proceed by looking into the equality of both cases.

After canceling the identical $P(Y,W|Z)$, what is left is the equality of $P(X|Y, Z)$ and $ P(X|W, Z)$.

> **When simplifying, we rely on the assumption that $P(Y,W|Z)>0$.** Otherwise, it could happen that $P(X|Y, Z)$ and $P(X|W, Z)$ are not equal, but both cases still evaluate to the same value as $P(Y,W|Z)=0$ renders them $0$ - in this case, we could not drop $P(Y,W|Z)$.

The strict positive assumption should hold for all values of the variables; otherwise, we could not write $P(X|Y, Z)= P(X|W, Z)$ Thus, **we can drop $W$ and $Y$**. The reason for this is that for $X=x, Z=z$, $P(X=x|Y, Z=z)= P(X=x|W, Z=z)$ still holds for all $Y, W$. If this is true, then it remains true even if we drop $Y$ and $W$. 

>Why can we drop these variables? 

Because if the equality holds for all value combinations, then they are irrelevant, they do not change anything. Again, having the strict positivity assumption is an important safeguard as if for _some_ values $X=x$ or $Z=z$ would have $0$ probability, that would "screen off" any effect of $Y$ and $W$. Of course, as the result would evaluate to $0$, the values of $Y$ and $W$ would be still irrelevant. But when $X=x$ and $Z=z$ are not impossible (note that having a distribution that is $0$ everywhere make no sense), the effect of $Y$ and $W$ would cause problems.

Hopefully I convinced you that we can drop $Y$ and $W$; what remains is $P(X|Z)$. Substituting this back into the $RHS$, we get $P(X,Y, W| Z) = P(X|Z)P(Y,W|Z)$; thus, concluding the proof.

### Example
In our example graph, we can apply intersection to the nodes $\{B,C,F,H\}$, namely $F\perp C\|BH$ and $F\perp H\|BC$ hold, and so does $F\perp HC\|B$.


# Summary
If you are reading this, then you should be proud of yourself for staying with me until the end. This was a rather technical post - and I hope, also an "enlightening" one. I have tried to do my best to provide intuition, a formal proof, and a few examples for each property of d-separation. By synthesizing this knowledge, you will be able to manipulate probabilities to the desired form - and this will turn out to be an invaluable skill in the future.

