# Proving lower bounds (Track L): recipes

## Shape of every known lower bound
$h=n-\tau$. A transversal inequality $\tau\le an+bm+\dots$, combined with
$m\le n-2$, gives $h\ge(1-a-b)n-O(1)$. To beat 9/17 you need, for realizable AP hypergraphs,
something like $17\tau\le(8-\varepsilon)n+O(1)$. Equivalently, using the excess $D=17h-9n$, prove
$D\ge\varepsilon n-C$ (START_HERE §3). The best-supported concrete candidate so far is I11, $11\tau\le3n+2m$ (kb/notes/i11_conjecture.md). With $m\le n-2$ it gives $17\tau\le\frac{85}{11}n-\frac{68}{11}$, i.e. $\varepsilon=3/11$ (equivalently $D\ge(3n+68)/11$). I11 is [conjecture] in general. Its falsifier run (experiments/falsify/i11-inequality/README.md, HOLDS-ON-DATA) and the computer-assisted window-cell induction of certificates L007-L011 and L013 (I11 verified on the abstract class for $n\le26$ [verified-here]; no general proof) illustrate workflow steps 2 and 4 below. The stronger $\tau\le3n/7$ (the 4/7 conjecture) was consistent with the data of that README §0 but is [refuted] (verified here 2026-10-20): the 65-point member C003 of an anonymous reader's family (Erdős Problem a Day, 19 Oct 2026; community construction, verified here and not discovered here; K59) has $\tau=28$ and $3n/7=195/7\approx27.86$ ($7\tau=196>195$). I11 holds on C003 with slack 13 ($3n+2m-11\tau=195+126-308$) and on the whole community family $S_K$ with slack $7+K$ (L015, K60).

## Workflow for any candidate inequality
1. **State it exactly**: class, constants, which subsets it is claimed for (all induced
   subhypergraphs? traces after deleting an independent set?).
2. **Falsify first** (`falsifier` subagent) on:
   - $A_{\rm base}$ and all its $2^{14}$ induced subsets;
   - the 12-point sets and data/small_records.json;
   - gluings and amalgams (the omega amalgams kill constant-cost inductions);
   - random realizable sets from the search tools.
3. **Fit constants by LP.** Over the configurations in the dataset, solve for the best $(a,b,c)$
   in $\tau\le an+bm+c\cdot(\text{feature})$. The tight configurations are the "special pieces"
   the proof must handle. Sketch:
   ```python
   from scipy.optimize import linprog
   # rows: one per configuration H with features (n, m, f3 = #vertices of AP-degree >= 3, ...)
   # constraint: a*n + b*m + c*f3 >= tau(H)  ->  -[n, m, f3] . [a, b, c] <= -tau(H)
   # objective: minimize the bound on the target family, e.g. a + b (since m ~ n)
   res = linprog(c=[1, 1, 0], A_ub=[[-n, -m, -f3] for (n, m, f3, tau) in data],
                 b_ub=[-tau for (n, m, f3, tau) in data], bounds=[(0, None)] * 3)
   ```
4. **Proof architecture:** minimal counterexample, then reducible configurations, then
   discharging or a deficiency argument (Henning–Yeo; kb/notes/henning_yeo_transversals.md §2).
   Typical steps:
   - no cut vertex (omega reduction);
   - minimum degree;
   - degree-2 chains (the max-degree-2 theory gives 5/9);
   - special pieces and Hall's theorem to extend transversals across their boundary edges.
5. Write it with the `prover` subagent, then the verify-claim skill.

## Where arithmetic can enter (the unused hypotheses)
- **Hereditary sparsity** $e(S)\le|S|-2$ for every $S$: Henning–Yeo uses only the global count.
- **Realizability:** a forbidden-configuration list beyond $F_7$. The library for $n\le8$ exists:
  287 minimal forbidden cores with up to 6 edges (44 for $n\le7$, 243 new at $n=8$), in
  `data/forbidden_ordered_n7.json` and `data/forbidden_ordered_n8.json`, generated with
  `e757/realizability.py` (exact, with Farkas certificates); K32, K33, Q7 [verified-here]. The Q8
  inductive inequality ($7\tau(K)\le3|R|+2e_2+4e_1$) is false for the abstract class that excludes
  only $\le4$-edge cores, so any Q8-type route needs cores with $\ge5$ edges (K38, K39, D17)
  [verified-here]. Cores for 9 and 10 vertices are not computed.
- **Order:** a midpoint lies strictly between its endpoints. So the leftmost and rightmost points
  are never midpoints, and in any induced subset its own extremes are not midpoints of APs inside
  the subset.
- **Rigidity:** in saturated sets the pattern determines the set. Many patterns are forced to be
  non-realizable (coincidences).

## Sanity values to check any inequality against [verified-here for the single sets, recomputed from data/small_records.json with e757.core; the all-classes rows are derived-here exact arithmetic on K41, K45]
| Set | n | m | τ | h | HY slack | D |
|---|---|---|---|---|---|---|
| $A_{\rm base}$ | 14 | 12 | 6 | 8 | 4 | 10 |
| 12-pt sets (all 54,243 classes, K41; the three known sets included) | 12 | 10 | 5 | 7 | 5 | 11 |
| 14-pt saturated extremal sets (all 2,910 classes, K45; $A_{\rm base}$ among them) | 14 | 12 | 6 | 8 | 4 | 10 |
| n=10 record | 10 | 8 | 4 | 6 | 6 | 12 |
| n=8 record | 8 | 5 | 3 | 5 | 4 | 13 |
| community family $S_K$: an anonymous reader's construction (Erdős Problem a Day, 19 Oct 2026) [community], verified here, not discovered here; formulas for all $K$ from L015 (K60), counts checked for $K\le8$ against data/reader_5_9_family.json; $K=6$ is the 65-point C003 (K59); $\tau>3n/7$ iff $K>5$ | $11+9K$ | $9+9K$ | $4+4K$ | $7+5K$ | $14+4K$ | $20+4K$ |
