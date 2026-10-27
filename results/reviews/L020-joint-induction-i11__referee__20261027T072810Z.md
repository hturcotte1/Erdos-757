VERDICT: NEEDS-WORK

# Referee report on results/proofs/L020-joint-induction-i11.md: round 1, referee #1 (opus)

## Summary

I found no mathematical error, and Conjecture T'' is refuted. I checked everything load-bearing with my own code, which imports nothing from e757/, judge/ or the prover's scripts; the prover's files were read as data only. The scratch folder is experiments/referee/L020-round1-opus/.

**Theorem 1 holds.** I took the explicit graph $K_{29}$ directly from the certificate text. It is 3-uniform and linear. It is $F_7$-free: none of its 33,649 five-edge subsets forms $F_7$, by two separate tests. It satisfies (P3) by an exhaustive check over all $2^{23}$ edge subsets (the minimum of $|\bigcup E'|-|E'|$ is 2), and separately by my own Hall/Kuhn matching test for all 406 vertex pairs. It is connected, with $\Delta=3$ and degree multiset $2^{18}3^{11}$. Its transversal number is $\tau=12$: my own branch and bound gives 12, the CP-SAT optimum is 12, and CP-SAT proves that no transversal has at most 11 vertices. So the slack is $87+46-132=1$.

**The 45 classes.**
- The same checks pass for all 45 classes, and the 45 are pairwise non-isomorphic (45 distinct colour-refinement invariants).
- I rebuilt them from the stored lists and got exactly the prover's 45 classes:
  - 24 of the 953 $(20,15,8,3)$ classes carry an e-configuration, one each;
  - the two $(8,5,3)$ classes carry 2 and 3;
  - this gives 120 gluings, all in $C$, all with $\Delta\le3$ and $\tau=12$.
- Theorem 1(i)–(iii) hold for all 45:
  - I enumerated all minimum transversals, 18,283 to 20,912 per class;
  - for classes 0 to 2 I cross-checked the enumeration by direct exact searches for all 29 vertices and all 406 pairs;
  - there are no NC pairs and no pair-pair failures;
  - each class has exactly 6 uncovered triples out of about 4.08 million, and none of the 6 gives $K+v\in C$.

**The hand proofs and the reduction.** I checked Theorems 2 and 3, Proposition 6 and the logic of Theorem 4 and Corollary 5 line by line. I also tested them numerically:
- Lemma 2.1 on all 5,389 subcubic graphs with at most 10 vertices;
- Theorem 2 on 3,000 random linear 3-graphs with $\Delta\le2$;
- Theorem 3 at all 4,111 degree-3 vertices of the stored near-tight graphs and at the 495 degree-3 vertices of the 45 classes, with 0 failures;
- the equivalences of Theorem 3, by synthetic two-sided tests in which ($\star$) is computed directly;
- the role facts of L017 C5 used in Step 4.3, re-derived on the 483 small near-tight graphs;
- Proposition 6 on all 204 NC pairs.

**Why NEEDS-WORK.** The verdict comes only from editorial inaccuracies that must be fixed before acceptance; in the workflow's vocabulary this is ACCEPT WITH FIXES. The main ones:
- One sentence of Theorem 1 says that "the same classes also arise" by pattern (f) from $(18,13,7,3)+(10,7,4)$ and by pattern (b) from $(25,19,10,3)+E_1$. Read as "all 45 classes", this is false: only 27 of the 45 have the first kind of vertex and 31 of the 45 the second, and the prover's pattern-(b) sample reached only 4.
- The DEPENDS ON entry for L017 is stale.
- The b-configuration counts in C3 and C8 use a narrower notion than the certificate's own definition.

## Independence statement

I did not read any other review of L020; none existed when I started. I used no code from e757/, judge/, experiments/prover/L020/ or experiments/prover/L017/. Data files were read as data only:
- experiments/prover/L020/K29_classes.json, bf_18_13_7.json and bf_25_19_10_sample.json;
- the stored lists in experiments/20261027-0300-transversal-richness/inputs/ and experiments/prover/L017/out/.

| Purpose | Own script (experiments/referee/L020-round1-opus/) | Method |
|---|---|---|
| shared routines | `hg.py` | see the methods listed below |
| Theorem 1 | `t1_verify.py`, `iso_check.py`, `t1_roles_triples.py`, `glue_check.py`, `k29_decomp.py` | |
| Theorem 3 | `t3_check.py`, `t3_perclass.py`, `t3_equiv.py`, `t3_equiv2.py` | |
| L017 C5 role facts and Proposition 6 | `roles_check.py` | |
| Theorem 2 and Lemma 2.1 | `t2_check.py` | own bitmask DP for $\nu$ |
| cell table of Step 4.3 | `cells_enum.py` | |
| Observation 7 | `obs7_perclass.py`, `theta_rebuild.py` | |
| prover's (b)/(f) outputs | `bf_classes.py` | |
| b-configurations in slack-2 cells | `bcfg_slack2.py` | |

Methods in `hg.py`:
- (P3) exhaustively with numpy, and separately by an own Kuhn augmenting-path matching;
- $\tau$ by an own branch and bound and by OR-tools CP-SAT;
- all minimum transversals by an exclusion-branching enumerator in which each transversal is reached exactly once;
- colour refinement with a global colour table, for non-isomorphism;
- exact isomorphism by backtracking.

External tools: nauty `geng` was used only to generate the subcubic graphs for Lemma 2.1, as the prover did, but $\nu$ was computed by my own code; OR-tools was used for CP-SAT. Every command ran under `nice -n 10` and `timeout`, with essentially one process at a time.

## Checks performed (commands run from experiments/referee/L020-round1-opus/; outputs in the `*_output*.txt` files there)

### (a) Theorem 1

1. **The explicit graph.** `python3 t1_verify.py` → `t1_verify_output.txt` (also `t1_k29_from_text_output.txt`).
   - $K_{29}$ is parsed with a regular expression from the two displayed formulas of the certificate: 23 edges on the vertex set $\{0,\dots,28\}$.
   - Results:
     - 3-uniform with distinct edges; linear;
     - 0 copies of $F_7$ among all 33,649 five-edge subsets (a structural test and a brute-force test over $7!$ maps, asserted to agree);
     - (P3): exhaustive minimum of $|\bigcup E'|-|E'|$ over all $2^{23}-1$ nonempty edge subsets $=2$, and the Hall/Kuhn test passes for all 406 pairs;
     - connected, $\Delta=3$, degrees $\{2:18,3:11\}$;
     - $\tau_{\rm B\&B}=12$, $\tau_{\rm CP\text{-}SAT}=12$, CP-SAT proves no transversal of size $\le11$, and the own search finds no 11-transversal;
     - slack $=1$.
   - $K_{29}$ is literally class 0 of `K29_classes.json`.
   - The same checks pass for each of the 45 classes ("ALL 45 OK", degree multiset $2^{18}3^{11}$ in all 45).
   - Completeness of the (P3) check: (P3) holds iff $|E'|\le|\bigcup E'|-2$ for every nonempty edge set $E'$. Given $S$, take $E'=E(S)$, so that $\bigcup E'\subseteq S$; conversely take $S=\bigcup E'$. So enumerating all edge subsets is the definition itself, not a criterion. I also checked the certificate's Hall equivalence in Step 1.1 by hand: both directions are correct, and $|S|-2=|\bigcup E'\setminus\{x,y\}|$ holds in all cases.
2. **Pairwise non-isomorphism.** `python3 iso_check.py` gives 45 distinct invariants, so no collisions. A self-test confirms that random relabellings are recognised as isomorphic, 0 failures. The invariant is computed with a shared colour table, so isomorphic graphs receive identical invariants and different invariants prove non-isomorphism.
3. **Theorem 1(i)–(iii) on all 45 classes.** `python3 t1_roles_triples.py` → `t1_roles_triples_output.txt`. For every class:
   - all minimum transversals: 18,283 to 20,912, the same range as the certificate;
   - every vertex lies in a minimum transversal;
   - 0 NC pairs among the 18 vertices of degree 2;
   - 337 pairs not inside an edge;
   - 0 pair-pair failures;
   - about 4,078,620 triples of pairwise disjoint such pairs examined, exactly 6 uncovered, and for all 6 my own test gives $K+v\notin C$; "TOTAL K+v in C among uncovered triples: 0".
   - For classes 0, 1 and 2 the co-transversality of every vertex and of every one of the 406 pairs was recomputed by direct exact searches, without the enumeration: 0 mismatches.
   - Hence (i), (ii) and (iii) hold, and so do "every admissible triple is covered" and "$\tau(K+v)=12$, slack 10" (by 0.3).
4. **Independent rebuild of the construction.** `python3 glue_check.py` → `glue_check_output.txt`.
   - $(20,15,8,3)$: 24 of 953 classes have an e-configuration, exactly one each.
   - $(8,5,3)$: 2 and 3 e-configurations.
   - Gluings: 120. All 120 are in $C$ by both the Hall test and the exhaustive (P3) check, have $\Delta\le3$, have $\tau=12$ and are connected.
   - They fall into 45 classes, which match the prover's 45 classes one to one.
   - `k29_decomp.py`: at $v=28$, $K_{29}-v=F\sqcup X$ with $F$ in $(20,15,8)$, slack 2, e-configuration $(0;1,12)$, isomorphic to stored class 61, and $X$ in $(8,5,3)$, slack 1, $\Delta=2$, e-configurations $(20;21,23),(20;22,23)$, isomorphic to stored class 0. This is as stated.
5. **"At least 45", and whether the generation can miss classes.**
   - **The claim is correct as a lower bound.** The certificate claims "at least 45". 45 pairwise non-isomorphic members are verified.
   - **The 45 are exactly the classes with a pattern-(e) vertex, unconditionally given the refereed lists.** Let $K$ lie in cell$(29,23,12,3)$ and let $v$ be a vertex at which $K-v$ has pattern (e). Then both components have at most 25 vertices, so by L016 (I11 below 28 vertices, so (H$_{29}$) is not needed):
     - $\tau(K-v)=11$ and the component slacks sum to 3;
     - free choice holds in both components;
     - both components therefore carry e-configurations (Step 3.7).
   - Then:
     - small tight graphs have no e-configuration (my C5 re-check below);
     - a tight $(25,23,11)$ component would leave $E_1$ and total slack 0, which is impossible;
     - so the slacks are $(1,2)$;
     - the slack-1 component, with at most 25 vertices, must be an $(8,5,3)$ graph (all slack-1 cells up to 25 vertices are computed);
     - so the other component is a $(20,15,8,3)$ graph.
   - Hence, given the completeness of the refereed lists $(20,15,8,3)$ and $(8,5,3,3)$, **the 45 classes are exactly the classes of cell$(29,23,12,3)$ that have a pattern-(e) vertex.**
   - **The same 45 arise from the triangle.** `obs7_perclass.py` shows that every one of the 45 also has a $\Theta$-vertex (triangle $+(22,17,9)$). Conversely, `theta_rebuild.py` → `theta_rebuild_output.txt` re-runs every $\Theta$-gluing: all 6 f-configurations of the triangle, every NC pair of every $(22,17,9,3)$ class in both orientations, and C, $\Delta\le3$ and $\tau$ tested. It gives 564 near-tight graphs with 29 vertices, as in C9; they hit all 45 classes and no others. So, by the same argument as above, the 45 are also exactly the classes with a $\Theta$-vertex.
   - **Classes without a pattern-(e) vertex cannot be found by this method.** That covers any class whose degree-3 vertices are all of pattern (a), where $K-v$ lies in $(28,20,11,3)$, an uncomputed cell. The prover's other searches do not close this gap:
     - pattern (f) with $(18,13,7,3)+(10,7,4)$ is complete and reached only 27 of the 45;
     - pattern (b) and (f) with $(25,19,10,3)+E_1$ ran on a 3,000/35,645 sample only.
   - So the true size of cell$(29,23,12,3)$ is unknown, as the certificate says in W2 and Open problem 4. "At least 45" is the correct form.
6. **Pattern profile of the 45 classes.**
   - `t3_check.py` on `K29_classes.json`, over 495 degree-3 vertices: (a) 216, (b) 45, (e) 72, (f) 162, failures 0.
   - `t3_perclass.py` (per-class profiles):
     - every class has 1 or 2 pattern-(e) vertices of type $(8,5,3)+(20,15,8)$;
     - every class has 3 pattern-(f) vertices of type $(6,3,2)+(22,17,9)$;
     - only 27 classes have a pattern-(f) vertex of type $(10,7,4)+(18,13,7)$;
     - only 31 classes have a pattern-(b) vertex of type $E_1+(25,19,10)$.
   - `bf_classes.py`: the prover's `bf_18_13_7.json` gives 48 labelled graphs with 29 vertices, hitting exactly 27 classes, all among the 45. `bf_25_19_10_sample.json` gives 4 graphs hitting 4 classes. This is the basis of Problem 1.

### (b) Theorem 2

- **Proof check.** I re-derived the dual-graph identity: $\tau=m-\nu(G^*)$ and $s=3n_0+11\nu(G^*)-3n_2$, using $3m=n_1+2n_2$. I checked the Tutte–Berge computation of Lemma 2.1 case by case: $c_i=1,\dots,5$, even $c_i\ge6$, and odd $c_i\ge7$, where $t_i\ge(c_i-5)/7$.
- **The connectivity step.** $G^*$ is connected when $H$ is. This gives:
  - $n_2\ge m-1$, so $7s\ge m-1$;
  - $s\le1\Rightarrow m\le8$ and $n\le2m+1\le17$;
  - $s\le3\Rightarrow m\le22$, $n\le45$;
  - $n\ge18\Rightarrow m\ge9$.
- **Numerics.**
  - Lemma 2.1: `geng -q -D3 N` for $N=1..10$ piped into `python3 t2_check.py lemma`. Result: 5,389 graphs, 0 failures, equality with $|E|>0$ in 7 graphs (the subdivided $K_4$ `D]w`, plus isolated vertices or a second copy). This matches C6.
  - Equality characterisation: equality forces $U=\emptyset$ and every component to be an isolated vertex or the unique 5-vertex, 7-edge subcubic graph, so the claim holds in general, not only up to 10 vertices.
  - Theorem 2: `python3 t2_check.py thm 3000`. 3,000 random linear 3-graphs with $\Delta\le2$, 596 of them connected with $m\ge2$; the identity, $\tau=m-\nu$, $7s\ge21n_0+n_2$ and $7s\ge m-1$ hold: 0 failures.
- **Tag.** Lemma 2.1 is also a consequence of Chvátal–Hanson ($|E|\le3\nu+\lfloor\nu/2\rfloor$), as the certificate notes.

### (c) Theorem 3

- **Proof check.** I re-derived every step by hand:
  - (i): distinctness, degrees, $\tau(G)=\tau(K)-1$ via $s(G)=s(K)-9$ otherwise, and ($\star$);
  - (ii): $|Y|\le1$, and if $Y\ne\emptyset$ then $s=1$ and all components are tight;
  - (iii): free choice by (U) with $s(F_i)\le3<5$; pair richness, where $F_i^+$ has at most $n(K)$ vertices and $s(F_i^+)=s(F_i)-4<0$; the pair lemma;
  - (iv): the Hall argument, the exclusion of two pairs inside one component when $r\ge2$, $r\le2$, and the type classification $\{s,s,s\},\{1,2,s\},\{1,s,s\}$, which is complete up to symmetry;
  - (v): the targets argument, $r=3$ only in shape (i3), and the five $r=2$ shapes with their conditions.
- **The equivalences of 3.7 and 3.8.** All are correct in both directions and use only free choice and the product structure of the minimum transversals of $G$.
- **Hypotheses.** Every application of (H$_{n(K)}$) is to a graph with at most $n(K)$ vertices.
- **Numerics.**
  - `t3_check.py` on the nine stored lists, output in `t3_check_stored_output.txt`: 482 graphs, 4,111 degree-3 vertices, patterns (a) 3,223, (b) 145, (e) 183, (f) 506, (i1) 39, (i2) 15 (all of type (i2-4)), 0 failures. This is identical to the certificate's C4. The checks include every conclusion of (i)–(v), the pair lemma on every NC pair of every component, and $F_1+w(P_1,\{c,e\})\notin C$ in pattern (f).
  - Pair richness (`--deep`, `t3_check_deep_output.txt`): on 5 small lists and 3 of the 45 classes, every pair of disjoint pairs that no minimum transversal meets gives $F_i+w\notin C$ (106 such tests on $(15,11,6)$ alone): 0 failures.
  - The 45 classes: 495 vertices, 0 failures, although (H$_{29}$) is not known.
  - Synthetic two-sided tests: $G$ is a disjoint union of stored graphs with free choice, attachments of the shapes (b), (e), (f), (i2-1)…(i2-4), (i3), and ($\star$) computed directly as $\tau(G+w)=\tau(G)+1$.
    - Random runs (`t3_equiv.py`, seeds 7 and 5): 2 × 1,200 configurations, 0 disagreements, with ($\star$) true in 34 and 29 of them.
    - Condition-forced run (`t3_equiv2.py 5 60`, output in `t3_equiv2_output.txt`): attachments built from the components' b-, e- and f-configurations and NC pairs so that the stated condition holds. In 60 of 60 configurations per pattern, for all 8 patterns, ($\star$) holds; 0 counterexamples. Here ($\star$) is evaluated from its definition over the product of the components' minimum transversals, and 67 of the cases were cross-checked against $\tau(G+w)=\tau(G)+1$ with full agreement.
  - Together these test both directions of every stated equivalence.

### (d) Theorem 4 and Corollary 5

- **Logic.**
  - 4.1 uses L017 Theorems 1 and 4, which are refereed (ACCEPT x2, K64).
  - 4.2 voids (c1), (c2) and (d): $F_1+w$ has at most $n-3$ vertices, so (H$_{n-1}$) applies.
  - 4.4 handles (a), (b), (e) and (f) correctly.
  - In Corollary 5, every use of I11 is below $n$, so there is no circularity. The base case is L016. The consequence $h\ge(6n+4)/11$ follows from $m\le n-2$.
  - (A), (B) and (C) contradict C1-big, R-big and FC1 exactly.
  - C1-big and R-big are precise statements: the definitions of near-tight, big, admissible, covered, b-configuration and e-configuration are unambiguous. They are legitimate conjectures.
  - Remark 4.6 correctly states that C1-big at size $N$ is, given (H$_N$), equivalent to the absence of pattern-(a) violators with $N+1$ vertices. The reduction is honest about its strength.
- **Unrefereed inputs.**
  - (1) L017 Corollary 13.3, C4 and C5: the cell table and the role facts.
  - (2) FC1, which is a hypothesis, not a computation.
  - Nothing uses the unrefereed $n=28$ result or the unrefereed $(24,20,10,3)$ list; those appear only in illustrative runs and in W2/W3.
- **Re-check of what 4.3 needs.**
  - The cell table: `python3 cells_enum.py` enumerates the cells with slack 0 or 1 and at most 26 vertices from $3n+2m-11\tau\in\{0,1\}$, $\lceil(n-1)/2\rceil\le m\le n-2$, $\tau\le m$ and $m\le3\tau$ (for $\Delta\le3$). It gives the 15 tight and 14 slack-1 cells of L017 C4 exactly. The Henning–Yeo bound prunes none of them, so "Not used: K8" is correct.
  - The stored $D=3$ lists for the empty cells exist in experiments/prover/L017/out/ (for example cell_21_18_9_D3, cell_23_21_10_D3, cell_26_16_10_D3).
  - The role facts: `python3 roles_check.py <ten slack ≤ 1 lists>` → `roles_check_output.txt`. On 1+4+2+6+2+149+19+227+37+36 = 483 graphs:
    - b-configurations, with the three vertices allowed to form an edge, occur only in $E_1$;
    - e-configurations occur only in the two $(8,5,3)$ classes;
    - f-configurations occur in none.
    - Every graph has the listed $\tau$, is in $C$, is connected, and has every vertex in a minimum transversal. So the three role statements of Step 4.3 hold.
  - The lists themselves: the inputs-folder files used by the prover and by me are identical, as sets of edge sets, to the refereed stored lists extracted in experiments/prover/L017/out/. This was checked for $(20,15,8,3)$ [953], $(8,5,3,4)$ [2], $(22,17,9,4)$ [95], $(26,22,11,3)$ [36], $(19,16,8,4)$ [956], $(12,10,5,4)$ [221] and $(15,11,6,4)$ [30].

### (e) Proposition 6

- **Proof check.** 5.1 follows from (U) and 0.1. In 5.2, $s(K)-3+2\sigma\ge0$ forces $\sigma=1$, $s=1$ and $s(K-x-y)=0$. All components are tight with no isolated vertex, and each contains one of the at most 5 vertices of the three edges meeting $\{x,y\}$.
- **Numerics.** `roles_check.py` gives 204 NC pairs, of types $(1,1,0)$ 1, $(1,1,1)$ 3, $(1,2,0)$ 1, $(1,2,1)$ 104, $(2,2,1)$ 95, exactly as in C7. In every case $\tau(K-x-y)=\tau-1$ and $s(K-x-y)=s+5-2|\partial|\ge0$, and for $(2,2,1)$ the remainder is at most 5 tight components with $\Delta\le3$: 0 failures.

### (f) DEPENDS ON and tags

- **Tags.** They are appropriate:
  - Theorem 1 and Observation 7 are tagged as unrefereed computations;
  - Theorems 2, 3 and Proposition 6 are [derived-here];
  - Theorem 4 is [derived-here] with the unrefereed C5 flagged;
  - C1-big and R-big are [conjecture];
  - T'' is [refuted].
- **Citations.** L018 and L019 are cited, but independent proofs are included (Lemma 2.1, 4.2, 3.4); L019 Theorem 4(b) appears only in Remark 4.6. That is honest. Problem 2 below is a stale status entry.
- **Observation 7** (`obs7_perclass.py`): every class of $(15,11,6,3)$ [19], $(19,16,8,3)$ [227], $(22,17,9,3)$ [37], $(26,22,11,3)$ [36] and every one of the 45 classes has a $\Theta$-vertex. At such a vertex $K-v$ is the triangle plus a graph of the preceding cell, and the triangle carries $P_1$ and $c,e$. The NC-pair fractions agree with my counts (2/2, 13/19, 37/37, 0/45; 59/149, 18/227, 0/36). The triangle has 4 b- and 6 f-configurations, as in C9.

## Problems, in order of severity

1. **An inaccurate sentence in the statement of Theorem 1.** Editorial; not load-bearing, but it sits in a theorem statement.
   - The text says: "The same classes also arise by pattern (f) of Theorem 3 from graphs of the stored cell $(18,13,7,3)$ (slack 3) and $(10,7,4)$ graphs, and by pattern (b) from graphs of $(25,19,10,3)$ (slack 3) and $E_1$ (C8)."
   - Read as "the 45 classes", this is false:
     - only 27 of the 45 classes have a degree-3 vertex $v$ with $K-v=(10,7,4)\sqcup(18,13,7)$ of pattern (f), and the prover's own `bf_18_13_7.json` hits exactly these 27;
     - only 31 of the 45 have a pattern-(b) vertex with $K-v=E_1\sqcup(25,19,10)$, and the prover's 3,000-sample produced only 4 of them.
   - What holds for all 45 is a pattern-(e) vertex and three $\Theta$-vertices (pattern (f) with $(6,3,2)+(22,17,9)$).
   - The last sentence of C8, "So the 45 classes arise at different vertices by patterns (b), (e) and (f)", needs the same qualification.
   - Fix: replace both sentences with the counts above. It would also help to add the characterisation of item (a)5: given the refereed lists, the 45 are exactly the classes of cell$(29,23,12,3)$ with a pattern-(e) vertex.
2. **The DEPENDS ON status of L017 is stale.** The entry reads "[derived-here; referee round 1: no mathematical error; round 2 pending]". L017 Theorems 1–6 were accepted twice in round 2 (reviews 20261027T052541Z and 20261027T053019Z, LEDGER K64) before L020 was submitted at 06:13 UTC. The entry should say:
   - L017 Theorems 1 and 4 (and Facts 0.x, Theorem 2(U)) [verified-here, ACCEPT x2, K64];
   - L017 Theorem 7 [published, re-proved];
   - L017 Corollary 13.3, C4 and C5 [unrefereed computations].
   - L020 already flags the last group correctly in the tags.
3. **The b-configuration notion is used inconsistently.** The Definitions allow the three vertices to form an edge. The counts for the slack-2 cells in C3 and the C8 sentence "the slack-3 cell $(21,14,8,3)$ … has no b- or f-configuration" use the narrower notion with edge triples excluded; C3 says so, C8 does not.
   - With the certificate's own definition, my counts (`bcfg_slack2_output.txt`) of classes with a b-configuration (edges allowed / non-edge triples only) are:

     | cell | edges allowed | non-edge only |
     |---|---|---|
     | $(9,4,3)$ | 1/1 | 0 |
     | $(10,8,4)$ | 1/63 | 0 |
     | $(13,9,5)$ | 32/84 | 3 |
     | $(16,10,6)$ | 16/16 | 0 |
     | $(20,15,8)$ | 159/953 | 0 |

     The non-edge counts equal the prover's.
   - This is not load-bearing. The slack $\le1$ role facts used in Theorem 4 were checked with the full definition by `roles_b_any.py` and by me. Also, an edge-forming b-configuration glued to $E_1$ creates an $F_7$, so the narrower notion is harmless for the reverse gluings with $E_1$. The text should still state which notion each count uses.
4. **Minor: Open problem 2.** It says "the subcases with a vertex of degree 1 give slack-1 or slack-2 remainders". This omits NC pairs of type $(1,1,1)$: two degree-1 vertices in one edge are never co-transversal, and Proposition 6 then gives $s(K-x-y)=s(K)+3$. It is a heuristic remark, so just rephrase it.
5. **Minor: Step 3.8.** The parenthetical "($|N_{B'}(\{1,2,3\})|=r$ would exceed $1+2$)" is correct but cryptic. Suggested wording: for $r\ge4$ the only possible deficient set is $\{P_i,\{f\}\}$ inside one component, and the two vertices of the remaining pair cannot meet the at least 3 other components.
6. **Remarks requiring no change.**
   - Theorem 3 assumes (H$_{n(K)}$), which is unknown for $n(K)\ge28$. In this certificate it serves as the template for 4.1 and 4.4, where only graphs with fewer than $n(H)$ vertices are involved, and for Step 6. That is legitimate.
   - Corollary 5 is weak as a reduction, since C1-big is essentially I11 for pattern (a), but Remark 4.6 says so honestly.

No step is wrong. Once Problems 1–3 are fixed, which needs editing only and no new mathematics, I would expect to recommend ACCEPT.
