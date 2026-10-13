# Ideas backlog (speculative; nothing here is established)

Pick from here when a track stalls. Move an idea to `kb/dead_ends.md` or `results/LEDGER.md` once tested.

1. **Harmonic-measure view of saturated sets.** Values are hitting probabilities of a random walk on the midpoint map. Potential theory, electrical networks and Markov-chain tools might constrain how many APs can coexist without forcing a parallelogram.
2. **Lattice constructions.** Translation-invariant AP structures in $\mathbb Z^2$ or $\mathbb Z^3$ with long-range edges, projected generically (Freiman invariance makes this legal). One-dimensional chains are dead (D5), so try 2D tilings whose AP hypergraph has independence density below 4/7.
3. **Expander-like hypergraphs.** Low $\alpha$ needs expansion. Look for realizable "almost-designs": partial Steiner triple systems with $m\approx n$ whose AP realizations avoid parallelograms.
4. **CEGAR loop.** SAT proposes a hypergraph; linear algebra refutes it with a forced relation; the refutation becomes a learned clause. The learned clauses are themselves data for the forbidden-configuration library (L2).
5. **LP-tested discharging.** Generate candidate local weights automatically: an LP over all small realizable configurations finds the best weights, then you try to prove the inequality.
6. **Flag algebras / SDP** on local configurations of realizable hypergraphs. The answer is a hereditary-family ratio, which fits the method.
7. **Stability of Henning–Yeo.** Show that near-equality forces many copies of a specific small configuration, then show those cannot all be realized.
8. **Variants over other groups:** $\mathbb Z_p$, $\mathbb F_p^k$, and $\mathbb F_3^k$ (where midpoints are not unique). These show which hypotheses matter.
9. **Fractional relaxations.** The fractional transversal number of realizable hypergraphs, and LP duality certificates as proof sketches.
10. **Program evolution.** LLM-written generator programs scored by exact $h/n$ (FunSearch/AlphaEvolve style), restricted to the feasible sizes in START_HERE §4.
11. **Degree-3 structure.** Every set beating 5/9 needs points on 3 or more APs (K10). Study what the neighbourhood of a degree-3 or degree-4 vertex can look like in a realizable set.
12. **Forbidden-pattern counting from the planar problem (#135).** Dumitrescu's 8 forbidden 4-point patterns and Tao's methods; check whether any transfer to the line.
