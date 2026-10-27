VERDICT: NEEDS-WORK
(Workflow category: ACCEPT WITH FIXES. My referee rules allow only ACCEPT, REJECT and NEEDS-WORK, and they say that any remaining fixable problem means NEEDS-WORK. Every round-1 item is applied correctly. The completion of Theorem 7(v) is correct, and so is every other step I checked. What remains is purely editorial: one wrong constant in an unedited inequality of Step 8.4, which the round-1 referees missed and whose conclusion is still true; one incomplete sentence in the KT* remark; two wording points in the README and the DEPENDS block. No theorem is affected.)

Referee #3, round 2. Certificate: results/proofs/L021-i11-deficiency-route.md as revised in commit 22e95c9. The certificate and experiments/prover/L021/README.md are unchanged between 22e95c9 and HEAD (`git log` and `git diff 22e95c9 HEAD` on both files). Scratch folder: experiments/referee/L021-round2-opus/.

## Summary

The certificate is PARTIAL and says so. It proves Theorems 1 to 6 and Propositions 8 and 9, verifies Theorem 7 by computation, and leaves Conjecture KT* (hence $c_*\ge35/66$) open as G1 to G4. Round 1 asked for one mathematical completion and a set of editorial fixes:
- the disconnected distribution in Theorem 7(v);
- the I11 qualification of the saturated-graph note;
- labelling KT* as a new conjecture;
- the sign of $A$ for hypertrees with a perfect matching;
- the scope of "32 pieces";
- the DEPENDS block;
- the README's claim that Theorem 6 is new;
- the (H$_3$) wording.

I read the whole diff of 22e95c9: 13 hunks in the certificate and one two-line hunk in the README. Every requested item is applied correctly. All edits are editorial except the new paragraph of Step 7.6, the L016 argument for the case where all three hub pairs lie in one piece. I verified that argument in full and it is correct. I also brute-forced it on all 32 pieces with my own code: 123,582 hub configurations, 74 of them raise $\tau$, and none of those 74 lies in $C$. I re-derived every edited formula by hand and with exact integer code. I recomputed the 18 graphs of cell$(27,13,9,3)$ independently: $A=-4$, DEF $=4$ and $A+\mathrm{DEF}=0$ for each. I also enumerated that cell from scratch by its structure and found exactly 18 isomorphism classes, matching the stored list one-to-one.

I spot-checked three unedited results adversarially, by hand and numerically. These are the Hall exchange 3.4 (247,521 Hall-violating sets tested), the case split 4.3 (integer brute force), and the Tutte–Berge step of Theorem 6 (513 graphs and all 3,966 Tutte–Berge sets for $N\le10$, with the explicit family of 6.4 validated each time). All are correct.

The only new defect is in the unedited Step 8.4 (H$_1$). There the chain "$e_{H'}(S)\le e_R(S\setminus\{z_1,z_2\})+1\le|S|-3$ for $S\supseteq e'$" is false for $S=e'$: the left side is $1$ and $|S|-3=0$. The bound that is actually needed, $\le|S|-2$, holds, so (H$_1$) and Proposition 8 are unaffected.

## 1. Item-by-item check of the round-1 requests (commit 22e95c9)

| # | Request (round 1) | Applied? | Check |
|---|---|---|---|
| 1 | Theorem 7(v) omits the distribution with all three pairs in one piece, which makes $H$ disconnected (opus 1, fable 1). | Yes. The statement now reads "(connected or not; see Step 7.6 ...)", and 7.6 has a new paragraph. | Correct; full verification in Section 2. |
| 2 | The saturated note uses I11 beyond $n\le27$ (opus 2). | Yes. Now "for $n\le27$ ... by $s\ge0$ (I11, ... L016); for $n\ge28$ this uses I11 ... (Henning–Yeo gives only $s\ge-(3n+2)/17$), so it is unproved there. The remark is not used in any proof." | Re-derived: $m=n-2$ gives $A=12s+2n-22$, and K8 with $m=n-2$ gives exactly $s\ge-(3n+2)/17$ (arith.py). The fix is needed: the Henning–Yeo floor alone allows $A<0$ for every $n\ge11$, so L016 is really used for $n\le27$. |
| 3 | Label KT* a NEW conjecture, not known to follow from or imply I11 (opus 3, fable 4). | Yes, in CLAIM-TYPE and in the new "Remark (status of KT*)". | Content checked in Section 3. |
| 4 | Sign typo: $A=3k-16$ (opus 4, fable 2). | Yes. | Re-derived in Section 3. |
| 5 | Scope of "32 pieces" (opus 5, fable 3). | Yes, in the title and README line 16: "among the connected members of $C_3$ with at most 24 vertices; at most 27 by the unrefereed run ...". | Every other "32" in the certificate (lines 30, 66, 127, 131, 159, 163, 164) is either about the fixed list $L^*$ or already scoped to $n\le24$ by 7.1–7.2. |
| 6 | DEPENDS: L017 status, and the missing uses of L016 (opus 6, fable 5b). | Yes. L017 is "[ACCEPTED, K64 ...]". The uses of L016 now listed are: the cell scan, $J_{1/6}$ of the pieces, Proposition 9 (9.2, 9.3), and 7.6. | Matches kb/known_results.md: K61 = L016; K64 = L017 Theorems 1–6, ACCEPT x2 in round 2; K67/K68/K69 = L018/L019/L020 as described. Cosmetic point in Section 5, item 4. |
| 7 | README: Theorem 6 is not "new" (opus 7). | Yes. The README now cites Henning–Yeo EJC 2017 Prop. 9 and Chvátal–Hanson, says "not claimed as new" and leaves novelty to the scout. | Cosmetic point in Section 5, item 3. |
| 8 | (H$_3$): $e'$ must be a new edge (fable 5a). | Yes: "a new edge (not in $E(R)$, $R=H-V(X)$)". | This narrows (H$_3$) to what 8.2 proves: the count $m(H)=m(H')-1+\dots$ needs $e'\notin E(R)$. The case $e'\in E(R)$ is still listed in G2 ("an edge of $H-V(X)$ containing two vertices of $e'$"), so nothing is lost. |
| 9 | (suggestion) G2 is narrower than stated (opus 8). | Added to G2 as "Referee's observation ..., [heuristic] until checked". | I re-derived it; it is correct (Section 3). The tag is conservative and could be upgraded to [derived-here]. It sits inside a GAP and nothing uses it. |

The other hunks are also editorial: STATUS, the "Not used" line, and README line 16. Nothing else changed: no theorem statement other than 7(v) and (H$_3$), and no proof step other than 7.6.

## 2. The completion of Theorem 7(v): full verification

Setting: $H\in C_3$, $d_H(v)=3$, $H-v=F_1\sqcup F_2$ with $F_i$ isomorphic to members of $L^*$, and $\tau(H)=\tau(H-v)+1$.

- **When does this case arise, and is it the only one missing?** Each pair $P_j=e_j\setminus\{v\}$ is of type "inside $F_1$", "inside $F_2$" or "split".
  - $H$ is disconnected exactly when no edge at $v$ meets both pieces, that is, when all three pairs are inside one piece. A split pair, or pairs inside different pieces, connect $F_1$ and $F_2$ through $v$.
  - L017 7.3 lists exactly the five $r=2$ multisets other than $\{1,1,1\}$ and $\{2,2,2\}$, which it excludes by Theorem 4(ii) (every component meets a pair, i.e. $H$ is connected).
  - So the new paragraph covers exactly the missing distributions. The parenthetical "excluded by L017 Theorem 4(ii) when $H$ is connected, which is the only case L017 7.3 lists" is accurate. I checked it against L017 lines 50–67 and 7.2–7.3.
- **Why $B:=H[V(F_1)\cup\{v\}]$ is in $C$.**
  - $B$ is an induced subgraph of $H\in C_3\subseteq C$.
  - Linearity and $F_7$-freeness pass to subgraphs.
  - (P3) passes to induced subgraphs because $e_B(S)=e_H(S)$ for $S\subseteq V(B)$ (L017 0.2).
  - $\Delta\le3$ is not needed for this step.
  - The word "so" in "so $H[V(F_1)\cup\{v\}]\in C$ (heredity)" is misplaced: membership follows from heredity, not from the $\tau$ statement before it. This is cosmetic.
- **Why $\tau$ rises by exactly 1.**
  - $H=B\sqcup F_2$, because all three edges at $v$ lie inside $V(F_1)\cup\{v\}$ and $F_2$ is a component of $H-v$.
  - $H-v=F_1\sqcup F_2$.
  - By additivity of $\tau$ over components (0.1), $\tau(B)+\tau(F_2)=\tau(H)=\tau(H-v)+1=\tau(F_1)+\tau(F_2)+1$, so $\tau(B)=\tau(F_1)+1$.
- **Why $B$ has at most 18 vertices, and its slack.**
  - $n(B)=n(F_1)+1\le18$, since every piece has at most 17 vertices.
  - $m(B)=m(F_1)+3$: $H[V(F_1)]=F_1$ because $F_1$ is induced in $H-v$, which is induced in $H$; all three $v$-edges lie inside $V(F_1)\cup\{v\}$; and no edge of $F_2$ meets $V(F_1)$.
  - Hence $s(B)=s(F_1)+3+6-11=s(F_1)-2$.
  - The pieces have $s\in\{0,1\}$. I recomputed this for all 32 with my own $\tau$ (hypertrees.py, first line of output). So $s(B)\le-1<0$.
- **Why L016 applies.** L016 (K61) states I11 for all members of $C$ with at most 27 vertices. $B\in C$, $n(B)\le18\le27$ and $s(B)<0$ give a contradiction, so the case is empty.
- **The rest of (v) is unchanged and still correct.**
  - In the connected case, L017 7.3–7.4 with free choice from (L1) apply.
  - The role tables were recomputed independently by both round-1 referees.
  - (b) gives $F_7$, (e) gives cell$(17,13,7,3)\subseteq L^*$, and (c1), (c2), (f) are impossible.
  - The consequence for (D2) in a minimal counterexample, which is connected by 3(A), follows from 4(a) and 3(C).
- **Numerical confirmation (disc_case.py; own code).** For every one of the 32 pieces $F$ I took every set of three pairwise disjoint pairs of vertices of $F$-degree $\le2$ with no pair inside an edge of $F$, which is what $H\in C_3$ forces.
  - I built $B$ and computed $\tau(B)$ directly by branching.
  - I compared it with the criterion "no minimum transversal of $F$ meets the three pairs".
  - For each $\tau$-raising $B$ I tested $F_7$-freeness and (P3).
  - Result: 123,582 configurations, 0 disagreements between direct $\tau$ and the criterion, and 74 $\tau$-raising configurations: $(8,5,3)$#0 15/49, #1 13/22, and 2 or 6 for 17 of the 19 $(15,11,6)$ classes. Each has $s(B)=s(F)-2<0$ (asserted), and **none of the 74 lies in $C$**.
  - The $(8,5,3)$ counts agree with L017 C9.
  - The certificate's own sentence ("410 of the 528 piece pairs") understates the evidence. This case depends only on $F_1$, so the single-piece brute force covers all 528 pairs.

## 3. Re-verified edited passages (by hand and by arith.py, exact integers/Fractions)

- **Definition of $A$.** I checked $A=27n+35m-132\tau=12s-9n+11m=12(s+n/6-11(n-m)/12)$ on a grid. The weights are 16, 5, 13, 2, 10, and the slacks are 0, 1, 0, 1, 0. $J_{1/6}$ and $W\le11(n-m)$ hold for all five types. $A(14,12,6)=+6$.
- **KT* remark.**
  - $(21,10,7)$: $s=63+20-77=6$, $A=567+350-924=-7$.
  - $(27,13,9)$: $s=81+26-99=8$, $A=729+455-1188=-4$.
  - Both cells are sparse: $11m<9n$ (110 < 189 and 143 < 243).
  - "I11 gives $A\ge0$ only when $11m\ge9n$" is right: $s\ge0$ gives $A\ge11m-9n$.
  - "Not known to follow from I11" is right: I11 gives $132\tau\le36n+24m$, and KT needs in addition $\mathrm{DEF}\ge9n-11m$, which nothing proves.
  - "Not known to imply I11" is right: Theorem 2 gives only $J_{1/6}$.
  - The computation summary agrees with experiments/20261027-0730-kt-cells/README.md, results.json and closure2_output.txt: 43 cells with $A<0$, 346 graphs, 13 non-empty cells, 32 irreducible pieces, 314 equality cases, no new piece.
  - My own scan (scan.py) gives the same 43 triples: 32 with $n\le24$, and 11 with $n\ge25$, namely (25,12,9), (25,13,9), (25,14,9), (25,18,10), (26,13,9), (26,16,10), (26,17,10), (27,13,9), (27,15,10), (27,16,10), (27,20,11).
  - The remark lists only three of the cells newly computed as empty and omits the three reused ones (Section 5, item 2).
- **cell$(27,13,9,3)$, own code (hypertrees.py, enum_hypertrees.py).** All 18 stored graphs satisfy:
  - $n=27$, $m=13$, distinct edges, connected, linear;
  - $\Delta=3$ for 15 of them and $\Delta=2$ for 3;
  - (P3), checked both over all $2^{13}$ edge subsets and by the surplus-2 Hall test;
  - $F_7$-free;
  - $\tau=9$ by branching, and a unique perfect matching.

  An induced-copy search for all 32 pieces (edge-subset enumeration plus typed incidence-graph isomorphism) finds only the 13 copies of $E_1$. Exhaustive maximisation over disjoint families gives DEF $=4$, attained by the perfect matching ($9\cdot16-35\cdot4$). Then $A=-4$ and $A+\mathrm{DEF}=0$ for all 18, and the 18 are pairwise non-isomorphic.

  Independent enumeration of the cell:
  - A connected 3-graph with $n=2m+1$ is a hypertree.
  - König's property gives $\tau=\nu$, so the graph has a perfect matching of 9 "blocks" plus 4 connectors.
  - The connectors form a block-level hypertree, and $\Delta\le3$ means at most 2 connectors per block vertex.
  - Over 105 growth sequences and 843 structures this gives **exactly 18 isomorphism classes, each matching exactly one stored graph**.
- **Sign fix.** With $n=6k+3$, $m=3k+1$, $\tau=2k+1$: $A=162k+81+105k+35-264k-132=3k-16$. The matching family has $2k+1$ copies of $E_1$ and $E^*$ equal to the other $k$ edges, so it gives $16(2k+1)-35k=16-3k$. Then $A+\mathrm{DEF}_H(M)=0$. More generally, for any $H$ with a perfect matching $M$ and $\tau=n/3$: $A=35m-17n$ and $\mathrm{DEF}_H(M)=17n-35m$. This confirms the closing clause of that bullet.
- **Scoped special-family statements and DEPENDS.** See items 5 and 6 of the table.
- **G2 remark ([heuristic]).** Take $p,q\in\partial(X)$ sharing no edge of $R$, with $|X|\ge3$, and $e'=\{p,q,z\}$.
  - $F_7$ has minimum degree 2, so no copy of $F_7$ uses $e'$.
  - Linearity holds.
  - For $S\supseteq e'$: $e_{H'}(S)=e_R(S-z)+1\le(|S|-3)+1$, because $|S-z|\ge2$.
  - $d(p)$ and $d(q)$ do not rise, since each loses an $E^*$ edge.
  - $n+m$ drops.
  - 8.2 with $\nu=1$ and 8.3 (both cases) go through verbatim, with $\mathrm{DEF}(H')\le16$.
  - So $A(H)\ge-16+19|X|-27=19|X|-43\ge14>0$.
  - The stated consequence for G2 is correct.

## 4. Adversarial spot-checks of unedited results

- **Theorem 3, Hall exchange 3.4 (by hand and hall_test.py).**
  - The saturating-matching branch contradicts (B).
  - $X'=\emptyset$ forces $|X^*|<|S|\le|E^*|$.
  - $E^*(X')\subseteq E^*(X^*)\setminus S$: an edge meeting $V(X')$ lies inside no member of $N_B(S)$, and edges of $S$ meet only members of $N_B(S)$.
  - This gives a strict decrease of $|E^*|-|X|$. Correct.
  - Random hosts: disjoint members, outside vertices, and extra edges meeting the members and not inside any member. Over 3,000 hosts I took **every** Hall-violating $S$ (247,521 of them) and checked the inclusion and the strict decrease. I also checked the identity $E^*_H(S')=\{e\in E^*(X^*):e\cap V(S')\ne\emptyset\}$, used in 8.1, for all 33,992 subfamilies. 0 failures.
- **Theorem 4, case split 4.3 (by hand and arith.py).**
  - The constraints are (i) $\sum W-35e_v\ge1$ and (ii) $e_v+k_v\ge j+1$, with $k_v\le3$.
  - Brute force over $j\le8$, $e_v\le24$ and all weight multisets from $\{16,13,10,5,2\}$, and separately with any $W\le16$, leaves exactly $(1,0,2)$, $(1,0,3)$, $(2,0,3)$ and $(3,1,3)$, the last with $\sum W\ge36$.
  - The largest value of $\sum W-35e_v$ is 32, which gives $A\ge-32$.
- **Theorem 6, Tutte–Berge step (by hand and thm6_check.py).**
  - By hand: the algebra $66(N+|U|-o)-16N-27M\ge35|U|+\sum\theta_i$ holds. Over all feasible $(c,e)$ with $c<200$, $\theta<0$ only for $(1,0)$ ($-16$) and $(5,7)$ ($-5$). The forced degree sequence $(3,3,3,3,2)$ gives $K_4^s$. The dual of $(8,5,3)$#0 is $K_4^s$ with the pendant at the subdivision vertex.
  - Numerically, on 513 connected subcubic $G$ (all 113 atlas graphs with $N\le7$, including $K_1$, plus 400 random graphs with $N\le16$):
    - $\tau(H)=N-\nu(G)$ and $A=132\nu-16N-27M$;
    - for **every** Tutte–Berge set $U$ when $N\le10$, and for the Gallai–Edmonds set otherwise (3,966 sets in all): $M\le3|U|+\sum e_i$, $A\ge35|U|+\sum\theta_i$, and the $\theta$ classification on the actual components;
    - the explicit family of 6.4 consists of induced copies of $E_1$ and $(8,5,3)$#0, is pairwise disjoint, and has $E^*_H(X)\subseteq U$;
    - $\mathrm{DEF}_H(X)\ge16o_1+5o_5-35|U|$ and $A+\mathrm{DEF}_H(X)\ge0$ (minimum 0); the $K_4^s$ branch occurred 8 times.
  - All assertions passed.
- **Theorem 3(B), Theorem 1(a,b), Theorem 2.2, Proposition 8 (8.2, 8.3, (H$_0$)) and the "Closes" balance (0, $-35$, $-70$).** Re-read line by line. Correct, except for the slip below.
- **New finding, Step 8.4 (H$_1$) (unedited text).** "$e_{H'}(S)\le e_R(S\setminus\{z_1,z_2\})+1\le|S|-3$ for $S\supseteq e'$" fails at $S=e'=\{u,z_1,z_2\}$: there $e_{H'}(S)=1$ and $|S|-3=0$, since (P3) for $R$ does not apply to the one-element set $\{u\}$. For $|S|\ge4$ the chain is right. (P3) needs only $\le|S|-2$, which holds for every $S$. So $H'\in C_3$ and the conclusion of (H$_1$) stand. Fix: replace "$\le|S|-3$" by "$\le|S|-2$" (or "$\le|S|-3$ for $|S|\ge4$, and $=1=|S|-2$ for $S=e'$").

## 5. Remaining problems (in order of severity; all editorial)

1. **Step 8.4 (H$_1$), wrong constant in the (P3) chain.** The inequality is false for $S=e'$, as shown in Section 4. The conclusion is true and no result changes. One-symbol fix.
2. **KT* remark, incomplete list of cells.** It says the new cells (25,14,9,3), (26,17,10,3) and (27,20,11,3) are empty. It does not say that the extension to $n\le27$ also relies on (26,13,9,3), (27,15,10,3) and (27,16,10,3). These three were reused as empty from experiments/20261027-0340-induction-n28-n29-f25, which is also unrefereed (kt-cells README, "Reused empty"). The certificate tags the computation unrefereed, so this is not misleading, but one clause should name them. Optional: "It is untested for $n\ge28$" would be more precise as "no computational test of KT for $n\ge28$ (Theorem 6 proves the case $\Delta\le2$ for all $n$)".
3. **README line 19 wording.** "a consequence of Henning–Yeo ... Prop. 9 ... plus Chvátal–Hanson-type matching bounds" asserts that Theorem 6 can be derived from those results, and no such derivation is given. Chvátal–Hanson alone does not give it: the $(9,4,3)$ star dual has $A=-13$ and needs the deficiency term. The proof in the certificate uses Tutte–Berge directly. "Closely related to" would be accurate. The disclaimer "not claimed as new; novelty left to the scout" is fine. Also, README "Computations needed" item 2 is stale: the unrefereed kt-cells run did those cells.
4. **DEPENDS cosmetic.** The Δ ≤ 2 formula $\tau=m-\nu(G)$ is L017 Theorem 7, which kb/known_results.md records as K65, not K64. The line cites only K64. Two smaller wording points: STATUS says "revised ... 09:10 UTC" while the commit is 09:08:40 UTC; and the misplaced "so" in 7.6 (Section 2).

Outside these items, everything presented as proved is proved. That covers Theorems 1–6, Propositions 8 and 9, Theorem 7(i)–(v) as computations, now including the disconnected case of (v), and the "Closes" list. The GAPs G1–G4 remain as marked, so KT* and $c_*\ge35/66$ are not proved, and the certificate says so.

## 6. Commands and outputs (all in experiments/referee/L021-round2-opus/, one process at a time, nice -n 10, each under timeout)

- `git show 22e95c9`, `git log --oneline -- <certificate> <README>`, `git diff 22e95c9 HEAD --stat -- <certificate> <README>`: the diff was read in full; there are no later edits.
- `timeout 300 nice -n 10 python3 arith.py` → arith_output.txt: 44 exact checks, 0 failures, `ALL OK`. They cover:
  - the $A$ identity;
  - the five types (W, s, $J_{1/6}$, and the 7.6 slack $s(B)=s(F)-2<0$ with $n(B)\le18$);
  - the remark cells;
  - hypertrees with $k=0..11$;
  - the saturated note and the Henning–Yeo floor;
  - 35/66 > 9/17, and $\varepsilon<3/17$;
  - the hub balances;
  - the 4.3 brute force;
  - the $\theta$ table and the 6.2 algebra.
- `timeout 900 nice -n 10 python3 hypertrees.py` → hypertrees_output.txt: the 32 pieces re-verified; 18/18 graphs OK; `A values [-4], DEF values [4], A+DEF values [0]`; pairwise non-isomorphic; `ALL OK`. A first run, which also enumerated all minimum transversals ($\binom{27}{9}$ subsets), was stopped as too slow after 3 graphs; those 3 graphs agreed.
- `timeout 900 nice -n 10 python3 enum_hypertrees.py` → enum_hypertrees_output.txt: `structures built: 843 isomorphism classes: 18`; each stored graph matched by exactly one class; `ALL OK`.
- `timeout 600 nice -n 10 python3 disc_case.py 10`, then `timeout 1800 nice -n 10 python3 disc_case.py 17` → disc_case_17_output.txt: `TOTAL configs=123582 tau-raising=74 tau-raising in C=0 criterion/direct-tau mismatches=0`, `ALL OK` (526 s).
- `timeout 1200 nice -n 10 python3 thm6_check.py 400 16 20261027` → thm6_check_output.txt: `graphs 513, U_sets 3966, minP 0`; no assertion failed.
- `timeout 600 nice -n 10 python3 hall_test.py 3000 7` → hall_test_output.txt: `Hall-violating S checked=247521 subfamilies checked=33992: ALL OK`.
- `timeout 60 nice -n 10 python3 scan.py` → scan_output.txt: 43 candidate triples, 32 with $n\le24$, and the 11 with $n\ge25$ as listed in Section 3.

Nothing was extracted; the scratch folder is under 100 KB.

## 7. Independence statement

My scripts (rlib.py, arith.py, hypertrees.py, enum_hypertrees.py, disc_case.py, thm6_check.py, hall_test.py, scan.py) import only networkx and my own rlib.py. They import nothing from e757/, judge/, experiments/prover/L021/ (kt.py and the others) or the round-1 referees' folders.

- **How things are computed.**
  - $\tau$: branching on an uncovered edge.
  - Minimum transversals: brute force over $\tau$-subsets.
  - (P3): edge-subset enumeration and a surplus-2 Hall reduction.
  - $F_7$: 5-edge subsets on 7 vertices plus isomorphism.
  - Induced copies: edge-subset enumeration plus typed incidence-graph isomorphism.
  - DEF: exhaustive over disjoint families.
  - $\nu$ and Tutte–Berge sets: networkx matching plus exhaustive or Gallai–Edmonds sets.
- **Data read.**
  - The 32 piece edge lists in experiments/prover/L021/closure_results.json, whose $n$, $m$, $\tau$, $W$ and $s$ I re-verified;
  - the list experiments/20261027-0730-kt-cells/lists/cell_27_13_9_D3.txt;
  - for comparison only: that folder's README.md, results.json and closure2_output.txt.
- **Documents read.** I read the two round-1 reviews (as instructed), the certificate in full, the commit diff, L017 Theorem 4 and Steps 7.1–7.4, the README of experiments/prover/L021/, and kb/known_results.md rows K61 and K64–K69.
- **Not read.** A third L021 review (results/reviews/L021-i11-deficiency-route__referee__20261027T092532Z.md) appeared while I was working. I have not read it, and nothing here depends on it.
- **Files written.** Only this review and my scratch folder.

Review written 20261027T093649Z by referee #3 (round 2), claude-opus-5-5.
