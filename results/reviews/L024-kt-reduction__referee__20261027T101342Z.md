VERDICT: NEEDS-WORK

# Referee report: results/proofs/L024-kt-reduction.md (referee #1, round 1)

Certificate reviewed at commit 614fa65. My scratch folder is experiments/referee/L024-round1-opus/. I wrote this report without reading any other review of L024.

Note on the verdict line: the workflow offered `ACCEPT / REJECT / ACCEPT WITH FIXES`. My standing referee instructions allow only `ACCEPT / REJECT / NEEDS-WORK` and say that "a minor fixable gap means NEEDS-WORK". This verdict means "accept once the fixes are made". I found no mathematical error. Every hand proof was checked line by line, and every load-bearing computation was reproduced by independent code. The required fixes are P1 and P2 below (one or two sentences each). P3–P6 are editorial.

## Summary

L024 proves reduction lemmas for a hypothetical minimal counterexample $H$ to L021's inequality KT$^{L^*}$. It claims no bound. It also proves a conditional theorem (Theorem 6): KT$^{L^*}$, hence $11\tau\le\frac{19}{6}n+2m$ on $C$ and $c_*\ge35/66$, follows from three open hypotheses R1–R3.

I checked the following by hand and they are correct:
- Lemma 1: (E+) gives (AH), and the special component is unique.
- Lemma 2, the new rich-member lemma. Its capacitated-Hall argument is sound: Claim E for the subfamilies $X\setminus N_B(S)$ gives Hall's condition with capacity 2 on the rich member. The resulting assignment, together with (L1) and richness, gives a union of minimum transversals that meets $E^*$, which contradicts Claim B.
- Lemma A(a) and (b).
- Lemma A+: cases (α)/(β)/(γ)/(δ), the counting $n\le31$ and $n\le46$, and hence the threshold 47.
- Proposition 3: the replacement inequality (5.1), and the linearity, $F_7$ and (P3) checks of the one- and two-vertex pendants.
- The structural part of Theorem 4.
- The logic of Theorem 6, which is valid and not circular.

All piece data were recomputed with my own code and agree with the certificate: richness, the non-co-transversal pairs, the degree sequences, the $\Delta\le2$ pieces, (L1), and the weights. The six 17-vertex pieces were matched bijectively to the stored list `cell_17_13_7.txt` and are all rich.

My independent enumerator reproduces Theorem 4's computation exactly: 783 $g$-orbits, 359 Claim-B configurations, 206 in $C_3$, all 206 isomorphic to members of $L^*$, and 0 configurations for the seven types with $n=24,31$. A brute-force enumerator that uses neither my pruning nor the prover's agrees on every type with $n\le24$.

The problems are of precision:
- (G2-i), and the restatement of L021 (H$_3$) in Step 0.5, drop L021's qualifier "new edge ($e'\notin E(R)$)". Under the set reading of $R+e'$, Step 5.6 then has a small uncovered case. A one-line argument closes it (P1).
- R2 speaks of "its minimal apex", but the minimal apex need not be unique (P2).

Neither affects the truth of any claim.

## Checks performed (all in experiments/referee/L024-round1-opus/; `nice -n 10`, under `timeout`, one process at a time)

My own library `rlib.py` contains the following. It does not import e757, judge, hyp24.py or kt.py.
- degrees and linearity;
- an $F_7$ test that is complete: every centre of degree at least 3, every 3 edges at it, all 8 splittings;
- (P3) via the equivalence "every $k$ edges span at least $k+2$ vertices". This is tested by tripling each edge in turn and checking that the vertex–edge incidence graph has a matching saturating the edge side (Hall). This is a different method from the prover's per-pair test.
- $\tau$ and all minimum transversals by brute force, plus a branch-and-bound $\tau$;
- automorphisms and isomorphism by backtracking with degree refinement.

1. **Library self-test.** `timeout 1200 nice -n 10 python3 selftest.py`: `selftest graphs 3000 F7 brute tested 300 F7 positives 0 mismatches 0`. This covers (P3) against brute force over edge subsets, and $\tau$ and minimum transversals against brute force. Because random graphs contain no $F_7$, I added `python3 selftest_f7.py`: `planted tests 60 positives 32 mismatches 0`, compared with brute force over injections.
2. **Pieces (C1, C2; Lemma 2's data; 0.6, 0.8).** `timeout 1200 nice -n 10 python3 check_pieces.py` → `check_pieces_output.txt`.
   - All 32 pieces are connected and lie in $C_3$. Their $(n,m,\tau,W)$ equal closure_results.json, and (L1) holds for all 32.
   - RICH: `(10,7,4)#0,#3`, `(15,11,6)#4,#5,#14,#15,#16,#17`, `(17,13,7)#0`–`#5`.
   - NON-RICH: $E_1$, `(8,5,3)#0,#1`, `(10,7,4)#1,#2` and `(15,11,6)#0,#1,#2,#3,#6`–`#13,#18`. For `(10,7,4)#1,#2` the non-co-transversal pairs are exactly $\{0,1\},\{0,2\}$, and $\{0,1,2\}$ is the edge at the unique degree-1 vertex 0.
   - $\Delta\le2$ holds only for `(3,1,1)#0` and `(8,5,3)#0`, the latter with degree sequence $2^7 1$, vertex 0 of degree 1, edges $012,156,247,346,357$.
   - Degree sequences: $3\,2^9$ for (10,7,4)#0,#3; $3^2 2^7 1$ for #1,#2; $3^5 2^{12}$ for every (17,13,7).
   - The $\Delta\le3$ classes of the stored lists `experiments/20261027-0300-transversal-richness/inputs/cell_{3_1_1,8_5_3,10_7_4,15_11_6,17_13_7}.txt` (1, 2, 4 of 5, 19 of 30, 6) are in bijection with the pieces up to isomorphism, and no two pieces are isomorphic.
   - `rich_stored.py` → `rich_stored_output.txt` recomputes richness directly on the stored graphs: 14 rich graphs (6 of (17,13,7), 2 of (10,7,4), 6 of (15,11,6)), as requested in the spec.
3. **Theorem 4, own complete search.** `timeout 3000 nice -n 10 python3 pattern_a_ref.py poor` → `pattern_a_ref_poor_output.txt` and `pattern_a_ref_poor.json`. The output is `TOTAL {'g_choices': 783, 'configs': 359, 'inC3': 206, 'tau_ok': 206, 'in_Lstar': 206, 'not_in_Lstar_inC3': 0, 'need2_zero_events': 0}`.

   | type | configurations | in $C_3$ | isomorphic to |
   |---|---|---|---|
   | $(E_1,E_1,E_1)$ | 44 | 32 | (10,7,4)#0, #2 |
   | $(E_1,E_1,(8,5,3)\#0)$ | 105 | 60 | (15,11,6) classes |
   | $(E_1,E_1,(8,5,3)\#1)$ | 138 | 86 | (15,11,6) classes |
   | $(E_1,E_1,(10,7,4)\#1)$ | 32 | 12 | (17,13,7) classes |
   | $(E_1,E_1,(10,7,4)\#2)$ | 40 | 16 | (17,13,7) classes |
   | 3 types with $n=24$ (25, 30, 36 $g$-orbits) | 0 | – | – |
   | 4 types with $n=31$ (125, 150, 180, 216 $g$-orbits) | 0 | – | – |

   - The method differs from pattern_a3.py:
     - restrict unions of minimum transversals meeting $g$ to the candidate co-vertices;
     - keep the inclusion-maximal ones;
     - branch three levels, each on "a pair killing the not-yet-killed union with fewest killers".
   - Every solution is re-verified by brute force over all triples of minimum transversals. $\tau$ is computed by branch and bound, and the isomorphism test is my own.
   - My orbit computation reproduces the 783 $g$-orbits. Reducing $g$ by $\mathrm{Aut}(F_1)\times\mathrm{Aut}(F_2)\times\mathrm{Aut}(F_3)$ is sound because the set of admissible pair-triples is equivariant.
4. **Completeness cross-check without any pruning.** `timeout 2400 nice -n 10 python3 pattern_a_brute.py 24` → `pattern_a_brute_output.txt`. It tests all triples of disjoint admissible pairs directly against all unions. The per-type counts are identical on every poor and rich type with $n\le24$ (44, 105, 138, 32, 40, 0, 0, 0; rich 8, 12, then 0 seven times), with `BRUTE TOTAL 379` $=359+20$.
5. **Rich types (C5).** `pattern_a_ref.py rich10` → evidence file `pattern_a_ref_rich10.json`, written at the end of the run; see P6 on the text log. It covers 25 type triples and finds 20 configurations: 8 of $(E_1,E_1,(10,7,4)\#0)$ and 12 of $(E_1,E_1,(10,7,4)\#3)$. None satisfies Claim E on the subfamilies of $X_v$, and none lies in $C_3$. This agrees with C5 and with Lemma 2.
6. **(D1) part 0 (6.1, C3 part 0).** `python3 d1_part0.py` → `PART0 raw 74, up to Aut 39, in C3 0`. This agrees with the certificate's 74. A hand argument gives the same result: such an $F+v$ has $n-m=n_F-m_F-2\le1$, so it violates (P3), and also $s(F+v)=s(F)-2<0$, which contradicts L016.
7. **Lemma 2, combinatorial core.** `python3 lemma2_random.py 1 20000` tests random disjoint copies of 1–3 pieces with $k+1$ random edge traces (at most 2 vertices per piece). Result: 10,762 instances with a rich piece and Claim E on all subfamilies, with 0 violations (a covering union always exists). As a control, 2,105 instances without a rich piece, of which 46 satisfy Claim B, so the test can fail.
8. **Hub identities (4.5–4.6).** `python3 hub_identity.py`: 5,013 hubs over random graphs and stored small cells, 0 mismatches with $\tau(G'\oplus(a,b,c))=\tau(G')+1$ or $+2$ according to whether some minimum transversal contains two of $a,b,c$ (3,159 b-configuration cases). In 919 of 919 hubs over an existing edge $\{a,b,c\}$ the result contains $F_7$.
9. **Prover's code re-run.** `python3 -B .../L024/richness.py` and `.../pieces_info.py`: outputs identical, after sorting, to the stored files. `prover_pattern_a3_copy.py poor` is a scratch copy of pattern_a3.py with only the output path changed. Its totals JSON equals the stored `pattern_a3_poor_results.json`: `{'type_triples': 12, 'g_choices': 783, 'configs': 359, 'claimE': 206, 'inC3': 206, 'inC3_claimE': 206, 'tau_ok': 206, 'Pneg': 0}`. I did not re-run C0 (test_hyp24) or C6 (sanity24). Neither is load-bearing; checks 1 and 8 cover their content with my own code.
10. **Data sanity (KT, the input of L021 Theorem 7(ii) used for $n\ge25$).** `kt_data_check.py`, output in `kt_abase_delta4_output.txt`, covers the AP hypergraphs of every set in data/small_records.json and of $\{F_3,\dots,F_{15}\}$: $A_{\rm base}$, the three 12-point sets, and the 8-, 10- and 11-point sets.
    - On every induced subgraph with $\Delta\le3$, $P=A+\mathrm{DEF}\ge0$, with DEF computed exactly with my own code.
    - The full sets have $A=6$ ($A_{\rm base}$), $14$, $14$, $14$, $22$, $49$ and $173$ (Fibonacci). The 8-point set has $A=-5$ and is itself $(8,5,3)$.
    - My first run, `kt_data_check_output_unfiltered_includes_Delta4.txt`, forgot the $\Delta\le3$ filter. It found $P=-13$ on the induced subgraph $\{0,136,200,249,272,298,400,528,596,1056\}$ of $A_{\rm base}$. This is a (10,7,4) graph with $\Delta=4$, not in $C_3$, with DEF $=0$. So KT$^{L^*}$ really is false outside $C_3$, and the condition $H'\in C_3$, which L024 checks in every replacement, is essential. This is not a problem of L024.
11. **Side check for R2(β).** `beta_cut.py`: see S2.

## Audit, statement by statement

**Conventions and Step 0.**
- The definitions match L021 Definition 2 and Theorem 3, including the definition of a minimal counterexample over $C_3$ with $n+m$ least.
- 0.6 is correct. The pair lemma is L017 Theorem 2(U) with $s(F-\{x,y\})\ge0$ from L016. The hand proof of richness for the tight pieces without a degree-1 vertex is valid: $|\partial|\ge3>5/2$.
- 0.8 is correct and confirmed by computation (check 2).
- 0.9 is standard.

**Lemma 1.**
- (a): from $35e\le16j-1$ and $e+k\ge j+2$ with $k\le3$ we get $e\ge j-1$, then $19j\le34$, so $j=1$, $e=0$ and $k=3$. A connected induced member with no edge leaving it in $H-v$ is a component.
- (b): checked item by item (existence, every special component met by all three edges, uniqueness, disjoint nonempty traces, Claim B, $\mathrm{DEF}(H-v)=W(F_v)$, and $-16\le A(H)\le-1$).

Correct.

**Lemma 2.**
- What is matched to what: the edges of $E^*_H(X)$ are assigned to members of $X$, along $e\sim F$ iff $e\cap V(F)\ne\emptyset$. The capacities are $c(F^*)=2$ and 1 for the other members, so the total capacity is $|X|+1=|E^*|$.
- Hall's condition: if $N_B(S)=X$ it is immediate. Otherwise $Y'=X\setminus N_B(S)\ne\emptyset$ satisfies $E^*_H(Y')\subseteq E^*_H(X)\setminus S$. An edge meeting $V(Y')$ lies inside no member of $X\setminus Y'$, and it is not in $S$. Claim E for $Y'$ then gives $|N_B(S)|\ge|S|$.
- The assignment and (L1) handle every member that receives one edge. Richness handles $F^*$ when it receives two edges with $u\ne u'$, and (L1) when $u=u'$. Every trace of an $E^*$-edge on a member has at most 2 vertices, because members are induced.
- The union then meets every edge of $E^*_H(X)$, which contradicts Claim B for $X$.
- Why a rich piece breaks Claim B: $|E^*|$ exceeds $|X|$ by exactly one, and richness is exactly what lets one member absorb two edges.
- The lemma uses only Claim B for $X$, Claim E for subfamilies of $X$, (L1) and richness. It does not need $X$ to be optimal. It applies to (D1) with $k_v=2$, to (D2) and to (D3), as the Sanity checks say.

Correct. Numerically confirmed (checks 5 and 7).

**Lemma A(a).**
- The two kinds of components are right. In kind (i), $V(F_w)$ lies inside a component of $F_v-w$, so $|V(F_w)|<|V(F_v)|$, which contradicts minimality.
- In kind (ii), $F_w=D_i$, and every edge leaving $D_i$ contains both $v$ and $w$. So $|E^*_H(\{D_i\})|\le1$, which contradicts Claim E, or equivalently Lemma 1(b) uniqueness.

Correct. This version is more careful than SYNTHESIS §3.

**Lemma A(b) ($n\ge67$).**
- $r\le3$: each $D_i$ contains an outer co-vertex, and there are at most three outer co-vertices.
- $\sum|V(D_i)|\ge49>48$ gives a component $D$ with $|V(D)|\ge17$. An edge at $v$ that meets $D$ and avoids $w$ would give $|V(F_w)|\ge18$.
- So $Z\subseteq\{f\}$ and $\Delta(F_v)\le2$. By 0.8, $F_v$ is $E_1$ or $(8,5,3)\#0$. The trace argument gives two or three vertices of $F_v$-degree at most 1 by (4.1), while $(8,5,3)\#0$ has one. So $F_v=E_1$ with singleton traces.
- 4.5: $27\cdot4+35\cdot4-132=116$ and $3\cdot35=105$, so $P(H)\ge P(G')+11$. This uses minimality for $G'$, which is induced, lies in $C_3$, and has $n+m$ smaller by 8.
- 4.6: $\tau(H)=\tau(G')+2$. $A(G')=A(H)+16\in[0,15]$ uses Lemma 1(b) with $W(E_1)=16$.
- The explicit $F_7$ embedding over an edge $\{a,b,c\}$ is right; I checked it by hand and in check 8.

Correct.

**Lemma A+.**
- The four cases are exhaustive and pairwise exclusive.
- (α) uses no bound on $n$.
- (β) is the case where some $w\in V(F_v)$ with $d_H(w)=d_{F_v}(w)=3$ is not a co-vertex of $v$. Then (4.2) puts $v$, all three edges at $v$ and every $D_i$ inside $V(F_w)$, as a disjoint union with $|Q_1\cup Q_2\cup Q_3|\ge3$. So $\sum|V(D_i)|\le13$, $n\le31$, and $V(H)=\{v\}\cup V(F_v)\cup V(F_w)$.
- (γ) is impossible, as shown.
- (δ) is the case where every vertex of $Z$ is a co-vertex of $v$ (so each has $F_v$-degree 2) and $Z$ meets two edges $e_j,e_k$. Then $\sum_{D\in\mathcal D_1}|V(D)|\le14$ via $F_w$ and $|V(D^\circ)|\le14$ via $F_{w'}$, so $n\le46$ and $V(H)\subseteq\{v\}\cup V(F_v)\cup V(F_w)\cup V(F_{w'})$.

The bounds are correct (they need not be sharp). The threshold 47 follows.

**Proposition 3.**
- 5.1 checked:
  - it uses H.1 (L021 8.1), which holds for every $X$ with $|E^*|=|X|+1$ by Claim E;
  - it uses 8.3. I re-derived Cases 1 and 2 of 8.3 for $e'=\{p,q,z\}$ and $e'=\{p,z_1,z_2\}$, and the maximality of $|X|$ is used where L021 uses it;
  - the bookkeeping $m(H)=m(H')-1+\sum m_F+|X|+1$ is right, and $n(H')+m(H')<n(H)+m(H)$.
- (a): $19|X|-43\ge14$ for $|X|\ge3$. The linearity check, the $F_7$ check (min degree 2 in $F_7$), the three (P3) cases and the degree check are all right.
- (b): $19|X|-70\ge6$ for $|X|\ge4$. The (P3) bound $\le|S|-2$ is right. The certificate's correction of L021 8.4 ("$\le|S|-3$" fails for $S=e'$) is right.
- (c): $R=\emptyset$, $\tau=\sum\tau_F+1$, $A=35|X|-97-\sum W$, and $|X|=5$ forces five copies of $E_1$ ($4\cdot16+13=77<79$), so $n=15<25$.
- (d): this is Lemma 2.
- The residue derivation in 5.6 is right, subject to P1.

**Theorem 4.**
- 6.1:
  - (D1) gives $H-v=F$, so $n\le18$ (also excluded by L016, see check 6);
  - (D2) is impossible;
  - (D3) gives $R_v=\emptyset$, $g$ meets each member in exactly one vertex, and $n\le52$;
  - (C1)–(C4) are exactly the necessary conditions.
- 6.2: Lemma 2 applies because $|E^*_H(X_v)|=4=|X_v|+1$. The weight enumeration gives exactly the 12 type triples; my type generator produces the same 12.
- Completeness: $g$ is reduced only by the automorphisms of each piece, and the pair-triples are not reduced. My search, a brute force without pruning (for $n\le24$), and the prover's level search, whose WLOG levels I checked are complete, all give 359.
- The 206 configurations in $C_3$ automatically have $\tau=\sum\tau_i+1$ (Claim B together with (L1) forces it) and $A=35-\sum W$. They are isomorphic to members of $L^*$, so $P\ge0$ (in fact $P=0$ by L021 Theorem 7(i)).
- For $n\le17$ the conclusion also follows without the search: a connected member of $C_3$ in cell (10,7,4), (15,11,6) or (17,13,7) is in $L^*$ because these cells are complete. The search is load-bearing only for $n=24$ and $n=31$.

Correct.

**Proposition 5 and Theorem 6.**
- The chain of reasoning: if KT fails, take a minimal counterexample. Then:
  - $n\ge25$ by L021 Theorem 7(ii);
  - R1 and 5.6 give (E+);
  - Lemma 1(a) gives (AH);
  - L021 Theorem 6 gives $\Delta=3$;
  - choose the minimal apex; Lemma A+ gives (α), (β) or (δ);
  - R2 excludes (β) and (δ);
  - (α) is the R3 configuration, which R3 excludes.
- Then KT gives $J_{1/6}$ on $C_3$ (L021 Theorem 2, with $J_{1/6}$ on $L^*$ by L016), then on $C$ (Theorem 1(a)), and then $f(n)\ge(35n+24)/66$ and $c_*\ge35/66>9/17$ (Theorem 1(b); $595>594$).
- The "spec form" variant is also valid.
- There is no circularity. R1–R3 are statements about minimal counterexamples and do not presuppose KT.

**Exact inputs.**
- Unrefereed inputs used:
  - L021 Theorems 1(a), 1(b), 2, 3 (Claims A, B, C, E, F), 4 ((a), (b), (D1)–(D3)) and 6;
  - L021 Proposition 8 (8.1 = H.1, 8.3, (H$_3$), (H$_0$));
  - L021 Theorem 7(ii) ($n\ge25$; a computation);
  - L021 Theorem 7(iii), which the prover and I re-verified.
- Refereed inputs: L016 and L017 (0.6, 0.7, Theorem 2(U)).
- Not used: L017 C5 (it enters L021 only through Theorem 7(v)), the kt-cells run, L021 Theorem 5, Theorem 7(i), (iv), (v), Proposition 9, and L022.

**R1–R3, W1, W2.**
- R1 and R3 are precise conjectures, modulo P1.
- R2 is precise modulo P2.
- (G2-iii) is a finite statement ($n\le60$) and W1 specifies it completely enough to implement:
  - pieces;
  - $k+1$ edges inside $V(X)$, each meeting at least two pieces;
  - linear, $\Delta\le3$;
  - $\sum W\ge35k-96$, $n\ge25$;
  - Claim B and Claim E;
  - then test membership in $C_3$ and compute $P$.
- R2 is finite ($n\le46$), but W2 is only a sketch (P4).
- (G2-i), (G2-ii) and R3 are infinite statements, and the certificate says so.

**Tags.**
- These are honest: no bound is claimed, KT is a [conjecture], Theorem 6 is conditional, the computations are [verified-here as computations, unrefereed], the lemmas are [derived-here], and the STATUS is unrefereed.
- One editorial point is under P3.

## Problems, in order of severity

**P1 (minor gap, fix required): $R+e'$ for an existing edge; the residue (G2-i) and Step 0.5.**
- L021 (H$_3$) applies only to "a 3-set $e'\subseteq\partial(X)$ that is a new edge (not in $E(R)$)".
- L024 drops "new" in two places:
  - Step 0.5 restates (H$_3$) as "if $|\partial(X)|\ge3$ and some 3-set $e'\subseteq\partial(X)$ has $R+e'\in C_3$, contradiction";
  - (G2-i) is defined as "no 3-subset $e'\subseteq\partial(X)$ has $R+e'\in C_3$".
- $R+e'$ is never defined for $e'\in E(R)$. Under L024's implicit convention $m(R+e')=m(R)+1$ (Step 5.1), a repeated edge is not linear, so $R+e'\notin C_3$, and (G2-i) and 5.6 are correct.
- Under the natural set reading ($R+e'=R$ when $e'\in E(R)$) there is an uncovered case. Take $|X|\le2$ with some 3-subset of $\partial(X)$ an edge of $R$ and no addable new 3-subset. Such an $X$ is not in (G2-i), and L021's (H$_3$) does not exclude it. So the claim of 5.6 ("(H$_3$) ... leaves (G2-i)") is unjustified for this case.
- The case is in fact impossible, by one line:
  - every minimum transversal $T'$ of $R$ meets that edge, so it contains some $u\in\partial(X)$ lying on some $e_u\in E^*(X)$;
  - H.1 for $e_u$ gives a transversal $T'\cup\bigcup_FT_F$ of $H$ of size $\tau(R)+\sum\tau_F$;
  - so $A(H)\ge A(R)-\sum W+35(|X|+1)$, while $\mathrm{DEF}(H)\ge\mathrm{DEF}_H(X)+\mathrm{DEF}(R)$ (L021 0.5);
  - hence $P(H)\ge P(R)\ge0$, a contradiction.
- Fix: either write "new ($e'\notin E(R)$)" in 0.5, in (G2-i) and in 5.6, or add the argument above. The argument proves more, see S1.

**P2 (minor, fix required): R2 and the choice of the minimal apex.**
- The minimal apex ($v$ minimising $|V(F_v)|$) need not be unique, and the cases of Lemma A+ depend on the choice. R2 says "has its minimal apex in case (β) or (δ)", and Theorem 6 picks an arbitrary minimal apex.
- Fix: state R2 for every minimal apex, i.e. "no minimal apex of a minimal counterexample satisfying (AH) is in case (β) or (δ)". Alternatively, state it existentially and let Theorem 6 choose such an apex.

**P3 (editorial): dependency lists.**
- DEPENDS ON and the "Where the induction closes" section say "Propositions 8 (… ) and 9" and "Propositions 8–9", but L021 Proposition 9 is used nowhere. Theorem 6's hypothesis list ("Theorems 1–6, Proposition 8 and Theorem 7(ii)") is the accurate one.
- Theorem 5 is in the range "Theorems 1–6" but is not used.
- Theorem 7(iii) is used (and re-verified) and could be named there.

**P4 (editorial): W2 is a sketch, not a specification.**
- "Enumerate the overlap patterns of the two (three) pieces" does not define a search space.
- If W2 is meant to be runnable, it should list the constraints that the proof supplies:
  - $F_v$ is a component of $H-v$, and $F_w$ is the component of $H-w$ containing $v$;
  - (4.1) and (4.2);
  - Lemma 1(b) at $w$ (and at $w'$), including Claim B for $F_w$;
  - $|V(F_w)|\ge|V(F_v)|\ge8$ and $n\ge25$.
- The certificate itself claims only "finite in principle", which is true.

**P5 (editorial, clarity): the role of Theorem 4.**
- Theorem 4 is not used in the proof of Theorem 6. Under (AH), which follows from R1, its conclusion is immediate: $H-v\supseteq F_v$ is connected only if $n\le18<25$.
- Its value is that it holds without R1. A sentence saying so would prevent readers from taking it as load-bearing.

**P6 (environment note, not a defect of the certificate): truncated text logs.**
- The certificate attributes its truncated logs to "commands that ran longer than about 100 s in the foreground". The same truncation hit two of my runs:
  - `pattern_a_ref_rich10_output.txt`, which was moved to the background by the harness;
  - `prover_pattern_a3_poor_rerun.txt`, which was started with `run_in_background`. Its committed snapshot at 10:09:36 UTC has 11 lines, the process continued, and the final type lines were lost while the end-of-run JSON is complete.
- So the cause looks environmental. The project's live-scratch commits coincide with the truncation, but I have not identified the mechanism.
- As in the certificate, the files written at the end of a run (JSON) should be the evidence of record. The certificate already does this, and I reproduced every number independently.

## Suggestions (not required)

- **S1.** The argument in P1 shows more. In a minimal counterexample, for any $X$ with $|E^*(X)|=|X|+1$, no minimum transversal of $R=H-V(X)$ contains a vertex of $\partial(X)$. Equivalently, every pendant replacement $R+e'$ of Step 5.1 has $\tau(R+e')=\tau(R)+1$. This holds in (G2-i) and (G2-ii) as well and may be a useful extra constraint for R1. It is the Claim-B argument of L021 Step 3.2 with one edge of $E^*$ covered from $R$ via H.1.
- **S2.** In case (β), Lemma 1(b) at $w$ shows that the components of $H-w$ other than $F_w$ are exactly the components of $F_v-w$ that contain no trace vertex. Then $n=1+|V(F_w)|+\sum_j|V(K_j)|$. With $n\ge25$, $w$ must be a cut vertex of $F_v$ whose non-trace components have at least 7 vertices in total, and $|V(F_v)|\ge11$. This is not decisive: `beta_cut.py` finds 68 (piece, degree-3 vertex) pairs that pass this test. It may still help W2.
- **S3.** In Theorem 4 one could say that for $n\le17$ the search is not needed (the cells are complete; see the audit), so the search is load-bearing only for $n\in\{24,31\}$.

## Independence statement

All checks above were made with my own code in experiments/referee/L024-round1-opus/: `rlib.py`, `check_pieces.py`, `rich_stored.py`, `pattern_a_ref.py`, `pattern_a_brute.py`, `d1_part0.py`, `lemma2_random.py`, `hub_identity.py`, `kt_data_check.py`, `kt_abase_delta4.py` and `beta_cut.py`. None imports e757, judge, hyp24.py or L021's kt.py. Only the edge lists in experiments/prover/L021/closure_results.json, the stored class lists in experiments/20261027-0300-transversal-richness/inputs/ and data/small_records.json were read as data.

Separately, as a re-run of the prover's own evidence, I ran the prover's `richness.py`, `pieces_info.py` and a scratch copy of `pattern_a3.py` (output path changed only). I ran them with `-B` and wrote nothing into the prover's folder; its git status is clean. The frozen judge does not apply, since there is no construction.

I did not read any other review of L024. I modified no file outside my scratch folder and this review.
