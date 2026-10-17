# Every 14-point (4,5)-set with h = 8 has exactly 12 three-term APs: there are no non-saturated extremal 14-point sets, so the 2,910 classes of L004 are all of them
CLAIM-TYPE: lemma + certificate (computer-assisted proof: a short case analysis on top of exhaustive enumerations; every enumeration that the proof uses was run by two independently written programs, and the final step has two independent proofs)
TYPE: certificate
STATUS: submitted 2026-10-17 03:39 UTC (prover draft; not yet refereed)
DEPENDS ON:
- K3 [published] (Ma–Tang Props 2.1, 2.2: a (4,5)-set is weak Sidon), K4 [published] (Ma–Tang Lemma 2.3: for a weak Sidon set the Sidon subsets are the 3-AP-free subsets, so $h(A)=\alpha(H(A))$), K5 [published] (Ma–Tang Lemma 2.4: the midpoint map is injective and never hits $\min A$ or $\max A$), K6 [published] (Ma–Tang Lemma 2.5: $H(A)$ is linear), K7 [published] (Gyárfás–Lehel Prop 2.6: $H(A)$ contains no $F_7$). Used only in Step 8.1 (realizable patterns lie in class $O$).
- K8 [published] (Henning–Yeo, Graphs Combin. 37 (2021) 867–890, Thm 7, as cited in Ma–Tang Thm 5.3: $17\tau\le 5n+3m$ for every linear 3-uniform hypergraph with no subhypergraph isomorphic to $F_7$). Used in Step 1 (it cuts Lemma A down to finitely many cells) and in Step 8.3 ($m\ge 11$ at $n=14$, $\tau=6$). The full text of Henning–Yeo was not obtained by the project; the statement used is the one cited by Ma–Tang (kb/notes/henning_yeo_2021_affine.md), and it is the same input on which the published bound $c_*\ge9/17$ rests.
- K24 [derived-here] ($f(14)=8$, $f(15)=9$): Steps 8.3 and 8.4 only.
- L004 [verified-here, ACCEPTED round 1; completeness re-checked by sampling, see its STATUS]: Corollary 3 only.
- L005 [verified-here, ACCEPTED rounds 2 and 3]: Corollary 4 only.
- Not used anywhere: K30 (monotone midpoints), K31 (medial triangle), the forbidden cores K32–K33, Lemmas E/U/Δ/Δ′, Tuza / Chvátal–McDiarmid. L002 is quoted only as a consistency check for one cell.
- Programs. Falsifier code (experiments/falsify/i11-inequality/): `conn_dfs2.c`, `conn_dfs2_all.c`, `ext_vertex_all.c`, `analyze_hits.py`, `ud_check.py`, `tight_classes.py`, `crosscheck_ext.py`, `sat_cell.py`, and `e757/cpsat_model.py:find_f7`. Prover code written for this certificate without reusing that code (experiments/prover/L007/): `indep/enum_conn.c`, `indep/ext_indep.c`, `indep/f7check.py`, `indep/bf_cells.c`, `indep/bf_cell.c`, `indep/compare_bf.py`, `indep/iso_compare.py`, `indep/member.py`, `indep/compare_hits.py`, `indep/hits_breakdown.py`, `build_input.py`, `cells.py`, `cells_table.py`, `witness_14_11.py`, `check_witness_records.py`, `sanity_m11_sets.py`; all commands in `experiments/prover/L007/reproduce.sh`.

## Statement

**Conventions.** A *3-graph* $H=(V,E)$ is a finite 3-uniform hypergraph without repeated edges; $n=|V|$, $m=|E|$, $\tau(H)$ is the transversal number (least size of a vertex set meeting every edge), $\alpha(H)=n-\tau(H)$, $d(v)$ is the degree of $v$ and $\Delta(H)$ the maximum degree. For $S\subseteq V$, $H[S]=(S,\{e\in E:e\subseteq S\})$, $e(S)=|E(H[S])|$, and $H-v=H[V\setminus\{v\}]$. $H$ is *linear* if two distinct edges share at most one vertex. $F_7$ is the 3-graph $\{012,034,056,135,246\}$ (AG(2,3) minus two points); $H$ *contains* $F_7$ if five edges of $H$ form a subhypergraph isomorphic to $F_7$ (not necessarily induced; this is the notion of K7 and K8), otherwise $H$ is *$F_7$-free*. Connectivity and components refer to the primal graph (two vertices adjacent iff some edge contains both). The *I11 slack* is $s(H):=3n+2m-11\,\tau(H)$.

**Classes.** $O^+$ is the class of 3-graphs with
- (P1) $H$ is linear;
- (P2) $H$ is $F_7$-free;
- (P3) $e(S)\le|S|-2$ for every $S\subseteq V$ with $|S|\ge2$.

$O$ is the class of *ordered midpoint patterns* (kb/00_START_HERE.md §2; experiments/falsify/i11-inequality/README.md): $V=\{0,\dots,n-1\}$, every edge is a triple $i<j<k$ with designated midpoint $j$, distinct edges have distinct midpoints, and $H$ is linear and $F_7$-free. (L002 and L004 use the name "class O" for the subclass that also satisfies K30; everything below holds for the larger classes.) $O\subseteq O^+$ (Step 0.3), so every statement about $O^+$ holds for $O$.

**Theorem 1 (abstract).** Every $H\in O^+$ with $n=14$ and $m=11$ has $\tau(H)\le5$, i.e. $\alpha(H)\ge9$. The bound is attained by realizable patterns (Step 7), so $\max\tau$ over $O$, and over $O^+$, at $(n,m)=(14,11)$ is exactly 5.

**Theorem 2 ((4,5)-sets).** There is no 14-point (4,5)-set $A$ with $h(A)\le8$ and exactly 11 three-term APs.

**Corollary 3.** Every 14-point (4,5)-set $A$ with $h(A)=8$ ($=f(14)$, the least possible value) has exactly $12=n-2$ three-term APs, i.e. it is midpoint-saturated. Consequently, by L004, up to affine equivalence there are exactly 2,910 fourteen-point (4,5)-sets with $h=8$ (all of them, not only the saturated ones), all affinely rigid, $A_{\rm base}$ among them; and the open question Q11 of kb/open_questions.md is answered: the $(14,11,\alpha\le8)$ case is empty, already in the abstract class $O^+$. (The number 2,910 inherits the caveat of L004: its completeness was re-checked by the referee on 28% of the prefixes plus consistency checks, not by a full second enumeration.)

**Corollary 4 (with L005).** If $C$ is a 16-point (4,5)-set with $h(C)\le9$, then $h(C)=9$ and every 14-point subset of $C$ has $h=9$; equivalently, for every two points $p,q\in C$ some maximum Sidon subset of $C$ avoids both $p$ and $q$.

**Lemma A (I11 below 14 vertices).** Every $H\in O^+$ with $n\le13$ satisfies $11\,\tau(H)\le3n+2m$.

Tags: Theorems 1, 2, Corollaries 3, 4 and Lemma A are **[verified-here] conditional on referee acceptance** (until then [derived-here], computer-assisted). Scope: nothing is claimed for $n\ge15$; the remarks of Step 9 (I11 on $O^+$ for $n\le15$ and its consequence for 16-point sets) are explicitly **not** certified here.

## Proof

### Step 0. Elementary facts

0.1 (Components.) Let $C_1,\dots,C_k$ be the components of $H$; each is $C_i=H[V(C_i)]$ and every edge lies in exactly one $C_i$. Then $n=\sum n(C_i)$, $m=\sum m(C_i)$, and $\tau(H)=\sum\tau(C_i)$, because $T\subseteq V$ is a transversal of $H$ iff $T\cap V(C_i)$ is a transversal of $C_i$ for every $i$. Hence $s(H)=\sum_i s(C_i)$. A component without edges is a single vertex and has $s=3\cdot1+0-0=3$; a component with an edge has at least 3 vertices.

0.2 (Heredity.) If $H\in O^+$ and $S\subseteq V$ then $H[S]\in O^+$: a subhypergraph of a linear ($F_7$-free) 3-graph is linear ($F_7$-free), and $e_{H[S]}(S')=e_H(S')\le|S'|-2$ for $S'\subseteq S$, $|S'|\ge2$. (Likewise $O$ is closed under $H\mapsto H[S]$ with the vertices of $S$ renumbered increasingly: edges, their midpoints and their internal order are kept.)

0.3 ($O\subseteq O^+$.) Let $H\in O$, $S\subseteq V$, $|S|\ge2$. Each edge $\{i<j<k\}\subseteq S$ has its midpoint $j$ in $S\setminus\{\min S,\max S\}$, and distinct edges have distinct midpoints, so $e(S)\le|S|-2$. (P1) and (P2) are part of the definition of $O$.

0.4 (Bounds.) For every 3-graph, $\tau(H)\le m$ (one vertex from each edge), and $\tau(H)-1\le\tau(H-v)\le\tau(H)$ for every vertex $v$ (if $T$ is a transversal of $H$, then $T\setminus\{v\}$ is one of $H-v$; if $T'$ is one of $H-v$, then $T'\cup\{v\}$ is one of $H$). For $H\in O^+$ with $n\ge2$: $m=e(V)\le n-2$ by (P3). For $H\in O^+$: $17\,\tau(H)\le5n+3m$ by K8, since $H$ is linear and $F_7$-free.

0.5 (Connected 3-graphs.) A connected 3-graph with $m\ge1$ edges has $n\le2m+1$. Indeed every vertex lies in an edge (a vertex in no edge is a component by itself), and the edges can be ordered $e_1,\dots,e_m$ so that each $e_t$ ($t\ge2$) meets $e_1\cup\dots\cup e_{t-1}$ (if at some stage every remaining edge were disjoint from the union $U$ of the edges taken so far, then $V\setminus U$ would be non-empty (it contains the remaining edges) and no edge would meet both $U$ and $V\setminus U$, contradicting connectivity); so $n=|e_1\cup\dots\cup e_m|\le3+2(m-1)$.

### Step 1. The window cells (arithmetic)

Call $(n,m)$ a *connected cell* if $n\ge3$ and $\lceil(n-1)/2\rceil\le m\le n-2$ (Step 0.5 and (P3)). Put $\mathrm{lo}(n,m)=\lfloor(3n+2m)/11\rfloor+1$, the least $\tau$ with $s<0$, and $\mathrm{hy}(n,m)=\lfloor(5n+3m)/17\rfloor$, the largest $\tau$ allowed by K8. A connected cell is a *window cell* if $\mathrm{lo}\le\min(\mathrm{hy},m)$. All connected cells with $n\le15$ (`experiments/prover/L007/cells_table.py`, output `cells_table.txt`; each entry is one line of integer arithmetic):

| $n$ | connected cells $m$: (lo, hy) |
|---|---|
| 3 | 1: (2, 1) |
| 4 | 2: (2, 1) |
| 5 | 2: (2, 1); **3: (2, 2) window** |
| 6 | 3: (3, 2); 4: (3, 2) |
| 7 | 3: (3, 2); 4: (3, 2); 5: (3, 2) |
| 8 | **4: (3, 3) window**; 5: (4, 3); 6: (4, 3) |
| 9 | 4: (4, 3); 5: (4, 3); 6: (4, 3); 7: (4, 3) |
| 10 | 5: (4, 3); **6: (4, 4) window**; 7: (5, 4); 8: (5, 4) |
| 11 | **5: (4, 4) window**; 6: (5, 4); 7: (5, 4); 8: (5, 4); 9: (5, 4) |
| 12 | 6: (5, 4); 7: (5, 4); 8: (5, 4); **9: (5, 5) window**; 10: (6, 5) |
| 13 | 6: (5, 4); **7: (5, 5) window**; 8: (6, 5); 9: (6, 5); 10: (6, 5); 11: (6, 5) |
| 14 | 7: (6, 5); 8: (6, 5); 9: (6, 5); 10: (6, 5); **11: (6, 6) window**; 12: (7, 6) |
| 15 | 7: (6, 5); 8: (6, 5); **9: (6, 6) window**; **10: (6, 6) window**; 11: (7, 6); 12: (7, 6); 13: (7, 6) |

Example rows of the arithmetic: $(12,9)$: $3n+2m=54$, $\lfloor54/11\rfloor+1=5$; $5n+3m=87$, $\lfloor87/17\rfloor=5$. $(13,8)$: $\lfloor55/11\rfloor+1=6>\lfloor89/17\rfloor=5$. $(14,11)$: $\lfloor64/11\rfloor+1=6=\lfloor103/17\rfloor$.

So the window cells with $n\le13$ are exactly $(5,3)$, $(8,4)$, $(10,6)$, $(11,5)$, $(12,9)$, $(13,7)$, each with the single admissible value $\tau=\mathrm{lo}=2,3,4,4,5,5$; written as $(n,m,\tau)$: (5,3,2), (8,4,3), (10,6,4), (11,5,4), (12,9,5), (13,7,5). In every window cell $\mathrm{hy}\le m$. For $n\in\{14,15\}$ the window cells are (14,11,6), (15,9,6), (15,10,6). (Note for the referee: the list in experiments/falsify/i11-inequality/README.md §2 omits (5,3,2); the falsifier's `verify_cells.py` did include and decide it, `results_verify_cells_n13.json`.)

### Step 2. Proof of Lemma A

2.1 Let $H\in O^+$ with $n\le13$ and suppose $s(H)<0$. By Step 0.1 some component $C$ has $s(C)<0$; $C$ is not a single vertex (that has $s=3$), so $C$ is a connected 3-graph with $n_C\ge3$ vertices and $m_C\ge1$ edges, $C\in O^+$ (Step 0.2), and $n_C\le n\le13$.

2.2 By Steps 0.4 and 0.5, $(n_C,m_C)$ is a connected cell, $\tau(C)\ge\mathrm{lo}(n_C,m_C)$ (as $s(C)<0$) and $\tau(C)\le\min(\mathrm{hy},m_C)$. So $(n_C,m_C)$ is one of the six window cells with $n\le13$ of Step 1, and $C$ is a connected linear 3-graph with $n_C$ vertices, $m_C$ edges and $\tau(C)\ge\mathrm{lo}(n_C,m_C)$.

2.3 Computation C1: for each of (5,3,2), (8,4,3), (10,6,4), (11,5,4), (12,9,5), (13,7,5) there is **no** connected linear 3-graph with these $n$, $m$ and $\tau\ge\mathrm{lo}$ (no $F_7$, order or midpoint condition imposed, so this is a statement about a class containing every candidate $C$). This contradicts 2.2, so $s(H)\ge0$. (For $n\le2$, $m=0$ and $s=3n\ge0$.) $\square$

2.4 (Hand proof of the smallest cell, as a check.) A linear 3-graph on 5 vertices has at most 2 edges: two distinct triples in a 5-set meet in $\ge6-5=1$ vertex, hence in exactly one, say $\{0,1,2\}$ and $\{0,3,4\}$. A third edge $e$ meets each of them in at most one vertex. If $0\in e$, its two other vertices avoid $\{1,2\}$ and $\{3,4\}$, which is impossible. If $0\notin e$, then $|e\cap\{1,2\}|\le1$ and $|e\cap\{3,4\}|\le1$ give $|e|\le2$. So the cell (5,3) is empty.

### Step 3. Lemma B (degrees)

Let $H\in O^+$ with $n=14$, $m=11$ and $\tau(H)\ge6$.

3.1 For every vertex $v$: $H-v\in O^+$ (Step 0.2) has 13 vertices and $11-d(v)$ edges, and $\tau(H-v)\ge\tau(H)-1\ge5$ (Step 0.4). Lemma A gives $11\,\tau(H-v)\le39+2(11-d(v))=61-2d(v)$.

3.2 Hence $55\le61-2d(v)$, i.e. $d(v)\le3$, for every $v$. Moreover $11\,\tau(H-v)\le61<66$, so $\tau(H-v)=5$, and $\tau(H)\le\tau(H-v)+1=6$; thus $\tau(H)=6$.

3.3 $\sum_v d(v)=3m=33$. If $d_3$ vertices have degree 3 and the other $14-d_3$ have degree $\le2$, then $33\le3d_3+2(14-d_3)=28+d_3$, so $d_3\ge5$. In particular $H$ has a vertex of degree 3.

### Step 4. Lemma C (the structure of $H-v$ for a degree-3 vertex)

Let $H$ be as in Step 3, $v$ a vertex with $d(v)=3$, and $G:=H-v$.

4.1 $G\in O^+$ has $n=13$, $m=8$ and $\tau(G)=5$ (Step 3.2), so $s(G)=39+16-55=0$.

4.2 Every component $C$ of $G$ is in $O^+$ (Step 0.2) and has at most 13 vertices, so $s(C)\ge0$ by Lemma A. The slacks add up to $s(G)=0$ (Step 0.1), so $s(C)=0$ for every component. A single vertex has slack 3, so $G$ has no isolated vertex, and every component is a connected 3-graph with $n_C\ge3$, $m_C\ge1$, $m_C\le n_C-2$ (P3), $n_C\le2m_C+1$ (Step 0.5) and $3n_C+2m_C=11\,\tau(C)$.

4.3 (Slack-0 connected cells with $n\le13$.) $3n+2m\equiv0\pmod{11}$ means $2m\equiv-3n$, i.e. $m\equiv4n\pmod{11}$ (multiply by $6=2^{-1}$; $-18\equiv4$). The range $\lceil(n-1)/2\rceil\le m\le n-2$ has at most $(n-1)/2\le6<11$ elements, so it contains at most one solution:

| $n$ | $4n \bmod 11$ | range of $m$ | solution $(n,m,\tau)$ |
|---|---|---|---|
| 3 | 1 | [1,1] | (3,1,1) |
| 4 | 5 | [2,2] | none |
| 5 | 9 | [2,3] | none |
| 6 | 2 | [3,4] | none ($m=2$ would give (6,2,2), which has $n>2m+1$) |
| 7 | 6 | [3,5] | none |
| 8 | 10 | [4,6] | none |
| 9 | 3 | [4,7] | none ($m=3$: (9,3,3), $n>2m+1$) |
| 10 | 7 | [5,8] | (10,7,4) |
| 11 | 0 | [5,9] | none |
| 12 | 4 | [6,10] | none ($m=4$: (12,4,4), $n>2m+1$) |
| 13 | 8 | [6,11] | (13,8,5) |

($\tau$ is forced by $3n+2m=11\tau$. The three survivors also satisfy $\tau\le m$ and K8: $17\le18$, $68\le71$, $85\le89$; the same list is printed by `experiments/prover/L007/cells.py`.)

4.4 The numbers of vertices of the components add up to $13=3a+10b+13c$ with $a,b,c\ge0$, whose only solutions are $(a,b,c)=(0,0,1)$ and $(1,1,0)$. Hence either
(i) $G$ is a connected linear 3-graph with $(n,m,\tau)=(13,8,5)$, or
(ii) $G$ is the disjoint union of a connected linear 3-graph $C$ with $(n,m,\tau)=(10,7,4)$ and a single edge.

### Step 5. Theorem 1, first proof (Route I)

Let $H\in O^+$ with $n=14$, $m=11$, and suppose $\tau(H)\ge6$. By Step 3, $\tau(H)=6$ and $H$ has a vertex $v$ of degree 3; let $G=H-v$ and apply Step 4.

5.1 Case (i). By Lemma D (computation C0), $G$ is isomorphic to one of the 159 labelled graphs output by `conn_dfs2_all 13 8 5` (computation C2; 2 isomorphism classes; the independent `enum_conn` outputs the same 159 graphs and the same 2 classes). By computation C3, each of the 159 contains $F_7$. Since $G$ is a subhypergraph of $H$, $H$ contains $F_7$, contradicting (P2).

5.2 Case (ii). By C2, $C$ is isomorphic to one of the 637 outputs $C_0$ (vertex set $\{0,\dots,9\}$) of `conn_dfs2_all 10 7 4`; hence some bijection $\varphi:V(G)\to\{0,\dots,12\}$ is an isomorphism from $G$ onto $G_0:=C_0+\{10,11,12\}$. Let $\{v,a_i,b_i\}$ ($i=1,2,3$) be the three edges of $H$ at $v$. By (P1) the pairs $\{a_i,b_i\}$ are pairwise disjoint (two edges at $v$ meet only in $v$) and no pair $\{a_i,b_i\}$ lies inside an edge of $G$ (that edge would share two vertices with $\{v,a_i,b_i\}$). The same holds for the pairs $\varphi(\{a_i,b_i\})$ relative to $G_0$. So $H_0:=G_0+\{13,\varphi(a_i),\varphi(b_i)\}_{i=1,2,3}$ is one of the extensions enumerated in computation C4 (for each of the 796 input graphs, all unordered triples of pairwise disjoint pairs of $\{0,\dots,12\}$ none of which lies inside an edge of the graph), and $\varphi\cup\{v\mapsto13\}$ is an isomorphism $H\to H_0$. Hence $\tau(H_0)=6$, so $H_0$ is one of the 3,186 extensions with $\tau\ge6$ found in C4. By C4 (with the $F_7$ tests of C3) every one of them contains $F_7$; hence so does $H$, contradicting (P2).

5.3 Both cases are impossible, so $\tau(H)\le5$. $\square$

### Step 6. Theorem 1, second proof (Route II)

This proof uses Lemma A and Step 3 only; it does not use Steps 4–5 or computations C2–C4.

6.1 Let $H\in O^+$ with $n=14$, $m=11$ and $\tau(H)\ge6$. $H$ is connected: otherwise every component has at most 13 vertices, hence slack $\ge0$ by Lemma A (and Step 0.2), so $s(H)\ge0$ by Step 0.1; but $s(H)=42+22-11\tau(H)\le64-66=-2$.

6.2 $\Delta(H)\le3$ by Step 3.2.

6.3 By Lemma D (C0), $H$ is isomorphic to one of the 998 outputs of `conn_dfs2_all 14 11 6 3` (computation C5; the independent `enum_conn 14 11 6 3` outputs the same 998 labelled graphs). By C5, every one of them contains $F_7$, contradicting (P2). $\square$

6.4 (What the 998 graphs are.) All 998 outputs are isomorphic to a single 3-graph $D_{14}$: two vertex-disjoint copies of $F_7$ joined by one edge that meets one copy in two vertices and the other in one, e.g. $\{(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13)\}\cup\{(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12)\}\cup\{(2,3,4)\}$ ($\tau=3+3=6$, $|\mathrm{Aut}|=4$, degrees $3^5\,2^9$; it satisfies (P1) and (P3) but not (P2)). So the only connected linear 3-graph with $n=14$, $m=11$, $\tau\ge6$ and $\Delta\le3$ is $D_{14}$, which is the falsifier's example `f7_containing_violation.json`.

### Step 7. The bound is attained

7.1 $W=\{0,323,523,566,569,572,595,609,621,646,723,851,919,1379\}$ is a (4,5)-set with exactly 11 three-term APs and $h(W)=9$ (computation C7, from the definitions: all 1,001 four-point subsets have at least 5 distinct differences; the largest Sidon subset, found by testing subsets, has 9 elements). ($W-323=(A_{\rm base}\setminus\{136\})\cup\{-323\}$.) The Fibonacci set $\{F_3,\dots,F_{16}\}=\{2,3,5,\dots,987\}$ is another such set: $n=14$, $m=11$, $h=9$ (C7). By Step 8.1 their AP patterns lie in $O\subseteq O^+$ and have $\tau=14-9=5$. Together with Theorem 1, $\max\tau=5$ at $(14,11)$ in $O$ and in $O^+$.

### Step 8. Theorem 2, Corollaries 3 and 4

8.1 (Realizable patterns lie in $O$.) Let $A=\{x_0<\dots<x_{n-1}\}$ be a (4,5)-set and $H(A)$ the 3-graph on $\{0,\dots,n-1\}$ whose edges are the triples $i<j<k$ with $x_i+x_k=2x_j$, with midpoint $j$. By K5 each $j$ is the midpoint of at most one edge, by K6 $H(A)$ is linear, and by K7 it contains no $F_7$; so $H(A)\in O\subseteq O^+$. By K3 and K4, $h(A)=\alpha(H(A))=n-\tau(H(A))$.

8.2 (Theorem 2.) If $|A|=14$, $A$ has exactly 11 three-term APs and $h(A)\le8$, then $H(A)\in O^+$ has $n=14$, $m=11$ and $\tau=14-h(A)\ge6$, contradicting Theorem 1. $\square$

8.3 (Corollary 3.) Let $|A|=14$ with $h(A)=8$, so $\tau(H(A))=6$. K8 gives $17\cdot6=102\le70+3m$, i.e. $m\ge11$ (as $3\cdot10=30<32$). K5 gives $m\le12$. Theorem 2 excludes $m=11$. Hence $m=12=n-2$: $A$ is midpoint-saturated, and by L004 it is affinely equivalent to one of the 2,910 classes (each of which is a 14-point (4,5)-set with $h=8$ and $m=12$, L004). Since $f(14)=8$ (K24), "$h(A)=8$" and "$h(A)\le8$" describe the same sets. Q11 asked whether the case $(14,11,\alpha\le8)$ contains realizable patterns; Theorem 1 shows that it contains no pattern of $O^+$ at all. $\square$

8.4 (Corollary 4.) Let $C$ be a 16-point (4,5)-set with $h(C)\le9$. Every subset of $C$ is a (4,5)-set (its 4-subsets are 4-subsets of $C$), and a Sidon subset of a subset of $C$ is a Sidon subset of $C$; so $9=f(15)\le h(C\setminus\{p\})\le h(C)\le9$ (K24) and $h(C)=9$. Let $A\subseteq C$, $|A|=14$; then $8=f(14)\le h(A)\le9$. If $h(A)=8$, Corollary 3 makes $A$ saturated ($m(A)=12$), and L005, which is stated for every 14-point (4,5)-set with $h=8$ and $m=12$, gives $h(C)=h(A\cup\{x,y\})=10$ for the two points $x,y$ of $C\setminus A$ ($C$ is a (4,5)-set), a contradiction. So $h(A)=9$. Applied to $A=C\setminus\{p,q\}$: a maximum Sidon subset of $A$ has 9 elements and is a maximum Sidon subset of $C$ avoiding $p$ and $q$. $\square$

### Step 9. Remarks (NOT certified here; to be certified separately)

9.1 (I11 on $O^+$ for $n\le15$.) The window cells with $n\in\{14,15\}$ are (14,11,6), (15,9,6), (15,10,6) (Step 1). The first is empty in $O^+$ by Theorem 1. For the other two, `conn_dfs2` finds no connected linear 3-graph (falsifier: 2,459,440 and 186,011,577 nodes; re-run here with identical node counts and found = 0; computation C6; the independent `enum_conn` also finds none). With the argument of Step 2 this would give $11\tau\le3n+2m$ for every $H\in O^+$ with $n\le15$. (The cell (16,8,6) is also empty: 19,144 nodes.)

9.2 (Consequence for 16-point sets, derived from 9.1 exactly as Step 3 is derived from Lemma A.) Let $C$ be a 16-point (4,5)-set with $h(C)=9$, $H=H(C)$, $\tau=7$. K8 gives $119\le80+3m$, so $m\ge13$; and $m\le14$. For each $v$, $\tau(H-v)\ge6$ and 9.1 gives $66\le11\tau(H-v)\le45+2(m-d(v))$. For $m=13$ this forces $d(v)\le2$ for all $v$, so $39=3m\le32$, impossible; hence $m=14$, $d(v)\le3$ and $\tau(H-v)=6$ for every $v$ (since $77>73-2d(v)$), and at least 10 vertices have degree 3 ($42\le32+d_3$). With Corollary 4, the pair constraint of D24 ("for every pair $p,q$ either an independent 9-set avoiding both or $m(C-p-q)=11$") reduces to its first alternative.

9.3 (Hypotheses are needed.) (P2) is essential: `experiments/falsify/i11-inequality/f7_containing_violation.json` is a connected linear (14,11) 3-graph with $\tau=6$ containing $F_7$ (by Step 6.4 it is the only one with $\Delta\le3$, up to isomorphism). For I11 in general, (P3) is essential: `f7free_nonO_violation_9_8_4.json` is linear, $F_7$-free, $(n,m,\tau)=(9,8,4)$, $s=-1$, with $m>n-2$.

## Computer-verified steps

All runs on this machine (gcc 13.3.0, Python 3, networkx 3.x), under load (4 cores, load average 7 to 14 from other jobs), so wall times are indicative only. All arithmetic is exact (integers, bitmasks).

**C0. Exhaustiveness of the enumerators (Lemma D) and its validation.**

*Lemma D.* Let $H$ be a connected linear 3-graph with $n\ge3$ vertices, $m\ge1$ edges, $\tau(H)\ge T_0$ and $\Delta(H)\le D$. Run the following *canonical process*: give an arbitrary vertex the label 0; set $\ell=1$ (labels used) and $P=\emptyset$ (placed edges); for $c=0,1,2,\dots$ while $P\ne E(H)$, let $x$ be the vertex labelled $c$ (write $\lambda(y)$ for the label of a labelled vertex $y$), $\ell_0:=\ell$, $F:=\{e\in E(H)\setminus P: x\in e\}$, and place (a) the edges $e\in F$ whose two other vertices are both labelled, in increasing lexicographic order of their label pairs; then (b) the edges $e\in F$ with exactly one other labelled vertex $y$, in increasing order of the label of $y$, giving the unlabelled vertex the label $\ell$ and increasing $\ell$; then (c) the remaining edges of $F$, in any order, giving their two vertices the labels $\ell,\ell+1$ and increasing $\ell$ by 2. Then:
- (D1) Edges of $F$ contain no vertex with label $<c$ (D2 for $c-1$). By linearity the sets $e\setminus\{x\}$, $e\in F$, are pairwise disjoint, so a vertex unlabelled at the start of turn $c$ lies in only one edge of $F$ and is still unlabelled when that edge is placed; a labelled vertex of $e\setminus\{x\}$ has a label in $(c,\ell_0)$ (it was not labelled during turn $c$, since the edge of $F$ that labelled it would share two vertices with $e$). Distinct (a)-edges have distinct label pairs and distinct (b)-edges have distinct $y$ (else they share two vertices), so the orders in (a) and (b) are strict.
- (D2) After turn $c$, every edge containing a vertex with label $\le c$ is in $P$ (induction on $c$: turn $c$ places all of $F$).
- (D3) If $P\ne E(H)$ after turn $c$, then $c+1<\ell$: the labelled vertices are $L=\bigcup P$ (vertex 0 lies in the first placed edge, every other label was given to a vertex of a placed edge, and turn 0 places at least one edge since $d(\text{vertex }0)\ge1$); if $L\ne V$, connectivity gives an edge meeting $L$ and $V\setminus L$, which is unplaced; if $L=V$, any unplaced edge meets $L$; in both cases a vertex $y\in L$ lies in an unplaced edge, so $\lambda(y)>c$ by (D2), and $c+1\le\lambda(y)\le\ell-1$.
- (D4) At the end $P=E(H)$ and $L=V$ (every vertex lies in an edge), so $\ell=n$.
- (D5) At every moment: $\ell\le n$; $\ell+2(m-|P|)\ge n$ (each unplaced edge contains, when placed, the already labelled vertex $x$, so it adds at most 2 labels, and finally $\ell=n$); $\tau(P)\ge\tau(H)-(m-|P|)\ge T_0-(m-|P|)$ (adding one vertex of each unplaced edge to a minimum transversal of $P$ gives a transversal of $H$); all degrees in $P$ are $\le D$.

*The programs contain this process as a branch.* `indep/enum_conn.c` (prover) processes vertices in label order exactly as above: at turn $c$ it offers (a) an edge $\{c,a,b\}$, $c<a<b<\ell_0$, lexicographically after the previous (a)-edge of the turn, (b) an edge $\{c,a,\ell\}$, $c<a<\ell_0$, with $a$ after the previous (b)-edge's, (c) an edge $\{c,\ell,\ell+1\}$, and "end of turn", allowed iff $c+1<\ell$; every edge must keep the hypergraph linear and all degrees $\le D$; after each placed edge it stops the branch when $|P|=M$ (output iff $\ell=N$ and $\tau(P)\ge T_0$) and otherwise continues only if $\ell\le N$, $\ell+2(M-|P|)\ge N$ and $\tau(P)\ge T_0-(M-|P|)$ (exact branching hitting-set test). `conn_dfs2.c`/`conn_dfs2_all.c` (falsifier; the two differ only in how many outputs they print) use the same turns, with the order (a) < (b) < (c) encoded by the key "number of new vertices, then old labels" (type (a) keys $o_1\cdot1000+o_2<10^6$, type (b) keys $10^6+1000\,o$, type (c) key $2\cdot10^6$; keys must be non-decreasing within a turn; equal keys are possible only for type (c), since two (a)- or (b)-edges with equal keys share two vertices) and with (a)/(b) choices ranging over all labelled $o>c$ (a superset); its tests are `v>n || v+2r<n`, `cur>=v` (never true on the canonical branch by (D3)), the exact cover test `cover_le(all, tau0-r-1)` (prunes only if $\tau(P)\le T_0-r-1$), the degree tests, and at $|P|=M$ the same cover test followed by the output test `v==n`. By (D1)–(D5) the canonical branch of $H$ passes every test of both programs and ends in an output, which is isomorphic to $H$ (via the labelling). Conversely every output is a connected linear 3-graph on exactly $N$ vertices with $M$ edges, $\tau\ge T_0$ and $\Delta\le D$ (each new edge passes the pair test and contains the current vertex, which is 0 or lies in an earlier edge). **Hence each program outputs at least one labelled copy of every isomorphism class of connected linear 3-graphs with these parameters, and nothing else; "found = 0" proves that a cell is empty.**

*Validation against brute force* (independent of the canonical-growth idea): `indep/bf_cells.c` enumerates all labelled linear 3-graphs on $[n]$ (DFS over triples in index order, no symmetry reduction) and tallies the connected spanning ones by $(m,\tau,\Delta)$. `indep/compare_bf.py mine|theirs` checks, for every $3\le n\le9$, every $m$, every $t$ from 0 to $\tau_{\max}+1$ and $D\in\{2,3,\Delta_{\max},100\}$, that the brute-force number of labelled graphs with $\tau\ge t$, $\Delta\le D$ equals $\sum n!/|\mathrm{Aut}|$ over the isomorphism classes of the enumerator's output (classes and $|\mathrm{Aut}|$ by networkx VF2 on the vertex–edge incidence graph with the two sides kept apart; side-preserving automorphisms of the incidence graph correspond bijectively to vertex permutations preserving the edge set, because distinct edges are distinct vertex sets; a class on the vertex set $[n]$ has exactly $n!/|\mathrm{Aut}|$ labelled copies), and that every output has the required parameters. Commands: `cd experiments/prover/L007/indep; for n in 3 4 5 6 7 8 9; do ./bf_cells $n > bf_n$n.txt; done; python3 compare_bf.py mine; python3 compare_bf.py theirs`. Output: `mine cells compared: 393 mismatches: 0 nonempty cells: 243 total classes: 1600` (369 s) and `theirs cells compared: 393 mismatches: 0 nonempty cells: 243 total classes: 1600` (463 s; outputs `compare_bf_mine.json`, `compare_bf_theirs.json`). This proves that both programs are exhaustive and sound on every cell with $n\le9$ (a test of the implementations; the general statement is Lemma D).

*Direct brute force on three cells used in the proof* (`indep/bf_cell.c`: all labelled linear 3-graphs on $[n]$ with exactly $m$ edges by DFS over triples in index order, pruned only by $\tau(P)\ge t-(m-|P|)$, with $\tau$ computed by testing all vertex sets of size $t-1$; connectivity and spanning checked at the leaves): `./bf_cell 10 6 4` → `nodes=14908931 labelled=0` (16 s) and `./bf_cell 11 5 4` → `nodes=2300156 labelled=0` (4 s), so the window cells (10,6,4) and (11,5,4) are empty by a method that uses no canonical labelling at all; `./bf_cell 10 7 4` → `nodes=150569981 labelled=6652800` (119 s), which equals $\sum10!/|\mathrm{Aut}|=10!\,(1/4+1/2+1/2+1/4+1/6+1/6)$ over the six classes of C2 ($|\mathrm{Aut}|=4,2,2,4,6,6$), so the 637 outputs of C2 represent every labelled (10,7,4) graph (`indep/bf_cell_n10_11.log`). (The cells with $n\ge12$ are out of reach of this brute force.)

**C1. Window cells with $n\le13$ (Lemma A, Step 2.3).**
- Falsifier program, recompiled from source: `gcc -O2 -o bin/conn_dfs2 ../../falsify/i11-inequality/conn_dfs2.c; for c in "5 3 2" "8 4 3" "10 6 4" "11 5 4" "13 7 5" "12 9 5"; do ./bin/conn_dfs2 $c | tail -n 1; done` (in experiments/prover/L007; log `rerun/window_cells_n13.log`). Output: `nodes=16 found=0`, `nodes=151 found=0`, `nodes=8448 found=0`, `nodes=197 found=0`, `nodes=19596 found=0`, `nodes=18326058 found=0` (6 s for the last), identical to the falsifier's `conn2_batch.log` and `results_verify_cells_n13.json`.
- Independent program: `cd indep; gcc -O2 -Wall -o enum_conn enum_conn.c; ./enum_conn N M T0 1000 0` for the same six cells. Output: `calls=52 found=0`, `calls=265 found=0`, `calls=15580 found=0`, `calls=249 found=0`, `calls=23256 found=0`, `calls=34515249 found=0` (5 s).
- Additional, different method (falsifier's `sat_cell.py`, CaDiCaL 1.5.3 via pysat; ordered class $O$ with lazy $F_7$ cuts, exactly $m$ edges, $\alpha\le n-\tau_0$, connectivity not imposed): `python3 sat_cell.py 8 4 3`, `10 6 4`, `11 5 4` re-run here: UNSAT in 0.1 s, 40.7 s and 144.0 s (`rerun/sat_cells.log`). (The module docstring of `sat_cell.py` says "F7 NOT imposed", but the code does add an $F_7$ cut for every $F_7$ copy of each model until a model is $F_7$-free or the formula is UNSAT, i.e. it decides class $O$.) The cell (12,9,5) is also consistent with L002, whose class-$O$ census (with K30) has no 12-vertex pattern with $m=9$ and $\alpha\le7$; that census is in a smaller class and is not used.
- What this proves: Step 2.3.

**C2. The tight cells (13,8,≥5) and (10,7,≥4) (Step 5).**
- `./bin/conn_dfs2_all 13 8 5 > rerun/conn_all_13_8_5.txt` → `nodes=1295881 found=159`; `./bin/conn_dfs2_all 10 7 4 > rerun/conn_all_10_7_4.txt` → `nodes=102701 found=637`; both files byte-identical (`cmp`) to the falsifier's `conn_all_13_8_5.txt`, `conn_all_10_7_4.txt`.
- Independent: `./enum_conn 13 8 5 1000 1` → `calls=1773159 found=159`; `./enum_conn 10 7 4 1000 1` → `calls=220291 found=637` (`indep/mine_13_8_5.txt`, `indep/mine_10_7_4.txt`). The two programs output the same labelled graphs (identical sets of edge sets, 159 and 637), as expected since both follow the canonical process of Lemma D; `calls` and `nodes` count different things and are not comparable.
- Isomorphism classes (`python3 indep/iso_compare.py <mine> <theirs> details`): (13,8,≥5): 2 classes in each list, the same 2; (10,7,≥4): 6 classes in each list, the same 6. All have $\tau$ exactly 5, resp. 4 (computed), and all satisfy (P3). The two (13,8,5) classes are $F_7$ plus three edges: $\{(0,1,2),(2,3,4),(3,5,6),(4,7,8),(4,9,10),(7,11,12),(8,9,11),(8,10,12)\}$ (an $F_7$ centred at 8: $\{4,7,8\},\{8,9,11\},\{8,10,12\},\{4,9,10\},\{7,11,12\}$) and $\{(0,1,2),(2,3,4),(3,5,6),(4,7,8),(4,9,10),(4,11,12),(7,9,11),(8,10,12)\}$ (centred at 4). Of the six (10,7,4) classes one contains $F_7$ (126 of the 637 labelled outputs) and five are $F_7$-free (511 outputs), as in `tight_classes.py`/`results_tight_classes.json`.
- What this proves: by Lemma D, every connected linear 3-graph with $(n,m)=(13,8)$, $\tau\ge5$ (resp. $(10,7)$, $\tau\ge4$) is isomorphic to one of the 159 (resp. 637) listed graphs. Isomorphism testing is not load-bearing anywhere in the proof: the class counts are descriptive, and C3, C4 and C5 process every labelled output.

**C3. $F_7$ tests (Steps 5.1, 5.2, 6.3).**
- *Lemma F.* In a linear 3-graph, five distinct edges form a copy of $F_7$ iff their union has exactly 7 vertices and, counted within these five edges, one vertex has degree 3 and six have degree 2. Proof: $F_7$ has this degree pattern (vertex 0 has degree 3, the others 2). Conversely let $p$ be the degree-3 vertex and $E_1,E_2,E_3$ the three edges at $p$; by linearity they meet only in $p$, so they cover $p$ and six further vertices, i.e. all 7. The other two edges $T_1,T_2$ avoid $p$; each of the six vertices has degree 2, so lies in exactly one of $T_1,T_2$, hence $T_1,T_2$ partition the six vertices; by linearity $|T_j\cap E_i|\le1$, so each $T_j$ takes exactly one vertex from each $E_i\setminus\{p\}$. Naming $E_i\setminus\{p\}=\{2i-1,2i\}$ with $2i-1\in T_1$ and $p=0$ gives exactly $\{012,034,056,135,246\}$.
- Independent test `indep/f7check.py` (tests all 5-subsets of edges by Lemma F; positive control $F_7$, negative control the Fano plane minus two lines, which has 7 vertices and 5 edges but degrees 3,3,2,2,2,2,1). Command (in `indep/`): `python3 f7check.py ext_indep_hits.txt:HIT ../rerun/ext_vertex_hits.txt:HIT ../rerun/conn_all_13_8_5.txt:FOUND ../rerun/conn_all_10_7_4.txt:FOUND ../rerun/conn2_all_14_11_6_deg3.txt:FOUND mine_14_11_6_deg3.txt:FOUND mine_13_8_5.txt:FOUND mine_10_7_4.txt:FOUND`. Output: 3,186 of 3,186 hits contain $F_7$ (both hit files); 159 of 159 (13,8,5) graphs contain $F_7$; 126 of 637 (10,7,4) graphs contain $F_7$; 998 of 998 (14,11,6,Δ≤3) graphs contain $F_7$ (in both lists); every graph is linear (`indep/f7check_results.json`).
- The falsifier's tests use `e757/cpsat_model.py:find_f7`, which enumerates a vertex $p$, three edges at $p$ and the four ways of choosing $T_1\ni$ (first other vertex of $E_1$) and checks $T_1,T_2\in E$; it is complete because the image of the unique degree-3 vertex of $F_7$ must be such a $p$. Their outputs agree: `analyze_hits.py` (3,186 hits, 0 $F_7$-free), `tight_classes.py` (both (13,8,5) classes contain $F_7$; 5 of the 6 (10,7,4) classes are $F_7$-free), `ud_check.py` / `results_ud_check.json` (998 graphs, 0 $F_7$-free).

**C4. The vertex extensions (Step 5.2).**
- Input: `python3 build_input.py` rebuilds the 796-line input (the 159 graphs of (13,8,5) and the 637 graphs of (10,7,4), each plus the edge $\{10,11,12\}$) from the re-run outputs of C2 and finds it equal, as a multiset of edge sets, to the falsifier's `ext_vertex_input.txt` (796 distinct lines: 159 of the first kind, 637 of the second).
- Falsifier program, recompiled: `./bin/ext_vertex_all < ../../falsify/i11-inequality/ext_vertex_input.txt > rerun/ext_vertex_hits.txt` → `graphs=796 tested=6699128 hits(tau>=6)=3186` (5 s), byte-identical to the stored `ext_vertex_hits.txt`. Its $\tau$ test is the exact branching test "no transversal of size $\le5$" on all 11 edges.
- Independent program `indep/ext_indep.c` with a different $\tau$ test: it first checks $\tau(G)=5$ exactly for each input $G$ (no 4-transversal, some 5-transversal; `bad_tau=0`), lists all 5-transversals of $G$, and declares $\tau(H)\ge6$ iff no 5-transversal of $G$ meets all three new pairs (correct because a transversal of $H$ with at most 5 vertices cannot contain the new vertex: its rest would be a 4-transversal of $G$). Command: `./ext_indep < ../rerun/ext_input_rebuilt.txt > ext_indep_hits.txt` → `graphs=796 bad_tau=0 tested=6699128 hits(tau>=6)=3186` (0.6 s). `python3 compare_hits.py`: the two hit lists are identical as sets of edge sets (3,186 distinct); 954 hits come from (13,8,5) graphs (redundant for the proof: case (i) is already closed by C3) and 2,232 from the (10,7,4)+edge graphs: 1,386 from the $F_7$-containing (10,7,4) class and 846 from the five $F_7$-free classes; in each of these 846, every copy of $F_7$ uses the new vertex 13 (checked with the Lemma F test on all 5-edge subsets).
- The falsifier's own cross-check `crosscheck_ext.py` (numpy, 25 random input graphs, 210,104 extensions, 111 hits both ways) is superseded by the full independent run.
- What this proves (with C3): every 3-graph obtained from one of the 796 input graphs by adding a vertex 13 and three edges $\{13,a_i,b_i\}$ with pairwise disjoint pairs not inside an edge of the graph, and having $\tau\ge6$, contains $F_7$.

**C5. Route II (Step 6.3).**
- Falsifier: `conn_dfs2_all 14 11 6 3` → `maxdeg=3 n=14 m=11 tau0=6 nodes=1165338864 found=998` (`conn2_14_11_6_deg3.log`, `conn2_all_14_11_6_deg3.txt`); re-run here from the recompiled source: identical output, byte-identical file (`cmp`), 1,747 s under load (`rerun/conn2_all_14_11_6_deg3.txt`).
- Independent: `./enum_conn 14 11 6 3 1 > indep/mine_14_11_6_deg3.txt` → `enum_conn N=14 M=11 T0=6 DMAX=3 calls=2468940032 found=998` (815 s); the two lists are identical as sets of labelled edge sets (998 each). `python3 iso_compare.py mine_14_11_6_deg3.txt ../rerun/conn2_all_14_11_6_deg3.txt` → 1 isomorphism class in each list, the same class; `python3 member.py mine_14_11_6_deg3.txt ../rerun/conn2_all_14_11_6_deg3.txt` → all 998 outputs of each list are isomorphic to `f7_containing_violation.json` ($=D_{14}$ of Step 6.4).
- $F_7$: all 998 contain $F_7$ (C3, both tests).
- What this proves: by Lemma D, every connected linear 3-graph with $n=14$, $m=11$, $\tau\ge6$, $\Delta\le3$ contains $F_7$.

**C6. Remark cells (Step 9.1; not load-bearing).** `./bin/conn_dfs2 15 9 6` → `nodes=2459440 found=0` (0.8 s); `./bin/conn_dfs2 16 8 6` → `nodes=19144 found=0`; `./bin/conn_dfs2 15 10 6` → `nodes=186011577 found=0` (165 s); identical to the falsifier's `conn2_batch.log`. Independent (`indep/enum_conn`, same arguments with DMAX 1000): (15,9,6) `calls=2534511 found=0` (1 s), (16,8,6) `calls=18778 found=0`, (15,10,6) `calls=216656914 found=0` (91 s) (`indep/enum_remark_small.log`, `indep/enum_15_10_6.log`).

**C7. Witnesses and sanity data (Step 7).** `python3 witness_14_11.py` (e757.core, exact integers; A_base scaled by 4): among the (4,5) one-point extensions $A_{\rm base}\cup\{x\}$ ($x$ in a new AP) and their one-point deletions, 291 fourteen-point sets have exactly 11 APs, all with $h=9$; the normalized first one is $W$ (`witness_14_11.json`). $W$ re-checked from the definitions by `python3 check_witness_records.py` (first part plain Python, no e757): all 1,001 four-subsets have $\ge5$ distinct differences, the 11 APs are $(0,323,646)$, $(323,523,723)$, $(323,621,919)$, $(323,851,1379)$, $(523,566,609)$, $(523,572,621)$, $(566,569,572)$, $(569,595,621)$, $(569,646,723)$, $(572,609,646)$, $(595,723,851)$, and the largest Sidon subset (all subsets tested) has 9 elements. Fibonacci $\{F_3,\dots,F_{16}\}$: (4,5), $m=11$, $h=9$ (e757.core, same script, which also prints the record-set values used in the Sanity checks).

## Sanity checks
- I11 and Theorem 1 on the record sets (e757.core): $A_{\rm base}$ $(n,m,\tau)=(14,12,6)$, $s=0$ (I11 equality; $m=12$, so not in the cell of Theorem 1); the two omega 12-point sets $(12,10,5)$, $s=1$; $W$ and the Fibonacci set $\{F_3,\dots,F_{16}\}$ $(14,11,5)$, $s=9$, $\tau=5\le5$ as Theorem 1 requires. Glued sets (Ma–Tang Lemma 3.6) of the records have $n\ge24$, so they never fall in the cell $(14,11)$; on them I11 holds with the falsifier's numbers (T6b: $A_{\rm base}+A_{\rm base}$ $(28,24,12)$, $s=0$; $A_{\rm base}+$12-point $(26,22,11)$, $s=1$).
- Realizable data at $(14,11)$: `python3 sanity_m11_sets.py 200`: from the first 200 classes of data/census_n14_m12_classes.jsonl.gz, 55,465 fourteen-point (4,5)-sets with exactly 11 APs (class plus a point $x$ in a new AP, minus a point; distinct within each class), histogram of $h$: $\{9: 55{,}465\}$ (`sanity_m11_sets_K200.json`). The falsifier's x3 test (all $2^{15}$ subsets of all 141,153 fifteen-point extensions of the 2,910 classes, `results_ext14_single.json`: 4,625,301,504 subsets, 0 I11 violations) implies in particular that every 14-point subset with 11 APs there has $\tau\le5$.
- The ordered prefix-split DFS of Q11 (class $O$ with K30 at $(14,11,\alpha\le8)$, experiments/20261014-1005-census-dfs/n14m11dfs, still running): 1,061 of 3,437 prefixes done at 2026-10-17 03:14 UTC, all with `solutions = 0`, `timed_out = 0`, and empty outputs, as Theorem 1 predicts for every prefix.
- Positive controls: the enumerators do find graphs where they exist (637 and 159 in the tight cells; 998 $F_7$-containing graphs at (14,11,6,Δ≤3); 243 non-empty cells with $n\le9$ reproduced exactly against brute force); the $F_7$ tests detect $F_7$ and reject the Fano plane minus two lines.
- Lemma A (the only input of Lemmas B and C) is consistent with all realizable and abstract data: the falsifier found no I11 violation on any subset of the record sets, of the 2,910 and 54,243 census classes, of their 141,153 and 1,887,566 one-point extensions, or of the 2,226,490 and 205,529 abstract census patterns (experiments/falsify/i11-inequality/README.md §1, tests T1–T3, x2–x6). Lemma B's hypothesis (P2) matters: the falsifier's $F_7$-containing example `f7_containing_violation.json` is a connected (14,11,6) 3-graph with $\Delta=3$, and it is (up to isomorphism) the only one (Step 6.4).
- The two routes agree: of the 3,186 hits of Route I (C4), 1,180 have maximum degree 3, and every one of them is isomorphic to $D_{14}$, the unique graph of Route II; the other 2,006 hits have maximum degree 4 and are excluded by Lemma B alone. The direct brute force (C0) reproduces the labelled count of the tight cell (10,7,4) used in Route I exactly.

## Falsifier report
experiments/falsify/i11-inequality/README.md (VERDICT HOLDS-ON-DATA for I11 on all realizable data; §2–§3 contain the reduction and the (14,11,6) argument certified here; no counterexample to I11 in $O^+$ was found anywhere). Discrepancies noted while checking it: its §2 list of window cells omits (5,3,2) (decided anyway by `verify_cells.py`); the docstring of `sat_cell.py` misdescribes its $F_7$ handling (the code imposes $F_7$-freeness lazily). Neither affects any result.
