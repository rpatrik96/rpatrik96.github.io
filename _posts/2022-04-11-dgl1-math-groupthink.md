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

This happens when mathematicians groupthink.

### DGL Post Series


# Introduction
Machine learning operates on images, text, speech and much more. We intuitively understand that they include structure, but for most of us, this is where our knowledge stops. With  the emergence of geometric deep learning, ther is an increased need to understand.

WHen I started my B.Sc. in electrical engineering at the Budapest University of Technology and Economics in 2015, the curriculum of our "Introduction to COmputer Science" class was changed; it no longer included abstract algebra. Looking into the assigned book, I thought this to be a reasonable decision, as I could not imagine myself using groups, rings, or bodies. I still think that this was a reasonable decision for _most_ students, but I have realized that I missed a great opportunity to understand a deeper level of mathematics, and a way to connect to the real-world. 

The name "abstract algebra" and connections to the real world seem to be controversial, but I think they are not. Though having a "rotation" is more abstract than a matrix in the mathematical sense, it is a concept we can easily relate to. When I think about rotation matrices, I always associate the phyical rotation in three dimensions to have an easy-to-grasp mental concept for the mathematical description. You might object that this only works in 3D. Yes and no: though I only have access to the _real-world_ meaning of rotations in 3D, but through this I have a _general_ idea about what rotations are, so I am not baffled when I hear about 100-dimensional objects being rotated.

Geoffrey Hinton's sarcastic remark also highlights our brain's capacity to handle complex scenarios:
> To deal with a 14-dimensional space, visualize a 3-D space and say 'fourteen' to yourself very loudly. Everyone does it.

**fig about the relatoions of different objects**

In abstract algebra, we deal with sets and equip them with different relationships and properties, which we will describe with the help of operations. Operations take a number of elements from a set and map they to another element in the set. We can distinguish unary (acts on one element), binary (acts on two elements), tertiary, etc. operations. 

This is the same concept you know from programming, so we can think of them as functions with a number of inputs. Negating a boolean is a unary operator (as it changes the value of a single variable, it is a function with one input), but adding two numbers is binary (two inputs, but still one output). 

In mathematics, we can describe such functions as operations mapping from  a sequence of elements of a $H$ (i.e., we take 2 elements from $H$ for a binary operator) and to another element in $H$.

In the case of addition (for integers in this example), the Python type hints describe $H$, and we can see that our function maps $H\times H \to H$, meaning that the first parameter `x` comes from the set `int`, and so does `y`. As a result, we get another `int` with the value `x+y`.
```python
a : int = 5
b : int = 7

def add(x:int, y:int)->int:
  return x+y

```

>An operation is a function,

and as one, it can have different properties. These properties are the instructions how we can apply the operators (functions), and have a role in what symmetries are present in the $H$.

- **Associativty:** the binary operator * is associative if it admits the rearrangement of parenthesis (i.e., the order of carrying out the operations). Thus, $a*(b*c)=(a*b)*c$.
- **Commutativity:** the binary operator * is commuttive if its arguments are exchangeable (i.e., if they can switch place). Thus, $a*b=b*a$.


> \* is used as a symbol for an arbitrary operator, it does not necessarily mean multiplication.

Abstract algebraic structures are defined by the set $H$, an operator/operators and their properties. They form a hierarchy, where we get more and more valid operations. This means that more complex structures admit more "exotic" functions. Intuitively, this equals of having richer "representations" (in the machine learning sense).

>Before advancing through this hierarchy, we should ponder the question: if we can have richer representations, why would be satisfied with simpler ones? That is, why do we need simpler algebraic structures?

Complexity has its price. Thinking in terms of neural networks, a larger model is more powerful, but is harder to train, whereas the smaller one is faster, but less expressive. A convolutional network is invariant to translations, which is useful for images, but could be useless or harmful in other contexts. As we would not choose a huge model for MNIST (we would risk overfitting), we select the simplest algebraic structure that admits the lements we want. In the following, we describe our choices.

# Groups

> A set $H$ is an **associative semigroup** if it has an associative operator *. If * is also commutative, we call it a **commutative (or abelian) semigroup**.

$n\times n$ matrices are a good example for associative semigroups. They can describe linear transformations, such as rotations, translations, so even this simple structure is powerful. Though they are not **abelian** as matrix multiplication is generally not commutative. THis means that selecting the set of matrices that commute w.r.t. * is a smaller set.

Having defined an algebraic structure, we can interpret what we mean by the operator mapping $H\times H\to H$: multiplying two $n\times n$ matrices will also be an $n\times n$ matrix. That is, $H$ is closed w.r.t. *. This is not the case for all operators. IF our operator is the subtraction, then $H=\mathbb{N}$ is not a group (w.r.t -), as $(7-9)\not\in\mathbb{N},$ which violates that the result of the operator should be in the same set. In this case, _enlarging_ $H$ is the solution. If we choose $H=\mathbb{Z}$, then $H$ is closed w.r.t. subtraction.


## Topological groups

# Rings

# Grids

# Bodies





# Summary



