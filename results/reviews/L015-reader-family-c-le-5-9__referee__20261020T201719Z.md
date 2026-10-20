VERDICT: ACCEPT WITH FIXES

# Referee report, round 1: results/proofs/L015-reader-family-c-le-5-9.md (CLAIM: c* <= 5/9)

Referee: L015 round-1 referee (adversarial). Certificate reviewed: commit 1894f5d, sha256 3165c5e9…6136 (file unchanged since then). Scratch folder: experiments/referee/L015-round1/. Verdict scale: the workflow asked for ACCEPT / REJECT / ACCEPT WITH FIXES. "ACCEPT WITH FIXES" here means what NEEDS-WORK means on the standard referee scale. Every mathematical step is verified. The remaining items are documentation fixes (provenance completeness and a few mislabels), and none of them is load-bearing.

## Summary

The certificate proves, for every depth $K\ge0$, that the anonymous reader's set $S_K=\bigcup_{j\le K}\varphi^j(O)$ is a $(11+9K)$-point (4,5)-set with $h(S_K)=7+5K$. That gives $c_*\le\inf_K(7+5K)/(11+9K)=5/9$, with $K=6$ (65 points, $h=37$) the first member below $4/7$.

I re-derived every step by hand:
- the level lemma 1.2 (269-adic valuation);
- the complete case analysis of Step 2 on the deepest level mod 269, $m=1,2,3,4$, including the symmetry reduction, the equal-point cases and the sign bookkeeping;
- the AP hypergraph and its linearity;
- the deduction of the (4,5)-property (Step 4);
- the bijection between Sidon subsets and consistent per-copy choices, and the max-plus recursion;
- all six hitting-set arguments of 5.6;
- the explicit witness $T_K$;
- the final arithmetic.

I found no gap, no missing case and no hidden assumption. The argument only needs F1, F3, F4 and F5 about the 11-point set $O$ plus the table of 5.5, and the upper bound needs only the hand-proved inequalities of 5.6.

I recomputed F0–F6, the 16-entry table, the 5.6 transversal numbers and $U^*$ with my own code. I also ran:
- the relation census for $K\le20$, by sums and separately by differences;
- the literal 4-subset test for $K\le8$;
- $h(S_K)$ for $K\le20$ by two exact methods of my own that use only the Sidon definition (a frontier DP, and a SAT proof with CaDiCaL: $\ge7+5K$ SAT, $\ge8+5K$ UNSAT), plus CP-SAT for $K\le3$ and literal enumeration for $K\le1$;
- $T_K$ for $K\le30$.

I also confirmed that the C003 set is exactly $269^6S_6$. All of these agree with the certificate, and all seven prover scripts reproduce bit for bit, up to timings, from a scratch copy.

The Provenance section is honest, but it is incomplete. It does not record the submission page's "VERIFIED" label, the submitter's declared tools ("Opus 5.5 found (and independently refereed) the bound. GPT Sol 6.1 also independently checked it.") or what the site checked. There are also three small mislabels in the computational descriptions. Nothing is claimed about the lower bound or about $c_*=5/9$.

## Dependencies (as checked)
- Definitions of kb/00_START_HERE.md §1. They are used consistently: (4,5) means every 4 distinct points give at least 5 distinct distances, i.e. $|B-B|\ge11$; Sidon means all sums $x+y$ with $x\le y$ are distinct.
- K1 [published] (Ma–Tang Thm 1.5, $c_*=\inf f(n)/n$). It is used only in 7.3. Step 7.4 correctly avoids it for the Formal-Conjectures formulation. I checked the wording against kb/literature/sources/aday_757_reader_5_9/problem_757.txt: "c is admissible if, for any finite set A such that every four-element subset B determines at least five positive differences, there exists a Sidon subset S of size at least c * A.ncard … supremum". Since $I_K\subset\mathbb Z_{\ge0}$, the family qualifies under any ambient type.
- Nothing else is load-bearing. Ma–Tang Lemma 2.3 (Sidon = AP-free) is re-proved for $S_K$ in 5.1. Henning–Yeo, L001–L014, e757/ and judge/ are not used in the proof. The judge verdict and the agent's numbers appear only in Corollary 3 and C6, as stated.

## Step-by-step audit (hand re-derivation)

**Step 0.**
- 0.1: correct ($|B-B|=1+2\cdot\#$distinct positive differences).
- 0.2: correct. If $p_1=p_3$ then $p_2=p_4$, so the multisets coincide; the same holds for the other three cases.
- 0.3: correct. An affine map with $\lambda\ne0$ preserves relations and scales distances.
- F0–F5 hand checks, all re-done:
  - $269$ is prime, with $269=3\cdot89+2=5\cdot53+4=7\cdot38+3=11\cdot24+5=13\cdot20+9$ and $17^2=289$;
  - $27169=101\cdot269$;
  - $251\cdot108=27108<27169<27359$;
  - $y(269)=150\cdot269$;
  - $269-x\notin O^\circ$;
  - $x_1+x_2-x_3\in[-61,269]$;
  - the sums $\le159$ are $98,124,132,147,150,150,158$, and only 98 lies in $O^\circ$.

**Step 1.**
- 1.1(A)–(D): correct ($\varphi^j(x)=L+r^j(x-L)$; $\varphi^J$ is affine and increasing).
- Lemma 1.2: correct.
  - $269^dy(x)=18^dy(x')$ forces $269^d\mid y(x')$.
  - $v_{269}(y(x'))\le1$ on $O$, with equality only at $x'\in\{0,269\}$. So $d=1$, and $x=\varphi(x')\in\{101,119\}$.
- 1.3–1.4: correct.
  - The intersections are exactly $\{\varphi^j(101),\varphi^j(119)\}$ for consecutive copies and empty otherwise.
  - No point lies in three copies, and $11(K+1)-2K=11+9K$.
- 1.5: correct. For level $\ge1$ we get $x_p\in O^\circ$, because 0 and 269 would give an earlier copy.
- 1.6: correct ($N_j=101\cdot269^j+18N_{j-1}$).

**Step 2 (the heart).**
- 2.1–2.2: correct. The identity $\sum_i\varepsilon_i18^{j_i}269^{J-j_i}y(x_i)=0$ holds in $\mathbb Z$. The terms with $j_i<J$ vanish mod 269, and $18^J$ and $251$ are units, which gives $(\ast)$. $(\ast)$ is valid for every $J$. For $m\le3$ we have $J\ge1$, so $x_i\in O^\circ$ for $i\in T$.
- 2.3, $m=1$: impossible, since $O^\circ\subset[49,159]$.
- 2.4, $m=2$:
  - Opposite sides give $x_i=x_k$, so the same point is on both sides, which 0.2 excludes.
  - Same side, including $p_i=p_k$, i.e. $2x\equiv0$, is impossible by F5(ii).
  - This covers e.g. $(u,u,v,w)$ with $u$ alone at the deepest level, and $\{v,w\}$ at the deepest level.
- 2.5, $m=3$: correct.
  - The swaps $(12)$, $(34)$, $(13)(24)$ generate $D_4$, which acts transitively on the positions and preserves the relation property, the point set and the levels. So $q=4$ may be assumed.
  - The only solutions of $x_1+x_2-x_3\equiv0$ on $O^\circ$ are $(49,49,98)$ and $(159,159,49)$.
  - $p_4=\varphi^J(2x_1-x_3)$ by affinity, giving $\varphi^J(e_1)$ and $\varphi^J(e_4)$.
  - I checked all four choices of the odd position $q$ directly (r1, F5(iv), every $T$ of size 3).
- 2.6, $m=4$: correct. $\sum\varepsilon_ix_i=0$ exactly, by 1.1(B). Injectivity keeps the multisets distinct, and F4 then applies.
- 2.7: the cases are exhaustive ($T\ne\emptyset$, $m\in\{1,2,3,4\}$). No distinctness or ordering assumption is hidden; positions, not points, are counted.
- The argument applies verbatim to $I_K$ by 0.3.

**Step 3.**
- 3.1–3.2: correct.
- 3.3: correct. Distinct copies share at most 2 points, so no edge lies in two copies.
- 3.4: correct. For linearity between copies $J$ and $J+1$, both common points would force $\{0,269\}\subseteq e'$, and no edge contains both.
- Saturation: $9(K+1)=n-2$ middles, which are exactly the non-extreme points.

**Step 4 (the (4,5)-property).** The deduction is rigorous.
- 4.1: two disjoint equal-length pairs would give a relation on four distinct points. Two equal-length pairs sharing a point give a 3-AP with that point as middle.
- 4.2: three equal-length pairs would pairwise intersect, so they form a star or a triangle. Both are impossible.
- 4.3: $c_1+2c_2=6$ and $c_1+c_2\le4$ give $c_2\ge2$. Two different 3-APs inside a 4-set share 2 points, which contradicts linearity.
- So "no relation on 4 distinct points + linear AP hypergraph ⟹ (4,5)" holds for every finite real set. I tested both directions numerically on about 48,000 sets (r6).

**Step 5.**
- 5.1: correct.
- 5.2: correct. Every edge lies in a single copy.
- 5.3: correct. The consistency $b(U_j)=a(U_{j+1})$ holds because the shared points are literally equal. The map $T\mapsto(U_j)$ is a bijection onto consistent tuples, and $|T|=|U_0|+\sum_{j\ge1}(|U_j|-|a(U_j)|)$ follows from 1.5(iii).
- 5.4: the recursion is correct. All 16 entries are finite, since every subset of $\{0,101,119,269\}$ is admissible; only $e_7$ meets this set twice.
- 5.5: the table, M and $R_0$ are correct, and $R_0\otimes M=(11,12,12,12)=R_0+5$. Translation-equivariance gives $R_K=R_0+5K$.
- 5.6: I re-did all six hand transversal arguments (a), (b), (c), (c′), (d), (d′). The edge lists, degrees, the disjoint triples $e_1,e_6,e_7$ and $e_4,e_5,e_7$, and every branch are correct. The resulting bounds give exactly $M\le M^+$ and $R_0\le R_0^+$, and monotonicity of max-plus multiplication yields $h\le7+5K$ without any computer table.

**Step 6.** $U^*$ is admissible (checked edge by edge) and $a=b=(1,1)$. The constant tuple is consistent, so $T_K$ is Sidon by 5.2–5.3, for every $K$, by proof. It is also 3-AP-free for every $K$: a 3-AP in $T_K$ is some $\varphi^J(e)$ by 3.2, which forces $e\subseteq U^*$, a contradiction. $|T_K|=7+5K$.

**Step 7.**
- $(7+5K)/(11+9K)=5/9+8/(9(11+9K))$, strictly decreasing.
- The ratio is below $4/7$ iff $K\ge6$. $K=5$ gives exactly $4/7$, and $K=6$ gives $37/65$, with $259<260$.
- 7.3 and 7.4 are correct.

**Step 8.** 8.1–8.3 describe the page's argument, the agent's README §5 (Lemmas 1–2 there; I checked the headings) and the reader's sketch accurately. The reader's "9 inner points" are the non-anchor points, and the reader's three statements are the table facts.

**Not-claimed / scope.** There is no claim about the lower bound $9/17$ or about $c_*=5/9$. The phrase "I11 would give only $c_*\ge6/11$" in the sanity checks is a conditional remark about a [conjecture], not a claim. The sanity-check numbers are right:
- $\tau=4+4K$;
- Henning–Yeo slack $14+4K$;
- $D=20+4K$;
- maximum degree 4 at $\varphi^J(49)$, and degree 3 at the shared points.

## Checks performed (commands and outputs)

All of these are my own code in experiments/referee/L015-round1/. I used exact `int`/`Fraction`, and the only libraries were ortools and pysat. Everything ran under `nice -n 10 timeout …`, one process at a time. `run_all.sh` reruns everything.

1. `python3 -I r1_facts_O.py > r1_facts_O.log`: **SUMMARY: 0 failures** (49 PASS).
   - F1: primality by trial division. F3: the 269-adic valuations of $y(x)$ are 0 on $O^\circ$ and 1 at 0 and 269.
   - F4: by enumerating all ordered quadruples in $O^4$ (not by grouping sums): 36 ordered relations in 9 classes, all of the form $(u,u,v,w)$, with point sets exactly $e_1..e_9$. The repeated sums are exactly as listed in 0.4; the middles are $O^\circ$; the edges are linear and none contains both 0 and 269. The literal (4,5) test on $O$ gives min 5.
   - F5: over every position subset $T$ with $|T|\le3$. F6: for $d\le30$.
   - Table: Sidon-by-differences equals $E(O)$-freeness on all 2048 subsets, and there are 831 Sidon subsets. `best = [[5,6,6,6],[5,6,6,6],[5,6,6,6],[6,7,7,7]]`, `M = [[5,6,6,6],[4,5,5,5],[4,5,5,5],[4,5,5,5]]`, `R0 = [6,7,7,7]`, `R0 (x) M = [11,12,12,12]`.
   - 5.6: the $\tau_W$ values are 4, 3, 4, 4, 3, 3 for (a), (b), (c), (c′), (d), (d′), each equal to $|W|-$(max admissible). The edge lists and degrees are as stated. $U^*$ is OK.
2. `python3 -I r2_family.py > r2_family.log`: **SUMMARY: 0 failures**.
   - Theorem 1(a) for $K\le40$, from Fractions: point count, intersections, no triple coincidences. $I_K$ is integral and equals the 1.6 recursion for $K\le40$.
   - C003: JSON integers, 65 distinct, `set == 269^6 S_6` exactly. The stored witness is Sidon of size 37, and claimed_h is 37.
   - Census for every $K\le20$: e.g. `K=20 n=191 sum-relations=189 (non-AP 0) diff-coincidences=189 (4-point 0) APs==pred:True linear:True`. Every sum class and every difference class has size at most 2.
   - $T_K$ for every $K\le30$: a subset of $S_K$, size $7+5K$, Sidon by sums, no 3-AP.
   - Literal (4,5) for $K=0..8$, e.g. `K=6 n=65: all 677040 4-subsets have >= 5 distinct distances (min 5; histogram {5: 3906, 6: 673134})` and `K=8 n=83: all 1837620 … min 5`. The count of 5-distance 4-sets equals $9(K+1)(n-3)$ exactly, as Steps 2–4 predict: each such set contains exactly one AP.
3. `python3 -I r3_h.py 20 3 > r3_h.log`: **SUMMARY: 0 failures**.
   - The forbidden sets are built from the Sidon definition: point sets of all pairs of distinct pairs with equal sums. Nothing assumes AP structure, and the sets found all have size 3.
   - Method A, an exact frontier DP with a generic BFS vertex order (max frontier 7): `h = 7+5K` for every $K=0..20$, e.g. `K=6 n=65 … h=37`, `K=8 n=83 … h=47`, `K=20 n=191 … h=107`.
   - Method C, literal DFS over all Sidon subsets: $K=0$ gives h=7 (831 Sidon subsets); $K=1$ gives h=12 (177,885 Sidon subsets).
   - Method B, CP-SAT with 1 worker: OPTIMAL with bound equal to value for $K\le3$. A first run, stopped by me at $K=4$ because single-worker CP-SAT was slow, is kept as r3_h_first_run_stopped.log.
   - Control: the DP agrees with brute force on 300 random integer sets (both vertex orders).
4. `python3 -I r4_sat.py 0 … 20 > r4_sat.log`: **ALL OK**. CaDiCaL 1.9.5 with a totalizer encoding: $\ge7+5K$ is SAT (the model is re-checked Sidon by definition) and $\ge8+5K$ is UNSAT, for every $K=0..20$. For example, `K=6 n=65: >=37 SAT … >=38 UNSAT`, and `K=8 n=83: >=47 SAT … >=48 UNSAT`.
5. `python3 -I r6_lemma_tests.py > r6_lemma_tests.log`: **SUMMARY: 0 failures**. This tests the general lemmas the proof uses.
   - Step 4's equivalence ((4,5) ⟺ no 4-point relation and linear AP hypergraph), on:
     - $A_{\rm base}$, $O$, Fibonacci $F_3..F_{20}$, and $\{1,2,3,5,…\}$ (a negative case);
     - all 7 sets of data/small_records.json;
     - all 27,316 induced subsets of $A_{\rm base}$ and of the three 12-point sets;
     - 20,000 random integer sets (11,086 of them not (4,5)), so both directions are tested;
     - 60 gluings $A_{\rm base}\cup(qO+t)$ with generic and integer $q$;
     - 750 census sets from data/census_n14_m12_classes and data/ext15_sets.
   - Step 5.1 ($h=\alpha_{AP}$ for weak Sidon sets), by brute force on 143 sets, including $A_{\rm base}$ ($h=8$) and $O$ ($h=7$).
   - Step 7 ratios exactly, for $K\le100$.
6. Prover scripts re-run from a copy (experiments/referee/L015-round1/prover_rerun/, `python3 -I -B`, with v7's sys.path pointed at the copy so that experiments/prover/L015 is untouched). The outputs of v1, v2, v5, v6 and v7 are byte-identical to the prover's, and v3 and v4 are identical up to timings, ending `ALL FACTS OK`, `ALL TRANSFER CHECKS OK`, `ALL FAMILY CHECKS OK`, `ALL h CHECKS OK`, `ALL WITNESS CHECKS OK`, `ALL COMPARISONS AGREE`, `ALL CONTROLS OK`. I also read the code of v1–v5 and v7. It does what C1–C7 say, except for the labels in Problems 2–4 below.
7. Provenance.
   - I compared the certificate with kb/literature/sources/aday_757_reader_5_9/ (the day page and the problem page). The quotations are accurate: submission 7bkzb8 of 17 Oct, page of 19 Oct, PARTIAL, "Unreviewed by humans", the "Whose." sentence, "none of the submitter's code; there was none", and the verification-folder URL.
   - I fetched https://erdosproblemaday.com/submission/7bkzb8 (HTTP 200, 2026-10-20 about 20:12Z, sha256 0a6ea5d4…827e). I kept it as untrusted text, extracted with tags stripped and nothing executed, in experiments/referee/L015-round1/provenance_submission_7bkzb8.txt. It contains the facts listed in Problem 1.
   - GitHub (the site's verification folder) is not reachable from this session: HTTP 403 through the proxy, and gh API access is not enabled. So I could not re-check the "HTTP 404" statement. It is non-load-bearing.
8. Not done by me: a rerun of `judge/judge.py` on C003. When I checked at 19:55 UTC, two identical judge runs on that file were already in progress (from the C003 referee rounds), on a machine at load about 9 with 4 cores. The logged run took 59 minutes, and the task limits me to one process. The judge verdict is not used in the proof, only in Corollary 3. I verified everything the judge checks independently: C003 is exactly $I_6$ and parses as integers with no duplicates, the literal (4,5) test passes on all 677,040 4-subsets, $h=37$ by DP and by SAT ($\ge38$ UNSAT), claimed_h is 37 with a valid witness, and $37/65<4/7$ in exact Fractions. I also read experiments/20261020-1730-reader-5-9/claim_K6.log, which contains the quoted `JUDGE: PASS NEW-RECORD C003-reader-5-9-K6 n=65 h=37 ratio=37/65` line.

## Problems found (in order of severity; none affects the mathematics)

1. **Provenance is incomplete (minor; fix).** The submission page https://erdosproblemaday.com/submission/7bkzb8 adds facts that the certificate and kb/literature/sources/aday_757_reader_5_9/ do not record:
   - the site's own verdict label "VERIFIED" (its review, dated 2026-10-19), with the disclaimer "Reviewed by Claude with Patrick White — an AI and a regular dude, not mathematicians. The verdict says what was checked; it is not community acceptance";
   - the line "Tools, as declared by the submitter: Opus 5.5 found (and independently refereed) the bound. GPT Sol 6.1 also independently checked it."

   The attribution "anonymous reader's" recurs throughout the certificate, so the submitter's declared AI-tool origin should be quoted verbatim in the Provenance section and in the Origin paragraph, and the submission page should be saved next to the day page. A referee extract is in my scratch folder.

   The section also does not say what the site checked. It only says these checks were "not ours and were not used". Add one sentence listing them:
   - the literal 4-subset test for $K\le12$;
   - the relation census of $S_{12}$;
   - CP-SAT and CaDiCaL for $K\le8$;
   - a hostile-referee pass that found four gaps, re-ran the census to depth 150 and rebuilt the transfer matrix to depth 200;
   - a novelty search as of 19 Oct.

   All other provenance statements check out. The certificate correctly claims no priority and no novelty, and it correctly says what it adds.
2. **C7 mislabel (minor; fix).** The certificate's C7 paragraph, the README table and the v7_controls.py docstring and output say the generic solver gives "h = … 5 for {1,…,9}". The number computed is $\alpha$ of the 3-AP hypergraph ($=r_3(9)=5$). Since $\{1,\dots,9\}$ is not weak Sidon, its largest Sidon subset has 4 points (I checked by brute force), so "h" is wrong there. Reword as "$\alpha_{AP}(\{1..9\})=5$ (not $h$; that set is not weak Sidon)". This is a non-load-bearing control.
3. **C4(b) description (minor; fix).** v4_h.py(b) computes $\alpha$ of the AP hypergraph (edges via `ap_edges`, midpoints), not $h$ from the Sidon definition. The certificate says "$h(S_K)=7+5K$ for every $K=0,\dots,20$". The identification $\alpha=h$ uses Theorem 1(b)/5.1, or weak-Sidonness, which C3 checks only for the $K$ in its list, and that list omits 13, 14 and 16–19. Say "$\alpha(H_{AP}(S_K))=7+5K$ (= $h$ by 5.1)". My r3 and r4 compute $h$ from the full Sidon definition for all $K\le20$, so nothing is missing in substance.
4. **Stale step numbers in script comments (cosmetic; fix for traceability):**
   - v2_transfer.py says "Step 4" for the transfer matrix and the upper-bound inequalities; they are Steps 5.4–5.6.
   - v1_facts_O.py says "Steps 1-3"; the facts are used in Steps 1–5.
   - v3_family.py says "(Step 3)" for the literal 4-subset test; that is Step 4.
   - v5_witness.py says "(Step 5)" for $T_K$; that is Step 6.
5. **Falsifier section outdated (informational).** The section says "No separate falsifier run", which was true at submission. A falsifier folder now exists (experiments/falsify/l015-reader-family/, launched after submission per commit c3e8f84). I did not read it. Update the section when it reports.

No GAP, no missing case, no off-by-one, no circularity, no use of a [community] fact as published, and no confusion of weak Sidon with (4,5) was found. The record statement (Corollary 3) and the integer set C003 are correct.

## Independence statement

All referee computations (r1–r4 and r6) were written from scratch in this round. They import no code from experiments/prover/L015, experiments/20261020-1730-reader-5-9, e757/, judge/ or any other referee folder, and use only ortools and pysat as libraries. They read the C003 JSON and data/*.json(.gz) only as data. The methods are different from the prover's:
- F4 by ordered quadruples rather than sum grouping;
- the table by the difference definition of Sidon;
- the census also by differences;
- $h$ by a frontier DP and by SAT on the Sidon-definition conflict sets, against the prover's AP-hypergraph branch-and-bound;
- CP-SAT and literal enumeration as further checks.

I read the prover's scripts only to audit them, and re-ran copies in prover_rerun/. I did not read the other referees' C003 reviews, the scout review of L015 or the falsifier folder. Every file I wrote is in experiments/referee/L015-round1/, apart from this review.
