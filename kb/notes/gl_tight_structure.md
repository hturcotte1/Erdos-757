# Structure of Gyárfás–Lehel-tight hypergraphs [derived-here; to be falsified on data]

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
transversal: $\tau(H-u-v)=k-2$ and a $(k-2)$-transversal of $H-u-v$ plus $\{u,v\}$ is a minimum transversal.
*Proof.* $h(A-v)\ge f(2k-1)=k+1=h(A)\ge h(A-v)$, so $\tau(H-v)=k-2$; add $v$. Same for pairs.

**Use.** Lemmas 1–3 are redundant for the SAT model but are strong implied constraints (Lemma 1 is the
`gl_constraints` option of e757/sat_indep.py, K37). Lemma 2 gives one constraint per midpoint; Lemma 3
gives one existential constraint per vertex pair.
