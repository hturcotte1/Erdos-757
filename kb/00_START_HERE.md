# START HERE: Erdős Problem #757

This is the canonical summary. If another file disagrees with this one, this one wins (it includes the corrections found on 13 Oct 2026 and the status update of 15 Oct 2026; the results of the autonomous run are in results/FINAL_REPORT.md and results/LEDGER.md).

Tags used everywhere in this repo:
- **[published]** refereed paper or arXiv preprint.
- **[community]** unrefereed GitHub or forum material.
- **[verified-here]** exact computation reproduced by a test in `tests/` or by the experiment folder named in the Source or Check column of `kb/known_results.md` (`tests/test_known_facts.py` pins only K3, K7, K11, K12, K17-K24 and K29; some rows also carry a referee-reviewed certificate, L001-L015: L007-L015 each ACCEPTED by three referees (L015 after a first round ACCEPT WITH FIXES), L005 and L006 by two referees after a NEEDS-WORK round, L001-L004 by a final ACCEPT after 4, 3, 3 and 1 rounds respectively, see results/LEDGER.md; the 5/9 construction behind C003 (K59, judged, referee ACCEPT x2) and L015 (K60) is a COMMUNITY construction, an anonymous reader's posted on Erdős Problem a Day on 19 Oct 2026, verified here and not discovered here).
- **[derived-here]** short argument from published theorems; re-check before relying on it.
- **[heuristic]**, **[conjecture]**, **[refuted]**.

## 1. The problem

- A finite set $A\subset\mathbb R$ is a **(4,5)-set** if every 4 distinct points determine at least 5 distinct absolute differences. Equivalently, $|B-B|\ge 11$ for every 4-subset $B$.
- $S$ is **Sidon** if all sums $x+y$ with $x\le y$ in $S$ are distinct. Equivalently, all positive differences in $S$ are distinct.
- $h(A)$ is the size of the largest Sidon subset of $A$.
- $f(n)=\min h(A)$ over $n$-point (4,5)-sets.
- $c_*=\lim f(n)/n=\inf_n f(n)/n$. The limit exists by Ma–Tang Thm 1.5 (subadditivity plus Fekete).

**Status.** $\tfrac{9}{17}\le c_*\le\tfrac47$, i.e. $0.52941\le c_*\le 0.57143$ [published: Ma–Tang, arXiv:2602.23282v2, 6 Mar 2026]. The problem is **open**, and the erdosproblems.com page (last edited 10 Apr 2026) lists exactly these bounds. **Update 2026-10-20 [community, verified-here].** The upper bound has been beaten by a construction that is not ours: an anonymous reader's self-similar family posted on Erdős Problem a Day on 19 Oct 2026 ('unreviewed by humans' there). Its 65-point member has $h=37$, so $c_*\le37/65=0.56923<4/7$ (claim C003: frozen judge PASS NEW-RECORD, two independent referee ACCEPTs; K59), and the whole family gives $c_*\le5/9=0.5556$ (certificate L015, K60: an independent proof for every depth, ACCEPTED by three referees). This project's own addition (2026-10-21): the two-point extension of Lemma E at the universal minimum of $S_5$ and $S_6$ gives smaller record sets, 58 points with $h=33$ ($33/58$) and 67 points with $h=38$ ($38/67$), both judged and accepted by two referees (K62, K63); the limit $5/9$ is unchanged. The lower bound $9/17$ is untouched.

**Autonomous run, 2026-10-13/16, the 48-hour extension 2026-10-17/18 and the resumption 2026-10-20.** No improvement of either bound was found by this project's own constructions or proofs; the improvement recorded on 2026-10-20 (K59, L015) is a community construction verified here (see Status above). The first 72 hours produced exact small-case results (section 5), three referee-accepted census certificates (L002 to L004), three extension certificates (L001, L005, L006), the structural lemmas K30, K31 [verified-here] and K44 [derived-here], the K47 structural census of the 2,910 saturated extremal 14-point classes and the extremal-subset counts K49 [verified-here], and the extension lemmas E, U, Δ, Δ′ of kb/notes/extension_lemmas.md [derived-here]. The extension found the inequality I11: $11\tau\le3n+2m$ (kb/notes/i11_conjecture.md; [conjecture] in general, tight on $A_{\rm base}$) and proved it on the abstract class for $n\le22$ by a window-cell induction (certificates L007–L011), giving: no non-saturated extremal 14-point set (K51, Q11 closed), $f(16)=10$ (K52), $f(18)=11$ (K53), $f(20)=12$ (K54) [verified-here, three referees each], $f(22)=13$ (K55) [verified-here, three referees each], hence no (4,5)-set with at most 22 points beats $4/7$; and, at the first I11-allowed record cell $(23,21,10)$, that a 23-point record would have all AP-degrees $\le3$ (L012, K56 [verified-here], three referees; the degree-3 case is Q14). The induction was then extended to $n\le26$ (certificate L013, K57 [verified-here], three referees); the first size it cannot pass without new cell lists is $n=27$ (Remark 5 of L013). Finally the degree-3 case of $(23,21,10)$ was decided: it is empty, so $f(23)=14$ and no (4,5)-set with at most 24 points beats $4/7$ (certificate L014, K58 [verified-here], three referees, 2026-10-20; Q14 closed); the first size at which a record is not excluded is $n=25$. Finally L016 (K61, three referees, 2026-10-21) carried I11 to $n=27$, giving $f(27)=16$ and no 27-point record. See results/FINAL_REPORT.md section 7 (the extension) and section 8 (the reader's 5/9 family: a community construction verified here).

**Invariances.**
- We may assume $A\subset\mathbb Z$.
- Every condition in the problem is a relation $a_1+a_2=a_3+a_4$, since $|x-y|=|z-w|$ iff $x+w=y+z$ or $x+z=y+w$. So the problem is invariant under **Freiman 2-isomorphisms**, and constructions may be built in $\mathbb Z^d$ and projected generically [derived-here].

## 2. The reduction every known proof uses

Let $H(A)$ be the 3-uniform hypergraph whose edges are the 3-term APs in $A$. For a (4,5)-set [published, Ma–Tang §2, Gyárfás–Lehel 1995]:

1. $A$ is weak Sidon: the sums $x+y$ with $x<y$ are distinct.
2. $h(A)=\alpha(H)=n-\tau(H)$. Sidon subsets are exactly the 3-AP-free subsets.
3. The midpoint map is injective and never hits $\min A$ or $\max A$. So $e(S)\le|S|-2$ for every $S\subseteq A$ with $|S|\ge2$.
4. $H$ is linear: two APs share at most one point.
5. $H$ contains no $F_7=\{012,034,056,135,246\}$, which is AG(2,3) minus two points.
6. (Monotone midpoints, K30 [verified-here].) If $(i,j,k)$ and $(i',j',k')$ are APs with $i\le i'$, $k\le k'$ and $(i,k)\ne(i',k')$ in rank order, then $j<j'$.
7. (No medial triangle, K31 [verified-here].) Three APs $\{a,b,c\},\{a,p,e\},\{c,q,e\}$ with midpoints $b,p,q$ never occur in a (4,5)-set (they force $x_a+x_q=x_b+x_p$).

**Lower bound 9/17.**
- Henning–Yeo (Graphs Combin. 37 (2021) 867–890): if $H$ is linear and $F_7$-free, then $17\tau\le 5n+3m$.
- Combined with $m\le n-2$ this gives $h\ge(9n+6)/17$.

**Upper bound 4/7.**
- $A_{\rm base}=\{0,136,200,243,246,249,272,286,298,323,400,528,596,1056\}$ has $h=8$ [published; verified-here].
- Gluing $C=A\cup(qB+t)$, with $q$ generic and $t$ large, gives $h(C)\le h(A)+h(B)$ (Ma–Tang Lemma 3.6). So one finite example bounds $c_*$.
- **$q$ must avoid every ratio $(a-a')/(b-b')$.** Integer scales often create parallelograms, which `judge/judge.py` rejects.
- **Update 2026-10-20 [community, verified-here]: 4/7 is no longer the best upper bound known to this project, but the improvement is NOT this project's.** An anonymous reader's self-similar family $S_K=O\cup\varphi(O)\cup\dots\cup\varphi^K(O)$ ($O$ an 11-point set, $\varphi(x)=101+18x/269$; Erdős Problem a Day, 19 Oct 2026, 'unreviewed by humans' there) contains a 65-point (4,5)-set with $h=37$ (K59) and gives $c_*\le5/9$ (K60). This project rebuilt it exactly, judged it, had it refereed and proved the family bound independently (L015); it did not find it. The bullets above describe only the published route (A_base and gluing).

## 3. The excess potential: one number for both directions [derived-here]

Define $D(A):=17\,h(A)-9|A|$. Then:

- $D(A)=\delta(A)+3\,(n-m)$, where:
  - $\delta=5n+3m-17\tau\ge0$ is the Henning–Yeo slack;
  - $n-m\ge2$ is the number of points that are **not** midpoints.

  Hence $D\ge 6$.
- $c_*=\tfrac{9}{17}+\tfrac{1}{17}\inf_A D(A)/|A|$. $D$ is subadditive under gluing.
- **Values on the record sets:**
  - $A_{\rm base}$: $n=14$, $m=12$, $\tau=6$, $\delta=4$, $D=10$, so $D/n=5/7$, which is exactly the 4/7 ratio.
  - The 12-point sets: $D=11$.
  - Every one of the 54,243 extremal 12-point classes has $m=10$, $\delta=5$, $D=11$ (K41); every one of the 2,910 saturated extremal 14-point classes has $m=12$, $\delta=4$, $D=10$ (K45) [derived-here from the counts].
- **The two directions in terms of $D$:**
  - **Beat 4/7** ⇔ find $A$ with $D(A)/|A|<5/7$. That requires almost every point to be a midpoint AND small Henning–Yeo slack.
  - **Beat 9/17** ⇔ prove $D(A)\ge\varepsilon|A|-C$. Realizable hypergraphs would have to be "far from Henning–Yeo-tight on average".

## 4. Where a better upper bound can and cannot live [derived-here]

Beating 4/7 at size $n$ needs $h\le\lceil 4n/7\rceil-1$, i.e. $\tau=n-h$ with $17\tau\le5n+3m$ and $m\le n-2$.

- **Impossible** for every $n\le15$ and for $n\in\{17,19,21,24,26,28\}$.
- **Possible only with these parameters:**

| $n$ | $h$ needed | $m$ needed | note |
|---|---|---|---|
| 16 | 9 | $\ge13$ (max 14) | |
| 18 | 10 | $=16$ | fully saturated and Henning–Yeo-tight |
| 20 | 11 | $=18$ | saturated |
| 22 | 12 | $=20$ | saturated |
| 23 | 13 | $\ge19$ | |
| 25 | 14 | $\ge21$ | |
| 27 | 15 | $\ge23$ | |
| 29 | 16 | $\ge26$ | |
| 30 | 17 | $\ge24$ | |

The full table is printed by `python3 -m e757.fn_bounds`.

Status of the feasible sizes: $n=16$ CLOSED, no record (L008, K52 [verified-here]); $n=18$ CLOSED, no record (L009, K53 [verified-here]); $n=20$ CLOSED, no record (L010, K54 [verified-here]); $n=22$ CLOSED, no record (L011, K55 [verified-here]); $n=23$ CLOSED, no record (L014, K58 [verified-here]); $n=27$ CLOSED, no record (L016, K61 [verified-here]); so for $n\le30$ a record is not excluded only at $n=25$ (cell $(25,23,11)$, I11-tight), $29$ and $30$ (this concerns the small sizes only and is not a claim that no record exists: a 65-point (4,5)-set with $h=37$, so $37/65<4/7$, is known, namely claim C003 of K59 [community, verified-here], the depth-6 member of the self-similar family behind $c_*\le5/9$ (K60); it is an anonymous reader's construction posted on Erdős Problem a Day on 19 Oct 2026, not found by this project, which rebuilt, judged and refereed it; of the rows of the table above, $n=16,18,20,22,23$ are now closed, see K52–K55 and K58); [heuristic]: $n=18,20,22,23,25$ searched in witness mode for 1200 to 3600 s each, UNKNOWN (D18). Degree bound in Gyárfás–Lehel-tight saturated hypergraphs (K44): $\deg\le5$ for $n\in\{12,14,16\}$, $\deg\le4$ for $n\in\{18,20,22\}$ [derived-here].

## 5. Small values of $f(n)$ [derived-here]

These follow from the Henning–Yeo lower bound, the known sets, monotonicity, and gluing.

- **Exact for every $n\le18$ and for $n=19,20,21,22,23,24,26,28$:** $f(1),\dots,f(15)=1,2,2,3,4,4,5,5,6,6,7,7,8,8,9$, $f(16)=10$ (certificate L008, K52), $f(17)=10$, $f(18)=11$ (L009, K53), $f(19)=11$ (claim C008, K70, 2026-10-27: a 19-point (4,5)-set with $h=11$, judge PASS NO-IMPROVEMENT, referee ACCEPT, scout CLEAR; lower bound from K8; [verified-here] for the set and $h$, [published] for the lower bound, [derived-here] for the value; $11/19>4/7$, not a record), $f(20)=12$ (L010, K54), $f(21)=12$ (claim C006, K66, 2026-10-27: a 21-point (4,5)-set with $h=12$, judge PASS NO-IMPROVEMENT, referee ACCEPT, scout CLEAR; lower bound from K8 [verified-here] for the set and $h$, [derived-here] for the value; $12/21=4/7$ exactly, not a record), $f(22)=13$ (L011, K55) [verified-here, 2026-10-17] and $f(23)=14$ (L014, K58; Theorem 1 [verified-here], the value [derived-here] from it, 2026-10-20) and $f(27)=16$ (L016, K61, 2026-10-21; I11 on $C$ for $n\le27$); hence no (4,5)-set with at most 24 points beats $4/7$ (for $n=24$ by the Henning–Yeo bound $h\ge14$, K8; L014 Corollary 3); also $f(24)=14$, $f(26)=15$, $f(28)=16$. The sets attaining $f(8)=5$ and $f(10)=6$ were found on 13 Oct 2026 by `e757/ordered_search.py` [verified-here]; all small extremal sets are in `data/small_records.json`. Pattern: $f(n)=\lceil n/2\rceil+1$ for $6\le n\le15$, $n=17$, $n=19$ and $n=21$. The Henning–Yeo bound $n-\lfloor(8n-6)/17\rfloor$ equals $\lceil n/2\rceil+1$ for every $6\le n\le23$ (K35). So within $6\le n\le23$ the exact $f(n)$ equals the Henning–Yeo bound for $n\le15$, $n=17$, $n=19$ (K70) and $n=21$ (K66). At $n=16,18,20,22$ it exceeds the bound by one, with $f(n)=\lceil n/2\rceil+2$ (L008–L011, K52–K55). $f(23)=14=\lceil23/2\rceil+2$ as well (L014). f(19) = 11 (C008, K70, 2026-10-27) and f(21) = 12 (C006, K66, 2026-10-27) are settled. [verified-here].
- **Open:**
  - **The cases $n=16,18,20,22$ are settled, not open:** $f(16)=10$ (L008, K52), $f(18)=11$ (L009, K53), $f(20)=12$ (L010, K54), $f(22)=13$ (L011, K55) [verified-here, computer-assisted, three referees each]; hence no (4,5)-set with at most 22 points beats 4/7. The direct solver attempts at $n=16$ (D15, D16, D24) never terminated; the decisions came from the inequality $11\tau\le3n+2m$ (kb/notes/i11_conjecture.md; [conjecture] for general $n$), verified on the abstract class $C$ (linear, $F_7$-free, $e(S)\le|S|-2$ for every vertex set $S$ with $|S|\ge2$; L007) for $n\le22$ by the window-cell induction of L007–L011;
  - $f(19)=11$ (C008, K70) and $f(21)=12$ (C006, K66) are settled, not open; $f(23)=14$ is settled (L014, K58: the degree-3 case of $(23,21,10)$ is empty; Q14 closed), so the first open record size is $n=25$ ($f(25)\in\{14,15\}$); $f(27)=16$ is settled too (L016, K61), and for $n\le30$ only $n=25,29,30$ remain.
- **Extremal-set counts [verified-here].** Saturated extremal affine classes for $n=6,\dots,14$: 1, 4, 66, 1262, 6644, 466961, 54243, (n=13 open: Q12, D22), 2910 (K41, K43, K45; certificates L002, L003, L004; for the saturated $n=14$ count (L004) the referee realized all 205,529 enumerated patterns independently but re-checked the completeness of the enumeration only on 28% of the prefixes (719 of 2,537; 8.8% of the DFS nodes) plus consistency checks, not by a full second enumeration; structure of the 2,910 classes: K47). For $4\le n\le11$ there are also non-saturated extremal families (infinitely many classes); $n=12$ is the smallest $n\ge4$ with finitely many. No non-saturated ($m=11$) extremal 14-point set exists (certificate L007, K51, referee ACCEPT x3; Q11 closed on 2026-10-17), so 2,910 is the total number of extremal 14-point classes provided the L004 enumeration is complete (that completeness was re-checked only by sampling, see above; L007 Corollary 3 states the same caveat). Non-saturated extremal sets also exist at $n=15$, with 11 and with 12 APs (a saturated 15-point set would have 13) (K50; judged examples C001, C002) [verified-here].

## 6. Structure of the known record sets [verified-here]

| Set | $n$ | $m$ | $h$ | $\tau$ | HY slack | $D$ | Rigid? |
|---|---|---|---|---|---|---|---|
| $A_{\rm base}$ (Ma–Tang) | 14 | 12 | 8 | 6 | 4 | 10 | yes |
| 12-pt #1 (omega #9804) | 12 | 10 | 7 | 5 | 5 | 11 | yes |
| 12-pt #2 (omega #9804) | 12 | 10 | 7 | 5 | 5 | 11 | yes |

- **Midpoint-saturated.** Every non-extreme point is a midpoint ($m=n-2$).
- **Affinely rigid.** The AP equations have rank $n-2$. So the labeled AP hypergraph determines the set up to $x\mapsto qx+t$, and `e757.saturated` rebuilds $A_{\rm base}$ from its hypergraph alone. Not every extremal set is saturated: for $n\le11$ there are positive-dimensional families (K43; the $n=8$ record set is one), but all 54,243 extremal 12-point classes and all 2,910 saturated 14-point classes are rigid (K41, K45).
- **The record 12-point sets are a small sample**: there are exactly 54,243 affine classes of 12-point (4,5)-sets with $h=7$ (K41), including the two omega sets (which share an incidence pattern but are not affinely equivalent) and the third set $\{0,269,385,467,501,511,521,523,535,538,549,575\}$ [verified-here].
- **More facts about $A_{\rm base}$:**
  - AP degrees: one vertex of degree 4 (the point 0), six of degree 3, seven of degree 2;
  - no cut vertex;
  - 143 maximum Sidon subsets;
  - $\tau=\lfloor106/17\rfloor$, i.e. Henning–Yeo-tight after rounding.
- **Saturated sets are discrete harmonic functions.** With $x_{\min}=0$ and $x_{\max}=1$, each $x_j$ is the probability that a random walk, jumping from $j$ to one of its two AP endpoints, reaches the max before the min.
- **The Fibonacci example.** $\{F_3,F_4,\dots\}=\{2,3,5,8,\dots\}$ has $h=3n/5+O(1)$. Note that $\{1,2,3,5\}$ is NOT a (4,5)-set, so do not start at 1.
- **Random saturated midpoint maps are almost never linear** (2 in 3000 at $n=16$). So generate maps edge by edge while keeping linearity.

## 7. Settled: do not redo

See `kb/dead_ends.md`. The highlights:
- Chvátal–McDiarmid gives only 1/2.
- Henning–Yeo gives 9/17.
- Gluing.
- Fibonacci gives 3/5.
- Periodic chain constructions have independence density $\ge3/5$ in every case tested, so none of the tested ones beats 4/7 (D5, K22). Tested range, linear chains only: single-class with $a\ne b$, $a+b\le11$; 2-class with span $\le8$; 3-class with span $\le6$ (span $=\max_c(a_c+b_c)$; non-linear chains are not valid (4,5)-set hypergraphs, and some of them have density $1/2$). This is not a theorem [verified-here for the tested range; `test_chain_densities` covers only single-class $a+b\le8$].
- No 2-point extension of $A_{\rm base}$ beats 4/7 [verified-here] (certificate L001, K13); more generally no 16-point (4,5)-set with $h\le9$ contains any saturated extremal 14-point set [verified-here] (certificate L005, K46): a 16-point record, if one existed, could contain no extremal 14-point subset at all (L005 with L007/K51, which shows that every extremal 14-point set is saturated). Likewise no extremal 14-point set contains an extremal 12-point set [verified-here] (certificate L006, K48): extremal 14-point sets are not two-point extensions of extremal 12-point sets. This is not a general pattern at smaller $n$ [verified-here; K49]: every saturated extremal class at $n=6..9$ and $n=11$ contains an extremal $(n-2)$-point subset, as do 6,625 of the 6,644 saturated classes at $n=10$ and 26,852 of the 54,243 classes at $n=12$ (49.5%).
- Q8 ($7\tau\le3|R|+2e_2+4e_1$; with no deleted vertex it says $h\ge4n/7$) is false for the abstract class (it would need forbidden cores with $\ge5$ edges: K38, K39, D17), and it is also false for realizable sets: the 65-point set C003 (an anonymous reader's construction posted on Erdős Problem a Day, 19 Oct 2026; verified here, not discovered here) has $h=37<4\cdot65/7$, i.e. $\tau=28$ and $7\tau=196>195=3n$ (K59) [derived-here]; so Q8 is refuted, the route "Q8 $\Rightarrow c_*=4/7$" is closed, and $c_*=4/7$ itself fails since $c_*\le5/9$ (K60, same provenance); direct SAT/CP-SAT/annealing decisions of $\alpha\le9$ at $n=16$ did not terminate within the budgets tried (at most 3.5 h per instance), even with the Henning–Yeo deletion constraints of Lemma Δ (D15, D16, D20, D24; D21 is the separate CP-SAT run on the $(14,11)$ case); witness sweeps at $n=18..25$ UNKNOWN (D18).
- $21\tau(K)\le9|R|+5e_2+12e_1$ is refuted [community].
- $F_7$ cannot be realized over $\mathbb Q$ under any midpoint labeling [verified-here; re-proves Gyárfás–Lehel].

## 8. Reading order

1. This file.
2. `kb/RESEARCH_PLAN.md`.
3. `kb/dead_ends.md`.
4. `kb/open_questions.md`.
5. `kb/known_results.md` (every fact with its source and its test).
6. `kb/notes/` (paper digests: Ma–Tang, Henning–Yeo, Gyárfás–Lehel, the omega thread, neighbouring problems) and `kb/methods/` (search engineering, proof and inequality testing).
7. `kb/literature/part2_supplement.md`: the full proof chain, hypergraph transversal theory (including the "deficiency" proof technique), and AI/computational methods.
8. `kb/literature/part1_literature_review.md`: history, neighbouring problems and bibliography, with inline corrections.
9. results/FINAL_REPORT.md and results/LEDGER.md (what the autonomous run established); kb/methods/trackL_inductive_framework.md; kb/notes/gl_tight_structure.md; kb/notes/i11_conjecture.md (the inequality I11, $11\tau\le3n+2m$: [conjecture] in general, [verified-here] on the abstract class for $n\le26$; the window-cell induction behind K51–K55 and K57, and the $n=23$ record cell (degree 4 excluded by L012, K56; the degree-3 case, Q14, closed by L014, K58); certificates results/proofs/L007–L014, each ACCEPTED by three referees (K51–K58); results/proofs/L015 (K60; ACCEPTED by three referees) is this project's independent every-depth proof of the self-similar family that an anonymous reader posted on Erdős Problem a Day on 19 Oct 2026, a [community] construction verified here, not discovered here (its $K=6$ member is the judged claim C003, K59; sources: kb/literature/sources/aday_757_reader_5_9/; rebuild: experiments/20261020-1730-reader-5-9/; falsifier: experiments/falsify/l015-reader-family); work folders experiments/prover/L007–L015 and experiments/falsify/i11-inequality); kb/notes/extension_lemmas.md (Lemmas E, U, Δ and Δ′ on two-point extensions, universal vertices, the degree bound for a 16-point record and the Henning–Yeo degree bound on which vertex pairs can be deleted to leave an extremal subset [derived-here, falsifier HOLDS-ON-DATA]; predicts the T2 outcome in K46 but is not load-bearing for L005); data/README.md (census files).
