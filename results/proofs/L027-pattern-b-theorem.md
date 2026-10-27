# L027: Pattern (b) in I11 minimal counterexamples: a pattern-(b) vertex is the centre of a pendant E1-hub over a connected slack-1 graph, and excluding pattern (b) is equivalent to the pendant-triple lemma PT
CLAIM-TYPE: lemma (partial; a reduction). No bound on $c_*$ and no value of $f(n)$ is claimed. Proved by hand: the exact effect of the compression operations on $(n,m,\tau,s)$ (Part A); every pairwise non-co-transversal non-edge triple of a connected member of $\mathcal C$ with slack $\le1$ is a pendant triple and forces slack 1, given I11 up to $n(G)+2$ vertices (Theorem B); in a minimal counterexample $H$ to I11 on $\mathcal C$ a vertex of degree 3 with pattern (b) exists only if $s(H)=-1$ and $H=G'\oplus(a,b,c)$ with $G'$ connected of slack 1 and $\{a,b,c\}$ a pendant b-configuration of $G'$, and then the rigid structure of Theorem P and Lemma Q holds (Theorem C); the pendant-triple lemma PT in two equivalent forms, and the equivalence "PT $\iff$ no minimal counterexample has a vertex with pattern (b) $\iff$ no minimal counterexample has an E1-hub" (Theorem D); the constraint J1 (Proposition J). NOT proved: PT itself. This is the only GAP.
TYPE: lemma (hand proofs) + computation (sanity checks only). No proof step depends on a computation. Remark B.5 is a computational remark and is not used in any proof.
STATUS: submitted 2026-10-27 11:50 UTC; unrefereed. Written by the prover for experiments/prover/e1hub-synthesis/SYNTHESIS.md Section 5, step 1. It consolidates the proved parts of L025 (Lemmas 1-9, Theorem 10, Remark 10.4, Corollary 11, Theorem 12, Lemma 13) and of L026 (Theorem 13, Corollary 14). I re-verified every step of them line by line and reproduce them in full, with one fix: the tight-set definition now requires $|S|\ge3$, as the judge asked (SYNTHESIS.md Section 1, L025 point 1). New here: Lemmas A10-A12; the self-contained connectivity proof in Corollary C.2; Theorem D; Proposition J (the judge's J1, now proved); and Theorem D(5) (the hypotheses "connected" and "$\Delta\le3$" of PT are redundant). Folder: experiments/prover/L027/.
DEPENDS ON:
- L017 (results/proofs/L017-i11-minimal-counterexample-structure.md) [verified-here, ACCEPTED x2, K64]. Used: the definitions of a minimal counterexample and of the seven patterns at a vertex of degree 3 (Theorem 4(iii)), of which only pattern (b) is used. Nothing else from L017 is load-bearing. The facts of L017 Step 0, Theorem 1(a),(b),(c), Theorem 2(U) and Theorem 4(i),(ii),(iv)(b) that the proofs need are re-proved here (Step 0, 0.8, Step 5.1). L017 Theorem 4(iii) (the Hall condition) is quoted in Corollary C.2 only as an alternative to the direct proof given there.
- L018 (results/proofs/L018-red-universality.md) [ACCEPTED as a partial certificate, K67]. Theorem 6(b′) (patterns (c1), (c2), (d) do not occur), used only in Corollary C.3.
- L019 (results/proofs/L019-triple-coverage-C1.md) [ACCEPTED as a partial certificate, K68]. Theorem 5 (folding lemma): the fold of Lemma A2 is the inverse operation, i.e. $G\oplus(a,b,c)$ folded at $x$. Not used; Lemma A2 is proved directly.
- L020 (results/proofs/L020-joint-induction-i11.md) [ACCEPTED, K69]. Proposition 6 (pair lemma for NC pairs of near-tight graphs) is the case $s\le1$ of Lemma A8(b), which is re-proved here. Not load-bearing.
- L021 (results/proofs/L021-i11-deficiency-route.md) [ACCEPTED as a partial certificate, K71]. Not used. The KT form of the E1-hub lemma is outside this certificate (Remark D.2).
- L022 (results/proofs/L022-i11-realizable-route.md) [ACCEPTED as a partial certificate, K72]. Theorem 2(v) is re-proved in Step 5.2. Theorem 2(i), (ii), (iii) are used only in Corollary C.3.
- L016 [verified-here, ACCEPTED x3, K61] (I11 on $\mathcal C$ for $n\le27$). Used only in Remark B.5 and in the Sanity checks.
- L025 (results/proofs/L025-e1hub-lemma-i11-form.md) and L026 (results/proofs/L026-e1hub-lemma-kt-form.md) [derived-here, unrefereed; checked line by line by the panel judge, SYNTHESIS.md Section 1]. They are the sources of Parts A, B, P, C. Every step taken from them was re-verified here and is reproduced in full, so neither is a dependency.
- experiments/prover/e1hub-synthesis/SYNTHESIS.md [panel judge, unrefereed]. Source of the statements of PT, its residual and gadget forms (Section 3), the combined Pattern-(b) theorem (Section 4.3) and the constraint J1 (Section 3). All are proved or stated here.
- Not used: KT and the potential of L021, realizability, the stored cell lists (except in the Sanity checks), Conjectures T, T′, T″, RU, C1, P2, P2′, P2⁺.

## Statement

### Conventions
- **3-graphs.** A *3-graph* $G$ has a finite vertex set $V(G)$ and an edge set $E(G)$ of 3-element subsets. Notation:
  - $n(G),m(G),\tau(G)$; $d_G(u)$ (degree); $\Delta(G)$ (maximum degree); $N_G(u)$ (the vertices $\ne u$ of the edges at $u$);
  - $e_G(S)$, the number of edges inside $S\subseteq V(G)$;
  - $G-Z$, the induced subgraph on $V(G)\setminus Z$;
  - $\partial_G(Z)$, the set of edges meeting $Z$, and $\partial_G(x,y)=\partial_G(\{x,y\})$.
- **Adjacency.** Two vertices are *adjacent* if some edge contains both; $\sigma_G(x,y)\in\{0,1\}$ records this.
- **Transversals.**
  - A *transversal* is a vertex set meeting every edge.
  - A *$k$-transversal* has exactly $k$ vertices; a *minimum transversal* has $\tau(G)$ vertices.
  - A set $X$ is *co-transversal* if some minimum transversal contains $X$.
  - A vertex is *avoided* if it lies in no minimum transversal.
  - An *NC pair* is a set of two distinct vertices that is not co-transversal.
- **Slack.** $s(G)=3n+2m-11\tau(G)$ is the *I11 slack*. I11 holds for $G$ if $s(G)\ge0$, and $G$ is *tight* if $s(G)=0$.
- **The class $\mathcal C$.** The 3-graphs that are:
  - (P1) linear;
  - (P2) $F_7$-free, where $F_7=\{012,034,056,135,246\}$;
  - (P3) $e(S)\le|S|-2$ for every $S$ with $|S|\ge2$.
- **Tight sets (fixed definition).** A *tight set* of $G$ is a set $S\subseteq V(G)$ with $|S|\ge3$ and $e_G(S)=|S|-2$. For $G\in\mathcal C$, by (P3), this is equivalent to $|S|\ge3$ and $e_G(S)\ge|S|-2$. $G$ is *saturated* if $m=n-2$.
  - The bound $|S|\ge3$ is the fix asked for by the judge. With $|S|\ge2$ every 2-set would be "tight" ($e=0$). The exception clause of L025 Lemma 4 ("unless $G$ has a tight set containing $x$ and $y$") would then always apply, and the lemma would say nothing. The proofs never produce a tight set with fewer than 3 vertices.
- **The hypotheses $(\mathrm H_N)$.** $(\mathrm H_N)$ means: every member of $\mathcal C$ with at most $N$ vertices satisfies I11. $(\mathrm H_N)$ implies $(\mathrm H_{N'})$ for $N'\le N$.
- **Minimal counterexample.** A *minimal counterexample* (to I11 on $\mathcal C$) is an $H\in\mathcal C$ with $s(H)<0$ and $(\mathrm H_{n(H)-1})$.
- **Facts about $F_7$.**
  - $F_7$ has 7 vertices, 5 edges and minimum degree 2.
  - The *centre* 0 has degree 3; the other six vertices have degree 2.
  - Every non-centre vertex lies in exactly one edge through the centre and in exactly one of the two edges avoiding it ($135$, $246$).
  - These two edges are disjoint, and each meets each edge through the centre in exactly one vertex.

**Constructions.** In each construction the letters $v,x,y,z,w,w_i$ denote new vertices.
- *Hub* $G\oplus(a,b,c)$ ($a,b,c$ distinct): $G$ plus $v,x,y,z$ and the four *hub edges* $e_0=\{x,y,z\}$, $h_a=\{v,x,a\}$, $h_b=\{v,y,b\}$, $h_c=\{v,z,c\}$.
- *Fold* $G\oplus^\circ(a,b\,|\,c)$: $G$ plus $v,z$ and the edges $\{v,a,b\}$, $\{v,z,c\}$.
- *Pendant replacement* $G^{\rm p}(c;a,b)=(G-c)+\{w,a,b\}$.
- *Identification* $G_{x=y}$: replace $y$ by $x$ in every edge and delete $y$.
- *Move* (for $d_G(x)=1$ with edge $\{x,x_1,x_2\}$): $M(x\to x_1;y,z)=(G-x)+\{x_1,y,z\}$.
- *Added edge* $F+Y$: $F$ plus the edge $Y$, for a 3-set $Y\subseteq V(F)$.
- *Pendant edges* $F^+(P_1,\dots,P_k)$ (pairwise disjoint 2-sets $P_i$): $F$ plus $w_1,\dots,w_k$ and the edges $\{w_i\}\cup P_i$.
- *Two-pair vertex* $K+w(B,C)$ (disjoint 2-sets $B,C$): $K$ plus $w$ and the edges $\{w\}\cup B$, $\{w\}\cup C$.
- *7-vertex gadget* $\Gamma(G'';A,B,C)$ (pairwise disjoint 2-sets): $\bigl(G''^+(A,B,C)\bigr)\oplus(a,b,c)$, where $a,b,c$ are the pendant vertices of $\{a\}\cup A$, $\{b\}\cup B$, $\{c\}\cup C$.
  - Its 7 new vertices are $a,b,c,v,x,y,z$.
  - Its 7 new edges are $\{a\}\cup A$, $\{b\}\cup B$, $\{c\}\cup C$, $e_0$, $h_a$, $h_b$, $h_c$.

**Configurations.**
- A *b-configuration* of $G$ is a set $\{a,b,c\}$ with these properties:
  - it consists of three vertices of $G$-degree $\le2$;
  - it is not an edge of $G$;
  - any two of its vertices form an NC pair.
- It is *pendant* if $d_G(a)=d_G(b)=d_G(c)=1$ and no edge contains two of $a,b,c$ (three degree-1 vertices in three distinct edges).
- An *E1-hub* of $H$ is $(v;x,y,z;a,b,c)$ with:
  - $\{x,y,z\},\{v,x,a\},\{v,y,b\},\{v,z,c\}\in E(H)$;
  - $d_H(x)=d_H(y)=d_H(z)=2$.

  Its *outer graph* is $G'=H-\{v,x,y,z\}$ and its *outer triple* is $\{a,b,c\}$.
- **Pattern (b)** (L017 Theorem 4(iii)). $H$ is a minimal counterexample and $v$ is a vertex of degree 3 with edges $\{v\}\cup P_j$ ($j=1,2,3$). The pattern at $v$ is (b) if:
  - $H-v$ has exactly two components $F_1,F_2$;
  - every pair is split: $P_j=\{x_j,y_j\}$ with $x_j\in V(F_1)$ and $y_j\in V(F_2)$.

### Part A. The operations and their exact effect

**Lemma A1 (hub).** Let $G\in\mathcal C$ and let $a,b,c$ be distinct vertices with $\{a,b,c\}\notin E(G)$. Put $G^\oplus=G\oplus(a,b,c)$. Then:
- $G^\oplus\in\mathcal C$;
- $d(v)=3$, $d(x)=d(y)=d(z)=2$, the degrees of $a,b,c$ rise by 1, and all other degrees are unchanged;
- $\tau(G^\oplus)=\tau(G)+1$ if some minimum transversal of $G$ contains two of $a,b,c$, and $\tau(G^\oplus)=\tau(G)+2$ otherwise.

So $s(G^\oplus)=s(G)+9$ or $s(G)-2$.

**Lemma A2 (fold).** Let $G\in\mathcal C$, let $a,b,c$ be distinct, and let $a,b$ be non-adjacent. Then $G^\circ=G\oplus^\circ(a,b\,|\,c)\in\mathcal C$. Moreover $\tau(G^\circ)=\tau(G)$ if some minimum transversal of $G$ contains $c$ and meets $\{a,b\}$, and $\tau(G^\circ)=\tau(G)+1$ otherwise, so $s(G^\circ)=s(G)+10$ or $s(G)-1$. In particular, if $\{a,c\}$ and $\{b,c\}$ are NC pairs, then $s(G^\circ)=s(G)-1$.

**Lemma A3 (pendant replacement).** Let $G\in\mathcal C$ and let $a,b,c$ be distinct, with:
- $a,b$ non-adjacent;
- $c$ co-transversal;
- $\{a,c\}$ and $\{b,c\}$ NC pairs.

Then $G^{\rm p}=G^{\rm p}(c;a,b)\in\mathcal C$. It has $n(G)$ vertices, $m(G)-d_G(c)+1$ edges and $\tau(G^{\rm p})=\tau(G)$, so $s(G^{\rm p})=s(G)+2-2d_G(c)$.

**Lemma A4 (identification).** Let $G$ be a 3-graph and $\{x,y\}$ an NC pair such that:
- $x$ is co-transversal;
- $x,y$ are non-adjacent;
- $N_G(x)\cap N_G(y)=\emptyset$.

Then:
- $G_{x=y}$ has $n-1$ vertices and exactly $m$ edges (no edge degenerates or doubles);
- it is linear if $G$ is;
- $\tau(G_{x=y})=\tau(G)$, so $s(G_{x=y})=s(G)-3$.

If $G\in\mathcal C$, then $G_{x=y}\in\mathcal C$ if and only if both:
- $G_{x=y}$ has no copy of $F_7$ containing $x$;
- $G$ has no tight set $S\supseteq\{x,y\}$.

**Lemma A5 (move).** Let $G$ be a 3-graph and let $x$ be a co-transversal vertex of degree 1 with edge $\{x,x_1,x_2\}$. Let $y,z$ be distinct vertices outside $\{x,x_1\}$ such that $\{x,y\}$ and $\{x,z\}$ are NC pairs. Then:
- no minimum transversal of $G-x$ meets $\{x_1,y,z\}$, so in particular $\{x_1,y,z\}\notin E(G)$;
- $M=M(x\to x_1;y,z)$ has $n-1$ vertices, exactly $m$ edges and $\tau(M)=\tau(G)$, so $s(M)=s(G)-3$.

**Lemma A6 (an edge on three avoided vertices).** If $Y$ is a set of three avoided vertices of a 3-graph $F$, then $Y\notin E(F)$, $\tau(F+Y)=\tau(F)+1$ and $s(F+Y)=s(F)-9$.

**Lemma A7 (pendant edges on pairs).** Let $F$ be a 3-graph, let $P_1,\dots,P_k$ be pairwise disjoint 2-sets of vertices, and put $F^+=F^+(P_1,\dots,P_k)$. Then
$$\tau(F^+)=\min_T\bigl(|T|+\#\{i:T\cap P_i=\emptyset\}\bigr),$$
the minimum taken over all transversals $T$ of $F$. If $F\in\mathcal C$ and no $P_i$ lies inside an edge of $F$, then $F^+\in\mathcal C$. Moreover $n(F^+)=n(F)+k$, $m(F^+)=m(F)+k$ and $s(F^+)=s(F)+5k-11(\tau(F^+)-\tau(F))$.

**Lemma A8 (deleting one or two vertices).**
(a) If $u$ is avoided, then $\tau(G-u)=\tau(G)$ and $s(G-u)=s(G)-3-2d_G(u)$. Hence, if $s(G-u)\ge0$ and $s(G)<3+2d_G(u)$, then $u$ is co-transversal.
(b) If $\{x,y\}$ is an NC pair, then $\tau(G-x-y)\ge\tau(G)-1$ and $s(G-x-y)\le s(G)+5-2|\partial_G(x,y)|$. If moreover $x$ is co-transversal, then $\tau(G-x-y)=\tau(G)-1$ and $s(G-x-y)=s(G)+5-2|\partial_G(x,y)|$.

**Lemma A9 (deleting a pairwise NC triple).** Let $G$ be a 3-graph and $\{a,b,c\}\notin E(G)$ three vertices of degree $\ge1$, pairwise NC, with $a$ co-transversal.
1. Then $\tau(G-a-b)=\tau(G)-1$ and $\tau(G-a-b-c)\in\{\tau(G)-2,\tau(G)-1\}$.
2. If $\tau(G-a-b-c)=\tau(G)-1$, then $s(G-a-b-c)=s(G)+2-2|\partial_G(\{a,b,c\})|\le s(G)-2$.
3. So if $s(G)\le1$ and $s(G-a-b-c)\ge0$, then $\tau(G-a-b-c)=\tau(G)-2$ and $s(G-a-b-c)=s(G)+13-2|\partial_G(\{a,b,c\})|$.
4. If, in that case, all three of $a,b,c$ are co-transversal, then none of them has all its edges meeting the other two.

**Lemma A10 (two-pair vertex).** Let $K$ be a 3-graph and $B,C$ disjoint 2-sets of vertices. Then:
- $\tau(K+w(B,C))=\tau(K)$ if some minimum transversal of $K$ meets both $B$ and $C$, and $\tau(K+w(B,C))=\tau(K)+1$ otherwise;
- $n$ rises by 1 and $m$ by 2, so $s(K+w(B,C))=s(K)+7$ or $s(K)-4$.

Now let $K\in\mathcal C$ with neither $B$ nor $C$ inside an edge of $K$. Then $K+w(B,C)$ is linear, and $K+w(B,C)\in\mathcal C$ if and only if both:
- $K$ has no tight set $S\supseteq B\cup C$;
- $K+w(B,C)$ has no copy of $F_7$ containing $w$.

Such a copy exists if and only if, for some labelling $\{\beta_1,\beta_2\},\{\gamma_1,\gamma_2\}$ of $B,C$ or of $C,B$ (in this order), $K$ has edges $\{\beta_1,\gamma_1,q\}$, $\{\beta_1,\gamma_2,r\}$ and $\{\beta_2,q,r\}$ for some vertices $q,r$.

**Lemma A11 (the 7-vertex gadget).** Let $G''$ be a 3-graph with $\tau''=\tau(G'')$, and let $A,B,C$ be pairwise disjoint 2-sets. Then $\tau(\Gamma(G'';A,B,C))\in\{\tau''+2,\tau''+3,\tau''+4\}$. Moreover $\tau(\Gamma)=\tau''+4$ if and only if both:
- (i) no minimum transversal of $G''$ meets $A\cup B\cup C$;
- (ii) no $(\tau''+1)$-transversal of $G''$ meets all three of $A$, $B$, $C$.

In that case $s(\Gamma)=s(G'')-9$. If $G''\in\mathcal C$ and none of $A,B,C$ lies inside an edge of $G''$, then $\Gamma\in\mathcal C$.

**Lemma A12 (tight sets).** Let $G\in\mathcal C$.
(a) If $S,S'$ are tight sets with $|S\cap S'|\ge2$, then $S\cup S'$ is tight.
(b) If $X\subseteq V(G)$ with $|X|\ge2$ lies in some tight set, then the union $S_X$ of all tight sets containing $X$ is tight. So $S_X$ is the largest tight set containing $X$.
(c) Every edge with at least two vertices in $S_X$ lies inside $S_X$.
(d) Every vertex of a tight set $S$ lies in an edge inside $S$.

**Table A (exact changes).** Here $\partial$ abbreviates $|\partial_G(\cdot)|$ of the deleted set.

| operation | where | $\Delta n$ | $\Delta m$ | $\Delta\tau$ | $\Delta s$ |
|---|---|---|---|---|---|
| hub $G\oplus(a,b,c)$ | A1 | $+4$ | $+4$ | $+1$ / $+2$ | $+9$ / $-2$ |
| fold $G\oplus^\circ(a,b\,\vert\,c)$ | A2 | $+2$ | $+2$ | $0$ / $+1$ | $+10$ / $-1$ |
| pendant replacement $G^{\rm p}(c;a,b)$ | A3 | $0$ | $1-d(c)$ | $0$ | $2-2d(c)$ |
| identification $G_{x=y}$ of an NC pair | A4 | $-1$ | $0$ | $0$ | $-3$ |
| move $M(x\to x_1;y,z)$ | A5 | $-1$ | $0$ | $0$ | $-3$ |
| edge on three avoided vertices | A6 | $0$ | $+1$ | $+1$ | $-9$ |
| two pendant pairs, $\tau$ rising by 2 | A7 | $+2$ | $+2$ | $+2$ | $-12$ |
| three pendant pairs, $\tau$ rising by 3 | A7 | $+3$ | $+3$ | $+3$ | $-18$ |
| deleting an avoided vertex $u$ | A8(a) | $-1$ | $-d(u)$ | $0$ | $-3-2d(u)$ |
| deleting an NC pair with $x$ co-transversal | A8(b) | $-2$ | $-\partial$ | $-1$ | $5-2\partial$ |
| deleting a pairwise NC non-edge triple | A9 | $-3$ | $-\partial$ | $-1$ / $-2$ | $2-2\partial$ / $13-2\partial$ |
| two-pair vertex $K+w(B,C)$ | A10 | $+1$ | $+2$ | $0$ / $+1$ | $+7$ / $-4$ |
| 7-vertex gadget $\Gamma(G'';A,B,C)$ | A11 | $+7$ | $+7$ | $+2$ / $+3$ / $+4$ | $+13$ / $+2$ / $-9$ |

### Part B. b-configurations of near-tight graphs are pendant

**Theorem B (b-configurations are pendant; = L025 Theorem 10 with Remark 10.4).** Let $G\in\mathcal C$ be connected with $s(G)\le1$, and suppose $(\mathrm H_{n(G)+2})$. Let $\{a,b,c\}\notin E(G)$ be three vertices that are pairwise NC (no degree assumption). Then:
- $d_G(a)=d_G(b)=d_G(c)=1$;
- no edge of $G$ contains two of $a,b,c$, so $\{a,b,c\}$ is a pendant b-configuration;
- $s(G)=1$.

In particular every b-configuration of $G$ is pendant, and if $G$ has one then $s(G)=1$. What is used:
- $(\mathrm H_{n})$ for the pendant replacement (rule R1);
- $(\mathrm H_{n-1})$ for free choice (Step 0.7);
- $(\mathrm H_{n-2})$ for the pair lemma (R2);
- $(\mathrm H_{n-3})$ for the triple deletion (R3);
- $(\mathrm H_{n+2})$, only in the last step (the fold).

Neither $\Delta(G)\le3$ nor any bound on $n(G)$ is used.

**Theorem B′ (tight case without connectivity; = L026 Theorem 13).** Let $G\in\mathcal C$ with $s(G)=0$, and suppose that every member of $\mathcal C$ with $n(G)-2$ or with $n(G)+2$ vertices satisfies I11. Then any three vertices $a,b,c$ with $\{a,b,c\}\notin E(G)$ include two that lie in a common minimum transversal.

**Corollary B.3 (the I11 form of the E1-hub lemma; = L025 Corollary 11(a)).** Let $G\in\mathcal C$ be connected with $s(G)\le1$ and $(\mathrm H_{n(G)+2})$, and let $a,b,c$ be distinct with $\{a,b,c\}\notin E(G)$. Suppose that $s(G)=0$, or that $s(G)=1$ and $\{a,b,c\}$ is not a pendant triple. Then:
- some minimum transversal of $G$ contains two of $a,b,c$;
- equivalently, $s(G\oplus(a,b,c))=s(G)+9\ge9$.

**Remark B.4.** Theorem B needs no lower bound on $n(G)$. If $n(G)\le n_0-2$, where I11 is known on $\mathcal C$ for $n\le n_0$ ($n_0=27$ by L016), then the hypothesis $(\mathrm H_{n(G)+2})$ is a theorem.

**Remark B.5 (small $n$) [verified-here as computations, unrefereed; NOT used in any proof].** This is L025 Remark 10.3, re-tagged as computational.
1. Given the completeness of the stored refereed lists (L013 Lemma E′) and the unrefereed cell table of L017 C4 and L020 Step 4.3, every connected member of $\mathcal C$ with $\Delta\le3$, slack $\le1$ and at most 26 vertices is one of two kinds:
   - one of the 483 stored near-tight graphs;
   - a member of the tight cell $(25,23,11,3)$, which has no b-configuration by Theorem B (with $(\mathrm H_{27})$, L016).
2. The 483 graphs contain no pairwise NC non-edge triple at all (check E4 here; L025 C3; L017 C5).
3. Hence, on these computations, a connected $G\in\mathcal C$ with $\Delta\le3$, $s(G)\le1$ and a b-configuration has $n(G)\ge27$. Then $n(G'')\ge24$ in Theorem P, and a minimal counterexample with a pattern-(b) vertex has $n(H)\ge31$.
4. This agrees with L022 Corollary 3′ (computational): $H-v$ is connected for $n(H)\le30$.

### Part P. The pendant case

**Theorem P (structure of a pendant b-configuration; = L025 Theorem 12).** Assume:
- $G\in\mathcal C$ is connected with $\Delta(G)\le3$ and $s(G)=1$;
- $(\mathrm H_{n(G)})$ holds;
- $\{a,b,c\}$ is a pendant b-configuration with edges $e_a=\{a\}\cup A$, $e_b=\{b\}\cup B$, $e_c=\{c\}\cup C$.

By Theorem B, $s(G)=1$ is forced when $(\mathrm H_{n(G)+2})$ holds. Put $n=n(G)$, $G''=G-\{a,b,c\}$, $\tau''=\tau(G'')$ and $W=A\cup B\cup C$. Then:

(a) The basic quantities:
  - $\tau''=\tau(G)-2$ and $s(G'')=8$;
  - every minimum transversal of $G''$ avoids $W$;
  - every transversal of $G''$ that meets $A$, $B$ and $C$ has at least $\tau''+2$ vertices;
  - for each of the three pairs, some $(\tau''+1)$-transversal of $G''$ meets the other two pairs.

(b) $G''$ is connected.

(c) $A,B,C$ are pairwise disjoint, so $|W|=6$. Each pair lies inside no edge of $G''$, and every vertex of $W$ has $G''$-degree 1 or 2.

(d) For every $X=\{x_A,x_B,x_C\}$ with $x_A\in A$, $x_B\in B$, $x_C\in C$:
  - $\tau(G''-X)=\tau''-1$;
  - $s(G''-X)=10-2|\partial_{G''}(X)|$;
  - $|\partial_{G''}(X)|\le5$.

(e) Let $Y=\{y_1,y_2,y_3\}$ be three pairwise non-adjacent avoided vertices of $G''$. Then $G''+Y\notin\mathcal C$. So either $G''$ has a tight set containing $Y$, or $G''+Y$ has a copy of $F_7$ using the edge $Y$. Such a copy has one of two shapes:
  - for some vertex $o$, $G''$ has edges $\{o,y_i,p_i\}$ ($i=1,2,3$) and $\{p_1,p_2,p_3\}$;
  - for some $i$, $y_i$ has two edges $\{y_i,p,q\},\{y_i,r,s\}$ in $G''$, and the other two vertices of $Y$ lie in edges $\{\cdot,p,r\}$ and $\{\cdot,q,s\}$ of $G''$, one in each.

(f) The three identifications $G_{a=b},G_{a=c},G_{b=c}$ and the six moves $M(a\to a_i;b,c)$, $M(b\to b_i;a,c)$, $M(c\to c_i;a,b)$ ($i=1,2$; $A=\{a_1,a_2\}$ etc.) are linear 3-graphs with $n-1$ vertices and slack $-2$, hence not in $\mathcal C$. Precisely:
  - $G_{a=b}\notin\mathcal C$ holds because one of the following holds:
    - $G''$ has a tight set containing $A\cup B$;
    - some $a_i$ has edges $\{a_i,b_1,q\}$ and $\{a_i,b_2,r\}$ with $\{a_{3-i},q,r\}\in E(G'')$;
    - the same with $A$ and $B$ exchanged.
  - $M(a\to a_i;b,c)\notin\mathcal C$ holds because one of the following holds:
    - $G''$ has a tight set containing $\{a_i\}\cup B\cup C$;
    - $a_i$ has edges $\{a_i,b_j,c_k\}$ and $\{a_i,b_{3-j},c_{3-k}\}$ in $G''$.

  The other identifications and moves are analogous.

(g) Let $P,Q\subseteq W$ be disjoint 2-sets, neither inside an edge of $G''$. Then some $(\tau''+1)$-transversal of $G''$ meets both $P$ and $Q$.

(h) Let $P,Q,R\subseteq W$ be pairwise disjoint 2-sets, none inside an edge of $G''$. Then one of the following holds:
  - some $(\tau''+1)$-transversal meets two of them;
  - some $(\tau''+2)$-transversal meets all three.

(i) No edge of $G''$ lies inside $W$. If an edge of $G''$ has two vertices in $W$, its third vertex lies in every minimum transversal of $G''$.

(j) (*All attachment vertices lie in one tight set.*) $G''$ has a tight set containing $W$; let $S_0$ be the largest one (Lemma A12(b)). Then:
  - $S_0\cup\{a,b,c\}$ is a tight set of $G$, and $S_0\cup\{a,b,c,v,x,y,z\}$ is a tight set of $G\oplus(a,b,c)$;
  - every edge of $G''$ that meets both $S_0$ and $V(G'')\setminus S_0$ has exactly one vertex in $S_0$;
  - every vertex of $W$ lies in an edge of $G''$ inside $S_0$.

  If $S_0=V(G'')$, then $G''$, $G$ and $G\oplus(a,b,c)$ are saturated and $n\equiv1\pmod{11}$.

(k) (*The saturated case.*) Suppose $S_0=V(G'')$. Then:
  - $a,b,c$ are the only vertices of $G$ of degree $\le2$; all others have degree 3;
  - the six vertices of $W$ have $G''$-degree 2 and are exactly the avoided vertices of $G''$;
  - every $X$ as in (d) contains two vertices of a common edge of $G''$, whose third vertex lies in every minimum transversal of $G''$ by (i).

Hypotheses used:
- $(\mathrm H_{n-k})$ for $k\in\{0,1,3,4,5,6\}$;
- $\Delta(G)\le3$, only in (c) and (k).

### Part C. Pattern (b) in a minimal counterexample

**Lemma Q (pendant block; = L025 Lemma 13, the I11 form of L026 Remark 7.3).** Let $H$ be a minimal counterexample and $e\in E(H)$. Suppose $V(H)=V_1\sqcup V_2$, where every edge other than $e$ lies inside $V_1$ or inside $V_2$, and $|e\cap V_2|=1$. Then $|V_2|=1$.

**Theorem C (the Pattern-(b) theorem).** Let $H$ be a minimal counterexample to I11 on $\mathcal C$, and let $v$ be a vertex of degree 3 whose pattern is (b): $H-v$ has exactly two components $F_1,F_2$, and the co-vertex pairs are $P_j=\{x_j,y_j\}$ with $x_j\in V(F_1)$, $y_j\in V(F_2)$. Then, after possibly exchanging the names $F_1$ and $F_2$:
1. *The E1-hub.*
   - $s(H)=-1$.
   - $F_1$ is the single edge $\{x_1,x_2,x_3\}$, and $d_H(x_j)=2$.
   - So $(v;x_1,x_2,x_3;y_1,y_2,y_3)$ is an E1-hub of $H$ with outer graph $G':=F_2=H-\{v,x_1,x_2,x_3\}$, and $H=G'\oplus(y_1,y_2,y_3)$.
2. *The outer graph.*
   - $G'\in\mathcal C$ is connected with $\Delta(G')\le3$.
   - $n(G')=n(H)-4$, $\tau(G')=\tau(H)-2$ and $s(G')=1$.
   - $\{y_1,y_2,y_3\}$ is a pendant b-configuration of $G'$, and $d_H(y_j)=2$.
3. *The rigid structure.* $G'$ satisfies all conclusions (a)-(k) of Theorem P with $(a,b,c)=(y_1,y_2,y_3)$, and Proposition J. Let $e_{y_j}=\{y_j\}\cup Q_j$ be the edge of $G'$ at $y_j$, $W=Q_1\cup Q_2\cup Q_3$ and $G''=G'-\{y_1,y_2,y_3\}$. Then:
   - $G''$ is connected, with $n(G'')=n(H)-7$, $\tau(G'')=\tau(H)-4$ and $s(G'')=8$;
   - $Q_1,Q_2,Q_3$ are pairwise disjoint, so the six attachment vertices are distinct;
   - every vertex of $W$ has $G''$-degree 1 or 2 and is avoided in $G''$;
   - $G''$ has a tight set containing $W$. The largest one, $S_0$, meets every edge of $G''$ that leaves it in exactly one vertex, and $S_H=S_0\cup\{y_1,y_2,y_3,v,x_1,x_2,x_3\}$ is a tight set of $H$.
4. *The dichotomy.* Exactly one of the following holds.
   - $S_0=V(G'')$. Then:
     - $G''$, $G'$ and $H$ are saturated;
     - $n(G')\equiv1\pmod{11}$, equivalently $n(H)\equiv5\pmod{11}$;
     - every vertex of $G'$ other than $y_1,y_2,y_3$ has degree 3 in $G'$;
     - $W$ is exactly the set of avoided vertices of $G''$.
   - $S_0\neq V(G'')$. Then at least two edges of $G''$ (equivalently, of $H$) leave $S_0$ (equivalently, $S_H$), each meeting it in exactly one vertex.

Every use of I11 in the proof is for a member of $\mathcal C$ with at most $n(H)-1$ vertices (Step 7).

**Corollary C.2 (E1-hubs).** Let $H$ be a minimal counterexample and $(v;x,y,z;a,b,c)$ an E1-hub of $H$. Then:
- $G'=H-\{v,x,y,z\}$ is connected;
- $H-v$ has exactly two components, the single edge $\{x,y,z\}$ and $G'$;
- the pattern at $v$ is (b), so Theorem C applies, with $F_1=\{x,y,z\}$.

Conversely, by Theorem C(1), every vertex of degree 3 with pattern (b) is the centre of an E1-hub.

**Corollary C.3 (slack $-2$; = the last sentence of L026 Corollary 14).** If $s(H)=-2$ for a minimal counterexample $H$, then $H-v$ is connected for every vertex $v$ of degree 3 (pattern (a)). This uses L022 Theorem 2(i)-(iii) [K72] or L018 Theorem 6(b′) [K67].

### Part D. The residual: the pendant-triple lemma PT

**Conjecture PT (pendant-triple lemma) [conjecture].**
- *Form I.* Let $G\in\mathcal C$ be connected with $\Delta(G)\le3$ and $s(G)=1$, and suppose $(\mathrm H_{n(G)+3})$. Then $G$ has no pendant b-configuration. That is, no three vertices of $G$-degree 1, lying in three different edges, are pairwise NC.
- *Form II (residual form).* Let $G''\in\mathcal C$ be connected with $\Delta(G'')\le3$ and $s(G'')=8$, and suppose $(\mathrm H_{n(G'')+6})$. Then there are no three pairwise disjoint 2-sets $A,B,C\subseteq V(G'')$ such that:
  - none of them lies inside an edge of $G''$;
  - all six of their vertices have $G''$-degree $\le2$;
  - (i) no minimum transversal of $G''$ meets $A\cup B\cup C$;
  - (ii) no $(\tau(G'')+1)$-transversal of $G''$ meets all three of $A,B,C$.

  By Lemma A11, (i) and (ii) together say exactly that $\tau(\Gamma(G'';A,B,C))=\tau(G'')+4$, i.e. $s(\Gamma)=s(G'')-9=-1$.

For an integer $N$, PT-I($N$) denotes Form I for graphs with $n(G)=N$, and PT-II($N$) denotes Form II for graphs with $n(G'')=N$.

**Theorem D (PT is exactly what remains of pattern (b)).** For every integer $N$, the following are equivalent:
1. PT-I($N$);
2. PT-II($N-3$);
3. no minimal counterexample to I11 on $\mathcal C$ with $N+4$ vertices has a vertex of degree 3 with pattern (b);
4. no minimal counterexample to I11 on $\mathcal C$ with $N+4$ vertices has an E1-hub.

In particular, **PT (for all $N$) holds if and only if no minimal counterexample to I11 on $\mathcal C$ has a vertex with pattern (b)**. Moreover:

5. *Redundant hypotheses.*
   - In Form I the hypotheses "connected" and "$\Delta(G)\le3$" are redundant: a $G\in\mathcal C$ with $s(G)=1$, $(\mathrm H_{n(G)+3})$ and a pendant b-configuration is automatically connected with $\Delta(G)\le3$.
   - In Form II the hypotheses "connected", "$\Delta(G'')\le3$" and "degree $\le2$ on $A\cup B\cup C$" are redundant in the same sense.
   - So PT is equivalent to: *no $G\in\mathcal C$ with $s(G)=1$ and $(\mathrm H_{n(G)+3})$ has a pendant b-configuration.*

**Proposition J (constraint J1; stated by the panel judge, proved here).** In the setting of Theorem P, let $u\in W$. Let $Y,Z$ be the two pairs among $A,B,C$ not containing $u$ (e.g. $u\in A$, $Y=B$, $Z=C$), and put $K_u=G''-u$. Then:
1. $u$ is avoided in $G''$, $\tau(K_u)=\tau''$ and $s(K_u)=5-2d_{G''}(u)\in\{1,3\}$.
2. No minimum transversal of $K_u$ meets both $Y$ and $Z$.
3. $K_u+w(Y,Z)$ is linear with $n(G'')=n-3$ vertices and slack $s(K_u)-4\in\{-3,-1\}$, so it is not in $\mathcal C$ by $(\mathrm H_{n-3})$.
4. Hence one of the following holds:
   - $G''$ has a tight set $S$ with $Y\cup Z\subseteq S$ and $u\notin S$;
   - for some labelling $\{\beta_1,\beta_2\},\{\gamma_1,\gamma_2\}$ of $Y,Z$ or of $Z,Y$, the graph $G''-u$ has edges $\{\beta_1,\gamma_1,q\}$, $\{\beta_1,\gamma_2,r\}$ and $\{\beta_2,q,r\}$.
5. Let $d$ be the number of edges of $G''$ at $u$ that lie inside $S_0$; by Theorem P(j), $d\in\{1,2\}$.
   - If $d=1$, then $S_0-u$ is a tight set as in item 4, so item 4 adds nothing to Theorem P(j).
   - If $d=2$, then $S_0-u$ is not tight, and item 4 is a genuinely new constraint.

**Remark D.1 (what a counterexample to PT must look like).** This collects Theorem P, Lemma Q, Proposition J and Theorem C, all proved. Let $H$ be a minimal counterexample with a pattern-(b) vertex, equivalently a counterexample to PT-I with $N=n(H)-4$. Then $G''$ (with $n(H)-7$ vertices) satisfies all of the following:
- it is connected, with $\Delta\le3$, $s=8$ and $\tau=\tau(H)-4$;
- its six attachment vertices $W=A\sqcup B\sqcup C$ have $G''$-degree 1 or 2, are avoided, and no edge lies inside $W$;
- every transversal triple $X$ of $(A,B,C)$ has $\tau(G''-X)=\tau''-1$ and $|\partial(X)|\le5$;
- the largest tight set $S_0\supseteq W$ is met by every leaving edge in one vertex;
- either $S_0=V(G'')$, with all non-$W$ vertices of degree 3 and $n(H)\equiv5\pmod{11}$, or at least two edges leave $S_0$;
- the identification, move, pendant-pair and avoided-triple obstructions (P(e)-(h)) hold;
- J1 holds at each of the six vertices of $W$.

On the computations of Remark B.5 (unrefereed), $n(H)\ge31$. Nothing proved here bounds $n(H)$ from above.

**Remark D.2 (the KT form is not treated).** The KT form of the E1-hub lemma (L026 GAP A; SYNTHESIS.md Sections 4.1, 4.2) is outside this certificate. Its residual on the L024 route is the KT analogue PT-KT of PT (SYNTHESIS.md Section 3), and nothing here proves it.
- The $\tau$ statements and membership criteria of Lemmas A1-A11 hold for every graph satisfying their hypotheses, so they give exact changes of any linear potential in $(n,m,\tau)$, for instance $27n+35m-132\tau$ (SYNTHESIS.md Section 4.2).
- Theorems B, P and C use $s(G)\le1$ and I11 itself at the sizes listed in Step 7, so they do not transfer to the KT potential.

Tags:
- Part A, Theorems B, B′, P, C, D, Corollaries B.3, C.2, C.3, Lemma Q and Proposition J are **[derived-here]**: hand proofs below, unrefereed. The proofs of the parts taken from L025 and L026 were re-verified here.
- Remark B.5 is **[verified-here as computations, unrefereed]**, and so are the Sanity checks E1-E7. They are tests of the statements, not proof steps.
- Conjecture PT, and I11 itself, are **[conjecture]**.

## Proof

### Step 0. Facts used (L017 Step 0, re-proved)
0.1 *Disjoint unions.*
- $n,m,\tau,s$ are additive over disjoint unions, and the minimum transversals of a disjoint union are exactly the unions of minimum transversals of the parts. Proof: a transversal restricts to a transversal of each part, and a union of transversals of the parts is a transversal.
- An isolated vertex has $s=3$, a single edge $E_1$ has $s=0$, and the empty 3-graph has $s=0$.

0.2 *Heredity.* Deleting vertices (with their edges) or edges preserves (P1), (P2) and (P3), so every induced subgraph of a member of $\mathcal C$ is in $\mathcal C$.

0.3 *Deleting a vertex set.* For $Z\subseteq V(G)$:
- $\tau(G)-|Z|\le\tau(G-Z)\le\tau(G)$, because $T\setminus Z$ and $T'\cup Z$ are transversals;
- $X$ is co-transversal iff $\tau(G-X)=\tau(G)-|X|$: a minimum transversal $T\supseteq X$ gives the transversal $T\setminus X$, and a transversal $T'$ of $G-X$ with $\tau(G)-|X|$ vertices gives the minimum transversal $T'\cup X$;
- an isolated vertex is avoided.

0.4 *Slack identity.* $s(G-Z)=s(G)-3|Z|-2|\partial_G(Z)|+11(\tau(G)-\tau(G-Z))$, since $m(G-Z)=m-|\partial_G(Z)|$.

0.5 *Linearity.* In a linear 3-graph two distinct vertices lie in at most one common edge, so:
- the edges at a vertex pairwise meet only in that vertex;
- $|\partial(x,y)|=d(x)+d(y)-\sigma(x,y)$.

0.6 *Components.*
- A connected 3-graph with at least 2 vertices has no isolated vertex. A connected 3-graph with exactly 3 vertices has an edge, and that edge is its whole vertex set.
- If $G$ is connected and $\emptyset\ne Z\subsetneq V(G)$, every component $K$ of $G-Z$ contains a vertex of an edge of $\partial_G(Z)$. Proof: some edge meets both $V(K)$ and $V(G)\setminus V(K)$, and it cannot be an edge of $G-Z$, so it meets $Z$.

0.7 *Free choice.* Let $G\in\mathcal C$ be connected with $n(G)\ge2$, $s(G)\le1$ and $(\mathrm H_{n(G)-1})$. Then every vertex $u$ is co-transversal. Proof:
- $d(u)\ge1$ by 0.6;
- $s(G-u)\ge0$ by $(\mathrm H_{n-1})$;
- $s(G)\le1<5\le3+2d(u)$;
- apply Lemma A8(a), proved in 1.8 without using 0.7.

0.8 *Minimal counterexamples* (L017 Theorem 1(a),(b),(c), re-proved). Let $H$ be a minimal counterexample. Then:
- $H$ is connected: otherwise $H=H_1\sqcup H_2$ with both parts in $\mathcal C$ and smaller, and $s(H)=s(H_1)+s(H_2)\ge0$.
- $m\ge1$, since $m=0$ gives $s=3n\ge0$.
- $H$ has at least 3 vertices and no isolated vertex.
- For every vertex $u$: $s(H-u)\ge0$ by $(\mathrm H_{n(H)-1})$, and $s(H)<0<3+2d(u)$. So $u$ is co-transversal (A8(a)), $\tau(H-u)=\tau(H)-1$, and $s(H-u)=s(H)+8-2d_H(u)\ge0$ (0.4).
- As $s(H)\le-1$, this gives $d_H(u)\le3$, so $\Delta(H)\le3$.
- If $d_H(u)=3$, then $s(H)\ge-2$.

### Step 1. Proofs of Part A
1.1 *Lemma A1, linearity and degrees.* Put $G^\oplus=G\oplus(a,b,c)$.
- Two hub edges meet in exactly one vertex: $e_0\cap h_a=\{x\}$, $e_0\cap h_b=\{y\}$, $e_0\cap h_c=\{z\}$, $h_a\cap h_b=h_a\cap h_c=h_b\cap h_c=\{v\}$, as $a,b,c$ are distinct.
- A hub edge has at most one vertex in $V(G)$, so it meets an edge of $G$ in at most one vertex.
- So $G^\oplus$ is linear.
- The degree statement holds because the new edges at $v,x,y,z,a,b,c$ are exactly the stated ones.

1.2 *Lemma A1, $F_7$.* Let $F\subseteq G^\oplus$ be a copy of $F_7$.
1. Suppose $x\in V(F)$. Then both edges at $x$ ($e_0,h_a$) lie in $F$, because $F_7$ has minimum degree 2 and $d_{G^\oplus}(x)=2$.
2. Hence $y,z\in V(F)$, and in the same way $h_b,h_c\in F$.
3. So $V(F)\supseteq\{v,x,y,z,a,b,c\}$, which has 7 elements, and equality holds.
4. The fifth edge of $F$ lies inside $V(F)$ and is not a hub edge. It contains none of $v,x,y,z$, since all their edges are hub edges.
5. So the fifth edge is $\{a,b,c\}\in E(G)$, which is excluded.
6. The same argument applies if $y$ or $z$ lies in $V(F)$.
7. If $v\in V(F)$ but $x,y,z\notin V(F)$, then every edge at $v$ contains one of $x,y,z$, so $v$ has $F$-degree 0, which is impossible.
8. So $V(F)\subseteq V(G)$ and $F\subseteq G$, contradicting $G\in\mathcal C$.

1.3 *Lemma A1, (P3).* Let $|S|\ge2$, $S_0=S\cap V(G)$, $S_1=S\cap\{v,x,y,z\}$, and let $h$ be the number of hub edges inside $S$. Then $e(S)=e_G(S_0)+h$.
- Case $S_1=\emptyset$: $e(S)=e_G(S_0)\le|S|-2$.
- Case $S_1=\{v,x,y,z\}$: $h=1+|S_0\cap\{a,b,c\}|$.
  - If $|S_0|\ge2$: $e(S)\le(|S_0|-2)+1+3=|S|-2$.
  - If $|S_0|\le1$: $e(S)\le2\le|S|-2$.
- Case $\emptyset\ne S_1\ne\{v,x,y,z\}$. First, $h\le|S_1|-1$:
  - if $v\notin S_1$, only $e_0$ can lie inside $S$, and only when $S_1=\{x,y,z\}$;
  - if $v\in S_1$, then $e_0\not\subseteq S$, and each of $h_a,h_b,h_c$ inside $S$ uses its own vertex $x,y,z$ of $S_1\setminus\{v\}$.

  Then:
  - If $|S_0|\ge2$: $e(S)\le|S_0|-2+|S_1|-1<|S|-2$.
  - If $|S_0|\le1$: $e_G(S_0)=0$ and $h\le1$. Indeed, if $v\notin S_1$ only $e_0$ can count; if $v\in S_1$, each of $h_a,h_b,h_c$ inside $S$ needs its own vertex $a,b,c$ in $S_0$. If $h=1$, then $|S|\ge3$. So $e(S)\le|S|-2$.

1.4 *Lemma A1, $\tau$.* Let $T$ be a transversal of $G^\oplus$.
1. $T\cap V(G)$ is a transversal of $G$, and $T$ meets $e_0\subseteq\{x,y,z\}$. So $|T|\ge\tau(G)+1$.
2. Suppose $|T|=\tau(G)+1$. Then $T_0=T\cap V(G)$ is a minimum transversal of $G$, and $T$ has exactly one vertex $t$ in $\{v,x,y,z\}$, with $t\in e_0$.
3. If $t=x$, then $h_b,h_c$ force $b,c\in T_0$. Likewise $t=y$ forces $a,c\in T_0$, and $t=z$ forces $a,b\in T_0$.
4. Conversely, if a minimum transversal $T_0$ contains (say) $b,c$, then $T_0\cup\{x\}$ is a transversal.
5. $T_0\cup\{v,x\}$ is always a transversal.
6. With $\Delta n=\Delta m=4$: $\Delta s=12+8-11\Delta\tau\in\{9,-2\}$. $\square$

1.5 *Lemma A2.*
- *Linear.* $\{v,a,b\}\cap\{v,z,c\}=\{v\}$. The edge $\{v,z,c\}$ meets an edge of $G$ at most in $c$. The edge $\{v,a,b\}$ meets an edge $f$ of $G$ in $f\cap\{a,b\}$, which has size $\le1$ because $a,b$ are non-adjacent.
- *$F_7$-free.* $z$ has degree 1, so a copy of $F_7$ contains neither $z$ nor the edge $\{v,z,c\}$. Then $v$ would have degree $\le1$ in it, so the copy avoids $v$ and lies in $G$, which is impossible.
- *(P3).* Let $|S|\ge2$ and $S_0=S\cap V(G)$. Then $e(S)=e_G(S_0)+[\{v,a,b\}\subseteq S]+[\{v,z,c\}\subseteq S]$.
  - If $v\notin S$: $e(S)=e_G(S_0)$, which is $\le|S_0|-2$ when $|S_0|\ge2$ and $0$ otherwise.
  - If $v\in S$ and $z\notin S$: $e(S)\le e_G(S_0)+1\le|S|-2$ when $|S_0|\ge2$. When $|S_0|\le1$, $e(S)=0$, because the edge $\{v,a,b\}$ needs $a,b\in S_0$.
  - If $v,z\in S$: $e(S)\le e_G(S_0)+2\le|S_0|=|S|-2$ when $|S_0|\ge2$. When $|S_0|\le1$, $e(S)\le1$, and $|S|\ge3$ if $e(S)=1$.
- *$\tau$.* Let $T$ be a transversal of $G^\circ$. Then $|T\cap V(G)|\ge\tau(G)$. If $|T|=\tau(G)$, then $v,z\notin T$, so $T$ is a minimum transversal of $G$ that meets $\{a,b\}$ (edge $\{v,a,b\}$) and contains $c$ (edge $\{v,z,c\}$). Conversely, such a $T$ is a transversal of $G^\circ$. For every minimum transversal $T_0$ of $G$, the set $T_0\cup\{v\}$ is a transversal.
- *Slack.* $\Delta s=6+4-11\Delta\tau\in\{10,-1\}$. If $\{a,c\},\{b,c\}$ are NC pairs, no minimum transversal contains $c$ together with $a$ or $b$, so $\Delta\tau=1$. $\square$

1.6 *Lemma A3.*
- *In $\mathcal C$.* $G-c\in\mathcal C$ (0.2).
  - The edge $\{w,a,b\}$ meets an edge of $G-c$ in at most one of $a,b$ (non-adjacent), and never in $w$. So $G^{\rm p}$ is linear.
  - $w$ has degree 1, so no copy of $F_7$ uses the new edge.
  - (P3): if $w\notin S$, then $e(S)=e_{G-c}(S)$. If $w\in S$ and $|S\setminus\{w\}|\ge2$, then $e(S)\le e_{G-c}(S\setminus\{w\})+1\le|S|-2$. If $S=\{w,t\}$, then $e(S)=0$.
- *$\tau$.* As $c$ is co-transversal, $\tau(G-c)=\tau(G)-1$ (0.3).
  1. Let $T'$ be a minimum transversal of $G-c$. Then $T'\cup\{c\}$ is a transversal of $G$ with $\tau(G)$ vertices, i.e. a minimum one containing $c$.
  2. Since $\{a,c\},\{b,c\}$ are NC pairs, $T'\cup\{c\}$ contains neither $a$ nor $b$. So no minimum transversal of $G-c$ meets $\{a,b\}$.
  3. A transversal of $G^{\rm p}$ restricts to a transversal of $G-c$. If the restriction is minimum, it misses $\{a,b\}$, so the transversal must contain $w$. Hence $\tau(G^{\rm p})\ge\tau(G-c)+1=\tau(G)$.
  4. $T'\cup\{w\}$ attains this.
- *Counting.* $n(G^{\rm p})=n$ and $m(G^{\rm p})=m-d(c)+1$. $\square$

1.7 *Lemma A4.*
- *No degenerate or doubled edges.* An edge containing $y$ does not contain $x$ (non-adjacent), so its image has three distinct vertices. Two distinct edges $f,g$ with the same image cannot both contain $y$, or both avoid it, since then the images would differ. So say $y\in g$ and $y\notin f$, with $f=(g\setminus\{y\})\cup\{x\}$. Then the two vertices of $g\setminus\{y\}$ are common neighbours of $x$ and $y$, which is excluded. Hence $m(G_{x=y})=m$.
- *Linearity.* Suppose two image edges share two vertices $p,q$, with preimages $f\ne g$.
  - If $x\notin\{p,q\}$: the vertices of an image edge other than $x$ are vertices of its preimage, so $p,q\in f\cap g$. If neither preimage contains $y$, the images are $f$ and $g$ themselves, so again $p,q\in f\cap g$. In both cases this contradicts linearity of $G$.
  - Otherwise $x\in\{p,q\}$, say $p=x$, and at least one preimage contains $y$.
    - If both $f,g$ contain $y$, then $f,g$ share $y$ and $q$, a contradiction.
    - If exactly one contains $y$, say $g$, then $x\in f$ and $q\in f\cap g$, so $q$ is a common neighbour of $x$ and $y$, a contradiction.
- *$\tau$.* We prove $\tau(G_{x=y})=\tau(G)$ in two inequalities.
  1. A minimum transversal $T$ of $G$ containing $x$ avoids $y$ (NC). It meets the image of every edge, because the vertex of $T$ in an edge is not $y$. So $\tau(G_{x=y})\le\tau(G)$.
  2. Conversely, let $T'$ be a transversal of $G_{x=y}$. If $x\notin T'$, then $T'$ is a transversal of $G$.
  3. If $x\in T'$, then $T'\cup\{y\}$ is a transversal of $G$ containing $x,y$. It is not minimum (NC), so $|T'|+1\ge\tau(G)+1$.
  4. Either way $|T'|\ge\tau(G)$.
- *Membership.* The edges of $G_{x=y}$ not containing $x$ are exactly the edges of $G$ meeting neither $x$ nor $y$. So $G_{x=y}-x=G-x-y\in\mathcal C$, and a copy of $F_7$ in $G_{x=y}$ contains $x$. Now let $S'$ be a vertex set of $G_{x=y}$ with $|S'|\ge2$.
  - If $x\notin S'$, then $e(S')=e_G(S')$.
  - If $x\in S'$, the edges inside $S'$ are exactly the images of the edges of $G$ inside $S=S'\cup\{y\}$, so $e(S')=e_G(S)$ with $|S|=|S'|+1\ge3$. Hence (P3) fails at $S'$ iff $e_G(S)\ge|S|-2$, i.e. (by (P3) in $G$) iff $S$ is a tight set of $G$ containing $x,y$.
  - Conversely, a tight set $S\supseteq\{x,y\}$ of $G$ gives the violating set $S'=S\setminus\{y\}$.
  - Linearity holds by the above. $\square$

1.8 *Lemma A8.* (a) is 0.3 (an avoided $u$ has $\tau(G-u)=\tau(G)$) together with 0.4. If $u$ were avoided with $s(G-u)\ge0$ and $s(G)<3+2d(u)$, then $s(G-u)=s(G)-3-2d(u)<0$. (b):
- By 0.3, $\tau(G-x-y)\ge\tau(G)-2$, with equality iff $\{x,y\}$ is co-transversal. So an NC pair has $\tau(G-x-y)\ge\tau(G)-1$, and 0.4 gives the inequality.
- If $x$ is co-transversal, then $\tau(G-x-y)\le\tau(G-x)=\tau(G)-1$. $\square$

1.9 *Lemma A5.* Since $x$ is co-transversal, $\tau(G-x)=\tau(G)-1$. Let $T'$ be a minimum transversal of $G-x$.
1. $T'\cup\{x\}$ is a transversal of $G$, since the only edge at $x$ is $\{x,x_1,x_2\}$. It has $\tau(G)$ vertices, so it is a minimum transversal containing $x$.
2. Hence it avoids $y,z$ (NC pairs).
3. Also $x_1\notin T'$: otherwise $T'$ would be a transversal of $G$ with $\tau(G)-1$ vertices.
4. So $T'$ misses $\{x_1,y,z\}$.
5. As $T'$ meets every edge of $G-x$, the set $\{x_1,y,z\}$ (three distinct vertices) is not an edge of $G-x$. It is not an edge at $x$ either. So $M$ has exactly $m-1+1=m$ edges.
6. A transversal of $M$ restricts to one of $G-x$. If the restriction is minimum, it misses $\{x_1,y,z\}$, and an extra vertex is needed. So $\tau(M)=\tau(G-x)+1=\tau(G)$, attained by $T'\cup\{x_1\}$. $\square$

1.10 *Lemma A6.* A minimum transversal meets every edge but avoids $Y$, so $Y\notin E(F)$. A transversal of $F+Y$ with $\tau(F)$ vertices would be a minimum transversal of $F$ meeting $Y$, so $\tau(F+Y)\ge\tau(F)+1$. Adding a vertex of $Y$ to a minimum transversal of $F$ attains this. $\Delta s=2-11$. $\square$

1.11 *Lemma A7.*
- *$\tau$.* Let $T^+$ be a transversal of $F^+$. Then $T=T^+\cap V(F)$ is a transversal of $F$, and each edge $\{w_i\}\cup P_i$ with $T\cap P_i=\emptyset$ forces $w_i\in T^+$. Conversely, $T\cup\{w_i:T\cap P_i=\emptyset\}$ is a transversal.
- *Membership, by induction on $k$.* Add the edges one at a time; when $\{w_j\}\cup P_j$ is added, $P_j$ lies inside no earlier edge, since the earlier new edges meet $P_j$ in nothing ($P$'s disjoint, $w_i$ new).
  - The new edge meets every edge in at most one vertex.
  - $w_j$ has degree 1, so no copy of $F_7$ uses it.
  - (P3) holds as in 1.6.
- *Counting.* $\Delta n=\Delta m=k$, so $\Delta s=5k-11\Delta\tau$. $\square$

1.12 *Lemma A9.*
1. By A8(b) (pair $\{a,b\}$, $a$ co-transversal), $\tau(G-a-b)=\tau(G)-1$. By 0.3, $\tau(G-a-b)-1\le\tau(G-a-b-c)\le\tau(G-a-b)$.
2. *The case of drop 1.* If $\tau(G-a-b-c)=\tau(G)-1$, then 0.4 gives $s(G-a-b-c)=s(G)-9-2|\partial|+11$, where $\partial=\partial_G(\{a,b,c\})$. Each of $a,b,c$ has degree $\ge1$, and no edge contains all three, so $|\partial|\ge2$. Hence $s(G-a-b-c)\le s(G)-2$.
3. If $s(G)\le1$ and $s(G-a-b-c)\ge0$, the drop 1 is excluded (it gives slack $\le-1$). So $\tau(G-a-b-c)=\tau(G)-2$, and 0.4 gives the formula.
4. *No vertex with all its edges meeting the other two.* If all edges at $c$ met $\{a,b\}$, then $c$ would be isolated in $G-a-b$, hence avoided, and $\tau(G-a-b-c)=\tau(G-a-b)=\tau(G)-1$, which was excluded in item 3.
5. If $b$ (resp. $c$) is also co-transversal, items 1-4 apply with that vertex in the role of $a$. This excludes the case where all edges at $a$ meet $\{b,c\}$ (resp. all edges at $b$ meet $\{a,c\}$). $\square$

1.13 *Lemma A10.*
- *$\tau$.* Let $T^+$ be a transversal of $K+w(B,C)$. Then $T^+\cap V(K)$ is a transversal of $K$, and if $w\notin T^+$ it meets $B$ and $C$. For every minimum transversal $T$ of $K$, the set $T\cup\{w\}$ is a transversal. This gives the $\tau$ statement. $\Delta s=3+4-11\Delta\tau$.
- *Linear.* The two new edges meet only in $w$ ($B\cap C=\emptyset$). A new edge meets an old edge $f$ in $f\cap B$ or $f\cap C$, which has size $\le1$.
- *(P3).* Let $S'$ be a vertex set with $|S'|\ge2$ and $w\in S'$; sets without $w$ are unaffected. Then $e(S')=e_K(S'\setminus w)+[B\subseteq S']+[C\subseteq S']$.
  - If neither $B$ nor $C$ lies in $S'$: $e(S')=e_K(S'\setminus w)\le\max(0,|S'|-3)$.
  - If exactly one does: $|S'\setminus w|\ge2$ and $e(S')\le|S'|-2$.
  - If both do: $e(S')\le|S'|-2$ unless $e_K(S'\setminus w)=|S'\setminus w|-2$, i.e. unless $S'\setminus w\supseteq B\cup C$ is a tight set of $K$. Conversely, such a tight set violates (P3) after adding $w$.
- *$F_7$ through $w$.*
  1. $w$ has degree 2, so a copy containing $w$ uses both edges at $w$, and $w$ is not its centre.
  2. One edge at $w$, say $\{w\}\cup B$, passes through the centre, so the centre is some $\beta_1\in B$. The other edge, $\{w\}\cup C$, avoids the centre.
  3. The centre $\beta_1$ has two more edges, each meeting $\{w\}\cup C$ in exactly one vertex. That vertex is not $w$, whose two edges are already used. So the two edges are $\{\beta_1,\gamma_1,q\}$ and $\{\beta_1,\gamma_2,r\}$.
  4. The second edge avoiding the centre consists of the remaining vertices of the three centre edges: $\{\beta_2,q,r\}$.
  5. These three edges do not contain $w$, so they are edges of $K$. The case with $B$ and $C$ exchanged is symmetric.
  6. Conversely, suppose the three edges exist. The seven vertices $w,\beta_1,\beta_2,\gamma_1,\gamma_2,q,r$ are distinct:
     - $q\ne\beta_2$ and $q\ne\gamma_2$, since otherwise $B$ or $C$ would lie inside an edge;
     - $q\ne r$ by linearity;
     - the same holds for $r$.
  7. With the two edges at $w$, these three edges form $F_7$ with centre $\beta_1$. $\square$

1.14 *Lemma A11.* Let $R=\{a,b,c,v,x,y,z\}$. A transversal $T_\Gamma$ of $\Gamma$ restricts to a transversal $T=T_\Gamma\cap V(G'')$ of $G''$. Let $k(T)$ be the number of pairs among $A,B,C$ that $T$ misses.
1. $T_\Gamma\cap R$ must:
   - meet $e_0,h_a,h_b,h_c$;
   - contain the pendant vertex of each missed pair (its edge has only that vertex outside $V(G'')$).
2. The least possible size of $T_\Gamma\cap R$ is $g(k)$, where $g(0)=2$, $g(1)=g(2)=3$, $g(3)=4$:
   - *$k=0$.* No single vertex meets the four hub edges: $x$ meets $e_0,h_a$; $y$ meets $e_0,h_b$; $z$ meets $e_0,h_c$; $v$ meets $h_a,h_b,h_c$; $a,b,c$ meet one edge each. The set $\{v,x\}$ works.
   - *$k=1$ (say $A$ missed).* $a$ is forced and meets $h_a$. No single vertex meets $e_0,h_b,h_c$, and $\{y,z\}$ does.
   - *$k=2$ (say $A,B$ missed).* $a,b$ are forced, and $z$ meets $e_0,h_c$.
   - *$k=3$.* $a,b,c$ are forced, and one vertex of $e_0$ is needed.
3. Hence $\tau(\Gamma)=\min_T\bigl(|T|+g(k(T))\bigr)$ over the transversals $T$ of $G''$. Since $2\le g\le4$, this lies in $[\tau''+2,\tau''+4]$.
4. $\tau(\Gamma)=\tau''+4$ iff every transversal $T$ has $|T|+g(k(T))\ge\tau''+4$. Since $g\ge2$, this is automatic for $|T|\ge\tau''+2$, so it amounts to two conditions:
   - every $T$ with $|T|=\tau''$ has $k=3$, which is (i);
   - every $T$ with $|T|=\tau''+1$ has $k\ge1$, which is (ii).
5. *Slack.* $\Delta s=21+14-44=-9$.
6. *Membership.* $G''^+(A,B,C)\in\mathcal C$ by A7, and $\{a,b,c\}$ is not an edge of it (the only edge at $a$ is $\{a\}\cup A$). So $\Gamma\in\mathcal C$ by A1. $\square$

1.15 *Lemma A12.*
- (a) An edge inside $S$ or inside $S'$ lies inside $S\cup S'$, and an edge inside both lies inside $S\cap S'$. So
  $$e(S\cup S')\ge e(S)+e(S')-e(S\cap S')\ge(|S|-2)+(|S'|-2)-(|S\cap S'|-2)=|S\cup S'|-2,$$
  using (P3) for $S\cap S'$ ($|S\cap S'|\ge2$). The reverse inequality is (P3). And $|S\cup S'|\ge3$.
- (b) Any two tight sets containing $X$ meet in at least $|X|\ge2$ vertices. Apply (a) repeatedly; each partial union contains $X$.
- (c) If an edge $f$ has $|f\cap S_X|=2$ and third vertex $r\notin S_X$, then $e(S_X\cup\{r\})\ge|S_X|-1=|S_X\cup\{r\}|-2$. So $S_X\cup\{r\}$ is a tight set containing $X$, contradicting maximality.
- (d) If $t\in S$ lies in no edge inside $S$, then $e(S\setminus t)=|S|-2=|S\setminus t|-1$ with $|S\setminus t|\ge2$, violating (P3). $\square$

### Step 2. Proofs of Theorem B, Theorem B′ and Corollary B.3
2.1 *Set-up for Theorem B.*
- $s(G)\ge0$ by $(\mathrm H_n)$, so $s(G)\in\{0,1\}$.
- $G$ is connected and $\{a,b,c\}$ is not an edge, so $n(G)\ge4$ (0.6).
- Every vertex has degree $\ge1$ (0.6) and is co-transversal (0.7, with $(\mathrm H_{n-1})$).
- For a pair, say $\{a,b\}$, write $\sigma_{ab}=\sigma_G(a,b)$.

2.2 *Rule R1: if $\sigma_{ab}=0$, then $d(c)=1$; likewise for the other two pairs.*
1. Lemma A3 applies to $(c;a,b)$: $c$ is co-transversal, $\{a,c\},\{b,c\}$ are NC, and $a,b$ are non-adjacent.
2. So $G^{\rm p}(c;a,b)\in\mathcal C$ has $n$ vertices and slack $s(G)+2-2d(c)$, which is $\ge0$ by $(\mathrm H_n)$.
3. Hence $d(c)\le(s(G)+2)/2\le3/2$, and $d(c)\ge1$ (2.1).

No degree bound is used.

2.3 *Rule R2: $d(p)+d(q)-\sigma_{pq}\le3$ for every pair $\{p,q\}\subseteq\{a,b,c\}$.*
1. Lemma A8(b) applies: $p$ is co-transversal and $\{p,q\}$ is NC.
2. So $0\le s(G-p-q)=s(G)+5-2|\partial(p,q)|$ by $(\mathrm H_{n-2})$, i.e. $|\partial(p,q)|\le3$.
3. Finally $|\partial(p,q)|=d(p)+d(q)-\sigma_{pq}$ (0.5).

2.4 *Rule R3: no vertex of the triple has all its edges meeting the other two.* Lemma A9 applies:
- all three vertices have degree $\ge1$ and are co-transversal;
- $\{a,b,c\}\notin E(G)$;
- $s(G)\le1$;
- $s(G-a-b-c)\ge0$ by $(\mathrm H_{n-3})$.

2.5 *Degree bound (L025 Remark 10.4).* Suppose $d(a)\ge3$.
1. R2 for $\{a,b\}$ gives $d(b)\le\sigma_{ab}\le1$, so $d(b)=1=\sigma_{ab}$. Likewise $d(c)=1=\sigma_{ac}$.
2. The only edges at $b$ and at $c$ both contain $a$. They are different edges, because an edge containing $a,b,c$ would be $\{a,b,c\}$.
3. So $b,c$ are not adjacent, and R1 for $\{b,c\}$ gives $d(a)=1$, a contradiction.

Hence $d(a),d(b),d(c)\le2$.

2.6 *The four adjacency patterns.*
- (i) *All three pairs adjacent.* The edges $e_{ab}\supseteq\{a,b\}$, $e_{ac}\supseteq\{a,c\}$, $e_{bc}\supseteq\{b,c\}$ are pairwise distinct: an edge containing two of the pairs contains $a,b,c$. So $c$ lies in the two distinct edges $e_{ac},e_{bc}$. As $d(c)\le2$ (2.5), these are all its edges, and both meet $\{a,b\}$. This contradicts R3.
- (ii) *Exactly two adjacencies*, say $\sigma_{ab}=\sigma_{ac}=1$ and $\sigma_{bc}=0$. R1 for $\{b,c\}$ gives $d(a)=1$, but $a$ lies in the distinct edges $e_{ab},e_{ac}$.
- (iii) *Exactly one*, say $\sigma_{ab}=1$. R1 for $\{a,c\}$ gives $d(b)=1$, and R1 for $\{b,c\}$ gives $d(a)=1$. The only edge at $b$ is $e_{ab}$, which meets $\{a,c\}$. This contradicts R3.
- (iv) *None.* R1 for the three pairs gives $d(a)=d(b)=d(c)=1$, and no edge contains two of them. So the triple is pendant.

2.7 *$s(G)=1$.* In case (iv), $a,b$ are non-adjacent and $\{a,c\},\{b,c\}$ are NC pairs. Lemma A2 gives $G\oplus^\circ(a,b\,|\,c)\in\mathcal C$ with $n+2$ vertices and slack $s(G)-1$, which is $\ge0$ by $(\mathrm H_{n+2})$. So $s(G)\ge1$, and $s(G)=1$ by 2.1. $\square$

2.8 *Theorem B′.* Let $\{a,b,c\}\notin E(G)$, and suppose no minimum transversal contains two of $a,b,c$ (pairwise NC).
1. *Each pair has $|\partial|\le2$.* For each pair, say $\{a,b\}$: $G-a-b\in\mathcal C$ has $n(G)-2$ vertices, so $s(G-a-b)\ge0$. Lemma A8(b) (first part, for an NC pair) gives $0\le s(G-a-b)\le s(G)+5-2|\partial(a,b)|=5-2|\partial(a,b)|$. So $|\partial(a,b)|\le2$.
2. *Each pair is adjacent.* If some pair, say $\{a,b\}$, were non-adjacent, Lemma A2 would give $G\oplus^\circ(a,b\,|\,c)\in\mathcal C$ with $n(G)+2$ vertices and slack $s(G)-1=-1$, contradicting the hypothesis.
3. *Contradiction.* With three adjacent pairs, the edges $e_{ab},e_{ac},e_{bc}$ are pairwise distinct (as in 2.6(i)). So $d(a),d(b)\ge2$, and $|\partial(a,b)|=d(a)+d(b)-1\ge3$, contradicting item 1. $\square$

Neither connectivity nor a degree bound is used. Theorem B also covers this case when $G$ is connected and $(\mathrm H_{n+2})$ holds.

2.9 *Corollary B.3.* Suppose no minimum transversal contains two of $a,b,c$. Then they are pairwise NC, and Theorem B gives $s(G)=1$ and a pendant triple, contrary to the hypothesis. The equivalence with $s(G\oplus(a,b,c))=s(G)+9$ is Lemma A1. $\square$

### Step 3. Proof of Theorem P
3.1 *Shape.*
- $a,b,c$ have degree 1, and no two of them share an edge. So $e_a,e_b,e_c$ are distinct and $b,c\notin A$, etc.
- $W\subseteq V(G'')$, and $\partial_G(\{a,b,c\})=\{e_a,e_b,e_c\}$.
- $G$ is $G''$ plus three pendant edges: $n(G'')=n-3$ and $m(G'')=m-3$.
- No pair among $A,B,C$ lies inside an edge of $G''$: such an edge would share two vertices with $e_a$, $e_b$ or $e_c$.
- $|A\cap B|\le1$, etc., since $e_a,e_b$ share at most one vertex. So $|W|\ge3$.
- Every vertex of $G$ is co-transversal (0.7, with $(\mathrm H_{n-1})$).

3.2 *(a).*
1. Lemma A9 applies, with $s(G)=1$, $|\partial|=3$ and $(\mathrm H_{n-3})$. It gives $\tau''=\tau(G)-2$ and $s(G'')=1+13-6=8$.
2. Suppose a minimum transversal $T$ of $G''$ met $A$. Then $T\cup\{b,c\}$ would be a transversal of $G$ with $\tau(G)$ vertices containing $b,c$, contradicting the NC pair $\{b,c\}$. The same holds for $B$ and $C$.
3. A transversal of $G''$ that meets $A,B,C$ is a transversal of $G$, so it has $\ge\tau(G)=\tau''+2$ vertices.
4. *The pair $A$ (the others are the same).* A minimum transversal $T_G$ of $G$ containing $a$ avoids $b,c$ (NC). So $T_G\setminus\{a\}$ is a $(\tau''+1)$-transversal of $G''$ meeting $B$ and $C$ (to cover $e_b,e_c$).

3.3 *(b).*
1. By 0.6 (with $Z=\{a,b,c\}$), every component $K$ of $G''$ contains a vertex of $W$.
2. That vertex is avoided in $K$. Otherwise a minimum transversal of $K$ containing it, together with minimum transversals of the other components, would be a minimum transversal of $G''$ meeting $W$ (0.1), contradicting (a).
3. Each $K$ has $s(K)\ge0$ by $(\mathrm H_{n-3})$.
4. Let $u$ be an avoided vertex of $K$.
   - If $d_K(u)\ge1$: $s(K)=s(K-u)+3+2d_K(u)\ge5$, by A8(a) and $(\mathrm H_{n-4})$.
   - If $d_K(u)=0$: $K=\{u\}$ and $s(K)=3$.
5. Since $\sum_Ks(K)=8$, there are at most two components. If there are two, one is a single vertex $w_0\in W$ and the other, $K$, has $s(K)=5$ and contains $W'=W\setminus\{w_0\}$, with $|W'|\ge2$.
6. Each $u\in W'$ is avoided in $K$, so $5=s(K-u)+3+2d_K(u)$ forces $d_K(u)\le1$. Also $d_K(u)\ge1$ (0.6). So $d_K(u)=1$.
7. *Some two vertices of $W'$ are non-adjacent.* Otherwise every two vertices of $W'$ share their unique edges, so $W'\subseteq g$ for a single edge $g$.
   - No pair among $A,B,C$ lies inside $g$ (3.1), so each pair contains $w_0$, i.e. $w_0\in A\cap B\cap C$.
   - Then a minimum transversal of $G''$ plus $w_0$ meets $A,B,C$ with $\tau''+1$ vertices, contradicting (a).
8. Let $u_2,u_3\in W'$ be non-adjacent, and $Y=\{w_0,u_2,u_3\}$. Then $G''+Y\in\mathcal C$:
   - it is linear, because $w_0$ is isolated in $G''$ and $u_2,u_3$ are non-adjacent;
   - $w_0$ has degree 1 in $G''+Y$, so no copy of $F_7$ uses $Y$;
   - for $S\supseteq Y$, $e(S)=e_{G''}(S\setminus w_0)+1\le|S|-2$, as $|S\setminus w_0|\ge2$; other sets are unaffected.
9. All of $Y$ is avoided in $G''$ ($w_0$ is isolated; $u_2,u_3\in W$ by (a)). So by A6, $s(G''+Y)=-1$ with $n-3$ vertices, contradicting $(\mathrm H_{n-3})$.

Hence $G''$ is connected.

3.4 *(c).*
1. *Degrees.* $G''$ is connected with $\ge3$ vertices, so its degrees are $\ge1$. A vertex of $W$ lies in a pendant edge of $G$, so its $G''$-degree is $\le\Delta(G)-1\le2$.
2. Suppose $u\in A\cap B$. Then $u\notin C$: otherwise $u$ added to a minimum transversal of $G''$ meets $A,B,C$ with $\tau''+1$ vertices, contradicting (a).
3. Let $x\in C$ and $X=\{u,x\}$. For a transversal $T^*$ of $G''-X$, the set $T^*\cup X$ meets $A,B,C$, so $|T^*|\ge\tau''$ by (a). Hence $\tau(G''-X)=\tau''$ (0.3).
4. By 0.4 and $(\mathrm H_{n-5})$: $0\le s(G''-X)=8-6-2|\partial_{G''}(X)|$, so $|\partial_{G''}(X)|\le1$.
5. As $d_{G''}(u),d_{G''}(x)\ge1$, this forces $d_{G''}(u)=d_{G''}(x)=1$ with a common edge.
6. Applying this to both $x\in C$: the only $G''$-edge $g$ at $u$ contains $C$, so $g=\{u\}\cup C$. This contradicts 3.1, since $C$ lies inside no edge of $G''$.

So $A,B,C$ are pairwise disjoint.

3.5 *(d).*
1. For a transversal $T^*$ of $G''-X$, the set $T^*\cup X$ meets $A,B,C$, so $|T^*|\ge\tau''-1$.
2. If $\tau(G''-X)=\tau''$, then $s(G''-X)=8-9-2|\partial_{G''}(X)|<0$ (0.4), contradicting $(\mathrm H_{n-6})$.
3. So $\tau(G''-X)=\tau''-1$, and 0.4 gives $s(G''-X)=10-2|\partial_{G''}(X)|\ge0$.

3.6 *(e).*
1. $Y\notin E(G'')$ (A6) and its vertices are pairwise non-adjacent, so $G''+Y$ is linear.
2. Its slack is $-1$ (A6) with $n-3$ vertices, so $G''+Y\notin\mathcal C$ by $(\mathrm H_{n-3})$.
3. A copy of $F_7$ in $G''+Y$ uses $Y$, since $G''\in\mathcal C$.
4. A set $S$ violating (P3) contains $Y$, and $e_{G''}(S)=e(S)-1\ge|S|-2$. So $S$ is a tight set of $G''$ ($|S|\ge3$).
5. *Shapes of a copy.*
   - If $Y$ is one of the two edges avoiding the centre $o$: the three edges through $o$ meet $Y$ in one vertex each, and the fifth edge consists of their third vertices. This is the first shape.
   - If $Y$ passes through the centre: the centre is some $y_i$, with two further edges $\{y_i,p,q\},\{y_i,r,s\}$. Each of the two edges avoiding the centre contains one of the other two vertices of $Y$, one of $p,q$ and one of $r,s$. This is the second shape.

3.7 *(f), identification.*
1. $a$ is co-transversal (3.1), $\{a,b\}$ is NC, $a,b$ are non-adjacent, and $N_G(a)\cap N_G(b)=A\cap B=\emptyset$ by (c).
2. By A4, $G_{a=b}$ is linear with $n-1$ vertices and slack $s(G)-3=-2$, so $G_{a=b}\notin\mathcal C$ by $(\mathrm H_{n-1})$.
3. *The tight-set case.* By A4, either $G$ has a tight set $S\ni a,b$, or $G_{a=b}$ has a copy of $F_7$ through the merged vertex $w$. Suppose first that $S$ is a tight set of $G$ containing $a,b$.
   - $e_a\subseteq S$: otherwise $e_G(S\setminus a)=e_G(S)=|S\setminus a|-1$ with $|S\setminus a|\ge2$, violating (P3).
   - Likewise $e_b\subseteq S$, and $e_c\subseteq S$ if $c\in S$.
   - Removing the vertices of $\{a,b,c\}\cap S$ removes as many edges, all pendant. So $S\setminus\{a,b,c\}$ is a tight set of $G''$ containing $A\cup B$; it has $\ge4$ vertices.
   - Conversely, a tight set $S''\supseteq A\cup B$ of $G''$ gives the tight set $S''\cup\{a,b\}$ of $G$.
4. *The $F_7$ case.* Here $w$ has degree 2 in $G_{a=b}$ (edges $\{w\}\cup A$, $\{w\}\cup B$).
   - So $w$ is not the centre. Its two edges are one edge through the centre and one avoiding it.
   - $c$ has degree 1, so $c$ and $e_c$ are not in the copy.
   - If $\{w\}\cup A$ passes through the centre, the centre is some $a_i$. Its other two edges meet $\{w\}\cup B$ in $b_1$ and $b_2$, so they are $\{a_i,b_1,q\},\{a_i,b_2,r\}$. The second edge avoiding the centre is $\{a_{3-i},q,r\}$.
   - The case where $\{w\}\cup B$ passes through the centre is symmetric, with $A$ and $B$ exchanged.
   - Conversely, these five edges form $F_7$; the seven vertices are distinct as in 1.13, using 3.1.
5. The pairs $\{a,c\}$ and $\{b,c\}$ are treated the same way.

3.8 *(f), move.* By A5 ($a$ co-transversal of degree 1; $\{a,b\},\{a,c\}$ NC; $b,c\notin\{a,a_i\}$), $M=M(a\to a_i;b,c)$ has $n-1$ vertices and slack $-2$. So $M\notin\mathcal C$ by $(\mathrm H_{n-1})$.
- *Linear.* $e_b\cap\{a_i,b,c\}=\{b\}$ and $e_c\cap\{a_i,b,c\}=\{c\}$, by (c). Every other edge of $G-a$ contains neither $b$ nor $c$, so it meets the new edge at most in $a_i$.
- *$F_7$.* Let $F$ be a copy of $F_7$ in $M$.
  1. $F$ uses the new edge, since $G-a\in\mathcal C$.
  2. $b$ and $c$ have degree 2 in $M$, so $e_b,e_c\in F$, and $V(F)=\{a_i,b,c\}\cup B\cup C$ (seven distinct vertices by (c)).
  3. The other two edges $f_1,f_2$ of $F$ avoid $b$ and $c$, which already have $F$-degree 2. So they lie in $G''$ inside $\{a_i\}\cup B\cup C$.
  4. *Degree count.* After the first three edges, $a_i,b_1,b_2,c_1,c_2$ have degree 1 and $b,c$ have degree 2. To reach the degrees $3,2,2,2,2,2,2$, the edges $f_1,f_2$ must meet in one vertex $o$ and cover $\{a_i\}\cup B\cup C$.
  5. Neither $f_j$ contains $B$ or $C$ (3.1). So $o\notin B\cup C$: if $o=b_1$, then $b_2\in f_1\cup f_2$ would put $B$ inside an edge.
  6. Hence $o=a_i$, $f_1=\{a_i,b_j,c_k\}$ and $f_2=\{a_i,b_{3-j},c_{3-k}\}$.
  7. Conversely, these five edges form $F_7$ with centre $a_i$: the non-centre edges $e_b,e_c$ are disjoint and meet each centre edge once.
- *(P3).*
  1. A set $S$ violating (P3) in $M$ contains the new edge $\{a_i,b,c\}$, since otherwise $e_M(S)=e_{G-a}(S)\le|S|-2$. Then $e_{G-a}(S)=e_M(S)-1\ge|S|-2$, so by (P3) in $G-a$ the set $S$ is a tight set of $G-a$.
  2. As $b,c$ have degree 1 in $G-a$, it contains $e_b$ and $e_c$ (as in 3.7).
  3. Removing $b,c$ leaves a tight set of $G''$ containing $\{a_i\}\cup B\cup C$.
  4. Conversely, a tight set $S''\supseteq\{a_i\}\cup B\cup C$ of $G''$ gives $e_M(S''\cup\{b,c\})=|S''|+1=|S''\cup\{b,c\}|-1$.

3.9 *(g).*
1. $F^+=G''^+(P,Q)\in\mathcal C$ (A7) has $n-1$ vertices and $m-1$ edges.
2. Minimum transversals of $G''$ miss $P\cup Q$ (a), so they contribute $\tau''+2$ to the formula of A7.
3. Suppose no $(\tau''+1)$-transversal met both $P$ and $Q$. Then every transversal would contribute at least $\tau''+2$, so $\tau(F^+)=\tau''+2$.
4. Then $s(F^+)=8+6+4-22=-4$, contradicting $(\mathrm H_{n-1})$.

3.10 *(h).*
1. Suppose neither alternative holds. Every transversal then contributes at least $\tau''+3$ in A7:
   - a $\tau''$-transversal misses all three pairs;
   - a $(\tau''+1)$-transversal misses at least two;
   - a $(\tau''+2)$-transversal misses at least one.
2. Then $s(G''^+(P,Q,R))=8+9+6-33=-10$ with $n$ vertices, contradicting $(\mathrm H_n)$.

3.11 *(i).* Minimum transversals of $G''$ avoid $W$ (a) and meet every edge. So no edge lies inside $W$, and an edge with two vertices in $W$ is met in its third vertex.

3.12 *(j).*
1. *Two tight sets from the moves.* By (f), $M(a\to a_1;b,c)$ is linear and not in $\mathcal C$. A copy of $F_7$ in it would need the edges $\{a_1,b_j,c_k\},\{a_1,b_{3-j},c_{3-k}\}$ of $G''$ inside $W$, which (i) excludes. So $G''$ has a tight set $S_1\supseteq\{a_1\}\cup B\cup C$. In the same way it has a tight set $S_2\supseteq\{a_2\}\cup B\cup C$.
2. *A tight set containing $W$.* As $|S_1\cap S_2|\ge4$, $S_1\cup S_2\supseteq W$ is tight (A12(a)). Let $S_0=S_W$ (A12(b)).
3. *The tight sets of $G$ and of $G\oplus(a,b,c)$.* $e_G(S_0\cup\{a,b,c\})=e_{G''}(S_0)+3=|S_0\cup\{a,b,c\}|-2$, since the three pendant edges lie inside. Adding $v,x,y,z$ adds the four hub edges, all inside, giving $|S_0|+5$ edges on $|S_0|+7$ vertices.
4. *Leaving edges.* An edge of $G''$ meeting both $S_0$ and its complement has exactly one vertex in $S_0$, by A12(c).
5. *Edges at $W$.* Every vertex of $W$ lies in an edge inside $S_0$, by A12(d).
6. *The saturated case.* If $S_0=V(G'')$, then $m(G'')=n(G'')-2$, so $m(G)=n-2$ and $m(G\oplus(a,b,c))=n(G\oplus(a,b,c))-2$. Then $1=s(G)=5n-4-11\tau(G)$ gives $5n\equiv5$, i.e. $n\equiv1\pmod{11}$.

3.13 *(k).*
1. *Degree count.* $G$ is saturated with $\Delta\le3$ and no isolated vertex, so $\sum_t(3-d_G(t))=3n-3m=6$, i.e. $2n_1+n_2=6$. As $n_1\ge3$ ($a,b,c$), we get $n_1=3$ and $n_2=0$.
2. *$G''$-degrees.* A vertex of $W$ lies in exactly one pendant edge (by (c)), so its $G''$-degree is 2. A vertex of $G''$ outside $W$ has $G''$-degree 3.
3. *Avoided vertices.* A vertex outside $W$ is co-transversal in $G''$ by A8(a): $s(G''-t)\ge0$ by $(\mathrm H_{n-4})$, and $8<3+6$. $W$ is avoided by (a). So the avoided vertices of $G''$ are exactly $W$.
4. *Edges with two vertices in $X$.* For $X$ as in (d), all three vertices have $G''$-degree 2, and no edge contains all three (i). So $|\partial_{G''}(X)|=6-p$, where $p$ is the number of edges with two vertices in $X$. By (d), $p\ge1$. $\square$

### Step 4. Proof of Lemma Q
4.1 *Set-up.* Write $e=\{p,q,c\}$ with $p,q\in V_1$ and $c\in V_2$, and let $H_i=H[V_i]$.
1. Both $H_i$ lie in $\mathcal C$ and have fewer vertices than $H$, so $s(H_i)\ge0$.
2. $n$ and $\tau$ are additive over $H_1\sqcup H_2$, and $m(H)=m(H_1)+m(H_2)+1$.
3. A transversal of $H$ restricts to transversals of $H_1,H_2$, and $T_1\cup T_2\cup\{c\}$ is a transversal. So $\tau(H)\in\{\tau(H_1)+\tau(H_2),\tau(H_1)+\tau(H_2)+1\}$.
4. The first value gives $s(H)=s(H_1)+s(H_2)+2\ge2$, which is impossible.
5. So $\tau(H)=\tau(H_1)+\tau(H_2)+1$. Hence no minimum transversal of $H_1$ meets $\{p,q\}$ and none of $H_2$ contains $c$: otherwise $T_1\cup T_2$ would cover $e$.

4.2 *The case $|V_2|\ge2$.* Suppose $|V_2|\ge2$.
1. *$H_2$ is connected.* $H$ is connected (0.8). By 0.6 with $Z=V_1$, every component of $H_2$ contains a vertex of an edge meeting $V_1$, i.e. a vertex of $e\setminus V_1=\{c\}$. So $H_2$ is connected with $\ge2$ vertices, and $d_{H_2}(c)\ge1$ (0.6).
2. *The auxiliary graph $H^\#$.* Let $H^\#=H_1^+(\{p,q\})$.
   - $p,q$ lie in no common edge of $H_1$ (linearity, as both lie in $e$), so $H^\#\in\mathcal C$ (A7).
   - It has $|V_1|+1\le n(H)-1$ vertices.
   - By A7 and 4.1, $\tau(H^\#)=\tau(H_1)+1$.
   - So $0\le s(H^\#)=s(H_1)-6$.
3. *The slack of $H_2$.* $c$ is avoided in $H_2$, so $s(H_2)=s(H_2-c)+3+2d_{H_2}(c)$ (A8(a)), with $s(H_2-c)\ge0$.
4. Hence $s(H)=s(H_1)+s(H_2)+2-11=s(H^\#)+s(H_2-c)+2d_{H_2}(c)\ge2$, a contradiction. So $|V_2|=1$. $\square$

### Step 5. Proofs of Theorem C and Corollaries C.2, C.3
5.1 *The facts used at $v$.* These are L017 Theorem 4(i), (ii), (iv)(b), re-proved for pattern (b).
1. *The six co-vertices.* They are distinct (0.5). Each has $H$-degree $\le3$ (0.8) and lies in exactly one edge with $v$, so its $(H-v)$-degree is at most 2.
2. *Slack of $H-v$.* By 0.8, $\tau(H-v)=\tau(H)-1$ and $s(H-v)=s(H)+2\ge0$. As $s(H)\le-1$, $s(H-v)\in\{0,1\}$.
3. *The components.* $F_1,F_2\in\mathcal C$ (0.2) have fewer vertices, so $s(F_i)\ge0$, and $s(F_1)+s(F_2)=s(H)+2\le1$ (0.1).
4. *Free choice.* Each $F_i$ is connected and contains three distinct co-vertices, so it has no isolated vertex (0.6). So every vertex $t$ of $F_i$ is co-transversal in $F_i$: $s(F_i-t)\ge0$ by $(\mathrm H_{n(H)-1})$ and $s(F_i)\le1<5\le3+2d_{F_i}(t)$ (A8(a)).
5. *No two co-vertices in one minimum transversal.* If a minimum transversal $T_1$ of $F_1$ contained $x_j,x_k$ ($j\ne k$), choose a minimum transversal $T_2\ni y_l$ of $F_2$, where $l$ is the third index. Then $T_1\cup T_2$ is a minimum transversal of $H-v$ (0.1) meeting $P_1,P_2,P_3$. So it is a transversal of $H$ with $\tau(H)-1$ vertices, which is impossible. Hence no minimum transversal of $F_1$ contains two of $x_1,x_2,x_3$, and likewise for $F_2$ and the $y_j$.

5.2 *A component whose attachment triple is an edge is that edge* (L022 Theorem 2(v), re-proved; L026 14.2). Suppose $g=\{y_1,y_2,y_3\}\in E(F_2)$ and $V(F_2)\ne g$. Put $Z=V(F_1)\cup\{v\}\cup g\ne V(H)$.
1. *The edges of $H[Z]$.* They are:
   - the edges of $F_1$;
   - the three edges at $v$;
   - the edge $g$, the only edge of $F_2$ inside $g$.

   There are no other edges, because $F_1,F_2$ are different components of $H-v$.
2. *A lower bound for $\tau(H[Z])$.* A transversal $T$ of $H[Z]$ has at least $\tau(F_1)$ vertices in $V(F_1)$ and a vertex of $g$. Suppose $|T|=\tau(F_1)+1$.
   - Then $T=T_1\cup\{y_j\}$ with $T_1$ a minimum transversal of $F_1$ and $v\notin T$.
   - The edges $\{v,x_k,y_k\}$ ($k\ne j$) then force $x_k\in T_1$ for both $k\ne j$, which contradicts 5.1.

   So $\tau(H[Z])\ge\tau(F_1)+2$.
3. *Contradiction.* $s(H[Z])\le s(F_1)+12+8-22=s(F_1)-2\le-1$, since $s(F_1)\le1$. But $H[Z]\in\mathcal C$ has fewer vertices than $H$, a contradiction.

The same holds with $F_1,F_2$ exchanged.

5.3 *One side is a single edge, and $s(H)=-1$* (L026 14.3).
1. Some $F_i$ is tight, since the slacks are $\ge0$ with sum $\le1$. Let $F=F_1$ be tight, say, and suppose $F$ is not a single edge.
2. By 5.2, $\{x_1,x_2,x_3\}\notin E(F_1)$, and by 5.1 it is pairwise NC in $F_1$.
3. $n(H)=n(F_1)+n(F_2)+1$ and $n(F_2)\ge3$, so $n(F_1)+2\le n(H)-2$. Hence every member of $\mathcal C$ with $n(F_1)\pm2$ vertices satisfies I11.
4. Theorem B′ then gives a contradiction. So every tight component is a single edge.
5. If both components were tight, $H$ would consist of the edges $\{v,x_j,y_j\}$, $\{x_1,x_2,x_3\}$, $\{y_1,y_2,y_3\}$, which form $F_7$ with centre $v$. This is impossible in $\mathcal C$.
6. So exactly one component is tight; name it $F_1$. Then $F_1=\{x_1,x_2,x_3\}$ with $d_H(x_j)=2$, and $s(F_2)=1=s(H)+2$, i.e. $s(H)=-1$.

5.4 *The outer graph.* Put $G'=F_2$; it is connected.
1. *Hub structure.* The edges meeting $\{v,x_1,x_2,x_3\}$ are the four hub edges, so $H=G'\oplus(y_1,y_2,y_3)$. Also $\Delta(G')\le\Delta(H)\le3$, $n(G')=n(H)-4$ and $s(G')=1$.
2. *$\tau(G')$.* Lemma A1 and $s(H)=s(G')-2$ give $\tau(H)=\tau(G')+2$.
3. *A b-configuration.* The $y_j$ have $G'$-degree $\le2$ (5.1) and are pairwise NC (5.1). Also $\{y_1,y_2,y_3\}\notin E(G')$ by 5.2, since $G'$ has slack 1 and is not a single edge. So $\{y_1,y_2,y_3\}$ is a b-configuration of $G'$.
4. *It is pendant.* $(\mathrm H_{n(G')+2})=(\mathrm H_{n(H)-2})$ holds, so Theorem B makes the triple pendant. Hence $d_{G'}(y_j)=1$ and $d_H(y_j)=2$.

This proves (1) and (2).

5.5 *(3) and the first case of (4).* $G'$ satisfies the hypotheses of Theorem P: connected, $\Delta\le3$, $s=1$, $(\mathrm H_{n(G')})$ since $n(G')<n(H)$, and a pendant b-configuration. So (a)-(k) hold.
- Proposition J holds as well (Step 6.4), with $(\mathrm H_{n(G')-3})$.
- The listed facts are P(a), (b), (c), (j); $\tau(G'')=\tau(G')-2=\tau(H)-4$.
- In the case $S_0=V(G'')$, the facts are P(j), (k), and $n(H)=n(G')+4\equiv5\pmod{11}$.

5.6 *(4): at least two leaving edges when $S_0\ne V(G'')$.*
1. $S_H$ is tight in $H$ (P(j)).
2. The hub and pendant edges lie inside $S_H$. So the edges of $H$ leaving $S_H$ are exactly the edges of $G''$ leaving $S_0$, each meeting $S_H$ in exactly one vertex (P(j)).
3. If $S_0\ne V(G'')$, then $S_H\ne V(H)$, and at least one edge leaves, since $H$ is connected.
4. If exactly one edge $e$ left, Lemma Q with $V_2=S_H$ and $V_1=V(H)\setminus S_H$ (so $|e\cap V_2|=1$) would give $|S_H|=1$. But $|S_H|\ge13$. $\square$

5.7 *Corollary C.2.*
1. *The hub edges.* $d_H(v)\ge3$ (three hub edges), and $\Delta(H)\le3$ (0.8). So $d_H(v)=3$, and the edges meeting $\{v,x,y,z\}$ are exactly the four hub edges.
2. *The outer triple.* $a,b,c$ are distinct and outside $\{v,x,y,z\}$ (linearity of the hub edges). Moreover $\{a,b,c\}\notin E(G')$, since otherwise the four hub edges and $\{a,b,c\}$ would form $F_7$ with centre $v$. So $H=G'\oplus(a,b,c)$.
3. *Slack and NC pairs.* $G'\in\mathcal C$ is smaller than $H$, so $s(G')\ge0$. By Lemma A1, $s(H)\in\{s(G')+9,s(G')-2\}$. As $s(H)<0$, $\tau(H)=\tau(G')+2$: no minimum transversal of $G'$ contains two of $a,b,c$, and $s(G')=s(H)+2\le1$.
4. *Connectivity.* $H$ is connected (0.8). So by 0.6 every component of $G'$ contains a vertex of a hub edge outside $\{v,x,y,z\}$, i.e. one of $a,b,c$.
   - Every component $K$ has $s(K)\ge0$, and these slacks sum to $\le1$. So no component is an isolated vertex ($s=3$).
   - Every vertex of every $K$ is co-transversal in $K$: $s(K-t)\ge0$ and $s(K)\le1<5\le3+2d_K(t)$ (A8(a)).
   - If two of $a,b,c$, say $a$ and $c$, lay in different components $K_1,K_2$, then minimum transversals $T_1\ni a$ of $K_1$ and $T_2\ni c$ of $K_2$, together with minimum transversals of the other components, would give a minimum transversal of $G'$ (0.1) containing $a$ and $c$. This contradicts item 3.
   - So $a,b,c$ lie in one component, and since every component contains one of them, $G'$ is connected.

   L017 Theorem 4(iii), the Hall condition, gives the same conclusion.
5. *The pattern at $v$.* In $H-v$ the vertices $x,y,z$ keep only $e_0$. So $H-v$ is the disjoint union of the edge $\{x,y,z\}$ and the connected graph $G'$, and every pair $\{x,a\},\{y,b\},\{z,c\}$ is split. The pattern is (b). $\square$

5.8 *Corollary C.3.* Let $s(H)=-2$ and let $v$ have degree 3.
- Patterns (c1), (c2), (d) do not occur (L022 Theorem 2(i) = L018 Theorem 6(b′)).
- Pattern (e) does not occur (L022 Theorem 2(ii)).
- Pattern (f) forces $s(H)=-1$ (L022 Theorem 2(iii)).
- Pattern (b) forces $s(H)=-1$ (Theorem C(1)).

So the pattern is (a). $\square$

### Step 6. Proofs of Theorem D and Proposition J
6.1 *(1) ⟹ (3) and (3) ⟹ (1).*
- *(1) ⟹ (3).* Let $H$ be a minimal counterexample with $N+4$ vertices and a pattern-(b) vertex. By Theorem C(1), (2), $G'$ is:
  - connected, with $\Delta(G')\le3$, $s(G')=1$ and $n(G')=N$;
  - in possession of the pendant b-configuration $\{y_1,y_2,y_3\}$.

  Also $(\mathrm H_{N+3})=(\mathrm H_{n(H)-1})$ holds. So $G'$ violates PT-I($N$).
- *(3) ⟹ (1).* Let $G$ violate PT-I($N$), with pendant b-configuration $\{a,b,c\}$.
  1. $H=G\oplus(a,b,c)\in\mathcal C$ (A1), and $\tau(H)=\tau(G)+2$ because the triple is pairwise NC. So $s(H)=-1$.
  2. $n(H)=N+4$, and $(\mathrm H_{N+3})$ holds, so $H$ is a minimal counterexample.
  3. In $H-v$ the vertices $x,y,z$ keep only $e_0$, so $H-v$ is the edge $\{x,y,z\}$ plus the connected graph $G$, with every pair $\{x,a\},\{y,b\},\{z,c\}$ split.
  4. So $v$ has pattern (b), contradicting (3).

6.2 *(1) ⟺ (2).*
- *A violator of PT-I($N$) gives one of PT-II($N-3$).* Let $G$ violate PT-I($N$). Theorem P applies, since $(\mathrm H_{N+3})$ implies $(\mathrm H_N)$.
  - $G''$ has $N-3$ vertices; it is connected (b), with $\Delta(G'')\le3$ and $s(G'')=8$ (a).
  - $A,B,C$ are pairwise disjoint and lie inside no edge of $G''$ (c), and their vertices have $G''$-degree $\le2$ (c).
  - (i) and (ii) hold by (a).
  - $(\mathrm H_{n(G'')+6})=(\mathrm H_{N+3})$.

  So $G''$ violates PT-II($N-3$).
- *A violator of PT-II($N-3$) gives one of PT-I($N$).* Let $G''$ violate PT-II($N-3$) with $(A,B,C)$, and let $G=G''^+(A,B,C)$ with pendant vertices $a,b,c$.
  1. *Membership and shape.* $G\in\mathcal C$ (A7). It is connected, because $G''$ is connected and each new edge meets it. $\Delta(G)\le3$, because each vertex of $A\cup B\cup C$ gains exactly one edge. And $a,b,c$ have degree 1 and lie in three different edges.
  2. *$\tau(G)$.* By A7, the minimum transversals of $G''$ contribute $\tau''+3$ by (i), and $(\tau''+1)$-transversals contribute at least $\tau''+2$ by (ii). So $\tau''+2\le\tau(G)\le\tau''+3$.
  3. If $\tau(G)=\tau''+3$, then $s(G)=8+15-33=-10$ with $n(G'')+3$ vertices, contradicting $(\mathrm H_{n(G'')+6})$. So $\tau(G)=\tau''+2$ and $s(G)=1$.
  4. *Pairwise NC.* Suppose a minimum transversal $T_G$ of $G$ contained $a$ and $b$.
     - $T=T_G\cap V(G'')$ is a transversal of $G''$ with $|T|\le\tau''$. So $|T|=\tau''$ and $c\notin T_G$.
     - Then $T$ must meet $C$ (edge $\{c\}\cup C$), which contradicts (i).

     The other two pairs are the same.
  5. So $G$ violates PT-I($N$), with $(\mathrm H_{N+3})=(\mathrm H_{n(G'')+6})$.

6.3 *(3) ⟺ (4), the corollary, and (5).*
- *(3) ⟺ (4).* By Corollary C.2 every E1-hub centre has pattern (b), and by Theorem C(1) every pattern-(b) vertex is an E1-hub centre.
- *The corollary.* "PT holds for all $N$" is $\bigwedge_N$(1), which is equivalent to $\bigwedge_N$(3).
- *(5), Form I.* Let $G\in\mathcal C$ have $s(G)=1$, $(\mathrm H_{n(G)+3})$ and a pendant b-configuration; no connectivity or degree bound is assumed. As in 6.1, $H=G\oplus(a,b,c)$ is a minimal counterexample; this step uses neither connectivity nor $\Delta\le3$. Then:
  - Corollary C.2 shows that $G=H-\{v,x,y,z\}$ is connected;
  - $\Delta(G)\le\Delta(H)\le3$ (0.8; this is L017 Theorem 1(c)).
- *(5), Form II.* Let $G''$ satisfy the remaining hypotheses, with $(A,B,C)$. Steps 6.2(1)-(4), except the connectivity and degree claims, show that $G=G''^+(A,B,C)\in\mathcal C$ has $s(G)=1$ and the pendant b-configuration $\{a,b,c\}$. By the Form I case:
  - $G$ is connected with $\Delta(G)\le3$;
  - so $\Delta(G'')\le3$, and the vertices of $A\cup B\cup C$ have $G''$-degree $\le2$;
  - Theorem P applies to $G$ (connected, $\Delta\le3$, $s=1$, $(\mathrm H_{n(G)})$, pendant b-configuration), and Theorem P(b) shows that $G''$ is connected.

  $\square$

6.4 *Proposition J.*
1. *Item 1.* $u$ is avoided in $G''$ by P(a). So $\tau(K_u)=\tau''$, and A8(a) gives $s(K_u)=8-3-2d_{G''}(u)$, with $d_{G''}(u)\in\{1,2\}$ by P(c).
2. *Item 2.* A minimum transversal $T$ of $K_u$ meeting $Y$ and $Z$ would make $T\cup\{u\}$ a transversal of $G''$ with $\tau''+1$ vertices meeting $A,B,C$, contradicting P(a).
3. *Item 3.*
   - $Y,Z$ are disjoint (P(c)) and lie inside no edge of $G''$ (3.1), hence inside no edge of $K_u$.
   - By A10 and item 2, $\tau(K_u+w(Y,Z))=\tau''+1$ and the slack is $s(K_u)-4$.
   - $K_u+w(Y,Z)$ is linear (A10) and has $n(G'')-1+1$ vertices. So it is not in $\mathcal C$ by $(\mathrm H_{n-3})$.
4. *Item 4.* By A10, $K_u$ has a tight set $S\supseteq Y\cup Z$ or an $F_7$-configuration of the stated shape. A tight set of $K_u$ is a tight set of $G''$ not containing $u$ (edges inside $S\not\ni u$ are the same in $K_u$ and $G''$). The edges of $K_u$ are the edges of $G''-u$.
5. *Item 5.* $Y\cup Z\subseteq S_0\setminus\{u\}$ and $|S_0\setminus\{u\}|\ge5$. The number of edges inside $S_0\setminus u$ is $|S_0|-2-d$, where $d\in\{1,2\}$ by P(j). So $S_0\setminus u$ is tight iff $d=1$. $\square$

### Step 7. No circularity
In every statement, I11 is used only through an explicit hypothesis $(\mathrm H_N)$.
- **Theorem B.** I11 is used on members of $\mathcal C$ with at most these numbers of vertices:
  - $n(G)+2$ (fold, 2.7);
  - $n(G)$ (pendant replacement, 2.2);
  - $n(G)-1$ (free choice, 0.7);
  - $n(G)-2$ (pair lemma, 2.3);
  - $n(G)-3$ (triple deletion, 2.4).
- **Theorem B′.** $n(G)+2$ and $n(G)-2$.
- **Theorem P.** At most $n(G)$ vertices:
  - $n$ for three pendant pairs;
  - $n-1$ for identifications, moves, two pendant pairs and free choice;
  - $n-3$ for components, $G''+Y$ and triple deletion;
  - $n-4$ for $K-u$ and in (k);
  - $n-5$ and $n-6$ for $G''-X$.
- **Proposition J.** $n(G)-3$ and $n(G)-4$.
- **Lemma Q, Theorem C, Corollaries C.2, C.3.** $H$ is a minimal counterexample, and every graph to which I11 is applied has at most $n(H)-1$ vertices:
  - $H-u$, $F_i$, $F_i-t$, $H[Z]$ (5.1-5.2);
  - the folds of $F_1$ ($n(F_1)+2\le n(H)-2$) in Theorem B′;
  - Theorem B on $G'$ (at most $n(G')+2=n(H)-2$);
  - Theorem P on $G'$ (at most $n(G')=n(H)-4$);
  - Proposition J (at most $n(H)-7$);
  - $H_1,H_2,H_2-c,H^\#$ in Lemma Q ($|V_1|+1\le n(H)-1$).
- **Theorem D.** I11 is used only through $(\mathrm H_{N+3})$ and the minimality of $H$ ($N+4$ vertices).

The only external inputs are:
- L017's definitions (minimal counterexample, pattern (b));
- L022 Theorem 2 and L018 Theorem 6(b′), in Corollary C.3 only.

## What remains
**GAP: Conjecture PT (the pendant-triple lemma) is not proved.** This is the only GAP of this certificate. By Theorem D it is exactly what remains of pattern (b), in either of these forms:
- PT-I: no connected slack-1 member of $\mathcal C$ with $\Delta\le3$ and $(\mathrm H_{n+3})$ has a pendant b-configuration;
- PT-II: no slack-8 member of $\mathcal C$ with $(\mathrm H_{n+6})$ has three disjoint pairs satisfying (i) and (ii).

PT is not a finite computation: nothing proved here bounds $n$ from above. Every counterexample has the rigid structure listed in Part D (Theorem P, Lemma Q, Proposition J). The two sub-cases are:
- (R1a) $S_0=V(G'')$: saturated, $n(H)\equiv5\pmod{11}$, $n(H)\in\{38,49,60,\dots\}$ given Remark B.5 ($n(H)\ge31$);
- (R1b) $S_0\ne V(G'')$, with at least two leaving edges.

A sufficient condition is Conjecture P2⁺ [conjecture]: a connected slack-1 member of $\mathcal C$ with $\Delta\le3$ has at most two vertices of degree 1. Suggested next steps are in SYNTHESIS.md Section 5, steps 2, 3 and 6:
- a falsifier for PT-II at $24\le n(G'')\le40$;
- an attack on R1a/R1b through $S_0$, J1 and the folds of $H$;
- the P2⁺ census at $n=27..30$.

Completing PT closes pattern (b) of the I11 induction. It does not close pattern (a) (C1-big, panel SYNTHESIS §0.3), which is the core of I11.

## Computer-verified steps
No proof step depends on a computation. Everything below tests the statements on data. All runs are in experiments/prover/L027/: Python 3, exact integer and bitmask arithmetic, own code `hyp27.py` (no import of e757/, judge/ or L0xx code), except E2 and E3, which re-run the panel judge's own `checks.py` unmodified. Each run used `nice -n 10`, one process and `timeout`.
- **E1 (Part A and J1 identities on random members of $\mathcal C$).** Command: `cd experiments/prover/L027 && timeout 1800 nice -n 10 python3 lemmas27.py 1 3000`, giving lemmas27_output.txt (exit 0, 4 min 44 s).
  - The base graphs were 3,000 random members of $\mathcal C$ with $5\le n\le11$, $1\le m\le n-2$, built edge by edge with exact linearity, $F_7$ and (P3) checks.
  - Every applicable configuration was tested, with **0 failures**. The counts:
    - A1: membership and $\tau$ on 12,000 triples;
    - A2: membership and $\tau$, 135,618;
    - A3: membership, $\tau$ and slack, 135,261;
    - A4: linearity, $\tau$, and the "iff" membership criterion with tight sets of size $\ge3$, 21,620;
    - A5: "new edge not an old edge" and $\tau$, 112,928;
    - A6: 43,253;
    - A7: $\tau$ formula 15,048, membership 8,092;
    - A8(a): 11,938; A8(b): 65,284;
    - A9: 64,455 (drop-1 slack, 45,841);
    - A10: $\tau$ 6,458; linearity, the "iff" membership criterion and the exact $F_7$ shape 2,751 each;
    - A11: $\tau\in\{\tau''+2,\tau''+3,\tau''+4\}$ and "$=\tau''+4$ iff (i) and (ii)", 1,640;
    - A12(a): 7,902.
  - *Shows:* the exact statements of Part A, including both "iff" membership criteria and the gadget formula, hold on every tested configuration. A first run had stated the A11 range as $\{\tau''+3,\tau''+4\}$; it found the case $\tau''+2$ (a minimum transversal meeting all three pairs), and the statement and test were corrected before the proof was written.
- **E2 (judge's S2 re-run).** `bash run_s2_s3.sh` (first half), giving S2_rerun_output.txt, which is identical to experiments/prover/e1hub-synthesis/checks/S2_output.txt.
  - The ten stored near-tight lists with $\Delta\le3$ were used: L012 cells $(3,1,1)$, $(8,5,3)$, $(10,7,4)$, $(12,10,5)$, $(14,12,6)$, $(15,11,6)$, $(17,13,7)$, $(19,16,8)$, $(22,17,9)$; L016 runB2 $(26,22,11)$; 483 classes in all.
  - Degree-1 histograms: $(8,5,3)$ $\{1{:}1,2{:}1\}$; $(12,10,5)$ $\{0{:}112,1{:}37\}$; $(15,11,6)$ $\{0{:}9,1{:}8,2{:}2\}$; $(19,16,8)$ $\{0{:}221,1{:}6\}$; $(22,17,9)$ $\{0{:}18,1{:}19\}$; $(26,22,11)$ $\{0{:}36\}$; the tight cells have at most one vertex of degree 1, except $E_1$ (three).
  - Result: **0 pendant b-configurations.**
- **E3 (judge's S3 re-run).** `bash run_s2_s3.sh` (second half), giving S3_rerun_output.txt, which is identical to S3_output.txt of the judge.
  - The stored slack-8 lists were used: $(5,2,1,3)$ (L014) and $(9,7,3)$ [empty], $(12,8,4)$, $(15,9,5)$, $(18,10,6)$, $(21,11,7)$ (L013, $\Delta\le2$), $(24,12,8)$ (L016 runA, $\Delta\le2$).
  - Result: **0 candidate triples $(A,B,C)$ of disjoint non-edge pairs of avoided vertices of degree $\le2$, and 0 hits.**
  - The PT-II configuration does not come near the stored slack-8 data: these classes have at most one avoided vertex (judge's diagnostic).
- **E4 (census of pairwise NC non-edge triples).** `bash run_census27.sh`, giving census27_output.txt (own code census27.py, exhaustive minimum-transversal enumeration).
  - It covers the same ten near-tight lists, with no degree restriction on the triple.
  - Result: **0 pairwise NC non-edge triples in every list** (the only pairwise NC triple of $E_1$ is its edge).
  - *Shows:* consistent with Theorem B (tight graphs have none; slack-1 graphs have only pendant ones), with Remark B.4/B.5, and with L025 C3 (census_near_output.txt).
- **Cited, not re-run:**
  - L025's checks C1-C3 and W1 (experiments/prover/L025/; 0 failures; 42 pairwise NC pendant triples on slack-7..9 classes, all with $s(G)\ge11$);
  - the judge's S1 (C10, 32 pieces of $L^*$, not needed here).

## Sanity checks
- **E5 (the triangle $(6,3,2)$, outside the hypotheses).** `python3 sanity27.py`, giving sanity27_output.txt. Take $T=\{034,135,245\}$, with $s(T)=2$.
  - $\{0,1,2\}$ is a pairwise NC pendant triple. Theorem B forbids this only at slack $\le1$, and here $s=2$.
  - The hub $T\oplus(0,1,2)$ is a $(10,7,4)$ member of $\mathcal C$ with $s=0=2-2$ (A1).
  - The fold $T\oplus^\circ(0,1\,|\,2)$ is an $(8,5,3)$ member with $s=1=2-1$ (A2).
  - $T-\{0,1,2\}$ is three isolated vertices with $s=9=2+13-6$ (A9).
  - The pairs $\{3,4\},\{3,5\},\{4,5\}$ intersect. Theorem P(c) forbids this at slack 1, and P(c)'s proof (bound $|\partial(X)|\le1$ at slack 1) does not apply at slack 2.
- **E6 ($A_{\rm base}$).** In sanity27_output.txt, the AP hypergraph of $A_{\rm base}$ is $(14,12,6)$, tight, in $\mathcal C$, with maximum degree 4 and 143 minimum transversals (the 143 maximum Sidon sets of START_HERE §6).
  - It has no NC pair at all, hence no pairwise NC non-edge triple. This is what Theorem B and Theorem B′ predict, since $(\mathrm H_{16})$ holds by L016 and neither theorem needs $\Delta\le3$.
  - C003 ($(65,63,28)$, slack 13) is outside the hypotheses.
- **E7 (Remark B.5 consistency).** By E2-E4, no stored near-tight graph with at most 26 vertices has a b-configuration. This agrees with the computational bound $n(H)\ge31$ for a pattern-(b) vertex and with L022 Corollary 3′.

## Falsifier report
No separate falsifier run for this consolidation. Every lemma of Part A and the identities behind J1 and the gadget form are tested in E1 on 3,000 random members of $\mathcal C$, and the hypothetical objects of Theorems P and D do not occur in the stored data (E2-E4). A falsifier for PT itself (SYNTHESIS.md Section 5, step 2) is the recommended next computation; it is not part of this certificate.
