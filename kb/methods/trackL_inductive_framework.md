# Track L: the avoidance/deletion induction behind Q8-type inequalities [derived-here]

Setting (omega issue #9804, kb/notes/omega_issue_9804.md). $A$ a (4,5)-set, $H=H(A)$ its AP
hypergraph, $D\subseteq A$ independent ("avoided": forced INTO the Sidon set), $R=A\setminus D$,
$K$ = clutter of inclusion-minimal traces $e\setminus D$ ($e\in E(H)$; sizes 1, 2, 3 counted by
$e_1,e_2,e_3$). An independent set $I\supseteq D$ of $H$ is the same as $D\cup J$ with $J\subseteq R$
containing no trace, so
$$\alpha(H;\supseteq D)=|D|+|R|-\tau(K).$$
A candidate inequality has the shape
$$a\,\tau(K)\le b\,|R|+c\,e_2+d\,e_1\qquad(\ast)$$
and with $D=\emptyset$ it reads $\tau(H)\le (b/a)\,n$, i.e. $h\ge(1-b/a)\,n$. Q8 is $(a,b,c,d)=(7,3,2,4)$:
with $D=\emptyset$ it is exactly $h\ge 4n/7$, so **Q8 is an inductive strengthening of the conjecture
$c_*=4/7$**. Henning–Yeo's constants correspond to $b/a=8/17$ (but HY uses $m$, not traces).

## The two moves and when they are free
Write $\Phi=b|R|+ce_2+de_1$. For $v\in R$ let $e_i(v)$ be the number of size-$i$ traces containing $v$.

**Deletion** ($A'=A\setminus\{v\}$, $D'=D$; $v$ goes into the transversal): $\tau(K)\le1+\tau(K')$ and
$\Phi'=\Phi-b-c\,e_2(v)-d\,e_1(v)$. The induction closes iff
$$a\le b+c\,e_2(v)+d\,e_1(v).$$

**Avoidance** ($D'=D\cup\{v\}$; legal iff $e_1(v)=0$): $\tau(K)\le\tau(K')$ (an independent set
containing $D\cup\{v\}$ contains $D$), the size-3 traces through $v$ become pairs and the pairs
through $v$ become singletons, so
$$\Phi'=\Phi-b+c\,e_3(v)+(d-c)\,e_2(v),$$
and the induction closes iff $c\,e_3(v)+(d-c)\,e_2(v)\le b$.

Hence in a **minimal counterexample** to $(\ast)$ every $v\in R$ satisfies
$$b+c\,e_2(v)+d\,e_1(v)<a\quad\text{and}\quad\bigl(e_1(v)\ge1\ \text{or}\ c\,e_3(v)+(d-c)\,e_2(v)>b\bigr).$$
For Q8: $e_1(v)=0$ for all $v$ (so $e_1=0$), $e_2(v)\le1$ (the pair graph is a matching) and
$2e_3(v)+2e_2(v)\ge4$, i.e. $e_3(v)+e_2(v)\ge2$. This reproduces omega's structural lemmas; their
extra claim $(d_2,d_3)\in\{(0,2),(1,1),(1,2)\}$ (so $e_3(v)\le2$) must come from a finer argument.

## Where realizability must enter
The pure-graph case ($e_3=0$) of $(\ast)$ follows from Turán for Q8's constants:
$\alpha(G)\ge v^2/(v+2e)\ge(4v-2e)/7$ always. The hard part is the 3-uniform part. An abstract
(linear, $F_7$-free, injective midpoints) version of $(\ast)$ with $b/a<8/17$ can only be true if the
class $O'$ is not HY-tight; the experiments/20261014-0500-slack-landscape data say how far from tight
it is. No proof below $8/17$ is known, and which hypotheses such a proof needs is open. On the abstract class $C$ (linear, $F_7$-free, hereditary sparsity $e(S)\le|S|-2$), $11\tau\le3n+2m$ (I11, $b/a=5/11$ at $m=n-2$) was proved for $n\le22$ by a window-cell induction that uses no forbidden core (not even K30, K31) and no harmonic structure (kb/notes/i11_conjecture.md, L007--L011; computer-assisted [verified-here], $n\le22$ only; I11 for all $n$ is [conjecture]). Hereditary sparsity cannot be dropped: a connected linear $F_7$-free $(9,8,4)$ graph has I11 slack $-1$. So forbidden cores and the exact harmonic structure of saturated sets are not known to be necessary for targets below $8/17$. The data show that they (more precisely, cores with $\ge5$ edges) are needed only for trace-based Q8-type targets of $(\ast)$ at Q8's weights $(c,d)=(2/7,4/7)\,a$ with $b/a<31/70$ (K38, K39, as next). Cores with at most 4 edges (K30, K31, K33 and the $\le4$-edge members of data/forbidden_ordered_n*.json) are not enough for Q8-type targets: Q8 itself ($b/a=3/7$) is false for the abstract class satisfying all of them, and every abstract violator found (89 hypergraphs of the $n=12$, $m=10$ census, all of tuple type $(\tau,|R|,e_2,e_1)=(5,10,2,0)$) contains a 5- or 6-edge core (K38, K39, D17) [verified-here]. Those larger cores are in the same files, data/forbidden_ordered_n7.json and n8.json. On that census the abstract class with $\le4$-edge cores forces only $b\ge31/70<8/17$ at Q8's $(c,d)$, so targets with $31/70\le b/a<8/17$ are not excluded by these data (K39) [heuristic: finite samples]. At Q8's constants, the dominant local type that is neither freely deletable nor avoidable is a vertex on three full traces, $(e_3,e_2,e_1)=(3,0,0)$, about 40% of the vertices of the irreducible states (40% for the abstract violators, 25 of 63 for the realizable ones, about 46% for the abstract slack-0 states; K39, experiments/20261014-0700-inductive-fit/README.md) [verified-here counts; heuristic as a statement about all sets].

## How to choose weaker targets
Any $(a,b,c,d)$ with $3/7<b/a<8/17$ and $d\ge a-b$ (singletons always deletable), tested first by the
falsifier on all data, is a legitimate intermediate target; the free-move conditions above tell which
local configurations survive in a minimal counterexample, and the discharging must kill those using
the forbidden cores.
