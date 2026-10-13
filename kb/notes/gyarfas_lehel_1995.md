# Gyárfás–Lehel, *Linear sets with five distinct differences among any four elements*, JCTB 64 (1995) 108–118 [published]

- **Citation:** A. Gyárfás, J. Lehel, J. Combin. Theory Ser. B 64 (1995) 108–118, doi:10.1006/jctb.1995.1028 (received 3 Dec 1993).
- **Link:** author scan https://users.renyi.hu/~gyarfas/Cikkek/69_linset5.pdf (local copy `kb/literature/papers/gyarfas_lehel_1995.pdf`).
- **Read from:** the local copy, in full, 11 pages. It is a **scanned image PDF with no text layer** (`pdftotext` gives nothing). The page images were read visually (renders in `experiments/20261013-2257-paper-digest/glh-*.png`). So every statement below is read off the actual paper, not from secondary sources. Statements marked [verified-here] are my own checks.
- **Paper length:** 11 pages: Intro and Theorems A, B (pp. 108–110); §2 properties of (4,5)-sets (pp. 110–113); §3 transversals (pp. 113–117); one corollary and the references (p. 118). There are no concluding remarks and no open-problem section.

## 0. What the paper does NOT contain
- **No forbidden configuration other than $H_0$ (= our $F_7$).** The only structural facts about AP hypergraphs are: 3-uniform, at most $n-2$ edges, distinct midpoints, linear (two edges share at most one vertex), $H_0$-free, 2-colourable. [published]
- **No exact small values, no lower bound better than $(1/2+\varepsilon)n$, and no stated open problem.** The only "remarks" are the notes after Theorems A and B (extremal structures for the Turán-type theorem, and $\varepsilon\le 1/26$).
- Sidon's statement: a $(p,q)$-set has every $p$-subset spanning at least $q$ distinct differences; Sidon sets = $(4,6)$-sets. Erdős and Sós "observed that any $(4,5)$-set of $n$ elements contains a $cn$-element Sidon set and asked about the maximum of $c$" (the paper gives no value of this first $c$; the $1/2$ is Prop 2.1 below).

## 1. Definitions (p. 108–109) [published]
- $(p,q)$-set: every $p$ elements determine $\ge q$ distinct differences. $g(n)$ = largest number such that every $n$-element $(4,5)$-set contains a Sidon set of size $g(n)$ (our $f(n)$).
- **Erdős–Sós observation** (stated without proof, p. 109): if $r_i-r_j=r_j-r_k>0$ then $r_j$ is the midpoint of the AP; (i) the elements involved in repeated differences are exactly APs; (ii) the midpoints of different 3-APs are different; (iii) two 3-APs have at most one common element.
- **A.P.-hypergraph** $H=(R,E)$ of $R$: vertex set $R$, edges the 3-APs. Hypergraph properties: 3-uniform; $\le n-2$ edges; distinct edges share at most one vertex.
- "Partial hypergraph" = a sub-hypergraph obtained by deleting vertices and/or edges (not necessarily induced). $\alpha(H)$ = independence number; Sidon sets of $R$ = independent sets of $H$; $\tau(H)=|R|-\alpha(H)$.

## 2. Main statements

**Theorem A (p. 109).** $H$ a 3-uniform hypergraph with $n$ vertices and at most $n$ edges $\Rightarrow\tau(H)\le n/2$. If moreover no two edges meet in two vertices and $H$ contains no $H_0$ (Fig. 1) then $\tau(H)\le(\tfrac12-\varepsilon)n$ for some constant $\varepsilon>0$. [published]

**Theorem B (p. 110; proof omitted, "in a preliminary version").** $H$ connected, 3-uniform, $n$ vertices, $\le n$ edges: $\tau(H)\le n/2$, with equality iff $H=J(n)$ or $H=L(8)$. [published]
- $J(n)$ ($n\ge4$ even): vertex set $\mathbb Z_n$, edges $\{i,i+1,i+n/2\}$, $i=0,\dots,n-1$.
- $L(n)$ ($n\ge3$): vertex set $\mathbb Z_n$, edges $\{i,i+1,i+3\}$, $i\in\mathbb Z_n$.
- Remark: $L(8)$ (and disjoint copies) is extremal and has **no two edges meeting in two vertices** (i.e. is linear), so excluding $H_0$ is crucial for improving $n/2$. [published]
- Remark: $\varepsilon\le1/26$ because disjoint copies of $L(13)$ have $\tau=6=(\tfrac12-\tfrac1{26})\cdot13$. [published]
- [verified-here] $L(8)\cong F_8=$ AG(2,3) minus a point (so contains $F_7$); $L(13)$ is linear, **$F_7$-free**, $n=m=13$, $\tau=6$ (so Henning–Yeo's $17\tau\le5n+3m$ reads $102\le104$, slack 2). $L(13)$ cannot be an AP hypergraph since it has $m=n>n-2$.

## 3. Section 2: properties of (4,5)-sets

**Prop 2.1 (p. 110). The A.P.-hypergraph of any (4,5)-set is 2-colourable.** [published]
- Proof as in the paper: define a graph $G=(R,U)$ with $xy\in U$ iff there is an AP $x<y<z$ in $R$ (the two smaller elements of each AP are joined, i.e. the **left endpoint to the midpoint**). "Since the midpoints of 3-term APs are distinct, $G$ is acyclic." A forest is bipartite; a proper 2-colouring of $G$ makes every AP bichromatic, so no colour class contains an edge of $H$.
- Why acyclic (the paper leaves it to the reader; [derived-here], short): orient each edge $x\to y$ (towards the midpoint). Every vertex is the midpoint of at most one AP, so every vertex has in-degree $\le1$. A cycle with $k$ edges has $k$ distinct heads, so each cycle vertex is the head of exactly one cycle edge: the cycle is directed, $x_1<x_2<\dots<x_k<x_1$ (each arrow goes from smaller to larger), a contradiction.
- **Corollary 2.2 (p. 111): $g(n)\ge(n+1)/2$.** Proof as the paper says: the larger class "results in an independent set containing more than half of the vertices". The "+1/2" is not spelled out. [derived-here] The maximum element is never a midpoint or a left endpoint, so it is isolated in $G$: colour $G-\{\max\}$, then put $\max$ in the larger class. This gives $\ge\lceil(n+1)/2\rceil$ points.
- This is the whole proof of $c_*\ge 1/2$. Note it uses only: midpoints distinct. It does not use linearity or $m\le n-2$ beyond that. (Ma–Tang show that for weak Sidon sets this is tight, $g(n)=\lceil(n+1)/2\rceil$.)

**Prop 2.3 (p. 111). The Fibonacci numbers $f(2),f(3),\dots,f(n+1)$ form a (4,5)-set** ($f(0)=f(1)=1$, $f(i)=f(i-1)+f(i-2)$, so the set is $\{2,3,5,8,13,\dots\}$). [published]
- Proof idea: show $f(j)-f(i)=f(l)-f(k)$ with $2<i<j\le k<l\le n+1$ forces $i=j-2$, $k=j$, $l=j+1$ (size comparison: $f(l)-f(k)\ge f(l-2)$ and $\ge f(k-1)$, while $f(j)-f(i)<f(j)$, so $j>\max\{k-1,l-2\}$). Among any four elements there is at most one triple $\{f(j-2),f(j),f(j+1)\}$, so at most one equal pair among the six differences, hence $\ge5$ distinct differences.
- Remark [verified-here]: the written proof assumes $i>2$, so it formally covers $f(3),\dots$; the case of the smallest element $f(2)=2$ is not treated, but the set $\{2,3,5,\dots\}$ passes `is_45_set` for $n\le14$. $\{1,2,3,5\}$ is NOT a (4,5)-set.
- Note the AP structure: the 3-APs of the Fibonacci set are exactly $\{f(j-2),f(j),f(j+1)\}$. [derived-here] This is the **path version of $L(n)$** (edges $\{i,i+2,i+3\}$, equivalently $\{i,i+1,i+3\}$ under reflection), with only $m=n-3$ edges, so it is not midpoint-saturated.

**Prop 2.4 (p. 111–112). For $n\ge4$ the A.P.-hypergraph $F(n)$ of the Fibonacci set has $\tau(F(n))=\lfloor 2(n-1)/5\rfloor$.** [published]
- Lower bound for $\tau$: take a minimum transversal $T$. $r_1,r_2$ have degree 1 so WLOG $\notin T$, hence one of $r_3,r_4\in T$. If $r_{i+2},r_{i+3},r_{i+4}\notin T$ then $r_i,r_{i+1}\in T$. Take a maximal family of $p$ disjoint such 5-tuples (they cover $5p$ vertices $P$), then at least half of the rest lies in $T$: $|T|\ge 2p+\frac{n-3-5p}{2}\ge 2p+\frac{2(n-1-5p)}{5}-1=\frac{2(n-1)}5-1$; the sharpness analysis (equality needs $r_3\notin T\cup P$ and $n-1-5p=0$, contradictory) then gives the floor.
- Upper bound for $\tau$: build minimum transversals for $4\le n_0\le8$ and extend by adding pairs $\{r_{5i+n_0+1},r_{5i+n_0+2}\}$, giving $n=5p+n_0$.
- [verified-here] `alpha` on the Fibonacci sets gives $\tau=\lfloor2(n-1)/5\rfloor$ for $n=4,\dots,15$.

**Corollary 2.5 (p. 112). $g(n)\le 3n/5+1$.** [published, **with a small off-by-constant error** [verified-here]]
- Since $h=n-\lfloor2(n-1)/5\rfloor\le(3n+6)/5$, the correct bound is $3n/5+6/5$. At $n=8$ the Fibonacci set has $h=6>5.8$, and at $n=13$ it has $h=9>8.8$. The asymptotic statement $c_*\le3/5$ is unaffected. (The exact finite values are in kb/00_START_HERE.md §5.)

**Prop 2.6 (p. 112–113). The A.P.-hypergraph of any (4,5)-set contains no $H_0$ as a partial hypergraph.** [published]
- $H_0$: $R=\{r_1,\dots,r_7\}$, $E=\{e_1=\{r_1,r_2,r_3\},\ e_2=\{r_4,r_5,r_6\},\ e_3=\{r_1,r_4,r_7\},\ e_4=\{r_2,r_5,r_7\},\ e_5=\{r_3,r_6,r_7\}\}$. This is the same as the project's $F_7=\{012,034,056,135,246\}$ (vertex 0 is $r_7$; $135,246$ are $e_1,e_2$). Equivalently AG(2,3) minus two points.
- The hypothesis used: $R$ has no four distinct numbers with $r_i-r_j=r_l-r_k$ other than the AP coincidences, i.e. the (4,5)-property in the form "no two disjoint equal differences".
- Proof (arithmetic, by midpoint labelling): five edges have five distinct midpoints, so exactly two of the seven vertices are non-midpoints. For edge $e_h=\{r_a,r_b,r_c\}$ with midpoint $r_c$ put $w(e_h)=2r_c-r_a-r_b=0$.
  - **Case a: $r_7$ is a midpoint** (the two non-midpoints $r_x,r_y$ lie in $\{r_1,\dots,r_6\}$). Take $W=w(e_1)+w(e_2)-w(e_3)-w(e_4)-w(e_5)=0$. The coefficients of $r_x,r_y,r_7$ vanish identically and one gets $W=3r_i+3r_j-3r_k-3r_l$ where $r_i,r_j$ are the midpoints of the two hyperedges not containing $r_7$ ($e_1,e_2$) and $r_k,r_l$ are the two midpoints "different from these" among the remaining three edges (the paper words it as "two further midpoints different from $r_i,r_j$"). Hence $r_i+r_j=r_k+r_l$, i.e. $r_i-r_k=r_l-r_j$, which violates the (4,5)-property. (I did not re-derive the coefficient bookkeeping by hand; the full 243-labelling linear-algebra check in the repo covers it.)
  - **Case b: $r_7$ is not a midpoint.** By symmetry the second non-midpoint is $r_1$ and $r_2$ is the midpoint of $e_1$. Then all midpoints are forced: $2r_2=r_1+r_3$, $2r_6=r_4+r_5$, $2r_4=r_1+r_7$, $2r_5=r_2+r_7$, $2r_3=r_6+r_7$. With $r_7=0$ and $\beta=r_5-r_3$: $r_4=5\beta$, $r_1=10\beta$, $r_5=3\beta$, $r_3=2\beta$, $r_6=4\beta$, $r_2=6\beta$. Then $r_2-r_4=\beta=r_5-r_3$, again violating the (4,5)-property. [verified-here: all five equations hold for these values]
- The project re-proves the result over all 243 midpoint labellings in `tests/test_known_facts.py::test_f7_not_realizable`.
- Because the AP structure is a Freiman 2-isomorphism invariant, "no $F_7$" holds for the sub-hypergraph of the AP-hypergraph with any labelling, not just the induced one.

## 4. Section 3: transversals in sparse 3-uniform hypergraphs

**Greedy + pairing construction (p. 113).** Greedy step: build $S=\{x_1,x_2,\dots\}$, each $x_{i+1}$ covering the maximum number of still-uncovered edges, stop when this maximum is $\le2$. Let $H_2$ be the hypergraph of uncovered edges (so $\Delta(H_2)\le2$). Pairing step: choose a maximum set of pairs of intersecting edges of $H_2$; $M$ = one common vertex per pair plus one vertex for each unpaired edge; $M$ is a minimum transversal of $H_2$ since $\Delta(H_2)\le2$. $T=S\cup M$.

**Lemma 3.1 (p. 113–114).** $G$ multigraph, maximum degree $\le3$ $\Rightarrow|E(G)|\le4\nu(G)$ ($\nu$ = matching number), with equality iff every component is a single vertex or a triangle with a double edge. If $G$ has no multiple edges then $|E(G)|\le3.5\,\nu(G)$. [published]
- Proof: take a maximum matching $Z$ maximizing the number of matched pairs with a parallel edge; count $s_i$ = edges "owned" by matched pair $i$, show $s_i\le4$ with equality only for "full" pairs, no edges outside $V(G|Z)$ by maximality. The $3.5$ bound for simple graphs is a special case of Chvátal–Hanson (cited as [LP, Thm 3.4.6]).

**Theorem 3.2 (p. 114–117) = Theorem A.** (a) $|V|=n$, $|E|\le n\Rightarrow\tau\le n/2$; (b) if no two edges meet in two vertices and no $H_0$, then $\tau\le(\tfrac12-\varepsilon)n$, $\varepsilon=(141\cdot76)^{-1}$. [published]
- **Part (a).** Let $S=S_0\cup S_1$ ($S_0$: greedy vertices that covered $\ge4$ new edges when added, $S_1$: those that covered exactly 3). $E=E_0\cup E_1\cup E_2$ (edges covered by $S_0$, by $S_1$, uncovered). $V\setminus S=V_0\cup V_1\cup V_2$, $V_i$ = vertices lying in exactly $i$ edges of $E_2$; $p_i=|V_i|$. Then $|S|+\sum p_i=n$ and $3|S|+|E_2|\le n$ (edge count). The dual of $H_2$ is a multigraph $G_2$ with $p_2$ edges, multiplicity $\le2$, max degree $\le3$; $|M|=|E_2|-\nu(G_2)\le|E_2|-p_2/4$ by Lemma 3.1. Using $3|E_2|=p_1+2p_2$ they get $\tau\le n/2-p_0/4$.
- **Part (b), the $\varepsilon$.** Refine to $|S_0|+|S_1|+\sum p_i=n$, $3|S_1|+|E_2|\le n$; with no double edges Lemma 3.1 gives $|M|\le|E_2|-p_2/3.5$, and then
  $\tau(H)\le n/2-(|S_0|+p_0/4+p_2/28)$ [(4') in the paper; note $p_2/28=\frac1{4}\cdot\frac{p_2}{7}$].
  Assume $|S_0|+p_0/4+p_2/28\le\varepsilon' n$. Let $A\subseteq V_1$ = the vertices of $V_1$ lying in an edge of $E_2$ that also meets $V_2$; $|A|\le4p_2$. $B=V_1\setminus A$; $F$ = edges of $E_2$ inside $B$ (pairwise disjoint, $\cup F=B$). $H_3=(S_1\cup B,\ \text{edges inside it})$. Claim (7): $\tau(H_3)\le(\tfrac12-\tfrac1{76})n$. Then $\tau(H)\le\tau(H_3)+(|S_0|+|V_0|+|V_2|+|A|)\le(\tfrac12-\tfrac1{76})n+140\varepsilon'n$, so $\varepsilon=\tfrac1{76}-140\varepsilon$ gives $\varepsilon=(141\cdot76)^{-1}$.
  - **Proof of (7).** Trivial bound $\tau(H_3)\le|S_1|+|F|$.
    - Case 1, $|S_1|\le(\tfrac14-\delta)n$: with $3|F|\le n-|S_1|$ get $\tau(H_3)\le\tfrac23|S_1|+\tfrac n3$. The paper then writes this as $\le(\tfrac12-\delta)n$, but the arithmetic gives $(\tfrac12-\tfrac23\delta)n$ [derived-here: small slip in the paper]. Redoing the optimisation with the corrected Case 1 gives $\delta=1/52$ and $\tau(H_3)\le(\tfrac12-\tfrac1{78})n$, i.e. $\varepsilon=(141\cdot78)^{-1}$ instead of $(141\cdot76)^{-1}$. Immaterial for #757 (superseded by 9/17), but quote the paper's constant as the published one.
    - Case 2, $|S_1|\ge(\tfrac14-\delta)n$: use **improving blocks** $B_i=\{x_i\}\cup\bigcup\{f:f\in A_i\}$ ($x_i\in S_1$, $A_i\subseteq F$ the edges of $F$ that meet its $d(x_i)$ edges) such that a $d(x_i)$-subset of $B$ meets all the relevant edges: each such block saves one vertex over the trivial bound. Maximum degree of $H_3\le3$ so blocks have 1, 4, 7 or 10 vertices, a greedy choice of disjoint blocks gives $\ge|S_1|/18$ of them, so $\tau(H_3)\le|S_1|+|F|-|S_1|/18$. **The case $d(x)=3$ is the critical one and is exactly where $H_0$-freeness is used**: three edges $f_i,f_j,f_k\in F$ meeting $e_1,e_2,e_3$ respectively must exist (otherwise an $H_0$ appears).
    - Optimizing: $\delta=\tfrac1{18}(\tfrac14-\delta)$ gives $\delta=\tfrac1{76}$. The constants $18$ (block count), $4$ and $28$ ($=4\cdot7$) are all quite wasteful.
- **Where $\varepsilon$ cannot go beyond:** the Theorem B remark $\varepsilon\le1/26$ from $L(13)$.
- **Corollary 3.3 (p. 118). Every (4,5)-set of $n$ elements contains a Sidon set of size $\ge(1/2+\varepsilon)n$.** From Thm 3.2(b) with Props 2.6 and linearity. [published]
- The theorem only uses $|E|\le n$, not $|E|\le n-2$ or the midpoint injectivity (the two non-midpoint points). So there was slack (Ma–Tang/Henning–Yeo exploit $m\le n-2$ together with a better transversal inequality).

## 5. The Fibonacci construction (summary)
- Set: $\{f(2),\dots,f(n+1)\}=\{2,3,5,8,\dots\}$; (4,5) by Prop 2.3; AP edges $\{f(j-2),f(j),f(j+1)\}$; $h=n-\lfloor2(n-1)/5\rfloor\approx3n/5$; hence $c_*\le3/5$ (the paper's Cor 2.5 constant should read $+6/5$).

## What transfers to #757
- **Lower-bound track.**
  - The reduction $h(A)=\alpha(H(A))$ and the list of properties (3-uniform, linear, $m\le n-2$, distinct midpoints, no $F_7$). [published: p. 109 and Prop 2.6]. Nothing beyond $F_7$ is available as a forbidden configuration: any new forbidden configuration must be found by us (e.g. by computing which small linear hypergraphs are non-realizable; see `e757/core.realize`).
  - Prop 2.6's proof technique: sum the midpoint equations with signs so that coefficients of "free" points vanish and you are left with a nontrivial repeated-difference relation $r_i+r_j=r_k+r_l$. This is a **certificate type**: a $\{0,\pm1\}$-combination of the midpoint equations that is identically a "four-point" relation. It generalizes: any hypergraph with a signed dependency among its midpoint equations whose result is a single 4-term relation is non-realizable. This suggests a systematic search for other forbidden configurations (subgraphs of larger linear hypergraphs where the labelled system forces some $r_a+r_b=r_c+r_d$).
  - The "forest of midpoints" $G$ (left-endpoint–midpoint graph). This forest 2-colouring gives only $1/2$. A possible improvement is to use two such forests (left–mid and right–mid) simultaneously.
  - The **greedy-plus-degree-2 structure** (Thm 3.2): vertices of AP-degree $\ge3$ handled greedily; what remains has $\Delta\le2$, where Henning–Yeo (EJC 2017) give $18\tau\le4n+4m+2$ ($5/9$-type bounds). Hence the extremal sets for $c_*$ need many vertices of AP-degree $\ge3$.
  - Extremal hypergraphs for the cruder bound ($J(n)$, $L(8)$ for $\tau=n/2$; $L(13)$ for $\varepsilon\le1/26$) show which pieces to look for: $L(13)$ is linear and $F_7$-free but has $m=n$, so impossible for AP hypergraphs.
- **Upper-bound track.** The Fibonacci hypergraph is the path $L(n)$ with only $n-3$ edges (not saturated). Saturating it ($m=n-2$) while keeping $\tau$ high is exactly the problem; the periodic chain constructions cap at $3/5$ (see kb/dead_ends.md).

## Open questions
The paper states none. Questions it suggests (not stated by the authors): the true $\varepsilon$ between $(141\cdot76)^{-1}$ and $1/26$ for Thm A (the AP case was settled differently, $9/17-1/2=1/34$); whether other minimal obstructions besides $H_0$ exist for hypergraphs with $|E|=n-2$; whether Theorem B's extremal characterization (proof "in a preliminary version") has been published.
