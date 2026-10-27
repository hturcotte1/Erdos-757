
## GAPs as marked, and whether anything outside them is unproved

The certificate marks four GAPs. I agree with each description.
- **G1: impure configurations.**
  - (D1) with H - v = F + G', G' non-empty;
  - (D2) with H - v strictly containing F_1 + F_2;
  - (D3).
  - The free-hub accounting gives exactly A(H) >= A(G') - W(F). This is balanced, so it yields no contradiction.
- **G2: Claim H in the exceptional cases.** The replacement leaves C_3, or |X| is small for the given boundary size. For |∂(X)| = 0 and |X| <= 5 there is a finite check, not done. Item 8 above narrows G2.
- **G3: degree-2 vertices.** Deleting such a vertex costs exactly 35, so Theorem 4 gives nothing there beyond co-transversality.
- **G4: the special family outside n <= 24.** This is KT* itself, as the certificate says.

Consequently KT* and c* >= 35/66 are not proved, and the certificate says so in its CLAIM-TYPE line and in the GAP section.

Outside G1 to G4, I found only two things that are not proved as written:
- the missing case in the proof of Theorem 7(v) (item 1; the statement is true by L016);
- the unqualified remark on saturated graphs for n >= 28 (item 2; not used anywhere).

Everything else presented as proved is proved. This covers Theorems 1 to 6, Propositions 8 and 9, Theorem 7(i) to (iv), and the "Closes" list of the GAP section.

## Independence statement

Before writing this review I did not read any other review of L021. I read section 1 (on L021) and the header of experiments/prover/panel-synthesis/SYNTHESIS.md, as the task instructed. I verified each of its points myself:
- the sign typo;
- the 32-pieces overstatement;
- the KT*/I11 labelling;
- its observation (b) on G2.

I did not look inside experiments/referee/L021/, which belongs to someone else.

My scripts in experiments/referee/L021-round1-ref1/ import neither experiments/prover/L021/kt.py nor e757 nor judge/:
- rcore.py, the core module: CP-SAT integer programs for tau and DEF; VF2 subgraph monomorphisms of typed incidence graphs plus an induced-edge count for the copies; brute-force minimum transversals; class-C tests by pairs, an explicit F7 search and (P3) by Hall matchings;
- check1.py to check5.py.

They read only:
- the cell lists that I re-extracted from the refereed tarballs;
- the edge lists of the 32 pieces in closure_results.json, which check1 re-derives from scratch.

The prover's own scripts were re-run only as copies in prover_rerun/, with their output paths redirected, so that no file outside my scratch folder and this review was written.
