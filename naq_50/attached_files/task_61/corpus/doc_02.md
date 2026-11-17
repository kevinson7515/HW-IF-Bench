# Document 02
Source URL: https://arxiv.org/abs/2207.08189

---
title: Title: Supplementing Recurrent Neural Networks with Annealing to Solve Combinatorial Optimization Problems
author: Authors Shoummo Ahsan Khandoker; Jawaril Munshad Abedin; Mohamed Hibat-Allah
date: 2022-07-17
---
Condensed Matter > Disordered Systems and Neural Networks

[Submitted on 17 Jul 2022 (v1), last revised 26 Oct 2023 (this version, v2)]

Title:Supplementing Recurrent Neural Networks with Annealing to Solve Combinatorial Optimization Problems

View PDFAbstract:Combinatorial optimization problems can be solved by heuristic algorithms such as simulated annealing (SA) which aims to find the optimal solution within a large search space through thermal fluctuations. The algorithm generates new solutions through Markov-chain Monte Carlo techniques. This sampling scheme can result in severe limitations, such as slow convergence and a tendency to stay within the same local search space at small temperatures. To overcome these shortcomings, we use the variational classical annealing (VCA) framework that combines autoregressive recurrent neural networks (RNNs) with traditional annealing to sample solutions that are uncorrelated. In this paper, we demonstrate the potential of using VCA as an approach to solving real-world optimization problems. We explore VCA's performance in comparison with SA at solving three popular optimization problems: the maximum cut problem (Max-Cut), the nurse scheduling problem (NSP), and the traveling salesman problem (TSP). For all three problems, we find that VCA outperforms SA on average in the asymptotic limit by one or more orders of magnitude in terms of relative error. Interestingly, we reach large system sizes of up to $256$ cities for the TSP. We also conclude that in the best case scenario, VCA can serve as a great alternative when SA fails to find the optimal solution.

Submission history

From: Mohamed Hibat-Allah [view email][v1] Sun, 17 Jul 2022 14:33:17 UTC (185 KB)

[v2] Thu, 26 Oct 2023 23:49:16 UTC (189 KB)

Current browse context:

cond-mat.dis-nn

References & Citations

Bibliographic and Citation Tools

Bibliographic Explorer (What is the Explorer?)

Connected Papers (What is Connected Papers?)

Litmaps (What is Litmaps?)

scite Smart Citations (What are Smart Citations?)

Code, Data and Media Associated with this Article

alphaXiv (What is alphaXiv?)

CatalyzeX Code Finder for Papers (What is CatalyzeX?)

DagsHub (What is DagsHub?)

Gotit.pub (What is GotitPub?)

Hugging Face (What is Huggingface?)

Papers with Code (What is Papers with Code?)

ScienceCast (What is ScienceCast?)

Demos

Recommenders and Search Tools

Influence Flower (What are Influence Flowers?)

CORE Recommender (What is CORE?)

IArxiv Recommender

(What is IArxiv?)

arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.