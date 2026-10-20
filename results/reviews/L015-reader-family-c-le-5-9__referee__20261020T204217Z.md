VERDICT: ACCEPT

# Referee report, round 2: results/proofs/L015-reader-family-c-le-5-9.md (CLAIM: c* <= 5/9)

Referee: L015 round-2 referee (fresh, independent, adversarial).
- Certificate reviewed: the version of commit 1e8abf6 (2026-10-20T20:23:12Z, "round-1 editorial fixes"), sha256 6b574474…0458070.
- Scratch folder: experiments/referee/L015-round2/.
- Verdict scale: the workflow's ACCEPT / REJECT / ACCEPT WITH FIXES. ACCEPT means the same here as on the standard ACCEPT / REJECT / NEEDS-WORK scale: every step is verified and nothing has to be fixed. The five remarks under "Problems found" are optional wording suggestions. None is a gap or a factual error.
- Independence: I formed and recorded my verdict (experiments/referee/L015-round2/verdict_before_round1.txt, 2026-10-20T20:39:52Z) before reading the round-1 review, the scout review or the falsifier report.

## Summary

The certificate proves, for every depth $K\ge0$, that the anonymous reader's set $S_K=O\cup\varphi(O)\cup\dots\cup\varphi^K(O)$ (with $O=\{0,49,75,83,98,101,117,119,121,159,269\}$ and $\varphi(x)=101+\frac{18}{269}x$) is an $(11+9K)$-point (4,5)-set with $h(S_K)=7+5K$. Hence $f(11+9K)\le7+5K$ and $c_*\le\inf_K\frac{7+5K}{11+9K}=\frac59$, via K1, and also without K1 for the Formal-Conjectures supremum of admissible constants. $K=6$ (65 points, $h=37$) is the first member below $4/7$, and its integer form $269^6S_6$ is exactly the C003 set. I re-derived every step by hand: the 269-adic level lemma; the complete deepest-level case analysis mod 269 for $m=1,2,3,4$, including equal points, signs and the $D_4$ symmetry reduction; the AP hypergraph and its linearity; the (4,5) deduction; the bijection between Sidon subsets and per-copy choices; the max-plus recursion and its monotonicity; all six hand transversal bounds of 5.6; the witness $T_K$; and the limit and supremum arguments. I found no gap, no missing case, no sign error and no hidden assumption. The proof rests only on the finite facts F0–F5 about $O$ and $\varphi$; Step 2 itself uses F1 and F3–F5, and F6 is only a consistency check. I redid each hand check. It further rests on the hand inequalities of 5.6, the explicit $T_K$, and K1 [published] in 7.3. I recomputed with my own code, by methods different from the prover's: F0–F6 and the 16-entry table; the relation census by ordered-triple completion, for every $K\le20$ and for $K=25,30,40$; the literal $|B-B|$ test on every 4-subset for $K\le8$, including the exact predicted distribution of the values 11 and 13; $h(S_K)$ by SAT with two solvers for $K\le8$ ($\ge8+5K$ is UNSAT) and by an exact frontier DP built from the Sidon definition for $K\le20$; $T_K$ for $K\le30$; and the C003 identity. Everything agrees with the certificate. My own re-run of the frozen judge on C003 was killed by an external signal before it finished, so it gave no verdict. The verdict quoted in Corollary 3 is still confirmed by claim_K6.log and by a live judge-cache entry written by status.py, keyed by the exact SHA-256 of the file and of the frozen judge. The proof does not depend on that verdict (check 8). The Provenance section agrees with the saved day page and submission page and is complete. It includes the site's labels PARTIAL and VERIFIED, its disclaimer, "Unreviewed by humans", the submitter's declared AI tools quoted verbatim, the site's own checks, and the HTTP 404, attributed to the scout. Nothing is claimed about $9/17$ or about $c_*=5/9$. The five remarks under Problems are optional wording suggestions; none of them blocks acceptance.

## Dependencies (as checked)

- **Definitions** (kb/00_START_HERE.md §1). The certificate uses them consistently:
  - "(4,5)" means that every 4 distinct points give at least 5 distinct distances, i.e. $|B-B|\ge11$;
  - "Sidon" means that all sums $x+y$ with $x\le y$ are distinct;
  - $f(n)$ and $c_*$ are as in START_HERE.
- **K1 [published]** (Ma–Tang Thm 1.5: $c_*=\lim f(n)/n=\inf f(n)/n$). It is used only in 7.3, and with the task's own definition $c_*=\inf_nf(n)/n$ it is not needed at all.
- **The Formal-Conjectures formulation** (Step 7.4). I checked it against kb/literature/sources/formal_conjectures_757.lean:
  - `IsAdmissible c` means: for every finite $A\subset\mathbb R$ with $11\le|B-B|$ for all 4-subsets $B$, there is a Sidon $S\subseteq A$ with $c\,|A|\le|S|$. There is no $o(n)$ term and no "for large $n$".
  - So 7.4 applies verbatim. The admissible set contains $0$ (take $S=\emptyset$) and is bounded above by $5/9$, so its `sSup` is at most $5/9$.
- **Nothing else is load-bearing.**
  - Ma–Tang Lemma 2.3 (Sidon = 3-AP-free) and the AP-hypergraph structure are re-proved for $S_K$ in Steps 2, 3 and 5.1.
  - Henning–Yeo, I11, K5, K54 and L014/K58 appear only in the sanity checks. I confirmed that K58 (f(23)=14) is now [verified-here], so the sanity remark "no (4,5)-set with at most 24 points beats 4/7" is correctly sourced.
  - The judge verdict and the agent's numbers are used only in Corollary 3 / 7.5 and in C6, as the certificate says.

## Step-by-step audit (hand re-derivation)

**Step 0.**
- 0.1: correct. $B-B=\{0\}\cup\{\pm\delta\}$, so $|B-B|=1+2\cdot\#\{\text{distinct positive differences}\}$.
- 0.2: correct. Each of the four cases $p_i=p_k$ across the two sides forces the other two points to agree, so the multisets would be equal.
- 0.3: correct. An affine map with $\lambda\ne0$ preserves relations and scales all distances by $|\lambda|$.
- F0–F6 hand checks, all redone:
  - $269=3\cdot89+2=5\cdot53+4=7\cdot38+3=11\cdot24+5=13\cdot20+9$, and $17^2=289>269$;
  - $27169=101\cdot269$;
  - $251\cdot108=27108<27169<27359=251\cdot109$;
  - $y(269)=251\cdot269-27169=40350=150\cdot269$;
  - $269-O^\circ=\{220,194,186,171,168,152,150,148,110\}$, which is disjoint from $O^\circ$;
  - $x_1+x_2-x_3\in[-61,269]$;
  - the sums $\le159$ of two elements of $O^\circ$ are $98,124,132,147,150,150,158$, and only 98 lies in $O^\circ$;
  - the value 269 needs $x_1=x_2=159$ and $x_3=49$.

**Step 1.**
- 1.1: correct. $\varphi^j(x)=L+r^j(x-L)$ by induction from F2; $\varphi^J$ is affine with positive slope, which gives (A)–(D).
- Lemma 1.2: correct.
  - From $269^dy(x)=18^dy(x')$ and $\gcd(269,18)=1$ we get $269^d\mid y(x')$, and $y(x')\ne0$ because $L\notin\mathbb Z$.
  - Then $269\mid y(x')$ gives $251x'\equiv0$, so $x'\in\{0,269\}$.
  - $v_{269}(y(0))=v_{269}(y(269))=1$, so $d=1$.
- 1.3: correct. Injectivity reduces a coincidence to $x=\varphi^{j'-j}(x')$.
- 1.4: correct. No point lies in three copies, and $c-\binom c2=1$ for $c\in\{1,2\}$ gives $11(K+1)-2K$.
- 1.5: correct, (i)–(iii).
- 1.6: correct: $N_j=101\cdot269^j+18N_{j-1}$.

**Step 2 (the heart).** Correct and exhaustive.
- 2.1: the identity $\sum_i\varepsilon_i18^{j_i}269^{J-j_i}y(x_i)=0$ holds in $\mathbb Z$.
- 2.2: terms with $j_i<J$ carry the factor $269^{J-j_i}$ with $J-j_i\ge1$. Since $18^J$ and $251$ are units mod 269, this gives $(\ast)$.
- 2.3, $m=1$: impossible.
- 2.4, $m=2$: I checked all six position pairs.
  - Opposite sides give $x_i=x_k$, hence $p_i=p_k$ on both sides, which 0.2 excludes.
  - Same side: F5(ii) is stated for not-necessarily-distinct pairs. This covers $p_1=p_2$ alone at the deepest level ($2x\equiv0$) as well as $\{p_3,p_4\}$ at the deepest level.
- 2.5, $m=3$:
  - The three maps generate $D_4$, which acts transitively on the positions and preserves the relation, its point set and the levels. So "$q=4$" is a valid WLOG.
  - The residual sign pattern is $(+,+,-)$. F5(iv) gives exactly $(49,49,98)$ and $(159,159,49)$; I also checked the negated pattern.
  - $x_1=x_2$ at level $J$ forces $p_1=p_2$, and affinity (1.1(C)) gives $p_4=\varphi^J(0)$ resp. $\varphi^J(269)$.
  - In the $e_1$ case the relation comes out as $(u,u,\varphi^J(98),\varphi^J(0))$. This is the normal form after the $p_3\leftrightarrow p_4$ exchange that Theorem 1(b) explicitly allows (see remark 5 below).
- 2.6, $m=4$: $\sum\varepsilon_ix_i=0$ exactly, by 1.1(B). Injectivity keeps the multisets distinct, and F4 is then used; this includes $J=0$.
- 2.7: the four cases are exhaustive. Positions are counted, not points, and nothing assumes distinctness or an ordering.
- The finite facts cover every case:
  - $m=1$ uses F5(i);
  - $m=2$ uses F5(ii), F5(iii) and 0.2;
  - $m=3$ uses F5(iv) and 1.1(C);
  - $m=4$ uses F4 and injectivity;
  - $(\ast)$ uses F1 and F3.
- For the integer sets $I_K$, the statement transfers by 0.3, and the identity in 2.1 is already an identity over $\mathbb Z$.

**Step 3.**
- 3.1–3.2: correct. A 3-AP gives the relation $(u,u,v,w)$, and its point set is an edge by Step 2.
- 3.3: correct. Two copies share at most 2 points, so no 3-set lies in two copies, and $|H|=9(K+1)$.
- 3.4: correct. Between copies $J$ and $J+1$, two common points would force $\{0,269\}\subseteq e'$, which F4 excludes. Saturation also checks out: the $9(K+1)$ middles are exactly the points of $S_K\setminus\{0,269\}$.

**Step 4.** Rigorous.
- 4.1: two disjoint pairs of equal length would give a relation on four distinct points. Two pairs sharing a point give a 3-AP with that point as middle.
- 4.2: three pairs of equal length would pairwise intersect, hence form a star (at most two points lie at distance $\delta$ from $u$) or a triangle (the largest distance is the sum of the other two). Both are impossible.
- 4.3: $c_1+2c_2=6$ and $c_1+c_2\le4$ give $c_2\ge2$. The two classes give two distinct 3-APs inside the 4-set, since a class determines its 3-set and the 3-set determines the class. These share 2 points, which contradicts 3.4.
- The deduction uses only Theorem 1(b) and linearity, so it is valid for any finite set of reals.

**Step 5.**
- 5.1: correct.
- 5.2: correct. Every edge lies in a single copy, so $\varphi^J(e)\subseteq T$ if and only if $e\subseteq U_J$.
- 5.3: correct. Consistency holds because the shared points are literally equal. I checked the bijection proof case by case ($i=j$, $i=j\pm1$, and $|i-j|\ge2$). The size formula follows from 1.5(iii).
- 5.4: the recursion is correct. For the max-plus recursion to be well defined, all 16 state pairs must be realisable. They are: every subset of $\{0,101,119,269\}$ is admissible, since only $e_7$ meets that set twice.
- 5.5: correct. The table, $M$, $R_0$ and $R_0\otimes M=(11,12,12,12)$ are right, and translation-equivariance gives $R_K=R_0+5K$.
- 5.6: I redid all six hand arguments. The edge lists and degree lists are right, and so is every branch:
  - the disjoint triples $e_1,e_6,e_7$ in (a) and (c′);
  - the disjoint triple $e_4,e_5,e_7$ in (c);
  - the $\{49,159\}$ argument in (b);
  - the 159 argument with $e_3\cap e_5=\emptyset$ in (d);
  - the degree-$\le2$ count in (d′).

  The consequences are exactly $M\le M^+$ and $R_0\le R_0^+$. Monotonicity of max-plus multiplication then gives $h(S_K)\le7+5K$ for every $K$ without any computer table.

**Step 6.**
- $U^*$ is admissible: I checked all nine edges, and the missed points are as listed.
- $a(U^*)=b(U^*)=(1,1)$, so the constant tuple is consistent.
- Hence $T_K$ is Sidon by 5.2–5.3, with $|T_K|=7+5K$, for every $K$, by proof.

**Step 7.**
- 7.2: $\frac{7+5K}{11+9K}-\frac59=\frac{8}{9(11+9K)}$, which is positive, strictly decreasing and tends to 0.
- 7.3 and 7.4: correct (see Dependencies).
- 7.5: correct. The ratio is below $4/7$ if and only if $K>5$; $K=5$ gives exactly $4/7$, and $K=6$ gives $37/65$, with $259<260$.

**Step 8, Not-claimed, Sanity checks.**
- 8.1 quotes the day page accurately.
- 8.2: the agent's README §5 has "Lemma 1 (minimal level)" and "Lemma 2 (all relations are APs inside one copy)" via the deepest level mod 269. I checked the headings.
- 8.3 matches the submission text.
- Not-claimed (i)–(v): correct.
- Sanity numbers: all correct.
  - $\tau=4+4K$;
  - Henning–Yeo slack $14+4K$;
  - $D=20+4K$;
  - I11 slack $7+K$;
  - maximum degree 4, at $\varphi^J(49)$;
  - degree 3 at the shared points;
  - the ratios for $K\le4$: $7/11$, $3/5$, $17/29$, $11/19$, $27/47$.

## Checks performed (commands and outputs)

All of these are my own code in experiments/referee/L015-round2/. I used exact `int`/`Fraction`, with pysat as the only library. Everything ran from that folder as `nice -n 10 timeout … python3 -I <script>`, one process at a time. `bash experiments/referee/L015-round2/run_all.sh` reruns checks 1–7 in about 30 s; I ran it at the end and every line printed `ALL … OK`.

1. **`r1_facts.py > r1_facts_output.txt`**: 62 OK lines, `FAILURES: 0`, `ALL R1 FACTS OK`.
   - F0–F3 directly. F2 is checked as an identity of affine maps at two points, and also at $L$ and at test points.
   - F4 by enumerating all ordered quadruples of $O^4$, not by grouping sums: 36 ordered quadruples in 9 classes, each $(u,u,v,w)$, with point sets exactly $e_1..e_9$. A second derivation from the triples $a<u<c$ with $a+c=2u$ agrees.
   - F4's other claims: the repeated sums are exactly $98,150,166,196,202,234,238,242,318$, each twice; the middles are $O^\circ$; the edges are linear; no edge contains both 0 and 269.
   - F5(i)–(iv) over all ordered tuples with repetition, plus every hand list of 0.4.
   - F6 / Lemma 1.2 for $d\le40$: the only hits are $(0\to101)$ and $(269\to119)$, both at $d=1$.
   - The table from the Sidon definition over all 2048 subsets: the 831 Sidon subsets are exactly the $E(O)$-free subsets. `best = [[5,6,6,6],[5,6,6,6],[5,6,6,6],[6,7,7,7]]`, `M = [[5,6,6,6],[4,5,5,5],[4,5,5,5],[4,5,5,5]]`, `R0 = [6,7,7,7]`, `R0 (x) M = [11,12,12,12]`.
   - The six sets $W$ of 5.6, by brute force:

     | case | $\lvert W\rvert$ | edges | $\tau_W$ | max admissible $\lvert U\rvert$ |
     |---|---|---|---|---|
     | (a) | 11 | 9 | 4 | 7 |
     | (b) | 9 | 6 | 3 | 6 |
     | (c) | 10 | 8 | 4 | 6 |
     | (c′) | 10 | 8 | 4 | 6 |
     | (d) | 8 | 5 | 3 | 5 |
     | (d′) | 8 | 5 | 3 | 5 |

     In every case the maximum equals $|W|-\tau_W$. The degree lists of (b), (d) and (d′) are as printed in 5.6.
   - $U^*$ is Sidon with 7 points, and every subset of $\{0,101,119,269\}$ is Sidon.
2. **Relation census by point completion**, a different method from the prover's sum grouping: `r2_family.py 0 … 10` and `r2_family.py 11 … 20 25 30 40` → `ALL R2 CENSUS OK`.
   - Method: for every ordered triple $(p_1,p_2,p_3)\in I_K^3$, set $p_4=p_1+p_2-p_3$, test membership, then classify the classes $\{\{p_1,p_2\},\{p_3,p_4\}\}$.
   - $I_K$ is built twice, as Fractions scaled by $269^K$ and by the integer recursion of 1.6, and the two agree.
   - For every $K\le20$ and $K=25,30,40$:
     - $n=11+9K$;
     - the copy intersections and levels are exactly as in Step 1, and no point lies in three copies;
     - there are $36(K+1)$ ordered relation quadruples and $9(K+1)$ classes, and 0 classes on 4 points;
     - every class is $(u,u)$ vs $(v,w)$ with $v<u<w$;
     - the AP point sets equal the predicted $\{\varphi^J(e)\}$;
     - the hypergraph is linear and saturated, with maximum degree 4.
   - Examples: `K=20 n=191 … ordered_quads=756 classes=189 four_point=0 bad=0 AP_sets==pred=True` and `K=40 n=371 … ordered_quads=1476 classes=369 four_point=0`.
3. **Controls** (`r2_controls.py` → `CONTROLS OK`). The census and the 4-subset code are not vacuous:
   - planting $a+b-c$ (copies 0, 2, 3 of $S_3$) gives 37 classes, one of them on 4 points, and min $|B-B|=9$;
   - planting $2a-c$ (copies 1, 3) gives 38 classes, one on 4 points, and min 9;
   - $\{1,2,3,5\}$ gives 9, and $\{0,1,3,7\}$ gives 13.
4. **Literal (4,5) test** (`r3_45.py 0 … 8` → `ALL R3 (4,5) CHECKS OK`; 7 s). For every 4-subset I compute the set $\{a-b\}$ itself.
   - The minimum is 11 for every $K\le8$.
   - The distribution is exactly $\{11: 9(K+1)(n-3),\ 13:\text{rest}\}$. This is the sharp prediction of Steps 2–4. Each AP lies in exactly $n-3$ four-sets, and no four-set contains two APs, by linearity. Every four-set without an AP has 6 distinct distances, because there is no relation on 4 distinct points.
   - Examples: `K=6 n=65 4-subsets=677040 … {11: 3906, 13: 673134}` and `K=8 n=83 4-subsets=1837620 … {11: 6480, 13: 1831140}`.
5. **$h(S_K)$ by two exact methods** (`r4_h.py 8 20 > r4_h_output.txt` → `ALL R4 h CHECKS OK`). Both start from the Sidon definition on $I_K$: every pair of distinct pairs with equal sums gives a forbidden point set. They use no APs, no copies and no transfer matrix; all forbidden sets found have size 3.
   - (i) **SAT** through pysat, with CaDiCaL 1.9.5 and Glucose 4 and a sequential-counter cardinality constraint. For every $K\le8$ and both solvers, $\ge7+5K$ is SAT (the model is re-checked Sidon by definition) and $\ge8+5K$ is UNSAT, e.g. `K=6 … >=37 SAT … >=38 UNSAT` and `K=8 … >=47 SAT … >=48 UNSAT`.
   - (ii) **Frontier DP** (vertex elimination), $h=7+5K$ for every $K\le20$.
     - Each step keeps, for every choice pattern on the processed vertices that still lie in a constraint with an unprocessed vertex, the best count.
     - A constraint is checked exactly once, when its last vertex is processed. At that moment all its other vertices are still in the frontier, so the check is complete.
     - It is therefore exact for any vertex order. I used a maximum-cardinality-search order computed from the constraint hypergraph alone; the maximum frontier was 6, with at most 45 states.
6. **Self-test of both $h$ methods** (`r6_selftest.py` → `ALL SELFTESTS OK`), against literal brute force (all subsets, Sidon by definition):
   - 300 random integer sets with $n\le13$, many with 4-point relations: 0 mismatches;
   - $A_{\rm base}$ (8), the third 12-point record (7) and all 7 sets of data/small_records.json (5, 6, 7, 7, 8, 7, 7);
   - the Fibonacci sets $\{F_3,\dots\}$ with $n=8,\dots,16$ (6, 7, 8, 9, 10).
7. **Witnesses and C003** (`r5_witness_c003.py` → `ALL WITNESS T_K (K<=30) OK`, `ALL C003 CHECKS OK`).
   - For every $K\le30$: $T_K\subseteq S_K$, $|T_K|=7+5K$, $T_K$ is Sidon by definition, contains no 3-AP, and $T_K=U^*\cup\varphi(T_{K-1})$.
   - C003 artifact checks:
     - the JSON `set` has 65 entries, all of Python type `int` (no strings, floats or bools) and pairwise distinct;
     - `sorted(set) == 269^6·S_6` exactly;
     - `claimed_h = 37`, and the stored 37-point witness is a Sidon subset;
     - on the raw set, $h=37$ by the DP, with SAT $\ge37$ SAT and $\ge38$ UNSAT, so the claimed_h hides no larger Sidon subset;
     - the literal min $|B-B|$ is 11;
     - $h/n=37/65<4/7$ in Fractions ($259<260$).
   - $K=5$ gives exactly $4/7$, and the first $K$ below $4/7$ is 6. The formula $\frac{7+5K}{11+9K}-\frac59=\frac8{9(11+9K)}$ was checked for $K\le1000$.
8. **Frozen judge on C003.**
   - My first attempt (20:33Z, `timeout 900`) was stopped by me after about 5 minutes. The logged run had needed 59 minutes, so 900 s could not have been enough.
   - My second attempt, `nice -n 10 timeout 5400 python3 judge/judge.py results/claims/C003-reader-5-9-K6.json`, started at 20:38:51Z and ended at about 20:44Z with exit code 144, i.e. a signal that neither I nor the timeout sent. It printed no verdict. I did not start a third run: `scripts/status.py` was running the same judge on the same file at that moment, and another referee's job shared the CPU.
   - The verdict is still confirmed, without using my run:
     - (a) experiments/20261020-1730-reader-5-9/claim_K6.log contains `JUDGE: PASS NEW-RECORD C003-reader-5-9-K6 n=65 h=37 ratio=37/65 (0.569231) vs 4/7=0.571429`.
     - (b) results/.judge_cache.json (written 2026-10-20T20:40Z by a completed status.py run, which re-judges records live) has the entry `{'ok': True, 'tag': 'NEW-RECORD', 'id': 'C003-reader-5-9-K6', 'n': 65, 'h': 37, 'ratio': '37/65'}`. Its key is `7c1f981c…ccf58:e061f0e2…10ed`. I checked with `sha256sum` that the first half is the SHA-256 of results/claims/C003-reader-5-9-K6.json and the second half is the SHA-256 of judge/judge.py, which equals judge/judge.sha256.
     - (c) Check 7 reproduces everything the judge checks, by my own exact methods: integer parsing, distinctness, the (4,5) test, $h=37$ exactly, and the ratio.
   - Corollary 3 uses the verdict only as a quoted record statement; the proof does not depend on it.
9. **Audit of the prover's code** (read, not used). I read v1–v5 and v7 in experiments/prover/L015/. They do what C1–C7 say:
   - v1 covers F0–F6, with trial division to 16 and the six $m=3$ sign patterns;
   - v2 computes the table by AP-free bitmasks and by the Sidon definition;
   - v3 groups pair sums;
   - v4 runs a branch-and-bound on the AP hypergraph and is correctly described as computing $\alpha(H_{AP})$;
   - v5 checks $T_K$;
   - v7 runs the controls.

   The stored outputs end with the seven `ALL … OK` lines. v7's printed label `h({1..9})` is kept on purpose and is explained in its docstring and in the certificate as $\alpha_{AP}$.
10. **Provenance.** I compared the certificate's Statement, Provenance, "Not claimed" and Step 8.1 with kb/literature/sources/aday_757_reader_5_9/day_757_reader_five_ninths_refereed.txt and submission_7bkzb8.md. Each item below is present in the certificate and agrees with the source:
    - the submission 7bkzb8 of 17 Oct, "ANONYMOUS";
    - the day page of 19 Oct, with status "PARTIAL";
    - "Unreviewed by humans";
    - the "Whose." sentence;
    - "Built and kept by Patrick White with Claude (Anthropic)";
    - the submission page's verdict label "VERIFIED" (review of 2026-10-19), with its disclaimer quoted verbatim;
    - the line "Tools, as declared by the submitter: Opus 5.5 found (and independently refereed) the bound. GPT Sol 6.1 also independently checked it.", quoted verbatim;
    - the list of what the site says it checked: the literal test for $K\le12$, the census of $S_{12}$, CP-SAT and CaDiCaL for $K\le8$, the hostile-referee pass with its four gaps, the depth-150 census and the depth-200 transfer matrix, and the novelty search;
    - "none of the submitter's code; there was none";
    - the verification-folder URL.

    The certificate makes no priority or novelty claim and says that its route follows the site's level argument (8.1, 8.2). Nothing is claimed about $9/17$ ("untouched") or about $c_*=5/9$ ("not attained"). The I11 sentence in the sanity checks is a conditional remark about a [conjecture].

## Problems found (in order of severity)

None affects correctness, completeness or honesty. Everything below is optional wording, which I do not require for acceptance.

1. **Credit for the level idea in "What this certificate adds" (wording).** The bullet lists "the level lemma" among the contents of "a complete written proof". The fixed-point identity $251(p-L)=(18/269)^j(251x-27169)$ and the deepest-level-mod-269 idea come from the site's write-up, and from the agent's README §5. Steps 8.1–8.2 say so, but the bullet itself does not. Suggest "… a complete written proof for every $K$ along the site's level argument (Step 8.1), without its span bound or census: …".
2. **"status PARTIAL" (wording).** In the header and in the Statement, "PARTIAL" is the site's problem-status tag; the submission page reads "A verified partial result (a case, a bound, an exact value)". It does not mean "partially verified". Half a sentence would prevent that misreading.
3. **Scout review not cited (bookkeeping).** The STATUS line and the Provenance tag line ("Novelty was not assessed here") could cite the scout review that now exists (results/reviews/L015-reader-family-c-le-5-9__scout__20261020T201417Z.md, NOVELTY: PARTIAL).
4. **Two notational looseness points (cosmetic).**
   - The symbol $T$ is used both for the deepest-level position set (Step 2) and for subsets of $S_K$ (Step 5).
   - In Theorem 1(b), "In particular no relation in $S_K$ has four distinct points ('no relation crosses copies')" puts two different consequences side by side. "Crosses no copies" follows from the main clause ($\varphi^J(e)\subseteq$ copy $J$), not from the 4-point statement.
5. **Normal form in 2.5 (cosmetic).** For $e_1$ the derived relation is $(u,u,\varphi^J(98),\varphi^J(0))$, so reaching "$(u,u,v,w)$ with $v<u<w$" uses the $p_3\leftrightarrow p_4$ exchange. Theorem 1(b) allows this exchange, so nothing is wrong; a two-word remark ("after $p_3\leftrightarrow p_4$") would make it explicit.

Hunted for and not found:
- induction without a base, or with a missed case: the recursions of 1.1 and 5.4 have their bases;
- a false WLOG: 2.5 is a genuine $D_4$ reduction;
- dropped boundary terms;
- [community] facts used as published;
- weak Sidon confused with (4,5): (4,5) is proved directly in Step 4;
- saturation-only properties;
- off-by-one constants;
- circularity.

## Independence statement

All my computations (r1–r6) were written from scratch in this round, in experiments/referee/L015-round2/. They import no code from experiments/prover/L015, experiments/20261020-1730-reader-5-9, experiments/falsify/l015-reader-family, e757/, judge/ or any other referee folder. The only library is pysat. They read results/claims/C003-reader-5-9-K6.json and data/small_records.json only as data.

My methods differ from the prover's:
- F4 by ordered quadruples, not sum grouping;
- the census by ordered-triple completion, not sum grouping;
- $h$ by SAT with two solvers and by a frontier DP on Sidon-definition constraints, not branch-and-bound on the AP hypergraph.

I read the prover's scripts only to audit them and did not run them; reproduce.sh would overwrite files in the prover folder. I recorded my verdict before reading the round-1 review, the scout review and the falsifier report. I did not edit any file outside my scratch folder and this review.

## Comparison with the round-1 review (results/reviews/L015-reader-family-c-le-5-9__referee__20261020T201719Z.md)

- **Verdicts.** Round 1 gave ACCEPT WITH FIXES (meaning NEEDS-WORK), with every mathematical step verified and five documentation items. I give ACCEPT on the current version. On the mathematics we agree completely: neither of us found a gap, a missing case or a hidden assumption in Steps 0–7, and our hand re-derivations of Lemma 1.2, the $m=1..4$ analysis, Step 4 and the six arguments of 5.6 reach the same conclusions.
- **Round-1 items, re-checked in the current version.** All five were applied.
  1. Provenance. The submission page is now saved as kb/literature/sources/aday_757_reader_5_9/submission_7bkzb8.md. The "VERIFIED" label, the disclaimer, the declared-tools line and the list of the site's checks are all quoted, and I found them verbatim in the saved page.
  2. C7. The certificate and README now say "$\alpha_{AP}(\{1..9\})=5$ … not $h$". v7 keeps its printed label and documents that in its docstring.
  3. C4(b). It now reads "$\alpha(H_{AP}(S_K))=7+5K$ (= $h$ by Step 5.1 / Theorem 1(b))".
  4. Step numbers. The script docstrings now say Steps 1–5 (v1), 5.4–5.6 (v2), Step 4 (v3) and Step 6 (v5).
  5. The falsifier section now reports HOLDS-ON-DATA.
- **Differences in what was checked.**
  - Census: round 1 used sums and differences for $K\le20$; I used ordered-triple completion for $K\le20$ and $K=25,30,40$.
  - DP vertex order: round 1 used BFS (maximum frontier 7); I used maximum cardinality search (maximum frontier 6).
  - SAT: round 1 used CaDiCaL with a totalizer for $K\le20$, plus CP-SAT for $K\le3$; I used CaDiCaL and Glucose with a sequential counter for $K\le8$.
  - Round 1 also tested the Step-4 equivalence on about 48,000 sets and re-ran the prover's scripts from a copy. I did neither, and relied on proof and audit for those parts.
  - I added the exact $|B-B|$ distribution check ($11$ exactly $9(K+1)(n-3)$ times) and a self-test of both $h$ methods against brute force.
  - Neither round completed its own judge run. Round 1 did not start one, citing the load. Mine was killed by an external signal (check 8). I confirmed the verdict from the status.py judge cache, keyed by the exact file and judge hashes, in addition to the log that round 1 read.
  - Round 1 fetched the submission page live. I used the saved copy that now exists.
- **New in round 2.** Optional remarks 1–5 above, none of which round 1 raised. They are wording only and do not change the verdict.
