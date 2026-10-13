# the-omega-institute/trureturing issue #9804 (opened 24 Sep 2026) [community]

Snapshot digest of an unrefereed thread produced by Codex CLI workers with host-side exact checks.
It claims no solution. The data are exact and reproducible.

## Setting
- $D\subseteq A$ independent (the "avoided" points), $R=A\setminus D$.
- $K$ is the clutter of inclusion-minimal nonempty AP traces $e\setminus D$ (isolated active
  vertices kept). $e_1,e_2,e_3$ count the traces of size 1, 2, 3.

## Refuted: $21\tau(K)\le 9|R|+5e_2+12e_1$ [refuted]
- **Counterexample 1:** $A=\{0,178,198,218,227,235,272,276,287,317,356,436\}$, $D=\{287\}$.
  - APs: $E_1=\{0,178,356\}$, $E_2=\{0,218,436\}$, $E_3=\{178,198,218\}$, $E_4=\{178,227,276\}$,
    $E_5=\{198,235,272\}$, $E_6=\{198,317,436\}$, $E_7=\{218,287,356\}$, $E_8=\{227,272,317\}$,
    $E_9=\{235,276,317\}$, $E_{10}=\{276,356,436\}$.
  - Repeated differences: 20, 37, 41, 45, 49, 69, 80, 119, 178, 218, each exactly twice, as the
    consecutive gaps of one AP. The other 46 differences occur once.
  - Trace clutter: the 9 triples $E_i$ ($i\ne7$) plus the pair $\{218,356\}$. So $|R|=11$, $e_2=1$,
    $\tau(K)=5$ (witness $\{0,178,198,317,356\}$), and $105>104$.
  - A Sidon 7-subset: $\{218,227,235,272,276,287,436\}$.
- **Counterexample 2:** $\{-336,-168,-44,-24,-4,0,39,44,49,80,102,160\}$, $D=\{-336\}$.
  - Same incidence pattern, but not affinely equivalent [verified-here].
  - Avoiding 80 gives a "mixed equality child": 10 active vertices, 3 pairs, 7 triples, $\tau=5$.

## Amalgams (refute a constant cost per avoided point)
- $B=\{0,168,292,312,332,336,375,380,385,416,438,496\}$ (counterexample 2 translated).
- $A_k=\bigcup_{j<k}4096^jB$, glued at 0; since $4096>4\cdot496$, relations split by scale.
- $\tau(H(A_k))=4k+1$ and $\alpha=7k$. The deficit grows like $k$ with $|D|=1$.
- $A_2$ (23 points) was checked on all 8,855 quadruples.

## Valid reduction
- If every proper induced subhypergraph has $\alpha\ge c\cdot$order ($0<c<1$), a minimal
  counterexample has no cut vertex in its primal graph (one-vertex amalgam argument).

## Open candidate: $7\tau(K)\le 3|R|+2e_2+4e_1$
- It is tight on the amalgam traces.
- No violation was found over all deletion/avoidance states of both 12-point sets. That is one
  isomorphism class of evidence.
- In a minimal counterexample:
  - the pair graph is a matching;
  - the local types are $(d_2,d_3)\in\{(0,2),(1,1),(1,2)\}$.

## Extension certificate for $A_{\rm base}$
- For any two distinct reals $x,y$ with $A_{\rm base}\cup\{x,y\}$ a (4,5)-set, $h=10$ exactly.
- Covered: 124 compatible triples, 6,484 pairs, 6,609 extensions.
- Ten-witness certificate: every extension has an independent 10-set containing both new points.
- Also: all $3^{14}=4{,}782{,}969$ deletion/avoidance states of $A_{\rm base}$ were checked
  (3,253,568 valid; 99,153 equality states; no violations of the tested inequality).

## Other retained claims (unverified here)
- Private-blocker inequality: $t-s+\sum_x\binom{d_G(x)}2\le i-2$.
- An arithmetic degree bound $\Delta(G)\le6$ under maximum-independent-set hypotheses.
- Automatic one-for-two exchanges are blocked by a real 10-point example.
- Whole midpoint-depth layers and the shortest multiplicative recurrence recover only known bounds.
