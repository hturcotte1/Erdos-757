# No 2-point (4,5) extension of A_base has a largest Sidon subset of size 9
CLAIM-TYPE: certificate (exact computation with a case analysis)
TYPE: certificate
STATUS: ACCEPTED by referee round 4 (results/reviews/L001-abase-two-point-extensions__referee__20261014T095734Z.md); revised after rounds 1-3: wording, witnesses.json, independent brute force with exact keys, K3 hypothesis made explicit; after the ACCEPT only the title was changed, adding the (4,5) qualifier per the round-4 editorial Note 1
DEPENDS ON: K11 [published] (A_base is a (4,5)-set with h=8); K3 [published] ((4,5) ⊂ weak Sidon, so K4 applies to B); K4 [published] (for weak Sidon sets h = alpha of the AP hypergraph). K5-K6 [published] (midpoint injectivity, linearity) are explanatory only.

## Statement
Let $A=A_{\rm base}=\{0,136,200,243,246,249,272,286,298,323,400,528,596,1056\}$. For every pair of distinct reals
$x,y\notin A$ such that $B=A\cup\{x,y\}$ is a (4,5)-set, $h(B)=10$. In particular no 16-point (4,5)-set
containing $A_{\rm base}$ has $h\le 9$ (and, deleting a point, no 17-point one has $h\le 9$ either). The statement says
nothing about extensions by four or more points: an 18-point (4,5)-set containing $A_{\rm base}$ with $h=10$ would
still be a record (ratio $5/9<4/7$) and is NOT excluded here.
(This upgrades K13 [community] to [verified-here]; the omega thread stated it with a ten-witness certificate.)

## Proof (case analysis; every case decided by exact rational arithmetic)
$h(B)\le h(A)+2=10$ trivially, so the content is $h(B)\ge10$. A 3-AP-free subset of $B$ of size 10 is exhibited or constructed in every case (B is a (4,5)-set, hence weak Sidon by K3, so its 3-AP-free subsets are Sidon by K4).
Let $P_x$ be the finite set of reals not in $A$ that form a 3-AP with two points of $A$ (midpoints $(a+b)/2$ and endpoints $2b-a$, $a\ne b\in A$, minus $A$).
Case T0: neither $x$ nor $y$ lies in any 3-AP of $B$. Then $S\cup\{x,y\}$ is 3-AP-free for a maximum Sidon subset $S$ of $A$: $h=10$.
Case T1: $x\in P_x$ (by symmetry; $|P_x|=223$; exactly 50 values give a (4,5)-set $A\cup\{x\}$). Sub-case T1a: $y$ in no 3-AP of $A\cup\{x,y\}$: $h(B)=h(A\cup\{x\})+1=10$ (computed exactly for all 50 $x$). Sub-case T1b: $y$ in some 3-AP of $A\cup\{x,y\}$: $y$ ranges over a finite exact set; 11,774 candidate pairs, 1,743 of them (4,5)-sets, every one has $\alpha=10$; an explicit 3-AP-free 10-subset is recomputed for each of them by extend.py and stored in witnesses.json (added after the first referee round).
Case T2: $x,y\notin P_x$ but $\{a,x,y\}$ is a 3-AP for some $a\in A$ (3 roles). For each of the 42 lines $y=\lambda x+\mu$: at a generic point of the line the AP hypergraph of $B$ is the 12 APs of $A$ plus the one new AP, and its independence number is 10 (computed exactly on the labeled 16-vertex hypergraph); the 498 exceptional points (where two such lines meet) are all decided exactly and none is a (4,5)-set.
These cases are exhaustive: either some new AP exists (then it involves $x$ or $y$ with two points of $A$, Case T1, or exactly $\{a,x,y\}$, Case T2) or none does (Case T0).

## Computer-verified steps
experiments/20261014-0640-abase-extensions/extend.py (exact Fractions; results.json), tests/test_abase_extensions.py (re-checks 50 stored extensions: (4,5) and h=10).
Independent cross-check: bruteforce_check.py (plain integers, no e757 or extend.py imports) over all half-integer pairs in [-300, 1699.5]: 5,185,660 (4,5) pairs, every one with a verified 3-AP-free 10-subset (0 failures), including all 15,800 line-generic pairs; the 766 non-line-generic pairs (both points in 3-APs with points of $A$, not merely on a common line $\{a,x,y\}$) are all contained in results.json, with exact rational keys; h(A_base)=8 re-checked exhaustively (the whole script runs in about 5.5 minutes). The first referee round (results/reviews/L001-abase-two-point-extensions__referee__20261014T080455Z.md) re-derived all counts with three implementations sharing no code with e757 (formula enumeration, CP-SAT on equal distances, a grid scan) and computed h = 10 directly for all 6,876 (4,5) pairs with both points in 3-APs in the earlier window of half-integers in [-60,1120] (589 non-line-generic, 6,287 line-generic).

## Sanity checks
h(A_base)=8 (judge); the stored 1,743 (4,5)-sets all have 16 points, ratio 10/16 = 5/8 as in K13.

## Falsifier report
Not applicable (exhaustive case analysis); the brute-force check above plays that role.
