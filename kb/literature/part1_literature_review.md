# Part 1: Literature review (12 Oct 2026), with corrections

*This is the original deep-research report. Corrections found on 13 Oct 2026 are marked **[CORRECTION]** inline. Where anything here conflicts with `kb/00_START_HERE.md`, START_HERE wins.*

# Erdős Problem #757: Sidon Subsets of (4,5)-Sets, Literature Review and Agent Briefing

The problem is still open. As of October 2026 the best published bounds are $\tfrac{9}{17}\le c_*\le\tfrac{4}{7}$, i.e. $0.5294\le c_*\le 0.5714$. Both come from Jie Ma and Quanyu Tang (arXiv:2602.23282v2, 6 March 2026). Their paper improves the 1995 Gyárfás–Lehel bounds $\tfrac12+\tfrac{1}{141\cdot 76}\le c_*\le \tfrac35$. Every lower-bound proof so far runs through one reduction: a hypergraph whose edges are the 3-term arithmetic progressions in the set. The 9/17 bound comes from plugging in an existing transversal inequality from hypergraph theory (Henning–Yeo) that does not use the arithmetic. Closing the gap will most likely need extra arithmetic structure that these hypergraphs inherit from the real line. No one has published such an argument.

## TL;DR

- **Open problem:** for a finite set $A\subset\mathbb R$ in which every 4 points determine at least 5 distinct distances, find the best constant $c_*$ such that $A$ always contains a Sidon subset of size at least $c_*|A|$. Ma–Tang (2026) proved that the limit $c_*=\lim f(n)/n=\inf_n f(n)/n$ exists, and they established $9/17\le c_*\le 4/7$.
- **How the bounds are proved:** the upper bound 4/7 comes from one explicit 14-point set whose largest Sidon subset has 8 elements. This set was found with AI help and checked by exhaustive search. The lower bound 9/17 comes from the 3-AP hypergraph $H(A)$, which is 3-uniform, linear, $F_7$-free and has at most $n-2$ edges. Combining this with Henning–Yeo's inequality $17\tau\le 5n+3m$ gives the result.
- **Where to attack:** the gap is $[0.5294, 0.5714]$. Two routes look most promising. (a) Construct better (4,5)-sets with computer search; one unpublished check found the published 14-point block cannot be beaten by adding two more points. (b) Prove a transversal bound for 3-AP hypergraphs that uses realizability on the real line, not just the abstract hypergraph properties. A community attempt at (b) refuted a natural auxiliary inequality on explicit 12-point sets.

---

## 1. Precise statement, notation and variants

**Definitions.**
- **Sidon set:** a finite set $S\subset\mathbb R$ is Sidon if the sums $x+y$ with $x\le y$ in $S$ are all distinct. Equivalently, all positive differences in $S$ are distinct (sometimes called a Golomb ruler).
- **(4,5)-set:** a finite set $A\subset\mathbb R$ is a (4,5)-set if every 4-element subset determines at least 5 distinct values among its 6 pairwise absolute differences.
- **Weak Sidon set:** the sums $x+y$ with $x<y$ are all distinct.
- $h(A)$ is the size of the largest Sidon subset of $A$.
- $f(n)=\min\{h(A): A \text{ is a (4,5)-set}, |A|=n\}$.
- $c_*$ is the optimal constant in "every (4,5)-set of size $n$ has a Sidon subset of size at least $c_* n$".

**Formulations by source.**
- **erdosproblems.com.** The problem is stated as: "Let $A\subset \mathbb{R}$ be a set of size $n$ such that every subset $B\subseteq A$ with $\lvert B\rvert =4$ has $\lvert B-B\rvert\geq 11$. Find the best constant $c>0$ such that $A$ must always contain a Sidon set of size $\geq cn$."
  - The site notes that a Sidon $B$ would have $|B-B|=13$, so the condition says at most one difference is "missing".
  - It gives the equivalent distance reformulation: every four points determine at least five distinct distances, and we want a subset with all distances distinct.
  - It says one may assume $A\subset\mathbb N$.
  - The source is cited as [Er97b], meaning Erdős, *Some old and new problems in various branches of combinatorics*, Discrete Math. 165/166 (1997), 227–231. Ma–Tang locate the problem on p. 231.
  - Tags: geometry, distances, Sidon sets. No prize is attached; the problems.yaml metadata records prize "no".
- **Ma–Tang (Problem 1.4).** The same problem, phrased directly with absolute differences.
- **Gyárfás–Lehel (1995).** They define $g(n)$ as the largest number such that every $n$-element (4,5)-set contains a $g(n)$-element Sidon set. They prove $(\tfrac12+\epsilon)n\le g(n)\le \tfrac{3n}{5}+1$.
- **Versions of the site page.** An older snapshot (accessed Dec 2025) wrote the bounds as $\frac12<c<\frac35$, restricted to $A\subset\mathbb R_{>0}$, and credited "Erdős and Sós" with $c\ge 1/2$. Later snapshots (July–Oct 2026) give the explicit $\frac{1}{2}+\frac{1}{141\cdot 76}$, say "the example proving the upper bound is the set of the first $n$ Fibonacci numbers", and thank Yongxi Lin and Quanyu Tang.
  - **[CORRECTION]** Taken literally, "the first $n$ Fibonacci numbers" contains $\{1,2,3,5\}$, which has only four distances, so it is not a (4,5)-set. Starting at 2 ($\{2,3,5,8,\dots\}$) works, with ratio $3/5+O(1/n)$.
- **Status discrepancy.** I could not fetch the live 757 page, which blocks automated access, so I cannot confirm it lists Ma–Tang's 9/17 and 4/7. Treat the arXiv paper as the authoritative state of the art.
  - **[CORRECTION]** The forum page was read on 13 Oct 2026. It lists $\frac{9}{17}\le c\le\frac47$ (last edit 10 April 2026), says "Formalised statement? Yes", and contains no proof claims.
- **Site policy change.** Bloom announced in October 2026 that the site will no longer display problem statuses, so "open" here is based on the literature.

**Equivalence of the (4,5) condition.** Four points $a<b<c<d$ fail the condition exactly when two different pairs of difference coincidences occur. Ma–Tang show:
- Every Sidon set is a (4,5)-set, and every (4,5)-set is weak Sidon. Both inclusions are strict.
- $\{1,2,3,5\}$ is weak Sidon but not (4,5).
- $\{1,2,3,6\}$ is (4,5) but not Sidon.

**Key reformulation (Gyárfás–Lehel; proofs written out by Ma–Tang).** Let $H(A)$ be the 3-uniform hypergraph whose edges are the 3-term APs in $A$.
- **Lemma 2.3:** if $A$ is weak Sidon, a subset is Sidon exactly when it contains no 3-AP. Hence $h(A)=\alpha(H(A))=n-\tau(H(A))$.
- **Lemma 2.4:** for weak Sidon $A$, the map from an AP to its midpoint is injective. So $m\le n-2$, and the same holds for every induced subset.
- **Lemma 2.5:** for a (4,5)-set, $H(A)$ is linear, meaning two APs share at most one point.
- **Lemma 5.2 (Gyárfás–Lehel Prop. 2.6):** $H(A)$ contains no copy of $F_7$, the hypergraph on $\{0,\dots,6\}$ with edges $\{012,034,056,135,246\}$.

So the problem becomes: **find the minimum independence ratio over 3-uniform hypergraphs that can be realized as the 3-AP hypergraphs of real (4,5)-sets.** The abstract properties (linear, $F_7$-free, $m\le n-2$ on every induced subset, distinct midpoints) are necessary but are not known to be sufficient for realizability.

## 2. Origin and history

- **Erdős (1997), [Er97b].** The problem first appears here (Discrete Math. 165/166, 227–231, p. 231). The same paper contains the planar distinct-distance question #135. In that context Erdős "makes the even stronger conjecture that $A$ must contain $\gg n$ many points such that all pairwise distances are distinct" (erdosproblems #135 page).
- **Erdős–Sós.** The site attributes the lower bound $c\ge 1/2$ to them. One way to see it: Gyárfás–Lehel Prop. 2.1 gives a 2-colouring of a (4,5)-set into two Sidon sets via a forest-colouring argument (as described in the community issue cited in §5). No separate Erdős–Sós paper was located.
- **Gyárfás–Lehel (1995).** *Linear Sets with Five Distinct Differences among Any Four Elements*, J. Combin. Theory Ser. B 64 (1995), 108–118, doi:10.1006/jctb.1995.1028. Their abstract says "the main result is the lower bound whose proof is based on a Turán-type theorem obtained for sparse 3-uniform hypergraphs associated with (4,5)-sets." They get $\epsilon=1/(141\cdot76)$. The upper bound $3n/5+1$ comes from a Fibonacci-based sequence. An author PDF exists on Gyárfás's Rényi page (users.renyi.hu/~gyarfas/Cikkek/69_linset5.pdf), but I could not fetch it.
- **Wider context.** The (4,5) condition comes from the Erdős–Gyárfás generalized Ramsey function $f(n,p,q)$. Bennett, Cushman, Dudek and Prałat proved $f(n,4,5)=\tfrac56 n+o(n)$ (JCTB 169 (2024), 253–297); Joos and Mubayi reproved it (PAMS 152 (2024)). Ma–Tang call the (4,5) concept "closely related to an anti-Ramsey problem."
- **Sárközy–Sós.** In *On additive representative functions* (The Mathematics of Paul Erdős I, 2013, p. 247, Problem 12) they asked about the analogous constant for weak Sidon sets. They noted Gyárfás–Lehel might be relevant, but Ma–Tang point out it does not apply directly.
- **Ma–Tang (Feb/Mar 2026).** arXiv:2602.23282, v1 26 Feb 2026, v2 6 Mar 2026. They solve the weak-Sidon problem exactly and improve both bounds for #757.

## 3. Current status: every known result

| Result | Statement | Source |
|---|---|---|
| Trivial and folklore lower bound | $c_*\ge 1/2$ | attributed to Erdős–Sós (site); Gyárfás–Lehel Prop. 2.1 forest colouring |
| Gyárfás–Lehel 1995 | $(\tfrac12+\tfrac{1}{141\cdot 76})n\le f(n)\le \tfrac35 n+1$ | JCTB 64 (1995) |
| Existence of the limit | $c_*=\lim f(n)/n=\inf_n f(n)/n$, since $f$ is subadditive (Fekete) | Ma–Tang Thm 1.5 |
| Upper bound | $c_*\le 4/7$ via $f(14)\le 8$ | Ma–Tang Lemma 5.1 |
| Lower bound | $f(n)\ge \tfrac{9}{17}n$ for all $n$ | Ma–Tang Thm 1.6 |
| AI-found intermediate | a 12-point example gave $c_*\le 7/12$ before the 14-point one | Ma–Tang AI declaration |
| Weak-Sidon analogue (solved) | $g(n)=\lceil (n+1)/2\rceil$ exactly, so $\gamma_*=1/2$ | Ma–Tang Thm 1.3 |

**The 14-point extremal block.**
- $A_{\rm base}=\{0,136,200,243,246,249,272,286,298,323,400,528,596,1056\}$ has $h=8$.
- A largest Sidon subset is $\{0,136,200,243,246,298,323,528\}$.
- Verification code: github.com/QuanyuTang/ep757-45set-base-block-verification.
- An independent check (the-omega-institute issue #9804) confirmed all 1001 quadruples satisfy the condition and that the hypergraph has 12 AP edges and independence number 8.

**Why subadditivity matters.** Lemma 3.6 shows that two (4,5)-sets $A$ and $qB+t$, with $q$ generic and $t$ large, can be joined into a (4,5)-set with $h(C)\le h(A)+h(B)$. So **any single finite example with ratio $r$ gives $c_*\le r$**. Upper bounds are therefore a finite-search problem. The problem is not finitely decidable in general, though, because the lower bound must hold for all $n$.

## 4. Catalogue of methods

### 4.1 The AP-hypergraph and transversal method (all lower bounds)
- **Idea:** $h(A)=n-\tau(H)$, so any inequality $\tau\le an+bm$ combined with $m\le n-2$ gives $h\ge (1-a-b)n$.
- **Chvátal–McDiarmid / Tuza:** $4\tau\le n+m$ for every 3-uniform hypergraph (Combinatorica 12 (1992); Discrete Math. 86 (1990)). This gives exactly $h\ge (n+1)/2$, which is sharp for weak Sidon sets but only yields 1/2 for #757.
- **Gyárfás–Lehel:** their own Turán-type transversal estimate for linear $F_7$-free sparse hypergraphs gave $+1/(141\cdot76)$.
- **Henning–Yeo 2021:** for a 3-uniform linear hypergraph with no copy of $F_7$ (which is $AG(2,3)$ with two vertices deleted), $17\tau\le 5n+3m$ (Graphs and Combinatorics 37 (2021), 867–890, Thm 7). Then $17\tau\le 8n-6$, so $h\ge 9n/17$. Ma–Tang say this result "does not appear to have been noted previously" in this context.
- **Where it breaks:** Henning–Yeo is a statement about abstract hypergraphs, and its extremal configurations need not come from real 3-AP hypergraphs. The bound $m\le n-2$ also holds on every induced subset, i.e. the hypergraph is "everywhere sparse", but a global inequality only uses it once. To improve the bound one must either (i) prove a stronger transversal inequality for hypergraphs that are sparse on every subset, or (ii) use the real-line structure. That structure includes the order, the midpoint lying between endpoints, the injective midpoint map, the absence of 4-term APs, and the incidence constraints that come from linear relations between differences.
- **Background reading:** Henning and Yeo's book *Transversals in Linear Uniform Hypergraphs* (Springer, 2020) surveys the relevant transversal bounds and their extremal hypergraphs, which are built from affine and projective planes.

### 4.2 Explicit constructions (upper bounds)
- **Gyárfás–Lehel:** Fibonacci numbers give ratio 3/5. Fibonacci recurrences create many 3-APs of the form $F_{k-2}+F_{k+1}=2F_k$ in a chain-like pattern. **[CORRECTION]** Start at 2, not 1 (see §1).
- **Ma–Tang:** the 14-point set above, ratio 4/7, found by AI-assisted search with refinement (12 points, then 14).
- **Weak-Sidon analogue:** the 2-3-smooth construction $X_i=2^{n-i}3^i$, $Y_i=2^{n-i+1}3^i$ gives a path-like AP hypergraph with independence ratio about 1/2. These sets are not (4,5)-sets, since the APs overlap in two points. That shows linearity is what pushes the (4,5) constant above 1/2.

### 4.3 Community and AI attempts (unrefereed; treat as claims)
- **The-omega-institute "trureturing" issue #9804 (Sep 2026).** This was produced with Codex CLI workers plus separate host checking, and it does **not** claim a solution. Its findings:
  - **A refuted auxiliary inequality.** The proposed bound was $21\tau(K)\le 9|R|+5e_2+12e_1$ for minimal traces after deleting an independent set $D$. It fails on $A=\{0,178,198,218,227,235,272,276,287,317,356,436\}$ with $D=\{287\}$. This set has 10 APs, is a (4,5)-set, and has $h=7$, giving ratio $7/12>4/7$.
  - **A second counterexample:** $\{-336,-168,-44,-24,-4,0,39,44,49,80,102,160\}$.
  - **Amalgams:** gluing scaled copies at a common point (scales $4096^j$) gives $\tau(H(A_k))=4k+1$ and $\alpha=7k$.
  - **Reduction:** a minimal counterexample has no cut vertex in its primal graph.
  - **Still unproved:** the candidate $7\tau(K)\le 3|R|+2e_2+4e_1$.
  - **Other claims:** an arithmetic degree bound $\Delta(G)\le 6$ under certain hypotheses, and a "private-blocker inequality".
  - **Extension result:** adding any two real points to $A_{\rm base}$ (keeping the (4,5) property) gives $h$ exactly 10. So the 14-point block cannot be locally extended to 16 points with $h\le 9$.
  - **Exhaustive state check:** all $3^{14}$ deletion/avoidance states on $A_{\rm base}$ showed no violation of the inequality under test.
- **teorth/erdosproblems wiki (AI contributions).** It lists problem #757 under "AI tools used to perform numerical computation", dated 26 Feb 2026, tool GPT-5.2 Pro, "Computational exploration". This plausibly corresponds to Ma–Tang's AI-assisted search.
- **grandchallenge/MATH-PROGRAMME issue #2028.** An open task: "state the smallest missing lemma". It references a formal-conjectures file for 757.

### 4.4 Approaches that are known not to work
- **Abstract transversal bounds with only "linear + $F_7$-free + $m\le n-2$".** Henning–Yeo is about the limit of this route unless sharper hypergraph theorems exist for "everywhere sparse" linear hypergraphs.
- **A constant cost per avoided point in induction.** Shown to fail by the amalgam family above.
- **Whole midpoint-depth layers and the shortest multiplicative recurrence.** According to issue #9804, these only recover known bounds.

## 5. Computational work

- **Ma–Tang:** exhaustive verification of the 14-point block (all $2^{14}$ subsets checked for the Sidon property; all quadruples checked). Code is on GitHub (QuanyuTang).
- **Issue #9804:** exact enumerations:
  - 495 quadruples for each 12-point example;
  - 8,855 quadruples for the 23-point amalgam;
  - 6,609 two-point extensions of $A_{\rm base}$;
  - $3^{14}=4{,}782{,}969$ deletion/avoidance assignments.
- **Not found:** no OEIS sequence for $f(n)$; the site listed "Possible". Computing $f(n)$ for small $n$ (say $n\le 20$) would be a natural new OEIS entry.
- **Useful search formulation.** Small integer (4,5)-sets can be searched via their AP-hypergraph pattern, then checked for realizability with a linear-programming or integer-programming feasibility check on the difference equalities and inequalities. This is promising because the hypergraph pattern decides $h$.

## 6. Related and neighbouring problems

- **#135 (planar (4,5)-sets).** Erdős asked whether such sets must determine $\gg n^2$ distances, and conjectured they contain $\gg n$ points with all distances distinct.
  - Tao disproved the first part (arXiv:2409.01343): he built sets with $O(n^2/\sqrt{\log n})$ distances by randomizing the Thiele–Dumitrescu parabola construction $\{(x,y): y\equiv x^2 \bmod p\}$. Dumitrescu had earlier classified the 8 forbidden 4-point patterns (Discrete Math. 343 (2020) 111967).
  - On the line, by contrast, #757 shows a linear-size Sidon subset always exists, with ratio at least 9/17. That is consistent with Erdős's stronger conjecture in dimension 1.
- **#530 (Sidon subsets of arbitrary sets).** Here $\ell(N)\asymp N^{1/2}$ (Komlós–Sulyok–Szemerédi). A 2026 improvement to $(\frac{1}{3\sqrt3}+o(1))\sqrt n$ (Riblet, arXiv:2605.03181) uses Freiman 2-isomorphisms into cyclic groups. That compression idea might help realize hypergraph patterns modulo $m$.
- **Sidon subsets of $B_2[k]$ sets** (the problem with $H_k(n)\gg_k n^{2/3}$). Alon–Erdős solved it by random sampling followed by deletion. In #757 the sampling-and-deletion method only gives about 1/2.
- **Sárközy–Sós weak-Sidon problem:** solved exactly by Ma–Tang ($g(n)=\lceil (n+1)/2\rceil$).
- **Erdős–Gyárfás $f(n,4,5)=\frac56n+o(n)$.** Solved with conflict-free hypergraph matchings (Glock–Joos–Kim–Kühn–Lichev; Delcourt–Postle), an example of nibble methods handling a (4,5)-type local condition.
- **Geometric Sidon problems:** distance-Sidon subsets of planar sets $\gg |P|^{1/3}$ (Clemen–Führer–Roche-Newton, arXiv:2606.05841), and 3-AP-free versus isosceles-free sets (arXiv:2606.17487).

## 7. Cross-domain and speculative perspectives

These are labelled as speculative; none has been published as working for #757.

1. **Hypergraph theory with realizability constraints.** Classify the minimal "critical" 3-AP hypergraphs, analogous to how Henning–Yeo characterize equality cases via $AG(2,3)$ and Fano-like pieces. Then show which ones embed in $\mathbb R$. Linear-algebraic realizability is a rank condition: the AP equations $a_i+a_k=2a_j$ must have a solution with distinct values and no extra coincidences. Matroid ideas apply, since the edges give rows of a matrix over $\mathbb Q$.
2. **Fractional and LP relaxations.** Compute the fractional transversal number of realizable hypergraphs, and look for a weighted charging argument (discharging on midpoints) that exploits the injective midpoint map.
3. **Flag algebras and semidefinite programming** for densities of local hypergraph configurations, restricted to the (4,5) family. The answer is a ratio over hereditary families, so the method fits.
4. **SAT, SMT and integer programming** to find $f(n)$ exactly for $n$ up to about 25, and to search for sets with ratio below 4/7 (e.g. 11/20 or 9/16). An extremal set may come from a periodic gluing pattern.
5. **p-adic and multiplicative constructions** (Fibonacci, $2^a3^b$, other linear recurrences). Pisot-number recurrences such as $x^3=x+1$ or tribonacci could produce denser chain-of-AP hypergraphs while staying linear.
   - **[CORRECTION]** Tested on 13 Oct 2026: periodic chain hypergraphs of this kind have independence density ≥ 3/5 in every case checked (dead end D5).
6. **Limit objects** (an ergodic or compactness view). Since $c_*=\inf f(n)/n$, one can ask whether there is an infinite (4,5)-set, or a measure-theoretic limit, that attains $c_*$. One could study translation-invariant AP hypergraphs on lattices $\mathbb Z^d$ projected generically to $\mathbb R$.
7. **Machine-learning-guided search** (AlphaEvolve or FunSearch style) over parametrized families. AI search already produced 7/12 and then 4/7.

## 8. Barriers and heuristics

- The abstract hypergraph properties do not encode realizability. Any proof must either find a new hypergraph theorem for "hereditarily sparse" linear hypergraphs or use arithmetic.
- Upper bounds have improved only via computer search. There is no structural conjecture for the true value. Plausible guesses range from about 0.54 to 4/7, and no expert conjecture was found.
- Amalgam constructions (gluing at a point, or disjoint scaled unions) preserve ratios. So extremal sets are probably "2-connected cores", and one finite core decides the constant.

## 9. Formalization status

- **Lean:** the grandchallenge issue #2028 references `FormalConjectures/ErdosProblems/757.lean` in google-deepmind/formal-conjectures (commit 85f8637). I could not inspect its contents.
  - **[CORRECTION]** The file was read on 13 Oct 2026. It defines `IsAdmissible c` and states `answer(sorry) = sSup {c | IsAdmissible c}`, plus "solved" variants `1/2 < sSup` and `sSup < 3/5`, all with `sorry`. It has not been updated to 9/17 and 4/7.
- **Older site snapshot:** listed "Formalised statement? No". **[CORRECTION]** The current page says Yes.
- **Name collision:** an unrelated "JSP-000757 factorial exponents" Lean repository (zjukop3/erdos757-factorial-exponents) refers to a different catalogue and is **not** this problem.
  - **[CORRECTION]** Erdős #757 is **JSP-000621** in the Justin Sun Prize catalog. Issue #49 there proposes a Lean formalization of $c_*\le4/7$; no proof is attached.
- **Neighbouring problem:** #135 was added to formal-conjectures in PR #6657 (Sept–Oct 2026).

## 10. Open sub-questions that would count as progress

1. Any (4,5)-set with $h/|A|<4/7$; candidate ratios are 13/23, 9/16 and 11/20.
2. The exact values of $f(n)$ for $n\le 20$.
3. Any lower bound above 9/17 that uses arithmetic structure.
4. Prove or refute the candidate $7\tau(K)\le 3|R|+2e_2+4e_1$ from issue #9804.
5. Characterize the hypergraphs that can be realized as 3-AP hypergraphs of (4,5)-sets.
6. Decide whether $c_*$ is attained by some finite $n$, i.e. whether $f(n)=c_*n$ ever holds.

## 11. Annotated bibliography

- **P. Erdős**, *Some old and new problems in various branches of combinatorics*, Discrete Math. 165/166 (1997) 227–231. Original source, p. 231.
- **A. Gyárfás, J. Lehel**, *Linear sets with five distinct differences among any four elements*, JCTB 64 (1995) 108–118, doi:10.1006/jctb.1995.1028. Introduces the hypergraph reduction, the Fibonacci 3/5 construction and the $\frac12+\frac{1}{141\cdot76}$ bound.
- **J. Ma, Q. Tang**, *Largest Sidon subsets in weak Sidon sets*, arXiv:2602.23282 (v2 6 Mar 2026). Current state of the art; includes AI-use declaration; code at github.com/QuanyuTang/ep757-45set-base-block-verification.
- **M. A. Henning, A. Yeo**, *Affine Planes and Transversals in 3-Uniform Linear Hypergraphs*, Graphs Combin. 37 (2021) 867–890, doi:10.1007/s00373-021-02285-x. Proves $17\tau\le5n+3m$.
- **V. Chvátal, C. McDiarmid**, *Small transversals in hypergraphs*, Combinatorica 12 (1992) 19–26; **Zs. Tuza**, Discrete Math. 86 (1990) 117–126. Prove $4\tau\le n+m$.
- **M. A. Henning, A. Yeo**, *Transversals in Linear Uniform Hypergraphs*, Springer 2020. Survey of transversal bounds.
- **A. Sárközy, V. T. Sós**, *On additive representative functions*, The Mathematics of Paul Erdős I (2013) 233–262. Source of the weak-Sidon problem.
- **P. Bennett, R. Cushman, A. Dudek, P. Prałat**, JCTB 169 (2024) 253–297, arXiv:2207.02920. Proves $f(n,4,5)=\frac56n+o(n)$.
- **F. Joos, D. Mubayi**, PAMS 152 (2024) 4537–4550. Reproves the same via hypergraph matchings.
- **T. Tao**, arXiv:2409.01343, plus blog post (3 Sep 2024). Resolves #135.
- **A. Dumitrescu**, Discrete Math. 343 (2020) 111967. Classifies the 8 forbidden 4-point patterns.
- **P. M. Kayll**, *A note on weak Sidon sequences*, Discrete Math. 299 (2005) 141–144.
- **K. O'Bryant**, *A complete annotated bibliography of work related to Sidon sequences*, EJC DS11 (2004).
- **the-omega-institute/trureturing issue #9804** (Sept 2026). Unrefereed computational and partial work.
- **teorth/erdosproblems wiki**, "AI contributions to Erdős problems". Lists GPT-5.2 Pro computational exploration for #757 on 26 Feb 2026.

## 12. Briefing for an AI agent

**State of the art.**
- $9/17\le c_*\le 4/7$, with $c_*=\inf_n f(n)/n$.
- Sidon subsets of (4,5)-sets are exactly the 3-AP-free subsets.
- The AP hypergraph is linear, $F_7$-free, and has at most $|S|-2$ edges on every subset $S$ with $|S|\ge 2$ (distinct midpoints, none at the extremes).

**Do not rediscover:**
- the 1/2 bound via Chvátal–McDiarmid;
- the 9/17 bound via Henning–Yeo;
- subadditivity and gluing;
- the Fibonacci 3/5 construction;
- the forest 2-colouring;
- the refuted $21\tau\le 9|R|+5e_2+12e_1$;
- constant-cost-per-avoided-point inductions.

**Recommended experiments.**
1. **Enumerate realizable hypergraphs.** Generate linear 3-uniform hypergraphs with injective midpoint labels and an order, then solve an integer program for an integer realization, requiring every quadruple to have at least 5 distinct differences. Minimize $\alpha/n$ for $n$ from 15 to 30. **[CORRECTION]** Only the sizes listed in START_HERE §4 can beat 4/7.
2. **Local search on integer sets** in $[0,10^4]$. Use a simulated-annealing objective that combines $\alpha(H)$ with penalties for violating the (4,5) condition. Start from the 14-point block and the 12-point examples. Note that adding two points to $A_{\rm base}$ is already ruled out.
3. **Test transversal inequalities** on realizable hypergraphs, using all induced subhypergraphs, to guess the right weighted charging scheme.
4. **Check Henning–Yeo extremal hypergraphs for realizability.** If none of them can be realized, a stability version of their theorem could push the lower bound above 9/17.

**Pitfalls.**
- Verify the (4,5) condition with exact arithmetic.
- Remember that $c_*$ is an infimum, so one good finite example suffices for an upper bound.
- Keep weak-Sidon and (4,5) results separate.
- Check the literature before claiming novelty; erdosproblems has had several cases where a problem marked open was already solved in an old paper.
