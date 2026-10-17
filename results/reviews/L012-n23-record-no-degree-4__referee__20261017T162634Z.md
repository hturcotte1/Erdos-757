VERDICT: ACCEPT

# Referee report: L012-n23-record-no-degree-4 (round 1)

- **Claim reviewed:** `results/proofs/L012-n23-record-no-degree-4.md`, as committed in 30aca94 (2026-10-17 15:52:32 UTC; SHA-256 c7fa088e…; the only change since the submission commit cfd5c35 is the L011 status line). The file did not change during this review.
- **Programs reviewed:** `experiments/prover/L012/` (engine.py, route.py, decomp22.py, indep/ext_d.c, indep/filt.c, indep/canon.c, indep/realize.c, outputs) and the falsifier folder `experiments/20261017-1030-n23-record-cell/`. I read these programs but ran almost none of them. All the evidence below comes from my own programs.
- **Referee workspace:** `experiments/referee/L012-round1/`. Sources are in `src/`, and every command is in `reproduce.sh`. Binaries, large files and logs are in `out/` and `logs/`, which are git-ignored.
- **Resources:** about 1 h wall time, nice 5, never more than 2 processes.

## Summary

The certificate makes four claims. (i) A 23-point (4,5)-set with $h=13$ has a saturated AP pattern $(23,21,10)$ with every degree at most 3 (Theorem 1). (ii) The cells $(23,19,10)$ and $(23,20,10)$ are empty in $C$ (Theorem 2). (iii) Exactly 699 classes of $C$ have $(23,21,10)$, $\Delta\le4$ and a degree-4 vertex. (iv) None of these 699 is realized by a set with an injective midpoint map (Theorem 3).

I checked every step of the argument by hand: the degree bound from I11 at $n=22$, the slack decompositions, Lemma E, the extension criterion, the normal form of a realization and Lemma N. I then re-did every load-bearing computation with programs I wrote myself, using different methods:

- **Exact realizability.** A new realizability test with a different formulation: all $n$ unknowns, incremental elimination along the DFS, a different prime, and correctness justified a priori by a Hadamard bound.
  - On the 699 classes it gives the prover's numbers class by class: 27,206,877 assignments, 0 singular, 6,051,773 distinct-valued, 0 realizations.
  - It passes two-sided controls. At $n=12$ it recovers exactly the 54,243 census classes, no more and no fewer. At $n=14$ it finds all 2,910 census sets. On $A_{\rm base}$ it finds 948 realizations, all re-verified with Fractions, $A_{\rm base}$ among them.
- **Route 4 and route 20.** A new extension enumerator, a new filter (centre-based $F_7$ test, BFS Hall test for (P3), exact $\tau$ by branching) and networkx VF2 instead of nauty.
  - Route 4: 552,560 extensions → 450,606 contain $F_7$ → 87,664 more violate (P3) → 14,290 survivors. These fall into exactly the 699 classes, all of them, pairwise non-isomorphic.
  - Route 20: 128 extensions, 0 in $C$.
- **The engine's class lists.**
  - I re-derived the top recursion level of every recursive cell with my own tools, including $(22,17,9,4)$ with 95 classes and $(19,16,8,4)$ with 956. Every per-branch count of the prover's log is reproduced, and the class sets agree under VF2.
  - I enumerated directly, with unmodified genbg plus my own pruning hooks, all 94 directly-enumerated cells and 10 of the recursive cells, up to $(15,12,6,3)$ with 10,617 classes. All agree under VF2 bijection.
  - A closure test (every deletion of a maximum-degree vertex lands in the lists) found nothing missing.

I found no mathematical or computational error. The only remarks are editorial (see Problems).

## Dependencies

- **L011** (I11 on $C$ for $n\le22$). Three referee reports, all `VERDICT: ACCEPT`: rounds 1, 2 and 3 (`results/reviews/L011-f22-equals-13__referee__20261017T133431Z.md`, `…T154609Z.md`, `…T150941Z.md`). The certificate's condition "conditional on the acceptance of L011" is therefore met.
  - I checked that L011 Theorem 1 covers all of $C$ with $n\le22$, not only connected members. This matters because $H-v$ and the components in Lemma E may be disconnected or contain isolated vertices.
- **L007–L010** were accepted earlier. The base of the engine is `enum_conn`, covered by L007 Lemma D. Its source is byte-identical in L007 through L012 (md5 db76da72… in all six folders). I also re-enumerated all 94 direct cells independently (check 6b), so the base no longer rests on Lemma D alone.
- **K3–K8 [published].**
  - Henning–Yeo is used for 3-uniform, linear, $F_7$-free hypergraphs, which is what members of $C$ are. Its hypotheses hold.
  - HY is used only in Step 1 ($m\ge19$) and as a filter. My brute force gives the same decomposition lists without HY.

## Step-by-step audit

| Step | Content | Status |
|---|---|---|
| 0.1 | Additivity, heredity, $\tau(H)-1\le\tau(H-v)\le\tau(H)$, $m\le n-2$, $n\le2m+1$ for connected graphs | correct |
| 0.2 | I11 for every $H\in C$ with $n\le22$ (L011 Thm 1, any connectivity) | correct |
| 0.3 | $11\tau(H-v)\le66+2(m-d)\le108<110$, so $\tau(H-v)=9$ and $d\le m-17$; slack of $H-v$ is $2m-33-2d$. This also excludes isolated vertices | correct (re-derived) |
| 0.4–0.5 | Transfer of extensions under isomorphism; edges at a maximum-degree vertex: disjoint pairs, not inside an edge, endpoint degree $\le\Delta-1$ | correct |
| 0.6 | $m=n-2$ forces connected with no isolated vertex | correct |
| 1 | $m\in\{19,20,21\}$ (P3 and HY); $\Delta\le2,3,4$; slacks $-3,-1,+1$ | correct (`arith_decomp.py`) |
| 2 | $(23,19,10)$: $57>46$ | correct |
| 3.1–3.4 | Lemma E and the engine. Branches $d\in[\lceil3m/n\rceil,D]$, $t'\in\{t-1,t\}$, $S'\ge0$; components in $\mathcal C(\cdot,\cdot,\cdot,d)$; multisets via `combinations_with_replacement`; output filters | correct (code audited; every branch present; see checks 6a–6e) |
| 3.5 | The extension criterion "$\tau(H)\ge t$ iff every $(t-1)$-cover of $G$ misses some pair" when $\tau(G)=t-1$; kill search with exclusion produces each $d$-set exactly once; $F_7$ pruning is sound | correct (proved; independent implementation with a different branching order agrees, check 4) |
| 4.1–4.3 | Route 20: decompositions [(22,17,9)], [AP,(19,16,8)], [(10,7,4),(12,10,5)], [(8,5,3),(14,12,6)]; 864 inputs; none in $C$ | correct (checks 2 and 5) |
| 5.1–5.3 | Route 4: 2,178 inputs; 14,290 extensions in $C$; 699 classes | correct (check 4) |
| 6.1 | A (4,5)-set has an injective midpoint map; normal form $x_u=0$, $x_v=1$ with $\{u,v\}$ the extremes | correct |
| 6.2 | Lemma N: a non-zero solution $y$ of the homogeneous system gives a maximum level set $S\not\ni u,v$ with $\mu^{-1}(S)\subseteq E(S)$, so $e(S)\ge\lvert S\rvert$, contradicting (P3) | correct (uses $m=n-2$ for $\mu$ to be a bijection onto $V\setminus\{u,v\}$, and (P3) for $\lvert S\rvert\ge3$) |
| 6.3 | Enumerate all injective $\mu$; exact solve; distinct values and exactly $m$ APs | correct (check 3) |
| 7 | Assembly; $n_2+2n_3=40$ gives $n_3\ge17$ | correct |
| 8, C7, Remarks 4–5 | Descriptive or open | decomposition counts 5, 6, 20 and the 14 record cells of Remark 5 re-derived; the falsifier's size figures in 8.2 are flagged by the prover as not re-derived and are not load-bearing |

## Checks performed (commands and outputs)

All commands are run from `experiments/referee/L012-round1/`.

### 1. Arithmetic and decompositions
`python3 src/arith_decomp.py`.

- **Step 1.** P3 with HY at $(23,\tau=10)$ allows $m\in\{19,20,21\}$. Maximum degrees are 2, 3, 4 and $H$-slacks are $-3,-1,1$. No degree permits $\tau(H-v)=10$. For $\Delta\le3$ the degree count gives min $n_3=17$.
- **Decompositions.** My own brute force over multisets of connected types plus isolated vertices, with and without HY:
  - $(22,17)$, slack 1: 4 decompositions, identical to the proof's;
  - $(22,18)$, slack 3: 5;
  - $(22,19)$, slack 5: 2;
  - the no-HY versions are identical.
- **Engine branches.** All 36 branches recorded in the prover's cell files have decomposition lists equal to my brute force. Every $(d,t')$ with $S'\ge0$ is present: `engine branches compared: 36, mismatches: 0`.
- `python3 src/misc_checks.py`:
  - Remark 5's 14 record cells are reproduced with the stated slacks.
  - Degree statistics of the 699: 2, 3 or 4 vertices of degree 4 in 227, 402, 70 classes; 1 or 2 vertices of degree 1 in 630, 69 classes; six degree patterns.
- The Step 8 decomposition counts $(20,15)$ slack 2, $(18,14)$ slack 5 and $(21,15)$ slack 5 are 5, 6, 20, as stated.

### 2. Validity of every component representative used by the routes
`python3 src/build_inputs.py 4` and `python3 src/build_inputs.py 20`. These use my own Python checks: connected, linear, centre-based $F_7$ test, (P3) by matching, exact $\tau$, $\Delta$.

- D4: 0 failures among 95, 1, 956, 5, 221, 2, 11 representatives. D3: 0 failures among 37, 1, 227, 4, 149, 2, 2.
- Inputs: 2,178 for route 4, identical as a set to the prover's `out/route4_inputs.txt`; 864 for route 20.

### 3. Exact realization, re-implemented independently (`src/rreal.c`)

**Method.**
- All $n$ values are unknowns. The rows $2x_{\mu(e)}-x_a-x_c$ are added incrementally along the DFS and reduced modulo $p=2^{31}-1$ against the previous pivot rows.
- At a leaf, a null vector $z$ with $z_{f_1}=0$, $z_{f_2}=1$ is computed, where $f_1,f_2$ are the two free columns. Then $z=\alpha+\beta x^*$ with $\beta\ne0$.
- **Rigour.** With $y=Dx^*$ we have $y_i=\det M_i$ (Cramer), and Hadamard gives $\lvert y_i\rvert,\lvert D\rvert\le6^{(n-2)/2}\approx1.48\cdot10^8$, since every row has norm $\le\sqrt6$. Because $4H<p$, the following hold exactly:
  - "$z_i\equiv z_j$" is equivalent to $y_i=y_j$;
  - "$z_i+z_k\equiv2z_j$" is equivalent to an exact AP;
  - Lemma N together with $\lvert D\rvert<p$ means the rank cannot drop mod $p$.
- Each leaf re-checks every edge equation mod $p$.
- This shares nothing with `realize.c` except the definition of the test. `realize.c` uses Gauss–Jordan mod $2^{61}-1$ per leaf with an a posteriori integer check.

**Results.**
- `./out/bin/rreal 23 < out/r4_699.txt` (117 s): `TOTAL graphs=699 assignments=27206877 singular=0 distinct=6051773 realizations=0 realizable_graphs=0`.
  - Per class, (assignments, distinct, realizations) equals the prover's `out/realize_r4_part0{0,1}.txt` on all 699 lines: `mismatched lines: 0`.
  - Per class: 22,785 to 49,606 assignments, at least 1,656 distinct-valued.
- **Positive control, A_base** (`src/abase_control.py`): `assignments=1596 distinct=1413 realizations=948`. All 948 were re-solved exactly with Fractions; each has distinct values and AP set = edge set, and the mod-$p$ values agree. 948 distinct normalised sets, exactly one equal to $A_{\rm base}$ or its reflection.
- **Two-sided control against the $n=12$ census** (L002; `src/census12_control.py`, 7 min).
  - (A) All 54,243 census sets: each is found by `rreal` among the realizations of its own pattern.
  - (B) `rreal` on the 221 classes of `cell(12,10,5,4)`:
    - 219 classes have a realization and 195 have a (4,5)-realization;
    - 83,021 realizations, all exactly reconstructed (rational reconstruction, $2H^2<p$) and re-verified with Fractions;
    - 58,999 of them are (4,5)-sets;
    - the set of their affine classes (up to reflection) equals the census exactly: `54243; equal to census set: True; census minus realized: 0; realized minus census: 0`.
  - **Negative controls.** The 2 classes with no realization at all, and the 24 with only non-(4,5) realizations, are confirmed by the census to carry no 12-point (4,5)-set with $h=7$. The prover's `realize` agrees with mine class by class on all 221 (`mismatches: 0`).
- **$n=14$ census** (L004; `src/census14_control.py`): `census sets 2910, own set found 2910, total realizations 2671044, singular 0`. 2,671,044 is the prover's number.
- **Descriptive** (`src/rreal_extra.c`): the minimum number of extra APs over the distinct-valued solutions is 4 for 675 classes and 6 for 24, as stated in C5.

### 4. Route 4 re-run with my own extension program, filter and isomorphism test

**`src/rext.c`.**
- $\tau(G)$ by branching. All $t$-covers by brute force over all $2^{22}$ masks.
- Kill search with exclusion, but the branching cover is the first alive cover in a static order by increasing number of killing pairs, a different search tree from `ext_d`.
- No $F_7$ pruning. Every output is re-checked a posteriori (disjoint pairs, every cover killed).

**Validation of `rext`.**
- `src/bf_rext.py`: 72 cases against my Python brute force (all $d$-sets of disjoint admissible pairs, exact $\tau$), $d=2,3,4$, with isolated vertices. 6,930 hits, 0 mismatches.
- On the prover's 12 constrained-mode validation files, the counts equal their `bf_ext.py` counts: 152, 0, 2272, 67524, 1170, 10497, 35762, 1430, 2100, 7500, 11280, 200640.

**Results.**
- `rext 22 4 3` on the 2,178 inputs: every input has $\tau=9$; 246,797 + 305,763 = **552,560** extensions with $\tau\ge10$, the prover's unpruned number.
- `src/rfilt.c`: centre-based $F_7$ test, (P3) via BFS augmenting paths for every pair, exact $\tau$, union-find connectivity.
  - contain $F_7$: 229,702 + 220,904 = **450,606**;
  - $F_7$-free but (P3) violated: 6,913 + 80,751 = **87,664**;
  - survivors **14,290**, all connected, `tau_range=[10,10]`, `maxdeg_range=[4,4]`.
- `src/iso_match.py` (networkx VF2 on the incidence graph, inside Weisfeiler–Lehman buckets; no nauty):
  - (1) the 699 prover representatives are pairwise non-isomorphic (634 buckets, 68 pairs tested, 0 isomorphic);
  - (2) `connected survivors 14290, matched to a representative 14290, UNMATCHED 0, representatives hit 699 of 699`.
- So Theorem 3(a) holds exactly, given the input cells, without using nauty. The realization in check 3 covers every graph my pipeline produced.

### 5. Route 20 re-run
`rext 22 3 2` on 864 inputs gives 128 extensions with $\tau\ge10$. `rfilt`: 44 contain $F_7$, 84 are $F_7$-free and all violate (P3), 0 survivors. The prover reports 84 $F_7$-free and none in $C$. Theorem 2 holds, given the cells.

### 6. The engine's class lists (the remaining dependency)

**(a) Code audit.** `engine.py`, `route.py` and `decomp22.slack_cells` implement Lemma E as stated:
- correct $d$ range, $t'\in\{t-1,t\}$, $S'\ge0$;
- isolated vertices included when $S'\ge3$;
- multisets of representatives for repeated types;
- component cells taken with maximum degree $d$, endpoint bound $d-1$;
- `bad_tau` aborts the run;
- `tau == t` re-checked when $t'=t$ (for $t'=t-1$, $\tau=t$ is forced).

The trivial empty-cell rules (`t>m`, `n>2m+1`, `m>n-2`, HY) are valid for connected members of $C$.

**(b) Direct enumeration.** I built unmodified genbg from the nauty 2.8.8 sources. `src/myhooks.c` adds my own isomorphism-invariant, monotone prunes:
- $\tau(\text{partial})+(\text{remaining edges})<t$;
- $F_7$ containment;
- (P3) violation.

The output re-checks $\tau=t$, $F_7$ and (P3). Command: `genbg -c -Z1 -d1:3 -D<D>:3`. Results:

- **All 94 cells the engine enumerated directly with `enum_conn`:** 82 equal counts, and 12 trivially empty ($3m>Dn$; genbg refuses the parameters; prover count 0). For example (14,9,5,3) 1060, (11,8,4,3) 471, (17,10,6,3) 339, (12,10,5,4) 221, (16,9,5,2) 166, (12,10,5,3) 149, (19,10,6,2) 128.
- **Recursive cells:**

| Cell | Classes (genbg = prover) | Time |
|---|---|---|
| (14,12,6,3) | 2 | 45 s |
| (14,12,6,4) | 11 | 228 s |
| (15,11,6,3) | 19 | |
| (15,11,6,4) | 30 | |
| (17,11,6,2) | 114 | |
| (19,12,7,2) | 1 | |
| (20,12,7,2) | 38 | |
| (20,11,7,2) | 1 | |
| (20,11,7,3) | 45 | |
| (15,12,6,3) | 10,617 | |

  (17,13,7,3) timed out at 500 s; it is covered by (c).
- Plain unpruned genbg + `gfilt` gives the same results for (8,5,3,3/4), (10,7,4,3/4), (12,10,5,3/4), (13,9,5,3), (10,8,4,3).
- `src/cmp_lists.py`: VF2 bijection between my lists and the prover's on all 69 non-empty lists, 3,365 classes. No unmatched class and no class hit twice.

**(c) Independent recomputation of the top recursion level of every recursive cell** (`src/recompute_cell.py`). This covers all 23 of the 25 recursive cells that have branches. The other two, (15,11,6,2) and (16,11,6,2), are empty by the degree count: $3m=33>2n$. My decompositions, the prover's next-lower lists as components, my `rext`, my `rfilt`, VF2 classes. Every per-branch number in the prover's cell logs is reproduced, and the class sets agree.

| Cell | Branch counts (mine = prover's log) | Connected survivors → classes |
|---|---|---|
| (22,17,9,4) | $d=3$: 163,773 extensions, 29,919 $F_7$-free, 27,322 in $C$; $d=4$: 464,451, 130,912, 115,270 | 3,778 → **95** |
| (19,16,8,4) | $d=3$: 6,085 / 4,649; $d=4$: 26,452 / 14,038 | 18,687 → **956** |
| (22,17,9,3) | | 1,114 → 37 |
| (19,16,8,3) | | 4,649 → 227 |
| (21,14,8,3) | 336,840 in $C$ | 13,264 → 299 |
| (18,13,7,3) | 237,511 in $C$ | 62,050 → 2,544 |
| (15,12,6,3) | 141,229 in $C$ | 141,212 → 10,617 |
| (17,13,7,3) | | 113 → 6 |
| (20,12,7,2) | | 1,242 → 38 |
| (17,11,6,2) | | 2,644 → 114 |
| (20,11,7,3) | | 5,317 → 45 |
| (14,12,6,4) | | 167 → 11 |
| (15,11,6,4) | | 1,052 → 30 |
| (14,12,6,3) | | 17 → 2 |
| (15,11,6,3) | | 440 → 19 |
| (19,12,7,2) | | 11 → 1 |
| (20,11,7,2) | | 55 → 1 |
| (21,13,8,4) | 3,512 and 10,800 in $C$ | 0 → 0 |
| (18,12,7,4) | | 0 → 0 |
| (20,14,8,3) | | 0 → 0 |
| (19,11,7,3) | | 0 → 0 |
| (18,12,7,2) | | 0 → 0 |
| (19,11,7,2) | | 0 → 0 |

Every recursive list therefore equals what my tools produce from the next-lower lists, and the lowest lists are confirmed by (b). By induction on the recursion, every list used by routes 4 and 20 is reproduced without nauty canonical forms. The only nauty used is genbg's generation of the base cells, and those agree with `enum_conn`.

**(d) Closure test** (`src/closure_check.py`). For every class $X$ of a recursive list and every vertex $w$ of maximum degree, and for every degree-4 vertex of each of the 699, every component of $X-w$ must be VF2-isomorphic to a member of the corresponding list. The engine used only one $w$ per class. Over 18 lists (the 699 route-4 classes and the 17 non-empty recursive cells), 97,813 deletions and 116,761 components with at least 3 vertices, I found 0 components without a match and 0 missing cells. For example: route-4 classes 1,940 deletions / 3,880 components; (15,12,6,3) 71,725 / 77,261; (18,13,7,3) 13,916 / 20,671.

**(e) D3 = D4 restricted to $\Delta\le3$** (`src/d3_subset.py`). For (8,5,3), (10,7,4), (12,10,5), (14,12,6), (15,11,6), (19,16,8) and (22,17,9), the $\Delta\le3$ members of the D4 list are exactly the D3 list (2, 4, 149, 2, 19, 227, 37).

### 7. Canonical forms (nauty)

`canon.c` prints the hypergraph relabelled by nauty's canonical labelling. The colour cells are kept, so positions $\ge n$ are edges. Consequences:
- Equal outputs imply isomorphic inputs, by construction.
- Every graph is replaced by an isomorphic copy, so de-duplication can never lose a class, even if nauty were wrong.
- nauty's canonicity (isomorphic implies equal output) matters only for the exact class counts.

The counts 699, 95, 956, 227, 37, 2,544, 10,617 and the others were confirmed by VF2 in checks 4 and 6.

## Problems found (in order of severity)

No error that affects any theorem was found. The items below are editorial or clarifications. They are not gaps and need no further review.

1. **Dependency wording (editorial).** The DEPENDS ON line now records L011 as ACCEPTED in rounds 1–3 (true: three ACCEPT reports exist). The same line and the Tags line still say the certificate is "conditional on the acceptance of L011". That condition is now met, so the conditional can be dropped when the result is recorded. The STATUS line ("no referee round yet") is out of date after this report.
2. **The role of nauty is overstated (clarification).** Step 3.4 and the header call nauty canonical forms load-bearing for completeness. They are not, for the reason given in check 7: false merges are impossible, and false splits would only create duplicates. nauty matters only for the exact counts in Theorem 3(a) and in the cell table. Those are now confirmed independently by VF2.
3. **Lift in Step 6.3 (remark).** The a posteriori integer check already makes the computation rigorous. One could add that the Hadamard bound $\lvert y_i\rvert,\lvert D\rvert\le6^{(n-2)/2}<1.5\cdot10^8\ll p/2$ shows a priori that the symmetric lift is the true value. This is what my independent test relies on.
4. **Scope (no action needed).** Step 8.2 quotes size figures from the falsifier that are not re-derived. The prover labels them as such, and nothing depends on them. The maximum-degree-3 case (Remark 4) stays open, as the claim says.
