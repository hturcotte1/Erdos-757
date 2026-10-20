VERDICT: ACCEPT

# Referee report on L007-no-nonsaturated-extremal-14-point-sets (round 1)

- Claim: results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md (sha256 prefix 0b18ddc5a8b7e58f, identical at the start and end of the review).
- Referee: referee subagent, 2026-10-17, 03:49 to 04:35 UTC.
- Scratch folder: experiments/referee/L007-round1/. All code there is mine except the authors' sources, which were recompiled into `rerun/` and `rerun_c0/`. No file outside that folder and this review was modified.

## Summary

The certificate proves Theorem 1: every 3-graph on 14 vertices with 11 edges in the class O+ has τ ≤ 5. O+ means linear, F7-free, and e(S) ≤ |S|−2 for every |S| ≥ 2. It follows (Theorem 2, Corollary 3) that every 14-point (4,5)-set with h = 8 is midpoint-saturated. So the 2,910 classes of L004 are all the extremal 14-point sets, with L004's sampling caveat.

I re-derived every step of the case analysis:
- the slack additivity over components and the hereditary properties;
- the window-cell table and the slack-0 cells, with their modular arithmetic;
- the degree bound and the two-case structure of H−v;
- the extension step and Lemma D, the authors' canonical BFS process.

I read all the load-bearing programs: `conn_dfs2.c`, `conn_dfs2_all.c`, `enum_conn.c`, `ext_vertex_all.c`, `ext_indep.c`, `bf_cell.c` and both F7 tests. I re-ran every authors' computation that takes under 20 minutes from freshly compiled sources. Every node count, call count and output was reproduced exactly, and every stored file was byte-identical.

The authors' two enumerators are separate code but follow the same canonical process. So I wrote a third enumerator with a different canonical scheme: necessary conditions of the lexicographically minimal labelling. I validated it against my own labelled brute force on all 384 (n,m,τ≥t,Δ≤D) runs with 3 ≤ n ≤ 9, with 0 mismatches. It then confirms independently every load-bearing enumeration:
- the six window cells of Lemma A are empty;
- (10,7,≥4) and (13,8,≥5) have exactly the authors' 6 and 2 isomorphism classes;
- Route I: 3,116,602 extensions of my own tight-cell graphs, 1,562 of them with τ ≥ 6, all containing F7;
- Route II: (14,11,≥6,Δ≤3) is the single class D14, which contains F7.

I implemented F7 detection from the definition and tested it, and checked Lemma F exhaustively. As a by-product, Lemma A, and with it Theorems 1 and 2, does not need Henning–Yeo at all: two different enumerators show that in every connected cell with n ≤ 13 and m ≤ n−2, the only connected linear 3-graph with 11τ > 3n+2m is F7.

I found no mathematical or computational error. Only two non-blocking editorial remarks remain: a DEPENDS ON line and a caveat to propagate. Neither changes the truth of any statement.

## Files reviewed (sha256 prefixes)

| file | sha256 prefix |
|---|---|
| results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md | 0b18ddc5a8b7e58f |
| experiments/falsify/i11-inequality/conn_dfs2.c | d9ca727e09ec2b86 |
| experiments/falsify/i11-inequality/conn_dfs2_all.c | a19ea62df6538922 |
| experiments/falsify/i11-inequality/ext_vertex_all.c | 4c19fbe4e71b29a3 |
| experiments/prover/L007/indep/enum_conn.c | c561cdf173a67b41 |
| experiments/prover/L007/indep/ext_indep.c | a46fe47ee698cec2 |
| experiments/prover/L007/indep/f7check.py | 7d8da1a13c1669fb |
| experiments/prover/L007/indep/bf_cell.c | b80a35047bc63267 |
| experiments/prover/L007/indep/bf_cells.c | 7bd79720368065ab |

Also read: `compare_bf.py`, `build_input.py`, `reproduce.sh`, `cells_table.txt` and `cells_output.txt`; `e757/cpsat_model.py:find_f7`; `sat_cell.py` (its F7 loop); kb/notes/henning_yeo_2021_affine.md; and the L004/L005 entries in results/LEDGER.md and the L005 Statement and DEPENDS ON.

## Step-by-step check of the argument

- **0.1 Components.** n, m and τ are additive over components, because a transversal restricts to transversals of the components. So s(H) = Σ s(C_i), and an isolated vertex has s = 3. Correct.
- **0.2 Heredity.** Induced subgraphs of linear (resp. F7-free) 3-graphs are linear (resp. F7-free), and (P3) restricts to subsets. Correct.
- **0.3 O ⊆ O+.** The midpoint of an edge inside S lies in S∖{min S, max S}, and midpoints are distinct. So e(S) ≤ |S|−2. Correct.
- **0.4 Bounds.** τ−1 ≤ τ(H−v) ≤ τ, τ ≤ m, m ≤ n−2, and K8 for linear F7-free H. Correct.
- **0.5 Connected cells.** n ≤ 2m+1 follows from a connected edge ordering. Correct.
- **Step 1.** I recomputed the table (`cells_ref.py`). It is identical, row for row, to the proof's table and to `cells_table.txt`.
  - The window cells with n ≤ 13 are exactly (5,3), (8,4), (10,6), (11,5), (12,9), (13,7), with lo = hy = 2, 3, 4, 4, 5, 5.
  - In each of them, lo ≤ τ ≤ min(hy,m) forces τ = lo.
  - For n = 14 and 15 the window cells are (14,11), (15,9), (15,10).
  - The proof's note that the falsifier README §2 omits (5,3,2) is correct.
- **Step 2 (Lemma A).** A negative-slack H has a negative-slack component C in O+ with n_C ≤ 13. (n_C, m_C) is a connected cell with lo ≤ τ(C) ≤ min(hy, m_C), so it is a window cell, and C1 says that cell is empty even among all connected linear 3-graphs. Correct. The hand proof for (5,3) is correct.
- **Step 3 (Lemma B).** H−v is induced, with 13 vertices and 11−d(v) edges, and τ(H−v) ≥ 5.
  - Lemma A gives 55 ≤ 61−2d(v), so d(v) ≤ 3.
  - 11τ(H−v) ≤ 61 < 66 gives τ(H−v) = 5, hence τ(H) = 6.
  - 33 ≤ 28 + d₃ gives d₃ ≥ 5.

  All verified.
- **Step 4 (Lemma C).** s(G) = 39+16−55 = 0, and every component has s ≥ 0 by Lemma A. So every component has slack 0 and none is an isolated vertex.
  - The slack-0 condition is m ≡ 4n (mod 11): 2⁻¹ = 6 and −18 ≡ 4.
  - I enumerated the slack-0 connected cells directly over all m (no modular shortcut): only (3,1,1), (10,7,4), (13,8,5).
  - The rejected solutions (6,2,2), (9,3,3), (12,4,4) violate n ≤ 2m+1, as stated.
  - The only multisets of sizes in {3,10,13} that sum to 13 are {13} and {3,10}.
  - The totals are consistent: m = 8 = 7+1 and τ = 5 = 4+1.

  So the dichotomy (i)/(ii) is correct.
- **Step 5 (Route I).** Case (i): every connected linear (13,8,τ≥5) graph is isomorphic to an output of C2 (Lemma D), and all of those contain F7. Case (ii): the three edges at v give pairwise disjoint pairs, none inside an edge of G (linearity). So H is isomorphic to an enumerated extension with τ = 6.
  - Both extension programs enumerate exactly "all unordered triples of pairwise disjoint pairs of {0..12}, none inside an edge" (code read).
  - The reduction in `ext_indep.c` is correct: since τ(G) = 5, no transversal of H of size ≤ 5 can contain 13.
  - Every labelled output is processed, so isomorphism testing is not load-bearing.
- **Step 6 (Route II).** H is connected, since otherwise s(H) ≥ 0 > −2, and Δ ≤ 3 by Step 3. Then the (14,11,≥6,≤3) enumeration applies. Correct.
- **Step 7.** I re-verified W and {F₃..F₁₆} from the definitions in my own plain Python (`check_witness.py`). Both are (4,5)-sets with 11 APs and h = 9, W−323 = (A_base∖{136}) ∪ {−323}, and the 11 APs of W are exactly those listed.
- **Step 8.**
  - 8.1 uses K3–K7 correctly.
  - 8.3: at τ = 6, 102 ≤ 70+3m gives m ≥ 11, and K5 gives m ≤ 12.
  - 8.4 uses only f(15) ≥ 9 and f(14) ≥ 8. These follow at once from K8 and K5 (17τ ≤ 75+39 and 17τ ≤ 70+36), so the [derived-here] K24 is re-derived as far as it is used.
  - L005 is stated for every 14-point (4,5)-set with h = 8 and m = 12, as quoted (checked in its Statement), and it lists L004 in its own DEPENDS ON.

  Correct.
- **Lemma D.** I checked (D1) to (D5) line by line:
  - the (a) and (b) orders are strict under linearity;
  - no vertex of an F-edge is labelled during its own turn;
  - (D3) holds by connectivity;
  - ℓ + 2r ≥ n.

  Both programs contain the canonical branch and prune only by valid tests:
  - `conn_dfs2.c`: the key order (a) < (b) < (c), with superset ranges for o; it prunes on `cover_le(all,tau0-r-1)`, `v>n || v+2r<n`, `cur>=v` and the degree caps.
  - `enum_conn.c`: phases A/B/C with `a,b < vstart` and strictly increasing (a,b) or a; it prunes on `viable()`.

  Both hitting-set tests are exact branching on the vertices of one uncovered edge. `conn_dfs2_all.c` differs from `conn_dfs2.c` only in printing (diff checked). `find_f7` is complete: it loops over every centre and every 3 edges at it, with both complementary T1/T2 choices.

## Checks performed (in experiments/referee/L007-round1/, nice 5, at most 2 processes)

### A. Arithmetic

`python3 cells_ref.py` prints:
- the connected-cell table for n = 3..16, identical to Step 1;
- the window cells `[(5,3,2,2), (8,4,3,3), (10,6,4,4), (11,5,4,4), (12,9,5,5), (13,7,5,5), (14,11,6,6), (15,9,6,6), (15,10,6,6), (16,8,6,6), (16,13,7,7), (16,14,7,7)]`;
- the slack-0 connected cells with n ≤ 13, `[(3,1,1), (10,7,4), (13,8,5)]`, each with τ ≤ m and K8 satisfied;
- the multisets summing to 13, `[(3,10), (13,)]`;
- under K8 at n = 14, τ = 6, the minimum is m = 11;
- 55 ≤ 61−2d fails exactly for d ≥ 4.

### B. Re-runs of the authors' computations (recompiled from source)

| computation | command | output, identical to the proof |
|---|---|---|
| C1, falsifier | `rerun/conn_dfs2 N M T` on the 6 window cells | nodes 16, 151, 8448, 197, 19596, 18326058; found = 0 for all |
| C1, prover | `rerun/enum_conn N M T 1000 0` | calls 52, 265, 15580, 249, 23256, 34515249; found = 0 for all |
| C2 | `conn_dfs2_all 10 7 4` and `13 8 5` | nodes=102701 found=637 and nodes=1295881 found=159; `cmp`-identical to the falsifier's files |
| C2 | `enum_conn 10 7 4 1000 1` and `13 8 5 1000 1` | calls=220291 found=637 and calls=1773159 found=159; `cmp`-identical to `mine_*.txt`; equal as labelled sets to the conn_dfs2_all outputs (`check_misc.py`) |
| C4 input | rebuilt in my folder (`check_misc.py`) | 796 lines, equal as a multiset to `ext_vertex_input.txt` |
| C4 | `ext_vertex_all < ext_vertex_input.txt` | graphs=796 tested=6699128 hits(tau>=6)=3186; `cmp`-identical to the stored hits |
| C4 | `ext_indep < ext_input_rebuilt.txt` | graphs=796 bad_tau=0 tested=6699128 hits(tau>=6)=3186; the two hit lists are equal as sets of 3,186 distinct graphs |
| C5 | `enum_conn 14 11 6 3 1` (background, 557 s) | `calls=2468940032 found=998`; byte-identical to `indep/mine_14_11_6_deg3.txt` and equal as a labelled set to the falsifier's `conn2_all_14_11_6_deg3.txt` |
| C6 (remark) | `conn_dfs2 15 9 6` and `16 8 6` | nodes=2459440 found=0; nodes=19144 found=0 |
| C0 brute force | `bf_cell 10 6 4`, `11 5 4`, `10 7 4` | nodes=14908931 labelled=0; nodes=2300156 labelled=0; nodes=150569981 labelled=6652800 |
| C0 tallies | `bf_cells n`, n = 3..9 | byte-identical to the stored `bf_n*.txt`, and identical cell by cell to my own `ref_bf` |
| C0 validation | `compare_bf.py mine` and `compare_bf.py theirs` (copied into `rerun_c0/indep`) | `mine cells compared: 393 mismatches: 0 nonempty cells: 243 total classes: 1600` and `theirs cells compared: 393 mismatches: 0 nonempty cells: 243 total classes: 1600` |

Not re-run, and why:
- `conn_dfs2_all 14 11 6 3` takes 1,747 s, over the 20-minute limit. Its stored output equals my re-run of `enum_conn` as a labelled set, and the prover's re-run file is `cmp`-identical to the falsifier's.
- The SAT cross-check `sat_cell.py`, `witness_14_11.py` and `sanity_m11_sets.py` are not load-bearing. I re-verified W and the Fibonacci set from the definitions instead.

### C. Independent enumerator with a different canonical method (`ref_enum.c`)

Every connected linear 3-graph has a labelling L that minimizes the sorted list of sorted edge triples, compared lexicographically. Such a labelling satisfies four conditions, each proved in the code header:

- **(L1)** The edges come in increasing lex order.
- **(L2)** Vertex 0 has maximum degree D, and its edges are exactly {0,1,2}, …, {0,2D−1,2D}. If some w had larger degree, relabelling w as 0 would place {0,2D+1,2D+2} at position D+1, giving a smaller list.
- **(L3)** The vertices of the first t edges form an initial segment of labels. If label g first appears strictly before label f < g, swap f and g. The first k−1 edges are unchanged and a new edge below e_k appears, so the sorted list becomes smaller.
- **(L4)** If H is connected, every edge after the first contains an earlier vertex. A fully new edge {ℓ,ℓ+1,ℓ+2} would make {0..ℓ−1} a union of components, because all later edges have minimum ≥ ℓ.

The search generates edge lists satisfying (L1) to (L4), with linearity and degree ≤ D, and prunes by ℓ+2r ≥ N and τ(P) ≥ T0−r. τ is computed by its own branching code over vertex-incidence masks. The search is ordered globally by lex order, with no BFS turns, so it differs from Lemma D. An optional prune (L5) proved vacuous, because (L4) keeps the partial graph connected; node counts are identical with and without it.

**Validation.** `ref_bf.c` is my own labelled brute force over all subsets of triples on [n] (linear, connected, spanning), tallied by (m, τ, Δ). It gives 30 labelled Fano planes (= 7!/168) and 420 labelled F7s (= 7!/12). Its tallies are identical to the prover's `bf_cells` for every n ≤ 9, with 19,371,345 labelled graphs at n = 9.

`validate_small.py 9` takes every n = 3..9, every m, every t = 0..τ_max+1 and every D ∈ {1, 2, 3, Δ_max, 1000}. For each it compares the brute-force labelled count with Σ n!/|Aut| over the isomorphism classes output by ref_enum, computed with networkx VF2 on the incidence graph with the two sides kept apart. It also checks every output's parameters, and runs with and without (L5). Output: `{"cells": 384, "mismatches": 0, "nonempty": 195, "bad_params": 0}`.

**Cross-validation of the two methods beyond n = 9** (`cross_methods.py`): the class sets of ref_enum and conn_dfs2_all are equal on the cells (11,7,≥4), with 40 classes from each (3,606 vs 8,786 labelled outputs), and (13,9,≥5), with 156 classes from each (36,515 vs 80,876 labelled outputs).

### D. Independent results on the load-bearing enumerations

| claim | referee command | result |
|---|---|---|
| Lemma A cells (C1) | `ref_enum N M T 1000 0 1` for (5,3,2), (8,4,3), (10,6,4), (11,5,4), (13,7,5), (12,9,5) | out=0 in all six (nodes 2, 49, 2193, 79, 6003, 5931500); identical without (L5) |
| (10,7,≥4) (C2) | `ref_enum 10 7 4 1000 1 1` + `compare_classes.py` | 316 outputs; 6 classes, the same 6 as the authors' 637 outputs. |Aut| = 4, 2, 2, 6, 6, 4 (matching the proof's 4, 2, 2, 4, 6, 6, so Σ 10!/|Aut| = 6,652,800 = bf_cell). τ = 4 in all; P3 holds; exactly one class contains F7 |
| (13,8,≥5) (C2) | `ref_enum 13 8 5 1000 1 1` | 55 outputs; 2 classes, the same 2 as the authors' (|Aut| = 16 and 96); τ = 5; P3 holds; all 55 contain F7. The two explicit graphs in C2 are representatives of the two different classes, each with τ = 5 and one F7 copy as stated |
| Route I (C4) | `ref_ext 6 < out/ext_input_ref.txt` on MY 316 (10,7,4)+{10,11,12} and 55 (13,8,5) graphs, then `route1_summary.py` | graphs=371 tested=3116602 hits=1562 nonlinear=0. All 1,562 contain F7 (definitional test). The 588 degree-3 hits are all isomorphic to D14 |
| Route II (C5) | `ref_enum 14 11 6 3 1 1` (108 s) | nodes=394197530 out=672; 1 isomorphism class, the same as the authors' 998 outputs. It is D14: τ = 6, Δ = 3, |Aut| = 4, P3 holds, and all 672 contain F7 |
| HY-free Lemma A (new) | `ref_enum` on all 29 connected cells with n ≤ 13 and lo ≤ m but lo > hy (`out/nonwindow_cells.txt`) | Only (7,5,3) is non-empty: 4 outputs, all labelled copies of F7. The falsifier's `conn_dfs2` on the same 29 cells gives the same (only (7,5,3), found=9; up to 1,092,899,274 nodes at (13,11,6)). ref_bf at n = 7 gives (m,τ) = (5,3) exactly 420 = #labelled F7 |
| Remark cells (Step 9.1, not certified) | `ref_enum` (15,9,6), (16,8,6), (15,10,6) | out=0 in all three (nodes 751270, 6054, 63242928) |

### E. F7 detection

`ref_f7.py` works from the definition, not from Lemma F. A 5-edge subset with a 7-vertex union is F7 iff, after relabelling the union increasingly, it is one of the 420 labelled copies obtained by applying all 5040 permutations to {012,034,056,135,246}.

`test_f7.py` checks it as follows:
- On all 1,050 labelled linear 5-edge 3-graphs spanning [7], ref_f7, the Lemma F degree-pattern test and the prover's `f7check.has_f7` agree; there are 420 F7 copies. This verifies Lemma F exhaustively.
- Positive controls F7, AG(2,3), AG(2,3) minus 1 point, AG(2,3) minus 2 points and D14 are detected. D14 has exactly 2 copies.
- Negative controls are not detected: the Fano plane, Fano minus 2 lines (7 vertices, 5 edges), F7 minus an edge, and L(13) = {i, i+1, i+3} mod 13.
- On the authors' lists (`out/ref_f7_on_prover_lists.log`), ref_f7 gives: 3,186/3,186 for both hit files; 159/159 at (13,8,5); 126/637 at (10,7,4); 998/998 for both (14,11,6,Δ≤3) lists; all linear. This agrees with `f7check_results.json`.

### F. Descriptive claims (non-load-bearing, all exact)

`check_descriptive.py` and `check_misc.py`:
- 954 hits come from (13,8,5), 1,386 from the F7-containing (10,7,4) class and 846 from the five F7-free classes. In all 846, every F7 copy uses vertex 13.
- 1,180 hits have maximum degree 3, all isomorphic to D14; 2,006 have maximum degree 4.
- The Step 6.4 graph has degrees 3⁵2⁹, τ = 6 and |Aut| = 4. It is linear, contains F7 and is isomorphic to `f7_containing_violation.json`.
- `f7free_nonO_violation_9_8_4.json` is linear and F7-free with (n,m,τ) = (9,8,4) and s = −1.

## Problems found (in order of severity)

No mathematical or computational problem was found. The items below are non-blocking. None of them makes any statement of the certificate false, and none leaves a step unproved.

1. **Editorial: DEPENDS ON for K5.** The line for K3–K7 says "Used only in Step 8.1". Step 8.3 also cites K5 ("K5 gives m ≤ 12"), and K24 (Step 8.4) uses it too. The use in 8.3 is logically the consequence H(A) ∈ O+, hence m ≤ n−2, of Step 8.1, so nothing changes. Suggested wording: "Used in Step 8.1, and K5 again in Step 8.3 (m ≤ 12)".
2. **Editorial: the L004 caveat in Corollary 4.** Corollary 3 states L004's caveat (completeness re-checked by sampling). Corollary 4 rests on L005, whose own DEPENDS ON and LEDGER entry say it inherits that caveat, but Corollary 4 and L007's DEPENDS ON ("L004: Corollary 3 only") do not say so. The citation is accurate as written. For consistency, add "(inherits the L004 completeness caveat through L005)" to Corollary 4.
3. **Observation: method independence.** "Every enumeration ... run by two independently written programs" is true. Both programs implement the same canonical process, however, as the proof itself says, so they share Lemma D's logic. This review supplies a methodologically different enumerator (Section C), which reproduces every load-bearing result. No action is needed beyond citing it if desired.
4. **Optional strengthening: Henning–Yeo is not needed for Theorems 1 and 2.** Two different enumerators (Section D, row "HY-free Lemma A") show that every connected linear 3-graph with n ≤ 13, ⌈(n−1)/2⌉ ≤ m ≤ n−2 and 11τ > 3n+2m is isomorphic to F7. Cells with lo > m are empty because τ ≤ m. So Lemma A follows from (P1), (P2) and m ≤ n−2 alone. K8 is then used only in Corollary 3 (m ≥ 11) and, through K24, in Corollary 4. The authors may add this; it removes the dependence of Theorems 1 and 2 on a paper whose full text the project has not seen.

## Commands to reproduce this review

From experiments/referee/L007-round1/:
1. Build the tools: `gcc -O2 -o ref_enum ref_enum.c; gcc -O2 -o ref_bf ref_bf.c; gcc -O2 -o ref_ext ref_ext.c`.
2. Brute-force tallies: `for n in 3 4 5 6 7 8 9; do ./ref_bf $n > bf/bf_$n.txt; done`.
3. Validation and tests: `python3 validate_small.py 9; python3 test_f7.py; python3 cells_ref.py; python3 check_witness.py`.
4. Tight cells, Route II and class comparisons: `./ref_enum 10 7 4 1000 1 1 > out/ref_10_7_4.txt; ./ref_enum 13 8 5 1000 1 1 > out/ref_13_8_5.txt; ./ref_enum 14 11 6 3 1 1 > out/ref_14_11_6_3.txt`, then `python3 compare_classes.py <mine> <authors' list>`.
5. Route I: build `out/ext_input_ref.txt` (my (10,7,4) outputs plus (10,11,12), and my (13,8,5) outputs), run `./ref_ext 6 < out/ext_input_ref.txt > out/ref_ext_hits.txt`, then `python3 route1_summary.py`.
6. Remaining checks: `python3 cross_methods.py 11,7,4,1000 13,9,5,1000; python3 check_misc.py; python3 check_descriptive.py`.
7. HY-free Lemma A: the loops over `out/nonwindow_cells.txt` with `ref_enum` and `rerun/conn_dfs2`. Logs are in `out/`.
