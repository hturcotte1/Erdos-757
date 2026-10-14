# Known results (facts table)

Each row gives a tag, the statement, the source, and how it is checked (a test name in `tests/test_known_facts.py`, or "read the source"). Update this file only for results that are verified per the `verify-claim` skill.

| ID | Tag | Statement | Source | Check |
|---|---|---|---|---|
| K1 | published | $c_*=\lim f(n)/n=\inf_n f(n)/n$ exists ($f$ subadditive) | Ma–Tang Thm 1.5 | source |
| K2 | published | $9/17\le c_*\le4/7$ | Ma–Tang Thm 1.6 | source |
| K3 | published | Sidon ⊂ (4,5) ⊂ weak Sidon; both strict ($\{1,2,3,5\}$; $\{1,2,3,6\}$) | Ma–Tang Props 2.1, 2.2 | `test_fibonacci_caveat` |
| K4 | published | For weak Sidon $A$: Sidon subsets = 3-AP-free subsets; $h=\alpha(H)$ | Ma–Tang Lemma 2.3 | judge cross-check |
| K5 | published | Injective midpoint map, never at the extremes; $e(S)\le\|S\|-2$ for all $S$ | Ma–Tang Lemma 2.4 | source |
| K6 | published | $H(A)$ is linear for a (4,5)-set | Ma–Tang Lemma 2.5 | source |
| K7 | published | $H(A)$ is $F_7$-free | Gyárfás–Lehel Prop 2.6 | `test_f7_not_realizable` |
| K8 | published | $17\tau\le5n+3m$ for linear $F_7$-free 3-uniform $H$ | Henning–Yeo 2021, Thm 7 | source |
| K9 | published | $4\tau\le n+m$ (all 3-uniform); for linear connected $H$, equality iff $E_3$, $F_7$ or $F_8$ | Tuza; Chvátal–McDiarmid; Henning–Yeo | source |
| K10 | published | Connected, linear, max degree 2: $18\tau\le4n+4m+2$, hence $h\ge(5n+3)/9$ for such AP hypergraphs | Henning–Yeo EJC 24(2) P2.50 (derivation here) | source |
| K11 | published | $A_{\rm base}$ is a (4,5)-set with $h=8$ | Ma–Tang Lemma 5.1 | `test_abase` |
| K12 | community | Two 12-point (4,5)-sets with $h=7$ | omega issue #9804 | `test_twelve_point_sets` |
| K13 | community | Every 2-point extension of $A_{\rm base}$ that is a (4,5)-set has $h=10$ | omega issue #9804 | source (certificate in the issue) |
| K14 | community | $21\tau(K)\le9\|R\|+5e_2+12e_1$ is false | omega issue #9804 | source |
| K15 | community | A minimal counterexample (for any constant $c$) has no cut vertex in its primal graph | omega issue #9804 | source |
| K16 | published | Weak Sidon analogue solved: $g(n)=\lceil(n+1)/2\rceil$ | Ma–Tang Thm 1.3 | source |
| K17 | verified-here | $A_{\rm base}$: 143 maximum Sidon subsets; degrees 4,3×6,2×7; no cut vertex | computed | `test_abase` |
| K18 | verified-here | Record sets are midpoint-saturated ($m=n-2$) and affinely rigid (AP-system rank $n-2$) | computed | `test_rigidity` |
| K19 | verified-here | The two 12-point sets are not affinely equivalent | computed | `test_twelve_point_sets` |
| K20 | verified-here | $F_7$: none of the 243 midpoint labelings is realizable over ℚ (204 force a coincidence, 24 force an extra AP, 15 violate (4,5)) | computed | `test_f7_not_realizable` |
| K21 | verified-here | $\{1,2,3,5\}$ is not (4,5); $\{F_3,\dots,F_{n+2}\}$ is (4,5) with $h=\lceil3n/5\rceil+O(1)$ | computed | `test_fibonacci_caveat` |
| K22 | verified-here | Periodic chain hypergraphs (vertex $j$ is the midpoint of $\{j-a_c,j,j+b_c\}$) have independence density ≥ 3/5 in every case checked (see D5) | computed | `test_chain_densities` |
| K23 | derived-here | Beating 4/7 is impossible for $n\le15$ and $n\in\{17,19,21,24,26,28\}$; the parameters for the feasible $n$ are in `e757/fn_bounds.py` | HY + K5 | `test_hy_feasibility` |
| K24 | derived-here | Exact $f(n)$ for $n\in\{1..7,9,11..15,17,24,26,28\}$ (values in START_HERE §5) | HY + constructions + gluing | `test_fn_bounds` |
| K25 | derived-here | $D(A)=17h-9n=\delta+3(n-m)\ge6$; $c_*=9/17+\inf D/(17n)$ | algebra on K5 + K8 | source |
| K26 | derived-here | Every condition is Freiman-2-invariant, so constructions in $\mathbb Z^d$ are allowed | definitions | source |
| K27 | published | Planar analogue (#135): Tao, arXiv:2409.01343 | Tao | source |
| K29 | verified-here | $f(8)=5$, $f(10)=6$ (sets in data/small_records.json); hence $f(n)$ is known exactly for all $n\le15$ | e757.ordered_search + judge | `test_small_records` |
| K28 | published | $f(n,4,5)=\tfrac56n+o(n)$ (anti-Ramsey context) | Bennett–Cushman–Dudek–Prałat; Joos–Mubayi | source |
| K30 | verified-here | **Monotone midpoints.** For APs $(i,j,k)$, $(i',j',k')$ in rank order with $i\le i'$, $k\le k'$, $(i,k)\ne(i',k')$: $j<j'$. Proof: $x_j=(x_i+x_k)/2<(x_{i'}+x_{k'})/2=x_{j'}$. The two 2-edge order cores of the n<=7 library are exactly this. | derived from the AP equations; `e757.realizability.order_feasible` | experiments/20261013-2257-forbidden-library (cores n=5, n=6 order) |
| K31 | verified-here | **No medial triangle.** No (4,5)-set has three APs $\{a,b,c\},\{a,p,e\},\{c,q,e\}$ with midpoints $b,p,q$ (three APs pairwise meeting in a vertex that is an endpoint of both). Proof: $x_q-x_p=(x_c-x_a)/2=x_b-x_a$, so $x_a+x_q=x_b+x_p$ with $a,b,p,q$ distinct, contradicting weak Sidon. Triangles in which a shared vertex is a midpoint of one of its edges can be realizable. | derived; `e757.realizability.forced_relations` | experiments/20261013-2257-forbidden-library (3-edge diff core) |
| K32 | verified-here | Census of ordered midpoint patterns (linear, injective midpoints) on n<=7 vertices: totals 2, 5, 24, 189, 2364 for n=3..7; realizable 2, 5, 22, 142, 1312; the rest are order-infeasible (2, 45, 1006), force an extra AP (0, 0, 22) or a repeated difference (0, 2, 24). 44 minimal forbidden cores on 20 edge sets, all with <=5 edges. | `e757/realizability.py`, exact; cross-checked against the float-LP + sympy path (0 mismatches) | data/forbidden_ordered_n7.json; experiments/20261013-2257-forbidden-library/README.md |
| K33 | verified-here | Small-configuration catalogue (11 connected linear configurations with <=4 edges on <=8 vertices, 145 midpoint labelings, all vertex orders; `realize_exact` for every case) and n=8 census (46281 patterns = 16568 realizable + 28697 order-infeasible + 498 forced extra AP + 518 forced repeated difference; 243 new minimal cores, 287 in total). **Triangle** (3 edges, 6 vertices): the 7 labelings are 2 shared-midpoint (forbidden), 4 realizable (those with >=1 corner midpoint; 22 of 60 ordered patterns) and exactly one injective forbidden labeling, the medial triangle (all three midpoints edge-private; forbidden in every order, K31). **Pasch** (4 edges, 6 vertices): realizable in exactly one labeling and one order up to reflection, `[(0,1,3),(0,2,5),(1,4,5),(2,3,4)]`, e.g. {0,4,7,8,9,14} (h=4, saturated); the other injective Pasch labeling dies by K30 in its single order. No unlabeled configuration with <=4 edges is forbidden outright. Labelings forbidden in every order (beyond a shared midpoint): any labeling containing a medial triangle (K31), the **medial 4-cycle** (four edges {a,b,c},{a,d,e},{b,f,g},{d,f,h} with edge-private midpoints c,e,g,h: x_c+x_h=x_e+x_g, Varignon) and one Pasch labeling (K30). | `e757/realizability.py`, exact; independent consistency check of the two pattern generators for n=3..8 and of core counts (63 order, 10 diff, 8 extra-AP four-edge cores) | tests/test_forbidden_catalogue.py; data/forbidden_ordered_n8.json; experiments/20261014-0005-forbidden-n8/README.md |
| K34 | verified-here | The omega candidate Q8, $7\tau(K)\le3|R|+2e_2+4e_1$ (kb/notes/omega_issue_9804.md), holds on every deletion/avoidance state of all seven record sets (A_base: 3,253,568 valid states, 94,544 equalities, 0 violations), on ~560M sampled states of 1800 random saturated (4,5)-sets at n=12,14,16, and on 752 gluings; two independent implementations (Python+C falsifier, C verifier) agree on every count. With $D=\emptyset$ Q8 reads $h\ge4n/7$: it is an inductive strengthening of the conjecture $c_*=4/7$. Evidence only, not proof. | experiments/falsify/q8-omega-inequality/report.md; experiments/referee/q8/report.md | `experiments/referee/q8/check.py` |

**Derivation of K10.** For the AP hypergraph of a (4,5)-set with maximum degree ≤2, apply Henning–Yeo's $k=3$ bound to each component, using $m_C\le n_C-2$. This gives $\tau\le(4n-3)/9$.

**Derivation of $f(5)=4$.** A linear 3-uniform hypergraph on 5 vertices has at most 3 edges. Three triples on 5 points that pairwise meet in exactly one point must share a common point. So $\tau\le1$.
