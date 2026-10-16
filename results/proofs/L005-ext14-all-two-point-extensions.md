# No 16-point (4,5)-set with h <= 9 contains a saturated extremal 14-point set
CLAIM-TYPE: certificate (exact computation with a case analysis, applied to a complete census)
TYPE: certificate
STATUS: submitted (2026-10-16 00:15 UTC)
DEPENDS ON: L004 [verified-here, ACCEPTED] (the 2,910 classes of data/census_n14_m12_classes.jsonl.gz are ALL saturated 14-point (4,5)-sets with h = 8 up to affine equivalence); L001 [verified-here, ACCEPTED] (the case analysis T0/T1/T2 for two-point extensions; this certificate applies it to every class); K3-K6 [published] (a (4,5)-set is weak Sidon, its Sidon subsets are its 3-AP-free subsets, midpoints are injective and never extreme). Not load-bearing: Lemma U1 of kb/notes/extension_lemmas.md [derived-here] predicts the outcome of case T2.

## Statement
Let $A$ be a 14-point (4,5)-set with $h(A)=8$ and $m(A)=12$ (every non-extreme point of $A$ is the midpoint of a 3-term AP in $A$; by L004 these are the 2,910 affine classes of the census). For every pair of distinct reals $x,y\notin A$ such that $B=A\cup\{x,y\}$ is a (4,5)-set, $h(B)=10$.
Consequently: no 16-point (4,5)-set with $h\le 9$ (a set beating $4/7$ at $n=16$, see START_HERE section 4) contains a saturated extremal 14-point subset; equivalently, in any 16-point record set every 14-point subset with $h=8$ has $m=11$ (the open case Q11). The statement says nothing about extensions by four or more points, and nothing about non-saturated 14-point sets with $h=8$.

## Proof
Every property involved (being a (4,5)-set, $h$, the AP hypergraph, $m$) is invariant under affine maps $x\mapsto qx+t$, and $A\mapsto A\cup\{x,y\}$ commutes with them, so it suffices to treat one integer representative of each of the 2,910 classes of L004. Fix a class $A$ (scaled by 4 so that all midpoints and endpoints of pairs below are integers). $h(B)\le h(A)+2=10$ trivially (K4: Sidon subsets of a (4,5)-set are its 3-AP-free subsets, and $B$ is a (4,5)-set by hypothesis). The content is $h(B)\ge 10$, shown by exhibiting a 3-AP-free 10-subset (or computing $\alpha$ exactly) in every case of the L001 analysis:

Let $P_x$ be the finite set of reals not in $A$ that form a 3-AP with two points of $A$ (midpoints $(a+b)/2$ and endpoints $2b-a$, $a\ne b\in A$). Any 3-AP of $B$ that is not a 3-AP of $A$ contains $x$ or $y$; if it contains exactly one of them, that point lies in $P_x$.
- Case T0 (neither $x$ nor $y$ in any new AP): $S\cup\{x,y\}$ is 3-AP-free for a maximum Sidon subset $S$ of $A$, so $h(B)=10$.
- Case T1 ($x\in P_x$ up to the symmetry $x\leftrightarrow y$; $A\cup\{x\}$ must be a (4,5)-set, 32 to 61 admissible $x$ per class, 141,153 in total). T1a ($y$ in no new AP): $h(B)=h(A\cup\{x\})+1$; computed exactly for all 141,153 single extensions: always 10 (i.e. $h(A\cup\{x\})=9$ for every admissible $x$). T1b ($y$ in a new AP): then $y$ forms an AP with two points of $A\cup\{x\}$, so $y$ ranges over the finite set of midpoints/endpoints of pairs of $A\cup\{x\}$; every candidate pair is tested exactly for the (4,5) property (every 4-subset containing $x$ or $y$); for each of the 4,970,208 (4,5) pairs a 3-AP-free 10-subset was found (checked to be Sidon), so $h(B)=10$.
- Case T2 ($x,y\notin P_x$ but some new AP exists; it must contain both $x$ and $y$, so it is $\{a,x,y\}$ with $a\in A$ in one of 3 roles): $(x,y)$ lies on one of $3\cdot14=42$ lines. At a generic point of such a line the AP hypergraph of $B$ is $H(A)$ plus the single edge $\{a,x,y\}$; its independence number was computed exactly for all $2{,}910\times42=122{,}220$ line hypergraphs: always 10. Non-generic points of a line either put $x$ or $y$ into $P_x$ (Case T1) or lie on a second line (a second edge containing both $x$ and $y$): the 498 pairwise intersection points per class were tested exactly; none of them gives a (4,5)-set in any class.
These cases are exhaustive, so $h(B)=10$ for every (4,5) two-point extension of every class. $\square$

Remark (theory agrees). Lemma U1 (kb/notes/extension_lemmas.md, falsifier-checked) shows by Henning–Yeo applied to $H(A)-a$ that no vertex of a $(14,12,\tau=6)$ hypergraph lies in every maximum independent set, which is exactly the condition for a T2 line to give $\alpha=9$; the sweep confirms: no class has such a vertex (the number of maximum Sidon subsets per class ranges from 137 to 150; for $A_{\rm base}$ it is 143 as in L001).

## Computer-verified steps
- experiments/20261015-2340-ext14-all/extend_all.py (exact integer/Fraction arithmetic; no randomness), run as `bash scripts/start_job.sh experiments/20261015-2340-ext14-all 4 python3 experiments/20261015-2340-ext14-all/extend_all.py data/census_n14_m12_classes.jsonl.gz experiments/20261015-2340-ext14-all 2`; 1,844 s wall clock with 2 processes (about 1.0 CPU-hour). Per-class rows: results.jsonl; summary and all rows: results.json; README.md.
- Acceptance check against the refereed L001 numbers: on $A_{\rm base}$ (`python3 extend_all.py x x 1 --abase-test`): $|P_x|=223$, 50 single (4,5) extensions, 1,743 (4,5) T1b pairs all with $h=10$, 42 T2 lines all with $\alpha=10$, 143 maximum Sidon subsets, exactly as in L001; the census class with index 2440 reproduces these numbers.
- Totals: 2,910 classes, all with $h(A)=8$ recomputed; 141,153 (4,5) single extensions; 4,970,208 (4,5) two-point extensions, histogram of $h$: $\{10: 4{,}970{,}208\}$ (plus 141,153 T1a values and 122,220 T2 line values, all 10); classes with $\min h\le9$: 0.
- Independent cross-check: (to be added by the referee round: a plain-integer brute force over a window on a sample of classes, as bruteforce_check.py did for L001).

## Sanity checks
- Every class has $h(A)=8$, $m=12$, 14 points (recomputed inside extend_all.py).
- The class containing $A_{\rm base}$ reproduces L001 exactly (above).
- Lemma U1 predicts T2 empty; observed T2 pre-check false for all 2,910 classes.

## Falsifier report
Not applicable (exhaustive case analysis per class); the L001 brute-force cross-check played that role for $A_{\rm base}$. Lemma U1 and the related lemmas were falsifier-tested (experiments/falsify/extension-lemmas/).
