# Structure of Gyárfás–Lehel-tight hypergraphs [derived-here; falsifier NONE-FOUND on ~80k flip instances, all records and 14,645 abstract (12,10) solutions: experiments/falsify/gl-tight-structure/report.md]

Setting. $H$ an ordered midpoint hypergraph on $V=\{0,\dots,n-1\}$ (each interior $j$ the midpoint of at
most one edge $(\ell(j),j,r(j))$ with $\ell(j)<j<r(j)$; linear). Saturated: every $j\in\{1,\dots,n-2\}$ is a
midpoint, so $m=n-2$. Even $n=2k$. GL-tight means $\tau(H)=k-1$, the maximum allowed by the
Gyárfás–Lehel argument (K35: this is the case for all record sets with even $n\le14$).

**The two trees.** $G_L$ has the edges $\{\ell(j),j\}$; orienting $\ell(j)\to j$ every vertex has in-degree
$\le1$ and arcs increase, so $G_L$ is a forest. Saturated: $G_L$ is a spanning tree of $\{0,\dots,n-2\}$ plus the
isolated vertex $n-1$. Symmetrically $G_R$ (edges $\{j,r(j)\}$) is a spanning tree of $\{1,\dots,n-1\}$ plus
the isolated vertex $0$. Any proper 2-colouring of a selection graph (one pair chosen per edge) that is
bipartite makes every edge bichromatic, so **each colour class is a transversal of $H$**.

**Lemma 1 (balance).** If $H$ is saturated and GL-tight then the unique 2-colouring of the $G_L$-tree on
$\{0,\dots,n-2\}$ ($2k-1$ vertices) has classes of sizes exactly $k-1$ and $k$; the same holds for the
$G_R$-tree on $\{1,\dots,n-1\}$.
*Proof.* The smaller class is a transversal, so it has size $\ge\tau=k-1$; the classes sum to $2k-1$.

**Lemma 2 (flip).** Let $H$ be saturated and GL-tight, $c$ the $G_L$-colouring with small class $C_0$
($|C_0|=k-1$) and large class $C_1$. For a midpoint $j$ let $T_j$ be the vertex set of the subtree of the
$G_L$-tree hanging from $j$ (all vertices whose $\ell$-ancestor chain passes through $j$, including $j$), and
$t_0,t_1$ the numbers of $C_0$- and $C_1$-vertices in $T_j$. Suppose $r(j)\ne n-1$ and $r(j)\notin T_j$.
Then replacing the pair $\{\ell(j),j\}$ by $\{j,r(j)\}$ gives again a spanning tree of $\{0,\dots,n-2\}$, whose
colouring agrees with $c$ off $T_j$ and either agrees on $T_j$ (if $c(r(j))=c(\ell(j))$) or is flipped on $T_j$
(if $c(r(j))\ne c(\ell(j))$). In the flipped case GL-tightness forces $t_1-t_0\in\{0,1\}$.
*Proof.* Removing $\{\ell(j),j\}$ separates $T_j$ from the rest; adding $\{j,r(j)\}$ with $r(j)$ in the rest
reconnects without a cycle. The new colouring is determined by $c'(j)=1-c(r(j))$ and propagates down $T_j$.
After a flip the new class sizes are $(k-1)-t_0+t_1$ and $k-t_1+t_0$; both must be $\ge k-1$ (Lemma 1 for the
new tree, which also yields transversals), giving $0\le t_1-t_0\le1$.

**Lemma 3 (robustness; realizable case).** If $A$ is a $2k$-point (4,5)-set with $h(A)=k+1$ and $f(2k-1)=k+1$
(true for $2k=16$ since $f(15)=9$), then every vertex lies in some minimum transversal of $H(A)$ (equivalently,
every point is avoided by some maximum Sidon subset). If moreover no $(2k-2)$-point subset of $A$ has
$h=k$ (for $2k=16$: $A$ contains no 14-point record), then every PAIR of vertices lies in a common minimum
transversal: $\tau(H-u-v)=k-3$ (since $\alpha(H-u-v)=k+1$ on $2k-2$ vertices) and a $(k-3)$-transversal of $H-u-v$ plus $\{u,v\}$ is a minimum transversal.
*Proof.* $h(A-v)\ge f(2k-1)=k+1=h(A)\ge h(A-v)$, so $\tau(H-v)=(2k-1)-(k+1)=k-2$; add $v$. For pairs, $h(A-u-v)=k+1$ gives $\tau(H-u-v)=k-3$; add $u,v$.

**Use.** Lemmas 1–3 are redundant for the SAT model but are strong implied constraints (Lemma 1 is the
`gl_constraints` option of e757/sat_indep.py, K37). Lemma 2 gives one constraint per midpoint; Lemma 3
gives one existential constraint per vertex pair. Outcome [heuristic]: Lemma 1 sped up UNSAT proofs at n = 12 by about 1.4x to 14x (one instance per size; only about 1.2x at n = 11; no solver finished n = 13 with or without it; K37). At n = 16 the vertex and pair constraints of Lemma 3 (the pair constraint in the relaxed form "independent 9-set avoiding both, or m(C-p-q) = 11", which relies on K45/K46) did not let CP-SAT decide m = 13 or m = 14: UNKNOWN after 3.5 h each, and that model does not contain the Gyárfás-Lehel colouring. CaDiCaL with the same constraints also TIMED OUT at 3.5 h on both instances, with the Gyárfás-Lehel colouring (Lemma 1) added at m = 14 only (D24; experiments/20261016-0850-n16-deletion-cpsat/README.md, experiments/20261016-1240-n16-cnf-witness/README.md). So f(16) remains undecided.

**Consequences and checks (added 2026-10-16).** (K44) Let $H$ be saturated and GL-tight on $n=2k$ vertices and, as for $H(A)$ with $A$ a (4,5)-set, also $F_7$-free (Henning-Yeo needs linear and $F_7$-free). For a vertex $v$, a transversal of $H-v$ together with $v$ is a transversal of $H$, so $\tau(H-v)\ge k-2$; and $H-v$ is linear and $F_7$-free with $2k-1$ vertices and $2k-2-\deg v$ edges. Henning-Yeo gives $17(k-2)\le 5(2k-1)+3(2k-2-\deg v)=16k-11-3\deg v$, i.e. $\deg v\le(23-k)/3$: at most 5 for $n\in\{12,14,16\}$ and at most 4 for $n\in\{18,20,22\}$ [derived-here; kb/known_results.md K44]. (K47) Lemma 1 is confirmed by exact computation, with class sizes $\{6,7\}$ for both the $G_L$ and $G_R$ trees, in all 2,910 saturated extremal 14-point classes [verified-here; experiments/20261016-0150-structure-2910/results.json, kb/known_results.md K47]. (K46) For $2k=16$ the extra hypothesis of Lemma 3's pair statement (no 14-point subset with $h=8$) can fail only through a non-saturated ($m=11$) extremal 14-point subset, because a 14-point subset with $h=8$ has $m\in\{11,12\}$ by Henning-Yeo and a 16-point record contains no saturated one, granting that the 2,910 classes of the L004 census (K45) are all the saturated extremal 14-point classes (census completeness was re-checked independently only by sampling plus whole-census consistency checks, not by a second full enumeration) [verified-here; certificate L005, kb/known_results.md K46; open case Q11].
