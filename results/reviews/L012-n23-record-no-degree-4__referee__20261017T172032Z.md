VERDICT: ACCEPT

# Referee report: L012-n23-record-no-degree-4 (round 2)

- **Claim reviewed:** `results/proofs/L012-n23-record-no-degree-4.md` at commit b28e546 (SHA-256 844bd776…089518344).
  - During the review it was updated in d6d4fa8 (17:20 UTC; SHA-256 4f3bfe2e…3e04b4bae).
  - `git diff b28e546` shows only two changed lines, the STATUS line (line 4) and the Tags line (line 28). The mathematics and every number are identical.
  - This verdict applies to both versions.
- **Programs read:** `experiments/prover/L012/` (engine.py, route.py, decomp22.py, indep/canon.c, indep/realize.c, reproduce.sh, outputs) and the falsifier's README.
  - I ran none of the prover's programs, except its `bin/canon`, which was under test (check 7).
  - All evidence below comes from programs I wrote. They differ from both the prover's and round 1's in method.
- **Workspace:** `experiments/referee/L012-round2/`. Sources are in `src/` and every command is in `reproduce.sh`. `out/` and `logs/` are git-ignored.
  - An unrelated commit, bfced1a (16:43 UTC, another agent's `git add -A`), captured early copies of `src/rz.c`, `src/abase_ctrl.py` and a pre-fix `src/census_ctrl.py`. The current files are the ones described here.
- **Resources:** about 45 min wall time, nice 5, at most 2 processes.

## Summary

I numbered and checked by hand every step:
- the degree bound 0.3 from I11 at $n=22$;
- the arithmetic of Step 1;
- the slack decompositions and Lemma E;
- the kill criterion of 3.5;
- the normal form 6.1 and Lemma N (6.2);
- the deduction of Theorem 1 in Step 7.

All are correct. I then re-did every load-bearing computation with my own programs:
- **Exact realization test** (`rz`): it enumerates the unmatched pair first and then a perfect matching driven by vertices. It solves the system, ordered by midpoint as an M-matrix, in floating point; the integer solution is then verified exactly. A second, all-integer fraction-free Bareiss mode agrees class by class.
  - On the 699 classes it gives 27,206,877 assignments, 6,051,773 distinct-valued and **0 realizations**, equal to the prover's numbers class by class.
  - Every one of the 27,206,877 systems has $\det>0$, a numerical confirmation of Lemma N.
  - A pure-Python Fractions solver with the other, edge-driven, enumeration reproduces the full multiset of exact solution vectors on three classes.
  - Positive and negative controls: A_base; the $n=14$ census, one-sided and two-sided; the $n=12$ census, two-sided; seven newly grown saturated 23-point (4,5)-sets. The test finds exactly what must be found.
- **Extension, filter and isomorphism tools** (`xr`, `fr`, igraph/BLISS with explicit verified relabellings; no nauty, no VF2). Validated against brute force.
  - **Route 4:** 552,560 → 450,606 contain $F_7$ → 87,664 violate (P3) → 14,290 in $C$. These fall into exactly the prover's 699 classes, every survivor mapped explicitly to one of them.
  - **Route 20:** 0 members of $C$.
- **Engine.** I recomputed the top level of all 25 recursive cells from the lower lists and re-enumerated all 94 directly-enumerated cells with my own build of unmodified nauty `genbg`. Every list matches the prover's as a set of classes, so the cell lists are verified by induction with my tools.

I found no mathematical or computational error. The remaining remarks are editorial.

## Dependencies

- **L011** (I11 on $C$ for $n\le22$). Accepted in referee rounds 1–3. It is used in 0.3, in the slack $\ge0$ of every component (Lemma E, 4.1, 5.1) and hence in every decomposition.
  - I did not re-prove it.
  - I probed it on fresh members of $C$: all vertex-deleted and two-vertex-deleted subgraphs of the 699 (check 8). No violation.
- **L007 Lemma D** (`enum_conn`). My checks do not rely on it: I re-enumerated every direct cell with genbg (check 6b).
- **K3–K7 [published].** They give $H(A)\in C$, $h=\alpha=n-\tau$, and the injective midpoint map that misses $\min A$ and $\max A$. Step 6.1 re-proves the last; I checked that argument.
- **K8 (Henning–Yeo) [published].** Its hypotheses are 3-uniform, linear and $F_7$-free (kb/notes/henning_yeo_2021_affine.md); no connectivity is needed. They hold for every member of $C$.
  - HY is **not needed** in the logical chain: for $m\le18$ the degree count with 0.3 already excludes the cell (check 1).
  - It is used only as the engine's rule declaring a cell trivially empty, which is valid.
- **nauty.** Not needed for completeness: `canon` outputs a faithful relabelled copy, so equal outputs imply isomorphic inputs. The counts were re-derived with BLISS (checks 5–7).

## Step-by-step audit

| Step | Content | Status |
|---|---|---|
| 0.1 | Additivity of $n,m,\tau,s$; heredity of $C$; $\tau(H)-1\le\tau(H-v)\le\tau(H)$; $m\le n-2$; $n\le2m+1$ for connected graphs | correct |
| 0.2 | I11 on $C$ for $n\le22$, any connectivity (L011) | cited; probed (check 8) |
| 0.3 | $11\tau(H-v)\le66+2(m-d)\le108<110$, so $\tau(H-v)=9$ and $d\le m-17$; slack of $H-v$ is $2m-33-2d$ | correct (re-derived; check 1) |
| 0.4–0.5 | Transfer under isomorphism; edges at a max-degree vertex: disjoint pairs, not inside an edge, endpoint degree $\le\Delta-1$; isolated endpoints allowed | correct |
| 0.6 | $m=n-2$ forces connected with no isolated vertex: $m\le n-z-2c$ | correct |
| 1 | $m\in\{19,20,21\}$; $\Delta\le2,3,4$; slacks $-3,-1,1$ | correct; HY not needed |
| 2 | $(23,19,10)$: $3m=57>46$ | correct |
| 3.1–3.4 | Lemma E and the recursion: $d\in[\lceil3m/n\rceil,D]$, $t'\in\{t-1,t\}$, $S'\ge0$, components in $\mathcal C(\cdot,\cdot,\cdot,d)$, endpoint bound $d-1$, multisets via `combinations_with_replacement`, filters (connected, $C$, $\tau=t$); induction on $m$ | correct (engine.py, route.py, decomp22.slack_cells read; checks 1, 6) |
| 3.5 | With $\tau(G)=t-1$: $\tau(H)\ge t$ iff every $(t-1)$-cover misses a pair; exclusion branching gives each $d$-set once; $F_7$ pruning sound (containment is inherited) | correct (proved; independent implementation, check 4) |
| 4.1–4.3 | Route 20: 4 decompositions; 37+227+596+4 = 864 inputs; 0 in $C$ | correct (check 5) |
| 5.1–5.3 | Route 4: 95+956+5·221+2·11 = 2,178 inputs; 552,560 / 450,606 / 87,664 / 14,290; 699 classes | correct (check 5) |
| 6.1 | Normal form: injective $\mu$, unmatched pair $=\{\varphi^{-1}\min,\varphi^{-1}\max\}$; injectivity for (4,5)-sets via $\{a,a',c',c\}$ having $\le4$ distances | correct |
| 6.2 | Lemma N: maximum principle on $S=\arg\max y$ gives $e(S)\ge\lvert S\rvert$, contradicting (P3). Also: $2I-B$ is a nonsingular M-matrix, so $\det>0$ | correct; $\det>0$ on all 27,206,877 systems (check 2) |
| 6.3 | The test (all injective $\mu$; distinct values; exactly $m$ APs) is necessary for realizability; the counts | correct (check 2) |
| 7 | Theorems 1, 2; $n_3\ge17$ from $n_2+2n_3=40$, $n_1\ge0$ | correct (check 1) |
| 8, C7 | Descriptive: decomposition counts 5; 5, 6, 20 | correct (check 1); 8.2's falsifier figures not re-derived (labelled as such) |
| Remark 5 | 14 record cells for $23\le n\le40$ with the stated slacks | correct (check 1) |

## Checks performed

All commands are run from `experiments/referee/L012-round2/`. Outputs are quoted from `logs/` or the console.

### 1. Arithmetic and decompositions (`python3 src/arith_bf.py`; `src/decomp_bf.py`)

- **Step 1.** For $m=17,\dots,21$ the feasible $(d,\tau(H-v))$ have $\tau(H-v)=9$ only. Maximum degree is $m-17$, giving 2, 3, 4 for $m=19,20,21$. $H$-slacks are $-3,-1,1$.
- **Without HY**, `3m <= n*(m-17)` holds only for `[20, 21]`.
- **Degree count** for $\Delta\le3$: vectors $(n_1,n_2,n_3)$ = (0,6,17), (1,4,18), (2,2,19), (3,0,20); min $n_3=17$.
- **Brute-force decompositions** (partition-first, connected types of $C$ with $m\le n-2$, $n\le2m+1$, $1\le\tau\le m$, slack $\ge0$, plus the isolated vertex; **no HY**):
  - $(22,17)$ slack 1: **4**, namely [AP,(19,16,8)], [(8,5,3),(14,12,6)], [(10,7,4),(12,10,5)], [(22,17,9)];
  - $(22,18)$ slack 3: 5;
  - $(22,19)$ slack 5: 2.
- **Engine branches.** Against all 119 cell files: `recursive branches checked 36, mismatches 0, branch-set differences 0`. Every $(d,t')$ with $S'\ge0$ is present, and no other.
- **Step 8 / C7 counts:** $(20,15)$ slack 2 → 5; $(18,14)$ slack 5 → 6; $(21,15)$ slack 5 → 20.
- **Remark 5:** the 14 cells (23,21,10,1) … (39,37,17,4) are reproduced exactly.

### 2. Exact realization, re-implemented (`src/rz.c`)

**Method.**
- For every pair $u<v$ and every bijection $\beta:V\setminus\{u,v\}\to E$ with $w\in\beta(w)$ (DFS over vertices by increasing degree), $\mu=\beta^{-1}$. Each injective $\mu$ arises exactly once.
- The row of vertex $w$ is $2x_w-x_a-x_c=[a=v]+[c=v]$. The matrix $2I-B$ is a Z-matrix with row sums $\ge0$. Nonsingular by Lemma N, it is a nonsingular M-matrix, so it can be eliminated without pivoting.
- **Mode f.** Elimination in floating point; $D=\mathrm{round}(\prod\text{pivots})$, $y=\mathrm{round}(Dx)$. Then an **exact integer check** of every equation, with $y_u=0$ and $y_v=D\neq0$. By Lemma N, $y/D$ is then the unique solution. On failure it falls back to mode e.
- **Mode e.** Fraction-free Bareiss in int64 with __int128 products and partial pivoting. Every division is asserted exact and overflow is asserted absent. Exact back-substitution gives $y=Dx$. The same integer check follows, and the sign of $\det$ is recorded.
- Distinctness and the 3-AP count (two pointers per middle element) are computed on the exact integers.

**The 699 classes.**
- `./out/rz 23 < out/r4_699.txt` (67 s): `TOTAL graphs=699 asg=27206877 dist=6051773 real=0 fallback=0 realizable_graphs=0`.
- `./out/rz 23 e`: identical class by class; `singular=0`, `det<=0: 0` on every class.
- Per class against the prover's `out/realize_r4_part0{0,1}.txt`: `per-class mismatches: 0`.
  - Assignments range from 22,785 to 49,606; at least 1,656 distinct-valued.
  - Minimum number of extra APs: 4 for 675 classes, 6 for 24, as stated in C5.
- `src/py_solve_check.py` (pure-Python Fractions; edge-driven enumeration as in `realize.c`; Gauss–Jordan) on classes 1, 351 and 699:
  - assignments 33,703 / 41,049 / 25,426;
  - distinct 6,588 / 10,468 / 1,656;
  - realizations 0;
  - **multiset of exact solution vectors equal to rz's: True** (all three).
- Direct test of the labelled survivors (check 5): 3,227 of 14,290 survivors, 130,944,044 assignments, 0 realizations. I stopped it as redundant, because check 5 maps every survivor explicitly onto one of the 699.

**Positive and negative controls.**
- **A_base** (`src/abase_ctrl.py`; pattern computed from the set itself): `asg=1596 dist=1413 real=948` in both modes.
  - All 948 were re-verified with Fractions (distinct values, AP set equal to the edge set).
  - They give 948 distinct normalised sets, and A_base itself is among them.
- **$n=14$ census, one-sided** (`src/census_ctrl.py 14`; patterns recomputed from the sets and checked equal to the file's): `graphs 2910, total realizations 2671044, own set found 2910`.
- **$n=14$, two-sided** (`src/census14_twosided.py`). rz on the 11 classes of `cell(14,12,6,4)`:
  - 7,896 realizations, of which 4,691 are (4,5)-sets;
  - the affine classes of the (4,5)-realizations number **2,910 and equal the L004 census**;
  - 2 classes have no realization at all.
- **$n=12$, two-sided** (`src/census_ctrl.py 12`). The 221 classes of `cell(12,10,5,4)`:
  - 83,021 realizations, of which 58,999 are (4,5)-sets;
  - 219 classes have a realization and 195 have a (4,5)-realization;
  - classes 189 and 193 (1-based) have none, and 24 have only non-(4,5) realizations;
  - the affine classes of the (4,5)-realizations number **54,243 and equal the L002 census** (`census-realized 0; realized-census 0`).
  - On 3,000 realizations, "(4,5)" was cross-checked by brute force over 4-subsets against "weak Sidon", the two being equivalent for linear AP sets.
- **New positive controls at $n=23$** (`src/grow23_ctrl.py`).
  - I grew 7 saturated 23-point (4,5)-sets, from A_base and 6 random census sets, by repeatedly adding a new extreme $2\max-a$ or $2\min-a$. Each addition keeps the set (4,5), verified by brute force, and adds exactly one AP.
  - Each has 21 APs; $\tau=7$ or 8, so none is a record.
  - Their patterns, with scrambled labels, were all realized (2,526–14,505 realizations each), and each set was recovered exactly once.
  - So the test does find realizations of 23-vertex saturated patterns when they exist.

### 3. Validation of my extension enumerator and filter

**`src/xr.c` (extension enumerator).**
- $\tau(G)$ by branching; all $(T-1)$-covers by brute force over all $(T-1)$-subsets.
- Kill search with exclusion; the branching cover is chosen *dynamically* among the first 4 alive covers (fewest available vertices outside). This is a different search tree from both `ext_d` and round 1's `rext`.
- Free mode when $\tau(G)\ge T$; no $F_7$ pruning.

**`src/fr.c` (filter).**
- Linearity.
- Centre-based $F_7$ test: the unique degree-3 vertex of $F_7$, every 3 edges at it, all 4 splittings.
- (P3) via the criterion "for every pair $\{x,y\}$ the edges have an SDR in $V\setminus\{x,y\}$", which I proved equivalent to (P3) by Hall's theorem; Kuhn augmenting paths.
- Exact $\tau$, connectivity on all $n$ vertices, maximum degree.

**Tests.**
- `src/bf_xr.py` against a Python brute force (all $d$-sets of disjoint admissible pairs, $\tau$ by subset search): 22 cases covering $d=2,3,4$, endpoint bounds 1–3, constrained and free mode, an isolated vertex and an AP component. **2,341 hits, 0 mismatches, no duplicates.**
- `src/bf_fr.py` and `src/bf_fr_dense.py`: 800 random 3-graphs on 7–9 vertices, with planted $F_7$ copies and dense linear graphs. $F_7$ by exhaustive embedding, (P3) over all subsets, $\tau$ exact. Outcomes 175 nonlinear, 269 $F_7$, 45 (P3)-violated, 311 survivors; **0 mismatches**.

### 4. Data taken from the prover

My routes and cells use only the tracked `cells.tar.gz` (component representatives), checked as follows:
- every representative used by the routes passes `fr`: in $C$, connected, stated $\tau$, $\Delta\le D$;
- the recomputations of check 6 show that the archive is internally consistent and complete.

### 5. Route 4 and route 20 (`src/build_routes.py`, `xr`, `fr`, `src/bliss_classify.py`)

**Inputs.** Rebuilt from my decompositions and the cell lists: 2,178 for route 4 and 864 for route 20. Each set is **identical** to the prover's input file.

**Route 4.** `xr 22 4 3 10 < out/route4_in.txt | fr 23 print` (118 s):
- `XRSUMMARY graphs=2178 free=0 low=0 hits=552560 nodes=1820667548 maxcovers=2418`, so every input has $\tau=9$;
- `FRSUMMARY total=552560 nonlinear=0 F7=450606 P3violated=87664 survivors=14290 connected=14290 tau=[10,10] maxdeg=[4,4]`.

**Isomorphism classes** (BLISS via igraph, with colour classes).
- For every graph I take the relabelling that actually maps it onto its canonical form, determined convention-independently by checking both $p$ and $p^{-1}$.
- Equal keys then give an **explicit isomorphism, which is verified**.
- Invariance was tested on 150 random relabellings.
- Result: `representatives 699, distinct BLISS classes 699`; `graphs 14290, matched 14290, unmatched 0, failed explicit verification 0, representatives hit 699 of 699`.
- So, given the cell lists, Theorem 3(a) holds exactly, and check 2 covers every graph my pipeline produced.

**Route 20.** `xr 22 3 2 10 | fr 23`: `hits=128`; `F7=44 P3violated=84 survivors=0`. Theorem 2 holds given the cells.

### 6. The engine's class lists

**(a) Top level of all 25 recursive cells** (`src/recompute_cell.py`, `src/run_all_rec.sh`; `logs/run_all_rec.log`).
- For each cell: every $(d,t')$ branch, my decompositions, inputs from the prover's next-lower lists (my code), `xr`, `fr`, BLISS classes.
- Compared with the prover's list both ways, with explicit maps: **25 of 25 identical; no lower list missing; no errors.**
- Branch counts that match the prover's log:
  - (22,17,9,4): $d=3$: 14,241 inputs, 163,773 extensions, 29,919 $F_7$-free, 27,322 in $C$. $d=4$: 261 inputs, 464,451 / 130,912 / 115,270. 3,778 connected → **95**.
  - (19,16,8,4): $d=3$: 6,085 / 4,649. $d=4$: 26,452 / 14,038. 18,687 connected → **956**.
- Other cells:

| Cell | Connected survivors → classes |
|---|---|
| (22,17,9,3) | 1,114 → 37 |
| (19,16,8,3) | 4,649 → 227 |
| (21,14,8,3) | 13,264 → 299 |
| (18,13,7,3) | 62,050 → 2,544 |
| (15,12,6,3) | 141,212 → 10,617 |
| (14,12,6,4) | 167 → 11 |
| (14,12,6,3) | 17 → 2 |
| (15,11,6,4) | 1,052 → 30 |
| (15,11,6,3) | 440 → 19 |
| (20,11,7,3) | 5,317 → 45 |
| (17,13,7,3) | 113 → 6 |
| (17,11,6,2) | 2,644 → 114 |
| (20,12,7,2) | 1,242 → 38 |
| (19,12,7,2) | 11 → 1 |
| (20,11,7,2) | 55 → 1 |

- The empty cells (21,13,8,4), (18,12,7,4), (20,14,8,3), (19,11,7,3), (18,12,7,2), (19,11,7,2), (15,11,6,2) and (16,11,6,2) are reproduced as empty.

**(b) All 94 directly-enumerated cells by genbg** (`src/genbg_check.py`; `logs/genbg_all.log`).
- `out/genbg` was built by me from the unmodified nauty 2.8.8 sources.
- Command: `genbg -q -c -Z1 -d1:3 -D<D>:3 n m 3m:3m`. Here `-Z1` says two edge-vertices share at most 1 neighbour, which is linearity. Output goes through my graph6 decoder, then `fr` ($C$, $\tau=t$, connected, $\Delta\le D$), then BLISS.
- Results: **82 cells equal (3,104 classes), 12 trivially empty ($3m>Dn$; prover count 0), 0 timeouts, 0 mismatches.**
  - Examples: (12,10,5,4) 94,633 graphs → 221; (12,10,5,3) → 149; (10,7,4,4) → 5; (8,5,3,4) → 2; (17,10,6,3) 142,142 → 339; (14,9,5,3) 24,468 → 1,060; (11,8,4,3) 895 → 471; (19,10,6,2) → 128.

With (a), by induction on $m$, every list used by routes 4 and 20 is reproduced by my tools. My tools use no nauty canonical form, only nauty's generator `genbg` for the base cells.

### 7. The prover's `canon` (`src/canon_check.py`)

- On the 699 and on the lists of `cell(19,16,8,4)` and `cell(12,10,5,4)`, with 3 random relabellings each (5,628 graphs): **0 invariance failures**.
- Every output is BLISS-isomorphic to its input, so the output is a faithful relabelled copy.
- The number of distinct outputs equals the list sizes.
- Degree statistics of the 699:
  - 2, 3 or 4 vertices of degree 4 in 227, 402 and 70 classes;
  - 1 or 2 vertices of degree 1 in 630 and 69 classes;
  - 6 degree patterns, as in C4.

### 8. Probe of the dependency I11 (`src/i11_probe.py`)

Every $H-v$ and $H-\{v,w\}$ of the 699 is in $C$ (hereditary), with 22 or 21 vertices.
- $H-v$: 16,077 graphs, all in $C$, $\tau=9$ for every one, min slack 1, **0 I11 violations**.
- $H-\{v,w\}$: 176,847 graphs, $\tau\in\{8,9\}$, min slack 0, **0 violations**.

This is consistent with L011. It is not a proof of it.

## Problems found (in order of severity)

No error affecting Theorems 1–3, Remark 4 or Remark 5 was found. The items below are editorial and need no further review.

1. **Residual "conditional" wording (editorial; resolved in d6d4fa8).** The round-1 fix updated the DEPENDS ON line to "no longer conditional (L011 is ACCEPTED x3)". The Tags line still reads "Theorems 1–3 **[verified-here] conditional on referee acceptance of this certificate and of L011**". The condition on L011 is met, so the two lines should be made consistent when the result is recorded. The current version (d6d4fa8) has already done this: its Tags line reads "[verified-here] (L011 is ACCEPTED x3; …)". No action is left.
2. **The role of nauty is overstated (clarification, as in round 1).** The CLAIM-TYPE header and Step 3.4 call the canonical forms load-bearing for completeness. They are not: `canon` prints the graph relabelled by nauty's labelling, so equal outputs imply isomorphic inputs whatever nauty does, and de-duplication cannot lose a class. Canonicity matters only for the exact counts (699, 95, 956, …). Those are now confirmed with BLISS (checks 5–7) as well as VF2 (round 1).
3. **HY is not needed (optional remark).** Step 1 derives $m\ge19$ from K8. The degree bound 0.3 alone already excludes $m\le18$: for $m\le16$ no vertex can satisfy $d\le m-17$; for $m=17,18$ we get $3m>23(m-17)$. HY enters only as the engine's valid trivially-empty rule. Saying so would make the dependency list shorter.
4. **Lift in 6.3 (optional, as in round 1).** Hadamard gives $\lvert D\rvert,\lvert y_i\rvert\le6^{21/2}<1.5\cdot10^8\ll p/2$, so the symmetric lift is correct a priori. The a-posteriori integer check already makes the computation rigorous.
5. **Scope (no action).** The figures in Step 8.2 are the falsifier's and are not re-derived; the proof labels them so. The maximum-degree-3 case stays open, as Remark 4 says. Nothing is claimed for $n\ge24$.
