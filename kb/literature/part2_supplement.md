# Erdős Problem #757: Part 2 Supplement

*Compiled 13 October 2026. Read alongside Part 1, the first literature review. This file adds new areas, corrects Part 1 where needed, and records new exact computations. The companion script `e757/core.py` reproduces every computation marked **[computed here]**.*

Labels used throughout:
- **[published]**: refereed paper or arXiv preprint.
- **[community]**: unrefereed GitHub or forum material.
- **[computed here]**: exact computation run for this supplement. These are checks, not theorems from the literature.
- **[speculative]**: idea or heuristic with no proof behind it.

---

## 0. What is new in Part 2

1. **Primary sources read in full.**
   - The Ma-Tang proof chain, lemma by lemma (§2).
   - The live erdosproblems.com page.
   - The actual DeepMind Lean file.
   - The JSP prize-catalog entry.
2. **The hypergraph transversal toolbox around the 9/17 bound** (§3), including:
   - what the extremal hypergraphs are;
   - a published bound for maximum degree 2 that already gives 5/9;
   - the "deficiency" proof technique an agent could imitate.
3. **New structural facts about every known record set** (§4) [computed here]:
   - all records are *midpoint-saturated* (every interior point is a midpoint);
   - all records are *affinely rigid* (their AP hypergraph determines the set up to $x\mapsto qx+t$);
   - $F_7$ fails to be realizable over $\mathbb Q$ for all 243 midpoint labelings.

   Together these turn the upper-bound search into a finite combinatorial search over labeled hypergraphs (§7).
4. **Freiman-isomorphism invariance**, and why $F_7$ is excluded: it is a characteristic-3 object (§4.1).
5. **Variant problems** that make good stepping stones (§5), and the AI and computer-search methods relevant to each direction (§6).

---

## 1. Corrections and updates to Part 1

**erdosproblems.com/757 is up to date.** Part 1 could not load the live page. The forum thread page has now been read, and it shows:
- status OPEN, with the note that the problem "cannot be resolved with a finite computation";
- Ma and Tang's bounds $\frac{9}{17}\le c\le \frac47$;
- "Formalised statement? Yes";
- last edit 10 April 2026.

Quanyu Tang's comment on the thread says the paper made exploratory use of ChatGPT-5.2 Pro, and that the human authors checked all arguments. There are no proof claims in the comments.
([page](https://www.erdosproblems.com/forum/thread/757))

**The Lean file states only the 1995 bounds.** `FormalConjectures/ErdosProblems/757.lean` in google-deepmind/formal-conjectures contains:
- `IsAdmissible c`: every finite $A\subset\mathbb R$ whose 4-subsets $B$ have `11 ≤ (B - B).ncard` contains a Sidon $S$ with `c * A.ncard ≤ S.ncard`;
- the main theorem `answer(sorry) = sSup {c | IsAdmissible c}`;
- two "solved" variants, `1/2 < sSup` and `sSup < 3/5`, both with `sorry` proofs.

The file has not been updated to 9/17 and 4/7. Note that `sSup < 3/5` is a strict inequality, which Gyárfás-Lehel's $3n/5+1$ does not give by itself. It is true now because of 4/7.
([file](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/757.lean))

**The Fibonacci example needs care** [computed here].
- The site says the 3/5 example is "the set of the first $n$ Fibonacci numbers". Taken literally, that set contains $\{1,2,3,5\}$, which has only four distinct distances ($1,2,3,4$). So it is **not** a (4,5)-set, and $\{1,2,3,5\}$ is its only violating quadruple among the first 20 Fibonacci numbers.
- Dropping the 1, i.e. $\{2,3,5,8,\dots\}$, gives (4,5)-sets with ratios $7/10,\ 13/20,\ 19/30$ for $n=10,20,30$. That matches the Gyárfás-Lehel bound $3n/5+1$.
- Treat the paper's phrase "based on Fibonacci numbers" as the precise source.

**Prize-catalog numbering.**
- Erdős #757 appears in the Justin Sun Prize catalog as **JSP-000621**. Part 1 correctly flagged "JSP-000757" as unrelated; the catalog uses its own numbering.
- Issue #49 in TheJustinSunPrize/awards (16 Sep 2026, now closed) proposes a Lean formalization of $c_*\le 4/7$. No Lean proof is attached. It reports that a LeanGenius file `Erdos757Problem.lean` contains only definitions.
- That issue's exact enumeration found **143 Sidon subsets of size 8** in $A_{\rm base}$, and none larger. This matches the independent computation in §4.
([issue](https://github.com/TheJustinSunPrize/awards/issues/49))

**No follow-up literature.** As of 13 Oct 2026, searches found no paper after Ma-Tang that improves either bound. Ma-Tang's latest version is v2 (6 Mar 2026).

---

## 2. The complete published proof chain (Ma-Tang, arXiv:2602.23282v2)

The agent should know exactly which hypothesis each step uses, since any improvement must strengthen one of them.

| Step | Statement | Hypothesis actually used |
|---|---|---|
| Prop 2.1 | Sidon ⇒ (4,5) | none |
| Prop 2.2 | (4,5) ⇒ weak Sidon. If $a_1+a_4=a_2+a_3$ then $a_4-a_3=a_2-a_1$ and $a_4-a_2=a_3-a_1$, leaving ≤4 distances. | (4,5) |
| Lemma 2.3 | For weak Sidon $A$: $S\subseteq A$ is Sidon iff $S$ is 3-AP-free. So $h(A)=\alpha(H(A))$. | weak Sidon |
| Lemma 2.4 | The midpoint map is injective and avoids $\min A$ and $\max A$, so $m\le n-2$. This holds for every subset too. | weak Sidon + **order of ℝ** (only for the "−2") |
| Lemma 2.5 | $H(A)$ is linear. Two APs sharing $u<v$ have third points among $u-d,\frac{u+v}2,v+d$; every combination produces ≤4 distances. | (4,5) |
| Lemma 5.2 (Gyárfás-Lehel Prop 2.6) | $H(A)$ is $F_7$-free, where $F_7=\{012,034,056,135,246\}$. | (4,5), via an arithmetic argument |
| Thm 5.3 (Henning-Yeo 2021, Thm 7) | linear, 3-uniform, $F_7$-free ⇒ $17\tau\le 5n+3m$ | abstract hypergraph only |
| Conclusion | $17\tau\le 5n+3(n-2)\le 8n$, so $h\ge \frac{9}{17}n$ | |
| Lemma 3.6 (gluing) | $C=A\cup(qB+t)$ with $q\notin\{(a-a')/(b-b')\}$ and $t$ large is (4,5) with $h(C)\le h(A)+h(B)$. So $f$ is subadditive and $c_*=\inf f(n)/n$. | |

Three remarks:

1. **The "−2" in $m\le n-2$ does not matter asymptotically.** Only *injectivity* of the midpoint map matters for the constant ($m\le n$ gives the same 9/17). That injectivity holds in any abelian group of odd order without the extra relations. So the 9/17 argument barely uses the real line: it uses linearity, $F_7$-freeness, and $m\lesssim n$, applied **once, globally**.
2. **The inequality $e(S)\le |S|-2$ holds on every induced subset** but is never used hereditarily. This is the most obvious unused hypothesis.
3. **The weak-Sidon extremal construction.** $A_{2n+1}=\{2^{n-i}3^i\}\cup\{2^{n-i+1}3^i\}$ has the path-like AP hypergraph $\{X_i,X_{i+1},Y_i\},\{X_i,Y_i,Y_{i+1}\}$, in which consecutive edges overlap in two points. That is exactly what (4,5) forbids, and it explains why $\gamma_*=1/2$ but $c_*>1/2$. Ma-Tang prove $\alpha=n+1$ by splitting $\{i:X_i\in T\}$ into maximal intervals, each of which forces as many absent $Y$'s as its length. That kind of charging argument could be adapted.

---

## 3. Hypergraph transversal theory around the bound

### 3.1 The landscape

For 3-uniform $H$ with $n$ vertices and $m$ edges, $\alpha=n-\tau$. The last column below plugs in $m\le n$, which is asymptotically what (4,5)-sets satisfy.

| Bound | Class | Extremal / equality cases | Implied $c_*\ge$ |
|---|---|---|---|
| $4\tau\le n+m$ (Tuza 1990; Chvátal-McDiarmid 1992) | all 3-uniform | For linear connected $H$: equality iff $H=E_3$ (single edge), $F_7$ or $F_8$ (Henning-Yeo; see Thm 2 of arXiv:1802.01825) | 1/2 |
| $6\tau\le 2n+m$ (Chvátal-McDiarmid) | all 3-uniform | linear cases characterized by Henning-Yeo (JGT 2008; DM 2013) | 1/2 |
| $17\tau\le 5n+3m$ (Henning-Yeo, Graphs Combin. 37 (2021) 867–890) | linear, no $F_7$ | not checked (paywalled) | **9/17 ≈ 0.5294** |
| $18\tau\le 4n+4m+2$ (Henning-Yeo, EJC 24(2) P2.50, 2017, $k=3$ case) | connected, linear, **max degree 2** | infinite tight families | **5/9 ≈ 0.5556** if Δ≤2 |

**Where the affine-plane pieces come from.**
- $F_9$ is the affine plane AG(2,3): 9 points, 12 lines, $\tau=5$.
- $F_8=F_9$ minus one point ($\tau=4$), and $F_7=F_9$ minus two points ($\tau=3$).
- The only linear configurations achieving equality in $4\tau\le n+m$ (other than a single edge) contain $F_7$. That is why $F_7$-freeness buys an improvement.

**Consequence of the max-degree-2 bound** (derivation done here; the inputs are [published]).
- For a (4,5)-set whose AP hypergraph has maximum degree at most 2, apply $18\tau\le 4n+4m+2$ to each component, using $m_C\le n_C-2$. This gives $\tau\le(4n-3)/9$, so $h(A)\ge (5n+3)/9$.
- **So any (4,5)-set with ratio below 5/9 must contain points lying on at least 3 APs.**
- $A_{\rm base}$ has degree sequence: one vertex of degree 4 (the point 0), six of degree 3, seven of degree 2 [computed here].
- **Suggested lower-bound route:** prove a weighted inequality that interpolates between the Δ≤2 bound (5/9) and the general $F_7$-free bound (9/17), charging degree-3+ vertices.

**Graph dictionary (total domination).** For a graph $G$, the *open-neighbourhood hypergraph* has one edge $N(v)$ for each vertex $v$, and its transversal number equals the total domination number $\gamma_t(G)$. It is linear exactly when $G$ has no 4-cycle.
- Henning-Yeo's 8/17 theorem has the graph form: min degree ≥3, $C_4$-free, and avoiding one specific 12-vertex graph ⇒ $\gamma_t\le \tfrac{8}{17}n$.
- So the total-domination literature on cubic graphs of large girth is a source of transversal techniques and examples. Caveat: AP hypergraphs are not regular, and not every hypergraph is an open-neighbourhood hypergraph.

### 3.2 The "deficiency" technique: a template for a stronger, class-specific inequality

In arXiv:1802.01825 (Transversals in uniform linear hypergraphs), Henning and Yeo prove $5\tau\le n+m$ for linear 4-uniform hypergraphs.

**How the proof works:**
1. Fix a finite list of "special" hypergraphs (fifteen of them) with large $\tau$, whose relevant properties were verified by computer.
2. For a family $X$ of disjoint special subhypergraphs, define a deficiency
   $$\operatorname{def}_H(X)=\sum_{F\in X} w(F)-13\,|E^*(X)|,$$
   where $E^*(X)$ is the set of edges touching $X$ from outside.
3. Prove the strengthened statement $45\tau\le 6n+13m+\operatorname{def}(H)$ by taking a minimal counterexample (minimizing $n+m$).
4. Use Hall's theorem on the bipartite graph between special pieces and outside edges to show transversals can be extended. Then run a long case analysis.

**Why this matters for #757** [speculative but concrete]:
- The natural next theorem has the shape $a\tau\le bn+cm$ (or with hereditary sparsity), restricted to **realizable** AP hypergraphs.
- Its extremal pieces would be small realizable configurations of high transversal number, such as the 12- and 14-point records.
- A computer can (i) enumerate the small realizable "special" configurations, (ii) verify their transversal-extension properties (the analogues of Observation 1(g)–(p) in that paper), and (iii) leave a human-checkable discharging or Hall argument.
- This is the most credible route to a lower bound above 9/17. The omega-institute issue (§3.4) tried an informal version and found that counterexamples appear as soon as the inequality is not tight on the right pieces.

### 3.3 Other transversal results worth knowing

- **Henning-Yeo, *Lower bounds on Tuza constants for transversals in linear uniform hypergraphs*,** DAM 304 (2021) 12–22. For all $0<a<1$, $q_k\ge a(1-a)^k/((1-a)^k+a\ln(e/a))$. These are general lower bounds on the best constants in $\tau\le q_k(n+m)$.
- **Dorfling-Henning, EJC (Eur. J. Combin.) 36 (2014) 231–236.** For linear hypergraphs with max degree ≤2, $(k+1)\tau\le n+m$, with the equality cases characterized.
- **Henning-Yeo, *Transversals in Linear Uniform Hypergraphs*** (Springer, 2020). A book-length survey with chapters on affine and projective planes, the Tuza constant, and the cap-set connection.
- **Random restriction of projective planes** (1802.01825, Thm 4). Taking random $k$-subsets of the lines of a projective plane gives linear hypergraphs with $\tau>(n+m)/(k+1)$ for large $k$. This is not directly relevant at $k=3$, but it is a reminder that "geometric" objects are where extremal transversal behaviour lives.

### 3.4 The omega-institute issue in full detail [community]

the-omega-institute/trureturing #9804 (opened 24 Sep 2026; Codex CLI workers with host checking).

**Setup.** Take $D\subseteq A$ independent (the points "avoided"), let $R=A\setminus D$, and let $K$ be the clutter of inclusion-minimal nonempty traces $e\setminus D$. Write $e_1,e_2$ for its numbers of 1- and 2-element traces.

**Refuted:** $21\tau(K)\le 9|R|+5e_2+12e_1$.
- First counterexample: $A=\{0,178,198,218,227,235,272,276,287,317,356,436\}$ with $D=\{287\}$. Its AP list is
  $$\{0,178,356\},\{0,218,436\},\{178,198,218\},\{178,227,276\},\{198,235,272\},\{198,317,436\},$$
  $$\{218,287,356\},\{227,272,317\},\{235,276,317\},\{276,356,436\}.$$
  This gives $|R|=11$, $e_2=1$ and $\tau(K)=5$, so $105>104$.
- A second counterexample: $\{-336,-168,-44,-24,-4,0,39,44,49,80,102,160\}$ with $D=\{-336\}$.
  - The issue says its AP incidence pattern is isomorphic to the first example's.
  - The two sets are **not** affinely equivalent [computed here]. Same pattern, different midpoint and order data.
  - Avoiding its vertex 80 gives a mixed equality child with 10 active vertices, 3 pairs, 7 triples and $\tau=5$.

**Amalgams refute any "constant cost per avoided point" induction.**
- Translate the second set to $B=\{0,168,292,312,332,336,375,380,385,416,438,496\}$ and let $A_k=\bigcup_j 4096^jB$, glued at 0.
- Then $\tau(H(A_k))=4k+1$, $\alpha=7k$, and the deficit grows linearly in $k$ with $|D|=1$.

**Valid reduction:** a minimal counterexample has no cut vertex in its primal graph. This uses a one-vertex amalgam argument that holds for any $c\in(0,1)$.

**Still open:** the candidate $7\tau(K)\le 3|R|+2e_2+4e_1$.
- It is tight on the amalgam traces.
- An exact check of all deletion/avoidance states in both 12-point sets found no violation. The issue notes this is one isomorphism class of evidence.
- A minimal counterexample would have a pair graph that is a matching, with local types $(d_2,d_3)\in\{(0,2),(1,1),(1,2)\}$.

**Other retained claims (unverified here):**
- a private-blocker inequality $t-s+\sum_x\binom{d_G(x)}{2}\le i-2$;
- an arithmetic degree bound $\Delta(G)\le 6$ under maximum-independent-set hypotheses;
- one-for-two exchanges are blocked by a real 10-point example.

**Extension result.** For any two real points $x,y$ with $A_{\rm base}\cup\{x,y\}$ a (4,5)-set, the largest Sidon subset has size exactly 10.
- The issue checked this with a certificate covering 124 compatible triples, 6,484 pairs and 6,609 extensions.
- So $A_{\rm base}$ cannot be extended locally to beat 4/7 at 16 points.

---

## 4. The arithmetic side: new structural facts [computed here]

### 4.1 Freiman invariance, and why $F_7$ is a characteristic-3 object

**Everything in the problem is a "2-relation".**
- $|x-y|=|z-w|$ holds iff $x+w=y+z$ or $x+z=y+w$.
- Sidon, weak Sidon, the 3-AP relation $a+c=2b$, and the (4,5) condition are all statements about relations $a_1+a_2=a_3+a_4$ (with repeats allowed).

**Consequence.** The whole problem is invariant under **Freiman 2-isomorphism**, i.e. bijections that preserve exactly these relations.
- Every finite subset of a torsion-free abelian group (such as $\mathbb Z^d$ or $\mathbb Q^d$) is Freiman-isomorphic to a set of integers.
- **So the agent may build constructions in $\mathbb Z^d$ (lattice-like configurations) and project them generically.** $c_*$ is the same for every torsion-free group.

**Why torsion is different: $F_7$ lives naturally in characteristic 3.**
- In $\mathbb F_3^2$, every line $\{p,p+d,p+2d\}$ is a 3-AP *with every point a midpoint*, since $3d=0$.
- So the AP hypergraph of $\mathbb F_3^2$ is exactly AG(2,3) $=F_9$. That gives $m=12>n$, and midpoint injectivity fails.
- The extremal hypergraphs for Chvátal-McDiarmid ($F_7,F_8$) are therefore characteristic-3 AP hypergraphs. The real line rules them out because midpoints are injective and the (4,5) arithmetic holds.

**Exact confirmation.** For all $3^5=243$ ways of choosing a midpoint in each edge of $F_7$, the AP equations force a failure over $\mathbb Q$ (generic point of the solution space):

| Outcome | Labelings |
|---|---|
| two points forced equal | 204 |
| an extra AP forced, and the (4,5) condition then fails | 24 |
| (4,5) condition violated (with a 3-dimensional solution space) | 15 |

This independently reproduces Gyárfás-Lehel Prop 2.6 by linear algebra. A quick mod-$p$ search (exhaustive or sampled) found no 7-point (4,5)-set in $\mathbb Z_p$ with AP hypergraph exactly $F_7$ for $5\le p\le 37$. That is evidence, not proof, that the obstruction is characteristic-free except at 3.

**Takeaway for the agent:** "forced relation" linear algebra is a complete, mechanical test of whether a labeled hypergraph is realizable (see `realize()`). Any finite list of forbidden configurations, analogous to $F_7$, can be generated automatically.

### 4.2 Every known record set is midpoint-saturated and affinely rigid

| Set | $n$ | $m$ | $n-2$ | $h$ | ratio | max deg | HY slack $5n+3m-17\tau$ | rank of AP system | solution dim |
|---|---|---|---|---|---|---|---|---|---|
| $A_{\rm base}$ (Ma-Tang) | 14 | 12 | 12 | 8 | 0.5714 | 4 | 4 | 12 | **2** |
| 12-point #1 (omega) | 12 | 10 | 10 | 7 | 0.5833 | 3 | 5 | 10 | **2** |
| 12-point #2 (omega) | 12 | 10 | 10 | 7 | 0.5833 | 3 | 5 | 10 | **2** |
| $\{F_3,\dots,F_{22}\}$ (Fibonacci) | 20 | 17 | 18 | 13 | 0.65 | 3 | (n/a) | 17 | 3 |

**Midpoint saturation.**
- In all three record sets, $m=n-2$: **every point except the two extremes is the midpoint of an AP.**
- This is the maximum Lemma 2.4 allows. Empirically, low-ratio sets push the midpoint budget to its limit [speculative as a general principle].

**Affine rigidity.**
- In all three record sets the $m$ AP equations have full rank $n-2$, so their solution space is 2-dimensional: just translations and dilations.
- **Therefore the labeled AP hypergraph (edges plus the choice of midpoints) determines the set up to $x\mapsto qx+t$.**
- `realize()` rebuilds an affine copy of $A_{\rm base}$ from its labeled hypergraph alone.

**Other facts about $A_{\rm base}$:**
- Its primal graph is connected with no cut vertex, consistent with the omega reduction.
- It has 143 maximum Sidon subsets.
- 13 of its subsets $S$ with $|S|\ge3$ satisfy $e(S)=|S|-2$ exactly, including the whole set.

**Henning-Yeo slack.**
- For $A_{\rm base}$, $17\tau=102$ versus $5n+3m=106$. For the 12-point sets the slack is 5.
- **Hypergraphs that attain 9/17 (zero slack with $m\approx n$) would need $\tau\approx 8n/17$.** Whether any linear $F_7$-free hypergraph with $m\le n-2$ attains this, and whether any such hypergraph is realizable, is the key open question on the lower-bound side (§5, item 1).

### 4.3 Consequence: upper bounds become a finite combinatorial search

Midpoint saturation plus rigidity mean a candidate record with $n$ points can be specified as:
- a choice of two "extreme" vertices;
- for each of the other $n-2$ vertices, a pair of endpoints for the AP it is the midpoint of.

The set is then determined by linear algebra, and one only checks order, distinctness, absence of extra APs, and (4,5). Search pruning comes from necessary conditions that are cheap to check before solving:
- linearity;
- $F_7$-freeness;
- hereditary $e(S)\le|S|-2$;
- the forced-relation test on partial labelings.

§7 sketches a full pipeline.

---

## 5. Variant and neighbouring problems as stepping stones

1. **Pure hypergraph constant (sharpest sub-question).** Let $c_{\rm hyp}=\inf \alpha/n$ over 3-uniform linear $F_7$-free hypergraphs with an injective midpoint labeling and $e(S)\le|S|-2$ for every $S$.
   - Then $9/17\le c_{\rm hyp}\le c_*$.
   - If $c_{\rm hyp}=9/17$, which needs a matching construction, then **arithmetic structure must be used** to improve the lower bound. If $c_{\rm hyp}>9/17$, there is room for a purely combinatorial improvement.
   - Either answer is publishable progress, and small cases can be computed by SAT/ILP.
2. **The problem over other groups.** Define $c_*(G)$ for (4,5)-sets in an abelian group $G$ via 2-relations.
   - $c_*(\mathbb Z^d)=c_*$ by §4.1.
   - $\mathbb Z_p$ with $p$ large, $\mathbb F_p^k$, and $\mathbb F_3^k$ (where midpoints fail) are natural variants. Results there show which hypotheses really matter.
3. **The hereditary-sparsity version of Henning-Yeo.** Find the best $a,b$ with $\tau\le an+b\cdot m$ for linear $F_7$-free hypergraphs with $e(S)\le |S|-2$ for all $S$. A sharper "everywhere sparse" transversal theorem would improve 9/17 directly.
4. **Degree-split bounds.** Interpolate between the Δ≤2 bound (5/9, §3.1) and the general bound, e.g. $\tau\le an+b\,m+c\,|\{v:d(v)\ge3\}|$.
5. **Neighbouring Erdős problems on erdosproblems.com (Sidon tag):**
   - **#530:** largest Sidon subset of $N$ arbitrary reals, $\asymp N^{1/2}$. Riblet (arXiv:2605.03181) improves the constant to $(\frac{1}{3\sqrt3}+o(1))\sqrt N$ using Freiman isomorphisms into cyclic groups.
   - **#772:** Sidon subsets of $B_2[k]$ sets, $\gg n^{2/3}$ (Alon-Erdős). The method is random sampling followed by deletion, which gives only about 1/2 here.
   - **#863/#864:** sets with at most one repeated sum.
   - **#840:** quasi-Sidon sets.
   - **#707:** a Sidon-extension conjecture, disproved; see arXiv:2510.19804 (human-assisted proof) and arXiv:2604.25214 (size-4 counterexamples). These are useful case studies in AI-plus-human work on Sidon problems.
   - **#135:** the planar (4,5) problem, solved by Tao (arXiv:2409.01343).
6. **Independence numbers of AP hypergraphs in cyclic groups.** Liber, *On the Independence Numbers of the Cyclic Van der Waerden Hypergraphs* (arXiv:2509.07926), constructs large $k$-AP-free subsets of $\mathbb Z_{mk}$ and bounds the related chromatic numbers. It is a different regime (all APs present), but it is the closest literature on independence in AP hypergraphs as such.
7. **Anti-Ramsey context.** The (4,5) condition comes from the Erdős-Gyárfás function $f(n,4,5)=\frac56n+o(n)$ (Bennett-Cushman-Dudek-Prałat; Joos-Mubayi). There, conflict-free hypergraph matchings handle a "(4,5)-type" local condition. This is a possible source of random-greedy constructions for large (4,5)-sets with structured AP hypergraphs [speculative].

---

## 6. AI and computational methods, matched to each direction

| Method | Reference | Fit for #757 |
|---|---|---|
| LLM-guided exploration plus exact verification | Ma-Tang AI declaration (GPT-5.2 Pro found 12 points, then 14) | Already produced the current upper bound. Exploit its rigidity: search over labeled hypergraphs, not raw integers. |
| FunSearch (program search with LLMs) | Romera-Paredes et al., *Nature* 625 (2024) | Evolves *programs* that generate set families. Good for finding infinite families such as recurrence-based ones. |
| AlphaEvolve | Georgiev, Gómez-Serrano, Tao, Wagner, *Mathematical exploration and discovery at scale*, arXiv:2511.02864 | Large-scale evolutionary code search on many extremal problems. A natural fit for "minimize $h(A)/|A|$ over (4,5)-sets". |
| PatternBoost | Charton, Ellenberg, Wagner, Williamson, arXiv:2411.00566 | Alternates a transformer with local search. Suits a discrete encoding (labeled hypergraphs). |
| Cross-entropy RL constructions | Wagner, *Constructions in combinatorics via neural networks*, arXiv:2104.14516 | A simple baseline for the same search. |
| LP-based refutation of conjectures | *Refuting conjectures in extremal combinatorics via linear programming*, arXiv:1903.05495 | For testing candidate weighted inequalities (§3.2) on enumerated realizable configurations. |
| Codex-style parallel workers plus exact host checks | the omega-institute issue #9804 | Found counterexamples to proposed auxiliary inequalities. Useful as a "falsification engine" for lemma candidates. |
| SAT/ILP for $\alpha$ and for $c_{\rm hyp}$ | standard | Gives exact $f(n)$ for small $n$ and exact $c_{\rm hyp}$ for small $n$ (§5.1). |
| Lean formalization | formal-conjectures 757.lean; JSP issue #49 | Final certification. The 4/7 bound is a finite check plus the gluing lemma. |

Also relevant: *Early science acceleration experiments with GPT-5* (arXiv:2511.16072), and the teorth/erdosproblems wiki page on AI contributions, which lists #757 under computational exploration.

---

## 7. Additions to the agent briefing

### 7.1 Ready-made tools
`e757/core.py` provides:
- `ap_edges`, `is_45_set`, `is_weak_sidon`, `alpha` (exact $h(A)$);
- `ap_rank_report` (the rigidity test);
- `realize`, which turns a labeled hypergraph into an integer (4,5)-set or returns the forced obstruction.

Running the file reproduces every [computed here] number above.

### 7.2 Upper-bound pipeline (hypergraph-first search)
1. **Enumerate labeled hypergraphs.** Work on $n$ vertices with two extremes and $n-2$ midpoint vertices, each midpoint assigned an endpoint pair. Prune by linearity, $F_7$-freeness and hereditary $e(S)\le|S|-2$. Use symmetry breaking, e.g. canonical forms via nauty, or SAT with symmetry predicates.
2. **Bound $\alpha$ before realizing.** Compute $\alpha$ first, which is cheap for $n\le 30$. Keep only candidates with $\alpha/n<4/7$. Targets: $13/23,\ 9/16,\ 11/20,\ 10/18$.
3. **Realize.** Call `realize()`. A 2-dimensional solution space means a unique candidate up to affinity. Higher-dimensional spaces need a generic point plus a check that no forbidden relation is forced.
4. **Search well.** Use local moves on labelings (rewire one midpoint's endpoints) inside simulated annealing, PatternBoost or AlphaEvolve-style loops.
5. **Seed** the search with the three record patterns and with gluings of them, e.g. identifying vertices of two copies. A single-vertex amalgam keeps the ratio above the parts, so look for 2-vertex or edge-sharing gluings.

### 7.3 Lower-bound program
1. Compute $c_{\rm hyp}$ for small $n$ (§5.1) by ILP. Compare it with realizable minima to see whether arithmetic is needed.
2. Look for linear $F_7$-free hypergraphs with $m\le n$ near the $17\tau=5n+3m$ bound, then test them with `realize()`.
   - If **none** are realizable, prove a stability version: "near-extremal for Henning-Yeo ⇒ contains a forbidden configuration".
   - Use `realize()` to generate the list of forbidden configurations up to 9–10 vertices, the analogues of $F_7$.
3. Imitate the deficiency method of §3.2, with special pieces taken from enumerated realizable high-$\tau$ configurations. Test candidate inequalities against all enumerated configurations by LP before trying to prove them. The omega issue shows how quickly untested inequalities fail.
4. Use the degree split: Δ≤2 already gives 5/9. Concentrate the charging on vertices of degree ≥3.

### 7.4 Pitfalls (beyond Part 1)
- The literal "first $n$ Fibonacci numbers" are not a (4,5)-set. Start from 2.
- The Lean file still states $1/2<c<3/5$. Do not mistake it for the current state of the art.
- Erdős #757 = JSP-000621. Other "757" repositories may concern different catalogs.
- Henning-Yeo's equality cases for $17\tau\le5n+3m$ were not checked here (paywalled). Obtain the paper before assuming tightness or non-tightness.
- Lemma 2.4's "−2" uses the order of ℝ. Over other groups only $m\le n$ holds. That is the same asymptotically, but it matters for exact small cases.
- Generic-point realizability is exact for "forced or not" over $\mathbb Q$ once the relation is checked at a random point. Still confirm any final construction with `is_45_set` and `alpha`.

---

## Sources

- Ma, Tang, *Largest Sidon subsets in weak Sidon sets*, [arXiv:2602.23282v2](https://arxiv.org/abs/2602.23282v2)
- [erdosproblems.com forum thread #757](https://www.erdosproblems.com/forum/thread/757) and [Sidon-sets tag page](https://www.erdosproblems.com/tags/sidon%20sets)
- [formal-conjectures 757.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/757.lean)
- [TheJustinSunPrize/awards issue #49 (JSP-000621)](https://github.com/TheJustinSunPrize/awards/issues/49)
- [the-omega-institute/trureturing issue #9804](https://github.com/the-omega-institute/trureturing/issues/9804)
- Henning, Yeo, *Affine Planes and Transversals in 3-Uniform Linear Hypergraphs*, [Graphs Combin. 37 (2021)](https://link.springer.com/article/10.1007/s00373-021-02285-x); [UJ abstract](https://pure.uj.ac.za/en/publications/affine-planes-and-transversals-in-3-uniform-linear-hypergraphs/)
- Henning, Yeo, *Transversals in Uniform Linear Hypergraphs*, [arXiv:1802.01825](https://arxiv.org/abs/1802.01825)
- Henning, Yeo, *Transversals and Independence in Linear Hypergraphs with Maximum Degree Two*, [EJC 24(2) P2.50](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v24i2p50)
- Dorfling, Henning, [Eur. J. Combin. 36 (2014)](https://pure.uj.ac.za/en/publications/linear-hypergraphs-with-large-transversal-number-and-maximum-degr/)
- Henning, Yeo, *Lower bounds on Tuza constants...*, [DAM 304 (2021)](https://digitalscience.forskningsportal.dk/display/pub.1139964153)
- Henning, Yeo, [*Transversals in Linear Uniform Hypergraphs* (Springer 2020)](https://link.springer.com/978-3-030-46561-2)
- Liber, [arXiv:2509.07926](https://arxiv.org/abs/2509.07926)
- Riblet, [arXiv:2605.03181](https://arxiv.org/pdf/2605.03181)
- [arXiv:2510.19804](https://arxiv.org/html/2510.19804); [arXiv:2604.25214](https://arxiv.org/pdf/2604.25214)
- [AlphaEvolve, arXiv:2511.02864](https://arxiv.org/pdf/2511.02864); [PatternBoost, arXiv:2411.00566](https://arxiv.org/pdf/2411.00566); [LP refutation, arXiv:1903.05495](https://arxiv.org/pdf/1903.05495); [GPT-5 science, arXiv:2511.16072](https://arxiv.org/pdf/2511.16072)
