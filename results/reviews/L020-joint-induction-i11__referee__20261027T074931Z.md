VERDICT: NEEDS-WORK

# Referee #3 (opus), round 2: results/proofs/L020-joint-induction-i11.md (revision in commit ef5c9dc)

**Verdict mapping.** My referee rules allow only ACCEPT, NEEDS-WORK or REJECT on the first line, and they reserve ACCEPT for a document in which no problem remains. In the commissioning workflow's vocabulary this verdict is **ACCEPT WITH FIXES**:
- every remaining item is editorial;
- I found no mathematical error;
- no theorem statement needs to change in substance.

I did not use the requested first line `VERDICT: ACCEPT WITH FIXES` for two reasons. My rules forbid it, and it begins with the prefix `VERDICT: ACCEPT` that scripts/status.py tests for.

## Summary

I checked the revision against the three round-1 reports:
- opus NEEDS-WORK, results/reviews/L020-joint-induction-i11__referee__20261027T072810Z.md;
- fable ACCEPT WITH FIXES, results/reviews/L020-joint-induction-i11__referee__20261027T064109Z.md;
- scout PARTIAL, results/reviews/L020-joint-induction-i11__scout__20261027T064642Z.md.

**The diff.** Commit ef5c9dc is the only change to the certificate since its submission (db005b4). The working tree equals HEAD for this file. The diff has seven hunks:
1. STATUS and DEPENDS ON;
2. Definitions, Theorem 1 and Theorem 2;
3. Observation 7 and Tags;
4. Remark 4.7;
5. Step 6.1;
6. C3;
7. C8.

**The requested fixes.** Every required item of the two referees and the scout is applied, and correctly in substance:
- **Theorem 1 counts.** My own code, run on all 495 degree-3 vertices of the 45 classes, confirms the counts now written in Theorem 1, which also agree with the opus tables:
  - all 45 classes have a pattern-(e) vertex;
  - every class has exactly three $\Theta$-vertices;
  - 27 classes have an (f)-vertex with $K-v=(10,7,4)\sqcup(18,13,7)$;
  - 31 classes have a (b)-vertex with $K-v=E_1\sqcup(25,19,10)$.
- **The b-configuration table** in the Definitions agrees with the opus table and with my own recount.
- **Remark 4.7.** The new exclusion of the cell $(30,15,11)$ is correct.
- **Unchanged statements.** No statement of Theorems 2–4, Corollary 5, Proposition 6 or Observation 7 changed. Theorem 2 changed only its tag and citation. The only proof-text changes are the two requested rewordings.

**What goes beyond editing.** Two additions are more than editing:
- the Theorem 1 "Characterisation", which is true (I re-derived it) but is proved nowhere in the certificate;
- the Remark 4.7 clause, which is correct.

**Spot checks of unedited results.** I tested Theorem 3 on a stratified sample of 30 stored degree-3 instances, and on all 495 vertices of the 45 classes. I tested Proposition 6 on all 204 stored NC pairs. There were 0 failures. The Proposition-6 check exposed one false sentence in proof step 5.2: "1+2+2=5 vertices" should be "at most 5", and 21 of the 95 instances have 4. This is harmless for the statement.

**Remaining problems.** Eight editorial items remain, listed at the end. Items 1 and 2 should be fixed before ACCEPT; items 3–6 are small corrections of fact or wording; items 7–8 are wording and cosmetic.

## Item-by-item check of the round-1 requests

### fable (ACCEPT WITH FIXES)

**F1: stale statuses. Applied.**
- **L017.** The entry now reads "[Theorems 1-6 verified-here, ACCEPT x2, K64; Theorem 7 published, re-proved]", with C5, Corollary 13.3 and C4 marked as unrefereed computations. This matches the LEDGER row K64-K65, whose note reads "Corollaries 13.3, 13.5 and Remarks 13.2, 13.4, 13.6 are unrefereed computations, NOT covered by the acceptance". L020 does not use Corollary 13.5.
- **L018.** The entry now reads "[proved parts verified-here, K67]". This matches LEDGER K67, which lists Theorem 6(b′) and Theorem 2 among the proved parts.
- **L019.** The entry reads "[PARTIAL; two referee rounds, editorial fixes applied, final check pending]".
  - This was accurate when written.
  - LEDGER K68 now records the proved parts of L019 as [verified-here]. That row cites a review time-stamped 07:31:43, after the commit at 07:31:03.
  - So the status is now stale (cosmetic, item 8). L019 is not load-bearing here.

**F2: Consequence (b) and Step 6.1. Applied in both places.** The facts at vertex 28 are now presented as computed (C1/C2), "as Theorem 3 would predict under $(\mathrm H_{29})$, which is not established". This is correct. I verified it with my own code (`v28.py`): at $v=28$ of $K_{29}$ the pattern is (e).
- The components are $K_{29}[0..19]$ in $(20,15,8)$ and $K_{29}[20..27]$ in $(8,5,3)$.
- $\tau(K-28)=11$.
- Both e-configuration conditions hold, with 0 failed conclusions.

**F3: Remark 4.7 and the cell $(30,15,11)$. Applied, and the arithmetic is right.**
- **The arithmetic.** $s(30,15,11)=90+30-121=-1$. For a vertex $v$ of degree 3, $G=H-v$ has 29 vertices and 12 edges, no isolated vertex, and $r\le3$ components (L017 Theorem 4(i),(ii), refereed). Summing $n_i\le2m_i+1$ over the components gives $29\le24+r\le27$, which is false.
- **The cell list.** L017 Theorem 6(i) lists exactly $(30,15,11)$, $(30,20,12)$ and $(30,26,13)$ for $N=30$. My own enumeration of $11\tau=90+2m-s$ with $s\in\{-1,-2\}$ and $15\le m\le28$ gives the same three cells. The Henning–Yeo bound K8 prunes none of them ($187\le195$, $204\le210$, $221\le228$).
- **The derived cells.** The derived $G$-cells, $(29,17,11)$ with $s(H)=-2$ and $(29,23,12)$ with $s(H)=-1$, are right.

**F4: single-code basis of Theorem 1(ii). Applied** (the "Verification status" paragraph). It is accurate against both reviews:
- fable verified (i) for all 45 classes and (ii) for $K_{29}$;
- opus verified (i)–(iii) for all 45 classes.

**F5 (optional): a remark on "Not used: K8". Not applied.** Its substance is true: the round-1 referees found that K8 prunes no cell of the slack $\le1$ table. Optional.

### opus (NEEDS-WORK, editorial)

**O1: the false sentence "the same classes also arise". Replaced in Theorem 1 and in C8.**
- **The counts.** They are verified (Spot check A).
- **The characterisation.** It was added and is true (re-derived below), but it has no proof in the certificate (Problem 1).
- **The lower-bound caveat.** It was added, but it is incomplete (Problem 3).
- **The attribution.** "Counts verified by both referees" is inaccurate (Problem 4).

**O2: L017 status. Applied** (see F1).

**O3: the b-configuration notion. Applied** in three places:
- a Convention bullet in the Definitions;
- a parenthetical in C3;
- the sentence "In the rest of this paragraph b-configurations are counted with non-edge triples only" in C8.

The quoted numbers equal the opus table and my own recount (Spot check D). The claim that "an edge-forming triple glued to $E_1$ creates an $F_7$" is correct. With hub $v$, the edges $\{v,x_j,y_j\}$ together with $\{x_1,x_2,x_3\}$ and $\{y_1,y_2,y_3\}$ are exactly $\{012,034,056,135,246\}$. The narrower notion therefore loses nothing for the pattern-(b) partners that can occur. A slack-3 component's only possible b-partner is a tight graph with a b-configuration, which is $E_1$ alone.

**O4 (minor): Open problem 2. Not applied.** I also found a second inaccuracy in the same sentence (Problem 5).

**O5 (cosmetic): the parenthetical in Step 3.8. Not applied.** Optional.

### scout (PARTIAL)

**S1: Henning–Yeo as precedent. Applied** in three places: DEPENDS ON, the "Precedent" note after Theorem 1, and Observation 7.
- I checked the quotations against the local text kb/literature/sources/henning_yeo/henning_yeo_1504.02650_4uniform_3regular.txt: Definition 1 (D) at lines 112–129, Lemma 9 (vi)–(viii) at lines 337–343.
- Lemma 9(vii) says a pair is co-transversal iff it is not an (A)-pair, so "their (A)-pair is our NC pair" is a fair analogy.
- The words "is an instance of" overstate the relation (Problem 7).

**S2: Theorem 2 as a corollary of published results. Applied.**
- **The citation.** HY EJC 24(2) P2.50, Proposition 9, was checked in kb/literature/papers/henning_yeo_ejc_2017.pdf (p. 6): "If $H\in\mathcal H_k$ and $G_H$ is the dual graph of $H$, then $\alpha'(G_H)=|E(H)|-\tau(H)$". It matches the certificate's citation.
- **The tag.** "[published, re-proved here]" follows the project's practice for L017 Theorem 7 and L018 Theorem 2 (LEDGER K64, K67).
- **The Chvátal–Hanson formula.** The scout saw it only in secondary sources and said so. The parenthetical "extremal graph $K_4$ with one edge subdivided" is established in this certificate (C6 and the equality analysis); it is not a verified quotation from Chvátal–Hanson (item 8).

### Are the edits purely editorial?

**Yes, apart from the two additions noted in the Summary.**
- Theorem 1's main claim ("at least 45 … (i)–(iii)") is unchanged.
- The sentence that was replaced was false; its replacement is correct.
- The Theorem 1 "Characterisation" is a new claim (Problem 1).
- The Remark 4.7 clause is a new, correct argument in a non-load-bearing remark.
- No proof step in Steps 1–5 changed, and the definitions themselves are unchanged (the Convention bullet only describes counts).

## Re-verified passages (by hand)

**DEPENDS ON.** The statuses were checked against LEDGER rows K64–K68 and the review files on disk; see F1.

The citations of Tutte–Berge, Hall, HY 1504.02650 and HY P2.50 are accurate. In the Tutte–Berge bullet, "Proposition 9 above" refers to a bullet that comes below it (cosmetic).

**Definitions and the b-configuration table.** The definitions are unchanged. All five pairs of numbers in the table equal the opus round-1 table and my recount.

**Theorem 1 statement.**
- **Construction sentence.** It is correct. Each of the 24 e-configured $(20,15,8,3)$ classes carries exactly one e-configuration, and the two $(8,5,3)$ classes carry 2 and 3, so there are $24\times(2+3)=120$ labelled gluings (C1; re-derived by the opus round-1 referee).
- **Counts.** They are correct (Spot check A).
- **Characterisation.** It is correct. My derivation:
  1. Let $K\in{\rm cell}(29,23,12,3)$, and let $v$ be a degree-3 vertex with pattern (e).
  2. Each component contains a pair that lies in no edge, so it has at least 2 edges and at least 5 vertices. Hence both components have at most 23 vertices.
  3. L016 therefore gives I11 for $G$, for every $F_i-x$ and for every $F_i+w(Q_1,Q_2)$.
  4. Hence $\tau(G)=11$, the component slacks sum to 3, free choice holds, and Theorem 3(iv)(e), which uses only these facts, gives an e-configuration on each side.
  5. By the role facts (C5 of L017, re-checked by C3 and by both round-1 referees), no tight graph with at most 23 vertices and no slack-1 graph other than the two $(8,5,3)$ classes has an e-configuration.
  6. So the slacks are $\{1,2\}$, the slack-1 component lies in $(8,5,3)$, and the other component lies in $(20,15,8,3)$.
  7. The refereed lists are complete, and C1 enumerates all their e-configurations, so $K$ is one of the 120 gluings, i.e. one of the 45 classes.
  8. The $\Theta$ version follows in the same way, using:
     - the refereed $(22,17,9,3)$ list;
     - the uniqueness of the $(6,3,2)$ graph (three pairwise-meeting edges on 6 vertices form the triangle);
     - the complete $\Theta$ enumeration of C9, re-run by both round-1 referees.
- **Lower-bound caveat.** It is true as far as it goes, but incomplete (Problem 3).

**Theorem 2 tag and citations.** See S2.

**Consequence (b) and Step 6.1.** See F2.

**Remark 4.7.** See F3.

**Observation 7.** Only the precedent parenthetical was added (Problem 7). The rest is verbatim the earlier text.

**C3 and C8.**
- The edits are consistent with the Convention bullet.
- The C8 sentence "These runs hit 27 … and 4 … (31 of the 45 … by the referees' recomputation)" is correct in its numbers. Its attribution is not (Problem 4).
- An unedited phrase in C3 is ambiguous (Problem 6).

## Spot checks with own code

Everything is in experiments/referee/L020-round2-opus/. Each command was run from there as `timeout <=1200 nice -n 10 python3 <script>`, one process at a time. Outputs are in the `*_output.txt` files.

**A. `k29_profile.py` → `k29_profile_output.txt`.**
- The $K_{29}$ parsed from the certificate text equals class 0 of `K29_classes.json` (True).
- Pattern totals over all 495 degree-3 vertices: (a) 216, (b) 45, (e) 72, (f) 162. These are identical to the opus round-1 profile.
- 0 failed conclusions of Theorem 3, although $(\mathrm H_{29})$ is not known.
- Per class:

  | vertex type | classes with at least one | distribution per class |
  |---|---|---|
  | (e), $(8,5,3)+(20,15,8)$ | 45 | 18 classes with 1, 27 with 2 |
  | $\Theta$, (f) with $F_1=(6,3,2)$, $F_2=(22,17,9)$ | 45 | exactly 3 in every class |
  | (f), $F_1=(18,13,7)$, $F_2=(10,7,4)$ | 27 | exactly 1 each |
  | (b), $E_1+(25,19,10)$ | 31 | 19 with 1, 10 with 2, 2 with 3 |
  | (a), $K-v\in(28,20,11)$ | 45 | 2 to 7 per class |

- No other type occurs. So "all 45 … three $\Theta$-vertices; 27 of the 45 …; 31 of the 45 …" is exactly right.

**B. `t3_spot.py` → `t3_spot_output.txt`.**
- I re-classified all 4,111 degree-3 vertices of the 482 stored near-tight graphs ($n\le26$, so $(\mathrm H_n)$ holds by L016): (a) 3,223, (b) 145, (e) 183, (f) 506, (i1) 39, (i2) 15. This equals C4.
- A stratified random sample (seed 20261027) of 30 instances was checked in full: (a) 10, (b) 4, (e) 4, (f) 4, (i1) 4, (i2-4) 4. The (i2) instances on disk are all of type (i2-4). The sample covers the lists $(12,10,5)$, $(15,11,6)$, $(19,16,8)$, $(22,17,9)$ and $(26,22,11)$.
- Every conclusion was checked directly with my own $\tau$:
  - (i): distinctness, $d_G=d_K-1$, no pair inside an edge of $G$, $\tau(G)=\tau(K)-1$, $s(G)=s(K)+2$;
  - (ii): $|Y|\le1$; if $Y\neq\emptyset$ then $s(K)=1$ and all components are tight, with $Y$ a degree-1 co-vertex; otherwise the slacks sum to $s(K)+2$; each component slack lies in $[0,3]$ and each component contains a co-vertex;
  - (iii): free choice at every vertex of every component;
  - (iv)/(v): $r\le2$, or $r\le3$ with $Y$; the stated condition of the pattern, with NC pairs computed as $\tau(F-x-y)\ne\tau(F)-2$; for (f), also $F_1+w(P_1,\{c,e\})\notin C$; for (i1), the condition tested as $\tau((F_1-f)+w(P_1,P_2))=\tau(F_1-f)+1$.
- Result: 0 failures.

**C. `prop6_check.py` → `prop6_check_output.txt`, and `prop6_near.py`.**
- All 483 graphs of the ten slack $\le1$ lists: 204 NC pairs. The types $(d_{\min},d_{\max},\sigma)$ are $(1,1,0)$: 1, $(1,1,1)$: 3, $(1,2,0)$: 1, $(1,2,1)$: 104, $(2,2,1)$: 95. This equals C7.
- For every NC pair:
  - $|\partial|=d_x+d_y-\sigma$;
  - $\tau(K-x-y)=\tau-1$;
  - $s(K-x-y)$, computed from the actual $(n-2,m-|\partial|,\tau-1)$, equals $s+5-2|\partial|\ge0$.
- For every $(2,2)$ pair: $\sigma=1$, $s(K)=1$, $s(K-x-y)=0$, no isolated vertex, every component tight and meeting the attachment vertices, and at most 5 components. In fact there are 1 component in 60 cases and 2 in 35. Proposition 6 holds with 0 failures.
- I also checked the proof sentence of 5.2 ("1+2+2=5 vertices other than $x,y$"). It fails in 21 of the 95 $(2,2,1)$ cases, which have 4 attachment vertices. Example: $(8,5,3)$ class 1, NC pair $\{3,4\}$, edges $\{2,3,4\},\{3,5,7\},\{4,6,7\}$; the two unshared edges meet in 7. The bound of Proposition 6 is unaffected (Problem 2).

**D. `bcfg_recount.py` → `bcfg_recount_output.txt`.** Classes with a b-configuration, edges allowed / non-edge only:

| cell | edges allowed | non-edge only |
|---|---|---|
| $(9,4,3)$ | 1/1 | 0 |
| $(10,8,4)$ | 1/63 | 0 |
| $(13,9,5)$ | 32/84 | 3 |
| $(16,10,6)$ | 16/16 | 0 |
| $(20,15,8)$ | 159/953 | 0 |
| $(6,3,2)$ | 1/1 | 1 |

These equal the Definitions table. Classes with an e-configuration: $(10,8,4)$ 25, $(13,9,5)$ 5, $(20,15,8)$ 24, $(6,3,2)$ 1, $(9,4,3)$ 0, $(16,10,6)$ 0. These equal C3.

**E. `sanity.py` → `sanity_output.txt`.** Controls for my membership test:
- $K_{29}\in C$ with $\tau=12$;
- $F_7$ is detected and $F_7\notin C$;
- Pasch satisfies (P3);
- a 7-edge graph on 7 vertices fails (P3).

My $\tau$ reproduced the stored $\tau$ of all 482 + 1,118 stored graphs it was run on (assertions in B, C and D).

## Remaining problems, in order of severity

None is a mathematical error in a proved statement.

### 1. The Theorem 1 "Characterisation" has no proof in the certificate

**The problem.**
- The statement now asserts that, given the refereed lists, the 45 classes are exactly the classes of cell$(29,23,12,3)$ with a pattern-(e) vertex, equivalently with a $\Theta$-vertex.
- Step 1 proves only existence and the properties (i)–(iii). The parenthetical "both referees re-ran the gluings" supports only the enumeration, not the argument that every pattern-(e) or $\Theta$ class must arise from it.
- The claim is true (derivation above), and it depends on L016, the completeness of the lists $(8,5,3,3)$, $(20,15,8,3)$ and $(22,17,9,3)$, and the role facts of C5/C3.

**Fix.** Add a short Step 1.4 with the derivation given above (eight lines), or move the sentence to a remark that cites the opus round-1 review, item (a)5.

### 2. Step 5.2 contains a false count (unedited text)

**The problem.** "There are three such edges …, with $1+2+2=5$ vertices other than $x,y$". The two unshared edges may meet: by linearity they share at most one vertex, but they can share one. In 21 of the 95 stored $(2,2,1)$ instances there are only 4 such vertices.

**Fix.** "with at most $1+2+2=5$ vertices other than $x,y$; so at most 5 components". The statement of Proposition 6 is unaffected.

### 3. The lower-bound caveat is incomplete (Theorem 1 and C8)

**What the text says.** It names only:
- classes all of whose degree-3 vertices are of pattern (a);
- the unsampled part of "the pattern-(b) gluings $(25,19,10,3)+E_1$".

**What it omits.** By the same arguments as the characterisation (the role facts and the complete lists with at most 26 vertices), a class outside the 45 can have only degree-3 vertices of these types:
- (a), with $K-v\in(28,20,11,3)$;
- (b) **or (f)**, with $K-v=(25,19,10,3)\sqcup E_1$. `build_bf.py` glued both b- and f-configurations to $E_1$ on the same 3,000-class sample;
- (i1), with $K-v=\{y\}\sqcup(27,20,11,3)$, i.e. with a degree-1 vertex. L017 Remark 13.6 reports this cell empty only by an unrefereed worker computation.

All other types are already enumerated completely or excluded:
- (e), $\Theta$ and (f) with $(18,13,7)+(10,7,4)$ are fully enumerated;
- the other (b)/(f) splits are excluded because no slack $\le1$ graph and no slack-2 list other than $(6,3,2)$ has the required configuration, and the only tight graphs with NC pairs are $E_1$ and two $(10,7,4)$ classes;
- (i2) and (i3) are excluded because they need an e-configuration or an NC pair in a tight component, and the only tight components that fit (10 + 17, or 3 + 10 + 14 vertices) cannot supply one.

**Fix.** Either write "for example", or list the four types.

### 4. Misattribution of the new counts

**The problem.** Theorem 1 says "counts verified by both referees of round 1, who re-ran the gluings", and C8 says "by the referees' recomputation". The per-class counts (27, 31, three $\Theta$-vertices, 1 or 2 (e)-vertices) were computed in round 1 by the opus referee only. The fable report contains no per-class profile; fable re-ran the $\Theta$ gluings and canonicalised the prover's 120 e-gluings. The counts are now re-verified independently in round 2 (Spot check A).

**Fix.** Attribute the counts to "the opus referee of round 1, re-verified in round 2".

### 5. Open problem 2 is inaccurate (opus O4 not applied)

**The problem.** "The subcases with a vertex of degree 1 give slack-1 or slack-2 remainders." By Proposition 6, $s(K-x-y)=s(K)+5-2|\partial|$:

| type | $\lvert\partial\rvert$ | remainder slack |
|---|---|---|
| $(1,1,0)$, $(1,2,1)$ | 2 | $s(K)+1\in\{1,2\}$ |
| $(1,1,1)$ | 1 | $s(K)+3\in\{3,4\}$ |
| $(1,2,0)$ | 3 | $s(K)-1$, which forces $s(K)=1$ and a tight remainder |

Both exceptional types occur on disk, 3 times and once.

**Fix.** Rephrase the sentence (it is heuristic text, so a rewording suffices).

### 6. An ambiguous phrase in C3 (unedited)

**The problem.** "e-configurations in (6,3,2), …, none of 16 (16,10,6), 1 (9,4,3), 178 (23,16,9)" reads as if $(9,4,3)$ had 1 and $(23,16,9)$ had 178 e-configured classes. In fact there are none:
- the prover's `roles_output.txt` (lines 9, 12, 16) gives role_e = 0 for $(9,4,3)$ [1 class], $(16,10,6)$ [16] and $(23,16,9)$ [178];
- my recount gives 0 for $(9,4,3)$ and $(16,10,6)$, and by hand $(9,4,3)$ is the spider, whose NC pairs lie inside its three pendant edges.

**Fix.** "none in $(16,10,6)$ [16 classes], $(9,4,3)$ [1] or $(23,16,9)$ [178]".

### 7. The precedent wording overstates

**The problem.** "Gluing … is an instance of the Henning–Yeo operation (D)" and "this is the vertex-gluing … operation (D)". HY's (D) is an operation on non-uniform hypergraphs:
- it deletes a 2-edge $\{u_i,v_i\}$ from each piece;
- it adds $\{u_1,v_1,x\}$ and $\{u_2,v_2,x\}$;
- it adds the 4-edge $\{u_1,v_1,u_2,v_2\}$.

$\Theta$ and the pattern-(e) gluing instead add a vertex with three 3-edges, one or two of which cross between the pieces. They are analogous to (D), not instances of it.

**Fix.** Write "analogous to" or "of the same type as". The credit itself is appropriate.

### 8. Cosmetic and optional items

- STATUS says "revised 2026-10-27 07:35 UTC", but the commit containing it is time-stamped 07:31:03.
- In the Tutte–Berge bullet, "Proposition 9 above" should be "below".
- The L019 status could now read "[proved parts verified-here, K68]".
- The Theorem 2 tag attributes "extremal graph $K_4$ with one edge subdivided" to Chvátal–Hanson. That fact is established here (C6 and the equality analysis); it is not a checked quotation.
- The optional round-1 items F5 (a K8 remark) and O5 (the Step 3.8 wording) were not applied.

Once items 1–6 are fixed (editing only), I would recommend ACCEPT.

## Independence statement

I read the three round-1 reports, as the task required. I did not read or run any round-1 referee code.

All verification code was written for this review and is in experiments/referee/L020-round2-opus/:

| script | purpose |
|---|---|
| `hgr2.py` | shared 3-graph routines |
| `patt.py` | Theorem 3 pattern classifier |
| `k29_profile.py` | Spot check A |
| `t3_spot.py` | Spot check B |
| `prop6_check.py`, `prop6_near.py` | Spot check C |
| `bcfg_recount.py` | Spot check D |
| `sanity.py` | Spot check E |
| `v28.py` | vertex 28 of $K_{29}$ (F2) |

This code imports nothing from e757/, judge/, experiments/prover/ or other referees' folders.

**Methods.**
- $\tau$ by memoised exact branching on edge masks, validated on 1,600 stored graphs;
- co-transversality via $\tau(F-X)=\tau(F)-|X|$;
- membership in $C$ by pairwise linearity, an anchored $F_7$ search and a Hall/Kuhn test for (P3), using the equivalence of Step 1.1, which I re-proved by hand;
- pattern classification from the component structure of $K-v$.

**Data read as data only.**
- experiments/prover/L020/K29_classes.json;
- the stored lists in experiments/20261027-0300-transversal-richness/inputs/;
- the prover's `roles_output.txt` (only to resolve the C3 wording);
- the local Henning–Yeo texts;
- results/LEDGER.md, and L017 Theorem 6(i).

**Files touched.** I modified nothing outside my scratch folder and this review.
