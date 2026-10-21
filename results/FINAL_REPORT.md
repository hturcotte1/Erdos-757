# Erdős Problem #757: final report of the autonomous run (2026-10-13 23:06 UTC to 2026-10-16 23:06 UTC)

Last updated: 2026-10-21 04:40 UTC (final). Three phases: the 72 h run (2026-10-13/16: exact small-case censuses, certificates L001-L006) and the 48 h extension (2026-10-17/18: the I11 window-cell induction, L007-L014, f(16) = 10 to f(23) = 14, no (4,5)-set with <= 24 points beats 4/7), then the resumption of 2026-10-20/21 (the community 5/9 family rebuilt, judged and proved here: C003, L015; this project's Lemma-E record sets C004, C005; the n = 27 certificate L016, pending). Goal clauses per scripts/status.sh: (A) met by judged and refereed record sets (C003 is a COMMUNITY construction, an anonymous reader's family from Erdős Problem a Day, 19 Oct 2026, unreviewed by humans there, submitter declares AI tools; C004 and C005 are this project's Lemma-E extensions of that family, so the record rests on a community construction), (B) not met (the lower bound 9/17 is untouched; nothing is claimed about whether c* = 5/9), (C) met (budget_exhausted YES, this report in place). The published bounds $9/17\le c_*\le4/7$ (Ma-Tang 2026) are improved on the upper side only by the community family, verified here [verified-here] but neither [published] nor this project's discovery (section 8).

## 0. Executive summary (final, 2026-10-21)

**This project's own results** (all [verified-here], computer-assisted unless noted; three referees ACCEPT each unless noted):
- K51 / L007: no non-saturated extremal 14-point set (Q11 closed); 3 ACCEPTs.
- K52-K55 / L008-L011: f(16) = 10, f(18) = 11, f(20) = 12, f(22) = 13, and I11 on the class C for n <= 22; 3 ACCEPTs each.
- K56 / L012: a 23-point record would have all AP-degrees <= 3 (degree-4 case excluded); 3 ACCEPTs.
- K57 / L013: I11 on the class C for n <= 26; 3 ACCEPTs.
- K58 / L014: f(23) = 14, hence no (4,5)-set with <= 24 points beats 4/7; 3 ACCEPTs (Theorem 2 and Corollary 3 are [derived-here] from the computer-assisted Theorem 1).
- K62 / C004: 58-point (4,5)-set, h = 33 (33/58), the smallest record set known (Lemma-E extension of the community set S_5); 2 ACCEPTs + judge PASS.
- K63 / C005: 67-point set, h = 38 (38/67), best finite ratio among judged sets (Lemma-E extension of S_6); 2 ACCEPTs + judge PASS.
- Earlier censuses K41, K43, K45, K46, K48 (L001-L006) and K47, K49 [verified-here]; I11 itself in general is a [conjecture].

**Community construction verified here** (anonymous reader's self-similar family, Erdős Problem a Day, 19 Oct 2026, 'unreviewed by humans' there, submitter declares AI tools; [community] construction and claim, not this project's discovery):
- K59 / C003: 65-point set, h = 37, judged NEW-RECORD, 2 ACCEPTs (c* <= 37/65).
- K60 / L015: proof for every depth that S_K has 11 + 9K points, h = 7 + 5K, hence c* <= 5/9; 3 ACCEPTs.

**Unrefereed or heuristic:** [L016 STATUS TO BE UPDATED] certificate L016 (I11 at n = 27, f(27) = 16, hence no 27-point set beats 4/7; ACCEPTED by two referees so far, third round pending, scout CLEAR; [derived-here] until refereed, no K-number yet); the n = 27 cell computations behind it; the D27 search for other self-similar chains (nothing below 5/9 in the tested ranges, [verified-here] for those ranges only, not a theorem).

**Bounds on c*:** published 9/17 <= c* <= 4/7; verified here from the community family c* <= 5/9 (L015); smallest record set 58 points (C004). Lower bound untouched; nothing is claimed about c* = 5/9.


## 1. Verified results (each with a referee-accepted certificate or an exact, re-verifiable computation)

Tags (CLAUDE.md integrity rule 6; they follow kb/known_results.md and results/LEDGER.md):
- R1 (K41, L002), R2 (K43, L003), R3 (K45, L004), R4 (K13, L001), R6 (K32, K33), R9 (the certificate L005, K46), R10 (K47), R11 (L006, K48), R12 (K49, exact counts) and R13 (K51 to K55 and the certificates L007 to L011, computer-assisted) are [verified-here]; the trend read into R12 is [heuristic]; the general inequality I11 quoted in R13 is [conjecture] (it is proved only on the abstract class for n <= 22), and the sentence in R13 that 23 is the smallest size at which a record is possible also uses the Henning–Yeo exclusion of the other sizes (K24) and is [derived-here].
- R7 (K35, K36) is [verified-here] as arithmetic and exact computation. The exact values f(n) it relies on use the published Henning–Yeo bound and are [derived-here] (K24).
- In R5, K30, K31 and K33 are [verified-here]. The degree bound K44 is [derived-here].
- In R8, K34 and K38 are [verified-here]; K34 is evidence on data, not a proof of Q8. K39 is [verified-here] for its exact optima on the stated data sets. Reading them as predictions, including the sentence on the dominant hard local type in any minimal counterexample, is [heuristic]. The free-move conditions of kb/methods/trackL_inductive_framework.md are [derived-here].
- In R9, the lemmas E, U, Δ and Δ′ of kb/notes/extension_lemmas.md are [derived-here] (falsifier HOLDS-ON-DATA on about 11,000 sets, and Δ′ on all stored censuses).
- In sections 2 and 3, these are [heuristic]: the pre-extension statements "Two hypotheses remain", "the evidence favours H2", "everything tried is consistent with a wall" and "no certificate was reachable in this run", and the interpretation of unfinished or failed searches (D15 to D24). Since the extension, R13 (certificates L008 to L011, K52 to K55, each ACCEPTED by three referees) decides the finite part of H1 and H2: the exact values $f(16)=10$, $f(18)=11$, $f(20)=12$, $f(22)=13$ and the statement that no (4,5)-set with at most 22 points beats $4/7$ are [verified-here]; H1 is [refuted] (the Henning–Yeo bounds 9, 10, 11, 12 at $n=16,18,20,22$ are each one below these values). Reading the surviving f(n) pattern as support for $c_*=4/7$ or for Q8 stays [heuristic], and nothing is established for $n\ge23$. The exact counts quoted there keep their own tags:
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
14-point sets exist was open when this was written (CP-SAT returned UNKNOWN after two hours, D21; the exhaustive DFS was stopped at 1,081 of 3,437 prefixes with 0 patterns); it was closed on 2026-10-17 by certificate L007 (K51, ACCEPTED by three referees): no non-saturated extremal 14-point set exists, so the 2,910 classes are all the extremal 14-point classes, with the completeness caveat of L004 stated above (see R13).
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
the conjecture $c_*=4/7$. Q8 is **false for realizable sets**: with no avoided points it requires $7\tau\le3n$, but C003 (the 65-point member of an anonymous reader's self-similar family, posted on Erdős Problem a Day on 19 Oct 2026 [community]; rebuilt, judged and refereed here, not discovered here; K59, section 8) has $n=65$, $h=37$, hence $\tau=28$ and $7\tau=196>195=3n$ [derived-here from K59]. The same set shows that $c_*=4/7$ itself is false ($c_*\le37/65<4/7$ by K59; $c_*\le5/9$ by the reader's whole family, certificate L015, K60). The "holds on every state" counts above (K34) and the realizable-data constant $3/7$ below (K39) remain true for the data they cover. Q8 is likewise **false for the abstract class**: a 12-vertex pattern that is linear, $F_7$-free, monotone,
medial-free and clean of all $\le4$-edge cores violates it by one; every one of the 89 abstract violators found among the first 26,974 members of the (12,10,$\alpha\le7$) census snapshot (K38, K39) contains a 5- or 6-edge
forbidden core. On realizable data the best inductive constant is exactly $3/7$; on abstract data it is $31/70$. The
most frequent hard local type (about 40% of the hard vertices) among the local types that are neither freely deletable nor avoidable, in the abstract Q8 violators (910 vertices in 91 states) and in the realizable irreducible tight states (63 vertices in 6 states) alike, is a vertex on three full traces (K39) [heuristic]. kb/methods/trackL_inductive_framework.md
gives the exact free-move conditions for every $(a,b,c,d)$.

**R9. No 16-point record contains a saturated extremal 14-point set (certificate L005, ACCEPTED by two fresh referees at 01:37 UTC after a text-only NEEDS-WORK round; novelty CLEAR).**
The refereed L001 case analysis (two-point extensions of $A_{\rm base}$) was applied to all 2,910 saturated extremal 14-point
classes of R3 (L004): 141,153 (4,5) single extensions, 4,970,208 enumerated (4,5) two-point extensions (the finite case T1b; the cases T0, T1a, T2 contain continua and are decided by the case analysis), $122{,}220$ generic one-edge lines,
all with $h=10$; no class has a point lying in every maximum Sidon subset (137 to 150 such subsets per class). Hence every
14-point subset with $h=8$ of a hypothetical 16-point set with $h=9$ is non-saturated ($m=11$; at the time of L005 this was the open case Q11). Both questions are now settled: Q11 is closed (L007, K51: no non-saturated extremal 14-point set exists) and no 16-point set with $h\le9$ exists at all ($f(16)=10$, L008, K52, R13), so this conclusion and the Lemma $\Delta$/$\Delta'$ statements about a 16-point record below are vacuous; the L005 enumeration itself is unaffected. This inherits the completeness of the L004 census (R3), which the referee re-checked independently only by sampling (28% of the prefixes) plus consistency checks, not by a second full enumeration.
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

**R11. No extremal 14-point set contains an extremal 12-point set (certificate L006, ACCEPTED by two fresh referees at 08:31 UTC after a text-only NEEDS-WORK round; novelty CLEAR).** The L001/L005 two-point-extension analysis applied to all 54,243 extremal 12-point classes (R1, L002): 1,887,566 (4,5) single extensions (all $h=8$), 51,264,727 (4,5) two-point extensions with both new points in new APs (all $h=9$), 1,952,748 one-edge lines (all $\alpha=9$); referee round 3 confirmed the whole census independently with a Sidon-definition-only method. Hence every 12-point subset of every extremal 14-point set has $h=8$, and a non-saturated $(14,11)$ extremal set (the case Q11, open when this was written) would contain no extremal 12-point subset; by L007 (K51) no such set exists. Together with R9 and R10: no extremal 14-point set is a two-point extension of an extremal 12-point set, and no 16-point record is a two-point extension of a saturated extremal 14-point set; at size 12 this is different (R12): 26,852 of the 54,243 extremal classes are two-point extensions of extremal 10-point sets.
Evidence: experiments/20261016-0330-ext12-all/ (README, summary.json), data/ext12_all_rows.jsonl.gz, results/proofs/L006-ext12-all-two-point-extensions.md, tests/test_ext12_all.py.

**R12. The two-point-extension structure fades towards the wall (K49).** The fraction of extremal classes that contain an extremal subset two points smaller is 100% at $n=6,7,8,9,11$, 99.7% of the saturated classes at $n=10$ (6,625 of 6,644; 12,681 of 13,749, i.e. 92.2%, if the 7,105 stored non-saturated representatives are included), 49.5% at $n=12$ (26,852 of 54,243) and 0% at $n=14$ (K47, K48); no 16-point record can contain a saturated extremal 14-set (K46). Exact counts on the stored censuses; the trend itself is three even-$n$ data points [heuristic]. Evidence: experiments/20261016-0840-extremal-subsets/, tests/test_extremal_subsets.py.

**R13. $f(16)=10$: no 16-point (4,5)-set beats $4/7$ (certificate L008, ACCEPTED by three referees, one on the strongest model; novelty CLEAR).** The extension run (2026-10-17) found that the inequality I11: $11\tau\le3n+2m$ holds on all data (equality on $A_{\rm base}$) and, via a window-cell induction on the class of linear $F_7$-free 3-graphs with $e(S)\le|S|-2$, proved it for $n\le16$: a 16-point record would have $m=14$ and every AP-degree $\le3$, and every way of re-inserting a degree-3 vertex into the possible 15-vertex remainders yields, whenever $\tau\ge7$, a pattern that contains an $F_7$ or violates $e(S)\le|S|-2$ (L008 Steps 5.2-5.3, computation C5). The same induction closed Q11 (certificate L007, K51: no non-saturated extremal 14-point set, so the 2,910 classes of L004 are all the extremal 14-point classes; the count inherits the completeness caveat of L004 stated in R3, namely that completeness was re-checked on 28% of the prefixes and not by a full second enumeration) and gave $f(18)=11$ (L009) and $f(20)=12$ (L010), each ACCEPTED by three referees, so no record exists at $n=16,18,20$; and the same method emptied the cells at $n=21,22$ (certificate L011, ACCEPTED by three referees; $f(22)=13$), so no (4,5)-set with at most $22$ points beats $4/7$ and, at that point, 23 was the smallest size at which a record was not excluded (the cell $(23,21,10)$ has I11 slack 1; L011 Corollary 3 and Remark 5); that cell was excluded afterwards (degree 4: no realizable class, L012, K56; degree 3: empty in the abstract class, L014, K58), so $f(23)=14$ and the smallest size at which a record is not excluded is now $n=25$ (section 7). I11 in general is a conjecture (kb/notes/i11_conjecture.md) that would give $c_*\ge6/11$. Evidence: results/proofs/L007-L011, experiments/falsify/i11-inequality/, experiments/20261017-*-via-i11/.

## 2. The case $n=16$: closed by R13 (earlier negative results D15, D16, D24, L005, L006)

Beating $4/7$ first became arithmetically possible at $n=16$ ($h=9$, $m\in\{13,14\}$). Before the extension everything tried was consistent with a wall there, and certificate L008 (R13; computer-assisted, ACCEPTED by three referees) then proved it ($f(16)=10$). The bullets and the closing paragraph below record the evidence and the hypotheses H1/H2 as they stood before the extension:
- the abstract class has no $\alpha\le9$ member that any method could find at $n=16$ (CP-SAT, glucose, cadical, annealing over
  about 4 million maps with 28,589 genuine (4,5)-sets reached, constrained runs with all census invariants), while
  $n\le14$ witnesses are found in seconds and the realizable fraction of the filtered abstract extremal patterns (class O', K31 and cores with at most 4 edges) falls from 13.7% at $n=12$ (54,243 of 395,039) to 6.3% at $n=14$ (2,910 of 46,419);
- no witness at $n=18,20,22$ (3600 s each) and $n=23,25$ (1200 s per $m$ value) in realizability-CEGAR searches, all UNKNOWN; at $n=15$ no class-O' pattern with $\alpha\le9$ and $m'\in\{9,10\}$ was found in 2 h (no UNSAT proof either), and the census invariants (max degree $\le4$, balanced colour classes, no reflection symmetry hold for all 395,039 filtered $(12,10)$ patterns and for the 157 partial $(14,12)$ realizable patterns) do not make $n=16$ tractable;
- the number of saturated extremal classes drops from 54,243 ($n=12$) to 2,910 ($n=14$);
- none of the 2,910 saturated extremal 14-point sets extends by two points to a 16-point set with $h\le9$ (R9, L005): a 16-point record would have to be built on non-saturated 14-point extremal subsets (Q11, then open; closed by L007, K51: there are none) or contain no extremal 14-point subset at all; L008 (R13, K52) later showed that no 16-point record exists.
No certificate was reachable in this run: the n=16 sub-instances tried exceed the solver limits (including final CP-SAT and CaDiCaL runs with the Henning–Yeo deletion constraints of Lemmas Δ and Δ′, UNKNOWN or TIMEOUT after 3.5 h per case and solver, D24), the exact DFS needs about $10^{14}$ nodes,
and SAT UNSAT times grow from 2 s ($n=12$) to over 250 s ($n=13$). Two hypotheses were open before the extension: (H1) Henning–Yeo stays tight at even $n$ up to 22 (records at 16..22, $c_*\le6/11$); (H2) a wall at 16 ($f(16)=10$, consistent with $c_*=4/7$ and Q8). The evidence favoured H2 [heuristic]. The extension settled the finite part: $f(16)=10$, $f(18)=11$, $f(20)=12$, $f(22)=13$ (R13; K52 to K55, [verified-here], each with three accepting referees), so there is no record at $n=16,18,20,22$, H1 is refuted in its stated range, and no (4,5)-set with at most 22 points beats $4/7$ (L011, Corollary 3). On its own this finite result does not decide $c_*$. Since 2026-10-20, however, the self-similar family of section 8 (an anonymous reader's construction, Erdős Problem a Day, 19 Oct 2026 [community]; rebuilt, judged and refereed here, not discovered here) gives $c_*\le5/9<4/7$ (C003, K59; L015, K60; [verified-here]). Hence $c_*=4/7$ is false [derived-here from K60], and the Q8-type route to it (R8) is closed: without avoided points Q8 reads $7\tau\le3n$, which fails for the 65-point set of C003 ($\tau=65-37=28$ and $7\cdot28=196>195=3\cdot65$) [derived-here]. The open question is the true value of $c_*$ in $[9/17,5/9]$.

## 3. Lower-bound track: why no proof was attempted

Any improvement of $9/17$ must come from asymptotics (R7). The one candidate structure of the first 72 hours (the extension added a second one, the inequality I11 of section 7, which would give $c_*\ge6/11$ but is proved only for $n\le22$), a Q8-type inductive inequality,
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
  prefixes (2,407 of 3,437) would have needed roughly 67 to 110 hours of wall time at the rate then measured. This bullet is a snapshot of 2026-10-16 22:15 UTC: the job was stopped at 1,081 of 3,437 prefixes with 0 patterns (last progress line of its run.log) and is superseded by certificate L007 (K51, ACCEPTED by three referees, 2026-10-17), which proves the $(14,11,\alpha\le8)$ cell empty (Q11 closed). Hence 2,910 is the total number of extremal 14-point classes (with the completeness caveat of L004, R3). The question whether a 16-point record could contain an extremal 14-point subset (R9, R11) is moot, because R13 (certificate L008) shows that no 16-point (4,5)-set beats 4/7.
- The saturated census at $n=13$ was started and stopped as infeasible (D22, Q12): 8 of 1,811 prefixes already hold
  54,717,717 abstract patterns (Henning–Yeo slack 13 at $(13,11,5)$); a realizability-aware enumerator is needed.
- Recommended next steps as of 2026-10-16 (superseded by section 9): (i) [done differently in the extension: $f(16)=10$ was decided by the window-cell induction on the I11 slack (certificate L008, K52, R13), not by cube-and-conquer or a $10^{14}$-node DFS; the same induction then gave $f(18)=11$, $f(20)=12$ and $f(22)=13$ (L009 to L011)]; (ii) [confirmed: $f(16)=10$, L008] the abstract wall is combinatorial, and the natural proof program is now a proof of I11 in general (section 7; still a [conjecture], verified here only on the abstract class $C$: for $n\le22$ by L007–L011 and for $n\le26$ by L013, K57, each ACCEPTED by three referees), and the Q8-type induction with 5/6-edge cores is no longer an alternative: Q8 without avoided points reads $h\ge4n/7$ (R8), and the community 65-point set of section 8 (C003, K59; an anonymous reader's construction, verified here, not discovered here) has $h=37$, so $7(n-h)=196>195=3n$ and Q8 is false for realizable sets [derived-here];
  (iii) obtain Henning–Yeo 2021 for its equality cases (Lemma U shows how the equality structure constrains universal
  vertices); (iv) submit the census sequence to the OEIS; (v) [moot after the 48-hour extension, [verified-here]: $f(18)=11$ (L009, K53), so no 18-point record exists, and no non-saturated $(14,11)$ extremal set exists (L007, K51; Q11 closed); the rest of this item is the pre-extension rationale] four-point extensions of the 2,910 classes (an 18-point set
  with $h=10$ would be a record; it would need $m=16=n-2$ and $\tau=8=\lfloor(5n+3m)/17\rfloor$, i.e. be fully saturated and Henning–Yeo-tight after rounding [derived-here; kb/00_START_HERE.md section 4 and `python3 -m e757.fn_bounds`]; whether a new extreme point is forced is not established here) and two-point extensions
  of any $(14,11)$ classes found; (vi) a realizability-aware enumerator for the $n=13$ census (D22).
- Repository state: all work of this run is on branch claude/intelligent-pasteur-22z06m (remote origin). PR #1 (to main, opened 2026-10-15 23:07 UTC) is merged into main right after this final checkpoint (2026-10-16 18:20 UTC), with about 4.7 hours of budget left; any later commit on the branch (log lines, final search counts) is cosmetic and, if the session is still alive, merged through a small follow-up PR before 23:06 UTC.

## 5. Infrastructure built (e757/, all tested; 145 tests, 144 passed and 1 skipped in the full run completed 2026-10-16 16:32 UTC, including the regression tests of R9 to R12; the extension added tests/test_l007_cells.py (7 tests) and tests/test_l008_cells.py (5 tests), so 157 tests are collected as of 2026-10-17, and the 144-passed figure refers to the 2026-10-16 run)
Exact realizability oracle with Farkas certificates (realizability.py); CP-SAT model of the ordered-midpoint class
(cpsat_model.py, with monotone/medial/core constraints and a realizability-CEGAR); independent python-sat encoding
(sat_indep.py, with Gyárfás–Lehel colouring constraints); exact C DFS with resumable prefix split (c/ordered_dfs.c,
ordered_dfs_split.py); midpoint-map annealer (anneal.py). Experiment-level tools: the exact two-point-extension sweepers
(experiments/20261015-2340-ext14-all/extend_all.py, experiments/20261016-0330-ext12-all/extend12_all.py, with plain-integer
brute-force cross-checkers; the ext12 one reuses extend12_all's h routine and comparison, while the brute-force part of the ext14 one imports neither e757 nor extend_all, which is imported only afterwards for the comparison with the stored counts), the structural census (experiments/20261016-0150-structure-2910/stats.py,
experiments/20261016-0840-extremal-subsets/stats.py) and the deletion-constrained $n=16$ models
(experiments/20261016-0850-n16-deletion-cpsat/model16.py, experiments/20261016-1240-n16-cnf-witness/build_cnf.py).
The frozen judge (judge/judge.py) was used for every spot check.

## 6. Dead ends added (kb/dead_ends.md D15 to D27; D25, D26, D27 and the second CP-SAT run recorded under D21 come from the extension, see sections 7 and 8)
Direct SAT/CP-SAT at $n=16$ (with or without structure, with or without census invariants); annealing at $n=16$ and $18$;
Q8 for the abstract class (D17); witness sweeps $n=18..25$ (D18); the layered $15\to16$ search (D19); D20, D21 (solver variants);
the pattern-first saturated census at $n=13$ (D22); two-point extensions of smaller extremal sets as a route to records (D23: R4, R9,
R10, R11); CP-SAT and CaDiCaL at $n=16$ with the Henning–Yeo deletion constraints (D24).

## 7. The 48-hour extension (2026-10-17/18): the I11 induction

The user extended the run by 48 hours after the 72-hour budget (GOAL.md and the status script are unchanged, so the status
block keeps reporting clause C). The extension turned a data-driven conjecture into a chain of exact results.

**The inequality I11** [conjecture in general]: for the AP hypergraph of every (4,5)-set, $11\tau\le3n+2m$ (slack $s=3n+2m-11\tau\ge0$).
It is strictly stronger than Henning–Yeo for saturated sets ($h\ge(6n+4)/11$, so $c_*\ge6/11$ would follow from a proof)
and it is tight: equality on $A_{\rm base}$ $(14,12,6)$, on $(3,1,1)$, $(10,7,4)$, $(12,4,4)$, $(13,8,5)$ and their disjoint unions.
The falsifier found no violation on any data (experiments/falsify/i11-inequality: all subsets of all 2,910 and 54,243 census
classes, 1.33M realizable rows, Fibonacci prefixes, gluings, extensions, the abstract censuses). Both hypotheses of the class
$C$ (linear $F_7$-free 3-graphs with $e(S)\le|S|-2$ on every subset) are essential: abstract counterexamples exist without
either (kb/notes/i11_conjecture.md).

**The window-cell induction** [verified-here, certificates L007–L011 ACCEPTED by three referees each].
Slack is additive over components and $C$ is hereditary, so a violator has a connected violating component in one of finitely
many Henning–Yeo "window cells" $(n,m,\tau)$. I11 at $n-1$ bounds every degree of a hypothetical violator at $n$ (often to
$\le3$ or $\le2$), which either kills the cell by degree counting or reduces it to re-inserting one vertex into the few
connected low-slack graphs of the smaller cell, themselves rebuilt recursively from even smaller slack cells. Every enumeration
was done by at least three independently written generators (canonical BFS-growth DFS, nauty genbg orderly generation, SAT),
with definitional $F_7$ and $e(S)\le|S|-2$ filters, byte-for-byte reproduction of all outputs and $\tau$-lowered controls.
Results:
- L007 (K51): no non-saturated extremal 14-point set; the 2,910 classes of L004 are all extremal 14-point sets (Q11 closed; the completeness of the 2,910-class census is inherited from L004, which was re-checked only by sampling plus consistency checks, see R3 and L007 Corollary 3).
- L008 (K52): $f(16)=10$; no 16-point (4,5)-set beats $4/7$ (the open case Q1 closed). Witness: $A_{\rm base}\cup\{-323,5000\}$.
- L009 (K53): $f(18)=11$. L010 (K54): $f(20)=12$. L011 (K55): I11 on $C$ for $n\le22$, $f(22)=13$ (all ACCEPTED by three referees).
  Hence no (4,5)-set with at most 22 points beats $4/7$; the first record cells I11 allows are $(23,21,10)$, $(25,23,11)$,
  $(30,27,13)$, $(30,28,13)$, $(32,29,14)$, $(32,30,14)$, $(34,32,15)$.
- L013 (K57, ACCEPTED by three referees): I11 on $C$ for $n\le26$ (four more induction steps with the L012 engine; no new $f(n)$).
- L014 (K58, ACCEPTED by three referees, 2026-10-20): $f(23)=14$. The degree-3 case of the record cell $(23,21,10)$ is empty in $C$ (the slack-3 decompositions of $(22,18)$, with cell(22,18,9,3) = 94,513 classes, give 133,804 inputs and no extension in $C$); with L012 no 23-point (4,5)-set has $h=13$, and the explicit set $C_{23}=B_{12}\cup(10^9+7919B_{11})$ has $h=14$. Hence no (4,5)-set with at most 24 points beats $4/7$, and $n=25$ is the first open record size. The computation that L012 Step 8 estimated at $2.5\cdot10^{24}$ ordered-search calls took about 1.5 CPU-hours at the class level (Q14 closed).
- L012 (K56, ACCEPTED by three referees): a 23-point record, if one exists, has every AP-degree $\le3$: the degree-4 case leaves 699 abstract
  classes in $C$, none of them realizable (exact realization of the rigid saturated systems); the degree-3 case, open when L012 was written (Q14), was closed by L014 (K58, above).
- By-products: K50 (non-saturated extremal 15-point sets exist, with 11 and 12 APs; two judged examples C001, C002);
  D25 (the ordered DFS cannot clear the 15-point cells: $\sim8\cdot10^{13}$ nodes each, which the unordered slack method
  reduced to minutes); D26 (no record among one-point extensions of 2,337 sampled extremal 15-point sets); the CP-SAT
  attempt at $(14,11)$ with deletion constraints, UNKNOWN (D21), superseded by L007.

**What this means for the problem.** The project's own constructions and proofs leave $9/17\le c_*\le4/7$ unchanged; the community construction of section 8, verified here, gives $c_*\le37/65$ (C003, refereed) and $c_*\le5/9$ (L015, K60, three referees). A proof of I11 in general would give
$c_*\ge6/11$ (goal clause B); the induction proves it only for $n\le26$ and gives no asymptotic argument. On the upper-bound
side, any set beating $4/7$ has at least 25 points (L014), and the natural next target is the I11-tight cell $(25,23,11)$. Separately, the community post of 19 Oct 2026 on Erdős Problem a Day (an anonymous reader's self-similar family; its submitter declares that AI tools found and refereed the bound, see the Origin paragraph of results/proofs/L015-reader-family-c-le-5-9.md and K60; provenance in section 8) has been rebuilt and verified here (experiments/20261020-1730-reader-5-9/): its 65-point member was judged and refereed (C003, K59) and a proof for every depth $K$ was written and refereed (L015, K60). The construction and the claim are [community] (kb/literature/bibliography.md), not this project's discovery and not among the project's own constructions; the verification, the judging and the proof certificate L015 are this project's work, reported in section 8.

**Tags.** The certificates L007–L014 and their K-rows K51–K58 are [verified-here] (three referees each; the certificate L014 itself tags its Theorem 2 and f(23)=14 as [derived-here]); L015 (K60) is a [verified-here] proof (three referees) of a [community] construction and claim, which stay [community]; C003 (K59) is a [verified-here] judge and referee result (two referees) on a [community] set; I11 in general is [conjecture]; the implication $c_*\ge6/11$ is conditional on it.

## 8. The reader's 5/9 family (2026-10-20): a community construction, verified here [community; verified-here]

CLAIM: c* <= 5/9 (certificate L015, ACCEPTED by three referees: an independent proof for every depth of the reader's family) and c* <= 37/65 (judged and refereed record set C003). Provenance: NOT this project's construction; the proof certificate and the verification are this project's.

On 19 Oct 2026 Erdős Problem a Day (a site built and kept by Patrick White with Claude) posted an anonymous reader's submission (id 7bkzb8, 17 Oct 2026). Provenance as the site itself states it (kb/literature/sources/aday_757_reader_5_9/): the set, the map, the claim and the '+5 per level' sketch are the reader's; the submitter's declared tools line reads 'Opus 5.5 found (and independently refereed) the bound. GPT Sol 6.1 also independently checked it', so by the submitter's own declaration (unverified by us) the bound was found by AI tools; the every-depth proof write-up, the checks and the 'hostile referee' pass are credited by the page to the site ('Ours'), whose review is described as 'Reviewed by Claude with Patrick White — an AI and a regular dude, not mathematicians. The verdict says what was checked; it is not community acceptance', i.e. AI-assisted by the site's own account; the write-up is labelled 'Unreviewed by humans', and the page says the submitter provided no code ('there was none'). The project's scouts could not retrieve the site's verification folder (HTTP 404 or 403), so the site's own proof file and referee report were not read. The submission's claim, paraphrased: with $O=\{0,49,75,83,98,101,117,119,121,159,269\}$ and $\varphi(x)=101+18x/269$, the sets $S_K=O\cup\varphi(O)\cup\dots\cup\varphi^K(O)$ (scaled by $269^K$) are (4,5)-sets with $11+9K$ points and largest Sidon subset $7+5K$, so $c_*\le\lim(7+5K)/(11+9K)=5/9$. The L014 scout found it on 2026-10-20. What this project did: (i) rebuilt the family exactly from the page's definition and verified $|S_K|=11+9K$, the (4,5)-property, exactly $9(K+1)$ three-term APs and $h(S_K)=7+5K$ for $K\le8$ by several independent exact methods (experiments/20261020-1730-reader-5-9/); (ii) submitted the $K=6$ member (65 points) to the frozen judge: `JUDGE: PASS NEW-RECORD C003-reader-5-9-K6 n=65 h=37 ratio=37/65 (0.569231) vs 4/7=0.571429` (results/claims/C003-reader-5-9-K6.json); (iii) two independent referees (opus and the strongest model) ACCEPT: all 677,040 four-subsets checked literally, $h=37$ proved by frontier DP, SAT (size 38 UNSAT), MILP and a hand-checkable telescoping bound, the judge re-run from scratch (K59; reviews in results/reviews/C003-*); the scout's novelty verdict is KNOWN (community), with no human-reviewed source confirming or disputing the entry; (iv) wrote certificate L015 with an independent proof for every depth $K$ (a deepest-level modulo-269 argument replacing the page's depth-12 census) and an independent verification; L015 was ACCEPTED by three referees on 2026-10-20 (round 1 with editorial fixes, applied; rounds 2 and 3 fresh), the falsifier found nothing (HOLDS-ON-DATA), and the scout's novelty verdict is PARTIAL (the construction and the claim are the reader's; the level/fixed-point identity and its deepest-level modulo-269 starting point are already on the site's page; L015's proof differs from the page's summary in finishing with a complete case analysis on the deepest level, with no span bound and no depth-12 census, and adds, beyond the page's summary, a per-copy bijection, hand-proved table inequalities and an explicit Sidon subset $T_K$ for every $K$; the comparison is against the page's summary only, because the site's proof folder was not retrievable) (K60). $K=5$ gives exactly $4/7$; $K=6$ is the first member below it; the margin at $K=6$ is one point ($37\cdot7=259<260$).

**This project's own addition (2026-10-21, K62, K63).** Lemma E of kb/notes/extension_lemmas.md (two points $a-t,a+t$ at a universal extreme point $a$ raise $h$ by exactly one and keep the (4,5)-property for generic $t$) applies to the family: the minimum and maximum of $S_K$ are its only universal vertices ($K\le6$, exact DP). The extension of $S_5$ is a 58-point (4,5)-set with $h=33$ ($33/58=0.56897$), the smallest record set known, and that of $S_6$ a 67-point set with $h=38$ ($38/67=0.56716$), the best finite ratio among the judged sets; both passed the frozen judge and two independent referees each (C004, C005; experiments/20261021-0225-lemmaE-extensions/). The two-sided extension raises $h$ by three, not two, so it gives no record at 51 or 60 points. The limit $5/9$ is not improved; a search for other self-similar seeds found none below $5/9$ (D27).

How this relates to the project's own results: it is consistent with everything proved here (no record at $n\le24$, K52–K58; the family's sizes are $11,20,29,\dots$ and its $n=20$ member has $h=12=f(20)$), and with I11 ($5/9>6/11$). It does not affect the lower bound $9/17$. Gluing (Ma–Tang Lemma 3.6) turns the single 65-point set into $c_*\le37/65$; the family itself gives $5/9$.

## 9. Recommended next steps (final)

1. Prove I11 ($11\tau\le3n+2m$) in general; this would give $c_*\ge6/11$ (clause B). It is a [conjecture], verified here on the class C for $n\le26$ (L007-L013) with L016 for $n=27$ pending.
2. Push the exact-value induction to $n=29$ ($f(29)=17$ would follow if I11 holds there); the first obstruction is the cell list needed beyond $n=27$.
3. Search self-similar seeds with 12-15 points and growth $h_0-2$ (D27 shows $h_0-1$ is the typical minimum; the reader's 11-point seed reaches $h_0-2$), and tree / multi-map recursions and chains sharing $\ge3$ points, which D27 did not run.
4. Decide $f(19)$, $f(21)$, $f(25)$ (open; $n=25$ is the first open record size by L014, with the I11-tight cell $(25,23,11)$).
5. A human-reviewed write-up of L015, since its source entry on Erdős Problem a Day is marked 'unreviewed by humans' and its provenance is AI-assisted.
