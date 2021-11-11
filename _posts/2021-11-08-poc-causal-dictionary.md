---
title: 'Pearls of Causality: The Causal Dictionary'
date: 2021-10-31
permalink: /posts/2021/10/poc-causal-dictionary/
tags:
  - causality
  - DAG
  - Markov
 
---

No one told me that I need a dictionary for learning causal inference. Indeed, there was none before. Now there is.

### PoC Post Series
- [PoC #1: DAGs, d-separation, conditional independence](/posts/2021/10/poc1-dags-d-sep/)
- [PoC #2: Markov Factorization, Compatibility, and Equivalence](/posts/2021/10/poc2-markov/)
- [PoC #3: The properties of d-separation](/posts/2021/10/poc3-d-sep-prop/)
- [PoC #4: Causal Queries](/posts/2021/11/poc4-causal-queries/)
- [PoC #5: Statistical vs Causal Inference](/posts/2021/11/stats-vs-causality/)
- [PoC #6: Markov Conditions](/posts/2021/11/poc6-markov-conditions/)
- [PoC #7: Latents and Inferred Causation](/posts/2021/11/poc6-latents-stability-ic/)


# The Causal Dictionary

|  Concept | Names  |  Reference| 
|---|---|---|
| DAG-distribution correspondence  |  - Markov compatibility<br>-  I-map |   [PoC#2](/posts/2021/10/poc2-markov/) |   
| Qualitative child-node relationships  |  - Structural Equation Model (SEM)<br>- Structural Causal Model (SCM)<br>- Functional Causal Model (FCM)<br>- Causal  Model|   [PoC #4](/posts/2021/11/poc4-causal-queries/) |  
| Causal source (determined by the environment)  |  - Exogenous variable<br>- Noise/Disturbance/Error variable<br>- Independent variable<br>- Causal variable|   [PoC #4](/posts/2021/11/poc4-causal-queries/) |   
| Causal observation (determined by the model)  |  - Endogenous variable<br>- Dependent variable<br>- Observed variable|   [PoC #4](/posts/2021/11/poc4-causal-queries/) |   
| Graph induced by structural equations  |  - Causal structure<br>- Causal diagram|   [PoC #4](/posts/2021/11/poc4-causal-queries/) |   
| Relation of independencies between the $G$ and $P$ belonging to a causal model  |  - Stability<br>- Faithfulness<br>- DAG-isomorphism<br>- Perfect-mapness|   [PoC #7](/posts/2021/11/poc6-latents-stability-ic/) |
| Unobserved common cause  |  - Confounder<br>- Unobserved common cause |   A future post |

