VERDICT: NEEDS-WORK

# Referee report #3, round 2: results/proofs/L024-kt-reduction.md (revision 5da1199)

Referee: opus (Claude), adversarial review. Window: 2026-10-27 10:21 to 10:40 UTC. Scratch folder: experiments/referee/L024-round2-opus/ (own code; it imports nothing from e757, the judge, hyp24.py or kt.py).

**Note on the verdict line.** The workflow offered `ACCEPT / REJECT / ACCEPT WITH FIXES`. My standing referee instructions allow only `ACCEPT / REJECT / NEEDS-WORK`. They also say "ACCEPT only if ... no problem remains", and "a minor fixable gap means NEEDS-WORK". Round-1 referee #1 resolved the same conflict the same way.

Here NEEDS-WORK means **ACCEPT WITH FIXES**:
- every mathematical step of the revision checks out;
- the two required round-1 fixes (P1, P2) are applied correctly;
- what remains is editorial: one round-1 wording fix applied in only one of its three places (N1), a wrong internal cross-reference in the new text (N2), and a one-line derivation that 7.3 asserts but does not write out (N3).

None of these touches a proved statement.

## Summary

The revision makes the round-1 fixes and nothing else of substance. I confirmed this from the full diff of 5da1199, and found no later commit and no uncommitted change to the certificate or to experiments/prover/L024/.

**P1, the new closure in Step 5.6, is correct.** It is L021's Claim-B computation (L021 3.2) with one $E^*$-edge covered from $R$:
- every minimum transversal $T'$ of $R$ meets the edge $e'\subseteq\partial(X)$, so it contains some $u\in\partial(X)$ on some $e_u\in E^*(X)$;
- H.1 (L021 8.1, which applies to the optimal $X$ with $|E^*(X)|=|X|+1$) covers $E^*(X)\setminus\{e_u\}$ by minimum transversals of the members;
- this gives $\tau(H)\le\tau(R)+\sum\tau_F$, hence $A(H)\ge A(R)-\mathrm{DEF}_H(X)$;
- together with $\mathrm{DEF}(H)\ge\mathrm{DEF}_H(X)+\mathrm{DEF}(R)$ (L021 0.5) this gives $P(H)\ge P(R)\ge0$, a contradiction.

The case analysis of 5.6 is now exhaustive under either reading of $R+e'$. The "new edge" qualifier is in 0.5, (G2-i) and 5.6.

**P2 is applied correctly.**
- R2 is now universal ("no minimal apex is in (β) or (δ)").
- Lemma A and Lemma A+ use only $|V(F_v)|\le|V(F_u)|$ for all degree-3 $u$, so they hold for every minimal apex.
- 7.1 picks an arbitrary minimal apex, and universal R2 is exactly what it needs. The existential alternative is also correctly stated to suffice.

**The concrete W2 statement in 7.3 is true.** In (β), $V(H)=V(F_v)\cup V(F_w)$ and $E(H)=E(F_v)\cup E(F_w)$. In (δ), the same holds with the three pieces $F_v,F_w,F_{w'}$. I re-derived both by hand and tested them on 38,711 random (β)/(δ) structures with no failure. However, the proofs as written in 4.7 give only the vertex statements; the edge statement needs one extra line (N3).

**Fable's documentation items are applied:**
- the kt.py import statement is now accurate (only pieces_info.py imports kt.py);
- pattern_a3.py takes an optional output path. My re-run with a scratch path reproduced the evidence of record exactly and left it untouched;
- the (G2-i) qualifier is in.

However, the "$\sum W\ge36$" qualifier for C5 was added only in 6.3. The C5 bullet and a Sanity-checks bullet still describe the coverage wrongly (N1).

**Adversarial spot-check (Lemma A+'s case split).** An exhaustive local check over all 32 pieces and all admissible trace triples, plus a random structural test, both pass. They also show a sharpening the certificate does not state (N5): case (δ) forces $F_v=(8,5,3)\#0$, hence $n\le37$.

## Item-by-item check of the round-1 requests

| Round-1 item | Where applied | Status |
|---|---|---|
| opus P1: the "new edge" qualifier | 0.5 ("that is a NEW edge ($e'\notin E(R)$)" plus the convention "$R+e'$ defined only for a new edge, $m(R+e')=m(R)+1$"); (G2-i); 5.6, second part | applied correctly |
| opus P1: closure of the existing-edge case for $\lvert X\rvert\le2$ | 5.6, first part | applied; verified in full (below) |
| opus P2: R2 for every minimal apex | Proposition 5 R2 ("ANY minimal apex", with the definition and the existential remark); Lemma A ("need not be unique ... hold for every choice"); 7.1 ("any one", "GAP R2 (stated for every minimal apex)"); 7.3 ("no minimal apex") | applied correctly |
| opus P3: Proposition 9 unused, Theorem 5 unused, Theorem 7(iii) named | DEPENDS ON ("Proposition 9 is not used"); "Where the induction closes" ("Theorem 5 is not used", "Theorem 7(iii)", "Proposition 9 is not used") | applied. Theorem 6's hypothesis list and DEPENDS ON still say "Theorems 1–6"; that over-assumes but does no harm (N6) |
| opus P4 / fable 4: W2 concrete | 7.3 and README W2: $E(H)=E(F_v)\cup E(F_w)$, resp. three pieces | applied; statement verified, but its derivation is not written (N3); not added to the statement of Lemma A+ (optional) |
| opus P5: Theorem 4 not used in Theorem 6 | parenthetical after Theorem 4; README | applied; correct (under (AH), $H-v$ connected forces $H-v=F_v$, $n\le18<25$) |
| opus S1 (optional) | 5.6, bracketed "[Referee remark]" | inserted; correct; one scope caveat (N4) |
| opus S3 (optional) | Theorem 4 parenthetical ("load-bearing only for $n\in\{24,31\}$") | inserted; rests on the completeness of L021's cell lists, not re-verified by me, not load-bearing (N6) |
| fable 1: kt.py import | DEPENDS ON, README | applied; accurate (grep: only pieces_info.py imports `tau_masks, masks, min_transversals, A_value` from kt.py; hyp24.py imports only json, itertools, sys; the other scripts import hyp24 only) |
| fable 2: hard-coded output path | pattern_a3.py (optional third argument), README (safe re-run command) | applied; tested (check 3). The default is still the evidence file, and the certificate's C4 command does not mention the argument (N6) |
| fable 3: the (G2-i) qualifier | (G2-i) | applied |
| fable 3: C5 "only under $\sum W\ge36$" | 6.3 only | **partly applied**: the C5 bullet and the Sanity-checks bullet are unchanged (N1) |
| STATUS line | header | updated; accurate |

Other changes in 5da1199: none.
- The certificate has 6 hunks, all listed above.
- README.md has 3 hunks: the Theorem 4 note, the imports and re-run paragraph, and W2.
- pattern_a3.py has one hunk, the output path only. The search is unchanged, and the re-run reproduces the evidence byte-for-byte in content.

## Re-verified passages

**Step 5.6, the new closure (case $\lvert X\rvert\le2$, some 3-subset $e'\subseteq\partial(X)$ with $e'\in E(R)$).**
- *Why H.1 applies.* $X$ is the family of Proposition 3: it minimises $\lvert E^*\rvert-\lvert X\rvert$, maximises $\lvert X\rvert$ among those, and has $\lvert E^*(X)\rvert=\lvert X\rvert+1$. These are exactly L021 Proposition 8's hypotheses. In fact L021 8.1's proof uses only $\lvert E^*(X)\rvert=\lvert X\rvert+1$, Claim E for the subfamilies (via Hall on $B-e$) and (L1). So H.1 gives minimum transversals $T_F$ whose union meets $E^*(X)\setminus\{e_u\}$.
- *Why a minimum transversal of $R$ extends.* $e'\in E(R)$, so every minimum transversal $T'$ of $R$ meets $e'\subseteq\partial(X)$ and contains some $u\in\partial(X)$. By the definition of $\partial(X)$, $u$ lies on some $e_u\in E^*(X)$. By the edge partition (L021 0.3; L024 0.1), $E(H)=E(R)\sqcup\bigsqcup E(F)\sqcup E^*(X)$. The set $T'\cup\bigcup T_F$ meets every edge:
  - edges of $R$ by $T'$;
  - edges of the members by the $T_F$;
  - $E^*(X)\setminus\{e_u\}$ by H.1;
  - $e_u$ by $u$.

  Hence $\tau(H)\le\tau(R)+\sum\tau_F$.
- *Why $P(H)\ge P(R)\ge0$.*
  - Use $n(H)=n(R)+\sum n_F$, $m(H)=m(R)+\sum m_F+\lvert X\rvert+1$ and $A(F)=-W(F)$. These give $A(H)\ge A(R)-\sum W+35(\lvert X\rvert+1)=A(R)-\mathrm{DEF}_H(X)$.
  - Take $Y$ attaining $\mathrm{DEF}(R)$. L021 0.5 gives $\mathrm{DEF}(H)\ge\mathrm{DEF}_H(X\cup Y)=\mathrm{DEF}_H(X)+\mathrm{DEF}(R)$.
  - Adding the two gives $P(H)\ge P(R)$.
  - $R$ is induced, so $R\in C_3$ by heredity. It is nonempty, since it contains $e'$. And $n(R)+m(R)<n(H)+m(H)$. So minimality gives $P(R)\ge0$, which contradicts $P(H)<0$ (0.2(F)).
- *The remark "no minimum transversal of $R$ meets $\partial(X)$".* Correct by the same argument, applied to any minimum transversal of $R$ that contains a vertex of $\partial(X)$.
  - "Equivalently $\tau(R+e')=\tau(R)+1$ for every pendant replacement" is also correct. Forward: new vertices lie only on $e'$. Converse: the one-vertex pendant $R+\{u,z_1,z_2\}$ lies in $C_3$ by 5.3.
  - The remark holds for every $X$ with $\lvert E^*(X)\rvert=\lvert X\rvert+1$, because H.1 does (see above). L024 0.5, however, states H.1 only for the optimal $X$ (N4).
- *Exhaustiveness of 5.6.* The cases are:
  - minimum $\ge2$: this is (E+);
  - $\partial(X)=\emptyset$: (G2-iii), by (c) and (d);
  - $\partial(X)\neq\emptyset$ and $\lvert X\rvert=3$: (G2-ii), by (a);
  - $\partial(X)\neq\emptyset$ and $\lvert X\rvert\le2$: either some 3-subset of $\partial(X)$ is in $E(R)$ (impossible, as above), or some new 3-subset is addable within $C_3$ (impossible by L021 (H$_3$), which needs $\lvert\partial(X)\rvert\ge3$ and holds since a 3-subset exists), or neither, which is (G2-i).

  (G2-i) as stated still contains the impossible existing-edge configurations. That only makes the hypothesis R1 cover more than it must, which is harmless.

**R2 for every minimal apex.**
- The proofs of Lemma A(a) (3.1–3.2), Lemma A(b) (4.3–4.6) and Lemma A+ (4.7) use the choice of $v$ only through minimality: kind (i) of 3.2, and $\lvert V(F_w)\rvert\ge\lvert V(F_v)\rvert$ in 7.3. So they hold for each minimal apex.
- Theorem 6 (7.1) fixes an arbitrary minimal apex $v$, applies Lemma A+ to it, and needs R2 to exclude (β) and (δ) *for that $v$*. The universal form is exactly that.
- The existential form ("some minimal apex is in (α)") would also do, with 7.1 choosing that apex, as the remark says.
- The spec's cruder form ("no minimal counterexample with $25\le n\le66$") implies universal R2, because (β) and (δ) have $n\le46$ and a minimal counterexample has $n\ge25$.

**W2 (7.3), derived from the proofs of (β) and (δ).**
- *(β).* $w\in V(F_v)$ has $d_H(w)=3$ and is not a co-vertex. So all three edges at $v$ avoid $w$. Since $v\in V(F_w)$ (Lemma A(a)) and $F_w$ is a component, hence induced, of $H-w$, these three edges are edges of $F_w$. Every component $D_i$ of $H-v$ other than $F_v$ contains an outer co-vertex of some $e_j$ (4.1), so $V(D_i)\subseteq V(F_w)$ by (4.2). The edges of $D_i$ avoid $w\in V(F_v)$, so they are edges of $F_w$. Every edge of $H$ either contains $v$ (one of $e_1,e_2,e_3$, in $E(F_w)$) or lies in a component of $H-v$ (in $E(F_v)$ or in $E(D_i)\subseteq E(F_w)$). Hence $E(H)=E(F_v)\cup E(F_w)$ and $V(H)=V(F_v)\cup V(F_w)$ (with $v\in V(F_w)$). The union is not disjoint in general.
- *(δ).* $w\in e_j$ and $w'\in e_k$, with third index $l$.
  - $e_k,e_l\in E(F_w)$ and $e_j,e_l\in E(F_{w'})$, by (4.2) and inducedness.
  - A component $D_i$ containing the outer co-vertex of $e_k$ or $e_l$ lies in $F_w$, edges included (they avoid $w$). The at most one remaining component $D^\circ$ lies in $F_{w'}$, edges included (they avoid $w'$).
  - Hence $E(H)=E(F_v)\cup E(F_w)\cup E(F_{w'})$, and $V(H)$ is the union of the three vertex sets.
- The side conditions $\lvert V(F_w)\rvert,\lvert V(F_{w'})\rvert\ge\lvert V(F_v)\rvert\ge8$ hold. Minimality gives the first inequality. For the second, $Z\neq\emptyset$ excludes $E_1$, because every vertex of $E_1$ has $H$-degree at most 2 by (4.1).
- So the statement "the proofs of (β) and (δ) give …" is true, but those proofs as written (4.7) state only $V(H)\subseteq\ldots$. The two lines above are needed (N3).

**Theorem 4 parenthetical.** Under (AH), Lemma 1(b) makes $F_v$ a component of $H-v$. If $H-v$ is connected then $H-v=F_v$ and $n\le18<25$, so Theorem 4's conclusion is immediate and Theorem 4 is not needed in 7.1. Correct. 7.4's "H − v is disconnected (Theorem 4)" is descriptive and also immediate under (AH).

## Checks performed

All checks were run with `nice -n 10`, under `timeout`, one process at a time, in experiments/referee/L024-round2-opus/.

1. **Diff audit.**
   - `git show 5da1199` and `git show --word-diff=plain 5da1199 -- results/proofs/L024-kt-reduction.md`: every change listed in the table above, and nothing else.
   - `git diff 5da1199 HEAD --stat -- results/proofs/L024-kt-reduction.md experiments/prover/L024/` is empty, and `git status --short` on those paths is clean.
   - `grep -n "^import\|^from\|sys.path\|from kt" experiments/prover/L024/*.py`: only pieces_info.py inserts experiments/prover/L021 into the path and imports kt.py.
2. **C5 coverage.** I read the `richcheck` branch of pattern_a3.py. It runs $(E_1,E_1,T_0)$ and $(E_1,E_1,T_3)$, the 7 pairs $(E_1,T_x,T_y)$ with $\{x,y\}\cap\{0,3\}\ne\emptyset$, and the 16 triples $(T_x,T_y,T_z)$ that meet $\{0,3\}$. These are the 25 type triples with a rich piece, pieces of at most 10 vertices, and $\sum W\ge36$. Without the weight condition there are $\binom{9}{3}-\binom{7}{3}=84-35=49$ such type triples.
3. **Re-run of C4 with the new output argument.**
   - Command: `timeout 1200 nice -n 10 python3 -B /home/user/Erdos-757/experiments/prover/L024/pattern_a3.py poor 0 <scratch>/rerun_poor_results.json` (run from my scratch folder; `-B` writes no bytecode into the prover's folder).
   - Log `rerun_poor_log.txt`: `poor TOTAL {'type_triples': 12, 'g_choices': 783, 'configs': 359, 'claimE': 206, 'inC3': 206, 'inC3_claimE': 206, 'tau_ok': 206, 'Pneg': 0}`, `done [308s]`, `exit 0`.
   - The scratch JSON and the evidence file `pattern_a3_poor_results.json` have equal totals and an identical multiset of the 359 configuration records.
   - The evidence file is untouched: sha256 `8eda7096…5b03c2`, mtime 08:18:27 UTC, git status clean.
   - This is a re-run of the prover's code, not an independent computation. Independent reproductions of C4 are in both round-1 reviews.
4. **Lemma A+ case split, exhaustive local check.**
   - Command: `timeout 1200 nice -n 10 python3 -B check_r2.py 20000 > check_r2_output.txt`, Part A.
   - For every piece $F$ of $L^*$ it enumerates all sets of three pairwise disjoint nonempty traces. Each trace has size 1 or 2. A 2-trace may not lie inside an edge of $F$ (linearity), and $d_F(u)+[u\text{ in a trace}]\le3$.
   - It computes $Z$ through (4.1) and classifies the case.
   - Output: `PART A TOTAL {'alpha': 1, 'beta': 322785, 'gamma': 0, 'delta': 488} BAD 0`.
   - (γ) never occurs. (α) occurs only for $E_1$, with singleton traces and all $H$-degrees 2. (β) occurs exactly for the pieces with a vertex of degree 3. (δ) occurs **only for $(8,5,3)\#0$**, which gives N5.
5. **(4.1), (4.2) and the W2 vertex and edge statements, random structural test.**
   - Same command, Part B. It generates random connected linear 3-graphs with $\Delta\le3$, built as an apex $v$ over a random $F$, with extra components attached through outer co-vertices, possibly sharing a component.
   - For every degree-3 $v$ and every component $F$ of $H-v$ met by all three edges at $v$, it tests:
     - (4.1);
     - (4.2) for each $w$ used;
     - $V(H)=V(F)\cup V(K_w)\,[\cup V(K_{w'})]$;
     - $E(H)=E(F)\cup E(K_w)\,[\cup E(K_{w'})]$.

     Here $K_w$ is the component of $H-w$ containing $v$; in L024, $F_w=K_w$ by Lemma A(a).
   - Output: `PART B {'graphs': 4242, 'apex_cases': 39686, 'alpha': 716, 'beta': 36519, 'gamma': 259, 'delta': 2192, 'beta_nontrivial': 11315, 'delta_nontrivial': 1034} BAD 0`. "Nontrivial" means $H-v$ has components other than $F$. (γ) occurs here because $F$ is an arbitrary graph, not a piece.
6. **The new 5.6 closure and the referee remark, numeric test.**
   - Command: `timeout 1800 nice -n 10 python3 -B check_56.py 20000 > check_56_output.txt` (216 s).
   - It builds random assemblies $H=R\cup X\cup E^*$ with $n\le14$ and $X\in\{\{E_1\},\{E_1,E_1\},\{(8,5,3)\#b\},\{E_1,(8,5,3)\#b\}\}$. There are $\lvert X\rvert+1$ edges in $E^*$, each with at most 2 vertices on each member, and $H$ is linear with $\Delta\le3$.
   - $\tau$ and the minimum transversals are computed by exact branching. DEF is computed **exactly** over all $L^*$-families: all induced copies of all pieces with at most $n$ vertices, that is $E_1$, $(8,5,3)$ and $(10,7,4)$, found with my own isomorphism test.
   - Output: `CHECK 5.6 {'inst': 18854, 'claimE': 17323, 'H1_ok': 42775, 'H1_fail': 0, 'hyp': 8359, 'tau_ok': 8359, 'P_ok': 8359, 'ctrl': 8870, 'ctrl_P_lt': 1721, 'ctrl_tau_plus1': 1721, 'bd_empty': 94, 'edge_in_bd': 610, 'edge_in_bd_ok': 610} BAD 0`.
   - H.1 held in all 42,775 (instance, edge) cases with Claim E on the subfamilies.
   - In all 8,359 instances where some minimum transversal of $R$ meets $\partial(X)$, $\tau(H)\le\tau(R)+\sum\tau_F$ and $P(H)\ge P(R)$.
   - In all 610 instances of the exact new case (an edge of $R$ inside $\partial(X)$), $P(H)\ge P(R)$.
   - Control: when no minimum transversal of $R$ meets $\partial(X)$, $P(H)<P(R)$ in 1,721 of 8,870 instances. So the test can fail, and the hypothesis of the closure is what makes the inequality hold.
7. **Hand verification.** I checked by hand every passage in "Re-verified passages" and the unchanged parts the new text relies on: L021 Definition 2, 0.3, 0.5, 3.2, 8.1, 8.3, (H$_3$), and L024 4.1–4.7.

## Remaining problems, in order of severity

None is a mathematical error. N1–N3 should be fixed before the certificate is recorded.

- **N1 (fix; round-1 fable item 3 only partly applied).** The C5 bullet of "Computer-verified steps" still says "All 25 type triples with a rich piece and pieces of at most 10 vertices". So does the Sanity-checks bullet "Lemma 2 on data: for every type triple with a rich piece (and pieces of at most 10 vertices) …". As worded, both claim coverage of all 49 such type triples. C5 ran exactly the 25 with $\sum W\ge36$ (check 2), so the computation is right and only its description is wrong. Fix: add "with $\sum W\ge36$" in both places, as was done in 6.3. Not load-bearing.
- **N2 (fix; new text).** Step 5.6 cites "(0.5/L021 0.5)" for $\mathrm{DEF}(H)\ge\mathrm{DEF}_H(X)+\mathrm{DEF}(R)$. L024's 0.5 is Proposition 8. The union-of-families fact is L024 **0.1** (= L021 0.5). Fix: "(0.1/L021 0.5)".
- **N3 (fix; new text).** 7.3 says "the proofs of (β) and (δ) give $E(H)=E(F_v)\cup E(F_w)$ …". The proofs in 4.7 give only the vertex statements. The edge statement is true, but needs the line given above under "Re-verified passages": the edges at $v$ avoiding $w$ are edges of the induced component $F_w$ (resp. $F_{w'}$), and every other edge lies in $F_v$ or in some $D_i$ inside $F_w$ (resp. $F_{w'}$), avoiding $w$ (resp. $w'$). Fix: add this line to 4.7 (β) and (δ), and preferably put the edge statement into Lemma A+ itself, as round-1 fable suggested. Not load-bearing: it specifies the open GAP R2.
- **N4 (cosmetic).** The bracketed referee remark in 5.6 claims its conclusion "for every $X$ with $\lvert E^*(X)\rvert=\lvert X\rvert+1$". That needs H.1 for such $X$, while L024 0.5 states H.1 only "for $X$ as in Proposition 3". The claim is true, because L021 8.1's proof uses only $\lvert E^*(X)\rvert=\lvert X\rvert+1$, Claim E for subfamilies and (L1). Add that clause, or restrict the remark to the optimal $X$. A bracketed referee remark inside a proof would also read better as a separate Remark.
- **N5 (suggestion; sharpening, not required).**
  - In case (δ), every vertex of $Z$ is a co-vertex. So $\Delta(F_v)\le2$: vertices outside $Z$ have $H$-degree at most 2, and vertices of $Z$ have $F_v$-degree 2 by (4.1). By 0.8 and $Z\ne\emptyset$, this forces $F_v=(8,5,3)\#0$. Hence $n\le1+8+28=37$, not 46.
  - Moreover, at most one trace avoids $Z$, and that trace is then $\{0\}$, the degree-1 vertex.
  - In case (β), $F_v$ has a vertex of degree 3, so $F_v\notin\{E_1,(8,5,3)\#0\}$.
  - Check 4 confirms this: (δ) local configurations exist only for $(8,5,3)\#0$.
  - This shrinks the W2 enumeration considerably.
- **N6 (cosmetic).**
  - Theorem 6's hypothesis list and DEPENDS ON still say "L021 Theorems 1–6" although Theorem 5 is unused. This over-assumes, which is harmless, and the closing list states it.
  - The certificate's C4 command does not mention the new optional output argument (the README does). With the default, a re-run still writes the evidence file, but check 3 shows that it rewrites identical content.
  - The new Theorem 4 parenthetical ("for $n\le17$ it also follows from the completeness of the cells …") rests on the completeness of L021's cell$(\cdot,\cdot,\cdot,3)$ lists (L021 Definition 2 and Theorem 7(i), unrefereed computations). I did not re-verify it. It is not load-bearing: Theorem 4 is not used in Theorem 6, and the search covers $n\le17$ directly.

## Independence statement

All new checks use my own code in experiments/referee/L024-round2-opus/: `rlib2.py`, `check_r2.py` and `check_56.py`, with outputs `check_r2_output.txt`, `check_56_output.txt` and `check_56_small_output.txt`. None imports e757, the judge, hyp24.py or L021's kt.py. Only the edge lists of the 32 pieces in experiments/prover/L021/closure_results.json were read, as data.

Check 3 re-ran the prover's own pattern_a3.py, to test the round-1 fix, writing only into my scratch folder (`rerun_poor_log.txt`, `rerun_poor_results.json`). It is a reproduction, not an independent computation.

I read both round-1 reviews, as instructed. I did not open any other round-2 review: an untracked file results/reviews/L024-kt-reduction__referee__20261027T103204Z.md appeared during my work, and I left it unread and untouched.

I modified nothing outside my scratch folder and this review file. The scratch folder is 120 KB.
