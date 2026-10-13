# Proving lower bounds (Track L): recipes

## Shape of every known lower bound
$h=n-\tau$. A transversal inequality $\tau\le an+bm+\dots$, combined with
$m\le n-2$, gives $h\ge(1-a-b)n-O(1)$. To beat 9/17 you need, for realizable AP hypergraphs,
something like $17\tau\le(8-\varepsilon)n+O(1)$. Equivalently, using the excess $D=17h-9n$, prove
$D\ge\varepsilon n-C$ (START_HERE §3).

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
- **Realizability:** a forbidden-configuration list beyond $F_7$ (generate it with
  `e757.core.realize` and the CEGAR no-goods).
- **Order:** a midpoint lies strictly between its endpoints. So the leftmost and rightmost points
  are never midpoints, and in any induced subset its own extremes are not midpoints of APs inside
  the subset.
- **Rigidity:** in saturated sets the pattern determines the set. Many patterns are forced to be
  non-realizable (coincidences).

## Sanity values to check any inequality against
| Set | n | m | τ | h | HY slack | D |
|---|---|---|---|---|---|---|
| $A_{\rm base}$ | 14 | 12 | 6 | 8 | 4 | 10 |
| 12-pt sets (three) | 12 | 10 | 5 | 7 | 5 | 11 |
| n=10 record | 10 | 8 | 4 | 6 | 6 | 12 |
| n=8 record | 8 | 5 | 3 | 5 | 4 | 13 |
