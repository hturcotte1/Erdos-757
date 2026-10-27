VERDICT: ACCEPT WITH FIXES

# Referee report, round 1: certificate L018 (results/proofs/L018-red-universality.md)

Referee: referee subagent (Claude Opus 5.5), round 1, 2026-10-27 (UTC). Scratch folder: experiments/referee/L018-round1/.
Scope: the verdict concerns only what the certificate claims as proved (Lemmas 0.1-0.7, Theorems 1-8, Corollaries 2.1, 5.2, 7.2, Propositions 6.2, 8.1, 8.2, and the arguments of Remark 7.3) and whether the open case is stated honestly. Conjecture RU and I11 are not claimed, and I do not judge them.
Verdict scale: the workflow asked for ACCEPT / REJECT / ACCEPT WITH FIXES. On the generic referee scale this would be NEEDS-WORK of the mildest kind. No claimed theorem is wrong. The fixes are a one-line missing case in Lemma 0.5, the labelling of Proposition 8.2, mislabelled (cumulative) census counts, and some wording. None of them affects a conclusion.

## Summary

I read the whole certificate, numbered and checked every step, and tested every computational claim with my own code, none of which imports e757, judge/ or the prover's modules.

- **Theorems 1, 2, 5, 6 and 7.** These are correct as written.
  - The polytope step of Theorem 2 is valid. There is also a short elementary proof of $\nu\ge2|E|/7$ for simple subcubic graphs via Tutte-Berge (given below).
  - The identities $\tau=m-\nu(G)$ and $\mathrm{slack}=3n_0+11\nu-3n_2$ hold on 3,253 test graphs.
- **Theorem 3.** The hand proof of (a) and (b) is correct. For (c) I wrote an independent enumerator. It reproduces the prover's search tree exactly: 40,912 nodes, 35,687 pruned and 10 leaves, namely the single edge, P-tree-3, and P-tri-3 with the four degree combinations. A falsification test on all census graphs with $5\le n\le14$ also passes: every pendant vertex is 3-reducible. Theorem 3(c) forces this for $n\le15$, because a P-tri-3 pendant needs $n\ge16$ and a P-tree-3 pendant needs $n\ge21$.
- **Theorem 4, the most delicate claim.** It is correct.
  - The construction is in $C$, has $\Delta=2$ and exactly one pendant vertex.
  - The forest lemma (4.4) gives $|Z|\ge g/2$ for every (Red) pair.
  - I checked the construction on six cubic graphs of girth 5 to 12, exhaustively over all $2^{17}$ sets $Z$ for the Petersen instance. P-tree-$r$ appears at $p$ and $p$ is not $r$-reducible, for every tested $r$ with $2r+4\le g$.
- **Theorem 8 and Step 7.2.4.** The transversal data of Step 8.3 matches my independent recomputation number for number. A brute-force gluing check of the 13 tight pieces finds failures only for $E_1+E_1$, the $F_7$ configuration with $n=7$.
- **Corollary 7.2.** It is correct as a conditional statement. My recomputed decomposition lists match 7.2.2 exactly, and every cell said to be empty is empty in the refereed L013 lists. It rests on the two unrefereed cell lists named in it, (27,15,10,3) and (27,20,11,3). Both exist, contain 0 classes and have complete INFO lines.
- **L017 and L018.** Both are right; details below. L018 Theorem 6(b') strictly strengthens L017 Theorem 4(iii). It uses no extra hypothesis, only one more application of minimality, to the proper induced subgraph $H[V(F_1)\cup\{v\}]$.
- **The open case.** GAP 1 and GAP 2 state it honestly.

## Checks performed (commands, outputs)

All runs used `nice -n 10`, one process, under `timeout`, in experiments/referee/L018-round1/.

1. **Theorem 3, independent enumerator.** `python3 pend_enum.py 1 R` for R = 1, 2, 3. This is my own code: BFS split configurations, an independent exact $\tau$, every leaf re-checked by brute force over all $Z$, and networkx rooted-isomorphism classes of the leaves.
   - R=1: `nodes 9 pruned 5 leaves 2`.
   - R=2: `nodes 101 pruned 71 leaves 4`. There are 3 classes: the single edge, P-tree-2, and P-tri-2 (multiplicity 2).
   - R=3: `nodes 40912 pruned 35687 leaves 10`, taking 14 min 21 s wall on the loaded machine. There are 5 rooted classes: the single edge; P-tree-3 (15 processed vertices, all of degree 2 except the root); and P-tri-3 with the degrees of the two vertices of $C$ equal to (2,2) (multiplicity 2), (2,3)≅(3,2) (multiplicity 4) and (3,3) (multiplicity 2).
   - Best value is $-1$ on every non-closed leaf.
   - These numbers equal C1 of the certificate exactly. Files: enum_root1_R{1,2,3}.txt.
2. **Theorem 3 on real graphs.** `pendant_check.py 11`, then `pendant_check2.py 12 12`, `13 13` and `14 14`. This is my own code. It tests r-reducibility directly in every census graph, applies my own structural tests for P-tree-2 and P-tri-2, and checks that every pendant is 3-reducible.
   - Result: **0 violations** over all census pendants with $5\le n\le14$. At $n=14$ there are 3,273,637 pendant vertices.
   - The per-n counts of radius-2-irreducible pendants are as follows. P-tri-2: 1, 6, 16, 71, 367, 2,333 at n = 9, ..., 14. P-tree-2: 2, 14, 76, 498 at n = 11, ..., 14. The "other" type is always 2-reducible.
   - Summed over $n\le N$ these give exactly the prover's numbers (23, 94, 461; 2, 16, 92; 350,999). So the prover's numbers are cumulative, not per-n (Problem 3).
3. **Theorem 4.** `thm4_check.py`. The input is a cubic graph $G_0$ of girth $g$ with one edge subdivided. The script builds $H$ as in 4.2 and checks the following:
   - linearity, $\Delta=2$ and exactly one pendant;
   - $e(S)\le|S|-2$ via the Hall form over all vertex pairs;
   - $\tau$, by CP-SAT, and $m-\nu$;
   - the maximum of value$_T(Z)$ over $|Z|<g/2$, by CP-SAT;
   - P-tree-$r$ at $p$ and the maximum value over $Z\subseteq B_r(p)$, for every $r$ with $2r+4\le g$.

   Results:
   - Petersen ($g=5$): $n=17$, $m=11$, $\tau=6=m-\nu$, slack 7. The maximum value over $|Z|\le2$ is $-1$ and the minimum $|Z|$ of a (Red) pair is 7. Exhaustively, of 131,070 sets $Z$, 1,326 have value $\ge0$, with **0 forest-lemma violations**.
   - Heawood ($g=6$): $n=23$, $\tau=8$, slack 11. The minimum $|Z|$ of a (Red) pair is 12. P-tree-1 holds with maximum value $-1$.
   - McGee ($g=7$): $n=38$, $\tau=13$, slack 21. The maximum over $|Z|\le3$ is $-1$. The min-$|Z|$ search did not finish within 20 min.
   - Tutte-Coxeter ($g=8$): $n=47$, $\tau=16$, slack 27. The maximum over $|Z|\le3$ is $-1$. P-tree-$r$ holds for $r=0,1,2$, with maximum values $-6,-1,-1$.
   - Foster ($g=10$): $n=137$, $\tau=46$, slack 87. P-tree-$r$ holds for $r\le3$, maximum value $-1$.
   - Tutte 12-cage ($g=12$): $n=191$, $\tau=64$, slack 123. P-tree-$r$ holds for $r\le4$, maximum value $-1$.
   - All instances are in $C$.
   - Files: thm4_small.txt, thm4_large.txt, thm4_large2.txt.
4. **Theorems 1 and 2, Lemma 2.2 and Theorem 7.** `thm2_thm7_check.py`.
   - (A) Theorem 2 on all subcubic graphs with $\le7$ vertices (networkx atlas) plus 3,000 random ones, 3,253 graphs in all. $\tau$ is computed by branch and bound, independently of matchings. Both identities hold. The minimum of $7\,$slack$-21n_0-n_2$ is 0. `eqcheck.py` tested a further 20,253 subcubic graphs: in all 157 cases of $7\nu=2|E|$, every component with an edge is $K_4$ with a subdivided edge, as the Tutte-Berge argument below predicts.
   - (D) Lemma 2.2 on all 135,586 pairs $(H,Z)$ coming from duals of subcubic graphs with $\le6$ vertices: all hold.
   - (B) Theorem 1, the closure form, agrees with a brute-force (Red) test on all 80 census graphs with $5\le n\le9$ and on 300 random linear $\Delta\le3$ 3-graphs.
   - (C) Theorem 7 holds on 8,823 instances $(H,S)$ from census graphs with $n\le11$, where $S$ is the set of degree-3 vertices or a random admissible $S$. The special case holds on 195 graphs.
   - Files: thm2_thm7_output.txt, thm2_D.txt, thm2_B.txt, thm2_C.txt.
5. **Step 8.3, Theorem 8 and Step 7.2.4.** `tight_glue_ref.py` (my own code). It loads the 13 pieces from the refereed L013 lists and re-checks for each: membership in $C$ (5-edge subsets for $F_7$; all edge subsets for $|V(F)|\ge|F|+2$), connectivity, $\Delta\le3$, $\tau$ by brute force, slack 0, and pairwise non-isomorphism. It then enumerates all minimum transversals.
   - Counts of minimum transversals: 31, 32, 33, 30; 139, 139; 366, 361, 372, 361, 350, 354.
   - $\Phi=\{(0,1),(0,2)\}$ for the two pendant (10,7,4) classes and $\emptyset$ for the others.
   - Pair-pair failures: 0 among 132, 89, 89, 132, 25, 25, 925, 891, 960, 960, 960, 925 instances.
   - All of this equals Step 8.3. U1 (every vertex lies in a minimum transversal) holds on all pieces.
   - The brute-force gluing check covers every gluing of a new degree-3 vertex to one or two pieces (ordered pairs of pieces, all inside/split types, all bijections of the split pairs). $r=1$: 42,673 configurations, 0 failures. $r=2$: 6 failures, all $E_1+E_1$ with three split pairs ($n=7$, i.e. $F_7$); 0 with $n\ge8$.
   - $r=3$ reduces to the pair-pair property plus U1 (6.5/8.5), both verified.
6. **Corollary 7.2 and Remark 7.3.** `decomp_check.py` (my own code).
   - At $n=28$ the violator cells are (28,16,11) with slack $-5$, (28,17,11) $-3$, (28,18,11) $-1$, (28,22,12) $-4$ and (28,23,12) $-2$.
   - The decompositions with at most 2 parts are exactly those listed in 7.2.2.
   - Counts in L013's cells.tar.gz: 0 FOUND for (24,14,9), (19,10,7), (17,8,6), (11,6,4), (16,9,6), (13,8,5), (14,7,5) and (24,19,10), all with D3. The INFO lines show completed direct or recurse runs.
   - At $n=29$ the lists equal Remark 7.3.
   - The two unrefereed cells:
     - experiments/20261027-0340-induction-n28-n29-f25/out/cells/cell_27_15_10_D3.txt: 0 FOUND, complete INFO, progress.tsv `(27,15,10,3) 0 102 12137486 ... 2026-10-27T03:32:33Z`. That run's README says "IN PROGRESS".
     - experiments/20261027-0300-tight-cells-d4/out/cells/cell_27_20_11_D3.txt: 0 FOUND, also present with 0 in the 0340 run.
7. **Prover's scripts re-run on a copy.** experiments/referee/L018-round1/prover_copy/, outputs written there.
   - `tight_glue.py`, `tightdeg.py` and `localconf.py 1 2` give outputs **byte-identical** to the stored ones.
   - `prune28.py 28 29` differs only in one line: (28,19,11,3) is now found, with 0 classes, in the unrefereed 0340 run, which finished it at 04:41Z, after the certificate was written.
   - I did not run the full reproduce.sh. It overwrites files in the prover's folder, and on this machine (load 9-14) it would clearly exceed 20 minutes: localconf R=3 alone took 14 min with my code, and pendant_census n=14 needs 2.45M graphs.
8. **Proposition 8.2.** `prop82_check.py`. From the census list redk5_free_graphs.txt.gz I selected the graphs with $9\le n\le14$ and slack $\le5$: there are 17.
   - For each one, brute force confirms that there is no (Red) pair with $|Z|\le5$. It also gives all minimum-size (Red) sets, the structure of $H-Z$, and $g=0$.
   - Summary: `[((11,7,3,7),1), ((12,10,1,6),7), ((12,10,1,9),1), ((13,9,2,7),1), ((13,10,4,6),1), ((13,10,4,7),4), ((13,10,4,9),2)]`. This is identical to C5. The structures of $H-Z$ are as stated (two disjoint edges; one edge; two edges plus an isolated vertex; an edge plus an isolated vertex; a triangle), and every reduction is exact.

## Theorem-by-theorem audit

**0.1-0.7.**
- Lemma 0.1 (additivity) is correct.
- Lemma 0.2: the identity slack$(H)=$slack$(H-Z)+$value$_T(Z)+11g$ holds with $g\ge0$. I re-derived it.
- Lemma 0.3 (a)-(d) is correct; (b) uses the facts that $m\ge2$ (a single vertex has slack 3 and a single edge has slack 0) and that a connected linear 3-graph with $m\ge2$ has $n\ge5$.
- U1 and U2 are correct. Both bounds $\tau(F)-1\le\tau(F-x)\le\tau(F)$ and $\tau(F-\{x,x'\})\ge\tau(F)-2$ hold, and the slack arithmetic checks.
- **Lemma 0.5 (TP)** has a gap; see Problem 1. Cases $d(p)=3$ and $d(p)=1$ are right, but the statement has no degree bound and the case $d(p)\ge4$ is not treated.
- Lemma 0.7 is correct. The two remaining edges partition the six co-vertices, one from each pair by linearity, and the map to $012,034,056,135,246$ checks.

**Theorem 1.** Correct in both directions. Here $\mathrm{cl}(T)=\{v:$ every edge at $v$ meets $T\}$.
- 1.1: $T\subseteq\mathrm{cl}(T)$ and $E_{\mathrm{cl}(T)}=E_T$.
- (i)⇒(Red): take $Z=\mathrm{cl}(T)$.
- (ii)⇒(Red): $T$ is then a transversal; take $Z=V\setminus\{u\}$, which gives value $w-3\ge0$.
- (Red)⇒(i) or (ii): $Z\subseteq\mathrm{cl}(T)$ and $E_Z\subseteq E_T$, so $w(T)\ge$ value$_T(Z)$, plus 3 when $\mathrm{cl}(T)=V$, because then $|Z|\le n-1$.
- (ii)⇔ slack $\ge3$: via a minimum transversal, which is nonempty because no vertex is isolated and $n\ge2$.
- Numerical check: item 4(B).

**Theorem 2 (Lemma M).** Correct.
- 2.1: the dual $G$ is simple ($\Delta(H)\le2$, linear) with $\Delta(G)\le3$, $|V(G)|=m$ and $|E(G)|=n_2$.
- 2.2: $\tau=m-\nu(G)$. For (≥): $m\le|V(F)|+|T|-|F|$ and $|V(F)|-|F|\le\#$components of $(V(F),F)\le\nu$. Correct.
- 2.3: slack $=3n_0+11\nu-3n_2$. Correct, and it shows the roles of the variables: each isolated vertex contributes only to $3n$, and the degree-2 vertices are exactly the dual edges.
- 2.4: $x\equiv2/7$ satisfies the degree constraints ($6/7\le1$). For the odd-set constraints: $|S|=3$ gives at most 3 edges and $6/7\le1$; for $|S|=2k+1\ge5$, $|E(G[S])|\le3k+1$ and $\frac27(3k+1)\le k$. By Edmonds' theorem some matching has size $\ge2|E|/7$. Correct; this is the statement $\chi'_f\le7/2$ for simple subcubic graphs.
- 2.5 and 2.6 are correct. The equality case is the first class of cell_8_5_3_D3, degrees $1^12^7$, whose dual I checked is $K_4$ with edge $BC$ subdivided.
- An elementary alternative, as the task asked. By Tutte-Berge, $2\nu=\min_U(|V|+|U|-\mathrm{odd}(G-U))$. For every $U$,
  $7(|V|+|U|-\mathrm{odd})=14|U|+\sum_C7(|C|-[|C|\text{ odd}])\ge12|U|+\sum_C4e(C)\ge4|E|$,
  because $|E|\le3|U|+\sum_Ce(C)$ and $7(c-[c\text{ odd}])\ge4\,e_{\max}(c)$ for $e_{\max}(c)=\min(\binom c2,\lfloor3c/2\rfloor)$. Checking $c=1,\dots,5$ gives $0\ge0$, $14\ge4$, $14\ge12$, $28\ge24$ and $28\ge28$; even $c$ needs $7c\ge6c$, and odd $c\ge5$ needs $7c-7\ge6c-2$. Hence $\nu\ge2|E|/7$, with equality at $c=5$.
- Comparison with L017 Theorem 7. L017's Tutte-Berge bound $11\nu\ge3|E|$ is weaker ($3/11<2/7$). It suffices for I11 at $\Delta\le2$, since slack $=3n_0+(11\nu-3n_2)$. It does not give the bound slack $\ge n_2/7$ that 4.6 uses. The two statements are consistent: both give slack 0 iff $H$ is a matching, and slack $\ge1$ for connected $H$ with $m\ge2$.
- Corollary 2.1 and Lemma 2.2 are correct; for Lemma 2.2, (2)-(4) re-derived, and see item 4(D).

**Theorem 3.**
- The hand proof of (a) and (b), 3.0.1-3.0.4, is correct step by step. I recomputed every value: 1, $\ge0$, 2, 0, 1, 1 or 3, 0 and 1. Every $Z$ lies in $B_2(y)$ and misses a vertex of $H$. The membership statements of (iii)/(iv), such as $A_1\cap B_2(y)=\{a_1\}$, follow from linearity and $A'\neq B'$.
- For (c), the soundness argument 3.1-3.4 is correct. Monotonicity holds because re-identifying split copies maps transversals to transversals and leaves $E_Z$ unchanged. Exhaustiveness holds because vertex ids are sorted by BFS distance, the edges at a processed vertex are final, and no boundary vertex is reused at $d_q=R$.
- I read the prover's localconf.py and found it implements exactly this rule. My pend_enum.py implements the same rule with no shared code and gives the identical tree (item 1).
- The leaf list, read against the wording of (c), matches: the six vertices of $(C\cup A'\cup B')\setminus\{c,a',b'\}$ are distinct, and all further edges are fresh, so they are distinct and meet $B_3$ once.
- (d): "P-tree-$r$ not $r$-reducible for all $r$" follows from Theorem 4. The census counts quoted are cumulative (Problem 3).

**Theorem 4.** Correct. This is the most delicate claim, so I re-derived each step.
- 4.1-4.2: subdividing preserves girth $\ge g$ and simplicity. $H$ is 3-uniform, connected, linear ($|\delta(w)\cap\delta(w')|=[ww'\in E(G)]$) and has exactly one pendant.
- 4.3: $F_7$ needs three pairwise intersecting edges with distinct intersections, which is a triangle in $G$. The bound $e_{\rm ind}(S)\le|S|-2$ reduces to $|E(G[W])|\le2|W|-2$, which holds for $|W|\le3$ (forest) and for $|W|\ge4$ ($3|W|/2$). Correct. Hall checked numerically on all six instances.
- 4.4: Lemma 2.2 applies ($\Delta(H)\le2$, no isolated vertices). For a forest, $|E_G(W)|\ge(3|W|-1)-(|W|-1)=2|W|$ and $\nu(G[W])\le|W|/2$, so value $\le-|W|/2<0$. So a (Red) pair needs a cycle in $G[W]$, hence $|W|\ge g$, and $|Z|\ge|W|/2\ge g/2\ge R+1$. Correct.
- 4.5: the distance formula (H-distance of $f$ = 1 + G-distance of its nearer endpoint) is correct by induction. $K_r$ is the set of the $\delta(w)$, $w\in V_r$. $G[V_r]$ is a tree when $2r+1<g$; the justification as written is imprecise (Problem 4), but the conclusion is right. That gives the binary hypertree. Note that $2r+2\le g$ would already suffice; the stated $2r+4\le g$ is merely stronger.
- 4.6: $n_2=|E(G)|\ge g\ge22$, so slack $\ge22/7$, hence $\ge4$, and Theorem 1 gives a (Red) pair.
- Numerical check: item 3.
- Remark 4.1 is correct for $r\le3$. For general $r$ the distance condition must be $>r+1$ (Problem 5).

**Theorem 5.** Correct; all eleven steps re-derived.
- 5.1-5.3 are as in 3.0.
- 5.4: $\tau(H-y)=\tau-1$, else slack$(H-y)=s-5$.
- 5.5: $\tau(K_a)=\tau(H)-1$, slack$(K_a)=s+1$, and so $s=-1$.
- 5.6 is correct.
- 5.7: $K_a$ is connected. Every component contains $b$, $a_1$ or $a_2$, and U1 in two different components would contradict (iv).
- 5.8: by U2 in $K_a$ with $|E_{b,a_1}|=3>(0+5)/2$, a degree-3 vertex among $a_1,a_2$ lies in $B$.
- 5.9: if $d(c)=2$ then $Z=\{y,a,b,c,a'\}$, $T=\{b,a'\}$ gives value 1, a contradiction.
- 5.10: $n\ge7$ and $|V(K_a)|\ge5$.
- 5.11: Lemma 0.5 is applied to $K_a$, which has $\Delta\le3$, so Lemma 0.5's gap is not triggered. Also $u,w\notin e_0\cup A$.
- Corollary 5.2 is immediate. Remark 5.4's tight-cell list for $n\le27$ is complete: I solved $11\tau=3n+2m$ with $\lceil(n-1)/2\rceil\le m\le n-2$ myself; HY is automatic for tight cells since it amounts to $m\le4n$.

**Theorem 6.** Correct.
- (a) as in 6.1.
- (b), steps 6.2-6.5. The Hall step: with $\ge4$ components a deficient set of size 2 would force $\ge3$ components onto one pair. Correct.
- (b') the gadget lemma, 6.5'. Suppose $r\ge2$ and $P_1\cup P_2\subseteq V(F_1)$. Then $H_1=H[V(F_1)\cup\{v\}]$ has edges $E(F_1)\cup\{e_1,e_2\}$ and fewer vertices than $H$. If no minimum transversal of $F_1$ met both pairs, then $\tau(H_1)=\tau(F_1)+1$ and slack$(H_1)=$slack$(F_1)-4\le-3$, contradicting minimality. Otherwise $T_1$ together with U1 in a component meeting $P_3$ meets all three pairs, contradicting 6.4. The consequences $r\le2$ and "each component contains at most one pair" follow via Hall. Correct.
- (c), 6.6, is correct, including the U2 step with $|E_{z,z'}|=4$ and slack 2.
- **Proposition 6.2** (conditional on P2): 6.7-6.9 are correct. The only $P2$-dependent input is "at most one pendant" in 6.8. The $E_1+E_1$ case is $F_7$ by Lemma 0.7.

**Theorem 7.** Correct; Lemma 0.2 with $Z=T=S$ is combined with Theorem 2 on $H-S$. In the special case $|E_S|=3n_3$ and $n_2(H-S)\ge n_2-6n_3$. Numerical check: item 4(C).

**Theorem 8** (conditional on T'). Correct.
- 8.2 relies on the completeness of the refereed L013 lists of cells with $n\le17$, plus U1.
- 8.4: under T', $n-1\ge27>17$.
- 8.5 is also covered by (b').
- 8.6 (i)-(iv): I re-derived each failure condition. For example, in (iii) failure needs $\{x_2',x_3'\}\in\Phi(F_2)$ and both $x_2$ and $x_3$ $\Phi$-adjacent to both vertices of $P_1$. With the data of 8.3 these conditions are excluded.
- Both the data and the conclusion were recomputed independently (item 5).

**Corollary 7.2.** Correct as a conditional statement; checked in item 6.
- 7.2.1: the cells were re-enumerated.
- 7.2.2: the decompositions were re-enumerated, using (b') for at most 2 parts and 6.2 for no isolated vertex.
- 7.2.3: the empty refereed cells were re-counted.
- 7.2.4: steps 8.5-8.6 need only that the pieces are among the 13 classes. For (10,7,4)+(17,13,7) the brute-force gluing check of item 5 finds no failure.
- **What it rests on:**
  - cell(27,15,10,3) is computed, by an unrefereed run that is still marked "IN PROGRESS", and has 0 classes;
  - cell(27,20,11,3) is computed by two unrefereed runs and has 0 classes;
  - L016 (refereed), the L013 lists (refereed) and HY (K8, [published]).
  - No uncomputed cell is used. The certificate states the dependence on the two unrefereed lists correctly.

**Remark 7.3** ($n=29$; not claimed as a theorem). Its bookkeeping matches my decomp_check. The argument voiding $(3,1,1)+(25,23,11)$ is correct:
- degree count $2n_1+n_2=6$;
- Lemma 0.5 excludes $n_1=3$ and the case $n_1=2,n_2=2$ by linearity;
- so 6.8 applies, and 6.9 for the types $\{1,s,s\}$ and $\{s,s,s\}$.

**Propositions 8.1 and 8.2.** 8.1 is immediate from Lemma 0.2. For 8.2, the properties of the 17 graphs were re-checked (item 8), but the "exactly 17" depends on the unrefereed census (Problem 2).

**Section 9 (GAPs).** Honest and accurate.
- The equivalence quoted in (M2) is correct: for a degree-3 vertex, slack$(H)=$slack$(H-v)+9$ or $-2$, according as some minimum transversal of $H-v$ meets the three pairs or not.
- RU and I11 are explicitly not claimed.
- The $n\ge29$ statement is correctly conditioned on the unrefereed lists.

## L017 / L018 reconciliation (L017 Theorem 4 versus L018 Theorem 6(b,b'))

**Both are right; L018 is strictly stronger and uses no extra hypothesis.**
- **What L017 Theorem 4(iii) says.** The bipartite graph between the three co-vertex pairs and the components of $G=H-v$ has no matching that saturates the pairs. Hence $r\le3$. The *Hall-deficient* distributions are exactly the seven patterns (a), (b), (c1), (c2), (e), (f), (d). As a statement about Hall deficiency this is correct; I re-derived that for $r=3$ deficiency occurs iff two pairs lie inside one component and the third pair is split between the other two. L017 does not claim that the seven patterns occur. Its own computation C5 even finds role_c = 0 on all 483 known low-slack classes.
- **What L018 adds.** L018 Theorem 6(b) reproves $r\le3$. Then (b') applies the minimal-counterexample hypothesis once more, to the proper induced subgraph $H_1=H[V(F_1)\cup\{v\}]$. This rules out exactly the condition that L017 Theorem 4(iv) attaches to (c1), (c2) and (d), namely "no minimum transversal of $F_1$ meets both $P_1$ and $P_2$": if that held, slack$(H_1)=$slack$(F_1)-4<0$.
- **Consequences.** Patterns (c1), (c2) and (d) are void, so $r\le2$, and with two components each contains at most one pair entirely. The patterns that remain are L017's (a), (b), (e) and (f); these are L018's $r=1$, $\{s,s,s\}$, $\{1,2,s\}$ and $\{1,s,s\}$.
- **No extra hypothesis.** The extra step uses I11 only for a proper induced subgraph, which is also available for L017's "vertex-critical violators". So L018's statement also holds in L017's more general setting. Both are consistent with the small vertex-critical violators of L017 C3: $F_7$ has pattern (b), and the (9,8,4) graphs have patterns (a) and (b).
- **Recommendation.** L017 Theorem 4(iii) and Theorem 6(ii) could be sharpened to $r\le2$ and four patterns by citing L018 6.5'.

## Problems, in order of severity

None of these invalidates a claimed theorem. All of them can be fixed by editing the text.

1. **Lemma 0.5 (TP): missing case.** The statement has no degree bound, but the proof treats only $d_K(p)=3$ and $d_K(p)=1$, so $d_K(p)\ge4$ is not covered. Fix: let step (1) read "if $d_K(p)\ge3$", since the value $6+2d_K(p)-11\ge1$, or add $\Delta(K)\le3$ to the hypotheses. Every use (5.11, 6.8, Remark 7.3) has $\Delta\le3$, so no theorem is affected.
2. **Proposition 8.2 is mislabelled.** The STATUS line counts it among the results "proved below with every step written out". It is an exhaustive statement over the census of experiments/20261027-0230-red-config, which the certificate itself calls unrefereed, and DEPENDS ON says no theorem depends on that census. "Exactly 17 ... (none at n = 14)" holds only if the census and its Red$_5$ filter are complete. Fix: tag it [verified-here as an unrefereed computation, conditional on the census]. The properties of the 17 listed graphs are confirmed (item 8).
3. **Cumulative counts reported as per-n.** This affects 3.6, Theorem 3(d) and C2: "P-tree-2 92 times and P-tri-2 461 times at n=13", "(92 at n=13, 16 at n=12, 2 at n=11) ... (461, 94, 23)", "350,999 at n=13". validate_catalog.py never resets its Counter, so these are totals over $5\le n\le N$. The per-n numbers are in item 2. No theorem is affected.
4. **Step 4.5, a justification that does not hold in general.** "A cycle of $G$ all of whose vertices lie in $V_r$ has length $\le2r+1$" is not true as a general statement. The correct one-liner: an edge of $G[V_r]$ outside the BFS tree closes, with the two tree paths to $g_0$, a cycle of length $\le2r+1<g$. So $G[V_r]$ is the BFS tree. The conclusion is right and is verified numerically.
5. **Remarks and wording.**
   - Remark 4.1: "distance $>4$ from $p$" keeps $K^{\rm sp}_r(p)$ unchanged only for $r\le3$. In general it must be $>r+1$.
   - Remark 8.3: "(... no (Red) pair of $H$ has $|Z|\le R$)" does not by itself exclude a (Red) pair inside a ball $B_r(x)$, because balls have more than $R$ vertices. The forest argument of 4.4, with girth large compared with $r$, does exclude it.
   - GAP 1's parenthesis "(with $\Delta=2$, and configurations inside graphs with $\Delta=3$, Remark 4.1) whose (Red) pairs all have $|Z|>R$" reads as if $H'$ had no small (Red) pair. It has one, $(\{q,x_1\},\{x_1\})$, as Remark 4.1 itself says.
   - The "Insight (dense core)" paragraph opens with "In every census graph, the (Red) pairs are of two kinds ...". That is more than Proposition 8.2 shows, since 8.2 is about 17 graphs and their minimum-size (Red) sets. It is tagged heuristic, but it should be phrased as such.
6. **Dependencies (not a defect, recorded for the ledger).**
   - Corollary 7.2 depends on the unrefereed lists cell(27,15,10,3) and cell(27,20,11,3). The first is only in experiments/20261027-0340-induction-n28-n29-f25, which is marked IN PROGRESS.
   - Theorem 8 and Step 7.2.4 depend on the computer data of Step 8.3. That data is now independently reproduced.
   - The certificate states all of this. A future version could add that cell(28,19,11,3) is now also computed empty (unrefereed, 0340 run, 04:41Z). That narrows Remark 7.3's open input at $n=29$ to cell(28,24,12,3).

## Independence statement

- All verification code is my own, in experiments/referee/L018-round1/: pend_enum.py, pendant_check.py, pendant_check2.py, thm4_check.py, thm2_thm7_check.py, eqcheck.py, tight_glue_ref.py, decomp_check.py and prop82_check.py. None of it imports e757/, judge/ or the prover's hg.py or localconf.py.
- I read the prover's localconf.py, validate_catalog.py and hg.py only to audit them. My enumerator implements the same branching rule, because it is the rule justified in Step 3.4, but shares no code with theirs and uses its own $\tau$ routine and an exhaustive re-check of every leaf. The identical node counts therefore confirm the implementation. The soundness of the rule I checked by hand, and the census falsification test (item 2) is independent of the enumeration.
- The prover's scripts were re-run only on a copy (item 7).
- I did not read the other referee review of L018 in results/reviews (…__referee__20261027T051820Z.md), nor the L017 referee or scout reviews. For L017 I read only its Statement section and the parts of its proof and computer-verified-steps text needed for the reconciliation.
- I modified no file outside my scratch folder and this review.
