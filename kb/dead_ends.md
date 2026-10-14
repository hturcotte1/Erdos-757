# Dead ends: do not retry without a genuinely new ingredient

Before starting a direction, grep this file. When you abandon an approach, add an entry: what was tried, the evidence it fails, and a pointer to the data or commit.

| ID | Approach | Why it is dead | Evidence |
|---|---|---|---|
| D1 | Abstract transversal bounds using only "linear + $F_7$-free + $m\le n-2$" | Henning–Yeo already gives 9/17 this way. Any improvement must use either hereditary sparsity or realizability (arithmetic). | Ma–Tang §5; Part 2 §2 |
| D2 | Chvátal–McDiarmid / Tuza ($4\tau\le n+m$) | Gives exactly 1/2. Its extremal linear cases ($F_7$, $F_8$) are not realizable. | K9, K20 |
| D3 | Induction with a constant cost per avoided point | One-vertex amalgams $A_k$ have deficit growing like $k$ with $\|D\|=1$ | omega #9804 |
| D4 | The inequality $21\tau(K)\le9\|R\|+5e_2+12e_1$ | Explicit 12-point counterexamples | omega #9804, K14 |
| D5 | **Periodic chain constructions**, i.e. Fibonacci, tribonacci, Pisot recurrences $x_{j+b}=2x_j-x_{j-a}$, and multi-class periodic versions | Independence density ≥ 3/5 for every linear single-class chain with $a+b\le11$, every 2-class chain with span ≤8, and every 3-class chain with span ≤6 | [verified-here] `e757/chains.py`, `test_chain_densities` |
| D6 | Adding two points to $A_{\rm base}$ | Every such (4,5) extension has $h=10$, ratio 5/8 [verified-here, certificate L001 ACCEPTED]; adding four or more points is not excluded | results/proofs/L001-abase-two-point-extensions.md, K13 |
| D7 | One-vertex amalgams and disjoint unions of records | They can never lower the ratio, because $h$ is subadditive | Ma–Tang Lemma 3.6 |
| D8 | Searching for a better set with $n\le15$ or $n\in\{17,19,21,24,26,28\}$ | Impossible by Henning–Yeo | K23 |
| D9 | Random sampling plus deletion (Alon–Erdős style) | Gives about 1/2 here | Part 1 §6 |
| D10 | Gluing with integer or "nice" scale factors | Creates parallelograms (a shared difference), which violates (4,5); the scale must avoid all ratios $(a-a')/(b-b')$ | [verified-here] judge rejects e.g. scale 7 on $A_{\rm base}$ |
| D11 | Structures built from AG(2,3), $F_7$, $F_8$ | These are characteristic-3 AP hypergraphs and not realizable over ℝ | K7, K20 |
| D12 | The 2·3-smooth weak-Sidon construction of Ma–Tang | Its APs overlap in two points, so it is not linear and not (4,5) | Ma–Tang §4.1 |
| D13 | Whole midpoint-depth layers; the shortest multiplicative recurrence | Recover only known bounds | omega #9804 |
| D14 | Uniformly random midpoint maps | Almost never linear (2 in 3000 at $n=16$); generate maps with constraint propagation instead | [verified-here] |
| D15 | Direct SAT/CP-SAT decision of alpha<=9 at n=16 (even with K30/K31/cores and a 30-way case split) | every sub-case exceeds 3000 s in CP-SAT and 600-700 s in glucose/cadical; pure-SAT UNSAT time grows from 2.4 s (n=12) to 256 s (n=13) | experiments/20261014-0450-n16-cases, experiments/20261014-0515-sat-indep |
| D16 | Simulated annealing over saturated midpoint maps at n=16 (and 18) | ~4M states, 28,589 genuine (4,5)-sets, best h=10; alpha<=9 never reached even combinatorially | experiments/20261013-2257-anneal16/best.json |
