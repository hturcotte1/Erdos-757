# experiments/prover/L025: the E1-hub (b-configuration) lemma, I11 form

Certificate: results/proofs/L025-e1hub-lemma-i11-form.md (submitted 2026-10-27, unrefereed).

## Question
SYNTHESIS.md (experiments/prover/panel-synthesis/) Section 3, I11 form: for a connected $G\in C$ with $\Delta\le3$,
slack $s(G)\le1$ and I11 below $n(G)+4$, and $a,b,c$ of degree $\le2$ with $\{a,b,c\}$ not an edge, does some minimum
transversal of $G$ contain two of $a,b,c$ (equivalently, does the E1-hub $G\oplus(a,b,c)$ satisfy I11)?

## Result (proved in the certificate, unrefereed; tags there)
- Theorem 10: given I11 up to $n(G)+2$ vertices, every b-configuration of a connected $G\in C$ with $s(G)\le1$ is a
  *pendant triple* (three degree-1 vertices in three different edges) and forces $s(G)=1$. So the I11 form holds for
  tight $G$ (statement B0 of the synthesis, for every $n$) and for every outer triple that is not a pendant triple.
- Corollary 11(b): an E1-hub in a minimal counterexample $H$ has a connected outer graph $G'$, $s(H)=-1$, and outer
  vertices of $H$-degree 2.
- Theorem 12: structure of the pendant case: $G''=G-\{a,b,c\}$ is connected with slack 8, the six other vertices of the
  three pendant edges are distinct, of $G''$-degree 1 or 2, and avoided by every minimum transversal of $G''$; every
  edge-adding gadget (an edge on three avoided vertices, identifications, moves) would give a smaller violator and is
  blocked only by an $F_7$ through the new edge or by a tight set ($e(S)=|S|-2$) of $G''$.
- NOT proved: the pendant case itself (GAP in the certificate). It is not a finite computation.

The key mechanism: "compression gadgets". A pairwise non-co-transversal triple can be replaced by smaller graphs whose
transversal numbers are forced by the NC conditions: the fold $G\oplus^\circ(a,b|c)$ (slack $-1$), the pendant
replacement $(G-c)+\{w,a,b\}$ (slack $+2-2d(c)$), the identification $G_{a=b}$ and the move $(G-a)+\{a_1,b,c\}$ (slack
$-3$), an edge on three avoided vertices (slack $-9$). Each one that stays in $C$ contradicts I11 below; the first two
always stay in $C$ and kill every non-pendant case.

## Files (own code; no import of e757/, judge/ or other L0xx code)
- `hyp25.py`: hypergraph utilities (linearity, $F_7$ test, (P3) by per-pair SDR, exact branch-and-bound $\tau$, all
  minimum transversals by bitmask enumeration, co-transversal pairs, hub/identify/delete builders). Written for this
  certificate (first session 07:58-08:17 UTC, before the rate-limit interruption; reviewed and reused).
- `lemmas25.py`: the tests C2 (Lemmas 1-9 and the rules R1-R3 and the fold rule of Theorem 10) with a fast (P3) test
  `p3_fast` (one SDR, then per pair only the two displaced edges are re-routed).
- `p3check.py`: C1, cross-check of `p3_fast` against `hyp25.p3`.
- `w1_pendant.py`: W1, pendant b-configurations built on stored classes (consistency test of Theorem 10 and Remark 10.3).
- `run_c2.sh`, `run_w1.sh`, `run_w1b.sh`: the exact command sequences of the runs (sequential, `timeout`, `nice -n 10`).
- `pendants.py` → `pendants_output.txt`: number of degree-1 vertices in the stored near-tight classes (evidence for Conjecture P2$^+$).
- `census.py`, `census2.py`, `census_one.py`: C3, b-configurations and NC-pair types in stored lists.
- `lemma_tests.py` (with test_crit_output.txt, test_nc_near_output.txt): earlier exploratory tests from the first session
  (identification, pendant gadget, edge-criticality); superseded by `lemmas25.py`, kept for the record.

## Commands and outputs (all under `timeout ... nice -n 10`, one process)
Run from this folder.
- C1: `python3 p3check.py` → `p3check_output.txt`:
  `p3 cross-check graphs 1854 P3-violating 652 mismatches 0`.
- C2 (near-tight lists, 483 classes): `python3 lemmas25.py near --hubsample 30` → `lemmas_near_output.txt`:
  `{'classes': 483, 'L1': 12581, 'L2': 28430, 'L3': 6, 'L4': 0, 'L4_drop1': 0, 'L5': 258, 'L6': 2, 'L6_inC': 0, 'L7': 6, 'L7_inC': 0, 'L8': 0, 'L8_inC': 0, 'L9': 0, 'bconf': 0} failures 0`.
- C2 (slack-2 lists; run by `run_c2.sh`, per-cell cumulative counters): `python3 lemmas25.py file:<inputs>/cell_6_3_2.txt ... --hubsample 10`
  → `lemmas_slack2_output.txt`: cells (6,3,2), (9,4,3), (10,8,4), (13,9,5), (16,10,6), (23,16,9), (20,15,8): 1,296 classes,
  L1 12,924, L2 31,808, L3 164, L4 21, L5 4,180, L6 28 (none in C), L7 208 (none in C), b-configurations 7, failures 0.
  Its output for the last cell (17,14,7) and the TOTAL line were lost (the tracked output file was replaced under the
  running process by another agent's `git pull --rebase --autostash`); that cell was re-run by `run_w1.sh` →
  `lemmas_slack2_17_14_7_output.txt`: 1,708 classes, L1 17,080, L2 39,112, L3 102, L5 1,411, L6 48 (none in C),
  L7 102 (none in C), no b-configuration, failures 0. Later runs (`run_w1b.sh`) write to a scratch folder outside the
  repository and are copied here afterwards.
- C2 (higher-slack L013 cells; `run_c2.sh`): (11,6,4) [empty file], (12,6,4), (13,6,4), (11,7,4), (14,7,5), (15,8,5), (18,9,6),
  (19,12,7), (12,7,4), (13,8,5), all D3 → `lemmas_highslack_output.txt`: 1,053 classes, L1 10,530, L2 25,939, L3 6,826,
  L4 3,201 (2,303 with $\tau(G-a-b-c)=\tau-1$, all with $s\ge2|\partial|-2$), L5 12,444, L6 812 (707 in C, all at slack $\ge3$),
  L7 8,192 (3,817 in C), L8 0 (no three avoided vertices in these cells), 1,122 b-configurations checked against R1-R3 and
  the fold rule, failures 0.
- C2 (slack-8/9 cells (5,2,1), (7,5,2), (10,6,3), (13,7,4), (16,8,5), (19,9,6), for Lemma 6, which needs three avoided
  vertices; `run_w1b.sh`) → `lemmas_slack89_output.txt`.
- W1 (`run_w1b.sh`): `python3 w1_pendant.py <13 cells of slack 9, 8, 7>` → `w1_output.txt`.
- C3: `python3 census.py` → `census_near_output.txt`; `python3 census2.py n m t 4` for the slack-2 cells →
  `census2_slack2_small_output.txt`, `census2_slack2_big_output.txt`.

Counter names in the C2 output: L1 hub triples, L2 fold orientations, L3 pendant replacements, L4 deletions of
b-configurations (L4_drop1: those with $\tau(G-a-b-c)=\tau-1$), L5 NC pairs (pair lemma), L6 identifications (L6_inC: in
$C$), L7 moves (L7_inC), L8 avoided triples (L8_inC: pairwise non-adjacent and in $C$; an 'L8-I11' failure would be an I11
violation), L9 b-configurations checked against the rules, bconf b-configurations found. "failures 0" means every
identity held and no rule was violated.

## Suggested computations (they test, but cannot close, the GAP)
- W1: among stored connected cells of slack 8 (or any slack) with at most 26 vertices, search for three pairwise disjoint
  2-sets inside no edge, whose six vertices are avoided and such that every transversal meeting all three has
  $\ge\tau+2$ vertices (Theorem 12(a)); by Remark 10.3 none can exist with at most 22 vertices, so a hit there would
  refute a step of the certificate.
- W2: a falsifier for the pendant case at $24\le n(G'')\le40$: glue stored slack-$\le4$ pieces along six attachment
  vertices and test Theorem 12(a); any $G''$ found gives an I11 violator $G''+$pendants$\oplus(a,b,c)$ or a smaller one.
