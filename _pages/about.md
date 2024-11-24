---
permalink: /
title: "Casual Causality"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am a final-year Ph.D. student in the Robust Machine Learning group at the Max Planck Institute of Intelligent Systems in Tübingen, supervised by Wieland Brendel, Ferenc Huszár, Matthias Bethge, and Bernhard Schölkopf. I am part of the [ELLIS](https://ellis.eu/phd-postdoc) and [IMPRS-IS](http://imprs.is.mpg.de/) programs. 

**I am actively looking for postdoctoral and junior group leader positions, starting in early 2026.**

The main motivation for my research is to advance our **understanding of how and why deep learning models work**. 
My research toolkit currently focuses around _identifiable causal and self-supervised representation learning_ and _out-of-distribution (OOD) generalization,_ with a focus on _compositionality in language models_. During my Ph.D., I [realized](https://openreview.net/forum?id=pVyOchWUBa) that current machine learning theory is insufficient to explain especially the interesting and useful properties of deep neural networks. 
I aim to help close this gap, by focusing on:
- extending machine learning theory to understand the role of inductive biases (e.g., model architecture or optimization algorithm)
- grounding machine learning in the physical world via (causal) principles and humanity's prior knowledge
- extending our understanding of out-of-distribution and compositional generalization
- uncovering overarching patterns across different fields in machine learning


I have done both my M.Sc. and B.Sc. at the Budapest University of Technology in electrical engineering and specialized in control engineering and intelligent systems. In my free time, I enjoy being outdoors and often bring my [camera](https://500px.com/p/rpatrik96) with me.

{% include base_path %}
{% capture written_year %}'None'{% endcapture %}
{% for post in site.posts %}
  {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
  {% include archive-single.html %}
{% endfor %}

