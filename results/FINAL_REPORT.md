# Erdős Problem #757: final report of the autonomous run (2026-10-13 23:06 UTC to 2026-10-16 23:06 UTC)

Last updated: 2026-10-16 02:50 UTC (elapsed about 51.7 of 72 budget hours). Status of the goal clauses at this
update: (A) no new record set; (B) no new lower-bound proof; (C) budget not yet exhausted. The published bounds
$9/17\le c_*\le4/7$ (Ma–Tang 2026, via Henning–Yeo 2021 and the 14-point set $A_{\rm base}$) are unchanged.

## 1. Verified results (each with a referee-accepted certificate or an exact, re-verifiable computation)

Tags (CLAUDE.md integrity rule 6; they follow kb/known_results.md and results/LEDGER.md):
- R1 (K41, L002), R2 (K43, L003), R3 (K45, L004), R4 (K13, L001), R6 (K32, K33), R9 (the certificate L005, K46) and R10 (K47) are [verified-here].
- R7 (K35, K36) is [verified-here] as arithmetic and exact computation. The exact values f(n) it relies on use the published Henning–Yeo bound and are [derived-here] (K24).
- In R5, K30, K31 and K33 are [verified-here]. The degree bound K44 is [derived-here].
- In R8, K34 and K38 are [verified-here]; K34 is evidence on data, not a proof of Q8. K39 is [verified-here] for its exact optima on the stated data sets. Reading them as predictions, including the sentence on the dominant hard local type in any minimal counterexample, is [heuristic]. The free-move conditions of kb/methods/trackL_inductive_framework.md are [derived-here].
- In R9, the lemmas E, U, Δ of kb/notes/extension_lemmas.md are [derived-here] (falsifier HOLDS-ON-DATA on about 11,000 sets).
- In sections 2 and 3, these are [heuristic]: the hypotheses H1 and H2, "the evidence favours H2", "everything tried is consistent with a wall", "no certificate is reachable", and the interpretation of unfinished or failed searches (D15 to D22). The exact counts quoted there keep their own tags:
  - the drop from 54,243 to 2,910 classes, and the R9 bullet, are [verified-here];
  - the slack statistics on the 1,333,217-row dataset of experiments/20261014-0020-lp-fit are [verified-here] as counts on that dataset, while its fitted frontier is [heuristic];
  - the Gyárfás–Lehel structure lemmas (kb/notes/gl_tight_structure.md) are [derived-here].
- Section 4 is a status report. The partial D22 counts are [verified-here]. The projection that the (14,11) DFS will not finish in this run is [heuristic]. The recommended next steps make no claim.

**R1. Exact census of extremal 12-point sets (certificate L002, ACCEPT after three referee rounds, four independent
pipelines).** Up to affine equivalence there are exactly **54,243** twelve-point (4,5)-sets with $h=7=f(12)$. Every such
set has exactly 10 three-term APs and is affinely rigid. By-product: every linear, midpoint-injective, monotone pattern on
12 vertices with $\alpha\le7$ is saturated even when $F_7$ is allowed, and $\alpha\le6$ is impossible, so $f(12)\ge7$ holds
without Henning–Yeo. (kb/known_results.md K41; results/proofs/L002-census-12-point-extremal-sets.md.)

**R2. Exact counts for $n\le11$ (certificate L003, ACCEPT after three rounds, three independent enumerators).** The
numbers of affine classes of saturated ($m=n-2$) extremal sets are 1, 4, 66, 1,262, 6,644, 466,961 for $n=6,\dots,11$.
For every $4\le n\le11$ there are infinitely many extremal sets up to affine equivalence (non-saturated patterns give
positive-dimensional families; $n=4,5$: $\{0,1,2,x\}$, $\{0,1,2,x,3x\}$), one class each for $n\le3$, and $n=12$ is the
smallest $n\ge4$ with finitely many. (K43; results/proofs/L003-census-small-n-extremal-sets.md.)

**R3. Exact census of saturated extremal 14-point sets (certificate L004, ACCEPT).** Exactly **2,910** affine classes of
14-point (4,5)-sets with $h=8$ and $m=12$; $A_{\rm base}$ is one of them. Enumeration: 205,529 abstract patterns up to
reflection over $1.13\cdot10^{11}$ DFS nodes; the referee realized all 205,529 patterns independently without the
pipeline's pre-filters and reproduced the count; completeness was re-checked by sampling 28% of the prefixes plus
consistency checks (not by a full second enumeration). Whether non-saturated ($m=11$, Henning–Yeo slack 1) extremal
14-point sets exist is open: CP-SAT returned UNKNOWN after two hours and an exhaustive DFS is running (section 4).
(K45; results/proofs/L004-census-14-point-extremal-sets.md.)

The sequence of saturated extremal classes for $n=6,\dots,14$ is therefore
$1,\ 4,\ 66,\ 1262,\ 6644,\ 466961,\ 54243,\ ?,\ 2910$; it is not in the OEIS (novelty scan: results/reviews/L002-*__scout__*.md).

**R4. No 2-point extension of $A_{\rm base}$ reaches $h\le9$ (certificate L001, ACCEPT after four rounds, four independent
methods).** All 1,743 non-generic (4,5) extension pairs and all generic cases have $h=10$. This upgrades the community
fact K13; extensions by four or more points are not covered. (results/proofs/L001-abase-two-point-extensions.md.)

**R5. Structural lemmas with one-line proofs (K30, K31, K33, K44).** Monotone midpoints: for APs $(i,j,k)$,
$(i',j',k')$ in rank order with $i\le i'$, $k\le k'$, $(i,k)\ne(i',k')$, one has $j<j'$. No medial triangle: three APs
pairwise meeting in shared endpoints force a parallelogram, so they never occur; likewise the medial 4-cycle. Degree
bound: in a Gyárfás–Lehel-tight saturated hypergraph on $n=2k$ vertices every vertex has degree $\le(23-k)/3$. A
novelty scan of 2026-10-14 (OEIS, the erdosproblems forum thread, the omega issue, the repo digests; Ma–Tang and Gyárfás–Lehel were not re-read in full) found K30 and K31 absent; K33 and K44 were not scanned.

**R6. Forbidden-configuration library (K32, K33; independently recomputed by a referee subagent without e757, every verdict matched; no results/reviews file, hence no formal ACCEPT).** All ordered midpoint patterns on
$\le8$ vertices classified exactly (46,281 at $n=8$: 16,568 realizable, 28,697 order-infeasible, 498 force an extra AP,
518 force a repeated difference); 287 minimal forbidden cores with $\le6$ edges (data/forbidden_ordered_n7.json,
data/forbidden_ordered_n8.json); catalogue of every $\le4$-edge configuration with every midpoint labeling
(experiments/20261014-0005-forbidden-n8). The Pasch configuration is realizable in exactly one labeling.

**R7. Where the trivial bound is tight (K35, K36).** $f(n)=\lceil n/2\rceil+1$ for $6\le n\le15$ and $n=17$, which equals the
Henning–Yeo bound for every $6\le n\le23$; the Gyárfás–Lehel bound $h\ge\lceil(n+1)/2\rceil$ is already tight at every even
$n\le14$. Hence no lower-bound improvement is possible below $n=16$, and in the abstract class the saturated extremal value
is $\tau=n/2-1$ at every even $n\le14$, equal to the realizable value in every resolved cell.

**R8. The community's candidate inequality Q8 (K34, K38, K39).** $7\tau(K)\le3|R|+2e_2+4e_1$ holds on every
deletion/avoidance state of all record sets (A_base: 3,253,568 states) and on about 570M sampled states, with two
independent implementations agreeing; with no avoided points it reads $h\ge4n/7$, i.e. it is an inductive strengthening of
the conjecture $c_*=4/7$. It is **false for the abstract class**: a 12-vertex pattern that is linear, $F_7$-free, monotone,
medial-free and clean of all $\le4$-edge cores violates it by one; every abstract violator contains a 5- or 6-edge
forbidden core. On realizable data the best inductive constant is exactly $3/7$; on abstract data it is $31/70$. The
dominant hard local type in any minimal counterexample is a vertex on three full traces. kb/methods/trackL_inductive_framework.md
gives the exact free-move conditions for every $(a,b,c,d)$.

**R9. No 16-point record contains a saturated extremal 14-point set (certificate L005, ACCEPTED by two fresh referees at 01:37 UTC after a text-only NEEDS-WORK round; novelty CLEAR).**
The refereed L001 case analysis (two-point extensions of $A_{\rm base}$) was applied to all 2,910 saturated extremal 14-point
classes of R3 (L004): 141,153 (4,5) single extensions, 4,970,208 enumerated (4,5) two-point extensions (the finite case T1b; the cases T0, T1a, T2 contain continua and are decided by the case analysis), $122{,}220$ generic one-edge lines,
all with $h=10$; no class has a point lying in every maximum Sidon subset (137 to 150 such subsets per class). Hence every
14-point subset with $h=8$ of a hypothetical 16-point set with $h=9$ is non-saturated ($m=11$, the open case Q11). This inherits the completeness of the L004 census (R3), which the referee re-checked independently only by sampling (28% of the prefixes) plus consistency checks, not by a second full enumeration.
Evidence: experiments/20261015-2340-ext14-all/ (README, results.json), results/proofs/L005-ext14-all-two-point-extensions.md.
Supporting theory [derived-here, falsifier-checked on about 11,000 sets]: kb/notes/extension_lemmas.md. Lemma E: adding
$a\pm t$ (generic $t$) at an extreme point $a$, or $x$ and $2x-a$ at any point $a$, gives a (4,5)-set with $h+1$ exactly when $a$
lies in every maximum Sidon subset (then $D$ drops by 1); Lemma U: such a vertex forces Henning–Yeo slack $\ge5+3\deg a$, so
record-type sets have none; Lemma Δ: in a 16-point record every 15-point subset is extremal, no vertex is universal and
$\deg p\le m-9$, and a two-point extension of a saturated extremal 14-set can be a record only with exactly two new APs.

**R10. Structure of the 2,910 saturated extremal 14-point classes (K47).** AP degrees are 2, 3 or 4 only (never 5, though
K44 allows it), in three degree sequences ($3^82^6$: 700 classes; $4\,3^62^7$, the $A_{\rm base}$ type: 1,270; $4^23^42^8$: 940);
137 to 150 maximum Sidon subsets per class; no class is mirror-symmetric and no two are mirror images; **no class contains an
extremal 12-point subset** (all 91 two-point deletions keep $h=8$), so the 14-point extremal sets are not two-point extensions
of 12-point extremal sets, just as (R9) 16-point records cannot be two-point extensions of saturated 14-point extremal sets;
the Gyárfás–Lehel tree colourings have classes of sizes 6 and 7 in every class (Lemma 1 of kb/notes/gl_tight_structure.md);
no universal vertex (Lemma U1). Evidence: experiments/20261016-0150-structure-2910/ (12.9 s), tests/test_structure_2910.py.

## 2. The open case $n=16$ (negative results, D15, D16, L005)

Beating $4/7$ first becomes possible at $n=16$ ($h=9$, $m\in\{13,14\}$). Everything tried is consistent with a wall there:
- the abstract class has no $\alpha\le9$ member that any method could find at $n=16$ (CP-SAT, glucose, cadical, annealing over
  about 4 million maps with 28,589 genuine (4,5)-sets reached, constrained runs with all census invariants), while
  $n\le14$ witnesses are found in seconds and the realizable fraction of the filtered abstract extremal patterns (class O', K31 and cores with at most 4 edges) falls from 13.7% at $n=12$ (54,243 of 395,039) to 6.3% at $n=14$ (2,910 of 46,419);
- no witness at $n=18,20,22$ (3600 s each) and $n=23,25$ (1200 s per $m$ value) in realizability-CEGAR searches, all UNKNOWN; at $n=15$ no class-O' pattern with $\alpha\le9$ and $m'\in\{9,10\}$ was found in 2 h (no UNSAT proof either), and the census invariants (max degree $\le4$, balanced colour classes, no reflection symmetry hold for all 395,039 filtered $(12,10)$ patterns and for the 157 partial $(14,12)$ realizable patterns) do not make $n=16$ tractable;
- the number of saturated extremal classes drops from 54,243 ($n=12$) to 2,910 ($n=14$);
- none of the 2,910 saturated extremal 14-point sets extends by two points to a 16-point set with $h\le9$ (R9, L005): a 16-point record would have to be built on non-saturated 14-point extremal subsets (if any exist, Q11) or contain no extremal 14-point subset at all.
No certificate is reachable: every n=16 sub-instance exceeds the solver limits, the exact DFS needs about $10^{14}$ nodes,
and SAT UNSAT times grow from 2 s ($n=12$) to over 250 s ($n=13$). Two hypotheses remain: (H1) Henning–Yeo stays tight at
even $n$ up to 22 (records at 16..22, $c_*\le6/11$); (H2) a wall at 16 ($f(16)=10$, consistent with $c_*=4/7$ and Q8). The
evidence favours H2.

## 3. Lower-bound track: why no proof was attempted

Any improvement of $9/17$ must come from asymptotics (R7). The one candidate structure, a Q8-type inductive inequality,
provably needs forbidden configurations with $\ge5$ edges (R8), and no discharge argument for the dominant local type was
found; the Henning–Yeo 2021 paper (closed access, no preprint) was not obtainable, so its tightness structure is unknown.
The ingredients are recorded for a future attempt: the free-move framework, the forbidden-core library, the GL-tight
structure lemmas (kb/notes/gl_tight_structure.md; falsifier NONE-FOUND on about 80,000 instances), and the role statistics
of near-tight configurations (experiments/20261014-0020-lp-fit: over 1,333,217 realizable AP hypergraphs the Henning–Yeo slack is never negative and is at least 3 for $n\ge10$; the exact frontier $\tau\le(33/119)n+(3/17)m$ holds on all rows and no row has $D/n<5/7$; experiments/20261014-0700-inductive-fit).

## 4. Running at the time of writing and how to continue

- Exhaustive DFS at $(14,11,\alpha\le8)$ (experiments/20261014-1005-census-dfs/n14m11dfs; resumable; relaunch with
  `python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 10 --tag n14_m11`,
  3,437 depth-3 prefixes; 0 patterns in every finished prefix (all `*.jsonl.gz` empty). Count of `.done` markers: 130 when stopped at
  2026-10-16 01:18 UTC, 139 at 02:03 UTC, 150 at the relaunch of 02:26 UTC after the seventh container restart (journal/LOG.md,
  2026-10-16T02:26Z), 161 at 02:50 UTC; running on 4 workers. Measured rate about 22 to 36 prefixes/h (journal/LOG.md 2026-10-16T02:02Z;
  `.done` timestamps), so the remaining prefixes need roughly 90 to 150 hours of wall time and it cannot finish before the budget
  ends at 2026-10-16 23:06 UTC; refresh these counts at the final checkpoint). Completion decides whether 2,910 is the total number of extremal 14-point
  classes and, with R9, whether any 16-point record can contain an extremal 14-point subset at all.
- The saturated census at $n=13$ was started and stopped as infeasible (D22, Q12): 8 of 1,811 prefixes already hold
  54,717,717 abstract patterns (Henning–Yeo slack 13 at $(13,11,5)$); a realizability-aware enumerator is needed.
- Recommended next steps: (i) a dedicated exact engine for $n=16$ (SAT with symbolic symmetry breaking and the
  deletion-lemma case structure of Lemma Δ, or a distributed DFS of about $10^{14}$ nodes); (ii) if $f(16)=10$ is confirmed, the
  abstract wall is combinatorial and the Q8-type induction with 5/6-edge cores is the natural proof program;
  (iii) obtain Henning–Yeo 2021 for its equality cases (Lemma U shows how the equality structure constrains universal
  vertices); (iv) submit the census sequence to the OEIS; (v) four-point extensions of the 2,910 classes (an 18-point set
  with $h=10$ would be a record) and two-point extensions of any $(14,11)$ classes found.
- Repository state: all work of this run is on branch claude/intelligent-pasteur-22z06m (remote origin). PR #1 (to main, opened 2026-10-15 23:07 UTC) was still open and unmerged at the time of writing; it is to be merged at about 21:00 UTC on 2026-10-16, after the final checkpoint and before the budget ends at 2026-10-16 23:06 UTC (update this line after the merge).

## 5. Infrastructure built (e757/, all tested)
Exact realizability oracle with Farkas certificates (realizability.py); CP-SAT model of the ordered-midpoint class
(cpsat_model.py, with monotone/medial/core constraints and a realizability-CEGAR); independent python-sat encoding
(sat_indep.py, with Gyárfás–Lehel colouring constraints); exact C DFS with resumable prefix split (c/ordered_dfs.c,
ordered_dfs_split.py); midpoint-map annealer (anneal.py). The frozen judge (judge/judge.py) was used for every spot check.

## 6. Dead ends added (kb/dead_ends.md D15 to D22)
Direct SAT/CP-SAT at $n=16$ (with or without structure, with or without census invariants); annealing at $n=16$ and $18$;
Q8 for the abstract class (D17); witness sweeps $n=18..25$ (D18); the layered $15\to16$ search (D19); D20, D21 (solver variants);
the pattern-first saturated census at $n=13$ (D22).
