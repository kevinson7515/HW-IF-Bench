# Document 05
Source URL: https://arxiv.org/pdf/2207.08189

Supplementing Recurrent Neural Networks with
Annealing to Solve Combinatorial Optimization
Problems
Shoummo Ahsan Khandoker
Department of Computer Science
BRAC University
shoummo.ahsan.khandoker@g.bracu.ac.bd
Jawaril Munshad Abedin
Department of Computer Science
BRAC University
jawaril.munshad.abedin@g.bracu.ac.bd
Mohamed Hibat-Allah
Department of Physics and Astronomy
University of Waterloo
Vector Institute for Artificial Intelligence
mohamed.hibat.allah@uwaterloo.ca
Abstract
Combinatorial optimization problems can be solved by heuristic algorithms such
as simulated annealing (SA) which aims to find the optimal solution within a
large search space through thermal fluctuations. The algorithm generates new
solutions through Markov-chain Monte Carlo techniques. This sampling scheme
can result in severe limitations, such as slow convergence and a tendency to stay
within the same local search space at small temperatures. To overcome these
shortcomings, we use the variational classical annealing (VCA) framework [ 1 ]
that combines autoregressive recurrent neural networks (RNNs) with traditional
annealing to sample solutions that are uncorrelated. In this paper, we demonstrate
the potential of using VCA as an approach to solving real-world optimization
problems. We explore VCA’s performance in comparison with SA at solving three
popular optimization problems: the maximum cut problem (Max-Cut), the nurse
scheduling problem (NSP), and the traveling salesman problem (TSP). For all three
problems, we find that VCA outperforms SA on average in the asymptotic limit
by one or more orders of magnitude in terms of relative error. Interestingly, we
reach large system sizes of up to 256 cities for the TSP. We also conclude that in
the best case scenario, VCA can serve as a great alternative when SA fails to find
the optimal solution.
1 Introduction
Combinatorial optimization is widely used in many areas of science such as physics, computer
science, and biology. It also has a wide range of applications in the industry including without
limitation to supply chain, energy, and transportation. Providing an efficient solution to combinatorial
optimization problems can boost scientific progress and provide optimal solutions to lots of industry
problems. Nevertheless, a large class of these problems is NP-Hard [ 2]. Thus, devising clever
arXiv:2207.08189v2 [cond-mat.dis-nn] 26 Oct 2023Table 2: A table of the hyperparameters used for the VCA experiments in our study.
Hyperparameter Max-Cut (Fig. 2) NSP (Fig. 3(a)) TSP (Fig. 3(b))
Architecture Dilated and
Vanilla RNN
Dilated and
Vanilla RNN
Dilated RNN with
weight sharing
Nsamples 50 (5 × 105 after
annealing)
50 (5 × 105 after
annealing)
50 (106 after annealing)
Ntrain 5 5 5
Nwarmup 1000 1000 2000
Nannealing [24, 25, ...., 214] [24, 25, ...., 214] [24, 25, ...., 214]
Learning rate 1 × 10−4 5 × 10−4 1 × 10−3
T0 2.0 2.0 2.0
RNN hidden units 40 40 40
Seed 111 111 111
Table 3: A table of the hyperparameters used for the SA experiments in this paper. Nsamples corresponds to the number of SA runs similarly to the batch size in VCA.
Hyperparameter Max-Cut (Fig. 2) NSP (Fig. 3(a)) TSP (Fig. 3(b))
Metropolis move Bit flips Bit flips Permutations (2Opt) [53]
Nsamples 50 50 50
Neq 5 5 5
Nwarmup 1000 1000 2000
Nannealing [24, 25, ...., 214] [24, 25, ...., 214] [24, 25, ...., 214]
T0 2.0 2.0 2.0
Seed 111 111 111
A Hyperparameters and Training
The VCA hyperparameters are detailed in Tab. 2. Our SA implementation is based on Metropolis
moves. At the initial temperatures T0, we perform Nwarmup warmup steps where each step corresponds
to a sweep of N Metropolis moves, where N is the number of variables. After this step, we alternate
between annealing steps (by decreasing temperature) and equilibrium steps Neq. The latter is similar
in spirit to Ntrain in VCA. The hyperparameters of SA (see Tab. 3) are chosen to be consistent with
VCA hyperparameters.
To train our RNN architectures, we minimize the variational free energy function Fλ(t) =
⟨H(X)⟩λ − T (t)S(Pλ). Here we approximate the true variational free energy at any given temperature by taking the average over Nsamples solutions sampled from the RNN distribution Pλ. This
approximation is given by
Fλ(t) ≈ 1
Nsamples
Nsamples
X
i=1
(H(Xi) + T (t) log(Pλ(Xi))) . (18)
Furthermore, the gradients of the variational free energy ∂λFλ(t) have a similar expression as shown
in Ref. [1]. We also optimize the relevant parameters λ with the Adam optimizer [52].
B Masking in TSP
To avoid revisiting the same cities during the processing of autoregressive sampling in VCA, we take
inspiration from Ref. [ 54 ], where constraints were applied in the context of quantum physics, and
from Ref. [55 ] in the context of TSP. Here we apply masking on the visited cities when computing
the conditional probabilities Pθ (ci|ci−1, . . . , c2, c1) at the level of the Softmax layer (see Eq. (13)),
where ci ∈ {1, 2, . . . , N } corresponds to the city to be visited at step i and θ are the parameters of
our model.
13Table 4: The NSP parameters used in our experiments along with (a) a ground state solution and (b) a
sub-optimal solution for NSP with D = 5, N = 2.
α λ γ W (d) F (n)
3.5 1.3 0.3 1 ⌊D/N ⌋
(a) Ground state solution X∗.
d1 d2 d3 d4 d5
n1 1 0 1 0 1
n2 0 1 0 1 0
(b) Sub-optimal solution X′.
d1 d2 d3 d4 d5
n1 1 0 1 0 0
n2 0 1 0 1 0
The masking at step i is done as follows:
• If cities (c1, c2, . . . ci−1) were visited, where cj ∈ {1, 2, . . . , N }, then
Pθ (cj |ci−1, . . . , c2, c1) is set to zero for 1 ≤ j ≤ i − 1.
• After the previous step, the conditional probability P θ (.|ci−1, . . . , c2, c1) is renormalized
to 1.
After implementing these steps, our autoregressive model generates permutations π of the cities. We
note that this masking trick can be implemented in parallel across the batch size.
C NSP Ground State Energy
Instead of deriving the ground state energy for NSP with days D = 15 and nurses N = 7, we
show near identical calculations for NSP with a relatively simpler configuration of D = 5, N = 2.
The NSP parameters used in our experiment are shown in Tab. 4. Looking at the ground state (see
Tab. 4(a)), we see that the hard nurse constraint is respected since neither nurse n1 nor nurse n2 has
to work two days in a row. Referring back to the penalty functions from Sec. 4.1, we obtain
H1(X∗) = 0.
We also know that each of the days only requires W (d) = 1 amount of workforce. Therefore, the
hard shift constraint is also satisfied since there is only one nurse assigned each day:
H2(X∗) = 0.
However, the soft nurse constraint is broken exactly once because 5%2 = 1 where % is the modulo
operator. This observation leaves exactly one day (here d5) to which a nurse will be assigned to (in
this case n1) who has to work an extra day. Therefore
H3(X∗) = 1.
Summing the penalty functions with their respective scaling, we obtain
H(X∗) = H1(X∗) + λH2(X∗) + γH3(X∗) = γ.
One can notice that it is energetically favorable to break the soft nurse constraint once than the hard
shift constraint as γ < λ, α. Thus, a solution X′ that does not have any nurse working on d5 can not
be the ground state (see Tab. 4(b)).