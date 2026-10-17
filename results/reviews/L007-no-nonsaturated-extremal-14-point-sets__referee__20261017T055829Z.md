VERDICT: ACCEPT

# Referee report on L007-no-nonsaturated-extremal-14-point-sets (round 2)

- Claim: results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md (sha256 prefix 9030878fcd3a18a1, identical at the start (04:40 UTC) and end (05:58 UTC) of this review; this is the text after the 04:37 fixes of round 1).
- Referee: referee subagent, 2026-10-17, 04:40 to 06:00 UTC. Fresh review: round 1's scratch code was not used. Its report was read only to choose methods different from its lex-minimal enumerator.
- Scratch folder: experiments/referee/L007-round2/ (README.md lists every script). The authors' C sources were recompiled into `rerun/`. The authors' scripts that write files were copied into this folder and run with it as working directory. `sat_cell.py`, `iso_compare.py` and `member.py` only print, so they were run in place with `python3 -B`. No file outside the scratch folder and this review was created or modified.
- Machine: load average 9 to 12 on 4 cores from other jobs. All my jobs ran at nice 5 with at most 2 processes, apart from two sub-second slips with a third. Wall times are indicative only.

## Summary

The certificate proves Theorem 1: every 3-graph in O+ (linear, F7-free, e(S) ≤ |S|−2) with n = 14 and m = 11 has τ ≤ 5. The consequences are Theorem 2 (no 14-point (4,5)-set with h ≤ 8 and exactly 11 APs), Corollary 3 (every 14-point (4,5)-set with h = 8 is saturated, so the 2,910 classes of L004 are all of them, with L004's caveat) and Corollary 4 (with L005).

I re-derived the case analysis step by step and found it correct:
- the I11 slack is additive over components;
- K8 limits the problem to six window cells;
- Lemma A gives Δ ≤ 3, τ = 6 and connectivity;
- the slack-0 structure of H − v, and the two routes.

I re-ran every authors' computation that takes under 20 minutes from recompiled sources, and every count and file was reproduced exactly.

Then, as the independent load-bearing implementation, I decided every computational step with a SAT solver (CaDiCaL 1.5.3 via pysat). This method uses no canonical labelling at all. It is therefore methodologically independent of both authors' enumerators (Lemma D) and of round 1's lex-minimal enumerator. The encoding and its symmetry breaks were validated against my own labelled brute force on 1,456 small instances in each of three modes, with 0 mismatches, and by class-coverage tests. SAT confirms independently:
- the six window cells of Lemma A are empty;
- Route I case (i): no connected linear F7-free (13,8,≥5) graph exists;
- Route I case (ii): the extension structure has no linear F7-free completion with τ ≥ 6, decided directly, without any enumerated list;
- Route II: no connected linear F7-free (14,11,≥6,Δ≤3) graph exists. Without the F7 condition, a complete SAT enumeration of that cell yields exactly one isomorphism class, D14.

I also wrote two definitional F7 detectors, and tested the authors' two detectors against them, on positive and negative examples. I gave a hand proof of the window cell (13,7,5), and tested Lemma A and Theorem 2 on all available realizable data.

I found no mathematical or computational error. The remarks at the end are editorial and non-blocking.

## Step-by-step check of the argument

1. **Step 0.1 (components).** n, m and τ are additive over components, since a transversal restricts to a transversal of every component. So s is additive, and an isolated vertex has s = 3. Correct.
2. **Step 0.2 (heredity).** Induced subgraphs keep (P1) to (P3). The class O is closed under renumbering induced subgraphs. Correct.
3. **Step 0.3 (O ⊆ O+).** Midpoints of edges inside S lie in S∖{min S, max S} and are distinct. Correct.
4. **Step 0.4.** τ(H) − 1 ≤ τ(H−v) ≤ τ(H) and τ ≤ m. m ≤ n−2 is (P3) applied to S = V. K8 applies because H is linear and F7-free, which is the hypothesis as cited in kb/notes/henning_yeo_2021_affine.md. Correct.
   - Since F7 is a maximal linear 3-graph on its 7 points (checked: no triple can be added), induced and non-induced containment of F7 coincide for linear graphs. So the reading of "subhypergraph" in K7 and K8 does not matter here.
5. **Step 0.5.** A connected 3-graph with m edges has n ≤ 2m+1. Correct.
6. **Step 1 (window cells).** Recomputed by `arith.py`, enumerating τ directly with no floor formulas.
   - Window cells with n ≤ 16: (5,3,{2}), (8,4,{3}), (10,6,{4}), (11,5,{4}), (12,9,{5}), (13,7,{5}), (14,11,{6}), (15,9,{6}), (15,10,{6}), (16,8,{6}), (16,13,{7}), (16,14,{7}).
   - This is identical to the proof's table and lists for n ≤ 15.
7. **Step 2 (Lemma A).** A negative-slack H ∈ O+ with n ≤ 13 has a negative-slack component C ∈ O+ with n_C ≥ 3, lying in a connected cell with lo ≤ τ(C) ≤ min(hy, m_C). Hence C lies in a window cell, which C1 says is empty. Correct. The hand proof for (5,3) is correct.
8. **Step 3 (Lemma B).**
   - 11τ(H−v) ≤ 61 − 2d(v) and τ(H−v) ≥ 5 give d(v) ≤ 3 and τ(H−v) = 5, hence τ(H) = 6.
   - 33 ≤ 28 + d₃ gives d₃ ≥ 5.

   Rechecked by `arith.py`.
9. **Step 4 (Lemma C).**
   - s(G) = 0, and every component has s ≥ 0 (Lemma A), so all slacks are 0 and there are no isolated vertices.
   - The slack-0 connected cells with n ≤ 13 are exactly (3,1,1), (10,7,4) and (13,8,5), enumerated over all m and τ, with no modular shortcut.
   - The only size multisets summing to 13 are {13} and {3,10}.

   So the dichotomy (i)/(ii) is correct.
10. **Step 5 (Route I).**
    - 5.1 needs: every connected linear (13,8,≥5) graph contains F7.
    - 5.2 needs the extension statement. The three edges at v give pairwise disjoint pairs, none inside an edge of G (linearity), so H is isomorphic to an enumerated extension.
    - The reduction in `ext_indep.c` is valid: since τ(G) = 5, a transversal of H of size ≤ 5 avoids vertex 13.

    Correct.
11. **Step 6 (Route II).** H is connected, since otherwise s(H) ≥ 0 > −2, and Δ ≤ 3 by Lemma B. C5 then applies. Correct.
12. **Step 7.** W and the Fibonacci set {F₃..F₁₆} were verified from the definitions (`witness_check.py`, below). Correct.
13. **Step 8.**
    - 8.1 uses K3 to K7 correctly.
    - 8.3: 102 ≤ 70 + 3m gives m ≥ 11, and K5 gives m ≤ 12.
    - 8.4 needs only f(15) ≥ 9 and f(14) ≥ 8. Both follow at once from K8 with m ≤ n−2: τ ≤ 6 at n = 14 and at n = 15.
    - L005's Statement is indeed for every 14-point (4,5)-set with h = 8 and m = 12 (via L004). Both corollaries state the inherited L004 completeness caveat.

    Correct.
14. **Lemma D.** I checked (D1) to (D5) line by line. In (D1), the parenthetical correctly excludes a vertex labelled earlier in the same turn: the two edges at x would share two vertices.
    - In `conn_dfs2.c`, the key order (a) < (b) < (c) is right, and keys are non-decreasing with equal keys possible only for (c).
    - `conn_dfs2.c` prunes by `cover_le(all, tau0−r−1)` (exact branching), `v>n || v+2r<n`, `cur>=v` and the degree caps. None of these fires on the canonical branch.
    - `enum_conn.c` uses phases A/B/C with a, b < vstart and strictly increasing pairs, and its `viable()` test is valid.
    - No size limit is reached: 32-bit masks with n ≤ 16, `E[16]` with m ≤ 11, `t5[1300]` ≥ C(13,5) = 1287, `pr[78]` = C(13,2).
    - `conn_dfs2_all.c` differs from `conn_dfs2.c` only in printing (diff checked).

## Checks performed (all in experiments/referee/L007-round2/)

### A. Arithmetic
`python3 arith.py` prints:
- the window cells above;
- slack-0 connected cells `[(3,1,1),(10,7,4),(13,8,5)]` (and disconnected-only (6,2,2), (9,3,3), (11,0,3), (12,4,4));
- multisets `[(3,10),(13,)]`;
- d ∈ {0,1,2,3}, τ(H−v) = 5, d₃ ≥ 5;
- m ∈ {11,12} at n = 14, τ = 6;
- s(14,11,6) = −2;
- h ≥ 8 at n = 14 and h ≥ 9 at n = 15.

### B. Re-runs of the authors' computations (recompiled with gcc 13.3.0 -O2)

| item | command | output (identical to the proof) |
|---|---|---|
| C1 falsifier | `rerun/conn_dfs2 N M T` on the 6 window cells | nodes 16, 151, 8448, 197, 19596, 18326058; found=0 for all |
| C1 prover | `rerun/enum_conn N M T 1000 0` | calls 52, 265, 15580, 249, 23256, 34515249; found=0 for all |
| C2 | `conn_dfs2_all 10 7 4` and `13 8 5` | nodes=102701 found=637 and nodes=1295881 found=159; `cmp`-identical to the falsifier's files |
| C2 | `enum_conn 10 7 4 1000 1` and `13 8 5 1000 1` | calls=220291 found=637 and calls=1773159 found=159; `cmp`-identical to the prover's files |
| C2 classes | `iso_compare.py ... details` (prover's, read-only, `-B`) | 6 classes, the same in both lists, exactly one containing F7; 2 classes, the same in both, both containing F7; τ = 4 and 5 respectively; P3 holds for all |
| C4 input | `build_ext_input.py` (my own parser, from my re-run outputs) | 796 graphs, equal as a multiset to `ext_vertex_input.txt` |
| C4 | `ext_vertex_all` on my input and on the stored input | `graphs=796 tested=6699128 hits(tau>=6)=3186` both times; the stored-input output is `cmp`-identical to `ext_vertex_hits.txt` |
| C4 | `ext_indep` on my input | `graphs=796 bad_tau=0 tested=6699128 hits(tau>=6)=3186`; the three hit lists are equal as sets |
| C5 | `enum_conn 14 11 6 3 1` (620 s) | `calls=2468940032 found=998`; byte-identical to `indep/mine_14_11_6_deg3.txt`; equal as a labelled set to the falsifier's `conn2_all_14_11_6_deg3.txt`; `member.py`: 998/998 isomorphic to `f7_containing_violation.json` in both lists |
| C6 (remark) | `conn_dfs2` and `enum_conn` on (15,9,6), (16,8,6), (15,10,6) | nodes 2459440, 19144, 186011577 and calls 2534511, 18778, 216656914; found=0 for all |
| C0 | `bf_cells n`, n = 3..9 | byte-identical to the stored `bf_n*.txt` |
| C0 | `compare_bf.py mine` and `theirs` (copies run in `c0/`) | both `cells compared: 393 mismatches: 0 nonempty cells: 243 total classes: 1600` (327 s and 266 s) |
| C0 | `bf_cell 10 6 4`, `11 5 4`, `10 7 4` | nodes=14908931 labelled=0; nodes=2300156 labelled=0; nodes=150569981 labelled=6652800 |
| C1 extra | `sat_cell.py 8 4 3`, `10 6 4`, `11 5 4` | sat=false for all three |
| C7 | `check_witness_records.py`, `witness_14_11.py` (copies in `misc/`) | W is a (4,5)-set with the 11 listed APs and h = 9; 291 sets with m = 11, all with h = 9; record-set values as in the Sanity checks |

Not re-run:
- `conn_dfs2_all 14 11 6 3` (1,747 s, over the 20-minute limit). Its stored output equals my `enum_conn` re-run as a labelled set, and the SAT checks in D below cover it.
- `sanity_m11_sets.py 200`. I replaced it with my own test on a disjoint sample (section H, part C).

### C. My own brute force
`bf_ref.c` enumerates all labelled linear 3-graphs on [n], tallying the connected spanning ones by (m, τ, Δ, hasF7). Summed over hasF7, its tallies are identical to the prover's `bf_n*.txt` for every n ≤ 9, with 19,371,345 labelled graphs at n = 9. At n = 7 the (5,3,3) cell is exactly 420 labelled F7 copies, and there are 30 Fano planes.

So `compare_bf.py` (0 mismatches above) also validates both enumerators against my brute force.

### D. Independent implementation: SAT decision of every computational step (`sat_ref.py`)

**Encoding.** There is one variable per triple of [n], with:
- pairwise at-most-one per vertex pair (linearity);
- a sequential counter for exactly m edges;
- for every (t−1)-subset S, a clause "some edge avoids S" (τ ≥ t);
- one cover clause per vertex;
- connectivity, either by lazy cut clauses or eagerly, by one cut clause per vertex set containing 0;
- optional degree caps;
- one clause per F7 copy of K_n^(3) when F7-freeness is required.

The F7 clause generator gives exactly the 420 definitional copies on [7] and C(n,7)·420 distinct copies on [n] (checked for n = 8, 9, 10 and 14).

**Symmetry breaking (sound, proved in the code header).**
- (SB1) Split on d0 = Δ. Vertex 0 has degree d0 with edges {0,1,2}, …, {0,2d0−1,2d0}, and all degrees are ≤ d0. Take a maximum-degree vertex: by linearity its edges meet only in it, so it can be relabelled this way.
- (SB2, only where stated) Lex-leader constraints X ≤lex σ(X) for the involutions σ that fix 0 and permute the forced edges: the within-pair swaps, the swaps of consecutive pairs, and the adjacent transpositions of free vertices. Every constraint family is σ-invariant, so the lex-least member of any orbit survives.
- Splits d0 < ⌈3m/n⌉ are dropped only where noted, by the averaging bound Δ ≥ 3m/n.

**Validation.**
- `validate_sat.py 9 [lazy|eager] [lex]` covers every n = 3..9, m ≤ m_max+1, t ≤ τ_max+1, D ∈ {1,2,3,∞} and F7-free on/off. In each of the three modes it reports `{"instances": 1456, "nonempty": 269, "mismatches": 0}` against my brute force. Every SAT witness was re-verified from scratch.
- Class coverage of SB1+SB2 (`lex_coverage.py`, `lex_coverage2.py`): the complete SAT enumeration with blocking clauses yields exactly the isomorphism classes of the authors' outputs, all covered and none extra:

  | cell | classes | lex-leader solutions |
  |---|---|---|
  | (9,6,≥3) | 24 | 56 |
  | (10,7,≥4) | 6 | 17 |
  | (11,7,≥4) | 40 | 132 |
  | (13,8,≥5) | 2 | 7 |
  | (14,11,≥6,Δ≤3) | 1 | 37 |

**Results.**

| statement | instance | result |
|---|---|---|
| Lemma A cell (5,3,2) | all d0 | UNSAT (0.0 s) |
| (8,4,3) | d0 = 1..3 | UNSAT (0.0 s) |
| (10,6,4) | d0 = 1..4 | UNSAT (0.3 s) |
| (11,5,4) | d0 = 1..5 | UNSAT (0.9 s) |
| (13,7,5) | d0 = 1..6 | UNSAT (d0 = 2: 201 s; others ≤ 6 s) |
| (12,9,5) | d0 = 1..5 | UNSAT (d0 = 3: 231 s; d0 = 2: 6.6 s; others ≤ 16 s) |
| controls, one τ lower | (8,4,2), (10,6,3), (11,5,3), (13,7,4), (12,9,4) | SAT, with witnesses |
| Route I case (i) | connected linear F7-free (13,8,≥5), d0 = 3..6; d0 = 2 below; d0 = 1 excluded since 24 > 13 | UNSAT (260 s); control without F7: SAT, τ = 5, the witness contains F7 |
| Route I case (ii) | H on [14]: 7 edges inside {0..9}, connected and spanning; the edge {10,11,12}; exactly 3 edges at 13; linear, F7-free, τ ≥ 6; SB1 on C, d0 ∈ {3,4} (Δ(C) ≥ ⌈21/10⌉) | UNSAT (29 s + 12 s); control without F7: SAT, τ = 6, the witness contains F7 |
| Route II (C5) | connected linear F7-free (14,11,≥6,Δ≤3), d0 = 3 (degree sum 33 > 28), SB1+SB2, 721,588 F7 clauses | UNSAT (62.5 s); control without F7: SAT, isomorphic to D14 and containing F7 (with and without SB2) |

A second Route II run with SB1 only, no lex-leader constraints, was still running after 56 minutes (42 CPU-minutes) when this report was written, with no result. It is not used.

**Δ ≤ 2 sub-cases by a different reduction (`dual_13_7.py`, `dual_bf.c`).** For a connected linear H with Δ ≤ 2, the dual graph G* (nodes = edges of H, one edge per degree-2 vertex) is simple and connected, with max degree ≤ 3, and τ(H) = m − ν(G*). This identity was proved here and checked on 300 random instances.
- (13,7,5): all 203,490 graphs with 7 nodes and 8 edges were checked. 56,070 are connected with Δ ≤ 3, and none has ν ≤ 2.
- Case (i) with d0 = 2: there are 328,020 graphs with 8 nodes, 11 edges and Δ ≤ 3, and none is connected with ν ≤ 3.
- Positive controls: 56,070 and 327,600 respectively when the ν bound is relaxed by one.

**Hand proof of the window cell (13,7,5)** (independent of all code).
- If d(v) ≥ 3, then H − v has ≤ 4 edges and τ ≥ 4, so it is a 4-matching covering the other 12 vertices. The 3 edges at v connect the 4 matching edges in a spanning tree. Orienting the tree away from a root picks one vertex per matching edge that hits all 3 edges at v, so τ ≤ 4.
- If Δ ≤ 2, then τ = 7 − ν(G*) with G* connected, 7 nodes, 8 edges, Δ ≤ 3. By Tutte–Berge, ν ≤ 2 would need a set U with odd(G*−U) ≥ |U|+3. This is impossible: for |U| = 0 there is 1 odd component; for |U| = 1 there are ≤ 3 components; for |U| = 2 all 5 other nodes would be isolated, leaving ≤ 6 edges < 8.

### E. F7 detection
- `f7_ref.py` has two detectors written from the definition. det_A checks every 5-subset of edges with a 7-vertex union against all 420 labelled F7 copies on {0..6}. det_B is a networkx subgraph monomorphism of the typed incidence graph of F7.
- Positive controls, all detected: F7, F7 relabelled, AG(2,3), AG(2,3) minus 1 point, AG(2,3) minus 2 points, and D14.
- Negative controls, none detected: the Fano plane, the Fano plane minus 2 lines, F7 minus an edge, L(13) = {i,i+1,i+3} mod 13, a linear 5-cycle and a 4-star.
- On all 1,050 labelled linear 5-edge 3-graphs spanning [7], the two detectors agree (420 contain F7). Lemma F's degree-pattern test agrees on all 1,050 (`lemmaF_check.py`), so Lemma F is verified by exhaustion. They also agree on 400 random linear graphs.
- `test_their_f7.py` tested the authors' detectors against det_A on 1,800 graphs, 818 containing F7 (F7 planted under random relabellings in random linear supergraphs, plus random graphs). Both `f7check.has_f7` and `e757.cpsat_model.find_f7` gave 0 disagreements. `find_f7` returns the exact copy count on 300 maximal linear graphs.
- On every list of the proof, det_A and det_B (which agree everywhere) give:

  | list | contain F7 |
  |---|---|
  | each of the 3 hit lists | 3,186 of 3,186 |
  | (13,8,5), both lists | 159 of 159 |
  | (10,7,4), both lists | 126 of 637 |
  | (14,11,6,Δ≤3), all three lists | 998 of 998 |

  Every graph in these lists is linear and distinct.

### F. Lemma D tested empirically
- `canon_branch_test.py`: my own implementation of the canonical process, with a random start vertex and random orders of (c)-edges and of pair labels. On 60 random connected linear graphs (n ≤ 11), all 300 canonical labelled copies appear in the outputs of both `conn_dfs2_all` and `enum_conn` with parameters (n, m, τ(H), Δ(H)).
- `d14_check.py`: 200 of 200 canonical copies of D14 appear in the 998 list. D14 has τ = 6, |Aut| = 4, degrees 3⁵2⁹, is linear and satisfies P3, contains F7, and is isomorphic to `f7_containing_violation.json`. This matches Step 6.4.

### G. Witnesses (Step 7)
`witness_check.py` checks the (4,5) property from the definition and computes h twice: by testing all 2^14 subsets for distinct differences, and by a CP-SAT maximum Sidon subset.
- W: (4,5), m = 11, h = 9 by both methods; its 11 APs are exactly the proof's list; W − 323 = (A_base∖{136}) ∪ {−323}.
- {F₃..F₁₆}: (4,5), m = 11, h = 9.
- A_base: (4,5), m = 12, h = 8.

### H. Lemma A and Theorem 2 on realizable data (`data_tests.py`; τ by exact branching)
- Part A: all 64,756 subsets with ≤ 13 points of the record sets in data/small_records.json (n = 8, 10, 11, the three 12-point sets and A_base), W and {F₃..F₁₆} show 0 violations of 11τ ≤ 3n+2m. W and Fibonacci (m = 11) have τ = 5.
- Part B: all 305,550 13- and 12-point subsets of the 2,910 census classes show 0 violations.
- Part C: from census classes 2000 to 2199 (disjoint from the prover's sample of classes 0 to 199), sets of the form class ∪ {x in a new AP} minus a point give 57,324 distinct fourteen-point (4,5)-sets with exactly 11 APs. All have h = 9, as Theorem 2 predicts.

### I. Descriptive claims (not load-bearing)
`hits_descr.py`, with my own F7-copy routine, gives:
- 954 hits from (13,8,5), 1,386 from the F7-containing (10,7,4) class and 846 from the F7-free classes; in all 846, every F7 copy uses vertex 13;
- maximum degree 3: 1,180 hits, all isomorphic to D14; maximum degree 4: 2,006.

The class counts of C2 (2 and 6) and the uniqueness of D14 in Step 6.4 are also confirmed by the SAT class enumeration in D.

## Problems found (in order of severity)

No mathematical or computational problem was found. Every load-bearing step was re-derived or recomputed, and confirmed by a method independent of the authors' (and of round 1's). The remarks below are editorial; none makes a statement false or leaves a step unproved.

1. **Method independence (observation).** The header says every enumeration "was run by two independently written programs". That is true, but both implement the same canonical process (Lemma D), as C2 itself notes. Methodologically independent confirmations now exist: round 1's lex-minimal enumerator and this review's SAT decisions. The latter cover all window cells, both Route I cases without enumerated lists, and Route II. The authors may cite them; no change is required.
2. **Dependence on K8 (optional strengthening, as in round 1).** Theorems 1 and 2 use K8 only to reduce Lemma A to the window cells. Round 1 reports that, without K8, the only connected linear graph with n ≤ 13, m ≤ n−2 and 11τ > 3n+2m is F7. I did not re-check that extension, and it is not needed: K8 is [published] via Ma–Tang Thm 5.3, and its hypotheses (3-uniform, linear, F7-free) hold for every graph to which it is applied.
3. **Inherited scope (already stated).** Corollaries 3 and 4 inherit the completeness caveat of the L004 census (sampling re-check), and the proof states this explicitly. Theorems 1 and 2 and Lemma A do not depend on L004 or L005.

## Commands to reproduce (from experiments/referee/L007-round2/)
1. Arithmetic and witnesses: `python3 arith.py; python3 witness_check.py`.
2. Re-runs: compile into `rerun/` (see README.md), then run the C1/C2/C4/C5/C6 commands of table B. Then:
   - `python3 build_ext_input.py`;
   - `./c0/run_c0.sh`;
   - `./misc/run_misc.sh`.
3. Brute force and SAT validation:
   - `gcc -O2 -o bf_ref bf_ref.c; for n in 3 4 5 6 7 8 9; do ./bf_ref $n > bf/bf_$n.txt; done`;
   - `python3 validate_sat.py 9 lazy; python3 validate_sat.py 9 eager; python3 validate_sat.py 9 eager lex`.
4. SAT decisions:
   - `python3 run_window_sat.py; python3 run_12_9_5.py`;
   - `python3 run_route1_sat.py case_i|case_ii|case_i_nof7|case_ii_nof7`;
   - `python3 run_route2_lex.py control|main`;
   - `python3 lex_coverage.py 9,6,3,100 10,7,4,100 13,8,5,100; python3 lex_coverage2.py`.
5. Dual graphs and the remaining checks:
   - `python3 dual_13_7.py; gcc -O2 -o dual_bf dual_bf.c; ./dual_bf 7 8 2; ./dual_bf 8 11 3`;
   - `python3 f7_ref.py <lists>; python3 test_their_f7.py; python3 lemmaF_check.py`;
   - `python3 canon_branch_test.py; python3 d14_check.py; python3 data_tests.py 2000 2200; python3 hits_descr.py`.
