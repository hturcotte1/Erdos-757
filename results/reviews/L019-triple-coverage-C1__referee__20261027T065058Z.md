VERDICT: NEEDS-WORK

# Referee report: L019 (results/proofs/L019-triple-coverage-C1.md), round 1, referee #1 (opus)

Certificate read in full (213 lines, every step numbered and checked). Work folder of the prover: experiments/prover/L019/. Referee scratch folder: experiments/referee/L019-round1-opus/. I did not read any other review of L019.

## Summary

L019 does not claim to prove Conjecture C1. Everything it presents as proved is correct as stated: Theorems 1-6, Lemma 7, Propositions 8 and 10, and Lemma 11. Proposition 9 is correctly proved under Conjecture T3. I re-derived every step by hand and found no mathematical error and no unmarked gap. The two GAPs ($s(F)=1$ and $s(F)=0$) are marked exactly where the argument stops, and nothing outside them is left unproved.

I also tested the statements with code written for this review, which imports nothing from the prover, pyverify, e757/ or judge/. No counterexample turned up:
- **Folding lemma (Theorem 5 (a)-(d), including the exact slack change +1):** 79,426 folds, on
  - 655 stored class-C graphs from 18 cells;
  - 2,500 random linear 3-graphs;
  - 11,691 AP hypergraphs of (4,5)-sets: $A_{\rm base}$ and all 11,529 of its induced subsets that contain an edge, the three 12-point sets, the records for n = 8, 10, 11, Fibonacci $\{2,3,5,\dots\}$, the reader family K = 0, 1, two generic gluings, and 150 census-14 classes.
- **Lemma 11:** 31,686 saturated sets.
- **Theorem 2(iv):** all 586 stored graphs with slack at most 1.
- **Theorems 1-4, Lemma 7 and Proposition 10 in two hereditary analogues of C where the theory is not vacuous:**
  - L, all linear 3-graphs (first violator $F_7$, with N = 6);
  - L′, linear and $F_7$-free. I enumerated all 231,577 labelled linear 3-graphs on 8 vertices, so I11 holds in L′ up to N = 8. The setting of C1 is non-empty there (6 failures of C1, giving the two (9,8,4) violators).
- **Prover's computations C1-C8:** these reproduce byte-for-byte. My independent recomputation confirms every number the certificate quotes, including the (26,22,11) entry of C8.

The defects are editorial:
- the stored C8 output file lacks the (26,22,11) line that the certificate cites;
- the dependency tags are stale: L017 is now ACCEPTED (K64), while the unrefereed L017 Corollaries 13.3 and 13.5 used in Remark 9.2 are not flagged as unrefereed;
- the statement called "Conjecture C1" adds two hypotheses to the source conjecture without saying it is a restricted form;
- several remarks are imprecise.

On the verdict line: the referee format I must follow allows only ACCEPT, NEEDS-WORK or REJECT, and reserves ACCEPT for a document in which no problem remains. The verdict is therefore NEEDS-WORK. In the commissioning workflow's vocabulary this is **ACCEPT WITH FIXES**: no theorem, proof step or GAP statement needs to change.

## Theorem-by-theorem audit

**Step 0 (facts).**
- 0.1-0.7: checked. 0.5 is the identity $s(K-Z)=s-3|Z|-2|\partial Z|+11(\tau-\tau(K-Z))$, and the same identity holds for edge sets. In 0.7, $\tau(K^+)=\tau(K)$ holds iff some minimum transversal of $K$ meets all the $Q_j$; this is correct, since a transversal of $K^+$ of size $\tau(K)$ cannot contain $w$.
- 0.8 (L017 Theorem 7 = K65, a known result):
  - the dual graph is simple and subcubic, and $\tau\le m-\nu$;
  - $s\ge3n_0+11\nu-3|E(G)|$, using $3m=n_1+2n_2$;
  - in the Tutte–Berge bookkeeping, every $t_i\ge0$: $c=1$: 0; $c=2$: $16/11$; $c=3$: $4/11$; $c=4$: $8/11$; $c=5$: $2/11$ (using $e\le7$); even $c\ge6$: $2c/11$; odd $c\ge7$: $(2c-8)/11$. Correct.

**Theorem 1 (slack floor).**
- 1.1: by definition, $K$ is a minimal counterexample.
- 1.2: $K-x\in C$ has $N$ vertices, so $s(K-x)\ge0$, and $\tau(K-x)\in\{\tau-1,\tau\}$ by 0.3. If $\tau(K-x)=\tau$, then 0.5 gives $s(K-x)=s-3-2d<0$, which is impossible. Hence $x$ is co-transversal (0.4) and $s(K-x)=s-3-2d+11=s+8-2d$. **The bookkeeping and the justification of $\tau(K-x)=\tau-1$ are correct.**
- 1.3: from $2d\le s+8\le7$ we get $d\le3$. The case $\Delta\le2$ is excluded by 0.8, and a vertex of degree 3 gives $s\ge-2$.

**Theorem 2 (richness).**
- 2.1: if no minimum transversal meets the pairs, then $s(K^+)=s(K)+2k-8$. Then:
  - (i) $\ge0$ gives $s(K)\ge8-2k$;
  - (ii) $\ge-2$ (Theorem 1 at $N+1$) gives $s(K)\ge6-2k$;
  - (iii) $s(K^+)\le-1$ forces $\Delta(K^+)=3$.
  All three contradict the respective hypotheses.
- 2.2 (iv): $K\setminus D$ stays in C. Linearity, $F_7$-freeness and (P3) are all preserved by deleting edges, and the vertex set does not change.
  - The slack of $K\setminus D$ is bounded below by 0 if $n\le N$, and by $-2$ if $n=N+1$. The latter comes from **Theorem 1, which needs I11 only up to N vertices, not minimality of m**, so the improvement over L017 Theorem 1(g) is legitimate.
  - Single edges: $\lceil(2-s)/11\rceil=1$ for $s\in\{0,1\}$, and $\lceil -s/11\rceil=1$ for $s\in\{-1,-2\}$.
- 2.3: the thresholds in the "Consequences" paragraph are correct:
  - $k=2$, $s(H-y)\le1=5-4$;
  - $k=3$ with a degree-4 witness, $1=7-6$;
  - $d(y)=2$, $3=7-4$;
  - (i) at $\le n-2$ vertices, 1 and 3.

**Theorem 3 (pair-pair coverage).**
- $F+v(P_i,P_j)$ and $H\setminus(\{v\}\cup P_k)$ are the same 3-graph (same vertex set, and edges $E(F)$ plus the two edges at $v$). It lies in C by edge-heredity.
- The relevant N is $N=n_F$: this is exactly the inductive hypothesis of the setting. $K^+$ has $n_F+1$ vertices, and Theorem 2(ii) with $k=2$ needs $s(F)\le1$, which holds.
- Equivalently, as in Remark 3.2: $s(K^+)=s(F)-4\le-3<-2$, which Theorem 1 forbids at $N+1=n_F+1$.
- Neither connectivity nor the third pair is used. Correct.

**Theorem 4.**
- (a) is 0.7 with $k=3$, plus 0.4. Here $s(H)\in\{s(F)+9,\ s(F)-2\}$ and $s(F)\in\{0,1\}$, so the sign of $s(H)$ separates the two cases.
- (b), forward: $H$ is a minimal counterexample by definition.
- (b), converse: the $P_j$ are disjoint by linearity; $s(F)=s(H)+2\le1$ by Theorem 1 with $N=n-1$; $F\in C$; $F$ is connected by hypothesis; and (a) gives the failure.
- (c): if $n_F\le26$ then $n(H)\le27$, and L016 (K61: I11 on C for $n\le27$) gives $s(H)\ge0$. The two degree conditions give $\Delta(H)\ge4$, contradicting Theorem 1.
- (d): correct.

**Theorem 5 (folding lemma).** (I recomputed n, m, $\tau$ and s.)
- (a): adjacency of $y$ and $z$ is the same in $K$ and in $K-x$, because $z\notin\{x,u,u'\}$.
  - No image edge is degenerate.
  - Equal images would each contain $\zeta$, one coming from $y$ and the other from $z$, and the two preimage edges would then share two vertices, contradicting linearity.
  - So $m(K^\circ)=m-2$ **exactly** (only the two edges at $x$ are lost; m never drops by only 1), $n(K^\circ)=n-2$, and $d(\zeta)=d(y)+d(z)-2$.
- (b): the lifting argument is correct.
- (c): the image of $T\setminus\{x\}$ is a transversal of $K^\circ$, so $\tau(K^\circ)=\tau-1$ and $s(K^\circ)=s-6-4+11=s+1$. In general $\tau(K^\circ)\in\{\tau-1,\tau\}$, which my random test confirms.
- (d):
  - the linearity criterion holds in both directions;
  - a copy of $F_7$ avoiding $\zeta$ is already a copy in $K$;
  - for (P3), pulling a set containing $\zeta$ back through the identification map gives $e_{K^\circ}(S^\circ)=e_K(S)\le|S^\circ|-1$, which yields the saturated-set criterion;
  - $|S|\ge6$: 3 vertices would make S an edge through $y,z$; 4 would put two edges in 4 points; 5 would need three edges of a linear 3-graph in 5 points, which is impossible.
- (e): correct.

**Theorem 6.**
- (Red) and (Pair) hold. For (Pair): if a pair is not co-transversal, then $\tau(G-y-z)\ge\tau(G)-1$.
- (a):
  - an isolated vertex would give $s\ge3$;
  - degree 1, first step: (Red) with $Z=\{t,a'\}$, $T=\{a'\}$ gives $0\le3-2d(a')$, so $d(a')\le1$;
  - degree 1, second step: (Red) with $Z=\{t,a',b'\}$, $T=\{b'\}$ gives $0\le-2d(b')$, which is absurd;
  - this uses $s=-2$; for $s=-1$ the first step only yields $d(a')\le2$, consistent with L017 Theorem 3(c);
  - $n_2=3(n-m)\ge6$ by (P3) on $V(H)$.
- (b): $s(H-x)=2$. A minimum transversal of $G$ containing $y,z$ would cover $H$ with $\tau-1$ vertices. (Pair) then gives $|\partial_G(y,z)|\le3$, i.e. $4-\sigma\le3$.
- (c): correct.
- (d):
  - $x'\notin\{p,q\}$, and $t\notin P_i$;
  - $2+d_H(t)-1-[t\in P_j\cup P_k]\le3$;
  - the neighbours of $v$ in $G$ are $P_j\cup P_k$, and $g_t$ is the only edge of $G$ at $t$;
  - the correspondence between $S$ and $U$ is correct: $d_{H[S]}(t)=0$ would violate (P3) on $S-t$, and the converse direction is also correct.
- 6.6 and 6.7: correct.

**Lemma 7.** $T'=(T-y)+t$ is a minimum transversal, because $g$ is the only edge whose trace on $T$ is $\{y\}$. Then $T'\supseteq T-y$ gives the conclusion. Correct.

**Proposition 8.** I re-derived every row of the table:
- deleting a co-transversal set X: 0.5 with $\tau(H-X)=\tau-|X|$ and $|\partial X|\le3|X|$;
- edge deletion: Theorem 1;
- fold: Theorem 5(c);
- replacement: 0.7 gives $s(H')=s+2k+5-11\varepsilon$.

The conclusions for $s=-1$ and $s=-2$ are correct.

**Proposition 9 (conditional on T3, as stated in L017 13.1).**
- $n(H^\circ)\ge26$ (L016).
- $H^\circ$ is connected, as the image of the connected $H-x$.
- $\Delta(H^\circ)\le3$, because $d(y)+d(z)-2\le3$.
- $s(H^\circ)=0$, and with these properties T3 (at most 24 vertices) gives the contradiction. Correct.

I checked the parenthetical citations against L017 Theorem 5(A)(iv), Corollary 13.5(i) and Corollary 13.3(iii). The last two are unrefereed computations; see problem 2.

**Proposition 10.**
- Every co-vertex has degree $\ge2$; otherwise it would be isolated in $H-v$ and $s(H-v)\ge3>1$.
- An edge of $H-v$ contains at most one vertex of each pair (linearity), so $k\ge2$. If $k=2$, the five edges form $F_7$ with centre $v$.
- $|\partial Z|=3+k$, and $Z\ne V(H)$.
- (Red) holds for any $s$, giving $11|T|\ge27+2k-s\ge28+2k$. The thresholds $|T|\ge4$ and $|T|\ge5$ are correct; see problem 5(i) for a superfluous clause.

**Lemma 11.**
- (a) is the degree sum.
- (b): isolation violates (P3) on $S-y$, and $S-y$ is saturated when $d_{K[S]}(y)=1$.
- (c): terms equal to 0 or 1, six ports, at most one leaving edge per port.
- Peeling: correct.

**GAP section.**
- By Theorem 4(a),(b), the restricted C1 fails exactly at minimal counterexamples with a degree-3 vertex $v$ and $H-v$ connected, with $s(F)\in\{0,1\}$. These are GAP 1 and GAP 2, and both are honestly stated.
- The conditional closure of GAP 2 under T3 is correct: $F$ is connected and tight with $\Delta\le3$ and $n_F\ge27>24$.
- Nothing outside the GAPs is unproved.

## Checks performed (commands run in experiments/referee/L019-round1-opus/, nice -n 10, one process at a time, each under timeout)

1. **`python3 selftest.py`** checks my own library `refhg.py`:
   - transversal number by branch and bound on a maximum-degree vertex, compared with brute force;
   - (P3) by a zeta transform over all subsets, compared with an independent Hall/Kuhn check;
   - $F_7$ search by two disjoint edges, a centre and a bijection.

   Output:
   - 400 random graphs, 0 mismatches;
   - 1 copy of $F_7$ in $F_7$ and 0 in the Fano plane (correct: Fano minus two lines has degrees $1,2^4,3^2$);
   - the first 25 classes of each of the 19 stored cells: 318 headers (n, m, $\tau$) confirmed and all 318 graphs in C.
2. **`bash run_fold_all.sh`** runs `test_fold.py` (Theorem 5 (a)-(d), the slack change and $\tau(K^\circ)-\tau(K)$) on 18 cells and on 2,500 random linear graphs. Output: `fold_all_output.txt`.
   - Cells: 655 graphs, 14,528 folds. All are at co-transversal $x$, all have $\tau(K^\circ)=\tau-1$, and 6,337 of the folds are in C.
   - Random graphs: 21,581 folds. 4,768 are at non-co-transversal $x$, with $\tau(K^\circ)-\tau\in\{-1,0\}$.
   - Minimum saturated-set sizes 6 to 12.
   - **0 failures.**
3. **`python3 test_ap_and_lemma11.py ap`** runs on AP hypergraphs. Each set was first checked by brute force to be a (4,5)-set (the 24-point gluing included) and its AP hypergraph to lie in C. Output: `ap_output.txt`.
   - 11,691 graphs and 43,317 folds, **0 failures**.
   - Lemma 11 on 11,535 graphs with $\Delta\le3$: 24,808 saturated sets, **0 failures**.
4. **`python3 test_ap_and_lemma11.py lemma11 <cell> K`** on 14 cells (`lemma11_cells_output.txt`): 6,878 saturated sets, 0 failures. Together with check 3 this gives 31,686 sets, 300 of them 2-core.
5. **`python3 test_ap_and_lemma11.py thm2iv <cell> K`** (`thm2iv_output.txt`):
   - 586 stored graphs with slack at most 1, 8,382 edges, **all critical**;
   - 11,720 sampled bounds with $|D|\in\{2,3\}$, 0 failures.
   - (The run on the single-edge cell (3,1,1) crashed in my sampler; that case is trivial.)
6. **`python3 test_linear_analogue.py`** (`linear_analogue_output.txt`), class L:
   - all 5,596 labelled linear 3-graphs on 7 vertices, and I11 checked for $n\le6$;
   - Theorem 1 at $n=7$: the 420 labelled violators are exactly the copies of $F_7$ ($7!/12$), all with $\Delta=3$, $s=-2$, every vertex co-transversal and the bookkeeping exact;
   - Theorem 2(i)-(iii): 1,002 gadget instances. The thresholds are sharp in L: 360 uncovered pairs at $s(K)=2$ for $k=2$;
   - Theorem 2(iv): 66,882 pairs (K, D);
   - **0 failures**. (With $n_F=6$ no connected $F$ with slack at most 1 exists, so Theorems 3/4/6 are vacuous in L.)
7. **`python3 test_lprime.py`** (`lprime_output.txt`), class L′:
   - 231,577 labelled linear 3-graphs on 8 vertices; every $F_7$-free one satisfies I11;
   - 2 isomorphism classes of connected $F_7$-free $F$ with slack at most 1, both (8,5,3);
   - 43 admissible triples: C1 holds for 37 and fails for 6;
   - checked on these: Theorem 3, the equivalences of Theorem 4(a), 4(c), 4(d), Lemma 7 (58 instances), Theorem 1 and Theorem 2(iv) on H, and Proposition 10 ($(k,\tau)=(5,4)$);
   - the same checks directly on the two (9,8,4) violators (vertex-critical, $F_7$-free, every degree-3 vertex with $H-v$ connected);
   - **0 failures**.
8. **`python3 c8_check.py <cell> 100000`** (`c8_output.txt`) is an independent C8. It enumerates all minimum transversals, all uncoverable linear triples, k, and $\tau$ of the edges meeting $\{v\}\cup W$:

   | cell | uncoverable linear triples | $(k,\tau)$ counts |
   |---|---|---|
   | (17,13,7) | 24 | (6,4): 24 |
   | (15,11,6) | 154 | (5,4): 22, (6,4): 124, (7,5): 8 |
   | (22,17,9) | 380 | (6,4): 380 |
   | (26,22,11) | 144 | (6,4): 144 |

   These are exactly the certificate's values. No uncoverable triple is admissible, as Theorem 4(c) and L016 force, and every disjoint linear pair-pair is covered.
9. **`python3 test_blocked.py <cell> 300`** (`blocked_output.txt`) and **`python3 test_c7_23.py`** recompute C4-C7 independently.
   - (14,12,6): all-blocked classes #4 and #8, degrees $2^6 3^8$, each with 14 non-linear and 10 adjacent folds.
   - (12,10,5): #150 and #194 ($2^6 3^6$), #209 and #210 ($1\,2^4 3^7$).
   - (10,8,4): the classes with degrees in {2,3}, Theorem 6(b) everywhere and every fold blocked are #39, #40 and #60, blocked by adjacency or non-linearity only.
   - None in (10,7,4), (17,13,7), (15,11,6), (13,9,5), (16,10,6), (8,5,3), (9,4,3), (6,3,2), (22,17,9) or (26,22,11).
   - In (23,21,10), every one of the 699 classes has a degree outside {2,3}.
   - All of this matches the certificate.
10. **Reproducibility.**
    - `rerun/rerun_small.sh` (unmodified copies of the prover's scripts): identical outputs for C1 (cells), C2, C3, C5 (two cells), C6 (both), C7 (two cells) and C8 (17,13,7).
    - `rerun_full/reproduce_copy.sh` (byte-identical copy of reproduce.sh): all nine `*_output.txt` files identical to the prover's, **including the missing (26,22,11) line of nbhd_cover_output.txt**. The script exited 0 after 501 s.
    - `rerun_full/c8_loop.sh` (the exact C8 loop of reproduce.sh, alone, 503 s) prints all four lines, including `cell_26_22_11.txt ... {(6, 4): 144}`.
    - Why the fourth iteration left no line in the full run is unexplained: that run's 501 s total is shorter than the C8 loop alone needs, yet its exit status was 0. It may be an artefact of background execution here.

## Problems found (in order of severity; none affects a proved statement)

1. **The C8 evidence file is incomplete.**
   - The certificate (bullet C8) and Remark 10.3 ("all 702 uncoverable linear triples ... $k\in\{5,6,7\}$") cite a (26,22,11) entry: 144 triples, all (6,4). That line is not in experiments/prover/L019/nbhd_cover_output.txt, which has three lines.
   - reproduce.log is from 05:15 and predates the C7/C8 outputs (05:24-05:34).
   - The claim is true: my independent recomputation and a separate run of the prover's own C8 loop both give 144 triples, all (6,4).
   - Fix: regenerate nbhd_cover_output.txt with the (26,22,11) line, and refresh reproduce.log after a complete run.
2. **Stale dependency tags.**
   - DEPENDS ON tags L017 as "[derived-here, unrefereed]", and the GAP section says "all of L017 Theorems 1–5 (unrefereed)". In fact L017 Theorems 1–6 are [verified-here] (K64, referee ACCEPT x2 in round 2) and Theorem 7 is K65 [published, re-proved].
   - In the other direction, L017 Corollaries 13.3(iii) and 13.5(i) are unrefereed computations that the K64 acceptance excludes. They carry the "therefore" of Remark 9.2 ("Under T3 a minimal counterexample therefore has $s=-1$, no vertex of degree 1"), and that remark should be tagged as resting on them.
3. **The restated conjecture is not acknowledged as restricted.**
   - The source (experiments/20261027-0300-transversal-richness/README.md, "(C1) If F in C has slack ≤ 1 and v extends F inside C ...") has neither "F connected" nor "I11 holds for every member of C with at most $n_F$ vertices". L019's "Conjecture C1" adds both.
   - That is the form relevant to case (a) of L017 Theorem 4, and Theorem 4(b)'s equivalence and both GAPs concern only this restricted form.
   - Fix: say so explicitly, e.g. "Conjecture C1 (restricted form)".
4. **Remark-level inaccuracies.**
   - (i) In "On the data behind C1", the sentence "every uncoverable triple in the stored lists necessarily has F+v∉C (this much is forced by L016)" holds only for the lists with slack at most 1. The slack-2 lists contain admissible uncoverable triples, as the certificate's own Sanity checks (last item) say.
   - (ii) GAP 1 says "No local configuration argument of the kind used in L017/L018 or here can close this case without an additional structural input". GAP 2 says "It cannot be proved by a purely local argument from folds". Both are heuristic. Proposition 8 proves only that a single application of each listed operation gives no contradiction. Tag them [heuristic] or rephrase.
   - (iii) The sanity check "The hypothesis $s(K)\le1$ of Theorem 2(ii) at $k=2$ cannot simply be dropped" uses the (6,3,2) example, whose gadget is $F_7\notin C$. That example says nothing about the slack hypothesis inside C. It does show sharpness in the class of all linear 3-graphs (check 6). Rephrase.
   - (iv) C7 says "over all stored classes of all 17 cells of slack 0, 1, 2 (…/inputs)", but the inputs folder has 19 cells. (3,1,1) and the slack-1 cell (23,21,10), which has 699 classes, were not run. The conclusion still holds for (23,21,10), because every class there has a degree outside {2,3} (check 9). Say so.
5. **Typos and cosmetics.**
   - (i) Proposition 10, step 10.2: "With $k\ge9$ and $s(H)\ge-2$: $11|T|\ge46$". The bound already follows from "$\ge28+2k$", which uses $s(H)\le-1$; the clause "$s(H)\ge-2$" is superfluous and reads like a reversed inequality.
   - (ii) Naming is inconsistent:
     - the STATUS line says "Lemmas 7, 11 and Propositions 8, 10";
     - the work-folder README lists only "Theorems 1-6, Lemma 7, Propositions 8, 9";
     - the commissioning task calls Lemma 11 "Prop 11".

     Harmonise these.
   - (iii) The check_folding.py docstring says "random connected linear 3-graphs", but the generator does not enforce connectivity. This is harmless.

Fixes 1, 2, 3 and 4(i)–(iii) are needed for ACCEPT. The rest are optional.

## Independence statement

I did not read any other review of L019. The other L019 files in results/reviews/ were seen only as file names in a directory listing and were not opened.

All mathematical checks were done by hand from the certificate and from L017's statements, and all verification code in experiments/referee/L019-round1-opus/ was written for this review. It imports nothing from experiments/prover/L019/, experiments/20261027-0300-transversal-richness/ (pyverify.py), e757/ or judge/. The prover's scripts were used only as unmodified copies (rerun/, rerun_full/) to test reproducibility. I edited no file outside my scratch folder and this review.
