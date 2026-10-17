VERDICT: ACCEPT

# Referee report on L007-no-nonsaturated-extremal-14-point-sets (round 3)

- Claim: results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md, sha256 prefix 9030878fcd3a18a1. This is the version after the round-1 text fixes of 04:37 UTC (git 420506d). It was identical at the start and end of this review.
- Referee: referee subagent (round 3), 2026-10-17, 04:39 to 05:37 UTC.
- Scratch folder: experiments/referee/L007-round3/. All programs there are mine, except the authors' sources, which were copied into `rerun/src/`, recompiled and run inside `rerun/`. No other file was modified. All jobs ran at nice 5 with at most 2 processes.

## Summary

The certificate proves Theorem 1: every 3-graph in O+ with n = 14 and m = 11 has τ ≤ 5. O+ means linear, F7-free, and e(S) ≤ |S|−2 for every |S| ≥ 2.
- From this and the published facts K3–K8 it derives Theorem 2: no 14-point (4,5)-set has h ≤ 8 and exactly 11 three-term APs.
- Hence Corollary 3: every 14-point (4,5)-set with h = 8 is midpoint-saturated.

I re-derived every step by hand. That covers the slack additivity, heredity, the window-cell table and the slack-0 table (all 49 table entries re-computed), the degree bound, the structure of H−v, both routes, and Steps 7–8. I also audited Lemma D against both enumerators' code. Every authors' computation under 20 minutes was re-run from freshly compiled sources, and every count and stored file was reproduced exactly.

The two authors' enumerators are separately written but implement the same canonical-growth process. So I built a third, methodologically different tool chain:
- an individualisation-refinement canonical form;
- a level-wise isomorph-free generator of connected linear 3-graphs;
- my own labelled brute force, a definition-based F7 detector, and my own extension program.

I validated the generator against my brute force on all 41 cells and 447 pruned runs with n ≤ 9 (0 mismatches). It confirms independently every load-bearing enumeration:
- the six window cells of Lemma A are empty;
- (10,7,≥4) has 6 classes and (13,8,≥5) has 2;
- (14,11,≥6,Δ≤3) is the single class D14, which contains F7;
- my extension of the 8 class representatives gives exactly the 5 isomorphism classes into which the authors' 3,186 hits fall, all containing F7.

It also gives a direct, stronger check: no connected linear F7-free 3-graph has (n,m,τ) = (14,11,≥6), with no degree bound at all. Together with Step 6.1 this proves Theorem 1 without Lemma B.

I found no mathematical or computational error. The remaining remarks are editorial and non-blocking. The census count in Corollary 3 and the whole of Corollary 4 rest on the accepted certificates L004 and L005, with the caveats the proof itself states. I did not re-verify those certificates.

## Files reviewed (sha256 prefixes; unchanged during the review, `sha256_start.txt`)

| file | sha256 prefix |
|---|---|
| results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md | 9030878fcd3a18a1 |
| experiments/falsify/i11-inequality/conn_dfs2.c | d9ca727e09ec2b86 |
| experiments/falsify/i11-inequality/conn_dfs2_all.c | a19ea62df6538922 |
| experiments/falsify/i11-inequality/ext_vertex_all.c | 4c19fbe4e71b29a3 |
| experiments/prover/L007/indep/enum_conn.c | c561cdf173a67b41 |
| experiments/prover/L007/indep/ext_indep.c | a46fe47ee698cec2 |
| experiments/prover/L007/indep/f7check.py | 7d8da1a13c1669fb |
| e757/cpsat_model.py (find_f7) | 325060f22b2f19ce |

Also read:
- bf_cells.c, bf_cell.c, compare_bf.py, reproduce.sh, sat_cell.py (imports only; run as is);
- the L004 and L005 Statements;
- kb/notes/henning_yeo_2021_affine.md (K8 hypotheses);
- kb/known_results.md rows K3–K8 and K24;
- the round-1 review, only after my own checks were done.

## Step-by-step check of the argument

1. **Step 0.1 (components).** n, m and τ are additive over components: a vertex set is a transversal iff it meets every component's edges. So s(H) = Σ s(C_i), and an isolated vertex has s = 3. Correct.
2. **Step 0.2 (heredity).** Linearity, F7-freeness and (P3) pass to induced subgraphs, since e_{H[S]}(S') = e_H(S'). Correct.
3. **Step 0.3 (O ⊆ O+).** An edge i<j<k inside S has its midpoint j in S∖{min S, max S}, and midpoints are distinct. So e(S) ≤ |S|−2. Correct.
4. **Step 0.4.**
   - τ ≤ m.
   - τ(H)−1 ≤ τ(H−v) ≤ τ(H).
   - m ≤ n−2 for n ≥ 2, by (P3) with S = V.
   - K8 applies to O+, whose members are 3-uniform, linear and contain no F7.
   - Hypothesis check: in a linear 3-graph every copy of F7 is induced, since the 6 pairs that F7 leaves uncovered form a 6-cycle with no triangle. So "contains F7" means the same for K7, K8 and (P2).
5. **Step 0.5.** n ≤ 2m+1 for connected 3-graphs, via an edge order in which each new edge meets the earlier union. Correct.
6. **Step 1 (window cells).** I re-computed lo = ⌊(3n+2m)/11⌋+1 and hy = ⌊(5n+3m)/17⌋ over the connected range ⌈(n−1)/2⌉ ≤ m ≤ n−2 (`cells_ref3.py`). Window cells:
   - n ≤ 13: exactly (5,3), (8,4), (10,6), (11,5), (12,9), (13,7), each with τ = lo = 2, 3, 4, 4, 5, 5;
   - n ∈ {14,15}: (14,11), (15,9), (15,10).

   I also parsed all 49 entries of the table in the proof and checked each (lo, hy) and window flag, and that each row covers the full m-range: 0 problems.
7. **Step 2 (Lemma A).**
   - A component C with s(C) < 0 lies in a connected cell: n_C ≥ 3, m_C ≤ n_C−2 by (P3), and n_C ≤ 2m_C+1.
   - Its τ satisfies lo ≤ τ ≤ min(hy, m_C), the upper bound by K8 on C ∈ O+.
   - So (n_C, m_C) is one of the six window cells, and C1 (emptiness for connected linear 3-graphs, a superset of the candidates) closes the proof.
   - The n ≤ 2 case is handled. I also checked the hand proof of (5,3) in 2.4.

   Correct.
8. **Step 3 (Lemma B).** From Lemma A on H−v (13 vertices, 11−d(v) edges, τ ≥ 5):
   - 55 ≤ 61−2d(v), so d(v) ≤ 3;
   - 11τ(H−v) ≤ 61 < 66, so τ(H−v) = 5 and τ(H) = 6;
   - Σd = 33 ≤ 28 + d_3, so d_3 ≥ 5.

   All re-checked.
9. **Step 4 (Lemma C).**
   - s(G) = 39+16−55 = 0, and every component has s ≥ 0 by Lemma A, so every component has s = 0 and there is no isolated vertex.
   - m ≡ 4n (mod 11), since 2^{-1} = 6 and −18 ≡ 4. The slack-0 connected cells with n ≤ 13 are exactly (3,1,1), (10,7,4) and (13,8,5); I recomputed them, including τ ≤ m and K8.
   - 13 = 3a+10b+13c has only the solutions (0,0,1) and (1,1,0).

   Correct.
10. **Step 5 (Route I).**
    - Case (i) needs every connected linear (13,8,≥5) graph to contain F7. I verified this: 2 classes, both contain F7.
    - In case (ii), the three edges at v give pairwise disjoint pairs, none inside an edge of G, by linearity. Those are exactly the configurations enumerated by ext_vertex_all.c, ext_indep.c and my ext_ref.c (code read).
    - H is isomorphic to such an extension with τ = 6, and every extension with τ ≥ 6 contains F7 (verified).

    Correct.
11. **Step 6 (Route II).** Connectivity holds: otherwise each component has ≤ 13 vertices, so s(H) ≥ 0, but s(H) ≤ −2. Δ ≤ 3 comes from Step 3. Then the (14,11,≥6,Δ≤3) enumeration gives only D14, which contains F7 (verified). The 6.4 description of D14 is also right: two disjoint F7's plus the edge {2,3,4}, τ = 6, |Aut| = 4, degrees 3^5 2^9, linear, 0 violations of (P3) over all 2^14 subsets (`check_d14.py`).
12. **Step 7.** W is distinct and (4,5) (all 1,001 four-subsets checked). It has exactly the 11 listed APs and h = 9 by brute force over all 2^14 subsets with the Sidon definition, so τ = 5. W−323 = (A_base∖{136}) ∪ {−323}. {F_3,…,F_16} is (4,5) with m = 11 and h = 9. My own plain-Python check (`check_sets.py`) imports neither e757 nor the judge.
13. **Step 8.**
    - 8.1 uses K5 (each point is the midpoint of at most one AP), K6 and K7 to place H(A) in O, and K3/K4 to get h = α = n−τ.
    - 8.2 follows.
    - 8.3: K8 gives 102 ≤ 70+3m, so m ≥ 11, and K5 gives m ≤ 12. Theorem 2 excludes m = 11.
    - 8.4: only the lower bounds f(15) ≥ 9 and f(14) ≥ 8 of the [derived-here] K24 are used. I re-derived both from K8: 17τ ≤ 114 gives τ ≤ 6 at n = 15, and 17τ ≤ 106 gives τ ≤ 6 at n = 14. L005's Statement covers exactly "every 14-point (4,5)-set with h = 8 and m = 12", and the "equivalently" clause of Corollary 4 is correct given h(C) = 9.

    Correct.
14. **C0 (Lemma D) against the code.**
    - (D1)–(D5) are correct.
    - conn_dfs2.c: the "close" option iff cur+1 < v, the non-decreasing key order (a) < (b) < (c), and the exact cover prune τ(P) ≤ T0−r−1 ⇒ prune. Every test is passed by the canonical branch.
    - enum_conn.c: the phases A/B/C, with B restricted to a < vstart.
    - Both output only connected linear graphs with the required parameters.

    Correct.
15. **C3 (Lemma F, find_f7).**
    - Lemma F's proof is correct for linear 3-graphs.
    - find_f7 is complete: the degree-3 vertex of F7, three edges at it, and four transversal choices.
    - Both were checked against my detector (below).

## Checks performed: referee's independent implementations (experiments/referee/L007-round3/)

All commands are in `reproduce_ref.sh`. Wall times are under a load average of 9 to 12.

- **Canonical form `refcanon.h`.** Individualisation-refinement without pruning. The certificate is the lexicographically least relabelled edge list, so equal certificates imply isomorphic graphs and deduplication can never merge two classes. |Aut| is the number of leaves attaining the minimum, since Aut acts freely on the leaves.
- **Generator `levelgen.c`.** Level-wise isomorph-free generation. Every connected H has an edge order in which each edge meets the earlier union. Every prefix P_k satisfies |V| ≤ N, |V|+2(M−k) ≥ N, τ(P_k) ≥ T0−(M−k), Δ ≤ D and (optionally) F7-freeness. One representative per class is kept at each level, and each is extended by all edges with 0, 1 or 2 new vertices that keep the graph linear.
- **Brute force `bfref.c`.** All labelled linear 3-graphs on [n] (n ≤ 9; n = 9 in 14 s), tallied by (m, τ, Δ) for the connected spanning ones. τ is computed by exhaustive k-subsets.
  - The tallies are identical to the prover's bf_n3..bf_n9.txt.
  - Sanity: 30 labelled Fano planes, 420 labelled F7 (|Aut| = 12), 105 labelled 3-stars on 7 points.
- **`compare_ref.py 9`.** levelgen against bfref on every cell with n ≤ 9.
  - Unpruned: Σ n!/|Aut| per (τ, Δ) equals the brute force on all 41 cells.
  - Pruned: all 447 runs with t ∈ 0..τmax+1 and D ∈ {2,3,100} match.
  - Output: `n<=9: cells=41 pruned_runs=447 mismatches=0`.
- **Window cells (C1).** `./levelgen N M lo 100 0 1` gives `classes=0` for (5,3,2), (8,4,3), (10,6,4), (11,5,4), (13,7,5) and (12,9,5). Level sizes for (12,9,5): 1, 1, 3, 10, 37, 190, 969, 2434, then 0.
- **Lemma A without K8.** In every one of the 35 connected cells with n ≤ 13, m ≤ n−2 and lo ≤ m, with F7 pruned at every level: `classes=0` (`out/lemmaA_noHY.txt`).
- **Tight cells (C2).**
  - (10,7,≥4): 6 classes, |Aut| = 4, 4, 2, 2, 6, 6; labelled count 6,652,800 = bf_cell 10 7 4.
  - (13,8,≥5): 2 classes, |Aut| = 96 and 16. Both are F7 plus a 3-edge tree, and they canonicalise to the two graphs written out in C2.
  - All 8 classes have τ exactly 5 (resp. 4) and 0 violations of (P3).
  - The authors' files fall into exactly these classes: 159 = 106 + 53 in all three (13,8,5) files, and 637 = 165+115+126+143+48+40 in both (10,7,4) files.
  - Exactly one (10,7,4) class contains F7: the one with 126 labelled outputs, as stated.
- **Route II (C5).**
  - `./levelgen 14 11 6 3 0 1` gives one class (|Aut| = 4, τ = 6, Δ = 3), labelled count 14!/4 = 21,794,572,800 (32 s).
  - All 998 outputs in each of the falsifier's file, the prover's rerun and the prover's independent file canonicalise to this class. So do the D14 written out in Step 6.4 and f7_containing_violation.json.
- **Theorem 1 directly.**
  - `./levelgen 14 11 6 100 1 1`, connected, linear, F7-free, no degree bound, gives `classes=0` (58 s; level 10 had 84,911 classes).
  - Without F7 pruning, `./levelgen 14 11 6 100 0 1` gives 3 classes (Δ = 3, 4, 4), all containing F7.
- **F7 detector `reff7.py`.** Backtracking for an injective φ: V(F7) → V(H) with φ(e) ∈ E(H), straight from the definition.
  - Positive controls: F7, F7 relabelled, AG(2,3), AG(2,3) minus a point, F7 plus a pendant edge.
  - Negative controls: Fano plane, Fano minus two lines (two choices), L(13), F7 minus an edge, two near-F7 graphs.
  - Result: `ALL CONTROLS OK`.
  - `f7_agree.py`: on 6,000 random linear 3-graphs (2,205 with F7), mine, the prover's has_f7 (Lemma F) and the falsifier's find_f7 give 0 disagreements. All three detectors also pass the 8 controls in `f7_classes.py`.
- **Extension step (C4), different code and different τ test.**
  - `ext_ref.c` decides τ ≥ 6 by testing all 2,002 five-subsets of {0..13}, and re-checks τ(G) = 5 the same way.
  - It runs on the 8 class representatives: 54 admissible pairs each, 67,474 extensions, 29 hits with τ ≥ 6, all containing F7 (0.15 s).
  - These form 5 isomorphism classes, identical as sets of canonical forms to the classes of the 3,186 hits in each of ext_indep_hits.txt, prover rerun/ext_vertex_hits.txt and falsifier ext_vertex_hits.txt.
  - Hit statistics:
    - all 3,186 contain F7 under my detector, and all are linear;
    - 1,180 have Δ = 3, all isomorphic to D14, and 2,006 have Δ = 4;
    - H−13 is connected (13,8) for 954 hits and (10,7)+edge for 2,232;
    - of the 2,232, 1,386 have an F7-containing (10,7,4) part and 846 an F7-free part, and in those 846 every F7 uses vertex 13.

    All of this matches C4.
  - Note: my first classifier keyed on the presence of the edge (10,11,12) and gave 930/2,256. That was my error: 24 of the (13,8,5) inputs contain that edge. Classifying by the component structure of H−13 gives the proof's numbers.
- **Cross-validation of the authors' enumerators beyond n = 9 (`xval.py`).** For 12 further cells, the class sets of conn_dfs2_all and of enum_conn (canonicalised with my code) equal my generator's: 0 mismatches. The cells:
  - (10,7,≥3), (10,6,≥3), (10,8,≥4);
  - (11,7,≥4), (11,8,≥4), (11,9,≥4): 3,771 classes, 3,112,589 outputs;
  - (12,8,≥4); (12,9,≥4,Δ≤3): 7,400 classes, 5,401,796 outputs; (12,10,≥5,Δ≤3);
  - (13,9,≥5); (13,10,≥6): empty in all three; (13,8,≥4,Δ≤3): 1,997 classes, 1,147,893 outputs.
- **Remark cells (Step 9.1, not load-bearing).** levelgen finds (15,9,6), (16,8,6) and (15,10,6) empty, in agreement with the authors. Also empty without F7: (13,10,6), (13,11,6), (14,12,7).

## Checks performed: re-runs of the authors' computations (rerun/, sources recompiled)

- **C1.**
  - conn_dfs2 node counts: 16, 151, 8,448, 197, 19,596, 18,326,058, all `found=0`.
  - enum_conn call counts: 52, 265, 15,580, 249, 23,256, 34,515,249, all `found=0`.
  - Both are identical to the proof.
- **SAT cross-check.** `sat_cell.py 8 4 3 / 10 6 4 / 11 5 4` returns UNSAT in 0.2 s, 41.2 s and 172.9 s.
- **C2.**
  - `conn_dfs2_all 10 7 4`: nodes = 102,701, found = 637. `conn_dfs2_all 13 8 5`: nodes = 1,295,881, found = 159. Both byte-identical to the falsifier's files.
  - `enum_conn 10 7 4 / 13 8 5`: calls = 220,291 and 1,773,159, found = 637 and 159. Both byte-identical to the prover's files.
- **C4.**
  - ext_vertex_input.txt is, as a multiset of edge sets, exactly the 159 + 637(+{10,11,12}) graphs: 796 lines, all distinct.
  - `ext_vertex_all`: `graphs=796 tested=6699128 hits(tau>=6)=3186`, byte-identical.
  - `ext_indep` on the rebuilt input: `bad_tau=0 tested=6699128 hits=3186`, the same hit set.
- **C5.**
  - `enum_conn 14 11 6 3 1`: `calls=2468940032 found=998` (651 s), byte-identical to the prover's file.
  - `conn_dfs2_all 14 11 6 3` takes 1,747 s, over the 20-minute limit, so I did not re-run it. The stored falsifier log shows nodes = 1,165,338,864, found = 998, and the prover's rerun file is byte-identical to the falsifier's. Both canonicalise to D14 (above).
- **C0.**
  - The prover's bf_cells n = 3..9 regenerate byte-identical files.
  - `compare_bf.py mine` and `theirs`: `cells compared: 393 mismatches: 0 nonempty cells: 243 total classes: 1600` (338 s and 324 s).
  - `bf_cell 10 6 4 / 10 7 4 / 11 5 4`: nodes = 14,908,931 / 150,569,981 / 2,300,156, labelled = 0 / 6,652,800 / 0. Identical.
- **C6.**
  - conn_dfs2: 2,459,440, 19,144 and 186,011,577 nodes.
  - enum_conn: 2,534,511, 18,778 and 216,656,914 calls.
  - All `found=0`, identical.
- **C7 and sanity.**
  - check_witness_records.py reproduces the W, A_base, omega 12-point and Fibonacci rows.
  - witness_14_11.py: 291 sets with m = 11, all h = 9; the JSON is identical.
  - sanity_m11_sets.py 200: 55,465 sets, all h = 9; identical.
- **Arithmetic.** The sanity-row slacks are 0, 1, 9, 9, 0 and 1, all re-computed.

## Problems found (in order of severity)

No mathematical or computational problem was found. Every load-bearing statement was verified, most of them by two methods. The items below are editorial. None makes a statement false or leaves a step unproved.

1. **Scope of the Corollaries (already disclosed).** The "exactly 2,910 classes" part of Corollary 3 and the whole of Corollary 4 hold only as far as L004 and L005 do. L004's completeness was re-checked by its referee on 28% of the prefixes. The proof states this caveat, and I did not re-verify L004 or L005. Theorem 1, Theorem 2, Lemma A and the first sentence of Corollary 3 (h = 8 ⇒ m = 12) do not depend on them.
2. **Wording of the header.** "every enumeration ... was run by two independently written programs" is literally true, but conn_dfs2(_all) and enum_conn implement the same canonical-growth process of Lemma D. They are independent implementations, not independent methods. Methodologically independent confirmations now exist: round 1's lexicographic-minimum enumerator and this round's isomorph-free level-wise generator. The header could say so.
3. **DEPENDS ON line.** "Used only in Step 8.1" follows K7 and reads as covering K3–K7. K5 now carries its own note, and K3/K4 feed 8.2–8.3 through 8.1. This is cosmetic.
4. **Sanity checks.** The Q11 DFS snapshot ("1,061 of 3,437 prefixes at 03:14 UTC") is time-stamped and not load-bearing. Theorem 1 makes that DFS redundant, which could be said.

## Additional observations (optional strengthenings for the authors)

- Lemma A does not need K8. All 35 connected cells with n ≤ 13 and m ≤ n−2 that could hold a slack-negative graph are empty for connected linear F7-free 3-graphs, without the τ ≤ hy cut. Round 1 reported the same thing from a different enumerator.
- Theorem 1 does not need Lemma B. No connected linear F7-free 3-graph has (14,11,τ≥6) with no degree bound, and Step 6.1 gives connectivity. This is a third route; it uses only Lemma A.
- Without F7-freeness, the connected linear (14,11,≥6) graphs form exactly 3 classes: D14 and two with Δ = 4. All contain F7. These, plus two disconnected classes, are the 5 classes of the 3,186 Route I hits.
