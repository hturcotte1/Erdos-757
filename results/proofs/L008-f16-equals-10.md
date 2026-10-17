# f(16) = 10: every 16-point (4,5)-set has a Sidon subset of size 10, so no 16-point (4,5)-set beats the ratio 4/7
CLAIM-TYPE: lemma + certificate (computer-assisted proof: the L007 method one level up; every enumeration and every extension computation that the proof uses was run by two independently written programs)
TYPE: certificate
STATUS: ACCEPTED by referee rounds 1, 2 and 3 (results/reviews/L008-f16-equals-10__referee__20261017T070236Z.md, __referee__20261017T082214Z.md, __referee__20261017T080425Z.md; round 3 on the strongest available model; independent generation with nauty genbg and two further generators, a decomposition-free route over all 261 linear (15,11,tau>=6,Delta<=3) graphs, definitional F7 and e(S) filters, SHA-256 byte-for-byte reproduction of every computation, and 147,943 sixteen-point (4,5)-sets all with h = 10; rounds 2 and 3 also show that Henning-Yeo (K8) is dispensable for Lemma A' and that L007 Theorem 2 and K8 are not needed in Step 3.1, so DEPENDS ON overstates those two dependencies); novelty CLEAR (__scout__20261017T061250Z.md). Submitted 2026-10-17 06:09 UTC; two editorial fixes after round 1 (07:17 UTC)
DEPENDS ON:
- L007 [verified-here, ACCEPTED by referee rounds 1, 2 and 3; K51]: its Lemma A (I11 on $O^+$ for $n\le13$), its Theorem 1 (every $H\in O^+$ with $(n,m)=(14,11)$ has $\tau\le5$), its Lemma D (computation C0: exhaustiveness of the canonical-growth enumerators, validated against brute force), its Lemma F (computation C3: the $F_7$ test), and its computation C6 (no connected linear 3-graph in the cells (15,9,6), (15,10,6), (16,8,6), by two programs). Everything of L007 is used except its Corollaries 3 and 4.
- K3–K7 [published] (Ma–Tang Props 2.1, 2.2, Lemmas 2.3–2.5; Gyárfás–Lehel Prop 2.6): the AP pattern of a (4,5)-set lies in $O\subseteq O^+$ and $h=\alpha$ (Step 7.1).
- K8 [published] (Henning–Yeo 2021 Thm 7 as cited in Ma–Tang Thm 5.3: $17\tau\le5n+3m$ for linear $F_7$-free 3-graphs; full text not obtained by the project, kb/notes/henning_yeo_2021_affine.md). Used in Step 1 (window cells), Step 3.1 ($\tau=7$, $m\ge13$) and, through L007, in Lemma A.
- Not used: K24/K35 (the upper bound $f(16)\le10$ is re-proved here by an explicit set), K30, K31, the forbidden cores, L002–L006 (L002 appears only in a consistency check of the falsifier).
- Programs. Falsifier (experiments/20261017-0300-n16-via-i11/): `conn_dfs3.c`, `conn_dfs3s.c` (= `conn_dfs3.c` with `SD=6`), `ext_vertex2.c`, `post.py`, `prep_R12.py`, `slack_cells.py`, `classes_B.py`, `check_R12_classes.py`, `moves_check.py`, `random_search_B.py`, `crosscheck_ext2.py`; and, through L007, experiments/falsify/i11-inequality/`conn_dfs2.c`. Prover, written without reusing that code (experiments/prover/L008/): `indep/enum_conn.c` (the L007 enumerator, unchanged), `indep/ext_indep2.c`, `indep/filter_hits.c`, `decomp.py`, `build_inputs.py`, `compare_found.py`, `compare_hits.py`, `breakdown_A.py`, `classes_of.py`, `control_sample.py`, `witness_16.py`; all commands in `experiments/prover/L008/reproduce.sh`.

## Statement

Conventions and the classes $O^+$, $O$ are those of L007: a 3-graph is linear if two edges share at most one vertex; $F_7=\{012,034,056,135,246\}$ and "contains $F_7$" means five edges forming a copy of $F_7$; $O^+$ is the class of 3-graphs with (P1) linear, (P2) $F_7$-free, (P3) $e(S)\le|S|-2$ for every vertex set $S$ with $|S|\ge2$; $O\subseteq O^+$ is the class of ordered midpoint patterns. $s(H)=3n+2m-11\tau(H)$ is the I11 slack.

**Theorem 1 (abstract).** Every $H\in O^+$ with $n=16$ vertices has $\tau(H)\le6$, i.e. $\alpha(H)\ge10$. (By (P3), $m\le14$, so this covers every number of edges.)

**Theorem 2.** Every 16-point (4,5)-set $A$ has $h(A)\ge10$, and $C_{16}=A_{\rm base}\cup\{-323,5000\}$ is a 16-point (4,5)-set with $h(C_{16})=10$. Hence $f(16)=10$. Equivalently, no 16-point (4,5)-set beats the ratio $4/7$ (that would need $h\le\lceil4\cdot16/7\rceil-1=9$): the smallest size at which a new record was possible (kb/00_START_HERE.md §4) is closed.

**Lemma A′ (I11 below 16 vertices).** Every $H\in O^+$ with $n\le15$ satisfies $11\,\tau(H)\le3n+2m$.

**Corollary 3.** Every $H\in O^+$ with $n\le16$ satisfies $11\,\tau(H)\le3n+2m$.

**Corollary 4.** The sizes $n\le30$ at which a set beating $4/7$ can still exist are now $n=18,20,22,23,25,27,29,30$ (the table of kb/00_START_HERE.md §4 without $n=16$); $f(17)=10$ was already known and is consistent with $f(16)=10\le f(17)$; $f(18)\in\{10,11\}$ is unchanged.

Tags: Theorems 1, 2, Lemma A′ and Corollaries 3, 4 are **[verified-here] conditional on referee acceptance of this certificate** (L007 is accepted; until then [derived-here], computer-assisted). Scope: nothing is claimed for $n\ge17$.

## Proof

### Step 0. Facts used (as in L007 Step 0)
0.1 $n$, $m$, $\tau$ and hence $s$ are additive over components; a single vertex has $s=3$; a component with an edge has at least 3 vertices (L007 0.1).
0.2 $O^+$ is closed under induced subhypergraphs $H[S]$ (L007 0.2); in particular $H-v\in O^+$ and every component of a member of $O^+$ is in $O^+$.
0.3 For $H\in O^+$: $\tau\le m$; $\tau(H)-1\le\tau(H-v)\le\tau(H)$; $m\le n-2$ if $n\ge2$; $17\tau\le5n+3m$ (K8) (L007 0.4).
0.4 A connected 3-graph with $m\ge1$ edges has $n\le2m+1$ (L007 0.5).
0.5 Degrees do not increase under deletion: $d_{H-v}(u)\le d_H(u)$.

### Step 1. Window cells up to 16 vertices (arithmetic)
With $\mathrm{lo}(n,m)=\lfloor(3n+2m)/11\rfloor+1$ and $\mathrm{hy}(n,m)=\lfloor(5n+3m)/17\rfloor$ as in L007 Step 1, the connected cells $(n,m)$ ($\lceil(n-1)/2\rceil\le m\le n-2$) with $\mathrm{lo}\le\min(\mathrm{hy},m)$ and $n\le16$ are (L007 Step 1 for $n\le15$; `decomp.py` part (a) and L007's `cells_table.py 16` for all rows):
- $n\le13$: (5,3,2), (8,4,3), (10,6,4), (11,5,4), (12,9,5), (13,7,5) (written $(n,m,\tau)$ with the single admissible $\tau=\mathrm{lo}=\mathrm{hy}$);
- $n=14$: (14,11,6) [row: $m=7..10$: (lo, hy) = (6, 5); $m=11$: (6, 6); $m=12$: (7, 6)];
- $n=15$: (15,9,6), (15,10,6) [row: $m=7,8$: (6, 5); $m=9,10$: (6, 6); $m=11,12,13$: (7, 6)];
- $n=16$: (16,8,6), (16,13,7), (16,14,7) [row: $m=8$: (6, 6); $m=9..12$: (7, 6); $m=13$: (7, 7), from $\lfloor74/11\rfloor+1=7$, $\lfloor119/17\rfloor=7$; $m=14$: (7, 7), from $\lfloor76/11\rfloor+1=7$, $\lfloor122/17\rfloor=7$].

### Step 2. Proof of Lemma A′
2.1 Let $H\in O^+$, $n\le15$, and suppose $s(H)<0$. As in L007 Step 2.1–2.2, some component $C\in O^+$ has $s(C)<0$, $n_C\ge3$, $m_C\ge1$, and $(n_C,m_C,\tau(C))$ lies in a window cell with $n_C\le15$: $\tau(C)\ge\mathrm{lo}$.
2.2 If $n_C\le13$: impossible by L007 Lemma A (applied to $C$).
2.3 If $(n_C,m_C)=(14,11)$: $\tau(C)\ge6$ contradicts L007 Theorem 1 ($C\in O^+$ has $\tau\le5$).
2.4 If $(n_C,m_C)\in\{(15,9),(15,10)\}$: $C$ is a connected linear 3-graph with $\tau\ge6$, and there is none (these two cells are NOT part of L007's certified statement, which L007 lists as an uncertified remark; they were verified independently by L007 referee rounds 1 and 3 and by L008 referee round 1 with nauty genbg; L007 computation C6: `conn_dfs2 15 9 6` → 2,459,440 nodes, found 0; `conn_dfs2 15 10 6` → 186,011,577 nodes, found 0; independently `enum_conn 15 9 6` → found 0 and `enum_conn 15 10 6` → found 0).
2.5 Hence $s(H)\ge0$. $\square$

### Step 3. Lemma B′ (degrees at 16 vertices)
Let $H\in O^+$ with $n=16$ and $\tau(H)\ge7$.
3.1 $m\le14$ (Step 0.3). K8: $17\,\tau(H)\le80+3m\le122$, so $\tau(H)\le7$, hence $\tau(H)=7$; and $119\le80+3m$ gives $m\ge13$ ($3\cdot12=36<39$). So $m\in\{13,14\}$.
3.2 For every vertex $v$: $H-v\in O^+$ has 15 vertices, $m-d(v)$ edges and $\tau(H-v)\ge6$ (Step 0.3). Lemma A′: $11\,\tau(H-v)\le45+2(m-d(v))\le73-2d(v)$. As $77>73$, $\tau(H-v)=6$; and $66\le45+2m-2d(v)$, i.e. $2d(v)\le2m-21$, so $d(v)\le m-11$ (integers).
3.3 If $m=13$, then $d(v)\le2$ for all 16 vertices and $39=3m=\sum_vd(v)\le32$, a contradiction. Hence $m=14$, $d(v)\le3$ for every $v$, and with $d_3$ vertices of degree 3: $42=\sum_vd(v)\le3d_3+2(16-d_3)=32+d_3$, so $d_3\ge10$. In particular $H$ has a vertex of degree 3.

### Step 4. Lemma C′ (the structure of $H-v$)
Let $H$ be as in Step 3, $v$ a vertex of degree 3, $G:=H-v$.
4.1 $G\in O^+$ has $n=15$, $m=14-3=11$, $\tau(G)=6$ (Step 3.2), $s(G)=45+22-66=1$, and $\Delta(G)\le\Delta(H)\le3$ (Step 0.5).
4.2 Every component of $G$ is in $O^+$ with at most 15 vertices, so has slack $\ge0$ by Lemma A′; the slacks are integers adding up to 1 (Step 0.1), so exactly one component has slack 1 and all others have slack 0; there is no isolated vertex (slack 3). Each component $C$ is a connected 3-graph with $3\le n_C\le15$, $\lceil(n_C-1)/2\rceil\le m_C\le n_C-2$, and $3n_C+2m_C-11\tau(C)\in\{0,1\}$.
4.3 (Connected cells of slack 0 and 1, $n\le15$.) Slack 0: $m\equiv4n\pmod{11}$ (L007 Step 4.3); for $n\le13$ the solutions are (3,1,1), (10,7,4), (13,8,5) (L007 table); $n=14$: $4\cdot14\equiv1$, range $[7,12]$, $m=12$: (14,12,6); $n=15$: $60\equiv5$, range $[7,13]$: none. Slack 1: $3n+2m\equiv1$, i.e. $2m\equiv1-3n$, i.e. $m\equiv6(1-3n)\equiv4n+6\pmod{11}$; the range has at most 7 < 11 elements:

| $n$ | $4n+6 \bmod 11$ | range of $m$ | slack-1 cell |
|---|---|---|---|
| 3 | 7 | [1,1] | none |
| 4 | 0 | [2,2] | none |
| 5 | 4 | [2,3] | none |
| 6 | 8 | [3,4] | none |
| 7 | 1 | [3,5] | none |
| 8 | 5 | [4,6] | (8,5,3) |
| 9 | 9 | [4,7] | none |
| 10 | 2 | [5,8] | none |
| 11 | 6 | [5,9] | (11,6,4) |
| 12 | 10 | [6,10] | (12,10,5) |
| 13 | 3 | [6,11] | none |
| 14 | 7 | [7,12] | (14,7,5) |
| 15 | 0 | [7,13] | (15,11,6) |

($\tau=(3n+2m-1)/11$. All nine cells also satisfy $\tau\le m$ and K8: (8,5,3) $51\le55$; (11,6,4) $68\le73$; (12,10,5) $85\le90$; (14,7,5) $85\le91$; (15,11,6) $102\le108$; (14,12,6) $102\le106$; and L007's three. `decomp.py` part (b), which tries every $\tau$ from 0 to $m$ instead of solving the congruence, prints the same two lists, as does the falsifier's `slack_cells.py`.)
4.4 (Decompositions.) The component types must add up to $(n,m)=(15,11)$ with exactly one slack-1 type. Slack-1 type (15,11,6): nothing remains. (14,7,5): remainder (1,4), and no slack-0 type has 1 vertex. (12,10,5): remainder (3,1) = (3,1,1). (11,6,4): remainder (4,5); the only slack-0 type with at most 4 vertices is (3,1,1), leaving (1,4): impossible. (8,5,3): remainder (7,6); slack-0 types with at most 7 vertices: only (3,1,1), leaving (4,5), then (1,4): impossible. Hence (`decomp.py` part (c), an exhaustive search over all multisets of slack-0, slack-1 and isolated-vertex types with total slack exactly 1, confirms):
(A) $G=R\sqcup E$ with $R$ a connected linear 3-graph with $(n,m,\tau)=(12,10,5)$ and $E$ a single edge, or
(B) $G$ is a connected linear 3-graph with $(n,m,\tau)=(15,11,6)$.
In both cases $\Delta(G)\le3$, so $\Delta(R)\le3$ in case (A).

### Step 5. The extension step
5.1 Let $\{v,a_i,b_i\}$, $i=1,2,3$, be the edges of $H$ at $v$. By (P1) the pairs $\{a_i,b_i\}$ are pairwise disjoint and none lies inside an edge of $G$ (L007 Step 5.2). Each $a_i,b_i$ lies in exactly one edge at $v$, so $d_G(a_i)=d_H(a_i)-1\le2$, and likewise for $b_i$.
5.2 Case (A). By L007 Lemma D (C0 there), $R$ is isomorphic to one of the 145,033 labelled outputs $R_0$ (vertex set $\{0,\dots,11\}$) of the enumeration C2 below (connected linear, $(n,m)=(12,10)$, $\tau\ge5$, $\Delta\le3$). Choose an isomorphism $\varphi:G\to G_0:=R_0+\{12,13,14\}$. The pairs $\varphi(\{a_i,b_i\})$ are pairwise disjoint, not inside an edge of $G_0$, with $G_0$-degrees $\le2$, so $H_0:=G_0+\{15,\varphi(a_i),\varphi(b_i)\}_{i=1,2,3}$ is one of the 67,920,994 extensions enumerated in C4, and $\varphi\cup\{v\mapsto15\}$ is an isomorphism $H\to H_0$. As $\tau(H_0)=\tau(H)=7$, $H_0$ is one of the 31,673 hits of C4. By C5 every hit violates (P3); hence $H$ violates (P3), a contradiction.
5.3 Case (B). By L007 Lemma D, $G$ is isomorphic to one of the 50,606 labelled outputs $G_0$ (vertex set $\{0,\dots,14\}$) of the enumeration C3 below (connected linear, $(n,m)=(15,11)$, $\tau\ge6$, $\Delta\le3$). Exactly as in 5.2, $H$ is isomorphic to one of the 159,914,042 extensions of C4 with $\tau=7$, i.e. to one of its 173,687 hits. By C5 every hit contains $F_7$ (and also violates (P3)); hence $H$ contains $F_7$, contradicting (P2).
5.4 Both cases are impossible, so $\tau(H)\le6$ for every $H\in O^+$ with $n=16$. This proves Theorem 1. $\square$

### Step 6. Corollary 3
Let $H\in O^+$ with $n\le16$ and $s(H)<0$. Some component $C\in O^+$ has $s(C)<0$ and lies in a window cell with $n_C\le16$ (Step 2.1). $n_C\le15$ is impossible by Lemma A′. If $n_C=16$, then $C=H$ is connected, and $(16,m_C,\tau(C))$ is (16,8,6), (16,13,7) or (16,14,7) (Step 1): the first is excluded by L007 C6 (`conn_dfs2 16 8 6` → 19,144 nodes, found 0; `enum_conn 16 8 6` → found 0), the other two by Theorem 1 ($\tau\le6$). $\square$

### Step 7. Theorem 2 and Corollary 4
7.1 (Realizable patterns.) For a (4,5)-set $A$ the rank-order AP pattern $H(A)$ lies in $O\subseteq O^+$ and $h(A)=\alpha(H(A))=|A|-\tau(H(A))$ (L007 Step 8.1: K3–K7). If $|A|=16$, Theorem 1 gives $\tau(H(A))\le6$, so $h(A)\ge10$.
7.2 (Upper bound.) $C_{16}=\{-323,0,136,200,243,246,249,272,286,298,323,400,528,596,1056,5000\}$ is a (4,5)-set with 13 three-term APs and $h=10$ (C6, checked from the definitions). Hence $f(16)\le10$, so $f(16)=10$. ($f(16)\le10$ was also known, K24/K35.)
7.3 (Corollary 4.) By kb/00_START_HERE.md §4, beating $4/7$ at size $n$ needs $h\le\lceil4n/7\rceil-1$, which is $9$ at $n=16$; Theorem 2 excludes it. The other rows of that table (all $n\ne16$) are unaffected. $f$ is non-decreasing (deleting a point of an $(n+1)$-point (4,5)-set leaves an $n$-point (4,5)-set with no larger $h$), so $10=f(16)\le f(17)$, consistent with the known $f(17)=10$; for $n=18$ this gives only $f(18)\ge10$, the known bound. $\square$

### Step 8. Remarks (descriptive; not needed for the proof)
8.1 Case (A) in detail (`breakdown_A.py`). Of the 31,673 hits, 20,460 have an $R_0$ that contains $F_7$ and 1,116 an $R_0$ that is $F_7$-free but violates (P3); in all these 21,576 hits the three edges at 15 meet $\{12,13,14\}$. The remaining 10,097 hits have $R_0\in O^+$, and in every one of them no edge at 15 meets $\{12,13,14\}$, so $H_0=(R_0+15)\sqcup\{12,13,14\}$ with $R_0+15$ a 13-vertex 3-graph with 13 edges: $e(S)=|S|$ for $S=V(R_0)\cup\{15\}$. So for $R\in O^+$ the obstruction is always the same one: the three new edges stay inside $V(R)\cup\{v\}$ and overfill it.
8.2 Of the 145,033 labelled $R_0$, 36,916 contain $F_7$ and 186 more violate (P3); the 107,931 in $O^+$ form 149 isomorphism classes (`classes_of.py`; the falsifier's `prep_R12.py` finds the same 149 among 150 $F_7$-free classes). Of the 49 isomorphism classes of case (B) graphs, 27 contain $F_7$ and 3 more violate (P3), so only 19 lie in $O^+$ (`filter_hits` on the falsifier's class representatives). Every case-(B) hit violates both (P2) and (P3): in each there is an edge set $F$ with $|\bigcup F|=|F|+1$.
8.3 Where the hypotheses enter: K8 restricts Lemma A′ to the window cells of Step 1 and gives $\tau=7$, $m\ge13$ in Step 3.1; (P2) cannot be dropped from Lemma A′, since $F_7$ itself has $(n,m,\tau)=(7,5,3)$ and $s=-2$; (P3) is what kills case (A) (Step 8.1).

## Computer-verified steps

Machine: 4 cores shared with other jobs (load 6 to 14); wall times are indicative. All arithmetic is exact (integers, bitmasks). Paths are relative to experiments/prover/L008 unless stated; F = experiments/20261017-0300-n16-via-i11. Storage: the four main outputs are kept gzipped (`indep/mine_12_10_5_deg3.txt.gz`, `indep/mine_15_11_6_deg3.txt.gz`, `indep/hitsA_all_mine.txt.gz`, `indep/hitsB_mine_input_mine.txt.gz`); the other large intermediate files named below (inputs, re-run outputs, copies of falsifier files) were deleted after their SHA-256 sums were recorded in `checksums_large_outputs.txt` (the re-run `rerun/hitsB_ext_vertex2_rerun.txt` and the decompressed stored `F/hits_caseB.txt.gz` have the same SHA-256, i.e. are byte-identical); `reproduce.sh` regenerates all of them.

**C1. Cells and decompositions (Steps 1, 4).** `python3 decomp.py 16` (prover; output `decomp_output.txt`): (a) window cells for $n\le16$: (5,3), (8,4), (10,6), (11,5), (12,9), (13,7), (14,11), (15,9), (15,10), (16,8), (16,13), (16,14); (b) slack-0 cells $n\le15$: (3,1,1), (10,7,4), (13,8,5), (14,12,6); slack-1 cells: (8,5,3), (11,6,4), (12,10,5), (14,7,5), (15,11,6); (c) decompositions of (15,11) with total slack 1: [(15,11,6)] and [(3,1,1), (12,10,5)]; (d) check: decompositions of (13,8) with total slack 0: [(13,8,5)], [(3,1,1), (10,7,4)] (as in L007). The falsifier's `slack_cells.py` (`results_slack_cells.json`) gives the same lists and partitions.

**C2. Case (A) enumeration: connected linear (12,10,τ≥5), Δ≤3.**
- Prover: `./indep/enum_conn 12 10 5 3 1 > indep/mine_12_10_5_deg3.txt` → `calls=166011023 found=145033` (15 s).
- Falsifier program re-run: `./bin/conn_dfs3 12 10 5 3 0 0` → `nodes=56801671 found=145033` (59 s); split mode with the binary used in case (B): `./bin/conn_dfs3s 12 10 5 3 0 0 2 0` and `... 2 1` → 73,902 + 71,131 = 145,033, both processes reporting the same number `cnt=20543` of depth-6 split points (the falsifier's own partition check, $K=3$ with `SD`=4: 46,829 + 51,125 + 47,079 = 145,033, `F/results.json`).
- `python3 compare_found.py indep/mine_12_10_5_deg3.txt -- rerun/conn_dfs3_12_10_5.txt -- rerun/conn_dfs3s_12_10_5_part0.txt rerun/conn_dfs3s_12_10_5_part1.txt -- F/R12_labelled.txt.gz` → all four lists identical as sets of labelled edge sets (145,033 each).
- Exhaustiveness: L007 Lemma D covers `enum_conn` and `conn_dfs2`-type programs; `conn_dfs3.c` is `conn_dfs2_all.c` plus two optional prunes (disabled by the arguments `0 0`) and a slicing rule (C3 below); the identity of the four lists above checks this on this cell. Brute-force validation of `enum_conn` and of the same canonical scheme: L007 C0 (all cells with $n\le9$; direct brute force on (10,6,4), (10,7,4), (11,5,4)).
- Falsifier consistency checks (`check_R12_classes.py`, log `check_R12_classes.log`): all 39,309 realizable 12-point classes with maximum degree $\le3$ from the L002 census, and 14,813 of 14,813 sampled abstract (12,10) census patterns with maximum degree $\le3$, are isomorphic to one of the 150 $F_7$-free classes.

**C3. Case (B) enumeration: connected linear (15,11,τ≥6), Δ≤3.**
- Falsifier: `conn_dfs3s 15 11 6 3 0 0 2 0` and `... 2 1` (`F/g15_11_6_part0.txt.gz`, `part1`): 26,041 + 24,565 = 50,606 labelled graphs; 1,909,545,133 + 1,892,258,847 nodes; 32 CPU-min each.
- The slicing rule (`SLICE` macro of `conn_dfs3.c`): every process explores all nodes with fewer than `SD`=6 edges, counts in DFS order every node created with exactly 6 edges, and explores the subtree of the $c$-th such node iff $c\equiv I\pmod K$. The nodes with fewer than 6 edges, the order in which they are visited and the pruning tests are the same in every process (nothing above depth 6 depends on $I$), so the $K$ processes see the same sequence of depth-6 nodes and their subtrees partition the search tree. (The falsifier's README records that an earlier version had an inconsistent rule and found only 47 classes; the files used here were produced by the corrected version, timestamps 05:23–05:24 UTC.)
- Prover, independent single-process run: `./indep/enum_conn 15 11 6 3 1 > indep/mine_15_11_6_deg3.txt` → `enum_conn N=15 M=11 T0=6 DMAX=3 calls=6657152535 found=50606` (1,595 s).
- `python3 compare_found.py indep/mine_15_11_6_deg3.txt -- F/g15_11_6_part0.txt.gz F/g15_11_6_part1.txt.gz` → the prover's single-process list and the union of the falsifier's two slices are identical as sets of labelled edge sets (50,606 each). This checks the slicing rule and the split run independently. Descriptive: the 50,606 graphs form 49 isomorphism classes (`classes_of.py`), of which 27 contain $F_7$ and 3 more violate (P3), leaving 19 classes (15,335 labelled graphs) in $O^+$.
- Falsifier heuristic checks: single-incidence-move closure of the 49 classes (`moves_check.py`: 885 valid neighbours, all inside the 49 classes) and random local search (`random_search_B.py`, 2 × 600 s: 396 connected $\tau\ge6$ graphs, all inside the 49 classes).

**C4. Extensions (Step 5).** For each input graph $G$ on 15 vertices: all unordered triples of pairwise disjoint pairs of $V(G)$, no pair inside an edge of $G$, every endpoint of $G$-degree $\le2$; hit = $\tau(G+\{15,a_i,b_i\})\ge7$.
- Inputs: `python3 build_inputs.py A indep/mine_12_10_5_deg3.txt rerun/inputA_all.txt` (each of the 145,033 $R_0$ plus the edge (12,13,14)); case (B): `F/G_B_conn15.txt.gz` (the 50,606 falsifier graphs, decompressed to `rerun/inputB_falsifier.txt`) and, from the prover's own enumeration, `python3 build_inputs.py B indep/mine_15_11_6_deg3.txt rerun/inputB_mine.txt` (the same 50,606 graphs).
- Falsifier program, recompiled (`gcc -O2 -o bin/ext_vertex2 F/ext_vertex2.c`), exact branching test "no transversal of size $\le6$": `./bin/ext_vertex2 15 7 3 < rerun/inputA_all.txt` → `graphs=145033 tested=67920994 hits=31673` (183 s); `./bin/ext_vertex2 15 7 3 < rerun/inputB_falsifier.txt` → `graphs=50606 tested=159914042 hits=173687` (592 s), identical as a set to the stored `F/hits_caseB.txt.gz`.
- Prover program `indep/ext_indep2.c`, different test: it checks $\tau(G)=6$ exactly (no 5-transversal, some 6-transversal; `bad_tau=0` for every input), lists all 6-transversals of $G$, and declares $\tau(H)\ge7$ iff no 6-transversal of $G$ meets all three pairs (a transversal of $H$ with at most 6 vertices cannot contain 15, since its rest would be a 5-transversal of $G$); bitset implementation. `./indep/ext_indep2 15 6 3 < rerun/inputA_all.txt` → `graphs=145033 bad_tau=0 tested=67920994 hits=31673` (19 s); `./indep/ext_indep2 15 6 3 < rerun/inputB_falsifier.txt` → `graphs=50606 bad_tau=0 tested=159914042 hits=173687` (8 s). `python3 compare_hits.py`: case (A) hit sets of the two programs identical (31,673); case (B) identical to each other and to the stored file (173,687). On the prover's own case-(B) input: `./indep/ext_indep2 15 6 3 < rerun/inputB_mine.txt` → `graphs=50606 bad_tau=0 tested=159914042 hits=173687` (7 s), identical as a set to the stored hits. So in case (B) the whole chain enumeration → extension → filter has been run with prover code only.
- On the falsifier's class representatives: case (A) 149 classes: 74,916 extensions, 18 hits (both programs); case (B) 49 classes: 154,309 extensions, 218 hits (falsifier; numpy cross-check `crosscheck_ext2.py`).

**C5. Filters (Step 5).** Prover `indep/filter_hits.c`: linearity; $F_7$ by L007 Lemma F (all 5-edge subsets); (P3) in the equivalent form $|\bigcup F|\ge|F|+2$ for every non-empty edge set $F$ (equivalence: take $S=\bigcup F$; conversely $F=$ the edges inside $S$); exact $\tau$; maximum degree; connectivity. Controls: it flags $F_7$, accepts $F_7$ minus an edge and the Pasch configuration, and flags the Fano plane as violating (P3) but not containing $F_7$.
- Case (A): `./indep/filter_hits HIT < indep/hitsA_all_mine.txt` → `total=31673 linear=31673 contain_F7=21576 P3_violated=31673 F7free_and_P3_violated=10097 survivors=0 ... tau_range=[7,7] maxdeg_max=3`.
- Case (B): `./indep/filter_hits HIT < indep/hitsB_falsifier_input_mine.txt` → `total=173687 linear=173687 contain_F7=173687 P3_violated=173687 survivors=0 ... tau_range=[7,7] maxdeg_max=3` (34 s); the same line for `indep/hitsB_mine_input_mine.txt`.
- Falsifier's filters (`post.py`: `find_f7`, then (P3) over all $2^{16}$ vertex subsets, then an orderability SAT test): case (A) classes 18 hits: 0 with $F_7$, 18 violating (P3); case (B) classes 218 and all-labelled 173,687 hits: all contain $F_7$. Survivors 0 (`post_caseA.json`, `post_caseB.json`, `post_caseB_classes.json`).
- Control (the filters are not vacuous): `python3 control_sample.py; ./indep/filter_hits HIT < control_sample_hits.txt`: of 3,000 random extensions of the 149 case-(A) class inputs taken without the requirement $\tau\ge7$, 2,343 are linear, $F_7$-free and satisfy (P3) (`contain_F7=38`, `P3_violated=630`); the falsifier's analogous control found 2,634 of 3,000 surviving its three filters.
- What C2–C5 prove: by L007 Lemma D, every $G$ that can occur in case (A) or (B) is isomorphic to an input of C4; every extension of an input with $\tau\ge7$ and maximum degree $\le3$ violates (P3) (case A) or contains $F_7$ (case B).

**C6. The upper-bound witness (Step 7.2).** `python3 witness_16.py` (plain Python from the definitions, plus e757.core as a second opinion): $A_{\rm base}\cup\{-323\}$ is a (4,5)-set; the first $y\ge5000$ making $C_{16}=A_{\rm base}\cup\{-323,y\}$ a (4,5)-set is $y=5000$; $C_{16}$ is a (4,5)-set (all 1,820 four-subsets have $\ge5$ distinct differences), has 13 three-term APs, has a Sidon 10-subset and no Sidon 11-subset (all subsets of these sizes tested); e757.core: $m=13$, $h=10$ (`witness_16.json`).

**C7. Inherited from L007.** Lemma A ($n\le13$), Theorem 1 ((14,11)), Lemma D and its brute-force validation (C0), Lemma F (C3), and the cells (15,9,6), (15,10,6), (16,8,6) (C6): see results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md and experiments/prover/L007/.

## Sanity checks
- Slack bookkeeping on the records: $A_{\rm base}$ (14,12,6) $s=0$; 12-point sets (12,10,5) $s=1$; $C_{16}$ has $(n,m,\tau)=(16,13,6)$, $s=48+26-66=8\ge0$, and $\tau=6\le6$ as Theorem 1 requires.
- Theorem 2 is consistent with all 16-point data of the project: the annealing runs of D16 (28,589 genuine 16-point (4,5)-sets, best $h=10$), the L005 two-point extensions of the 2,910 classes (all $h=10$), and $C_{16}$.
- The requirement $\tau\ge7$ and the filters are both non-vacuous: hits exist (31,673 and 173,687 with $\tau=7$) and all of them are killed by (P2)/(P3), while 2,343 of 3,000 random extensions survive both filters (C5 control).
- Case-(A) structure check: the hits with $R_0\in O^+$ are exactly the overfilled ones of Step 8.1 (13 edges on 13 vertices), an obstruction that can be checked by hand on any of them.

## Falsifier report
experiments/20261017-0300-n16-via-i11/README.md (RESULT: EMPTY, with its own list of what the referee must check) and, for Lemma A′, experiments/falsify/i11-inequality/README.md. Notes from checking it: its step-1 table and this certificate agree on every count; it uses an isomorphism reduction to 149 classes in case (A), which this certificate avoids by running the extension on all 145,033 labelled graphs (no isomorphism test is load-bearing here); its README's "Assumed" list for I11 on $n\le15$ omits the window cell (5,3,2), which is empty (L007 Step 2.4); its item 3 asks for a second implementation of the enumeration: `enum_conn` (C2, C3) is one, written independently of `conn_dfs2`/`conn_dfs3` but following the same canonical-growth scheme, whose exhaustiveness is proved in L007 Lemma D and validated there against brute force; an orderly generation with nauty, which would also be independent of the scheme, was not done.
