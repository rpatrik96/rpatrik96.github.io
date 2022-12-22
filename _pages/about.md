---
permalink: /
title: "Casual Causality"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Patrik Reizinger is a PhD student at the University of Tübingen, supervised by Wieland Brendel, Ferenc Huszár, Matthias Bethge, and Bernhard Schölkopf. He is part of the ELLIS and IMPRS-IS programs. His main research interests include causal inference and representation learning. He has done both his MSc and BSc at the Budapest University of Technology in electrical engineering and specialized in control engineering and intelligent systems.

{% include base_path %}
{% capture written_year %}'None'{% endcapture %}
{% for post in site.posts %}
  {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
  {% include archive-single.html %}
{% endfor %}

