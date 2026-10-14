# Erdős Problem #757: final report (living document; updated at every checkpoint)

Last updated: 2026-10-14 06:55 UTC (elapsed about 7.8 of 72 budget hours). Status of the goal clauses at
this update: (A) no new record set; (B) no new lower-bound proof; (C) budget not yet exhausted.

## 1. Result summary

The published bounds $9/17\le c_*\le 4/7$ (Ma–Tang 2026, via Henning–Yeo 2021 and the 14-point set
$A_{\rm base}$) are unchanged by this run so far. The run produced the following verified partial results
(evidence paths in results/LEDGER.md and kb/known_results.md, rows K30–K34):

1. **Exact structure of (4,5)-sets beyond the published lemmas** [verified-here, with one-line proofs]:
   - **K30, monotone midpoints.** For APs $(i,j,k)$, $(i',j',k')$ in rank order with $i\le i'$, $k\le k'$,
     $(i,k)\ne(i',k')$: $j<j'$.
   - **K31, no medial triangle.** Three APs pairwise meeting in shared *endpoints* force a parallelogram
     ($x_q-x_p=(x_c-x_a)/2=x_b-x_a$), so they never occur. Likewise the medial 4-cycle (Varignon) is
     forbidden in every order (K33).
   - **Forbidden-configuration library.** All ordered midpoint patterns on $\le 8$ vertices were classified
     exactly (46,281 patterns at $n=8$: 16,568 realizable, 28,697 order-infeasible, 498 force an extra AP,
     518 force a repeated difference), giving 287 minimal forbidden cores with $\le 6$ edges
     (data/forbidden_ordered_n7.json, data/forbidden_ordered_n8.json). An independent referee re-derived
     every verdict with its own oracle (experiments/referee/catalogue-n8).
2. **The abstract constant.** Over the class $O'$ of ordered midpoint hypergraphs (linear, $F_7$-free,
   K30, K31, core-free), the minimum independence number equals $f(n)$ for every $n=5,\dots,15$
   (experiments/20261013-2257-chyp-table, experiments/20261014-0500-slack-landscape). In particular
   $f(n)=\lceil n/2\rceil+1$ for $6\le n\le 15$ and $n=17$, which coincides with the Henning–Yeo bound
   for every $6\le n\le 23$; the trivial Gyárfás–Lehel bound $h\ge\lceil (n+1)/2\rceil$ is already tight
   at every even $n\le 14$. **No lower-bound improvement is possible below $n=16$**, abstractly or
   arithmetically.
3. **Q8 (the community's candidate inequality $7\tau(K)\le 3|R|+2e_2+4e_1$)** holds on every
   deletion/avoidance state of all seven record sets (A_base: 3,253,568 states, 94,544 equalities),
   on about 560M sampled states of random saturated sets and on 752 gluings; two independent
   implementations agree on every count (K34). With no avoided points Q8 is exactly $h\ge 4n/7$, so it is
   an inductive strengthening of the conjecture $c_*=4/7$. Evidence only. **For the abstract class Q8 is false** (K38):
   a 12-vertex ordered midpoint hypergraph that is linear, $F_7$-free, monotone, medial-free and clean of all
   $\le4$-edge cores violates it by one; every abstract violator found contains a $\ge5$-edge forbidden core and is
   non-realizable. So a proof of Q8 must use the deeper forbidden configurations: the arithmetic is essential.
4. **Search engines** (e757/): exact realizability oracle with Farkas certificates
   (`realizability.py`), CP-SAT model of $O'$ with lazy/eager independence constraints
   (`cpsat_model.py`), an independent python-sat encoding (`sat_indep.py`), an exact DFS in Python and C
   (`ordered_dfs.py`, `c/`), and a midpoint-map annealer (`anneal.py`). All cross-validated on $n\le 12$.
5. **Negative heuristic results.** Annealing over about 4 million saturated midpoint maps at $n=16$
   (28,589 of them genuine (4,5)-sets) never produced a largest Sidon subset below 10; about 21% of random
   linear saturated maps are realizable, so realizability is not the obstacle at $n=16$, the independence
   number is.

## 2. The open case $n=16$ and how it decides the direction

Beating $4/7$ first becomes possible at $n=16$ ($h=9$, $m\in\{13,14\}$). Two hypotheses are consistent with
all data: (H1) Henning–Yeo stays tight at even $n$ up to 22 (records at $n=16,18,20,22$, hence
$c_*\le 6/11$); (H2) a wall appears at $n=16$ ($f(16)=10$, consistent with $c_*=4/7$ and Q8).
Direct CP-SAT and pure-SAT attacks on $n=16$ time out (each of 30 sub-cases exceeds 3000 s). The running
approach is layered: by the deletion-of-maximum lemma, a 16-vertex extremal hypergraph minus its maximum is a
15-vertex member of $O'$ with $\alpha\le 9$ and $m'\in\{9,\dots,13\}$ whose non-midpoints are exactly the
midpoints of the deleted vertex's edges; enumerate those and extend (experiments/20261014-0550-n16-layered).

## 3. Leads and recommended next steps

- Finish the layered $n=16$ enumeration; realize every abstract solution exactly (judge/judge.py). A
  realizable one is a new record ($9/16$); none means $f(16)=10$ (certify with the two independent
  encodings; the DFS cannot reach $n=16$).
- If $f(16)=10$: the wall is arithmetic or abstract; the forbidden-core library (K30–K33) is the tool for an
  inductive inequality of Q8 type (kb/methods/trackL_inductive_framework.md gives the exact free-move
  conditions for any constants $(a,b,c,d)$).
- If $f(16)=9$: run the same layered search at $n=18,20,22$.
- Obtain the Henning–Yeo 2021 paper (closed access) for the structure of its equality cases.

## 4. Dead ends added this run
See kb/dead_ends.md: direct CP-SAT/SAT at $n=16$ without structure; annealing at $n=16$; the unconstrained
abstract class is too loose without K30/K31/cores.
