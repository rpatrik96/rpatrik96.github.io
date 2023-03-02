---
title: 'Score functions and principal flows'
date: 2023-03-02
permalink: /posts/2023/03/2023-03-02-score-function-principal-flows
tags:
  - flows
---

# Score functions and principal flows

The score function for a probability distribution is defined as the gradient of the log density, i.e.,
 $$ \nabla_x \log p(x), $$
 which for a generative model depends on the latents.

 Assume a Gaussian density with mean $\mu$ and covariance $\Sigma$:
  $$ p(x) = \frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(x-\mu)^T\Sigma^{-1}(x-\mu)\right),$$
  where $d$ is the dimension of $x$. Let a neural network decode the latent $z$ to $\hat{x}$:
  $$ \hat{x} = f(z), $$
  where $f$ is a differentiable function. The score function is then given by
  $$ \nabla_{z} \log p(\hat{x}|x) \propto \nabla_{z} \left(-\frac{1}{2}(x- f(z))^T\Sigma^{-1}(x- f(z))\right) 
   = \dfrac{\partial}{\partial \hat{x}}\dfrac{\partial \hat{x}}{\partial z}  \left(-\frac{1}{2}(x- f(z))^T\Sigma^{-1}(x- f(z))\right) \\
   = -\dfrac{\partial f}{\partial z}^\top\Sigma^{-1}(x- f(z)). $$

   That is, the reconstruction error vector $\varepsilon = x - f(z)$ needs to be orthogonal to the Jacobian w.r.t $\Sigma$. If, as is the general case, $\Sigma$ is diagonal, then $\varepsilon \perp J_f$.

   This is similar to the notion of principal manifolds in (Cunningham et al., 2022), where is the noiseless limit, the Jacobian of the generative model describes the principal directions of the manifold.