---
permalink: /
title: "Casual Causality"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am a Ph.D. student at the University of Tübingen, supervised by Wieland Brendel, Ferenc Huszár, Matthias Bethge, and Bernhard Schölkopf. I am part of the [ELLIS](https://ellis.eu/phd-postdoc) and [IMPRS-IS](http://imprs.is.mpg.de/) programs. My main research interests include causal representation learning and identifiability. I have done both my M.Sc. and B.Sc. at the Budapest University of Technology in electrical engineering and specialized in control engineering and intelligent systems. In my free time, I enjoy being outdoors and often bring my [camera](https://500px.com/p/rpatrik96) with me.

{% include base_path %}
{% capture written_year %}'None'{% endcapture %}
{% for post in site.posts %}
  {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
  {% include archive-single.html %}
{% endfor %}

