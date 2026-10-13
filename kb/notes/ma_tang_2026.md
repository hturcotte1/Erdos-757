# Ma–Tang, *Largest Sidon subsets in weak Sidon sets*, arXiv:2602.23282v2 (6 Mar 2026) [published]

Digest made from the full arXiv text. Section numbers follow the paper.

## Results
- **Thm 1.3:** for weak Sidon sets, $g(n)=\lceil (n+1)/2\rceil$ for every $n$, so $\gamma_*=1/2$.
  This solves Sárközy–Sós Problem 12.
- **Thm 1.5:** $c_*=\lim f(n)/n=\inf_n f(n)/n$.
- **Thm 1.6:** $9/17\le c_*\le 4/7$.
- **AI declaration:** an AI assistant (ChatGPT-5.2 Pro, per the forum comment) found a 12-point
  example (giving 7/12) and, after refinement, $A_{\rm base}$. It also drafted the verification
  code. All other proofs are by the authors.

## Lemma chain (with exact hypotheses)
- **Prop 2.1:** Sidon ⇒ (4,5).
- **Prop 2.2:** (4,5) ⇒ weak Sidon. From $a_1+a_4=a_2+a_3$ (sorted) we get two equal-distance
  pairs, so at most 4 distances.
- Both inclusions are strict: $\{1,2,3,5\}$ is weak Sidon but not (4,5); $\{1,2,3,6\}$ is (4,5)
  but not Sidon.
- **Lemma 2.3 (weak Sidon $A$):** $S\subseteq A$ is Sidon ⟺ $S$ is 3-AP-free. A non-Sidon relation
  $u+v=x+y$ cannot use 4 distinct points (weak Sidon) or 2 distinct points, so it is $a+c=2b$.
- **Lemma 2.4 (weak Sidon):** the midpoint map $\mu$ is injective. Two APs with midpoint $x$ give
  $(x-d_1)+(x+d_1)=(x-d_2)+(x+d_2)$, four distinct points. Also $\mu$ never hits $\min A$ or
  $\max A$, so $m\le n-2$.
- **Lemma 2.5 ((4,5)):** $H(A)$ is linear. Two APs sharing $u<v$ have third points among
  $u-d$, $(u+v)/2$, $v+d$ with $d=v-u$; every pair of choices leaves at most 4 distances (the two
  outer ones give a 4-AP).
  - This fails for weak Sidon sets: in $\{1,2,3,5\}$ the APs $\{1,2,3\}$ and $\{1,3,5\}$ share 2
    points.
- **Lemma 5.2 (Gyárfás–Lehel Prop 2.6):** $H(A)$ is $F_7$-free, $F_7=\{012,034,056,135,246\}$.
- **Thm 5.3 (Henning–Yeo [6] Thm 7):** for 3-uniform, linear, $F_7$-free $H$:
  $17\tau\le 5n+3m$.
- **Thm 4.6 (Chvátal–McDiarmid; Tuza):** for every 3-uniform $H$: $4\tau\le n+m$.

## Proof of 9/17 (complete)
$h=\alpha=n-\tau$ and $17\tau\le5n+3m\le 5n+3(n-2)$, so $\tau\le 8n/17$ and $h\ge 9n/17$.
The argument uses $m\le n-2$ only once, globally.

## Subadditivity (Lemmas 3.5–3.6; Prop 3.7)
- Normalize $\min A=\min B=0$. Choose $q>0$ outside $\mathcal R=\{(a-a')/(b-b')\}$, and $t$ with
  $t-D_A>\max(D_A,qD_B)$.
- Then every mixed difference exceeds every within-block difference, and mixed differences are
  pairwise distinct (because $q\notin\mathcal R$).
- A 4-set meeting both blocks has:
  - with 1 or 3 points in $A$: 3 distinct mixed differences plus at least 2 within-block ones;
  - with 2 points in $A$: 4 distinct mixed differences plus at least 1 within-block one.

  Either way at least 5 distances.
- $h(C)\le h(A)+h(B)$, so $f$ is subadditive and Fekete applies.
- **Use:** any finite record set immediately bounds $c_*$.

## Weak Sidon extremal construction (Thm 4.5)
- $X_i=2^{n-i}3^i$ ($0\le i\le n-1$), $Y_i=2^{n-i+1}3^i$ ($0\le i\le n$), on $2n+1$ points.
- It is weak Sidon, via a 3-adic valuation argument (Lemmas 4.1–4.2).
- Its APs are exactly $\{X_i,X_{i+1},Y_i\}$ and $\{X_i,Y_i,Y_{i+1}\}$: $2n-1=n_H-2$ edges, so it is
  midpoint-saturated.
- $\alpha=n+1$. The proof splits $U=\{i:X_i\in T\}$ into maximal runs of consecutive indices.
  A run of length $\ell$ forces $\ell$ absent $Y$'s, and different runs force disjoint sets of
  absent $Y$'s. **Reusable "runs force exclusions" charging pattern.**
- It is not (4,5): consecutive edges share 2 points.

## Verification
- $A_{\rm base}=\{0,136,200,243,246,249,272,286,298,323,400,528,596,1056\}$.
- A witness Sidon 8-set: $\{0,136,200,243,246,298,323,528\}$.
- Code: kb/literature/sources/ma_tang_verify_base_block.py.

## What the paper does NOT do (openings)
- It uses no arithmetic beyond linearity, $F_7$-freeness and $m\le n-2$ in the lower bound.
- It never uses hereditary sparsity ($e(S)\le|S|-2$ for every $S$).
- It does not discuss which hypergraphs are realizable, or Henning–Yeo's equality cases.
- It gives no structural explanation of $A_{\rm base}$.
