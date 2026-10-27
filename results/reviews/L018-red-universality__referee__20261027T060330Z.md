VERDICT: ACCEPT WITH FIXES

# Referee report, round 2 (referee #3): certificate L018 (results/proofs/L018-red-universality.md), revision e187bd7

Referee: referee subagent (Claude Opus 5.5), round 2, 2026-10-27, 05:46-06:03 UTC. Scratch folder: experiments/referee/L018-round2-opus/.

Scope, as in round 1: the verdict covers only what the certificate presents as proved, plus the honesty of STATUS, DEPENDS ON and the GAPs. That means Lemmas 0.1-0.7; Theorems 1-8; Corollaries 2.1, 5.2 and 7.2; Propositions 6.2 and 8.1; and the argument in Remark 7.3. Conjecture RU and I11 are not claimed, and I do not judge them.

## Summary

Every fix requested in round 1 is in revision e187bd7, and I re-checked each one by hand.
- Round-1 opus review (…__20261027T054329Z.md): Lemma 0.5's case $d\ge4$, the Prop. 8.2 tag, the cumulative counts, Step 4.5, Remark 4.1, Remark 8.3, GAP 1, the Insight paragraph, and the cell(28,19,11,3) note.
- Round-1 fable review (…__20261027T051820Z.md): the Prop. 8.2 tag, the three isomorphism types of P-tri-3, and the Theorem 1 isolated-vertex remark.

The diff is editorial, as claimed:
- 12 line ranges (14 lines) were replaced. The working tree is identical to e187bd7.
- No theorem statement changed.
- Only two proof passages changed. Lemma 0.5 gained the missing case $d_K(p)\ge4$, and its case analysis is now complete. In Step 4.5 the faulty justification was replaced by a correct BFS-tree argument.

I adversarially re-checked two unedited results, Theorem 6(b') (the gadget lemma) and Theorem 4 (non-locality: construction, forest lemma, local configuration). Both hold, by hand and on data, with my own code.

Two of the edits introduced small textual inaccuracies, both outside the proved parts:
- N1: the new note after Corollary 7.2 names cell(25,23,11,3) as an open input. Remark 7.3 voids that decomposition by hand.
- N2: the rescoped Insight paragraph attributes local (Red) pairs to the 17 graphs of Prop. 8.2. Those graphs have none, by definition.

There is also one older inconsistency in DEPENDS ON (N3): the census/0300 bullet says "used ONLY for validation … no theorem depends on them", but Corollary 7.2's hypothesis cell(27,20,11,3) is taken from that run.

None of these affects a proved statement. All three are one-line fixes, hence ACCEPT WITH FIXES.

## Fix-by-fix check (requested fix, where, verdict)

Line numbers refer to the revised file.

1. **Lemma 0.5, missing case $d\ge4$ (opus P1).** Line 43. Step (1) now covers $d_K(p)\ge3$, with value$_T(Z)=6+2d_K(p)-11\ge1$ (equal to 1 at $d=3$), and step (3) notes that $d\ge4$ falls under (1). APPLIED, CORRECT.
   - The case split is now exhaustive: $d_K(p)\ge1$ because $p$ lies in the edge; $d=1$ is step (2); $d=2$ is the conclusion; $d\ge3$ is step (1).
   - In step (1), $Z=\{x,p\}\ne V(K)$, because $p$ has a second edge whose two other vertices lie outside $\{x,q\}$ (linearity).
   - Step (2) also covers $d_K(q)\ge4$: the value is $9+2d-11\ge2$.
   - $q$ follows by symmetry. The statement is unchanged.
2. **Proposition 8.2 labelled as proved (opus P2, fable P1).** Line 228 now carries the tag "[verified-here as an unrefereed computation, conditional on the census … and its Red$_5$ filter …]". The STATUS line (line 4) no longer lists 8.2 among the proved results and says it is an unrefereed computation. APPLIED, CORRECT.
3. **Cumulative counts reported as per-n (opus P3).** APPLIED, CORRECT. The fix is in Theorem 3(d) (line 92), Step 3.6 (line 110) and C2 (line 258).
   - I read experiments/prover/L018/validate_catalog.py: `cnt = collections.Counter()` is created once before `for n in range(5, NMAX+1)` and never reset, so its printed counts are cumulative.
   - Differencing validate_catalog_output.txt gives P-tri-2 irreducible = 1, 6, 16, 71, 367 at n = 9..13 and P-tree-2 irreducible = 2, 14, 76 at n = 11..13. These are exactly the per-n numbers now quoted.
   - The cumulative totals are also quoted correctly: 92/16/2, 461/94/23, "other" 350,999 at N=13, and "45 cumulatively up to n=13".
   - Remark 3.7's counts 1, 2, 4, 20, 114 (sum 141) are genuinely per-n: pendant_census.py filters by `k[0] == n`, as its output file shows. They needed no fix.
4. **Step 4.5, BFS-tree justification (opus P4).** Line 123. APPLIED, CORRECT; see "Re-verified passages".
5. **Remark 4.1, distance $>r+1$ (opus P5).** Line 126: "$>r+1$ … (the value 4 suffices for $r\le3$)". APPLIED, CORRECT. In fact distance $>r$ from $p$ already leaves $K_r^{\rm sp}(p)$ unchanged; $>r+1$ is sufficient, and that is all the remark needs.
6. **Remark 8.3 (opus P5).** Line 231 now says that a (Red) pair inside a ball $B_r(x)$ is excluded by the forest argument of 4.4 (girth large compared with $r$), not by $|Z|\le R$. APPLIED, CORRECT.
7. **GAP 1 (opus P5).** Line 237 now states that $\Delta=2$ members have only (Red) pairs with $|Z|>R$. For $\Delta=3$ it says the pendant configuration embeds unchanged although the graph has the small pair $(\{q,x_1\},\{x_1\})$; I verified that pair: value $6+6-11=1$. APPLIED, CORRECT.
8. **Insight paragraph phrased as heuristic (opus P5).** Line 233. APPLIED, but over-corrected; see N2.
9. **Dependency note on cell(28,19,11,3) (opus item 6).** Line 220. APPLIED; the fact is correct, but the added parenthetical is not (N1).
   - progress.tsv has `(28,19,11,3) 0 14348 … recurse 2026-10-27T04:41:27Z`.
   - The cell file has 0 FOUND lines and a complete INFO record: one branch with d=3, all 14,348 inputs searched, connected_hits 0.
10. **Three isomorphism types of P-tri-3 (fable P2).** Line 91. APPLIED, CORRECT. My own classifier (leaf_iso.py, networkx rooted isomorphism of the incidence graphs) applied to the prover's 10 radius-3 leaves gives 5 rooted classes:
    - the single edge;
    - P-tree-3 (15 processed vertices);
    - P-tri-3 with C-degrees (2,2), multiplicity 2;
    - P-tri-3 with C-degrees (2,3)≅(3,2), multiplicity 4;
    - P-tri-3 with C-degrees (3,3), multiplicity 2.

    That is three P-tri-3 types with 2+4+2 leaves. My own exact $\tau$ gives best value $-1$ on every non-closed leaf and $-3$ on the single edge, matching the prover.
11. **Theorem 1, isolated-vertex remark (fable P3).** Line 52. APPLIED. The hypothesis really is needed: the edgeless graph on 2 vertices has the (Red) pair $(\{v\},\emptyset)$ and slack 6, but no nonempty $T$ satisfies (i) or (ii). The remark's explanation is slightly loose (N5, cosmetic).
12. **STATUS revision line.** "editorial fixes only, no mathematical change" is accurate except that one proof (Lemma 0.5) was completed (N4, cosmetic).

## Re-verified passages (by hand)

- **Lemma 0.5.** All degree cases are covered (fix 1).
- **Step 4.5.** Let $xy$ be an edge of $G[V_r]$ that is not in a BFS tree from $g_0$, and let $z$ be the last common vertex of the tree paths from $x$ and $y$ to $g_0$.
  - Adjacent vertices have BFS levels differing by at most 1. If one of $x,y$ were an ancestor of the other, it would be the other's parent, and $xy$ would be a tree edge. So $z\ne x,y$.
  - The two tree paths from $z$ to $x$ and $y$, together with $xy$, form a genuine cycle of length $(d(x)-d(z))+(d(y)-d(z))+1\le2r+1<g$ (as $g\ge2r+4$). Contradiction.
  - Hence $G[V_r]$ is the BFS tree. Each $w\ne g_0$ has exactly one closer neighbour, and no edge joins two level-$r$ vertices.
  - Consequently no boundary vertex lies in two edges of $K_r$, so $K_r^{\rm sp}(p)=K_r$. It is the complete binary hypertree: the root edge is $\delta(g_0)\cup\{p\}$, each $\delta(w)$ with $w\in V_{r-1}\setminus\{g_0\}$ has one edge up and two down, and the boundary vertices are pairwise distinct. For $r=3$: $1+2+4+8=15$ processed vertices, as in C1.
  - For $Z\subseteq B_r(p)$, $W=E_Z\subseteq V_r$ induces a subforest, so value$(Z)<0$ by 4.4.
- **Remark 4.1.** If $d(p,x_i)>r$, a path from $p$ can reach the new edge only through $x_1$ or $x_2$, at length at least $r+1$. So $B_r$, $K_r$ and the boundary are unchanged.
  - The new edge does not meet $B_r(p)$.
  - Membership of $H'$ in $C$:
    - linearity needs $x_1,x_2$ non-adjacent, i.e. distance $\ge2$, which holds;
    - for $e(S)\le|S|-2$: if $q\in S$ and $|S\setminus q|\ge2$, then $e_{H'}(S)\le e_H(S\setminus q)+1\le|S|-2$; if $|S|\le2$ the bound is trivial;
    - $F_7$-freeness: every vertex of $F_7$ has $F_7$-degree at least 2, and $q$ has degree 1.
- **Remark 8.3.** For a degree-2 vertex $x=ww'$ of $H$, the edges meeting $B_r(x)$ are $\delta(u)$ for $u$ within G-distance $r$ of $\{w,w'\}$. With girth large compared with $r$ (about $g\ge2r+3$) these $u$ induce a forest, and 4.4 gives value $<0$ for every $Z\subseteq B_r(x)$. The added sentence is correct.
- **GAP 1.** Correct (fix 7).
- **Theorem 3(c).** The parenthetical is correct (fix 10). The structural description matches leaf 2: $c=3$, $C=(3,6,7)$, $A'=(4,8,9)$, $B'=(5,10,11)$, with fresh further edges.
- **Theorem 1 remark.** Correct in substance (fix 11). The theorem is used only in Theorem 4 (statement and 4.6), on a connected graph with edges.
- **Prop. 8.2 tag and STATUS list.** Correct (fix 2). The STATUS line now separates three things:
  - the hand-proved results: Thms 1, 2, 4, 5, 6, 7, Props 6.2 (under P2) and 8.1;
  - Thm 3: hand proof plus computer for (a) and (b), computer for (c);
  - the computer-assisted or conditional results: Thm 8 (under T'), Cor. 7.2 (two unrefereed lists) and Prop. 8.2 (unrefereed census).

  It also states clearly that RU and I11 are not proved.

## Adversarial spot checks of unedited results

### Theorem 6(b') (gadget lemma, Step 6.5'), by hand: correct

- **Setting.** $P_1\cup P_2\subseteq V(F_1)$ and $r\ge2$. Then $P_3\not\subseteq V(F_1)$ by 6.3.
- **$H_1$.** $H_1=H[V(F_1)\cup\{v\}]$ is an induced subgraph, so it is in $C$, and it has at most $n-1$ vertices since another component exists. Its edges are exactly $E(F_1)\cup\{e_1,e_2\}$.
- **Transversal step.**
  - A transversal of $H_1$ of size at most $\tau(F_1)$ that avoids $v$ is a minimum transversal of $F_1$ meeting $P_1$ and $P_2$.
  - One that contains $v$ leaves a transversal of $F_1$ that is too small.
  - So, if no minimum transversal of $F_1$ meets both pairs, then $\tau(H_1)=\tau(F_1)+1$ and slack$(H_1)=$slack$(F_1)+3+4-11\le1-4<0$. This contradicts minimality.
- **Completing the contradiction.** Otherwise, take $T_1$ for $F_1$. Another component $F_2$ meets $P_3$ in some $x_3$ with $d_{F_2}(x_3)\ge1$ (6.2), and U1 applies since slack$(F_2)\le1<5$. Together these give a minimum transversal of $H-v$ meeting all three pairs, contradicting 6.4.
- **$r=3$ is impossible.** If $N(\{e_i,e_j\})=\{Q\}$ then $P_i\cup P_j\subseteq V(Q)$, which is excluded. So Hall's condition holds and 6.5 is contradicted. Hence $r\le2$.
- **Comparison with L017 Theorem 4(iii).** L017 lists seven Hall-deficient patterns. (b') voids exactly the three with two pairs in one component, (c1), (c2) and (d). The survivors (a), (b), (e), (f) are L018's $r=1$, $\{s,s,s\}$, $\{1,2,s\}$ and $\{1,s,s\}$/$\{2,s,s\}$ (6.7). This is consistent: L017 states Hall deficiency, not occurrence. I agree with both round-1 reconciliations.

### Theorem 6(b'), on data (gadget_test.py, own code)

- **Setup.** I took every connected class with $\Delta\le3$ from the refereed L013 lists: tight (10,7,4), (14,12,6), (17,13,7), and slack-1 (8,5,3), (15,11,6), 33 classes in all. For every two disjoint admissible pairs $P_1,P_2$ I built $H_1=F+v+\{v\}\cup P_1+\{v\}\cup P_2$ and computed $\tau(H_1)$ directly.
- **Results.**
  - Over 19,134 instances, "$\tau(H_1)=\tau(F)+1$ ⇔ no minimum transversal of $F$ meets both pairs" never failed. Whenever it applied, slack$(H_1)=$slack$(F)-4$.
  - $\tau$ never went up, i.e. every two disjoint admissible pairs are co-transversal in all these classes.
  - My per-cell instance counts for the tight cells are 442, 50 and 5,621. They equal Step 8.3's 132+89+89+132, 25+25 and 925+891+960+960+960+925 exactly.
- **Caveat on the output file.** gadget_test_output.txt prints running totals, so its per-file lines are cumulative; only the TOTAL line is per run.

### Theorem 4, by hand: correct

- **4.1.** Subdividing an edge keeps the girth at least $g$.
- **4.2.** $H$ is linear because $G$ is simple, and $p$ is its unique pendant.
- **4.3.**
  - $F_7$-freeness follows via triangles. Even more simply, $F_7$ has a vertex of degree 3 and $\Delta(H)=2$.
  - Hall form: $3|W|-|E(G[W])|\ge|W|+2$.
- **4.4.**
  - Forest case: $\sum_W d_G\ge3|W|-1$ (only $g_0$ has degree 2), so $|E_G(W)|\ge2|W|$, and value $\le\tfrac{11}2|W|-6|W|<0$.
  - (Red) case: $G[W]$ has a cycle, so $|W|\ge g$; and $|W|\le2|Z|$, so $|Z|\ge g/2>R$ because $g\ge2R+2$.
- **4.5.** As above.
- **4.6.** $n_2=|E(G)|\ge g\ge22$, so slack $\ge22/7>3$. Theorems 2 and 1 apply: $H$ is linear with $\Delta\le2$, has no isolated vertex, and $n\ge2$.

### Theorem 4, on data (thm4_forest.py, own code)

- **Setup.** I built $H$ from $K_4$, $K_{3,3}$, $Q_3$ and Petersen, each with one edge subdivided, and checked every $Z$ exhaustively: 254, 2,046, 16,382 and 131,070 sets. On Heawood I checked 20,000 random $Z$.
- **Checks.**
  - Lemma 2.2's bound: 0 violations.
  - Forest ⇒ value $<0$: 0 violations.
  - Minimum $|Z|$ of a value-$\ge0$ set (with $Z\ne V$) is at least girth/2: 5, 7, 7 and 7, exhaustively; 14 for Heawood, as the minimum over the random sample only.
  - Each $H$ is linear, with $\Delta=2$ and exactly one pendant.
- **Cross-checks.**
  - The $K_4$ instance is $H=(8,5,3)$ with slack 1, the equality case of Step 2.6. Its minimum (Red) $|Z|$ is 5, as Prop. 8.2's second paragraph says.
  - Petersen has 1,326 value-$\ge0$ sets, independently matching round 1.
- **Low girth.** The low-girth instances ($g=3,4$) test the forest lemma itself, which needs no girth hypothesis, and it holds there too.

### Other passages re-derived

- **Theorem 6(c).** The U1 threshold $\le3<5$ and the U2 threshold $2<2\cdot4-5$ are right.
- **Proposition 6.2, Steps 6.8-6.9.**
  - Cases of $d+d'-[\text{share}]\le2$; the type list; the $F_7$ identification via Lemma 0.7.
  - The assumption "a component containing a pair has $\ge5$ vertices" holds because a pair inside a component lies in no edge of it, so the component is not a single edge.
- **Remark 7.3, degree count for (25,23,11).** $2n_1+n_2=6$, so $n_1\le1$ by Lemma 0.5 and linearity. Then 6.8/6.9 apply.
- **Theorem 7, special case.** $|E_S|=3n_3$ and $n_2(H-S)\ge n_2-6n_3$.

### Data test of the revised Lemma 0.5 (tp_test.py, own code)

- **Data.** All 42 tight cell lists ($3n+2m=11\tau$) of experiments/20261027-0300-tight-cells-d4 (unrefereed; used only as test data), including the $\Delta\le4$ lists.
- **Checks per class.** I recomputed $\tau$, tightness, connectivity and linearity for all 53 classes.
- **Result.** Every pendant of a class that is not a single edge has both co-vertices of degree 2: 21 such pendants, 0 violations. This includes the 12 $\Delta=4$ classes of (21,18,9), which carry 12 pendants. This exercises exactly the newly covered case $d\ge4$.

## Checks performed (commands and outputs)

All runs used nice -n 10, one process each, with timeouts, in experiments/referee/L018-round2-opus/.

1. **Diff audit.**
   - `git show e187bd7 --word-diff=plain -- results/proofs/L018-red-universality.md`, plus a Python token-level diff of `git show e187bd7~1:…` against `git show e187bd7:…`.
   - Result: 12 replaced ranges, at old/new lines 4, 43, 52, 91-92, 110, 123, 126, 220, 228, 231, 233, 237 and 258.
   - `cmp` shows the working tree equals e187bd7, and there is no later commit touching the file.
2. **Leaf classification.** `python3 leaf_iso.py experiments/prover/L018/out_root1_R3_leaves.txt` → leaf_iso_R3_output.txt. Output: `rooted isomorphism classes: 5`, with P-tri-3 Cdegs (2,2) ×2, (2,3) ×4, (3,3) ×2, and best value −1 on all 9 non-closed leaves.
3. **Lemma 0.5 data test.** `python3 tp_test.py $(cat tight_files.txt)` → tp_test_output.txt. Output: `TOTAL {'classes': 53, 'pendants': 30, 'viol': 0}`. The 30 pendants include 9 in single-edge classes, which the lemma excludes.
4. **Theorem 4 data test.** `python3 thm4_forest.py 20000` → thm4_forest_output.txt, all five instances with `l22viol 0, forestviol 0`.
5. **Gadget test.** `python3 gadget_test.py <L013 cells13 lists: 10_7_4, 14_12_6, 17_13_7, 8_5_3, 15_11_6 (D3)>` → gadget_test_output.txt. Output: `TOTAL {'classes': 33, 'instances': 19134, 'logic_viol': 0, 'tau_up': 0, 'tau_up_in_C': 0}`.
6. **Cell lists behind Corollary 7.2 and the new note.** `grep -c '^FOUND'` plus a parse of the INFO JSON:

   | Cell list | Classes | Branches | Inputs searched | connected_hits |
   |---|---|---|---|---|
   | 0340 run, cell_27_15_10_D3 | 0 | d=2, d=3 | all 47 and 55 | 0 |
   | 0300 run, cell_27_20_11_D3 | 0 | d=3 | all 3,865 | 0 |
   | 0340 run, cell_28_19_11_D3 | 0 | d=3 | all 14,348 | 0 |

   - cell_28_24_12_D3 does not exist yet.
   - cell_25_23_11_D3 exists in the 0340 run with 0 classes, computed at 05:52:37Z, after the revision.
7. **Code reading.** experiments/prover/L018/validate_catalog.py, which has the Counter that is never reset, and the counting loop of pendant_census.py.

The prover's longer scripts were not re-run. Both round-1 referees re-ran them and reproduced every quoted number. The machine load was about 9.7.

## New problems, in order of severity

None affects a claimed theorem. N1-N3 are the fixes required for ACCEPT; N4-N7 are optional.

- **N1 (minor; introduced by the revision).** The trailing note to Corollary 7.2 (line 220) says the computation of cell(28,19,11,3) "narrows the open input at $n=29$ in Remark 7.3 to `cell(28,24,12,3)` (and `cell(25,23,11,3)`)".
  - Remark 7.3 voids the only decomposition involving (25,23,11), namely (3,1,1)+(25,23,11) at (29,27,13), by its degree-count argument. So within Remark 7.3 the only open input is cell(28,24,12,3), which is what round 1 suggested.
  - The parenthetical appears to come from the engine route (needed_cells.json of the 0340 run). That route does not use the argument and does need cell(25,23,11,3).
  - Fix: delete the parenthetical, or say "(the engine route, which does not use the argument of Remark 7.3, also needs cell(25,23,11,3); the 0340 run has since computed it empty, 05:52:37Z, unrefereed)".
- **N2 (minor; introduced by the revision; heuristic paragraph).** The Insight paragraph (line 233) now reads "Heuristic reading of the 17 graphs of Proposition 8.2 and of their minimum-size (Red) sets …: the (Red) pairs seen there are of two kinds: *local* ones ($|Z|\le5$ …) and *global* ones".
  - The 17 graphs are defined by having NO (Red) pair with $|Z|\le5$, so no local pair is "seen there". The next sentence ("only global pairs exist") says so.
  - Fix: scope the dichotomy to Proposition 8.2 as a whole, i.e. both paragraphs, where in the low-slack census graphs the smallest (Red) sets have size 2-4 except for the listed graphs. Then say that in the 17 graphs only global, exact pairs occur.
- **N3 (minor; pre-existing; DEPENDS ON honesty).** The sixth DEPENDS ON bullet says the census and "experiments/20261027-0300-tight-cells-d4 (unrefereed)" are "used ONLY for validation …, for the evidence in Remark 5.4 and for the statistics of Section 8; no theorem depends on them". But Corollary 7.2's hypothesis cell(27,20,11,3) is cited from that run. So is the "$n\ge29$" of GAP 2. The fifth bullet correctly says that Corollary 7.2 uses two unrefereed lists, so the two bullets contradict each other.
  - Fix: add "except the hypothesis of Corollary 7.2 (cell(27,20,11,3) from this run and cell(27,15,10,3) from experiments/20261027-0340-induction-n28-n29-f25)".
  - Also add Corollary 7.2 and Remark 7.3 to the L016 bullet. It currently lists only Remarks 0.6 and 5.4 and Step 8.4, but Corollary 7.2 states "Assume I11 on $C$ for $n\le27$ (L016, K61)".
  - The STATUS line itself is accurate.
- **N4 (cosmetic).** The STATUS line says "editorial fixes only, no mathematical change". Lemma 0.5's proof gained a case, a trivial completion. "No change to any statement; the proof of Lemma 0.5 now treats $d\ge4$" would be exact.
- **N5 (cosmetic).** Theorem 1's new remark explains the hypothesis by "cl(T) would contain the isolated vertices". Where the hypothesis is actually used is 1.4, which needs $T\ne\emptyset$ because $Z$ has an edge, and 1.5, where a minimum transversal is nonempty. A two-word example would make it clear: the edgeless graph on 2 vertices.
  - "all uses (Theorem 4.6, Lemma 0.3 via connectedness)" also names Lemma 0.3, which does not use Theorem 1. It presumably means applications to minimal counterexamples, which are connected with at least 2 edges.
- **N6 (cosmetic; pre-existing).** GAP 2 (M1) gives the smallest open sub-case as "two pendant vertices and at least 26 vertices". By Remark 5.4, P2 holds for all tight connected $\Delta\le3$ members with $n\le26$, so the open sub-case has at least 27 vertices, or at least 28 given the unrefereed empty cell (27,20,11,3). "At least 26" is true but not sharp.
- **N7 (informational).** Remark 5.4 says "(25,23,11) with $\Delta\le3$ has not been computed". The 0340 run computed cell(25,23,11,3) empty at 05:52:37Z (unrefereed), after this revision; a later version may record that. The citations "referee 1" in Theorem 3(d) and Step 3.6 would be clearer with the review file name (…__20261027T054329Z.md); the per-n numbers are confirmed above.

## Independence statement

- I read both round-1 reviews, as instructed. I did not look into experiments/referee/L018-round1/ or experiments/referee/L018-round2/, or read any other review of L018.
- All verification code in experiments/referee/L018-round2-opus/ was written by me: leaf_iso.py, tp_test.py, thm4_forest.py and gadget_test.py. It imports nothing from e757/, judge/ or experiments/prover/L018/ (hg.py, localconf.py). It uses its own exact $\tau$ routines; networkx is used only for graph construction, isomorphism and matchings.
- I read the prover's validate_catalog.py and pendant_census.py only to audit the count semantics. I used the prover's stored leaf file and the stored cell lists as inputs.
- The hand verification covers every edited passage and Theorems 4 and 6(b') in full, plus Theorem 6(c), Proposition 6.2, Theorem 7 and the Remark 7.3 argument.
- I modified no file other than this review and my scratch folder.
