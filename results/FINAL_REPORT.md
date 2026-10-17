# Erdős Problem #757: final report of the autonomous run (2026-10-13 23:06 UTC to 2026-10-16 23:06 UTC)

Last updated: 2026-10-17 08:37 UTC (48-hour extension granted by the user after the 72-hour budget; the extension results are R13 and the certificates L007 to L010; main holds the state of 2026-10-16 22:15 UTC until the next merge). Status of the goal clauses: (A) no new record set; (B) no new
lower-bound proof; (C) the budget ends at 23:06 UTC with this report in place. The published bounds
$9/17\le c_*\le4/7$ (Ma–Tang 2026, via Henning–Yeo 2021 and the 14-point set $A_{\rm base}$) are unchanged.

## 1. Verified results (each with a referee-accepted certificate or an exact, re-verifiable computation)

Tags (CLAUDE.md integrity rule 6; they follow kb/known_results.md and results/LEDGER.md):
- R1 (K41, L002), R2 (K43, L003), R3 (K45, L004), R4 (K13, L001), R6 (K32, K33), R9 (the certificate L005, K46), R10 (K47), R11 (L006, K48) and R12 (K49, exact counts) are [verified-here]; the trend read into R12 is [heuristic].
- R7 (K35, K36) is [verified-here] as arithmetic and exact computation. The exact values f(n) it relies on use the published Henning–Yeo bound and are [derived-here] (K24).
- In R5, K30, K31 and K33 are [verified-here]. The degree bound K44 is [derived-here].
- In R8, K34 and K38 are [verified-here]; K34 is evidence on data, not a proof of Q8. K39 is [verified-here] for its exact optima on the stated data sets. Reading them as predictions, including the sentence on the dominant hard local type in any minimal counterexample, is [heuristic]. The free-move conditions of kb/methods/trackL_inductive_framework.md are [derived-here].
- In R9, the lemmas E, U, Δ and Δ′ of kb/notes/extension_lemmas.md are [derived-here] (falsifier HOLDS-ON-DATA on about 11,000 sets, and Δ′ on all stored censuses).
- In sections 2 and 3, these are [heuristic]: the hypotheses H1 and H2, "the evidence favours H2", "everything tried is consistent with a wall", "no certificate is reachable", and the interpretation of unfinished or failed searches (D15 to D24). The exact counts quoted there keep their own tags:
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
$1,\ 4,\ 66,\ 1262,\ 6644,\ 466961,\ 54243,\ ?,\ 2910$; its OEIS status is not established: on 2026-10-14 the prefix 1, 4, 66, 1262, 6644 (n=6 to 10) matched no OEIS entry, and the single term 54243 matched only unrelated sequences (8 incidental hits, none about Sidon or difference sets); the terms 466961 and 2910 and any longer prefix were not searched, the 2,910 count (2026-10-15) postdates that scan, and the full sequence cannot be searched while the n=13 term is unknown (results/reviews/L002-census-12-point-extremal-sets__scout__20261014T171802Z.md).

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
medial-free and clean of all $\le4$-edge cores violates it by one; every one of the 89 abstract violators found among the first 26,974 members of the (12,10,$\alpha\le7$) census snapshot (K38, K39) contains a 5- or 6-edge
forbidden core. On realizable data the best inductive constant is exactly $3/7$; on abstract data it is $31/70$. The
most frequent hard local type (about 40% of the hard vertices) among the local types that are neither freely deletable nor avoidable, in the abstract Q8 violators (910 vertices in 91 states) and in the realizable irreducible tight states (63 vertices in 6 states) alike, is a vertex on three full traces (K39) [heuristic]. kb/methods/trackL_inductive_framework.md
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
$\deg p\le m-9$, and a two-point extension of a saturated extremal 14-set can be a record only with exactly two new APs. Lemma Δ′ (deletion version of Henning–Yeo; [derived-here], checked with 0 violations on the stored censuses at $n=8,9,10,12,14$, not part of the 11,000-set sample above; experiments/falsify/deletion-lemma/): if deleting $p,q$ from an $n$-point extremal set leaves an extremal $(n-2)$-point set, then $\deg p+\deg q-\varepsilon\le m-(17\tau-5n-7)/3$, with $\varepsilon=1$ if $p,q$ share an AP. At $(n,m,\tau)=(14,12,6)$ the bound is $11/3$, so (all degrees being at least 2 by K47) only two adjacent degree-2 vertices could be deleted, and K47 shows that none works; at $(12,10,5)$ the bound is 4, which allows any two degree-2 vertices (consistent with R12); and in a 16-point record ($\tau=7$) an extremal 14-point subset needs $\deg p+\deg q-\varepsilon\le3$ ($m=14$) or $\le2$ ($m=13$).

**R10. Structure of the 2,910 saturated extremal 14-point classes (K47).** AP degrees are 2, 3 or 4 only (never 5, though
K44 allows it), in three degree sequences ($3^82^6$: 700 classes; $4\,3^62^7$, the $A_{\rm base}$ type: 1,270; $4^23^42^8$: 940);
137 to 150 maximum Sidon subsets per class; no class is mirror-symmetric and no two are mirror images; **no class contains an
extremal 12-point subset** (all 91 two-point deletions keep $h=8$), so the 2,910 saturated 14-point extremal sets (and, by R11, every extremal 14-point set, saturated or not) are not two-point extensions
of 12-point extremal sets, just as (R9) 16-point records cannot be two-point extensions of saturated 14-point extremal sets;
the Gyárfás–Lehel tree colourings have classes of sizes 6 and 7 in every class (Lemma 1 of kb/notes/gl_tight_structure.md);
no universal vertex (Lemma U1). Evidence: experiments/20261016-0150-structure-2910/ (12.9 s), tests/test_structure_2910.py.

**R11. No extremal 14-point set contains an extremal 12-point set (certificate L006, ACCEPTED by two fresh referees at 08:31 UTC after a text-only NEEDS-WORK round; novelty CLEAR).** The L001/L005 two-point-extension analysis applied to all 54,243 extremal 12-point classes (R1, L002): 1,887,566 (4,5) single extensions (all $h=8$), 51,264,727 (4,5) two-point extensions with both new points in new APs (all $h=9$), 1,952,748 one-edge lines (all $\alpha=9$); referee round 3 confirmed the whole census independently with a Sidon-definition-only method. Hence every 12-point subset of every extremal 14-point set has $h=8$, and a non-saturated $(14,11)$ extremal set, if one exists (Q11), contains no extremal 12-point subset. Together with R9 and R10: no extremal 14-point set is a two-point extension of an extremal 12-point set, and no 16-point record is a two-point extension of a saturated extremal 14-point set; at size 12 this is different (R12): 26,852 of the 54,243 extremal classes are two-point extensions of extremal 10-point sets.
Evidence: experiments/20261016-0330-ext12-all/ (README, summary.json), data/ext12_all_rows.jsonl.gz, results/proofs/L006-ext12-all-two-point-extensions.md, tests/test_ext12_all.py.

**R12. The two-point-extension structure fades towards the wall (K49).** The fraction of extremal classes that contain an extremal subset two points smaller is 100% at $n=6,7,8,9,11$, 99.7% of the saturated classes at $n=10$ (6,625 of 6,644; 12,681 of 13,749, i.e. 92.2%, if the 7,105 stored non-saturated representatives are included), 49.5% at $n=12$ (26,852 of 54,243) and 0% at $n=14$ (K47, K48); no 16-point record can contain a saturated extremal 14-set (K46). Exact counts on the stored censuses; the trend itself is three even-$n$ data points [heuristic]. Evidence: experiments/20261016-0840-extremal-subsets/, tests/test_extremal_subsets.py.

**R13. $f(16)=10$: no 16-point (4,5)-set beats $4/7$ (certificate L008, ACCEPTED by three referees, one on the strongest model; novelty CLEAR).** The extension run (2026-10-17) found that the inequality I11: $11\tau\le3n+2m$ holds on all data (equality on $A_{\rm base}$) and, via a window-cell induction on the class of linear $F_7$-free 3-graphs with $e(S)\le|S|-2$, proved it for $n\le16$: a 16-point record would have $m=14$ and every AP-degree $\le3$, and every way of re-inserting a degree-3 vertex into the possible 15-vertex remainders creates an $F_7$ or breaks midpoint injectivity. The same induction closed Q11 (certificate L007, K51: no non-saturated extremal 14-point set; 2,910 is the complete count) gives $f(18)=11$ (L009) and $f(20)=12$ (L010), each ACCEPTED by three referees, so no record exists at $n=16,18,20$; the same method has emptied the cells at $n=21,22$ (certificate L011, pending referees), which would make 23 the smallest size at which a record is possible. I11 in general is a conjecture (kb/notes/i11_conjecture.md) that would give $c_*\ge6/11$. Evidence: results/proofs/L007-L010, experiments/falsify/i11-inequality/, experiments/20261017-*-via-i11/.

## 2. The case $n=16$: closed by R13 (earlier negative results D15, D16, D24, L005, L006)

Beating $4/7$ first becomes possible at $n=16$ ($h=9$, $m\in\{13,14\}$). Everything tried is consistent with a wall there:
- the abstract class has no $\alpha\le9$ member that any method could find at $n=16$ (CP-SAT, glucose, cadical, annealing over
  about 4 million maps with 28,589 genuine (4,5)-sets reached, constrained runs with all census invariants), while
  $n\le14$ witnesses are found in seconds and the realizable fraction of the filtered abstract extremal patterns (class O', K31 and cores with at most 4 edges) falls from 13.7% at $n=12$ (54,243 of 395,039) to 6.3% at $n=14$ (2,910 of 46,419);
- no witness at $n=18,20,22$ (3600 s each) and $n=23,25$ (1200 s per $m$ value) in realizability-CEGAR searches, all UNKNOWN; at $n=15$ no class-O' pattern with $\alpha\le9$ and $m'\in\{9,10\}$ was found in 2 h (no UNSAT proof either), and the census invariants (max degree $\le4$, balanced colour classes, no reflection symmetry hold for all 395,039 filtered $(12,10)$ patterns and for the 157 partial $(14,12)$ realizable patterns) do not make $n=16$ tractable;
- the number of saturated extremal classes drops from 54,243 ($n=12$) to 2,910 ($n=14$);
- none of the 2,910 saturated extremal 14-point sets extends by two points to a 16-point set with $h\le9$ (R9, L005): a 16-point record would have to be built on non-saturated 14-point extremal subsets (if any exist, Q11) or contain no extremal 14-point subset at all.
No certificate was reachable in this run: the n=16 sub-instances tried exceed the solver limits (including final CP-SAT and CaDiCaL runs with the Henning–Yeo deletion constraints of Lemmas Δ and Δ′, UNKNOWN or TIMEOUT after 3.5 h per case and solver, D24), the exact DFS needs about $10^{14}$ nodes,
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
  3,437 depth-3 prefixes; 0 patterns in every finished prefix; the results directory is git-ignored (.gitignore line 29), so the per-prefix .done markers and .jsonl.gz outputs exist only on the machine that ran the job and are not in the repository (so not in PR #1); of the dated counts that follow, 130 and 431 are also recorded in journal/LOG.md, while the 558 at 16:12 UTC is taken from the .done markers' modification times and is not in the LOG). Progress: 130 prefixes done at 2026-10-16 01:18 UTC, 431 at 08:49 UTC
  (then paused 3.5 h for the solver runs of D24), 558 at 16:12 UTC, 706 at 18:20 UTC and 1030 at 22:14 UTC on 4 workers; measured rate 22 to 36 prefixes/h, so the remaining
  prefixes (2,879 of 3,437) need roughly 80 to 130 hours of wall time and the case stays open (Q11; final count at the end of the run in
  journal/LOG.md and section 4 of this report). Completion decides whether 2,910 is the total number of extremal 14-point classes and,
  with R9 and R11, whether any 16-point record can contain an extremal 14-point subset at all.
- The saturated census at $n=13$ was started and stopped as infeasible (D22, Q12): 8 of 1,811 prefixes already hold
  54,717,717 abstract patterns (Henning–Yeo slack 13 at $(13,11,5)$); a realizability-aware enumerator is needed.
- Recommended next steps: (i) a dedicated exact engine for $n=16$: cube-and-conquer on the first midpoint edges with the deletion
  constraints of D24 (CP-SAT and CaDiCaL both time out on the monolithic instance), or a distributed DFS of about $10^{14}$ nodes; (ii) if $f(16)=10$ is confirmed, the
  abstract wall is combinatorial and the Q8-type induction with 5/6-edge cores is the natural proof program;
  (iii) obtain Henning–Yeo 2021 for its equality cases (Lemma U shows how the equality structure constrains universal
  vertices); (iv) submit the census sequence to the OEIS; (v) four-point extensions of the 2,910 classes (an 18-point set
  with $h=10$ would be a record; it would need $m=16=n-2$ and $\tau=8=\lfloor(5n+3m)/17\rfloor$, i.e. be fully saturated and Henning–Yeo-tight after rounding [derived-here; kb/00_START_HERE.md section 4 and `python3 -m e757.fn_bounds`]; whether a new extreme point is forced is not established here) and two-point extensions
  of any $(14,11)$ classes found; (vi) a realizability-aware enumerator for the $n=13$ census (D22).
- Repository state: all work of this run is on branch claude/intelligent-pasteur-22z06m (remote origin). PR #1 (to main, opened 2026-10-15 23:07 UTC) is merged into main right after this final checkpoint (2026-10-16 18:20 UTC), with about 4.7 hours of budget left; any later commit on the branch (log lines, final search counts) is cosmetic and, if the session is still alive, merged through a small follow-up PR before 23:06 UTC.

## 5. Infrastructure built (e757/, all tested; 145 tests, 144 passed and 1 skipped in the full run completed 2026-10-16 16:32 UTC, including the regression tests of R9 to R12)
Exact realizability oracle with Farkas certificates (realizability.py); CP-SAT model of the ordered-midpoint class
(cpsat_model.py, with monotone/medial/core constraints and a realizability-CEGAR); independent python-sat encoding
(sat_indep.py, with Gyárfás–Lehel colouring constraints); exact C DFS with resumable prefix split (c/ordered_dfs.c,
ordered_dfs_split.py); midpoint-map annealer (anneal.py). Experiment-level tools: the exact two-point-extension sweepers
(experiments/20261015-2340-ext14-all/extend_all.py, experiments/20261016-0330-ext12-all/extend12_all.py, with plain-integer
brute-force cross-checkers; the ext12 one reuses extend12_all's h routine and comparison, while the brute-force part of the ext14 one imports neither e757 nor extend_all, which is imported only afterwards for the comparison with the stored counts), the structural census (experiments/20261016-0150-structure-2910/stats.py,
experiments/20261016-0840-extremal-subsets/stats.py) and the deletion-constrained $n=16$ models
(experiments/20261016-0850-n16-deletion-cpsat/model16.py, experiments/20261016-1240-n16-cnf-witness/build_cnf.py).
The frozen judge (judge/judge.py) was used for every spot check.

## 6. Dead ends added (kb/dead_ends.md D15 to D24)
Direct SAT/CP-SAT at $n=16$ (with or without structure, with or without census invariants); annealing at $n=16$ and $18$;
Q8 for the abstract class (D17); witness sweeps $n=18..25$ (D18); the layered $15\to16$ search (D19); D20, D21 (solver variants);
the pattern-first saturated census at $n=13$ (D22); two-point extensions of smaller extremal sets as a route to records (D23: R4, R9,
R10, R11); CP-SAT and CaDiCaL at $n=16$ with the Henning–Yeo deletion constraints (D24).
